#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker/production/docker-compose.yml"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "Docker Compose CLI not found. Install 'docker compose' or 'docker-compose'."
  exit 1
fi

echo "Pulling upstream changes..."
git -C "${REPO_ROOT}" fetch origin
git -C "${REPO_ROOT}" pull --ff-only

echo "Building and deploying updated stack..."
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" pull reverse-proxy
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" build --pull executive-shell
"${COMPOSE_CMD[@]}" -f "${COMPOSE_FILE}" up -d --remove-orphans

echo "Upgrade completed."
