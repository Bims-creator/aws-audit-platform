FROM python:3.12-slim

WORKDIR /app

COPY packages/audit-common /app/packages/audit-common
COPY apps/iam-auditor /app/apps/iam-auditor

RUN pip install --no-cache-dir /app/packages/audit-common /app/apps/iam-auditor

ENTRYPOINT ["python", "-m", "iam_auditor.main"]
