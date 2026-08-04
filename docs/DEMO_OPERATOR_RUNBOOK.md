Project Jebediah — Demo Operator Runbook
========================================

Purpose
-------
Operational runbook for running the Project Jebediah VBA executive demo. This
runbook covers startup, validation, recovery steps, and known limitations. It
is intentionally operational only — it does not change architecture or memory
contracts.

Prerequisites
-------------
- Host with Docker Engine and docker compose available and functional
- Access to the repository workspace (for compose files and scripts)
- Ollama reachable by containers (recommended: run Ollama container on the
  same docker network)

Quick paths
-----------
- Start the demo (create network if needed, start qdrant, memory, interaction):
  ./scripts/demo_start.sh
- Stop the demo (preserve data):
  ./scripts/demo_stop.sh
- Validate the running demo environment:
  ./scripts/demo_check.sh

Startup procedure
-----------------
1. On the demo VM, ensure Docker is running and the current user can run
   `docker`/`docker compose`.
2. From the repository root run: ./scripts/demo_start.sh
   - The script ensures the docker network `jebediah_internal` exists and
     creates it if missing.
   - It ensures qdrant is running (starts it via the memory compose if needed),
     then starts `jebediah-memory` and `jebediah-interaction` via their
     compose files.
   - After services start, it executes the validation script
     `scripts/demo_check.sh` and reports any warnings or failures.
3. If demo_start.sh reports issues, consult the validation checklist below.

Validation checklist (what scripts/demo_check.sh verifies)
---------------------------------------------------------
- Docker CLI and daemon are available
- docker network `jebediah_internal` exists
- `jebediah-memory`, `jebediah-interaction`, `qdrant` containers are running
  (or reported if missing)
- Memory service `/health` returns an HTTP response via the docker network
- Interaction service `/health` returns an HTTP response via the docker network
- Qdrant `/collections` endpoint reachable on `qdrant:6333`
- Ollama reachable at configured `OLLAMA_URL` and its model inventory is
  reachable at `/api/models` (best-effort)
- Approved embedding model (nomic-embed-text:v1.5) is present in Ollama's
  inventory (best-effort verification)
- End-to-end chat smoke test posts to `http://jebediah-interaction:8001/chat`
  and the response contains a `response` field

Recovery steps (common failures)
-------------------------------
- Docker daemon not running
  - Start Docker (systemctl start docker) or reboot the VM if services are
    unavailable.
- `jebediah_internal` network missing
  - Create it: docker network create jebediah_internal
  - Alternatively run ./scripts/demo_start.sh to auto-create and start services
- qdrant unreachable
  - Inspect logs: docker logs qdrant --tail 200
  - Restart qdrant: docker restart qdrant
  - If qdrant is not present, start it: docker compose -f services/jebediah-memory/docker-compose.yml up -d qdrant
- Ollama unreachable from containers
  - Preferred for demos: run Ollama as a container attached to `jebediah_internal` with hostname `ollama` and set OLLAMA_URL to http://ollama:11434
  - Alternative: run Ollama on host bound to 0.0.0.0:11434 and set the OLLAMA_URL env accordingly
  - Verify model installation: use `ollama pull nomic-embed-text:v1.5` on the Ollama host if models are missing
- Approved embedding model not installed
  - Install model in Ollama (follow Ollama documentation). The memory service will return HTTP 503 until the approved model is available.
- Service failing to start (memory or interaction)
  - Inspect logs: docker logs jebediah-memory --tail 300 and docker logs jebediah-interaction --tail 300
  - Rebuild and redeploy the specific service: docker compose -f <compose> up -d --build <service>

Known limitations
-----------------
- Containers may not see host-bound services unless host services are bound
  appropriately (0.0.0.0) or an Ollama container is attached to the demo
  network.
- Memory service will intentionally return HTTP 503 when the embedding
  provider is unavailable.
- Approved embedding model must be installed into Ollama (nomic-embed-text:v1.5)
  or the memory service will refuse to produce embeddings.
- This runbook focuses on operational hardening for the demo only; it does not
  change the canonical memory/service architecture, embedding identity, or
  Qdrant configuration.

Contacts / escalation
---------------------
- Infra owner for Ollama and network configuration
- Project maintainer for service build/runtime issues

Document history
----------------
- Generated/updated as part of Sprint 005 demo hardening work.
