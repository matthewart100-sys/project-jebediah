# Bonsaai Disaster Recovery Guide

## Recovery objectives

- Restore governed Executive Shell runtime continuity.
- Restore Qdrant memory retrieval data.
- Restore operational access through reverse proxy.

## Recovery prerequisites

- Repository checkout at target release tag/commit.
- Latest valid backup folder.
- Docker and Docker Compose available on replacement host.

## Restore sequence

1. Rebuild deployment baseline:

   ```bash
   cd ~/project-jebediah/docker/production
   cp .env.example .env
   docker compose up -d --build
   ```

2. Restore runtime data:

   ```bash
   ./scripts/operations/restore_bonsaai.sh /var/backups/bonsaai/<timestamp>
   ```

3. Validate:

   ```bash
   docker compose ps
   curl -k https://bonsaai.local/healthz
   curl -k https://bonsaai.local/health
   ```

## Post-recovery checks

- Knowledge Manager admission path loads.
- Governance review queues render.
- Organizational Intelligence ask flow returns evidence-backed or
  insufficient-evidence outcomes.
- Audit timeline remains visible.
