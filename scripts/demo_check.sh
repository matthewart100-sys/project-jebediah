#!/usr/bin/env bash
set -euo pipefail

# Demo validation script for Project Jebediah
# Runs checks to verify docker, containers, networks, Ollama, Qdrant and basic E2E chat

NETWORK=jebediah_internal
MEMORY_SVC=jebediah-memory
INTERACTION_SVC=jebediah-interaction
QDRANT_SVC=qdrant

# Defaults (overridable via environment when running the script)
OLLAMA_DEFAULT="http://100.110.120.15:11434"
E2E_MESSAGE='{"message":"Hello Jebediah. Introduce yourself briefly."}'

function info { echo "[INFO] $*"; }
function warn { echo "[WARN] $*"; }
function err { echo "[ERROR] $*" >&2; }

# Check docker availability
info "Checking Docker availability"
if ! command -v docker >/dev/null 2>&1; then
  err "Docker CLI not found in PATH. Install Docker Engine and ensure 'docker' is available."
  exit 1
fi

# Check docker daemon responding
if ! docker info >/dev/null 2>&1; then
  err "Docker daemon is not responding. Is the Docker service running and accessible?"
  exit 1
fi

# Check/Report network
info "Checking docker network: ${NETWORK}"
if ! docker network ls --format '{{.Name}}' | grep -q "^${NETWORK}$"; then
  warn "Docker network ${NETWORK} not found"
  warn "Create it with: docker network create ${NETWORK} (or run demo_start.sh to auto-create)"
  NETWORK_MISSING=1
else
  NETWORK_MISSING=0
fi

# Containers presence (running or not)
info "Inspecting required containers: ${MEMORY_SVC}, ${INTERACTION_SVC}, ${QDRANT_SVC}"
MISSING_CONTAINERS=0
for c in ${MEMORY_SVC} ${INTERACTION_SVC} ${QDRANT_SVC}; do
  if ! docker ps --format '{{.Names}}' | grep -q "^$c$"; then
    warn "Required container '$c' is not running"
    MISSING_CONTAINERS=1
  fi
done

# Determine repository root and identity file paths
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IDENTITY_FILE="${REPO_ROOT}/src/collector/embeddings/identity.py"

# Determine OLLAMA_URL: try reading from running memory container env, then shell env, then default
info "Determining OLLAMA_URL"
OLLAMA_URL=""
if docker ps --format '{{.Names}}' | grep -q "^${MEMORY_SVC}$"; then
  OLLAMA_URL=$(docker inspect ${MEMORY_SVC} --format '{{range .Config.Env}}{{println .}}{{end}}' 2>/dev/null | grep '^OLLAMA_URL=' | sed -e 's/^OLLAMA_URL=//' || true)
fi
OLLAMA_URL=${OLLAMA_URL:-${OLLAMA_DEFAULT}}
info "Using OLLAMA_URL=${OLLAMA_URL}"

# Read approved embedding model from source to verify presence in Ollama (best-effort)
APPROVED_EMBEDDING_MODEL=""
APPROVED_EMBEDDING_DIGEST=""
if [ -f "${IDENTITY_FILE}" ]; then
  APPROVED_EMBEDDING_MODEL=$(sed -n 's/APPROVED_EMBEDDING_MODEL = "\(.*\)"/\1/p' "${IDENTITY_FILE}" || true)
  APPROVED_EMBEDDING_DIGEST=$(sed -n "s/APPROVED_EMBEDDING_DIGEST = (\"\(.*\)\")/\1/p" "${IDENTITY_FILE}" || true)
else
  warn "Embedding identity file not found at ${IDENTITY_FILE}; model verification will be skipped"
fi
if [ -z "${APPROVED_EMBEDDING_MODEL}" ]; then
  warn "Approved embedding model not detected in source; model verification will be skipped"
fi

# Helper to perform HTTP check inside docker network (uses curlimages)
function http_check_network() {
  local target_url=$1
  info "HTTP check: ${target_url}"
  docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -I "${target_url}" -w '\nHTTP_STATUS:%{http_code}\n' || true
}

# If network missing, skip network-based checks
if [ ${NETWORK_MISSING} -eq 1 ]; then
  warn "Skipping network-based service checks because docker network ${NETWORK} is missing"
else
  # Memory health
  info "Checking memory service health"
  docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -w '\nHTTP_STATUS:%{http_code}\n' http://${MEMORY_SVC}:8000/health || true

  # Interaction health
  info "Checking interaction service health"
  docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -w '\nHTTP_STATUS:%{http_code}\n' http://${INTERACTION_SVC}:8001/health || true

  # Qdrant HTTP reachability and basic API check
  info "Checking Qdrant reachability and collections API"
  docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -w '\nHTTP_STATUS:%{http_code}\n' http://${QDRANT_SVC}:6333/collections || true

  # Ollama reachability and model inventory
  info "Checking Ollama reachability and model inventory"
  docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -w '\nHTTP_STATUS:%{http_code}\n' ${OLLAMA_URL}/api/models || true

  # If we have approved model name, attempt to verify it is present in Ollama inventory
  if [ -n "${APPROVED_EMBEDDING_MODEL}" ]; then
    info "Verifying approved embedding model '${APPROVED_EMBEDDING_MODEL}' is reported by Ollama (best-effort)"
    MODELS_JSON=$(docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS ${OLLAMA_URL}/api/models || true)
    if echo "${MODELS_JSON}" | grep -q "${APPROVED_EMBEDDING_MODEL}"; then
      info "Approved embedding model '${APPROVED_EMBEDDING_MODEL}' appears installed in Ollama"
    else
      warn "Approved embedding model '${APPROVED_EMBEDDING_MODEL}' not found in Ollama model list (output may be truncated):"
      echo "${MODELS_JSON}" | head -n 40
    fi
  fi

  # End-to-end chat test (simple smoke test)
  info "Performing end-to-end chat smoke test against ${INTERACTION_SVC} (expect 'response' field in JSON)"
  CHAT_OUTPUT=$(docker run --rm --network ${NETWORK} curlimages/curl:8.4.0 -sS -X POST -H 'Content-Type: application/json' --data "${E2E_MESSAGE}" http://${INTERACTION_SVC}:8001/chat || true)
  if echo "${CHAT_OUTPUT}" | grep -q '"response"'; then
    info "E2E chat POST returned a 'response' field"
  else
    warn "E2E chat POST did not return expected 'response' field. Output:"
    echo "${CHAT_OUTPUT}" | sed -n '1,200p'
  fi
fi

# Summarize findings
info "Summary"
if [ ${NETWORK_MISSING} -eq 1 ]; then
  warn "Docker network ${NETWORK} missing"
fi
if [ ${MISSING_CONTAINERS} -eq 1 ]; then
  warn "One or more required containers are not running: ${MEMORY_SVC}, ${INTERACTION_SVC}, ${QDRANT_SVC}"
fi

info "If no WARN/ERROR messages appeared above and HTTP checks returned successful codes, the demo environment appears ready."

exit 0
