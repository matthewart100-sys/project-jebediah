#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker/production/docker-compose.yml"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_ROOT="${1:-${REPO_ROOT}/backups}"
TARGET_DIR="${BACKUP_ROOT}/${TIMESTAMP}"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "Docker Compose CLI not found. Install 'docker compose' or 'docker-compose'."
  exit 1
fi

mkdir -p "${TARGET_DIR}"

echo "Exporting runtime volume archive..."
docker run --rm \
  -v bonsaai_runtime_data:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/runtime_data.tar.gz -C /data .

echo "Exporting reverse-proxy certificate volume..."
docker run --rm \
  -v bonsaai_caddy_data:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/caddy_data.tar.gz -C /data .

echo "Exporting reverse-proxy configuration volume..."
docker run --rm \
  -v bonsaai_caddy_config:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/caddy_config.tar.gz -C /data .

echo "Recording overlay service topology..."
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" config --services \
  > "${TARGET_DIR}/compose_services.txt"

echo "Backup completed: ${TARGET_DIR}"
