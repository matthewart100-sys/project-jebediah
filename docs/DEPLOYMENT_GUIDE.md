# Bonsaai Deployment Guide (Phase 4)

## Purpose

Deploy the current governed Executive Shell and canonical memory runtime as a
permanent service on the Dell PowerEdge R420 target host.

## Production architecture diagram

```mermaid
flowchart LR
    Client[Network Clients] --> RP[Reverse Proxy (Caddy)]
    RP --> ES[Executive Shell Runtime]
    ES --> Q[Qdrant]
    ES --> O[Ollama]
    MR[Memory Runtime API] --> Q
    MR --> O

    subgraph Private Internal Network
        ES
        MR
        Q
        O
    end

    subgraph Persistent Storage
        V1[(bonsaai_runtime_data)]
        V2[(bonsaai_qdrant_storage)]
        V3[(bonsaai_ollama_models)]
        V4[(bonsaai_caddy_data/config)]
    end

    ES --- V1
    Q --- V2
    O --- V3
    RP --- V4
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
  - `memory-runtime`
  - `qdrant`
  - `ollama`

## Host prerequisites

1. Ubuntu host on Dell PowerEdge R420.
2. Docker engine installed.
3. Docker Compose CLI (`docker-compose`) installed.
4. DNS/hosts entry for `bonsaai.local` (and optional production domain).

## First-time deployment

1. Copy environment template:

   ```bash
   cd /opt/project-jebediah/docker/production
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

3. Start stack:

   ```bash
   cd /opt/project-jebediah/docker/production
   docker-compose up -d --build
   ```

4. Verify runtime:

   ```bash
   docker-compose ps
   curl -k https://bonsaai.local/healthz
   curl -k https://bonsaai.local/health
   ```

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
WorkingDirectory=/opt/project-jebediah/docker/production
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
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
