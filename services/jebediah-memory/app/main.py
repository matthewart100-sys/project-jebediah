import os
import uuid

from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from embeddings import OllamaEmbeddingAdapter


app = FastAPI(
    title="Jebediah Memory Service",
    version="0.2.0"
)


QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "jebediah_memory"
)


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434"
)


client = QdrantClient(
    QDRANT_URL
)


embedding_service = OllamaEmbeddingAdapter(
    model="nomic-embed-text:latest",
    host="http://host.docker.internal:11434"
)

class MemoryRequest(BaseModel):

    source_identity: str

    content: str

    memory_type: str = "context"

    importance: float = 0.5



@app.get("/health")
def health():

    collections = client.get_collections()

    return {
        "status": "online",
        "service": "jebediah-memory",
        "qdrant": "connected",
        "collections": len(
            collections.collections
        )
    }



@app.post("/memory/store")
def store_memory(
    memory: MemoryRequest
):

    memory_id = str(
        uuid.uuid4()
    )


    vector = embedding_service.embed(
        memory.content
    )


    payload = {

        "memory_id": memory_id,

        "source_identity":
            memory.source_identity,

        "content":
            memory.content,

        "memory_type":
            memory.memory_type,

        "importance":
            memory.importance,

        "embedding_model":
            "nomic-embed-text:latest",

        "created_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "service":
            "jebediah-memory"
    }


    client.upsert(

        collection_name=
            COLLECTION_NAME,

        points=[

            PointStruct(

                id=memory_id,

                vector=vector,

                payload=payload
            )
        ]
    )


    return {

        "status":
            "stored",

        "memory_id":
            memory_id,

        "vector_dimensions":
            len(vector),

        "payload":
            payload
    }



@app.post("/memory/context")
def memory_context(
    request: MemoryRequest
):

    vector = embedding_service.embed(
        request.content
    )


    results = client.query_points(

        collection_name=
            COLLECTION_NAME,

        query=
            vector,

        limit=5,

        with_payload=True,

        with_vectors=False

    ).points



    memories = []


    for result in results:

        memories.append(

            {
                "score":
                    result.score,

                "content":
                    result.payload.get(
                        "content"
                    ),

                "metadata":
                    result.payload
            }

        )


    return {

        "query":
            request.content,

        "memories":
            memories
    }
