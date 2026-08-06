# Bonsaai Deployment Guide (Phase 4)

## Purpose

Deploy the governed Executive Shell as an additional application on top of an
existing Jebediah governed runtime on the Dell PowerEdge R420 target host.

## Production architecture diagram

```mermaid
flowchart LR
    Client[Network Clients] --> RP[Reverse Proxy (Caddy)]
    RP --> ES[Executive Shell Runtime]
    ES --> Q[Existing Qdrant]
    ES --> O[Existing Ollama]
    ES --> M[Existing jebediah-memory]

    subgraph Existing jebediah_internal Network
        ES
        M
        Q
        O
    end

    subgraph Persistent Storage
        V1[(bonsaai_runtime_data)]
        V2[(bonsaai_caddy_data/config)]
    end

    ES --- V1
    RP --- V2
```

## Deployment topology

- Compose file: `docker/production/docker-compose.yml`
- Reverse proxy: `docker/production/Caddyfile`
- Runtime env template: `docker/production/.env.example`
- Operations scripts: `scripts/operations/*.sh`
- Exposed services:
  - `reverse-proxy` on ports 80/443
- Private-only services:
  - `executive-shell`
  - existing runtime dependencies reached through `jebediah_internal`
    (`qdrant`, `ollama`, `jebediah-memory`)

## Host prerequisites (existing Jebediah server)

1. Ubuntu host on Dell PowerEdge R420.
2. Docker engine installed.
3. Docker Compose CLI (`docker compose` or `docker-compose`) installed.
4. DNS/hosts entry for `bonsaai.local` (and optional production domain).
5. Existing governed runtime is already running with:
   - `qdrant` container
   - `jebediah-memory` container
   - `jebediah-interaction` container
   - Docker networks `jebediah_internal` and `jebediah_external`

## Upgrade deployment (layering Bonsaai onto existing runtime)

1. Copy environment template:

   ```bash
   cd ~/project-jebediah/docker/production
   cp .env.example .env
   ```

2. Edit `.env`:
   - `BONSAAI_PUBLIC_HOSTS=bonsaai.local` for local mode.
   - Include production domain when available (for example
     `BONSAAI_PUBLIC_HOSTS=bonsaai.local,bonsaai.example.com`).
   - Set `ACME_EMAIL` for certificate registration on public domains.
   - Set workspace defaults:
     - `BONSAAI_WORKSPACE_MODE=production`
     - `BONSAAI_DEFAULT_WORKSPACE=production`
     - `BONSAAI_ORGANIZATION_ID=virginia-b-andes`
   - Confirm runtime discovery values match the existing server:
     - `BONSAAI_QDRANT_URL=http://qdrant:6333`
     - `BONSAAI_OLLAMA_URL=http://ollama:11434`
     - `BONSAAI_MEMORY_API_URL=http://jebediah-memory:8000`
     - `BONSAAI_INTERACTION_API_URL=http://jebediah-interaction:8000`
     - `BONSAAI_INTERACTION_ADMISSION_PATH=/admission/submit`
     - `BONSAAI_INTERACTION_ASK_PATH=/questions/ask`
     - `BONSAAI_CANONICAL_RUNTIME=1`

3. Start stack:

   ```bash
   cd ~/project-jebediah/docker/production
   docker compose up -d --build
   ```

4. Verify runtime:

   ```bash
   docker compose ps
   docker network inspect jebediah_internal
   curl -k https://bonsaai.local/healthz
   curl -k https://bonsaai.local/health
   ```

5. Confirm Bonsaai did not create replacement governed runtime services:
   - no `bonsaai-qdrant`
   - no `bonsaai-ollama`
   - no `bonsaai-memory-runtime`

## Deployment verification checklist

Run from `~/project-jebediah/docker/production`:

1. Validate compose services:

   ```bash
   docker compose config --services
   ```

   Expected output (exact service set):

   ```text
   executive-shell
   reverse-proxy
   ```

2. Validate running containers:

   ```bash
   docker compose ps
   ```

   Expected service entries:
   - `bonsaai-executive-shell` (`executive-shell`) state `Up` (health `healthy`)
   - `bonsaai-reverse-proxy` (`reverse-proxy`) state `Up`

3. Validate runtime connectivity from Executive Shell:

   ```bash
   curl -fsS http://jebediah-memory:8000/health
   curl -fsS http://jebediah-interaction:8000/health
   curl -fsS http://qdrant:6333/healthz
   curl -fsS http://ollama:11434/api/tags
   ```

   Expected: each command returns HTTP 200.

4. Confirm no duplicate governed runtime services were created:
   - `docker ps --format '{{.Names}}' | grep -E 'bonsaai-(qdrant|ollama|memory-runtime)'`
   - Expected: no output

## Permanent URL configuration

- Local URL: `https://bonsaai.local`
- Production URL(s): configured via `BONSAAI_PUBLIC_HOSTS`
- Startup workspace and organization: configured via
  `BONSAAI_WORKSPACE_MODE`, `BONSAAI_DEFAULT_WORKSPACE`, and
  `BONSAAI_ORGANIZATION_ID`
- Certificate behavior:
  - local hostnames: Caddy local CA certificate path
  - public domains: automatic ACME certificate issuance where DNS/routing is
    valid

## Boot persistence (systemd)

Create `/etc/systemd/system/bonsaai.service`:

```ini
[Unit]
Description=Bonsaai Executive Platform Stack
After=docker.service network-online.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/cryptids/project-jebediah/docker/production
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=300
TimeoutStopSec=120

[Install]
WantedBy=multi-user.target
```

Enable startup:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bonsaai.service
sudo systemctl start bonsaai.service
```
