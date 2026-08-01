import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_MEMORY = PROJECT_ROOT / "src" / "collector" / "memory"
SERVICE = PROJECT_ROOT / "services" / "jebediah-memory"


def test_service_app_contains_no_shadow_domain_or_embedding_package():
    python_files = sorted(
        path.relative_to(SERVICE / "app")
        for path in (SERVICE / "app").rglob("*.py")
    )

    assert python_files == [Path("main.py")]


def test_canonical_memory_domain_has_no_service_or_http_dependency():
    forbidden = ("fastapi", "services.jebediah", "Dockerfile")

    for path in CANONICAL_MEMORY.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert not any(value in source for value in forbidden), path


def test_fastapi_layer_composes_adapters_without_direct_qdrant_logic():
    main_path = SERVICE / "app" / "main.py"
    tree = ast.parse(main_path.read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }

    assert "qdrant_client" not in imported_modules
    assert not {
        "PointStruct",
        "VectorParams",
        "RetrievalCandidate",
        "SemanticRetrievalRanker",
        "MemoryGovernor",
    }.intersection(imported_names)
    assert "MemoryApplicationService" in imported_names
    assert "QdrantMemoryRepository" in imported_names


def test_service_packaging_installs_canonical_package_on_python_3_12():
    dockerfile = (SERVICE / "Dockerfile").read_text(encoding="utf-8")
    compose = (SERVICE / "docker-compose.yml").read_text(encoding="utf-8")

    assert "FROM python:3.12-slim" in dockerfile
    assert "COPY src ./src" in dockerfile
    assert "COPY pyproject.toml uv.lock ./" in dockerfile
    assert "uv sync --frozen --no-dev --group service --no-editable" in dockerfile
    assert "COPY services/jebediah-memory/app/main.py ./main.py" in dockerfile
    assert "PYTHONPATH" not in dockerfile
    assert "context: ../.." in compose
    assert "nomic-embed-text:v1.5" in compose
    assert ":latest" not in compose
