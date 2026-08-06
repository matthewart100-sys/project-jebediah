from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID

import pytest
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    UpdateStatus,
    VectorParams,
)

from collector.embeddings import (
    EmbeddingCompatibilityError,
    EmbeddingIdentity,
    EmbeddingVectorError,
)
from collector.memory import MemoryItem, MemoryType
from collector.memory.governance import (
    MemoryLifecycleState,
    VerificationState,
)
from collector.memory.persistence.qdrant_repository import (
    QdrantCollectionCompatibilityError,
    QdrantMemoryRepository,
    QdrantWriteOutcomeUnknown,
    QdrantWriteRejectedError,
)


APPROVED_IDENTITY = EmbeddingIdentity.approved()
APPROVED_VECTOR = [0.25] * 768


def memory(memory_id="application-memory-id"):
    return MemoryItem(
        id=memory_id,
        source_identity="synthetic-source",
        content="Synthetic persisted memory.",
        memory_type=MemoryType.FACT,
        importance=0.9,
        created_at=datetime(2026, 7, 31, tzinfo=timezone.utc),
    )


class FakeQdrantClient:
    def __init__(self, *, status=UpdateStatus.COMPLETED, upsert_error=None):
        self.status = status
        self.upsert_error = upsert_error
        self.upserts = []
        self.retrieved = []
        self.inventory = []
        self.reconciliation_matches = []
        self.query_results = []
        self.query_calls = []

    def collection_exists(self, collection_name):
        return True

    def get_collection(self, collection_name):
        return SimpleNamespace(
            config=SimpleNamespace(
                params=SimpleNamespace(
                    vectors=VectorParams(size=768, distance=Distance.COSINE)
                )
            )
        )

    def scroll(self, **kwargs):
        if kwargs.get("scroll_filter") is None:
            return self.inventory, None
        return self.reconciliation_matches, None

    def upsert(self, **kwargs):
        self.upserts.append(kwargs)
        if self.upsert_error:
            raise self.upsert_error
        return SimpleNamespace(status=self.status)

    def retrieve(self, **kwargs):
        return self.retrieved

    def query_points(self, **kwargs):
        self.query_calls.append(kwargs)
        return SimpleNamespace(points=self.query_results)


def test_acknowledged_index_is_one_point_write_with_full_payload():
    client = FakeQdrantClient()
    repository = QdrantMemoryRepository(client=client)

    result = repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert result.memory_id == "application-memory-id"
    assert result.vector_dimensions == 768
    assert result.reconciled is False
    UUID(result.point_id)
    assert result.point_id != result.memory_id
    assert len(client.upserts) == 1
    assert client.upserts[0]["wait"] is True
    point = client.upserts[0]["points"][0]
    assert point.vector == APPROVED_VECTOR
    assert point.payload == result.payload
    assert result.payload["memory_id"] == result.memory_id
    assert result.payload["provenance"]["source"] == "synthetic-source"
    assert result.payload["provenance"]["verification_state"] == "unverified"
    assert result.payload["lifecycle"]["state"] == "active"
    assert result.payload["embedding_model"] == "nomic-embed-text:v1.5"
    assert result.payload["embedding_identity"] == APPROVED_IDENTITY.to_payload()


def test_non_completed_write_is_unknown_and_never_retried():
    client = FakeQdrantClient(status=UpdateStatus.ACKNOWLEDGED)
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantWriteOutcomeUnknown):
        repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert len(client.upserts) == 1


def test_confirmed_rejection_is_failure_and_never_success():
    client = FakeQdrantClient(status="rejected")
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantWriteRejectedError):
        repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert len(client.upserts) == 1


def test_lost_acknowledgement_is_reconciled_by_generated_point_identity():
    client = FakeQdrantClient(upsert_error=TimeoutError("synthetic timeout"))

    def upsert_then_timeout(**kwargs):
        client.upserts.append(kwargs)
        point = kwargs["points"][0]
        client.retrieved = [SimpleNamespace(id=point.id, payload=point.payload)]
        raise TimeoutError("synthetic timeout")

    client.upsert = upsert_then_timeout
    repository = QdrantMemoryRepository(client=client)

    result = repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert result.reconciled is True
    assert result.point_id == client.upserts[0]["points"][0].id
    assert len(client.upserts) == 1


def test_lost_acknowledgement_without_readback_remains_unknown():
    client = FakeQdrantClient(upsert_error=TimeoutError("synthetic timeout"))
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantWriteOutcomeUnknown):
        repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert len(client.upserts) == 1


def test_mismatched_readback_never_confirms_success():
    client = FakeQdrantClient(upsert_error=TimeoutError("synthetic timeout"))
    client.retrieved = [
        SimpleNamespace(
            id="synthetic-point",
            payload={"memory_id": "application-memory-id"},
        )
    ]
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantWriteOutcomeUnknown):
        repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert len(client.upserts) == 1


