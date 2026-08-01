from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

from qdrant_client import QdrantClient

from collector.memory import MemoryItem, MemoryType
from collector.memory.governance import (
    MemoryLifecycleState,
    VerificationState,
)
from collector.memory.persistence.qdrant_repository import (
    QdrantMemoryRepository,
)
from collector.memory.persistence import qdrant_repository as repository_module


class FakeQdrantClient:
    def __init__(self):
        self.points = []
        self.retrieved = []

    def upsert(self, collection_name, points):
        self.collection_name = collection_name
        self.points = points

    def retrieve(self, collection_name, ids):
        return self.retrieved


def make_repository():
    repository = QdrantMemoryRepository.__new__(
        QdrantMemoryRepository
    )
    repository.client = FakeQdrantClient()
    repository.collection_name = "synthetic-memory"
    return repository


def test_qdrant_save_adds_governance_without_removing_existing_fields():
    repository = make_repository()
    memory_id = str(uuid4())
    memory = MemoryItem(
        id=memory_id,
        source_identity="synthetic-source",
        content="Synthetic persisted memory.",
        memory_type=MemoryType.FACT,
        importance=0.9,
    )

    assert repository.save(memory) == memory_id

    payload = repository.client.points[0].payload
    assert payload["source_identity"] == "synthetic-source"
    assert payload["content"] == "Synthetic persisted memory."
    assert payload["metadata"] == {}
    assert payload["provenance"]["source"] == "synthetic-source"
    assert payload["provenance"]["verification_state"] == "unverified"
    assert payload["lifecycle"]["state"] == "active"


def test_qdrant_find_reads_legacy_payload_with_safe_defaults():
    repository = make_repository()
    point_id = str(uuid4())
    repository.client.retrieved = [
        SimpleNamespace(
            id=point_id,
            payload={
                "source_identity": "legacy-source",
                "content": "Synthetic legacy memory.",
                "memory_type": "fact",
                "importance": 0.8,
                "created_at": datetime(
                    2026,
                    7,
                    31,
                    tzinfo=timezone.utc,
                ).isoformat(),
                "metadata": {},
            },
        )
    ]

    memory = repository.find(point_id)

    assert memory is not None
    assert memory.provenance is not None
    assert memory.provenance.source == "legacy-source"
    assert (
        memory.provenance.verification_state
        == VerificationState.UNVERIFIED
    )
    assert memory.lifecycle.state == MemoryLifecycleState.ACTIVE


def test_qdrant_local_storage_round_trip_preserves_governance(
    monkeypatch,
):
    client = QdrantClient(location=":memory:")
    monkeypatch.setattr(
        repository_module,
        "QdrantClient",
        lambda **kwargs: client,
    )
    repository = QdrantMemoryRepository(
        url="http://synthetic.invalid",
        collection_name="synthetic-round-trip",
    )
    memory_id = str(uuid4())
    memory = MemoryItem(
        id=memory_id,
        source_identity="round-trip-source",
        content="Synthetic Qdrant round trip.",
        memory_type=MemoryType.FACT,
        importance=0.85,
    )

    repository.save(memory)
    restored = repository.find(memory_id)

    assert restored is not None
    assert restored.content == memory.content
    assert restored.provenance is not None
    assert restored.provenance.source == "round-trip-source"
    assert restored.lifecycle.state == MemoryLifecycleState.ACTIVE

    client.close()
