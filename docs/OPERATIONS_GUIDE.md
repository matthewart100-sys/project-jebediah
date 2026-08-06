# Bonsaai Operations Guide

## Service lifecycle

From `docker/production`:

```bash
docker-compose up -d
docker-compose down
docker-compose restart executive-shell reverse-proxy
docker-compose ps
```

## Health and status checks

```bash
curl -k https://bonsaai.local/healthz
curl -k https://bonsaai.local/health
docker-compose ps
docker-compose logs --tail=200 executive-shell
docker-compose logs --tail=200 memory-runtime
```

Expected healthy state:

- `reverse-proxy`: running
- `executive-shell`: healthy
- `memory-runtime`: healthy
- `qdrant`: healthy
- `ollama`: running/ready

## Logging

- Container logs are available via `docker-compose logs`.
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
5. Memory runtime logs for retrieval/store failures.

## Controlled shutdown

```bash
docker-compose down
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
