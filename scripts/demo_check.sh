#!/usr/bin/env bash
set -euo pipefail

# Demo validation script for Project Jebediah
# Runs checks to verify containers and external dependencies are reachable.

NETWORK=jebediah_internal
MEMORY_SVC=jebediah-memory
INTERACTION_SVC=jebediah-interaction
QDRANT_SVC=qdrant

# Try to read OLLAMA_URL from running memory container env, fallback to default
OLLAMA_DEFAULT="http://100.110.120.15:11434"

function info { echo "[INFO] $*"; }
function err { echo "[ERROR] $*" >&2; }

info "Checking docker network: $NETWORK"
if ! docker network ls --format '{{.Name}}' | grep -q "^${NETWORK}$"; then
  err "Docker network ${NETWORK} not found"
  exit 2
fi

info "Checking containers are running"
for c in ${MEMORY_SVC} ${INTERACTION_SVC} ${QDRANT_SVC}; do
  if ! docker ps --format '{{.Names}}' | grep -q "^$c$"; then
    err "Required container '$c' is not running"
    docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
    exit 3
  fi
done

info "Extracting OLLAMA_URL from ${MEMORY_SVC} env (fallback ${OLLAMA_DEFAULT})"
OLLAMA_URL=$(docker inspect ${MEMORY_SVC} --format '{{range .Config.Env}}{{println .}}{{end}}' 2>/dev/null | grep '^OLLAMA_URL=' | sed -e 's/^OLLAMA_URL=//' || true)
if [ -z "${OLLAMA_URL}" ]; then
  OLLAMA_URL=${OLLAMA_DEFAULT}
fi
info "Using OLLAMA_URL=${OLLAMA_URL}"

info "Testing memory service health via docker network"
docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS http://${MEMORY_SVC}:8000/health -w '\nHTTP_STATUS:%{http_code}\n' || true

info "Testing interaction service health via docker network"
docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS http://${INTERACTION_SVC}:8001/health -w '\nHTTP_STATUS:%{http_code}\n' || true

info "Testing qdrant HTTP reachability"
docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -I http://${QDRANT_SVC}:6333 -w '\nHTTP_STATUS:%{http_code}\n' || true

info "Testing Ollama reachability from the docker network (this must succeed for embeddings)"
docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -I ${OLLAMA_URL} -w '\nHTTP_STATUS:%{http_code}\n' || true

info "If all responses above are HTTP 200 (or other successful codes), the demo environment appears ready."
info "If Ollama is unreachable or model verification fails, follow docs/DEMO_READINESS.md troubleshooting guidance to make Ollama reachable from the docker network and ensure the embedding model is installed."

exit 0
