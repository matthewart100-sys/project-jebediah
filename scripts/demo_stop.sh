#!/usr/bin/env bash
set -euo pipefail

# demo_stop.sh
# Safely stop demo services while preserving data (do not remove volumes).

NETWORK=jebediah_internal
MEMORY_COMPOSE=services/jebediah-memory/docker-compose.yml
INTERACTION_COMPOSE=services/jebediah-interaction/docker-compose.yml

function info { echo "[INFO] $*"; }
function err { echo "[ERROR] $*" >&2; }

info "Stopping interaction service (jebediah-interaction)"
if docker ps --format '{{.Names}}' | grep -q '^jebediah-interaction$'; then
  docker compose -f ${INTERACTION_COMPOSE} stop jebediah-interaction || true
  info "jebediah-interaction stopped"
else
  info "jebediah-interaction not running"
fi

info "Stopping memory service (jebediah-memory)"
if docker ps --format '{{.Names}}' | grep -q '^jebediah-memory$'; then
  docker compose -f ${MEMORY_COMPOSE} stop jebediah-memory || true
  info "jebediah-memory stopped"
else
  info "jebediah-memory not running"
fi

info "Preserving qdrant and other persistent volumes. To stop qdrant, run: docker compose -f ${MEMORY_COMPOSE} stop qdrant"

info "Stopped demo services (data preserved)."
exit 0
