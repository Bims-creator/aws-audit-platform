FROM python:3.12-slim

WORKDIR /app

COPY packages/audit-common /app/packages/audit-common
COPY apps/__APP_NAME__ /app/apps/__APP_NAME__

RUN pip install --no-cache-dir /app/packages/audit-common /app/apps/__APP_NAME__

ENTRYPOINT ["python", "-m", "__APP_MODULE__.main"]