def test_lost_acknowledgement_reconciles_by_application_memory_id():
    client = FakeQdrantClient(upsert_error=TimeoutError("synthetic timeout"))
    expected_payload = QdrantMemoryRepository._payload_for(
        memory(),
        APPROVED_IDENTITY,
    )
    client.reconciliation_matches = [
        SimpleNamespace(
            id="reconciled-point-id",
            payload=expected_payload,
        )
    ]
    repository = QdrantMemoryRepository(client=client)

    result = repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert result.reconciled is True
    assert result.point_id == "reconciled-point-id"
    assert len(client.upserts) == 1


@pytest.mark.parametrize(
    "vector",
    ([0.0] * 768, [1.0], [1.0] * 767 + [float("nan")]),
)
def test_incompatible_vector_never_writes(vector):
    client = FakeQdrantClient()
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(EmbeddingVectorError):
        repository.index(memory(), vector, APPROVED_IDENTITY)

    assert not client.upserts


def test_identity_mismatch_never_writes():
    client = FakeQdrantClient()
    repository = QdrantMemoryRepository(client=client)
    incompatible = EmbeddingIdentity(
        provider="ollama",
        model="nomic-embed-text:latest",
        manifest_digest="sha256:unknown",
        dimensions=768,
        normalization="none",
    )

    with pytest.raises(EmbeddingCompatibilityError):
        repository.index(memory(), APPROVED_VECTOR, incompatible)

    assert not client.upserts


def test_save_alias_never_fabricates_a_placeholder_vector():
    repository = QdrantMemoryRepository(client=FakeQdrantClient())

    with pytest.raises(EmbeddingCompatibilityError):
        repository.save(memory())


def test_existing_unknown_vector_identity_blocks_new_writes():
    client = FakeQdrantClient()
    client.inventory = [
        SimpleNamespace(
            id="legacy-point",
            payload={"embedding_model": "nomic-embed-text:latest"},
            vector=APPROVED_VECTOR,
        )
    ]
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantCollectionCompatibilityError):
        repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)

    assert not client.upserts


@pytest.mark.parametrize(
    ("identity_payload", "vector"),
    [
        (None, APPROVED_VECTOR),
        (
            {
                **APPROVED_IDENTITY.to_payload(),
                "manifest_digest": "sha256:" + "f" * 64,
            },
            APPROVED_VECTOR,
        ),
        (
            {
                **APPROVED_IDENTITY.to_payload(),
                "normalization": "l2",
            },
            APPROVED_VECTOR,
        ),
        (APPROVED_IDENTITY.to_payload(), [0.25] * 767),
        (APPROVED_IDENTITY.to_payload(), [0.0] * 768),
    ],
)
def test_post_scan_incompatible_point_blocks_semantic_search(
    identity_payload,
    vector,
):
    client = FakeQdrantClient()
    repository = QdrantMemoryRepository(client=client)
    repository.verify_vector_space()
    client.inventory = [
        SimpleNamespace(
            id="post-scan-point",
            payload={"embedding_identity": identity_payload},
            vector=vector,
        )
    ]

    with pytest.raises(QdrantCollectionCompatibilityError):
        repository.search(APPROVED_VECTOR, APPROVED_IDENTITY)

    assert not client.query_calls


@pytest.mark.parametrize(
    ("identity_payload", "vector"),
    [
        (None, APPROVED_VECTOR),
        (
            {
                **APPROVED_IDENTITY.to_payload(),
                "manifest_digest": "sha256:" + "f" * 64,
            },
            APPROVED_VECTOR,
        ),
        (
            {
                **APPROVED_IDENTITY.to_payload(),
                "normalization": "l2",
            },
            APPROVED_VECTOR,
        ),
        (APPROVED_IDENTITY.to_payload(), [0.25] * 767),
        (APPROVED_IDENTITY.to_payload(), [0.0] * 768),
    ],
)
def test_returned_semantic_candidate_requires_approved_identity_and_vector(
    identity_payload,
    vector,
):
    client = FakeQdrantClient()
    client.query_results = [
        SimpleNamespace(
            id="concurrent-point",
            payload={
                "memory_id": "concurrent-memory",
                "content": "Synthetic concurrent memory.",
                "embedding_identity": identity_payload,
            },
            vector=vector,
            score=0.9,
        )
    ]
    repository = QdrantMemoryRepository(client=client)

    with pytest.raises(QdrantCollectionCompatibilityError):
        repository.search(APPROVED_VECTOR, APPROVED_IDENTITY)

    assert len(client.query_calls) == 1
    assert client.query_calls[0]["with_vectors"] is True


def test_incompatible_collection_geometry_fails_without_recreation():
    client = QdrantClient(location=":memory:")
    client.create_collection(
        collection_name="synthetic-placeholder",
        vectors_config=VectorParams(size=1, distance=Distance.COSINE),
    )

    with pytest.raises(QdrantCollectionCompatibilityError):
        QdrantMemoryRepository(
            client=client,
            collection_name="synthetic-placeholder",
        )

    assert client.get_collection("synthetic-placeholder").points_count == 0
    client.close()


