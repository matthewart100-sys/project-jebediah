import os
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)

from .repository import MemoryRepository
from ..governance import (
    ensure_memory_governance,
    lifecycle_from_payload,
    lifecycle_to_payload,
    provenance_from_payload,
    provenance_to_payload,
)
from ..models import MemoryItem, MemoryType


class QdrantMemoryRepository(MemoryRepository):
    """
    Qdrant-backed memory persistence adapter.

    Stores promoted memories only.

    This adapter does NOT:
    - score memories
    - evaluate confidence
    - perform deduplication
    - create embeddings
    """


    def __init__(
        self,
        url: str | None = None,
        collection_name: str | None = None,
    ):

        self.client = QdrantClient(
            url=url
            or os.getenv(
                "QDRANT_URL",
                "http://qdrant:6333",
            )
        )

        self.collection_name = (
            collection_name
            or os.getenv(
                "COLLECTION_NAME",
                "jebediah_memory",
            )
        )

        self._ensure_collection()


    def _ensure_collection(self):

        collections = [
            c.name
            for c in self.client.get_collections().collections
        ]

        if self.collection_name not in collections:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1,
                    distance=Distance.COSINE,
                ),
            )


    def save(
        self,
        memory: MemoryItem,
    ) -> str:

        governed_memory = ensure_memory_governance(memory)


        point = PointStruct(
            id=governed_memory.id,

            vector=[
                governed_memory.importance
            ],

            payload={
                "source_identity": governed_memory.source_identity,
                "content": governed_memory.content,
                "memory_type": governed_memory.memory_type.value,
                "importance": governed_memory.importance,
                "created_at": (
                    governed_memory.created_at.isoformat()
                ),
                "metadata": governed_memory.metadata,
                "provenance": provenance_to_payload(
                    governed_memory.provenance,
                    governed_memory.source_identity,
                ),
                "lifecycle": lifecycle_to_payload(
                    governed_memory.lifecycle
                ),
            },
        )


        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                point
            ],
        )


        return governed_memory.id



    def find(
        self,
        memory_id: str,
    ) -> MemoryItem | None:


        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[
                memory_id
            ],
        )


        if not results:
            return None


        point = results[0]


        source_identity = point.payload["source_identity"]


        return MemoryItem(
            id=str(point.id),

            source_identity=source_identity,

            content=(
                point.payload["content"]
            ),

            memory_type=MemoryType(
                point.payload["memory_type"]
            ),

            importance=(
                point.payload["importance"]
            ),

            created_at=datetime.fromisoformat(
                point.payload["created_at"]
            ),

            metadata=(
                point.payload.get(
                    "metadata",
                    {},
                )
            ),

            provenance=provenance_from_payload(
                point.payload.get("provenance"),
                source_identity,
            ),

            lifecycle=lifecycle_from_payload(
                point.payload.get("lifecycle")
            ),
        )



    def contains(
        self,
        memory_id: str,
    ) -> bool:


        return bool(
            self.client.retrieve(
                collection_name=self.collection_name,
                ids=[
                    memory_id
                ],
            )
        )
