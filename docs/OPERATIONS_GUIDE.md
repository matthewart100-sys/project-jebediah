# Bonsaai Operations Guide

> **Historical pull request #60 audit and salvage artifact — do not execute.**
> This file is non-authoritative and grants no implementation, operations, or
> deployment permission. See the
> [Phase 3B reconciliation decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md).

## Service lifecycle

From `docker/production`:

```bash
docker compose up -d
docker compose down
docker compose restart executive-shell reverse-proxy
docker compose ps
```

## Health and status checks

```bash
curl -k https://bonsaai.local/healthz
curl -k https://bonsaai.local/health
docker compose ps
docker compose logs --tail=200 executive-shell
docker exec bonsaai-executive-shell python -c "import urllib.request; print('memory', urllib.request.urlopen('http://jebediah-memory:8000/health', timeout=8).status)"
docker exec bonsaai-executive-shell python -c "import urllib.request; print('interaction', urllib.request.urlopen('http://jebediah-interaction:8001/health', timeout=8).status)"
docker exec bonsaai-executive-shell python -c "import urllib.request; print('qdrant', urllib.request.urlopen('http://qdrant:6333/healthz', timeout=8).status)"
docker exec bonsaai-executive-shell python -c "import os, urllib.request; base=os.environ.get('OLLAMA_URL', 'http://ollama:11434').rstrip('/'); print('ollama', urllib.request.urlopen(base + '/api/tags', timeout=8).status)"
```

Expected healthy state:

- `reverse-proxy`: running
- `executive-shell`: healthy
- Existing runtime dependencies reachable from `executive-shell`:
  - `jebediah-memory`: HTTP 200
  - `jebediah-interaction`: HTTP 200
  - `qdrant`: HTTP 200
  - `ollama`: HTTP 200

## Logging

- Container logs are available via `docker compose logs`.
- Persist operational incidents in tracked issue/PR artifacts (not ad-hoc chat).

## Resource and capacity checks

```bash
docker stats --no-stream
docker system df
```

## Incident triage order

1. Reverse proxy reachability (`/healthz`).
2. Executive shell health (`/health`).
3. Qdrant health and storage.
4. Ollama readiness/model availability.
5. Existing canonical runtime dependency health from the Executive Shell
   container context.

## Controlled shutdown

```bash
docker compose down
```

Use controlled shutdown before host reboots whenever possible.

## Workspace operations

- Workspace selection is performed from the Executive Dashboard landing page.
- Demonstration workspace:
  - shows a persistent blue `Demonstration Mode` banner
  - uses synthetic organization data only
  - supports `Reset Demo` for one-click synthetic baseline restore
- Development workspace:
  - shows a persistent orange `Development Environment` banner
  - enables governed runtime plus diagnostics
- Production workspace:
  - shows a persistent green `Production Workspace` banner
  - uses governed runtime only (no synthetic workspace content)
