# Bonsaai Backup Guide

## Scope

Backups protect runtime custody/governance state and semantic storage needed for
service continuity.

## Backup command

```bash
./scripts/operations/backup_bonsaai.sh /var/backups/bonsaai
```

Generated outputs:

- `qdrant_snapshot_response.json`
- `runtime_data.tar.gz`
- `qdrant_storage.tar.gz`
- `caddy_data.tar.gz`
- `ollama_models.txt`

## Recommended schedule

- Daily incremental backups.
- Weekly retention checkpoints.
- Keep at least one off-host encrypted copy.

## Verification

After each backup:

1. Confirm backup directory exists with timestamp.
2. Confirm `runtime_data.tar.gz` is present and non-empty.
3. Confirm `qdrant_storage.tar.gz` and `caddy_data.tar.gz` are present.
4. Confirm snapshot response contains HTTP success payload.
