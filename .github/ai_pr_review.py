#!/usr/bin/env python3
"""AI PR review — runs inside GitHub Actions, reviews a PR diff with Claude.

Pipeline (todos/20260705-ai-loop-subagent-tasks.md §T5):

    read diff  ->  call Claude (structured P0/P1/P2)  ->  parse verdict
               ->  post PR comment  ->  label `ai-review-passed` when clean
               ->  optionally approve one trusted author when clean

Hard constraints (codex-adopted, see the workflow header comment for the WHY):

  * Auto-approve is narrowly gated: only the configured trusted PR author can be
    approved, only when there are zero P0 findings, and only when a separate
    approver token is present.
  * Budget guardrails: a daily USD spend cap, a per-review token cap, and a
    max-retries cap. Breaching the daily cap raises a Feishu alert (dry-run by
    default) and records a row in agent_runs when a local brain.db is reachable.
  * ZERO secrets in logs. The Anthropic key is read from the environment and is
    never printed, echoed, or embedded in the comment.

The script is self-contained: it talks to the Anthropic API over raw HTTPS
(stdlib only) so the CI step needs no third-party install. Comment posting and
labeling go through the GitHub REST API using the Actions-provided GITHUB_TOKEN.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# ── Model + pricing ──────────────────────────────────────────────────────────
# PR review is a bounded, high-volume task -> Sonnet 4.6 is the cost/quality pick
# (claude-api skill: balanced speed/intelligence for production workloads).
MODEL = "claude-sonnet-4-6"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
# $/1M tokens (claude-api skill cached table, 2026-05-26).
PRICE_IN_PER_MTOK = 3.00
PRICE_OUT_PER_MTOK = 15.00

AGENT_NAME = "github-pr-review"
PASS_LABEL = "ai-review-passed"
DEFAULT_TRUSTED_AUTHORS = ""

# ── Budget guardrails (overridable via env in the workflow) ──────────────────
DEFAULT_DAILY_USD_CAP = 10.00     # cumulative spend ceiling for this agent
DEFAULT_MAX_TOKENS = 4000         # per-review output cap (a review is short)
DEFAULT_MAX_RETRIES = 3           # Anthropic call attempts before giving up
DIFF_CHAR_BUDGET = 200_000        # ~50k tokens of diff; truncate beyond this

SYSTEM_PROMPT = """You are a senior engineer doing a pre-merge review of a pull \
request for the Rozo project (cross-chain USDC / stablecoin payment \
infrastructure). Review ONLY the provided diff. Be specific and concise; cite \
file:line where possible.

Classify every finding into exactly one severity:
  P0 = must fix before merge. Leaked secret / private key / mnemonic / API key / \
JWT in code or logs; a weakened or removed Supabase RLS policy; a public edge \
function deploy missing --no-verify-jwt; a write (INSERT/UPDATE/DELETE) to a \
read-only mirror table (rozo_payments, rozo_users, rozo_merchants, \
rozo_developers, analytics_*); payment / payout / withdrawal logic changed with \
zero test coverage; a blacklisted wallet address used as a receiver.
  P1 = should fix: real bug, security weakness, missing error handling, \
incorrect logic, or a meaningful test gap.
  P2 = nice to have: style, naming, minor cleanup, readability.

Report EVERY finding you have, including low-confidence ones — a downstream gate \
decides what blocks. Do not self-filter for importance.

Return your review as GitHub-flavored markdown with three sections in this exact \
order and with these exact headings:

## P0 (blocking)
## P1 (should fix)
## P2 (nice to have)