def test_incompatible_collection_distance_fails_without_recreation():
    client = QdrantClient(location=":memory:")
    client.create_collection(
        collection_name="synthetic-dot-product",
        vectors_config=VectorParams(size=768, distance=Distance.DOT),
    )

    with pytest.raises(QdrantCollectionCompatibilityError):
        QdrantMemoryRepository(
            client=client,
            collection_name="synthetic-dot-product",
        )

    assert client.get_collection("synthetic-dot-product").points_count == 0
    client.close()


def test_missing_default_collection_is_created_with_exact_schema(monkeypatch):
    monkeypatch.delenv("COLLECTION_NAME", raising=False)
    client = QdrantClient(location=":memory:")

    repository = QdrantMemoryRepository(client=client)
    vectors = client.get_collection(
        "jebediah_memory"
    ).config.params.vectors

    assert repository.collection_name == "jebediah_memory"
    assert vectors.size == 768
    assert vectors.distance == Distance.COSINE
    client.close()


def test_qdrant_round_trip_preserves_governance_and_application_identity():
    client = QdrantClient(location=":memory:")
    repository = QdrantMemoryRepository(
        client=client,
        collection_name="synthetic-round-trip",
    )

    result = repository.index(memory(), APPROVED_VECTOR, APPROVED_IDENTITY)
    restored = repository.find("application-memory-id")

    assert restored is not None
    assert restored.id == "application-memory-id"
    assert restored.content == "Synthetic persisted memory."
    assert restored.provenance is not None
    assert restored.provenance.source == "synthetic-source"
    assert restored.lifecycle.state == MemoryLifecycleState.ACTIVE
    assert repository.contains(result.memory_id)
    client.close()


def test_legacy_root_payload_is_readable_without_claiming_vector_compatibility():
    client = QdrantClient(location=":memory:")
    collection = "synthetic-legacy-read"
    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    client.upsert(
        collection_name=collection,
        wait=True,
        points=[
            PointStruct(
                id="51e69e38-b1fd-4cab-a9e7-247473e24738",
                vector=APPROVED_VECTOR,
                payload={
                    "source_identity": "legacy-source",
                    "content": "Synthetic legacy memory.",
                    "memory_type": "fact",
                    "importance": 0.8,
                    "created_at": datetime(
                        2026, 7, 31, tzinfo=timezone.utc
                    ).isoformat(),
                    "metadata": {"additive": "preserved on retrieval"},
                },
            )
        ],
    )
    repository = QdrantMemoryRepository(
        client=client,
        collection_name=collection,
    )

    restored = repository.find("51e69e38-b1fd-4cab-a9e7-247473e24738")

    assert restored is not None
    assert restored.id == "51e69e38-b1fd-4cab-a9e7-247473e24738"
    assert restored.provenance is not None
    assert restored.provenance.source == "legacy-source"
    assert restored.provenance.verification_state == VerificationState.UNVERIFIED
    assert restored.lifecycle.state == MemoryLifecycleState.ACTIVE
    with pytest.raises(QdrantCollectionCompatibilityError):
        repository.search(APPROVED_VECTOR, APPROVED_IDENTITY)
    client.close()


def test_semantic_search_maps_candidates_without_hidden_weighting():
    client = QdrantClient(location=":memory:")
    repository = QdrantMemoryRepository(
        client=client,
        collection_name="synthetic-search",
    )
    high = memory("high-semantic")
    low = MemoryItem(
        **{
            **memory("low-semantic").__dict__,
            "importance": 1.0,
            "content": "Low semantic relevance.",
        }
    )
    repository.index(high, APPROVED_VECTOR, APPROVED_IDENTITY)
    repository.index(low, [-0.25] * 768, APPROVED_IDENTITY)

    candidates = repository.search(
        APPROVED_VECTOR,
        APPROVED_IDENTITY,
        limit=5,
    )

    assert [candidate.memory_id for candidate in candidates] == [
        "high-semantic",
        "low-semantic",
    ]
    assert (
        candidates[0].signals.semantic_relevance
        > candidates[1].signals.semantic_relevance
    )
    client.close()


@pytest.mark.parametrize(
    "payload_change",
    [
        {"content": None},
        {"memory_type": "invalid"},
        {"created_at": "invalid"},
    ],
)
def test_invalid_required_payload_fields_fail_visibly(payload_change):
    payload = QdrantMemoryRepository._payload_for(
        memory(),
        APPROVED_IDENTITY,
    )
    payload.update(payload_change)
    if "content" in payload_change and payload_change["content"] is None:
        del payload["content"]
    point = SimpleNamespace(id="point-id", payload=payload)

    with pytest.raises((KeyError, ValueError)):
        QdrantMemoryRepository._memory_from_point(point)
