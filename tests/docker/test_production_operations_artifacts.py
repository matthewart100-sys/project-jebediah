from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRODUCTION_COMPOSE = PROJECT_ROOT / "docker" / "production" / "docker-compose.yml"
PRODUCTION_ENV_EXAMPLE = PROJECT_ROOT / "docker" / "production" / ".env.example"
INTERACTION_COMPOSE = (
    PROJECT_ROOT / "services" / "jebediah-interaction" / "docker-compose.yml"
)
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


def test_production_overlay_requires_authenticated_access() -> None:
    compose = PRODUCTION_COMPOSE.read_text(encoding="utf-8")

    assert 'BONSAAI_REQUIRE_AUTH: "1"' in compose
    assert 'BONSAAI_ALLOW_DEMO_ANONYMOUS: "0"' in compose
    assert "BONSAAI_BOOTSTRAP_ADMIN_EMAIL:" in compose
    assert "BONSAAI_BOOTSTRAP_ADMIN_PASSWORD:" in compose


def test_production_environment_example_contains_only_safe_placeholders() -> None:
    values = {}
    for line in PRODUCTION_ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key] = value

    assert values["BONSAAI_INTERACTION_SERVICE_TOKEN"] == (
        "replace-with-private-service-token"
    )
    assert values["INTERACTION_SERVICE_TOKEN"] == (
        "replace-with-private-service-token"
    )
    assert values["INTERACTION_STATE_KEY"] == "replace-with-generated-fernet-key"
    assert values["BONSAAI_BOOTSTRAP_ADMIN_EMAIL"] == ""
    assert values["BONSAAI_BOOTSTRAP_ADMIN_PASSWORD"] == ""


def test_interaction_gateway_is_private_persistent_and_health_checked() -> None:
    compose = INTERACTION_COMPOSE.read_text(encoding="utf-8")

    assert "\n    ports:" not in compose
    assert '      - "8001"' in compose
    assert "jebediah_interaction_state:/var/lib/jebediah-interaction" in compose
    assert "http://127.0.0.1:8001/health" in compose
    assert "${INTERACTION_SERVICE_TOKEN:?set INTERACTION_SERVICE_TOKEN}" in compose
    assert "${INTERACTION_STATE_KEY:?set INTERACTION_STATE_KEY}" in compose


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
