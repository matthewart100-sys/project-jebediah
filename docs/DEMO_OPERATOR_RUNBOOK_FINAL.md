Operator Runbook — Project Jebediah VBA Pilot (FINAL)

Purpose
-------
This runbook provides the minimal, tested operator steps to start, validate, run, and stop the Project Jebediah VBA pilot demonstration. It is intended for a single-operator live demo environment and assumes the demo laptop is the Ollama host.

Preconditions
-------------
- Demo laptop (host) is running Ollama bound to 0.0.0.0:11434 and has these models installed:
  - nomic-embed-text:v1.5
  - qwen3:8b
- Docker engine is running and the repository workspace is available on the host.
- Repository root path used in commands: the working directory where this runbook resides.

Files of interest
-----------------
- Compose files with Docker→Windows mapping (committed):
  - services/jebediah-interaction/docker-compose.yml
  - services/jebediah-memory/docker-compose.yml
- VBA seeder: tools/vba_pilot/load_vba_evidence.py
- Backup (pre-reset): qdrant_jebediah_memory_backup.json (repo root)

Quick start (single commands)
-----------------------------
1. Start services (from repo root):
   docker compose -f services/jebediah-memory/docker-compose.yml up -d --build
   docker compose -f services/jebediah-interaction/docker-compose.yml up -d --build

2. Health checks:
   curl -sS http://localhost:8001/health
   curl -sS http://localhost:8000/health
   curl -sS http://host.docker.internal:11434/api/tags
   docker run --rm --network jebediah_internal curlimages/curl:8.4.0 -sS http://qdrant:6333/collections/jebediah_memory | jq -r '.result | {points_count, indexed_vectors_count, config: .config.params.vectors}'

3. End-to-end demo test (example):
   curl -sS -X POST http://localhost:8001/chat -H 'Content-Type: application/json' -d '{"message":"Hello Jebediah. Introduce yourself and explain what you can do."}' -w '\nHTTP_STATUS:%{http_code}\n' -o /tmp/jeb_response.json
   jq -r '.response' /tmp/jeb_response.json

Detailed operator checklist
---------------------------
1. Preconditions
   - Confirm Ollama is running on the host and models present:
     curl -sS http://host.docker.internal:11434/api/tags | jq -r '.models[].model'
     Expect to see: nomic-embed-text:v1.5 and qwen3:8b

2. Start the services
   - From repository root run the compose up commands shown above.

3. Verify container → Ollama networking
   - Interaction container:
     docker exec jebediah-interaction getent hosts host.docker.internal
     docker exec jebediah-interaction python3 -c "import httpx; print(httpx.get('http://host.docker.internal:11434/api/tags').status_code)"
   - Memory container:
     docker exec jebediah-memory getent hosts host.docker.internal
     docker exec jebediah-memory python3 -c "import httpx,os; print(httpx.get(os.getenv('OLLAMA_URL') + '/api/tags').status_code)"

4. (Optional) Reset and reseed demo data — use only when necessary
   - Backup current collection (created during validation): ./qdrant_jebediah_memory_backup.json
   - Delete collection:
     docker run --rm --network jebediah_internal curlimages/curl:8.4.0 -sS -X DELETE http://qdrant:6333/collections/jebediah_memory
   - Recreate memory service:
     docker compose -f services/jebediah-memory/docker-compose.yml up -d --force-recreate
   - Reseed VBA demo data:
     docker run --rm --network jebediah_internal -v "$(pwd)":/workspace -w /workspace python:3.12-slim python /workspace/tools/vba_pilot/load_vba_evidence.py
   - Validate stored points and embedding identity:
     docker run --rm --network jebediah_internal curlimages/curl:8.4.0 -sS -X POST http://qdrant:6333/collections/jebediah_memory/points/scroll -H 'Content-Type: application/json' -d '{}' | jq -r '.result.points[] | {id: .id, embedding_model: .payload.embedding_model, embedding_identity: .payload.embedding_identity, content: .payload.content}'
     Expect embedding_model == "nomic-embed-text:v1.5" and embedding_identity.manifest_digest == sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f

5. Ensure Qdrant indexing for fast retrieval (optional)
   - Commit writes:
     docker run --rm --network jebediah_internal curlimages/curl:8.4.0 -sS -X POST http://qdrant:6333/collections/jebediah_memory/commit
   - Optimize (mild):
     docker run --rm --network jebediah_internal curlimages/curl:8.4.0 -sS -X POST http://qdrant:6333/collections/jebediah_memory/optimize -H 'Content-Type: application/json' -d '{"timeout":120}'

6. Demo run
   - Open the project WebUI (if configured) or run the example curl above. Deliver the prepared script prompts (see VBA_JEBEDIAH_BOARD_DEMO_SCRIPT.md).

7. Stop services after demo
   - docker compose -f services/jebediah-interaction/docker-compose.yml down
   - docker compose -f services/jebediah-memory/docker-compose.yml down

Troubleshooting (quick)
-----------------------
- If containers cannot resolve host.docker.internal, inspect compose extra_hosts mapping and recreate containers.
- If memory store fails with embedding errors, check memory logs (docker logs jebediah-memory) and ensure Ollama is reachable and has nomic-embed-text:v1.5 installed.
- If embedding identity is rejected for points in Qdrant, do not change governance — instead reseed the collection as described.

Contact
-------
For operational support during the demo, contact the on-call release engineer or the project maintainer.

Document history
----------------
- Created: 2026-08-04
- Creator: Senior Release Engineer (performed validation and reseed)

