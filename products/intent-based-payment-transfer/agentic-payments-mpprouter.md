---
description: >-
  Pay-per-call for AI agents. Call 402-gated HTTP APIs and settle automatically
  in Stellar USDC via MPP Router.
icon: robot
---

# Agentic Payments with MPP Router

Agentic payments let AI agents spend Stellar USDC to call paid HTTP APIs — no API keys, no subscriptions, no credit card on file. The agent makes a request, the server returns `402 Payment Required` with a Stellar payment challenge, the agent signs with its wallet, retries the request, and receives the response.

ROZO's agentic payment stack runs on **Stellar mainnet** via [MPP Router](https://www.mpprouter.dev) — a Stellar-native 402 proxy that accepts Stellar USDC and forwards the request to upstream merchants (Parallel.ai, Exa, Firecrawl, OpenRouter, and more).

## Why Stellar for agentic payments

- **Sub-cent fees.** Each 402-gated call settles for fractions of a cent, making microtransactions practical.
- **Fast finality.** Stellar closes ledgers every ~5 seconds, so the 402 → pay → retry loop completes in one round trip.
- **Sponsored transactions.** The agent's wallet does not need XLM for fees — MPP Router sponsors the fee payer.
- **One stablecoin balance, many APIs.** You hold USDC on Stellar once and spend it across dozens of upstream services — no need to fund Base, Tron, or Solana.

## The flow

```
Agent                           Server (402-gated)
  │                                      │
  │ ───── 1. POST /endpoint ────────────▶ │
  │                                      │
  │ ◀──── 402 Payment Required ───────── │
  │       WWW-Authenticate: Payment      │
  │       request="<challenge>"          │
  │                                      │
  │  sign challenge with                 │
  │  Stellar wallet (sponsored mode)     │
  │                                      │
  │ ───── 2. POST /endpoint ────────────▶ │
  │       Authorization: Payment <cred>  │
  │                                      │
  │ ◀──── 200 OK + Payment-Receipt ──── │
```

1. First request: plain HTTP POST to the service URL.
2. Server responds `402 Payment Required` with a Stellar charge challenge (either MPP's `WWW-Authenticate: Payment` header or the x402 `Payment-Required` header).
3. Agent signs the challenge with its Stellar key. The inner transaction is a sponsored SAC transfer — the agent's account is `ALL_ZEROS` and only the auth entries are signed, so the server can fee-bump and broadcast.
4. Agent retries the request with the signed credential in the `Authorization` header.
5. Server validates the credential, broadcasts the signed transaction, and returns the upstream response plus a `Payment-Receipt` header.

## Protocols supported

MPP Router emits a single `402` response that carries **both** dialects. The inner signed XDR is identical — a single signer produces both envelopes.

| Aspect | x402 | MPP |
|--------|------|-----|
| Outer envelope | `X-Payment` header (base64 JSON) | `Authorization: Payment <credential>` header |
| Field names | `payTo`, `asset`, `amount` | `recipient`, `currency`, `amount` |
| Sponsored flag | `extra.areFeesSponsored` | `feePayer: true` |
| Inner XDR | Same sponsored SAC transfer | Same sponsored SAC transfer |

The MPP and x402 `payTo` addresses in a single challenge are **different** and HMAC-bound — pay the address that matches the dialect you chose. Never mix.

## Discovering services

The service catalog is live at `https://apiserver.mpprouter.dev/v1/services/catalog`. Never hardcode service paths — the catalog is the source of truth.

Example services (as of publication — always fetch the live catalog):

| id | price | upstream |
|-----|-------|----------|
| `parallel_search` | $0.01 / request | Parallel.ai web search |
| `exa_search` | $0.005 / request | Exa neural search |
| `firecrawl_scrape` | $0.002 / request | Firecrawl HTML → markdown |
| `openrouter_chat` | dynamic | OpenRouter LLM proxy |

## Getting started

The fastest path for Claude Code or similar AI agents is the `stellar-agent-wallet` plugin, which ships two skills:

- `discover` — fetch and filter the MPP Router service catalog
- `pay-per-call` — execute the full 402 → sign → retry loop, handling both MPP and x402 dialects

Install the plugin, then:

```bash
# Find a service
npx tsx skills/discover/run.ts --query "web search"

# Call it — the skill pays automatically
npx tsx skills/pay-per-call/run.ts \
  "https://apiserver.mpprouter.dev/v1/services/parallel/search" \
  --body '{"query": "Summarize https://stripe.com/docs"}' \
  --method POST
```

For custom integrations, use the `@stellar/mpp` SDK on npm with `@stellar/stellar-sdk ^14.6.1` and `mppx ^0.4.11` as peer dependencies.

## Safety notes

- **Credentials are single-use.** The HMAC binding to amount, currency, and recipient is the router's defense against replay. If the retry fails, start fresh with a new 402 challenge — do not re-send the same credential.
- **Confirm above a threshold.** For mainnet calls above ~$1.00, prompt the user before signing. The `pay-per-call` skill enforces this by default (`--max-auto <usd>` to override).
- **Validate the challenge amount.** If you know the advertised price from the catalog, verify the 402 challenge amount matches before signing.
- **Mainnet only.** MPP Router does not run on Stellar testnet.

## Relationship to ROZO

MPP Router is the agentic payments rail that lets ROZO's Stellar-native wallets pay for off-chain services with the same USDC balance used for cross-chain intents. An agent holding USDC on Stellar can:

1. Bridge from another chain to Stellar USDC via a ROZO intent.
2. Call any MPP Router service and pay per request.
3. Send the result to an intent for further action (e.g. swap, settle, bridge back).

## Further reading

- MPP Router: [https://www.mpprouter.dev](https://www.mpprouter.dev)
- Live service catalog: [https://apiserver.mpprouter.dev/v1/services/catalog](https://apiserver.mpprouter.dev/v1/services/catalog)
- Stellar Soroban smart-account payments: [Stellar Smart Account Payments](../../integration/api-doc/api-for-advanced-used/stellar-contract-payments.md)
- `stellar-agent-wallet` plugin skills: `discover`, `pay-per-call`, `bridge`, `send-payment`, `check-balance`
