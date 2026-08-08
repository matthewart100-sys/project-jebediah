from __future__ import annotations

from pathlib import Path

import pytest

from apps.jebediah_executive.auth import AuthRuntime


def test_bootstrap_admin_initializes_existing_empty_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    assert AuthRuntime(tmp_path).users == ()

    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")

    runtime = AuthRuntime(tmp_path)

    assert len(runtime.users) == 1
    assert runtime.users[0].email == "admin@example.com"
    assert runtime.users[0].role == "platform_administrator"


def test_bootstrap_admin_survives_restart_without_bootstrap_secret(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")
    AuthRuntime(tmp_path)

    monkeypatch.delenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL")
    monkeypatch.delenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD")
    restarted = AuthRuntime(tmp_path)

    result = restarted.login(
        email="admin@example.com",
        password="AdminPassword!234",
        remember_device=False,
    )

    assert result.error is None
    assert result.session is not None


def test_malformed_store_is_not_replaced_by_bootstrap_credentials(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    auth_dir = tmp_path / "auth"
    auth_dir.mkdir()
    (auth_dir / "users.json").write_text("not-json", encoding="utf-8")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")

    runtime = AuthRuntime(tmp_path)

    assert runtime.users == ()
    assert (auth_dir / "users.json").read_text(encoding="utf-8") == "not-json"
