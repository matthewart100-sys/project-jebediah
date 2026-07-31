import os
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)

from .repository import MemoryRepository
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


        point = PointStruct(
            id=memory.id,

            vector=[
                memory.importance
            ],

            payload={
                "source_identity": memory.source_identity,
                "content": memory.content,
                "memory_type": memory.memory_type.value,
                "importance": memory.importance,
                "created_at": (
                    memory.created_at.isoformat()
                ),
                "metadata": memory.metadata,
            },
        )


        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                point
            ],
        )


        return memory.id



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


        return MemoryItem(
            id=str(point.id),

            source_identity=(
                point.payload["source_identity"]
            ),

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
