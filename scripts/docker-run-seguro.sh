#!/usr/bin/env bash
set -euo pipefail
: "${TASKFLOW_SECRET_KEY:?Defina TASKFLOW_SECRET_KEY no ambiente}"
IMAGE_NAME="${IMAGE_NAME:-taskflow:hardened}"
docker volume create taskflow-dados >/dev/null
docker run --rm --cap-drop=ALL --security-opt=no-new-privileges \
  -e TASKFLOW_SECRET_KEY -v taskflow-dados:/app/data \
  "$IMAGE_NAME" flask --app 'app:create_app()' init-db
docker run --rm -d --name taskflow-seguro \
  --read-only --cap-drop=ALL --security-opt=no-new-privileges \
  --memory=256m --cpus=0.5 --pids-limit=100 --user=10001:10001 \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  -v taskflow-dados:/app/data -p 127.0.0.1:5000:5000 \
  -e TASKFLOW_SECRET_KEY -e TASKFLOW_HTTPS=0 "$IMAGE_NAME"
