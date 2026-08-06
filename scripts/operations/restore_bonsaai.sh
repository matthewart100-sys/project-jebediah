#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup-directory>"
  exit 1
fi

BACKUP_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker/production/docker-compose.yml"

if [[ ! -d "${BACKUP_DIR}" ]]; then
  echo "Backup directory not found: ${BACKUP_DIR}"
  exit 1
fi

if [[ ! -f "${BACKUP_DIR}/runtime_data.tar.gz" ]]; then
  echo "runtime_data.tar.gz not found in ${BACKUP_DIR}"
  exit 1
fi

if [[ ! -f "${BACKUP_DIR}/qdrant_storage.tar.gz" ]]; then
  echo "qdrant_storage.tar.gz not found in ${BACKUP_DIR}"
  exit 1
fi

if [[ ! -f "${BACKUP_DIR}/caddy_data.tar.gz" ]]; then
  echo "caddy_data.tar.gz not found in ${BACKUP_DIR}"
  exit 1
fi

echo "Stopping stack for restore..."
docker-compose -f "${COMPOSE_FILE}" down

echo "Restoring runtime volume..."
docker run --rm \
  -v bonsaai_runtime_data:/data \
  -v "${BACKUP_DIR}:/backup:ro" \
  alpine:3.22 \
  sh -c "rm -rf /data/* && tar -xzf /backup/runtime_data.tar.gz -C /data"

echo "Restoring Qdrant volume..."
docker run --rm \
  -v bonsaai_qdrant_storage:/data \
  -v "${BACKUP_DIR}:/backup:ro" \
  alpine:3.22 \
  sh -c "rm -rf /data/* && tar -xzf /backup/qdrant_storage.tar.gz -C /data"

echo "Restoring reverse-proxy certificate volume..."
docker run --rm \
  -v bonsaai_caddy_data:/data \
  -v "${BACKUP_DIR}:/backup:ro" \
  alpine:3.22 \
  sh -c "rm -rf /data/* && tar -xzf /backup/caddy_data.tar.gz -C /data"

echo "Starting stack..."
docker-compose -f "${COMPOSE_FILE}" up -d

echo "Restore completed."
