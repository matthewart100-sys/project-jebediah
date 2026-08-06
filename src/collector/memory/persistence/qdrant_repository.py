import os
from datetime import datetime
from numbers import Real
from typing import Any, Sequence
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    UpdateStatus,
    VectorParams,
)

from collector.embeddings import (
    APPROVED_VECTOR_DIMENSIONS,
    EmbeddingCompatibilityError,
    EmbeddingIdentity,
    validate_embedding_vector,
)

from .repository import MemoryIndexWriteResult
from ..governance import (
    ensure_memory_governance,
    lifecycle_from_payload,
    lifecycle_to_payload,
    provenance_from_payload,
    provenance_to_payload,
)
from ..models import MemoryItem, MemoryType
from ..retrieval import RetrievalCandidate


class QdrantRepositoryError(RuntimeError):
    """Base error for the canonical Qdrant boundary."""


class QdrantCollectionCompatibilityError(QdrantRepositoryError):
    """The configured collection cannot contain approved embeddings."""


class QdrantWriteRejectedError(QdrantRepositoryError):
    """Qdrant confirmed that a point write did not complete."""


class QdrantWriteOutcomeUnknown(QdrantRepositoryError):
    """A point write may have applied but could not be confirmed."""


class QdrantMemoryRepository:
    """One Qdrant path for durable memory payloads and semantic vectors."""

    def __init__(
        self,
        url: str | None = None,
        collection_name: str | None = None,
        client: Any | None = None,
    ):
        self.client = client or QdrantClient(
            url=url or os.getenv("QDRANT_URL", "http://qdrant:6333")
        )
        self.collection_name = collection_name or os.getenv(
            "COLLECTION_NAME",
            "jebediah_memory",
        )
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=APPROVED_VECTOR_DIMENSIONS,
                    distance=Distance.COSINE,
                ),
            )
            return

        info = self.client.get_collection(self.collection_name)
        vectors = info.config.params.vectors
        if isinstance(vectors, dict):
            raise QdrantCollectionCompatibilityError(
                "named-vector collections are incompatible"
            )

        size = getattr(vectors, "size", None)
        distance = getattr(vectors, "distance", None)
        distance_value = getattr(distance, "value", distance)
        if (
            size != APPROVED_VECTOR_DIMENSIONS
            or str(distance_value).lower() != "cosine"
        ):
            raise QdrantCollectionCompatibilityError(
                "Qdrant collection vector geometry is incompatible"
            )

    def verify_vector_space(self) -> None:
        """Prove all existing vectors declare the exact approved identity."""
        offset = None
        while True:
            points, offset = self.client.scroll(
                collection_name=self.collection_name,
                offset=offset,
                limit=256,
                with_payload=True,
                with_vectors=True,
            )
            for point in points:
                self._require_compatible_point(point, "existing")
            if offset is None:
                break

    def index(
        self,
        memory: MemoryItem,
        vector: Sequence[Real],
        embedding_identity: EmbeddingIdentity,
    ) -> MemoryIndexWriteResult:
        embedding_identity.require_approved()
        validated_vector = validate_embedding_vector(vector)
        self.verify_vector_space()

        governed_memory = ensure_memory_governance(memory)
        point_id = str(uuid4())
        payload = self._payload_for(governed_memory, embedding_identity)
        point = PointStruct(
            id=point_id,
            vector=validated_vector,
            payload=payload,
        )

        try:
            response = self.client.upsert(
                collection_name=self.collection_name,
                points=[point],
                wait=True,
            )
        except Exception as exc:
            status_code = getattr(exc, "status_code", None)
            if (
                isinstance(status_code, int)
                and 400 <= status_code < 500
                and status_code not in {408, 429}
            ):
                raise QdrantWriteRejectedError(
                    "Qdrant rejected the point write"
                ) from exc
            return self._reconcile_or_raise(
                point_id,
                governed_memory.id,
                payload,
                exc,
            )

        status = getattr(response, "status", None)
        status_value = getattr(status, "value", status)
        if status is UpdateStatus.COMPLETED or status_value == "completed":
            return MemoryIndexWriteResult(
                memory_id=governed_memory.id,
                point_id=point_id,
                vector_dimensions=len(validated_vector),
                payload=payload,
            )

        if status_value in {
            None,
            UpdateStatus.ACKNOWLEDGED.value,
            UpdateStatus.WAIT_TIMEOUT.value,
        }:
            return self._reconcile_or_raise(
                point_id,
                governed_memory.id,
                payload,
                QdrantWriteOutcomeUnknown(
                    "Qdrant did not acknowledge a completed point write"
                ),
            )

        raise QdrantWriteRejectedError(
            "Qdrant rejected the point write"
        )

    def save(
        self,
        memory: MemoryItem,
        vector: Sequence[Real] | None = None,
        embedding_identity: EmbeddingIdentity | None = None,
    ) -> str:
        """Compatibility alias that never fabricates a semantic vector."""
        if vector is None or embedding_identity is None:
            raise EmbeddingCompatibilityError(
                "Qdrant persistence requires an approved embedding"
            )
        return self.index(memory, vector, embedding_identity).memory_id

    def _reconcile_or_raise(
        self,
        point_id: str,
        memory_id: str,
        payload: dict[str, Any],
        cause: Exception,
    ) -> MemoryIndexWriteResult:
        try:
            records = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id],
                with_payload=True,
                with_vectors=False,
            )
        except Exception as reconciliation_error:
            raise QdrantWriteOutcomeUnknown(
                "Qdrant write outcome is unknown and reconciliation failed"
            ) from reconciliation_error

        if records:
            stored_payload = dict(records[0].payload or {})
            if stored_payload == payload:
                return MemoryIndexWriteResult(
                    memory_id=memory_id,
                    point_id=point_id,
                    vector_dimensions=APPROVED_VECTOR_DIMENSIONS,
                    payload=payload,
                    reconciled=True,
                )

        try:
            matches, _ = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="memory_id",
                            match=MatchValue(value=memory_id),
                        )
                    ]
                ),
                limit=2,
                with_payload=True,
                with_vectors=False,
            )
        except Exception as reconciliation_error:
            raise QdrantWriteOutcomeUnknown(
                "Qdrant write outcome is unknown and reconciliation failed"
            ) from reconciliation_error

        if (
            len(matches) == 1
            and dict(matches[0].payload or {}) == payload
        ):
            return MemoryIndexWriteResult(
                memory_id=memory_id,
                point_id=str(matches[0].id),
                vector_dimensions=APPROVED_VECTOR_DIMENSIONS,
                payload=payload,
                reconciled=True,
            )

        raise QdrantWriteOutcomeUnknown(
            "Qdrant write outcome is unknown; operator reconciliation is required"
        ) from cause

    def find(self, memory_id: str) -> MemoryItem | None:
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="memory_id",
                        match=MatchValue(value=memory_id),
                    )
                ]
            ),
            limit=2,
            with_payload=True,
            with_vectors=False,
        )
        if len(points) > 1:
            raise QdrantRepositoryError(
                "multiple Qdrant points share one application memory ID"
            )
        if points:
            return self._memory_from_point(points[0])

        legacy = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[memory_id],
            with_payload=True,
            with_vectors=False,
        )
        if not legacy:
            return None
        return self._memory_from_point(legacy[0])

    def contains(self, memory_id: str) -> bool:
        return self.find(memory_id) is not None

    def search(
        self,
        query_vector: Sequence[Real],
        embedding_identity: EmbeddingIdentity,
        limit: int = 5,
    ) -> list[RetrievalCandidate]:
        embedding_identity.require_approved()
        validated_vector = validate_embedding_vector(query_vector)
        self.verify_vector_space()

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=validated_vector,
            limit=limit,
            with_payload=True,
            with_vectors=True,
        )
        candidates = []
        for point in results.points:
            payload = dict(point.payload or {})
            self._require_compatible_point(point, "returned semantic")
            candidates.append(
                RetrievalCandidate.from_payload(
                    semantic_relevance=point.score,
                    payload=payload,
                )
            )
        return candidates

    @staticmethod
    def _require_compatible_point(point: Any, context: str) -> None:
        payload = dict(point.payload or {})
        try:
            identity = EmbeddingIdentity.from_payload(
                payload.get("embedding_identity")
            )
        except EmbeddingCompatibilityError as exc:
            raise QdrantCollectionCompatibilityError(
                f"{context} vector identity is incompatible"
            ) from exc
        if identity is None:
            raise QdrantCollectionCompatibilityError(
                f"{context} vector identity is unknown"
            )

        vector = getattr(point, "vector", None)
        if not isinstance(vector, (list, tuple)):
            raise QdrantCollectionCompatibilityError(
                f"{context} vector geometry cannot be verified"
            )
        try:
            validate_embedding_vector(vector)
        except ValueError as exc:
            raise QdrantCollectionCompatibilityError(
                f"{context} vector geometry is incompatible"
            ) from exc

    @staticmethod
    def _payload_for(
        memory: MemoryItem,
        embedding_identity: EmbeddingIdentity,
    ) -> dict[str, Any]:
        return {
            "memory_id": memory.id,
            "source_identity": memory.source_identity,
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "importance": memory.importance,
            "metadata": memory.metadata,
            "provenance": provenance_to_payload(
                memory.provenance,
                memory.source_identity,
            ),
            "lifecycle": lifecycle_to_payload(memory.lifecycle),
            "created_at": memory.created_at.isoformat(),
            "embedding_model": embedding_identity.model,
            "embedding_identity": embedding_identity.to_payload(),
            "service": "jebediah-memory",
        }

    @staticmethod
    def _memory_from_point(point: Any) -> MemoryItem:
        payload = dict(point.payload or {})
        source_identity = payload["source_identity"]
        memory_id = payload.get("memory_id", point.id)
        return MemoryItem(
            id=str(memory_id),
            source_identity=source_identity,
            content=payload["content"],
            memory_type=MemoryType(payload["memory_type"]),
            importance=payload["importance"],
            created_at=datetime.fromisoformat(payload["created_at"]),
            metadata=payload.get("metadata", {}),
            provenance=provenance_from_payload(
                payload.get("provenance"),
                source_identity,
            ),
            lifecycle=lifecycle_from_payload(payload.get("lifecycle")),
        )
