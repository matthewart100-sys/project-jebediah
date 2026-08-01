import subprocess
import sys
from pathlib import Path


def test_memory_api_preserves_store_and_context_contracts():
    project_root = Path(__file__).resolve().parents[3]
    app_directory = (
        project_root
        / "services"
        / "jebediah-memory"
        / "app"
    )
    script = r'''
import sys
from types import ModuleType, SimpleNamespace


class FakeFastAPI:
    def __init__(self, **kwargs):
        self.metadata = kwargs

    def get(self, path):
        return lambda function: function

    def post(self, path):
        return lambda function: function


class FakePointStruct:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeQdrantClient:
    def __init__(self, **kwargs):
        self.upserts = []
        self.query_results = []

    def get_collections(self):
        return SimpleNamespace(
            collections=[SimpleNamespace(name="jebediah_memory")]
        )

    def create_collection(self, **kwargs):
        raise AssertionError("existing collection should not be recreated")

    def upsert(self, **kwargs):
        self.upserts.append(kwargs)

    def query_points(self, **kwargs):
        return SimpleNamespace(points=self.query_results)


class FakeEmbeddingAdapter:
    def __init__(self, **kwargs):
        self.options = kwargs

    def embed(self, text):
        return [0.0] * 768


fastapi = ModuleType("fastapi")
fastapi.FastAPI = FakeFastAPI
sys.modules["fastapi"] = fastapi

qdrant_client = ModuleType("qdrant_client")
qdrant_client.QdrantClient = FakeQdrantClient
qdrant_models = ModuleType("qdrant_client.models")
qdrant_models.PointStruct = FakePointStruct
qdrant_models.VectorParams = FakePointStruct
qdrant_models.FieldCondition = FakePointStruct
qdrant_models.Filter = FakePointStruct
qdrant_models.MatchValue = FakePointStruct
qdrant_models.Distance = SimpleNamespace(COSINE="cosine")
sys.modules["qdrant_client"] = qdrant_client
sys.modules["qdrant_client.models"] = qdrant_models

embeddings = ModuleType("embeddings")
embeddings.OllamaEmbeddingAdapter = FakeEmbeddingAdapter
sys.modules["embeddings"] = embeddings

import main

legacy_stored = main.store_memory(
    main.MemoryRequest(
        source_identity="legacy-synthetic-source",
        content="Synthetic legacy API memory.",
        memory_type="fact",
        importance=0.9,
    )
)

assert legacy_stored["status"] == "stored"
assert legacy_stored["payload"]["source_identity"] == (
    "legacy-synthetic-source"
)
assert legacy_stored["payload"]["provenance"]["source"] == "user"
assert legacy_stored["payload"]["lifecycle"]["state"] == "active"

stored = main.store_memory(
    main.MemoryRequest(
        source_identity="synthetic-source",
        content="Synthetic API memory.",
        memory_type="fact",
        importance=0.9,
        creator="synthetic-user",
        creation_context="API contract test",
        supporting_evidence=("fixture:evidence-1",),
    )
)

assert stored["status"] == "stored"
assert {
    "status",
    "memory_id",
    "pipeline",
    "intelligence",
    "vector_dimensions",
    "payload",
}.issubset(stored)
assert stored["pipeline"] == {
    "accepted": True,
    "consolidated": True,
    "stored": True,
}
assert stored["payload"]["provenance"]["creator"] == "synthetic-user"
assert stored["payload"]["provenance"]["confidence_basis"] == (
    "explicit user statement"
)
assert stored["payload"]["provenance"]["verification_state"] == "unverified"
assert stored["payload"]["lifecycle"]["state"] == "active"
assert main.qdrant.upserts

main.qdrant.query_results = [
    SimpleNamespace(
        score=0.2,
        payload={"content": "lower", "importance": 1.0},
    ),
    SimpleNamespace(
        score=0.9,
        payload={"content": "higher", "importance": 0.1},
    ),
]
context = main.memory_context(
    main.ContextRequest(
        source_identity="synthetic-query",
        content="Synthetic query.",
        memory_type="context",
        importance=0.5,
    )
)

assert set(context) == {"query", "memories"}
assert context["query"] == "Synthetic query."
assert [item["score"] for item in context["memories"]] == [0.9, 0.2]
assert all(
    set(item) == {"score", "content", "metadata"}
    for item in context["memories"]
)
'''

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=app_directory,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_service_qdrant_repository_round_trip_is_compatible():
    project_root = Path(__file__).resolve().parents[3]
    app_directory = (
        project_root
        / "services"
        / "jebediah-memory"
        / "app"
    )
    script = r'''
from qdrant_client import QdrantClient

from collector.memory import MemoryItem, MemoryType
from collector.memory.governance import MemoryLifecycleState
from collector.memory.persistence import qdrant_repository as module

client = QdrantClient(location=":memory:")
module.QdrantClient = lambda **kwargs: client
repository = module.QdrantMemoryRepository(
    url="http://synthetic.invalid",
    collection_name="synthetic-service-round-trip",
)
memory = MemoryItem(
    id="application-memory-id",
    source_identity="synthetic-service-source",
    content="Synthetic service Qdrant round trip.",
    memory_type=MemoryType.FACT,
    importance=0.9,
)

assert repository.save(memory) == "application-memory-id"
restored = repository.find("application-memory-id")
assert restored is not None
assert restored.id == "application-memory-id"
assert restored.provenance is not None
assert restored.provenance.source == "synthetic-service-source"
assert restored.lifecycle.state == MemoryLifecycleState.ACTIVE

client.close()
'''

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=app_directory,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
