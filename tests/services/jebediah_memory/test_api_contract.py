import asyncio
import importlib.util
import subprocess
import sys
from pathlib import Path

import httpx

from collector.embeddings import EmbeddingIdentity
from collector.memory.persistence import MemoryIndexWriteResult
from collector.memory.persistence.qdrant_repository import QdrantMemoryRepository
from collector.memory.runtime.application_service import MemoryApplicationService


def test_memory_api_preserves_contracts_and_uses_one_canonical_path():
    project_root = Path(__file__).resolve().parents[3]
    script = r'''
import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from types import ModuleType


class FakeFastAPI:
    def __init__(self, **kwargs):
        self.metadata = kwargs

    def get(self, path):
        return lambda function: function

    def post(self, path):
        return lambda function: function


fastapi = ModuleType("fastapi")
fastapi.FastAPI = FakeFastAPI
sys.modules["fastapi"] = fastapi

main_path = (
    Path.cwd() / "services" / "jebediah-memory" / "app" / "main.py"
)
spec = importlib.util.spec_from_file_location("jebediah_memory_main", main_path)
main = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(main)

from collector.embeddings import EmbeddingIdentity, EmbeddingVectorError
from collector.memory.intelligence import MemoryGovernor
from collector.memory.persistence import MemoryIndexWriteResult
from collector.memory.persistence.qdrant_repository import QdrantMemoryRepository
from collector.memory.pipeline import MemoryPipeline
from collector.memory.retrieval import RetrievalCandidate
from collector.memory.runtime.application_service import MemoryApplicationService


class FakeEmbeddingProvider:
    def __init__(self, error=None):
        self.identity = EmbeddingIdentity.approved()
        self.error = error
        self.calls = []
        self.ready_calls = 0

    def ensure_ready(self):
        self.ready_calls += 1

    def embed(self, text):
        self.calls.append(text)
        if self.error:
            raise self.error
        return [0.25] * 768


class FakeRepository:
    def __init__(self, error=None):
        self.error = error
        self.index_calls = []
        self.search_calls = []
        self.search_results = []
        self.verify_calls = 0

    def verify_vector_space(self):
        self.verify_calls += 1

    def index(self, memory, vector, identity):
        self.index_calls.append((memory, vector, identity))
        if self.error:
            raise self.error
        payload = QdrantMemoryRepository._payload_for(memory, identity)
        return MemoryIndexWriteResult(
            memory_id=memory.id,
            point_id="synthetic-point-id",
            vector_dimensions=len(vector),
            payload=payload,
        )

    def search(self, vector, identity, limit):
        self.search_calls.append((vector, identity, limit))
        return self.search_results


class CountingGovernor:
    def __init__(self):
        self.delegate = MemoryGovernor()
        self.calls = []

    def evaluate(self, **kwargs):
        self.calls.append(kwargs)
        return self.delegate.evaluate(**kwargs)


provider = FakeEmbeddingProvider()
repository = FakeRepository()
governor = CountingGovernor()
main._memory_application_service = MemoryApplicationService(
    embedding_provider=provider,
    repository=repository,
    pipeline=MemoryPipeline(governor=governor),
)

health = main.health()
assert health["status"] == "online"
assert health["service"] == "jebediah-memory"
datetime.fromisoformat(health["time"])

rejected = main.store_memory(
    main.MemoryRequest(
        source_identity="synthetic-rejected-source",
        content="Synthetic rejected API memory.",
        memory_type="fact",
        importance=0.1,
    )
)
assert set(rejected) == {"status", "reason", "memory_id"}
assert rejected["status"] == "rejected"
assert not provider.calls
assert not repository.index_calls

legacy_stored = main.store_memory(
    main.MemoryRequest(
        source_identity="legacy-synthetic-source",
        content="Synthetic legacy API memory.",
        memory_type="fact",
        importance=0.9,
    )
)
assert legacy_stored["status"] == "stored"
assert legacy_stored["payload"]["source_identity"] == "legacy-synthetic-source"
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
assert stored["payload"]["provenance"]["confidence_basis"] == "explicit user statement"
assert stored["payload"]["provenance"]["verification_state"] == "unverified"
assert stored["payload"]["lifecycle"]["state"] == "active"
assert stored["payload"]["embedding_model"] == "nomic-embed-text:v1.5"
assert stored["payload"]["embedding_identity"] == provider.identity.to_payload()

fallback = main.store_memory(
    main.MemoryRequest(
        source_identity="synthetic-fallback-source",
        content="Synthetic fallback type memory.",
        memory_type="future-type",
        importance=0.9,
    )
)
assert fallback["payload"]["memory_type"] == "context"

assert len(governor.calls) == 3
assert len(provider.calls) == 3
assert len(repository.index_calls) == 3

repository.search_results = [
    RetrievalCandidate.from_payload(
        0.2, {"content": "lower", "importance": 1.0}
    ),
    RetrievalCandidate.from_payload(
        0.9, {"content": "higher", "importance": 0.1}
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
assert all(set(item) == {"score", "content", "metadata"} for item in context["memories"])
assert repository.search_calls[0][2] == 5

embedding_failure_repository = FakeRepository()
main._memory_application_service = MemoryApplicationService(
    FakeEmbeddingProvider(EmbeddingVectorError("synthetic embedding failure")),
    embedding_failure_repository,
)
try:
    main.store_memory(
        main.MemoryRequest(
            source_identity="synthetic-failure",
            content="Synthetic failure memory.",
            memory_type="fact",
            importance=0.9,
        )
    )
except EmbeddingVectorError:
    pass
else:
    raise AssertionError("embedding failure must remain visible")
assert not embedding_failure_repository.index_calls

qdrant_failure_provider = FakeEmbeddingProvider()
main._memory_application_service = MemoryApplicationService(
    qdrant_failure_provider,
    FakeRepository(RuntimeError("synthetic Qdrant failure")),
)
try:
    main.store_memory(
        main.MemoryRequest(
            source_identity="synthetic-failure",
            content="Synthetic failed write.",
            memory_type="fact",
            importance=0.9,
        )
    )
except RuntimeError:
    pass
else:
    raise AssertionError("Qdrant failure must not return stored success")
assert len(qdrant_failure_provider.calls) == 1

main._memory_application_service = MemoryApplicationService(
    FakeEmbeddingProvider(EmbeddingVectorError("synthetic query failure")),
    FakeRepository(),
)
try:
    main.memory_context(
        main.ContextRequest(
            source_identity="synthetic-query-failure",
            content="Synthetic failed query.",
            memory_type="context",
            importance=0.5,
        )
    )
except EmbeddingVectorError:
    pass
else:
    raise AssertionError("query embedding failure must not fabricate success")
'''

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_service_resolves_only_the_installed_canonical_memory_package():
    project_root = Path(__file__).resolve().parents[3]
    script = r'''
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


class FakeFastAPI:
    def __init__(self, **kwargs):
        pass

    def get(self, path):
        return lambda function: function

    def post(self, path):
        return lambda function: function


fastapi = ModuleType("fastapi")
fastapi.FastAPI = FakeFastAPI
sys.modules["fastapi"] = fastapi

import collector.memory
from collector.memory.models import MemoryItem

canonical_path = Path(collector.memory.__file__).resolve()
assert canonical_path.is_relative_to(Path.cwd() / "src" / "collector" / "memory")

main_path = Path.cwd() / "services" / "jebediah-memory" / "app" / "main.py"
spec = importlib.util.spec_from_file_location("jebediah_memory_main", main_path)
main = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(main)
assert main.MemoryItem is MemoryItem
assert main._memory_application_service is None
'''
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_fastapi_paths_validation_status_and_lifespan_are_compatible():
    project_root = Path(__file__).resolve().parents[3]
    main_path = (
        project_root / "services" / "jebediah-memory" / "app" / "main.py"
    )
    spec = importlib.util.spec_from_file_location(
        "jebediah_memory_http_contract",
        main_path,
    )
    assert spec is not None and spec.loader is not None
    main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main)

    class Provider:
        identity = EmbeddingIdentity.approved()

        def __init__(self):
            self.ready_calls = 0

        def ensure_ready(self):
            self.ready_calls += 1

        def embed(self, _text):
            return [0.25] * 768

    class Repository:
        def __init__(self):
            self.verify_calls = 0

        def verify_vector_space(self):
            self.verify_calls += 1

        def index(self, memory, vector, identity):
            return MemoryIndexWriteResult(
                memory_id=memory.id,
                point_id="synthetic-point-id",
                vector_dimensions=len(vector),
                payload=QdrantMemoryRepository._payload_for(memory, identity),
            )

        def search(self, vector, identity, limit):
            return []

    provider = Provider()
    repository = Repository()
    main._memory_application_service = MemoryApplicationService(
        provider,
        repository,
    )

    async def exercise_api():
        transport = httpx.ASGITransport(app=main.app)
        async with main.lifespan(main.app):
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://synthetic.test",
            ) as client:
                health = await client.get("/health")
                assert health.status_code == 200
                assert health.json()["status"] == "online"

                invalid = await client.post(
                    "/memory/store",
                    json={
                        "source_identity": "synthetic",
                        "content": "missing",
                    },
                )
                assert invalid.status_code == 422

                rejected = await client.post(
                    "/memory/store",
                    json={
                        "source_identity": "synthetic",
                        "content": "Synthetic rejected memory.",
                        "memory_type": "fact",
                        "importance": 0.1,
                    },
                )
                assert rejected.status_code == 200
                assert rejected.json()["status"] == "rejected"

                stored = await client.post(
                    "/memory/store",
                    json={
                        "source_identity": "synthetic",
                        "content": "Synthetic stored memory.",
                        "memory_type": "future-type",
                        "importance": 0.9,
                    },
                )
                assert stored.status_code == 200
                assert stored.json()["status"] == "stored"
                assert stored.json()["payload"]["memory_type"] == "context"

                context = await client.post(
                    "/memory/context",
                    json={
                        "source_identity": "synthetic",
                        "content": "Synthetic context query.",
                        "memory_type": "context",
                        "importance": 0.5,
                    },
                )
                assert context.status_code == 200
                assert context.json() == {
                    "query": "Synthetic context query.",
                    "memories": [],
                }

    asyncio.run(exercise_api())

    assert provider.ready_calls == 1
    assert repository.verify_calls == 1
