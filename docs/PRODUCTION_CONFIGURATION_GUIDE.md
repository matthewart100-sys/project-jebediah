# Bonsaai Production Configuration Guide

## Configuration files

- Compose topology: `docker/production/docker-compose.yml`
- Proxy configuration: `docker/production/Caddyfile`
- Environment template: `docker/production/.env.example`

## Environment variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `BONSAAI_HTTP_PORT` | HTTP bind port on host | `80` |
| `BONSAAI_HTTPS_PORT` | HTTPS bind port on host | `443` |
| `BONSAAI_PUBLIC_HOSTS` | Caddy site hostnames | `bonsaai.local` |
| `ACME_EMAIL` | ACME registration email | `admin@example.invalid` |
| `COLLECTION_NAME` | Qdrant collection for memory | `jebediah_memory` |
| `EMBEDDING_MODEL` | Approved embedding model identity | `nomic-embed-text:v1.5` |
| `BONSAAI_WORKSPACE_MODE` | Startup workspace mode | `production` |
| `BONSAAI_DEFAULT_WORKSPACE` | Fallback startup workspace mode | `production` |
| `BONSAAI_ORGANIZATION_ID` | Startup organization profile | `virginia-b-andes` |

## Security posture

- Only reverse proxy publishes host ports.
- Internal services run on `bonsaai_internal` (`internal: true`).
- Qdrant, Ollama, and memory runtime are not directly exposed to the network.
- Executive runtime remains governed by existing admission/promotion/review
  boundaries.

## Runtime persistence

Persistent volumes:

- `bonsaai_runtime_data`
- `bonsaai_qdrant_storage`
- `bonsaai_ollama_models`
- `bonsaai_caddy_data`
- `bonsaai_caddy_config`

## Domain setup notes

1. Local-only mode:
   - `BONSAAI_PUBLIC_HOSTS=bonsaai.local`
   - Add DNS/hosts mapping to the server IP.
2. Production domain mode:
   - Include public hostname in `BONSAAI_PUBLIC_HOSTS`
   - Ensure DNS A/AAAA records resolve to the reverse-proxy host.
