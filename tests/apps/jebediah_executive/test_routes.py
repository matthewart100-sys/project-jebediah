"""Layer 4 - route resolution tests for the Executive Product Shell.

These tests prove that only the fixed route table and allowlisted subroutes
resolve, that resolution uses exact decoded values, and that traversal, encoded
traversal, backslashes, duplicate separators, null bytes, trailing slashes, and
unknown identifiers all fail to resolve (yielding a safe 404 at the application
layer).
"""

from __future__ import annotations

import pytest

from apps.jebediah_executive.routes import (
    ALLOWLISTED_PRESET_IDS,
    ALLOWLISTED_STATE_IDS,
    PRODUCT_ROUTES,
    resolve,
)

_FIXED_PAGES = [
    ("/", "overview"),
    ("/demo", "demo"),
    ("/knowledge-manager", "knowledge-manager"),
    ("/organizational-intelligence", "organizational-intelligence"),
    ("/organizational-memory", "organizational-memory"),
    ("/governance", "governance"),
    ("/audit", "audit"),
    ("/administration", "administration"),
    ("/attention", "attention"),
    ("/knowledge", "knowledge"),
    ("/next", "next"),
    ("/workspace", "workspace"),
    ("/ask", "ask"),
    ("/board", "board"),
    ("/states", "states"),
]


@pytest.mark.parametrize("path,route_id", _FIXED_PAGES)
def test_fixed_pages_resolve(path: str, route_id: str) -> None:
    resolution = resolve(path)
    assert resolution is not None
    assert resolution.route_id == route_id
    assert resolution.is_static is False
    assert resolution.render is not None


def test_stylesheet_resolves_as_static() -> None:
    resolution = resolve("/static/styles.css")
    assert resolution is not None
    assert resolution.route_id == "styles"
    assert resolution.is_static is True
    assert resolution.render is None


def test_product_routes_manifest_is_exact() -> None:
    assert PRODUCT_ROUTES == (
        "/",
        "/demo",
        "/knowledge-manager",
        "/organizational-intelligence",
        "/organizational-memory",
        "/governance",
        "/audit",
        "/administration",
        "/attention",
        "/knowledge",
        "/next",
        "/workspace",
        "/ask",
        "/board",
        "/states",
        "/static/styles.css",
    )


def test_allowlisted_presets_are_exact() -> None:
    assert set(ALLOWLISTED_PRESET_IDS) == {
        "grounded-priorities",
        "insufficient-program-outcomes",
        "failed-source-review",
    }


def test_allowlisted_states_are_exact() -> None:
    assert set(ALLOWLISTED_STATE_IDS) == {
        "ready",
        "loading",
        "empty",
        "partial",
        "stale",
        "insufficient-evidence",
        "held",
        "failed",
        "unauthorized",
        "unavailable",
        "disconnected",
    }


@pytest.mark.parametrize("preset", ALLOWLISTED_PRESET_IDS)
def test_ask_presets_resolve(preset: str) -> None:
    resolution = resolve(f"/ask/{preset}")
    assert resolution is not None
    assert resolution.route_id == "ask-preset"
    assert resolution.render is not None


@pytest.mark.parametrize("state_id", ALLOWLISTED_STATE_IDS)
def test_state_subroutes_resolve(state_id: str) -> None:
    resolution = resolve(f"/states/{state_id}")
    assert resolution is not None
    assert resolution.route_id == "state-detail"
    assert resolution.render is not None


@pytest.mark.parametrize(
    "path",
    [
        "/unknown",
        "/attention/",  # trailing slash, no alias
        "/ask",  # bare ask still resolves; handled separately
        "/ask/",  # empty preset
        "/ask/unknown-preset",
        "/states/",  # empty state
        "/states/unknown-state",
        "/states/insufficient_evidence",  # underscore form is not the route id
        "/ATTENTION",  # case-sensitive
        "/../attention",
        "/%2e%2e/attention",  # encoded traversal (decoded form still unknown)
        "//attention",  # duplicate separator
        "/attention//",  # duplicate trailing separator
        "\\attention",  # backslash
        "/attention\\x",
        "/next\x00",  # null byte
        "/static/styles.css/",  # trailing slash on static
        "/static/other.css",  # other file
        "/static/../models.py",  # traversal to source
    ],
)
def test_non_allowlisted_paths_do_not_resolve(path: str) -> None:
    if path == "/ask":
        # /ask is a legitimate fixed page; documented here for contrast.
        assert resolve(path) is not None
        return
    assert resolve(path) is None


def test_trailing_slash_has_no_alias() -> None:
    for path, _ in _FIXED_PAGES:
        if path == "/":
            continue
        assert resolve(path + "/") is None


def test_state_id_with_embedded_slash_rejected() -> None:
    assert resolve("/states/ready/extra") is None
    assert resolve("/ask/grounded-priorities/extra") is None
