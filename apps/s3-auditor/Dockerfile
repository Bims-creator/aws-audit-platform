FROM python:3.12-slim

WORKDIR /app

COPY packages/audit-common /app/packages/audit-common
COPY apps/s3-auditor /app/apps/s3-auditor

RUN pip install --no-cache-dir /app/packages/audit-common /app/apps/s3-auditor

ENTRYPOINT ["python", "-m", "s3_auditor.main"]
