#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker/production/docker-compose.yml"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_ROOT="${1:-${REPO_ROOT}/backups}"
TARGET_DIR="${BACKUP_ROOT}/${TIMESTAMP}"
COLLECTION="${COLLECTION_NAME:-jebediah_memory}"

mkdir -p "${TARGET_DIR}"

echo "Creating Qdrant snapshot..."
docker-compose -f "${COMPOSE_FILE}" exec -T memory-runtime \
  python -c "import json, urllib.request; \
request = urllib.request.Request('http://qdrant:6333/collections/${COLLECTION}/snapshots', method='POST'); \
response = urllib.request.urlopen(request, timeout=30); \
print(json.dumps(json.loads(response.read().decode('utf-8')), indent=2))" \
  > "${TARGET_DIR}/qdrant_snapshot_response.json"

echo "Exporting runtime volume archive..."
docker run --rm \
  -v bonsaai_runtime_data:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/runtime_data.tar.gz -C /data .

echo "Exporting Qdrant volume archive..."
docker run --rm \
  -v bonsaai_qdrant_storage:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/qdrant_storage.tar.gz -C /data .

echo "Exporting reverse-proxy certificate volume..."
docker run --rm \
  -v bonsaai_caddy_data:/data:ro \
  -v "${TARGET_DIR}:/backup" \
  alpine:3.22 \
  tar -czf /backup/caddy_data.tar.gz -C /data .

echo "Exporting Ollama model metadata..."
docker-compose -f "${COMPOSE_FILE}" exec -T ollama ollama list \
  > "${TARGET_DIR}/ollama_models.txt"

echo "Backup completed: ${TARGET_DIR}"
