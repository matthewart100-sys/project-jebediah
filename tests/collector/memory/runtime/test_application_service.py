import pytest

from collector.embeddings import (
    APPROVED_EMBEDDING_DIGEST,
    APPROVED_EMBEDDING_MODEL,
    EmbeddingConfigurationError,
    EmbeddingIdentity,
    EmbeddingVectorError,
    OllamaEmbeddingProvider,
)
from collector.memory import MemoryItem, MemoryType
from collector.memory.intelligence import MemoryGovernor
from collector.memory.persistence import MemoryIndexWriteResult
from collector.memory.pipeline import MemoryPipeline
from collector.memory.retrieval import RetrievalCandidate
from collector.memory.runtime.application_service import (
    MemoryApplicationService,
)


class FakeEmbeddingProvider:
    def __init__(self, vector=None, error=None):
        self.identity = EmbeddingIdentity.approved()
        self.vector = vector or [0.25] * 768
        self.error = error
        self.calls = []
        self.ready_calls = 0

    def ensure_ready(self):
        self.ready_calls += 1

    def embed(self, text):
        self.calls.append(text)
        if self.error:
            raise self.error
        return self.vector


class MutableOllamaClient:
    def __init__(
        self,
        digest=APPROVED_EMBEDDING_DIGEST.removeprefix("sha256:"),
    ):
        self.digest = digest
        self.embed_calls = []

    def list(self):
        return {
            "models": [
                {
                    "model": APPROVED_EMBEDDING_MODEL,
                    "digest": self.digest,
                }
            ]
        }

    def embed(self, **kwargs):
        self.embed_calls.append(kwargs)
        return {"embeddings": [[0.25] * 768]}


class FakeSemanticRepository:
    def __init__(self):
        self.index_calls = []
        self.search_calls = []
        self.search_results = []
        self.verify_calls = 0

    def verify_vector_space(self):
        self.verify_calls += 1

    def index(self, memory, vector, embedding_identity):
        self.index_calls.append((memory, vector, embedding_identity))
        return MemoryIndexWriteResult(
            memory_id=memory.id,
            point_id="point-id",
            vector_dimensions=len(vector),
            payload={"memory_id": memory.id},
        )

    def search(self, vector, embedding_identity, limit):
        self.search_calls.append((vector, embedding_identity, limit))
        return self.search_results


class CountingGovernor:
    def __init__(self):
        self.delegate = MemoryGovernor()
        self.calls = []

    def evaluate(self, **kwargs):
        self.calls.append(kwargs)
        return self.delegate.evaluate(**kwargs)


def memory(importance=0.9):
    return MemoryItem(
        id="application-memory-id",
        source_identity="synthetic-source",
        content="Synthetic application memory.",
        memory_type=MemoryType.FACT,
        importance=importance,
    )


def test_store_evaluates_embeds_and_writes_exactly_once():
    provider = FakeEmbeddingProvider()
    repository = FakeSemanticRepository()
    governor = CountingGovernor()
    service = MemoryApplicationService(
        embedding_provider=provider,
        repository=repository,
        pipeline=MemoryPipeline(governor=governor),
    )

    result = service.store(memory())

    assert len(governor.calls) == 1
    assert provider.calls == ["Synthetic application memory."]
    assert len(repository.index_calls) == 1
    assert result.pipeline.accepted is True
    assert result.pipeline.consolidated is True
    assert result.pipeline.stored is True
    assert result.write is not None
    assert result.write.memory_id == "application-memory-id"


def test_rejected_memory_never_embeds_or_writes():
    provider = FakeEmbeddingProvider()
    repository = FakeSemanticRepository()
    service = MemoryApplicationService(provider, repository)

    result = service.store(memory(importance=0.1))

    assert result.pipeline.accepted is False
    assert result.pipeline.stored is False
    assert result.write is None
    assert not provider.calls
    assert not repository.index_calls


def test_embedding_failure_never_writes_or_reports_success():
    provider = FakeEmbeddingProvider(
        error=EmbeddingVectorError("synthetic embedding failure")
    )
    repository = FakeSemanticRepository()
    service = MemoryApplicationService(provider, repository)

    with pytest.raises(EmbeddingVectorError):
        service.store(memory())

    assert not repository.index_calls


@pytest.mark.parametrize(
    "digest",
    [None, "", "not-a-digest", "a" * 63, "f" * 64],
)
def test_invalid_api_digest_fails_before_generation_or_persistence(digest):
    client = MutableOllamaClient(digest=digest)
    provider = OllamaEmbeddingProvider(client=client)
    repository = FakeSemanticRepository()
    service = MemoryApplicationService(provider, repository)

    with pytest.raises(EmbeddingConfigurationError):
        service.store(memory())

    assert not client.embed_calls
    assert not repository.index_calls


def test_model_digest_drift_fails_before_generation_or_persistence():
    client = MutableOllamaClient()
    provider = OllamaEmbeddingProvider(client=client)
    repository = FakeSemanticRepository()
    service = MemoryApplicationService(provider, repository)

    service.ensure_ready()
    client.digest = "f" * 64

    with pytest.raises(EmbeddingConfigurationError):
        service.store(memory())

    assert not client.embed_calls
    assert not repository.index_calls


def test_repository_failure_never_returns_stored_success():
    provider = FakeEmbeddingProvider()
    repository = FakeSemanticRepository()
    repository.index = lambda *args: (_ for _ in ()).throw(
        RuntimeError("synthetic repository failure")
    )
    service = MemoryApplicationService(provider, repository)

    with pytest.raises(RuntimeError):
        service.store(memory())

    assert provider.calls == ["Synthetic application memory."]


def test_context_ranking_remains_semantic_only():
    provider = FakeEmbeddingProvider()
    repository = FakeSemanticRepository()
    repository.search_results = [
        RetrievalCandidate.from_payload(
            0.2,
            {"memory_id": "low", "content": "low", "importance": 1.0},
        ),
        RetrievalCandidate.from_payload(
            0.9,
            {"memory_id": "high", "content": "high", "importance": 0.1},
        ),
    ]
    service = MemoryApplicationService(provider, repository)

    results = service.context("Synthetic query.")

    assert [candidate.memory_id for candidate in results] == ["high", "low"]
    assert len(repository.search_calls) == 1


def test_readiness_checks_both_dependencies():
    provider = FakeEmbeddingProvider()
    repository = FakeSemanticRepository()
    service = MemoryApplicationService(provider, repository)

    service.ensure_ready()

    assert provider.ready_calls == 1
    assert repository.verify_calls == 1
