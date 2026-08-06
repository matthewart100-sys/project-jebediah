# Bonsaai Administrator Quick Start

> **Historical pull request #60 audit and salvage artifact — do not execute.**
> This file is non-authoritative and grants no implementation, operations, or
> deployment permission. See the
> [Phase 3B reconciliation decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md).

## 1) Start services

```bash
cd ~/project-jebediah/docker/production
cp .env.example .env
docker compose up -d --build
```

## 2) Check status

```bash
docker compose ps
curl -k https://bonsaai.local/healthz
curl -k https://bonsaai.local/health
```

## 3) Access the platform

- Open: `https://bonsaai.local`
- Production domain (if configured): `https://<your-domain>`

## 4) Select workspace and organization

On the Executive Dashboard landing page:

- choose workspace mode (`Demonstration`, `Development`, `Production`)
- choose organization (`Demo Organization`, `Back Pack Kidz`, `Virginia B. Andes`)
- the shell remembers the previous selection in persistent runtime state

## 5) Basic operations

- Tail logs: `docker compose logs -f executive-shell`
- Restart app: `docker compose restart executive-shell`
- Stop stack: `docker compose down`

## 6) Back up data

```bash
./scripts/operations/backup_bonsaai.sh /var/backups/bonsaai
```

## 7) Restore from backup

```bash
./scripts/operations/restore_bonsaai.sh /var/backups/bonsaai/<timestamp>
```
