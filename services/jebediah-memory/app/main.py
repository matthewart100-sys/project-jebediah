import os
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)

from embeddings import OllamaEmbeddingAdapter

from collector.memory.models import (
    MemoryItem,
    MemoryType,
)

from collector.memory.pipeline.memory_pipeline import (
    MemoryPipeline,
)

from collector.memory.intelligence import (
    MemoryGovernor,
)


app = FastAPI(
    title="Jebediah Memory Service",
    version="0.4.0",
)


# ----------------------------
# External Services
# ----------------------------

qdrant = QdrantClient(
    url=os.getenv(
        "QDRANT_URL",
        "http://qdrant:6333",
    )
)


collection_name = os.getenv(
    "COLLECTION_NAME",
    "jebediah_memory",
)


embedding_service = OllamaEmbeddingAdapter(
    model="nomic-embed-text:latest"
)


memory_pipeline = MemoryPipeline()

memory_governor = MemoryGovernor()


# ----------------------------
# Ensure Collection
# ----------------------------

def ensure_collection():

    collections = [
        c.name
        for c in qdrant.get_collections().collections
    ]

    if collection_name not in collections:

        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )


ensure_collection()


# ----------------------------
# Models
# ----------------------------

class MemoryRequest(BaseModel):

    source_identity: str
    content: str
    memory_type: str
    importance: float



class ContextRequest(BaseModel):

    source_identity: str
    content: str
    memory_type: str
    importance: float



# ----------------------------
# Health
# ----------------------------

@app.get("/health")
def health():

    return {
        "status": "online",
        "service": "jebediah-memory",
        "time": datetime.now(
            timezone.utc
        ).isoformat(),
    }



# ----------------------------
# Store Memory
# ----------------------------

@app.post("/memory/store")
def store_memory(
    request: MemoryRequest,
):

    memory_id = str(
        uuid.uuid4()
    )


    try:

        memory_type = MemoryType(
            request.memory_type
        )

    except ValueError:

        memory_type = MemoryType.CONTEXT



    memory = MemoryItem(
        id=memory_id,
        source_identity=request.source_identity,
        content=request.content,
        memory_type=memory_type,
        importance=request.importance,
    )


    # Run intelligence layer

    intelligence = memory_governor.evaluate(
        memory_id=memory.id,
        content=memory.content,
        importance=memory.importance,
        source="user",
    )


    memory.metadata.update(
        {
            "intelligence":
            {
                "retention":
                    intelligence.score.retention.value,

                "confidence":
                    intelligence.confidence.value,

                "confidence_reason":
                    intelligence.confidence.reason,
            }
        }
    )


    # Run collector pipeline

    pipeline_result = memory_pipeline.process(
        memory
    )


    if not pipeline_result.stored:

        return {
            "status": "rejected",
            "reason": pipeline_result.reason,
            "memory_id": memory_id,
        }


    vector = embedding_service.embed(
        request.content
    )


    payload = {

        "memory_id": memory.id,

        "source_identity":
            memory.source_identity,

        "content":
            memory.content,

        "memory_type":
            memory.memory_type.value,

        "importance":
            memory.importance,

        "metadata":
            memory.metadata,

        "created_at":
            memory.created_at.isoformat(),

        "embedding_model":
            "nomic-embed-text:latest",

        "service":
            "jebediah-memory",
    }


    qdrant.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload,
            )
        ],
    )


    return {

        "status": "stored",

        "memory_id":
            memory.id,

        "pipeline":
        {
            "accepted":
                pipeline_result.accepted,

            "consolidated":
                pipeline_result.consolidated,

            "stored":
                pipeline_result.stored,
        },

        "intelligence":
            memory.metadata["intelligence"],

        "vector_dimensions":
            len(vector),

        "payload":
            payload,
    }



# ----------------------------
# Semantic Context Search
# ----------------------------

@app.post("/memory/context")
def memory_context(
    request: ContextRequest,
):

    vector = embedding_service.embed(
        request.content
    )


    results = qdrant.query_points(
        collection_name=collection_name,
        query=vector,
        limit=5,
        with_payload=True,
    )


    memories = []

    for point in results.points:

        memories.append(
            {
                "score":
                    point.score,

                "content":
                    point.payload.get(
                        "content"
                    ),

                "metadata":
                    point.payload,
            }
        )


    return {

        "query":
            request.content,

        "memories":
            memories,
    }
