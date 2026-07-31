import os
import uuid
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

    Qdrant IDs are storage identifiers.
    Memory IDs remain application identifiers.
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
                    size=768,
                    distance=Distance.COSINE,
                ),
            )


    def save(
        self,
        memory: MemoryItem,
    ) -> str:

        qdrant_id = str(uuid.uuid4())


        vector = [0.0] * 768


        payload = {
            "memory_id": memory.id,
            "source_identity": memory.source_identity,
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "importance": memory.importance,
            "created_at": (
                memory.created_at.isoformat()
            ),
            "metadata": memory.metadata,
        }


        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=qdrant_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )


        return memory.id


    def find(
        self,
        memory_id: str,
    ) -> MemoryItem | None:

        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {
                        "key": "memory_id",
                        "match": {
                            "value": memory_id
                        }
                    }
                ]
            },
            limit=1,
        )[0]


        if not results:
            return None


        point = results[0]


        return MemoryItem(
            id=point.payload["memory_id"],
            source_identity=point.payload["source_identity"],
            content=point.payload["content"],
            memory_type=MemoryType(
                point.payload["memory_type"]
            ),
            importance=point.payload["importance"],
            created_at=datetime.fromisoformat(
                point.payload["created_at"]
            ),
            metadata=point.payload.get(
                "metadata",
                {},
            ),
        )


    def contains(
        self,
        memory_id: str,
    ) -> bool:

        return (
            self.find(memory_id)
            is not None
        )
