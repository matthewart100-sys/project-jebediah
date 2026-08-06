#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/docker/production/docker-compose.yml"

echo "Pulling upstream changes..."
git -C "${REPO_ROOT}" fetch origin
git -C "${REPO_ROOT}" pull --ff-only

echo "Building and deploying updated stack..."
docker-compose -f "${COMPOSE_FILE}" pull
docker-compose -f "${COMPOSE_FILE}" build executive-shell memory-runtime
docker-compose -f "${COMPOSE_FILE}" up -d --remove-orphans

echo "Upgrade completed."
