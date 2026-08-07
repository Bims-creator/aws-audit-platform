# AWS Audit Platform

A small monorepo platform for running independent AWS security-posture auditors, each shipped as its
own container and released through a tag-triggered, environment-gated GitHub Actions pipeline.

## What it does

Each "auditor" app connects to AWS via `boto3`, runs a set of read-only checks against live resources,
and emits structured `Finding` objects (resource, severity, check ID, message) rather than free-text
output — so results can be piped into a dashboard, ticketing system, or CI gate later.

**Current auditors:**

| App | Checks |
|---|---|
| `apps/iam-auditor` | `iam-001-mfa-enabled` — flags IAM users with no MFA device attached |
| `apps/s3-auditor` | `s3-001-public-bucket-policy` — flags buckets whose bucket policy makes them publicly accessible; `s3-002-bucket-encryption` — flags buckets with no default server-side encryption |

## Architecture

- **`packages/audit-common`** — shared library used by every auditor: the `Finding`/`Severity` model
  and a `get_session()` helper for building a `boto3.Session`.
- **`apps/<name>-auditor`** — one auditor per AWS service/domain, each an independently versioned,
  independently released Python package with its own `Dockerfile`, tests, and release workflow.
- **`templates/auditor-app`** — a placeholder-driven template (`__APP_NAME__` / `__APP_MODULE__`) used
  to scaffold new auditors so every app starts from the same structure, lint config, and CI setup.

## Platform automation

- **AWS Multiapp Create** (`.github/workflows/aws-multiapp-create.yml`) — a `workflow_dispatch` job that
  takes an app name, copies `templates/auditor-app` into `apps/`, substitutes the placeholders, and opens
  a PR — the same scaffold-from-template pattern used to add `s3-auditor` from `iam-auditor`.
- **Release pipeline** (`release-<app>.yml`, triggered on `<app>-vX.Y.Z` tags) — builds and publishes the
  auditor's container to GHCR, then runs it against `dev`, `pre`, and `prod` in sequence using GitHub
  Environments, so a bad check only reaches later environments after the earlier ones pass.
- **CI** (`ci.yml`) — lints with `ruff` and runs `pytest` for each app on every push/PR.

## Status

Actively evolving personal project. `iam-auditor` and `s3-auditor` are functional with real AWS checks;
the audit findings are currently printed to stdout, and building an aggregation/reporting layer across
auditors is the next planned piece.

## Local development

```bash
pip install -e packages/audit-common
pip install -e apps/iam-auditor
python -m iam_auditor.main
```

Requires AWS credentials available to `boto3` (e.g. `AWS_PROFILE` or standard env vars).
