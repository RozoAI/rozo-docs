# Maintaining the documentation

Public navigation lives in `SUMMARY.md`. Keep existing page paths stable and use `.gitbook.yaml` redirects when a published path must change. Task guides should link to canonical API references rather than duplicate schemas, prices or limits.

## Secret scanning

Enable the local gitleaks pre-commit hook once per clone: `brew install gitleaks pre-commit && pre-commit install` (configuration in `.pre-commit-config.yaml`). CI also runs a report-only scan in `.github/workflows/secret-scan.yml`.
