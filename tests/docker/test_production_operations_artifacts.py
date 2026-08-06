from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_COMPOSE = PROJECT_ROOT / "docker" / "production" / "docker-compose.yml"
BACKUP_SCRIPT = PROJECT_ROOT / "scripts" / "operations" / "backup_bonsaai.sh"
RESTORE_SCRIPT = PROJECT_ROOT / "scripts" / "operations" / "restore_bonsaai.sh"
UPGRADE_SCRIPT = PROJECT_ROOT / "scripts" / "operations" / "upgrade_bonsaai.sh"
BACKUP_GUIDE = PROJECT_ROOT / "docs" / "BACKUP_GUIDE.md"
OPERATIONS_GUIDE = PROJECT_ROOT / "docs" / "OPERATIONS_GUIDE.md"
DEPLOYMENT_GUIDE = PROJECT_ROOT / "docs" / "DEPLOYMENT_GUIDE.md"


def test_production_overlay_compose_contains_only_overlay_services() -> None:
    compose = PRODUCTION_COMPOSE.read_text(encoding="utf-8")

    assert "executive-shell:" in compose
    assert "reverse-proxy:" in compose
    assert "\n  memory-runtime:" not in compose
    assert "\n  ollama:" not in compose
    assert "\n  qdrant:" not in compose


def test_backup_and_restore_scripts_track_only_overlay_volumes() -> None:
    backup = BACKUP_SCRIPT.read_text(encoding="utf-8")
    restore = RESTORE_SCRIPT.read_text(encoding="utf-8")

    for source in (backup, restore):
        assert "bonsaai_runtime_data" in source
        assert "bonsaai_caddy_data" in source
        assert "bonsaai_caddy_config" in source
        assert "memory-runtime" not in source
        assert "bonsaai_qdrant_storage" not in source
        assert "qdrant_storage.tar.gz" not in source
        assert "ollama_models.txt" not in source


def test_upgrade_script_matches_overlay_service_names_and_cli_support() -> None:
    upgrade = UPGRADE_SCRIPT.read_text(encoding="utf-8")

    assert "docker compose version" in upgrade
    assert "docker-compose" in upgrade
    assert "build --pull executive-shell" in upgrade
    assert "memory-runtime" not in upgrade


def test_operations_runbooks_match_overlay_runtime_boundary() -> None:
    backup_guide = BACKUP_GUIDE.read_text(encoding="utf-8")
    operations_guide = OPERATIONS_GUIDE.read_text(encoding="utf-8")
    deployment_guide = DEPLOYMENT_GUIDE.read_text(encoding="utf-8")

    assert "caddy_config.tar.gz" in backup_guide
    assert "compose_services.txt" in backup_guide
    assert "qdrant_storage.tar.gz" not in backup_guide
    assert "ollama_models.txt" not in backup_guide

    assert "docker compose logs --tail=200 executive-shell" in operations_guide
    assert "docker-compose logs --tail=200 memory-runtime" not in operations_guide
    assert "Existing runtime dependencies reachable from `executive-shell`" in operations_guide

    assert "/home/<operator>/project-jebediah/docker/production" in deployment_guide
    assert "/home/cryptids/project-jebediah/docker/production" not in deployment_guide
