import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from collector.embeddings import OllamaEmbeddingProvider
from collector.memory.governance import MemoryProvenance
from collector.memory.models import MemoryItem, MemoryType
from collector.memory.persistence import QdrantMemoryRepository
from collector.memory.runtime.application_service import (
    MemoryApplicationService,
)


_memory_application_service: MemoryApplicationService | None = None


def build_memory_application_service() -> MemoryApplicationService:
    """Compose canonical domain adapters without duplicating their logic."""
    return MemoryApplicationService(
        embedding_provider=OllamaEmbeddingProvider(),
        repository=QdrantMemoryRepository(),
    )


def get_memory_application_service() -> MemoryApplicationService:
    global _memory_application_service
    if _memory_application_service is None:
        _memory_application_service = build_memory_application_service()
    return _memory_application_service


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_memory_application_service().ensure_ready()
    yield


app = FastAPI(
    title="Jebediah Memory Service",
    version="0.4.0",
    lifespan=lifespan,
)


class MemoryRequest(BaseModel):
    memory_id: str | None = Field(default=None, min_length=1, max_length=200)
    source_identity: str
    content: str
    memory_type: str
    importance: float
    source: str = "user"
    creator: str | None = None
    creation_context: str | None = None
    supporting_evidence: tuple[str, ...] = ()
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContextRequest(BaseModel):
    source_identity: str
    content: str
    memory_type: str
    importance: float
    organization_id: str | None = None
    workspace_mode: str | None = None
    approved_only: bool = False


@app.get("/health")
def health():
    return {
        "status": "online",
        "service": "jebediah-memory",
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/memory/store")
def store_memory(request: MemoryRequest):
    memory_id = request.memory_id or str(uuid.uuid4())

    try:
        memory_type = MemoryType(request.memory_type)
    except ValueError:
        memory_type = MemoryType.CONTEXT

    memory = MemoryItem(
        id=memory_id,
        source_identity=request.source_identity,
        content=request.content,
        memory_type=memory_type,
        importance=request.importance,
        provenance=MemoryProvenance(
            source=request.source,
            creator=request.creator,
            creation_context=request.creation_context,
            supporting_evidence=request.supporting_evidence,
        ),
        metadata=request.metadata,
    )
    result = get_memory_application_service().store(memory)
    pipeline_result = result.pipeline

    if not pipeline_result.stored:
        return {
            "status": "rejected",
            "reason": pipeline_result.reason,
            "memory_id": memory_id,
        }

    if result.write is None:
        raise RuntimeError("stored memory is missing its durable write result")

    stored_memory = pipeline_result.memory
    return {
        "status": "stored",
        "memory_id": stored_memory.id,
        "pipeline": {
            "accepted": pipeline_result.accepted,
            "consolidated": pipeline_result.consolidated,
            "stored": pipeline_result.stored,
        },
        "intelligence": stored_memory.metadata["intelligence"],
        "vector_dimensions": result.write.vector_dimensions,
        "payload": result.write.payload,
    }


@app.post("/memory/context")
def memory_context(request: ContextRequest):
    metadata_filter: dict[str, str] = {}
    if request.organization_id is not None:
        metadata_filter["organization_id"] = request.organization_id
    if request.workspace_mode is not None:
        metadata_filter["workspace_mode"] = request.workspace_mode
    if request.approved_only:
        metadata_filter["governance_state"] = "approved"
    candidates = get_memory_application_service().context(
        request.content,
        limit=5,
        metadata_filter=metadata_filter or None,
    )
    memories = [
        {
            "score": candidate.signals.semantic_relevance,
            "content": candidate.content,
            "metadata": dict(candidate.metadata.get("metadata") or {}),
        }
        for candidate in candidates
    ]
    return {
        "query": request.content,
        "memories": memories,
    }
