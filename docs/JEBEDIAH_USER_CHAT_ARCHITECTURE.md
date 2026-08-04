# Jebediah User Chat Architecture

Status: Draft (feature/interaction-gateway)

Purpose: describe how a laptop browser running Open WebUI connects to the governed Jebediah interaction pipeline using the Interaction Gateway and the GPU-enabled Ollama instance without bypassing the Memory Service or Qdrant.


## User flow (logical)

Laptop Browser (Open WebUI frontend)
    |
    |--(HTTPS/HTTP from browser)-->
    |
Open WebUI configured to use Interaction Gateway (/chat)
    |
    |--(Canonical interaction envelope POST /chat {message: ...})-->
    |
Jebediah Interaction Gateway (FastAPI)
    |  - Receives canonical envelope, performs deterministic context assembly
    |  - Calls Jebediah Memory Service for retrieval
    |  - Builds messages/prompt
    |  - Calls Ollama (generation model) via configured OLLAMA_URL
    |
    |--(POST /memory/context)--> Jebediah Memory Service
    |                            -> Memory Service calls Qdrant for vector retrieval
    |                            <- Returns structured context (JSON)
    |
    |--(POST to Ollama REST API)--> Ollama (qwen3:8b) running on GPU (Windows host)
    |                                (HTTP API on port 11434)
    |<-- response (generated text)
    |
    <- Gateway returns canonical response to the browser with context metadata


## Network flow and Docker networking notes

- The Interaction Gateway runs inside the project's Docker network (service: `jebediah-interaction`).
- Ollama runs on the Windows host and exposes an HTTP API on port 11434.
- Containers cannot always reach arbitrary host IPs depending on platform and virtualization. Two practical approaches are provided:
  1. host.docker.internal (recommended when supported)
     - Add an entry mapping `host.docker.internal` to the Docker host gateway.
     - Example in docker-compose: `extra_hosts: - "host.docker.internal:host-gateway"` and set `OLLAMA_URL=http://host.docker.internal:11434`.
     - This is the approach adopted in services/jebediah-interaction/docker-compose.yml (feature branch change).
  2. Use the host's LAN IP or routed IP (if the container network can reach it)
     - Set `OLLAMA_URL` to `http://<windows-host-ip>:11434` and ensure firewalls allow the connection.
  3. Use `network_mode: "host"` for the interaction service (only when the interaction container is running on the same physical host that exposes Ollama on localhost). This is not set by default because it changes network isolation.

- Ensure the Interaction Gateway container can resolve and reach the configured OLLAMA_URL.
  - Docker Engine 20.10+ supports `host-gateway` for extra_hosts mapping.


## Service responsibilities

- Open WebUI (browser):
  - Presents chat UI to the user.
  - Produces canonical interaction envelope expected by the Interaction Gateway (see ADR-0006). If Open WebUI cannot natively emit that envelope, an adapter/proxy or small client-side mapping is required.
  - Should be configured to point its backend or proxy to the Interaction Gateway `/chat` endpoint instead of directly to Ollama.

- Jebediah Interaction Gateway (service/jebediah-interaction):
  - Exposes `/chat` canonical endpoint to upstream clients (Open WebUI).
  - Calls Memory Service for structured context retrieval.
  - Builds the prompt/messages using the canonical assembly rules.
  - Calls Ollama for generation and returns canonical response with evidence.
  - Enforces canonical envelopes and CORS (browser access). The gateway now includes permissive CORS middleware for local demo use; restrict production origins via configuration.

- Jebediah Memory Service (service/jebediah-memory):
  - Accepts retrieval requests, calls Qdrant, applies retrieval logic and ranking.
  - Returns structured JSON including "memories" array used to assemble the prompt.

- Qdrant:
  - Vector store and retrieval back-end used by the Memory Service.

- Ollama (qwen3:8b on Windows host):
  - Provides GPU-accelerated inference via HTTP API (port 11434).
  - Must expose its API on an address reachable from the Interaction Gateway container (see networking notes).


## Changes made (files)

- services/jebediah-interaction/app/main.py
  - Added FastAPI CORS middleware so browser-based Open WebUI can call /chat.

- services/jebediah-interaction/docker-compose.yml
  - Added `extra_hosts: - "host.docker.internal:host-gateway"` and set `OLLAMA_URL: http://host.docker.internal:11434`.

- docs/JEBEDIAH_USER_CHAT_ARCHITECTURE.md (this file)


## How to configure Open WebUI (client) to use Interaction Gateway

- On the laptop (Open WebUI browser): set the Open WebUI backend endpoint to the Interaction Gateway URL:
  - Example: `http://<ubuntu-vm-or-host-ip>:8001/chat` (Interaction Gateway listens on host port 8001 by default)
  - Ensure the browser can reach `<ubuntu-vm-or-host-ip>:8001` (forwarded port, firewall)

- Open WebUI must send a canonical JSON payload expected by the Interaction Gateway, e.g.:
  {
    "message": "Hello Jebediah, summarize recent notes about X"
  }

- If Open WebUI cannot be configured directly, run a small adapter/proxy on the laptop that maps the UI's API to `/chat`.


## Validation and verification commands

