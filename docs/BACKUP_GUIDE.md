# Bonsaai Backup Guide

## Scope

Backups protect runtime custody/governance state and semantic storage needed for
service continuity.

## Backup command

```bash
./scripts/operations/backup_bonsaai.sh /var/backups/bonsaai
```

Generated outputs:

- `runtime_data.tar.gz`
- `caddy_data.tar.gz`
- `caddy_config.tar.gz`
- `compose_services.txt`

The backup covers only Bonsaai-owned overlay state. Existing canonical runtime
dependencies such as Qdrant, Ollama, `jebediah-memory`, and
`jebediah-interaction` must be backed up through their own approved runtime
procedures.

## Recommended schedule

- Daily incremental backups.
- Weekly retention checkpoints.
- Keep at least one off-host encrypted copy.

## Verification

After each backup:

1. Confirm backup directory exists with timestamp.
2. Confirm `runtime_data.tar.gz` is present and non-empty.
3. Confirm `caddy_data.tar.gz` and `caddy_config.tar.gz` are present.
4. Confirm `compose_services.txt` contains exactly `executive-shell` and
   `reverse-proxy`.
