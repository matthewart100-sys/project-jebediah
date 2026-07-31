from collector.memory.models import MemoryItem, MemoryType
from collector.memory.pipeline.memory_pipeline import MemoryPipeline

from .events import MemoryCandidateEvent


class CollectorMemoryBridge:
    """
    Connects collector events to the memory pipeline.

    Responsibilities:
    - translate collector events into memory objects
    - pass candidates into the memory pipeline
    - return pipeline decisions

    This layer does not:
    - score memories
    - store memories
    - access Qdrant
    - create embeddings
    """

    def __init__(
        self,
        pipeline=None,
    ):
        self.pipeline = pipeline or MemoryPipeline()


    def process(
        self,
        event: MemoryCandidateEvent,
        importance: float = 0.5,
        memory_type: MemoryType = MemoryType.CONTEXT,
        existing_content: str | None = None,
    ):

        memory = MemoryItem(
            id=f"{event.source_identity}:memory",
            source_identity=event.source_identity,
            content=event.content,
            memory_type=memory_type,
            importance=importance,
            metadata=event.metadata,
        )

        return self.pipeline.process(
            memory,
            existing_content=existing_content,
        )