1. From the machine running containers (Ubuntu VM), verify the Interaction Gateway is up:

   curl -sS http://localhost:8001/health

   Expect: {"status":"ok","service":"jebediah-interaction"}

2. From the container host, verify the Interaction Gateway can reach the Memory Service (internal):

   curl -sS http://localhost:8001/health

   (Then from inside the interaction container) -- optional, run a simple script or use exec:

   docker exec -it jebediah-interaction /bin/sh -c "python -c \"import httpx;print(httpx.post('http://jebediah-memory:8000/memory/health').status_code)\""

   Replace with the Memory Service health endpoint if available.

3. Verify container can reach Ollama on the configured URL (host.docker.internal):

   docker exec -it jebediah-interaction /bin/sh -c "python -c \"import httpx; r=httpx.get('http://host.docker.internal:11434/api/health', timeout=10); print(r.status_code, r.text)\""

   (If Ollama uses a different health path, call `/api/models` or a simple known endpoint.)

4. Test the full flow with a canonical chat POST from the laptop browser or curl (replace HOST with the IP/hostname of the machine where the interaction gateway port 8001 is reachable):

   curl -sS -X POST http://HOST:8001/chat -H "Content-Type: application/json" -d '{"message":"Who is Jebediah?"}'

   Response should be JSON containing "response" and "context_used" keys.


## Proof artifacts to gather (operator steps)

1. Proof of GPU inference and qwen3:8b loading on GPU
   - On the Windows host (where Ollama runs), collect Ollama logs showing qwen3:8b loaded onto GPU or use `nvidia-smi` while a generation runs to show GPU utilization.
   - Example (on Ollama host):
     - Check Ollama server logs for model load messages mentioning qwen3:8b and CUDA/GPU.
     - Run a generation and capture `nvidia-smi` showing increased GPU usage and the Ollama process.

2. Proof the Interaction Gateway used memory retrieval
   - In the Interaction Gateway response `context_used` field, confirm it contains a structured JSON object returned by the Memory Service with a non-empty `memories` array.
   - Capture the `/chat` response and show `context_used["memories"]` content and the Memory Service request logs.

3. Proof Qdrant retrieval
   - From Jebediah Memory Service logs, show the Qdrant query and the returned vectors (or at least that the retrieval call to Qdrant returned non-empty results).
   - Alternatively, call Qdrant directly with the same query used by the Memory Service (if reproducible) and show its response.

4. Proof responses return successfully
   - Show the curl POST response from the Interaction Gateway including generated text and the context metadata.


## Troubleshooting checklist

1. CORS blocked in browser
   - Symptoms: browser console error about CORS when calling Interaction Gateway.
   - Fix: ensure the Interaction Gateway CORS allows the origin (this branch sets it to allow all origins). For production, set allowed origins explicitly.

2. Interaction Gateway cannot reach Ollama
   - Symptoms: Interaction Gateway logs show connection refused or timeout when calling OLLAMA_URL.
   - Fixes:
     - Ensure docker-compose has `extra_hosts: - "host.docker.internal:host-gateway"` and OLLAMA_URL uses host.docker.internal.
     - If not using Docker Engine that supports host-gateway, explicitly set OLLAMA_URL to the Windows host LAN IP and ensure port 11434 is reachable through firewall.
     - As a temporary diagnostic, run `docker exec -it jebediah-interaction /bin/sh` and use curl or python to request the Ollama API.

3. Ollama responds slowly or model not on GPU
   - Symptoms: long response times; `nvidia-smi` shows no model load; Ollama logs show CPU-only runtime.
   - Fixes:
     - Confirm Ollama process was started with GPU acceleration enabled and that qwen3:8b is available.
     - Check the Ollama startup flags and model manifest; consult Ollama operator documentation.

4. Memory service returns empty memories
   - Symptoms: `context_used.memories` empty in Interaction Gateway response.
   - Fixes:
     - Confirm embeddings were created and vectors inserted into Qdrant.
     - Check the Memory Service logs and Qdrant health and collections.

5. Docker-to-host name resolution fails
   - Symptoms: `host.docker.internal` does not resolve inside container.
   - Fix: add `extra_hosts` mapping to docker-compose as shown or set the container's network_mode to host if appropriate for the environment.


## Remaining limitations and operational notes

- The current Interaction Gateway CORS setting is permissive (allow_origins: ["*"]) to support local laptop browser demos. For production or wider networks, restrict this to explicit origins.
- Host reachability depends on Docker Engine and virtualization. The `host-gateway` mapping is supported on modern Docker versions; older setups may need explicit IP addresses or `network_mode: host`.
- The Interaction Gateway expects the canonical envelope (see docs/ADR-0006). If Open WebUI emits a different shape, an adapter is required at the client or a small proxy service.
- Ollama must be explicitly configured with GPU acceleration and qwen3:8b available. This doc records the integration wiring but does not change Ollama host configuration.


## Next steps and acceptance criteria

- Configure Open WebUI to target Interaction Gateway `/chat` endpoint.
- Start the stack with the updated docker-compose (or apply equivalent host routing) and validate the commands in "Validation and verification commands".
- Provide captured proof artifacts as described in "Proof artifacts to gather".


---

Document created for Sprint 005/006 integration work by the Interaction Gateway integration engineer. Update as operational evidence is collected.
