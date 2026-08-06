"""Layer 8 - package boundary and capability tests.

These tests statically enforce the ADR-0015 local preview boundary: the
``apps.jebediah_executive`` package depends only on the Python standard library
and its own modules, declares no networking client, persistence, subprocess,
dynamic-import, or evaluation capability, never imports collector / memory /
vector / model-serving components, and matches the exact accepted file
manifest. They read source as text and parse it with :mod:`ast`; they never
import or execute the modules under test for capability checks.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
APP_DIR = REPO_ROOT / "apps" / "jebediah_executive"
APPS_PKG_INIT = REPO_ROOT / "apps" / "__init__.py"
TEST_DIR = REPO_ROOT / "tests" / "apps" / "jebediah_executive"
OPERATOR_GUIDE = (
    REPO_ROOT / "docs" / "ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_LOCAL_PREVIEW.md"
)

# Exact accepted manifest (source side).
EXPECTED_APP_FILES = {
    "__init__.py",
    "__main__.py",
    "auth.py",
    "app.py",
    "fixtures.py",
    "governed_provider.py",
    "models.py",
    "rendering.py",
    "routes.py",
}
EXPECTED_STATIC_FILES = {"styles.css"}
EXPECTED_TEST_FILES = {
    "__init__.py",
    "test_accessibility.py",
    "test_app.py",
    "test_fixtures.py",
    "test_governed_provider.py",
    "test_models.py",
    "test_package_boundaries.py",
    "test_rendering.py",
    "test_routes.py",
}

# Roots that must never be imported directly by the application package.
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        # Networking / outbound clients.
        "socket",
        "ssl",
        "http",
        "urllib",
        "ftplib",
        "smtplib",
        "asyncio",
        "requests",
        "httpx",
        "urllib3",
        "aiohttp",
        # Subprocess / native execution.
        "subprocess",
        "multiprocessing",
        "ctypes",
        "signal",
        # Persistence / databases.
        "sqlite3",
        "dbm",
        "shelve",
        "pickle",
        "marshal",
        "sqlalchemy",
        "redis",
        "psycopg2",
        "pymongo",
        # Web frameworks / servers beyond the stdlib wsgiref reference server.
        "fastapi",
        "starlette",
        "flask",
        "django",
        "uvicorn",
        "gunicorn",
        # Project runtime / collector / memory / vector / model serving.
        "jebediah",
        "jebediah_memory",
        "qdrant_client",
        "qdrant",
        "ollama",
        "numpy",
        "pandas",
    }
)

FORBIDDEN_CALL_NAMES = frozenset({"eval", "exec", "compile", "__import__", "open"})
FORBIDDEN_DOTTED_CALLS = frozenset(
    {
        "os.system",
        "os.popen",
        "importlib.import_module",
        "subprocess.run",
        "subprocess.Popen",
        "subprocess.call",
        "socket.socket",
    }
)


def _app_source_files() -> list[Path]:
    return sorted(APP_DIR.glob("*.py")) + [APPS_PKG_INIT]


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _dotted_name(node: ast.expr) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def test_app_package_manifest_is_exact() -> None:
    present = {p.name for p in APP_DIR.glob("*.py")}
    assert present == EXPECTED_APP_FILES
    static = {p.name for p in (APP_DIR / "static").iterdir() if p.is_file()}
    assert static == EXPECTED_STATIC_FILES


def test_test_package_manifest_is_exact() -> None:
    present = {p.name for p in TEST_DIR.glob("*.py")}
    assert present == EXPECTED_TEST_FILES


def test_no_unexpected_subpackages() -> None:
    subdirs = {p.name for p in APP_DIR.iterdir() if p.is_dir() and p.name != "__pycache__"}
    assert subdirs == {"static"}


# ---------------------------------------------------------------------------
# Import boundary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", _app_source_files(), ids=lambda p: p.name)
def test_imports_are_stdlib_or_package_local(path: Path) -> None:
    tree = _parse(path)
    stdlib = sys.stdlib_module_names
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root == "collector":
                    assert path.name == "governed_provider.py", f"{path.name}: {alias.name}"
                    continue
                if root == "urllib" and path.name == "governed_provider.py":
                    assert alias.name in {"urllib.request", "urllib.error"}, (
                        f"{path.name}: {alias.name}"
                    )
                    continue
                assert root not in FORBIDDEN_IMPORT_ROOTS, f"{path.name}: {alias.name}"
                assert root in stdlib or root == "apps", f"{path.name}: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # package-local relative import
            module = node.module or ""
            root = module.split(".")[0]
            if module == "urllib.parse":
                assert path.name == "app.py", f"{path.name}: {module}"
                continue
            if module in {"urllib.request", "urllib.error"}:
                assert path.name == "governed_provider.py", f"{path.name}: {module}"
                continue
            if root == "collector":
                assert path.name == "governed_provider.py", f"{path.name}: {module}"
                continue
            assert root not in FORBIDDEN_IMPORT_ROOTS, f"{path.name}: {module}"
            assert root in stdlib or root == "apps", f"{path.name}: {module}"


# ---------------------------------------------------------------------------
# Capability boundary
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", _app_source_files(), ids=lambda p: p.name)
def test_no_forbidden_call_capabilities(path: Path) -> None:
    tree = _parse(path)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            assert func.id not in FORBIDDEN_CALL_NAMES, f"{path.name}: {func.id}("
        elif isinstance(func, ast.Attribute):
            dotted = _dotted_name(func)
            assert dotted not in FORBIDDEN_DOTTED_CALLS, f"{path.name}: {dotted}("
            # getattr(self, ...) reflection over the module's own dataclass is
            # allowed; setattr/delattr mutation is not.
            assert func.attr not in {"system", "popen"}, f"{path.name}: {dotted}"


@pytest.mark.parametrize("path", _app_source_files(), ids=lambda p: p.name)
def test_single_bounded_resource_read(path: Path) -> None:
    """Only bounded local resource reads are permitted in the app package."""
    source = path.read_text(encoding="utf-8")
    if path.name == "app.py":
        assert source.count(".read_bytes(") <= 1
        assert ".read_text(" not in source or "styles.css" in source
    elif path.name == "governed_provider.py":
        # Workspace mode persistence reads one local workspace-state JSON file.
        assert source.count(".read_text(") <= 1
        assert source.count(".write_text(") <= 1
    elif path.name == "auth.py":
        # Authentication runtime persists one bounded local user ledger.
        assert source.count(".read_text(") <= 1
        assert source.count(".write_text(") <= 1
    else:
        assert ".read_bytes(" not in source
        assert ".read_text(" not in source


def test_no_wildcard_imports() -> None:
    for path in _app_source_files():
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.ImportFrom):
                assert not any(a.name == "*" for a in node.names), path.name


def test_operator_launch_uses_no_package_manager_or_bytecode_cache() -> None:
    guide = OPERATOR_GUIDE.read_text(encoding="utf-8")
    assert "python -B -m apps.jebediah_executive --port 8765" in guide
    assert "uv run" not in guide


def test_application_initializes_without_site_packages_or_bytecode() -> None:
    cache_state_before = {
        path: (path.stat().st_mtime_ns, path.stat().st_size)
        for path in REPO_ROOT.rglob("*.pyc")
    }
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("VIRTUAL_ENV", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-S",
            "-c",
            "from apps.jebediah_executive.app import create_app; create_app()",
        ],
        cwd=REPO_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    cache_state_after = {
        path: (path.stat().st_mtime_ns, path.stat().st_size)
        for path in REPO_ROOT.rglob("*.pyc")
    }
    assert cache_state_after == cache_state_before
