FROM python:3.12.13-alpine3.23@sha256:601d3d3797e90e2534782e69c85fafb7971b43f24c7b1b079b7e48dd435e458d
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TASKFLOW_DATABASE=/app/data/taskflow.db
WORKDIR /app
RUN apk upgrade --no-cache && addgroup -g 10001 taskflow \
    && adduser -D -H -u 10001 -G taskflow taskflow \
    && mkdir /app/data && chown taskflow:taskflow /app/data
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt
COPY --chown=taskflow:taskflow app.py .
COPY --chown=taskflow:taskflow templates/ templates/
USER 10001:10001
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
