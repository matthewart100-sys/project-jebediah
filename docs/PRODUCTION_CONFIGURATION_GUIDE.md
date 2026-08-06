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
| `BONSAAI_QDRANT_URL` | Existing Jebediah Qdrant endpoint on `jebediah_internal` | `http://qdrant:6333` |
| `BONSAAI_OLLAMA_URL` | Existing Jebediah Ollama endpoint on `jebediah_internal` | `http://ollama:11434` |
| `BONSAAI_MEMORY_API_URL` | Existing Jebediah memory API endpoint on `jebediah_internal` | `http://jebediah-memory:8000` |
| `BONSAAI_INTERACTION_API_URL` | Existing Jebediah interaction API endpoint on `jebediah_internal` | `http://jebediah-interaction:8001` |
| `BONSAAI_INTERACTION_ADMISSION_PATH` | Interaction API admission route path | `/admission/submit` |
| `BONSAAI_INTERACTION_ASK_PATH` | Interaction API question-answer route path | `/questions/ask` |
| `BONSAAI_CANONICAL_RUNTIME` | Enables Executive Shell canonical-runtime client mode | `1` |
| `BONSAAI_WORKSPACE_MODE` | Startup workspace mode | `production` |
| `BONSAAI_DEFAULT_WORKSPACE` | Fallback startup workspace mode | `production` |
| `BONSAAI_ORGANIZATION_ID` | Startup organization profile | `virginia-b-andes` |

## Security posture

- Only reverse proxy publishes host ports.
- Internal Executive Shell traffic runs on existing `jebediah_internal`.
- Reverse proxy ingress runs on existing `jebediah_external`.
- Qdrant, Ollama, and jebediah-memory are reused from the existing governed
  runtime (no replacement containers are created).
- Executive runtime remains governed by existing admission/promotion/review
  boundaries.

## Runtime persistence

Persistent volumes:

- `bonsaai_runtime_data`
- `bonsaai_caddy_data`
- `bonsaai_caddy_config`

Existing runtime persistence for qdrant/ollama/memory remains owned by the
canonical Jebediah runtime stack.

## Domain setup notes

1. Local-only mode:
   - `BONSAAI_PUBLIC_HOSTS=bonsaai.local`
   - Add DNS/hosts mapping to the server IP.
2. Production domain mode:
   - Include public hostname in `BONSAAI_PUBLIC_HOSTS`
   - Ensure DNS A/AAAA records resolve to the reverse-proxy host.