Under each heading, list findings as markdown bullets. If a section has no \
findings, write the single line `_None._` under it. Do not add any other \
top-level headings."""


# ── small utils ──────────────────────────────────────────────────────────────

def eprint(*a: object) -> None:
    print(*a, file=sys.stderr)


def now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def estimate_cost(usage: dict) -> float:
    """USD estimate from an Anthropic usage block."""
    in_tok = (usage.get("input_tokens", 0) or 0) + (usage.get("cache_read_input_tokens", 0) or 0)
    out_tok = usage.get("output_tokens", 0) or 0
    return in_tok / 1_000_000 * PRICE_IN_PER_MTOK + out_tok / 1_000_000 * PRICE_OUT_PER_MTOK


# ── Anthropic call (raw HTTPS, retries, never logs the key) ──────────────────

class BudgetExceeded(Exception):
    """Raised when a hard budget cap is hit before/after the model call."""


def call_claude(api_key: str, diff: str, *, max_tokens: int, max_retries: int) -> dict:
    """Return {"text": str, "usage": dict}. Retries on 429/5xx with backoff.

    The api_key is only ever placed in the request header. It is NEVER logged.
    """
    if len(diff) > DIFF_CHAR_BUDGET:
        diff = diff[:DIFF_CHAR_BUDGET] + "\n\n[... diff truncated for length ...]"

    body = json.dumps({
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": f"Review this diff:\n\n{diff}"}],
    }).encode("utf-8")

    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        req = urllib.request.Request(
            ANTHROPIC_URL,
            data=body,
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,               # header only — never printed
                "anthropic-version": ANTHROPIC_VERSION,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            text = "".join(
                b.get("text", "") for b in payload.get("content", []) if b.get("type") == "text"
            )
            return {"text": text, "usage": payload.get("usage", {})}
        except urllib.error.HTTPError as e:
            status = e.code
            # Do NOT dump the response body verbatim — keep error logs terse and
            # secret-free. 4xx (except 429) is not retryable.
            if status == 429 or status >= 500:
                last_err = RuntimeError(f"Anthropic HTTP {status} (attempt {attempt}/{max_retries})")
                eprint(str(last_err))
                if attempt < max_retries:
                    time.sleep(min(2 ** attempt, 30))
                    continue
            else:
                raise RuntimeError(f"Anthropic HTTP {status} — non-retryable") from None
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = RuntimeError(f"Anthropic connection error (attempt {attempt}/{max_retries}): {type(e).__name__}")
            eprint(str(last_err))
            if attempt < max_retries:
                time.sleep(min(2 ** attempt, 30))
                continue
    raise RuntimeError(f"Anthropic call failed after {max_retries} attempts: {last_err}")


# ── verdict parsing ──────────────────────────────────────────────────────────

_SECTION_RE = re.compile(r"^##\s*(P[012])\b", re.IGNORECASE | re.MULTILINE)


def parse_findings(review_md: str) -> dict[str, list[str]]:
    """Split the markdown into {P0,P1,P2} -> [finding lines].

    Robust to the model omitting a heading: missing sections become empty.
    A section whose only content is `_None._` (case-insensitive) is empty.
    """
    findings: dict[str, list[str]] = {"P0": [], "P1": [], "P2": []}
    matches = list(_SECTION_RE.finditer(review_md))
    for i, m in enumerate(matches):
        sev = m.group(1).upper()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(review_md)
        block = review_md[start:end]
        for line in block.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.lower().strip("_. ") == "none":
                continue
            if s.startswith(("-", "*", "•")) or re.match(r"^\d+\.", s):
                findings[sev].append(s.lstrip("-*• ").strip())
    return findings


def verdict_from_findings(findings: dict[str, list[str]]) -> str:
    """clean | block. block only on P0 (P1/P2 do not gate — comment only)."""
    return "block" if findings["P0"] else "clean"


def build_comment(review_md: str, findings: dict[str, list[str]], verdict: str) -> str:
    counts = {k: len(v) for k, v in findings.items()}
    if verdict == "clean":
        header = (
            f"### AI review: {counts['P0']} P0 / {counts['P1']} P1 / {counts['P2']} P2 "
            f"— no blocking issues found\n"
            f"Labeled `{PASS_LABEL}`. This is advisory; a human still merges."
        )
    else:
        header = (
            f"### AI review: {counts['P0']} P0 (blocking) / {counts['P1']} P1 / "
            f"{counts['P2']} P2\n"
            f"P0 findings must be addressed before merge. This is advisory — no "
            f"auto-approve, no auto-block; a human decides."
        )
    return f"{header}\n\n{review_md.strip()}\n\n<sub>ai-pr-review · {MODEL}</sub>"


# ── GitHub REST (uses the Actions GITHUB_TOKEN; no PAT) ──────────────────────

def gh_request(method: str, url: str, token: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "authorization": f"Bearer {token}",     # header only — never printed
            "accept": "application/vnd.github+json",
            "content-type": "application/json",
            "user-agent": "ai-pr-review",
        },
        method=method,
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def post_comment(repo: str, pr: int, token: str, comment: str) -> None:
    gh_request(
        "POST",
        f"https://api.github.com/repos/{repo}/issues/{pr}/comments",
        token,
        {"body": comment},
    )


def add_label(repo: str, pr: int, token: str, label: str) -> None:
    try:
        gh_request(
            "POST",
            f"https://api.github.com/repos/{repo}/issues/{pr}/labels",
            token,
            {"labels": [label]},
        )
    except urllib.error.HTTPError as e:
        # Label may not exist yet in a fresh repo — create then retry once.
        if e.code in (404, 422):
            try:
                gh_request(
                    "POST",
                    f"https://api.github.com/repos/{repo}/labels",
                    token,
                    {"name": label, "color": "0e8a16",
                     "description": "AI PR review found no blocking issues"},
                )
            except urllib.error.HTTPError:
                pass  # already exists / race — fine
            gh_request(
                "POST",
                f"https://api.github.com/repos/{repo}/issues/{pr}/labels",
                token,
                {"labels": [label]},
            )
        else:
            raise


def submit_approval(repo: str, pr: int, token: str, body: str) -> None:
    gh_request(
        "POST",
        f"https://api.github.com/repos/{repo}/pulls/{pr}/reviews",
        token,
        {"event": "APPROVE", "body": body},
    )


# ── budget alerting: Feishu (dry-run) + local agent_runs (best-effort) ───────

def _project_root_for_brain() -> Path | None:
    """Find a local ainative checkout with brain.db + scripts, if reachable.

    In CI this returns None (no brain.db in the reviewed repo) — the run metadata
    is emitted as JSON to stdout/step-summary instead, for a later local sync.
    """
    env = os.environ.get("AINATIVE_ROOT")
    candidates = [Path(env)] if env else []
    candidates.append(Path(__file__).resolve().parents[3])  # if run from ainative repo
    for c in candidates:
        if (c / ".ainative" / "brain.db").exists() and (c / "scripts" / "agent_runs_lib.py").exists():
            return c
    return None


def raise_budget_alert(cost: float, cap: float, *, send: bool) -> None:
    """Feishu alert (dry-run by default) that the daily cap was breached."""
    title = f"agent {AGENT_NAME} 成本超限"
    text = (f"{AGENT_NAME} 累计成本估算 ${cost:.2f} 超过日上限 ${cap:.2f}，"
            f"PR review 已停跑，请检查是否失控。")
    root = _project_root_for_brain()
    if root is not None:
        notify = root / "scripts" / "notify_feishu.py"
        cmd = [sys.executable, str(notify), "--title", title, "--text", text,
               "--severity", "warning"]
        if not send:
            cmd.append("--dry-run")
        import subprocess
        subprocess.run(cmd, check=False)
    else:
        # CI path: no notify script reachable — print the alert so it lands in the
        # workflow log and the step summary. A local sync can forward it.
        prefix = "FEISHU-ALERT (dry-run)" if not send else "FEISHU-ALERT"
        print(f"{prefix}: {title} — {text}")


def record_run_local(success: bool, *, error: str | None, cost: float) -> bool:
    """Best-effort: log this run into local brain.db agent_runs. Returns True if written."""
    root = _project_root_for_brain()
    if root is None:
        return False
    sys.path.insert(0, str(root / "scripts"))
    try:
        from agent_runs_lib import record_run  # type: ignore
        record_run(AGENT_NAME, success, error=error, cost=cost)
        return True
    except Exception as e:  # never let telemetry crash the review
        eprint(f"agent_runs record skipped: {type(e).__name__}")
        return False


def read_prior_cumulative_cost() -> float:
    """Read this agent's cumulative cost_estimate from a local brain.db, else 0.

    In CI there is no local brain.db, so the daily cap is enforced against the
    per-run cost plus whatever the workflow carries in AGENT_PRIOR_COST_USD (set
    from a cached artifact). Falls back to 0.0.
    """
    env = os.environ.get("AGENT_PRIOR_COST_USD")
    if env:
        try:
            return float(env)
        except ValueError:
            pass
    root = _project_root_for_brain()
    if root is None:
        return 0.0
    sys.path.insert(0, str(root / "scripts"))
    try:
        from agent_runs_lib import connect  # type: ignore
        with connect() as c:
            row = c.execute(
                "SELECT cost_estimate FROM agent_runs WHERE agent_name = ?",
                (AGENT_NAME,),
            ).fetchone()
        return float(row["cost_estimate"]) if row else 0.0
    except Exception:
        return 0.0


# ── step summary + outputs ───────────────────────────────────────────────────

def write_step_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def set_output(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="AI PR review with budget guardrails.")
    ap.add_argument("--diff-file", required=True, help="path to the unified diff")
    ap.add_argument("--repo", help="owner/repo (env GITHUB_REPOSITORY)")
    ap.add_argument("--pr", type=int, help="PR number (env PR_NUMBER)")
    ap.add_argument("--dry-run", action="store_true",
                    help="mock the Claude call + do not post to GitHub (local test)")
    ap.add_argument("--mock-response", help="path to a canned review markdown (with --dry-run)")
    ap.add_argument("--force-budget-exceeded", action="store_true",
                    help="simulate a daily-cap breach to exercise the alert path")
    ap.add_argument("--send-alert", action="store_true",
                    help="actually send the Feishu alert (default: dry-run print)")
    ap.add_argument("--trusted-authors",
                    default=os.environ.get("AI_REVIEW_TRUSTED_AUTHORS", DEFAULT_TRUSTED_AUTHORS),
                    help="comma-separated GitHub logins eligible for clean auto-approval")
    args = ap.parse_args()

    repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
    pr = args.pr or (int(os.environ["PR_NUMBER"]) if os.environ.get("PR_NUMBER") else 0)
    pr_author = os.environ.get("PR_AUTHOR", "")
    trusted_authors = {a.strip().lower() for a in args.trusted_authors.split(",") if a.strip()}

    daily_cap = float(os.environ.get("AI_REVIEW_DAILY_USD_CAP", DEFAULT_DAILY_USD_CAP))
    max_tokens = int(os.environ.get("AI_REVIEW_MAX_TOKENS", DEFAULT_MAX_TOKENS))
    max_retries = int(os.environ.get("AI_REVIEW_MAX_RETRIES", DEFAULT_MAX_RETRIES))

    diff = Path(args.diff_file).read_text(encoding="utf-8", errors="replace")
    if not diff.strip():
        print("Empty diff — nothing to review.")
        write_step_summary("AI review: empty diff, skipped.")
        return 0

    # ── budget pre-check ─────────────────────────────────────────────────────
    prior_cost = read_prior_cumulative_cost()
    if args.force_budget_exceeded or prior_cost >= daily_cap:
        cost_for_alert = daily_cap + 0.01 if args.force_budget_exceeded else prior_cost
        raise_budget_alert(cost_for_alert, daily_cap, send=args.send_alert)
        record_run_local(False, error="daily budget cap exceeded", cost=0.0)
        msg = (f"AI review skipped: daily cost cap ${daily_cap:.2f} reached "
               f"(cumulative ${cost_for_alert:.2f}). Feishu alerted.")
        print(msg)
        write_step_summary(msg)
        set_output("verdict", "skipped-budget")
        return 0  # non-fatal: don't fail the PR, just skip the review

    # ── the review ───────────────────────────────────────────────────────────
    if args.dry_run:
        if args.mock_response:
            review_md = Path(args.mock_response).read_text(encoding="utf-8")
        else:
            review_md = ("## P0 (blocking)\n_None._\n\n## P1 (should fix)\n"
                         "- Example P1 finding for dry-run.\n\n## P2 (nice to have)\n"
                         "- Example P2 nit for dry-run.")
        usage = {"input_tokens": 1200, "output_tokens": 300}
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            eprint("ANTHROPIC_API_KEY not set — cannot run review.")
            return 1
        try:
            result = call_claude(api_key, diff, max_tokens=max_tokens, max_retries=max_retries)
        except Exception as e:  # network / API failure -> record + fail soft
            err = f"{type(e).__name__}: {e}"
            eprint(f"Review call failed: {err}")
            record_run_local(False, error=err, cost=0.0)
            write_step_summary(f"AI review failed: {err}")
            return 1
        review_md = result["text"]
        usage = result["usage"]

    cost = estimate_cost(usage)
    findings = parse_findings(review_md)
    verdict = verdict_from_findings(findings)
    comment = build_comment(review_md, findings, verdict)

    # ── post + label ─────────────────────────────────────────────────────────
    if args.dry_run:
        print("── dry-run: would post this PR comment ──")
        print(comment)
        print(f"── verdict={verdict}  cost=${cost:.4f}  "
              f"P0={len(findings['P0'])} P1={len(findings['P1'])} P2={len(findings['P2'])} ──")
    else:
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token or not repo or not pr:
            eprint("Missing GITHUB_TOKEN / repo / pr — cannot post.")
            record_run_local(False, error="missing gh context", cost=cost)
            return 1
        post_comment(repo, pr, token, comment)
        if verdict == "clean":
            add_label(repo, pr, token, PASS_LABEL)
            if pr_author.lower() in trusted_authors:
                approver_token = os.environ.get("AI_REVIEW_APPROVER_TOKEN", "")
                if approver_token:
                    submit_approval(
                        repo,
                        pr,
                        approver_token,
                        "AI review found no P0 blockers for a trusted Rozo contributor.",
                    )
                    set_output("trusted_auto_approve", "approved")
                    write_step_summary(
                        "Trusted-author auto-approve submitted."
                    )
                else:
                    set_output("trusted_auto_approve", "skipped-no-token")
                    write_step_summary(
                        "Trusted-author auto-approve skipped: "
                        "`AI_REVIEW_APPROVER_TOKEN` is not configured."
                    )
            else:
                set_output("trusted_auto_approve", "skipped-author")
        else:
            set_output("trusted_auto_approve", "skipped-p0")

    # ── budget post-check + telemetry ────────────────────────────────────────
    new_cumulative = prior_cost + cost
    record_run_local(True, error=None, cost=cost)
    if new_cumulative > daily_cap:
        raise_budget_alert(new_cumulative, daily_cap, send=args.send_alert)

    set_output("verdict", verdict)
    set_output("cost_usd", f"{cost:.4f}")
    set_output("cumulative_cost_usd", f"{new_cumulative:.4f}")
    write_step_summary(
        f"AI review: **{verdict}** — P0={len(findings['P0'])} "
        f"P1={len(findings['P1'])} P2={len(findings['P2'])} · "
        f"est. cost ${cost:.4f} (cumulative ${new_cumulative:.4f} / cap ${daily_cap:.2f})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
