#!/usr/bin/env bash
set -euo pipefail

# demo_start.sh
# Operational startup script for Project Jebediah demo environment.
# - verifies docker
# - creates jebediah_internal network if missing
# - ensures qdrant is running
# - starts memory and interaction services
# - runs scripts/demo_check.sh for post-start validation

NETWORK=jebediah_internal
MEMORY_COMPOSE=services/jebediah-memory/docker-compose.yml
INTERACTION_COMPOSE=services/jebediah-interaction/docker-compose.yml
QDRANT_SERVICE=qdrant

function info { echo "[INFO] $*"; }
function err { echo "[ERROR] $*" >&2; }

info "Verifying Docker CLI and daemon"
if ! command -v docker >/dev/null 2>&1; then
  err "Docker CLI not found. Install Docker and ensure it's available in PATH."
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  err "Docker daemon not responding. Start Docker and retry."
  exit 1
fi

info "Ensuring docker network '${NETWORK}' exists"
if ! docker network ls --format '{{.Name}}' | grep -q "^${NETWORK}$"; then
  info "Creating network ${NETWORK}"
  docker network create ${NETWORK}
else
  info "Network ${NETWORK} already present"
fi

# Start qdrant if not running (use the memory compose that defines qdrant)
info "Ensuring Qdrant service '${QDRANT_SERVICE}' is running"
if ! docker ps --format '{{.Names}}' | grep -q "^${QDRANT_SERVICE}$"; then
  info "Starting qdrant via compose: ${MEMORY_COMPOSE}"
  docker compose -f ${MEMORY_COMPOSE} up -d ${QDRANT_SERVICE}
else
  info "qdrant already running"
fi

# Start memory service
info "Starting memory service using compose: ${MEMORY_COMPOSE}"
docker compose -f ${MEMORY_COMPOSE} up -d --build jebediah-memory

# Start interaction service
info "Starting interaction service using compose: ${INTERACTION_COMPOSE}"
docker compose -f ${INTERACTION_COMPOSE} up -d --build jebediah-interaction

# Run post-start validation
info "Running demo validation: scripts/demo_check.sh"
if [ -x scripts/demo_check.sh ]; then
  scripts/demo_check.sh || {
    warn_rc=$?
    err "demo_check.sh finished with non-zero exit (${warn_rc}). Review messages above for issues."
    exit ${warn_rc}
  }
else
  err "scripts/demo_check.sh not executable. Run: chmod +x scripts/demo_check.sh"
  exit 1
fi

info "Startup completed (services started)."
exit 0
