from ..models import MemoryItem
from ..consolidation.engine import MemoryConsolidationEngine
from ..consolidation.models import ConsolidationAction
from ..runtime.memory_service import MemoryService

from ..intelligence.governor import MemoryGovernor

from .result import MemoryPipelineResult


class MemoryPipeline:
    """
    Coordinates the complete memory lifecycle.

    Flow:

    MemoryItem
        |
        v
    Consolidation Engine
        |
        v
    Memory Governor
        |
        v
    Memory Service
        |
        v
    Repository

    The pipeline coordinates lifecycle decisions.
    Intelligence evaluation happens before storage.
    """

    def __init__(
        self,
        consolidation_engine=None,
        memory_service=None,
        governor=None,
    ):

        self.consolidation_engine = (
            consolidation_engine
            or MemoryConsolidationEngine()
        )

        self.governor = (
            governor
            or MemoryGovernor()
        )

        self.memory_service = (
            memory_service
            or MemoryService()
        )


    def process(
        self,
        memory: MemoryItem,
        existing_content: str | None = None,
    ) -> MemoryPipelineResult:

        consolidation = (
            self.consolidation_engine.evaluate(
                memory,
                existing_content=existing_content,
            )
        )


        if consolidation.action != ConsolidationAction.PROMOTE:
            return MemoryPipelineResult(
                memory=memory,
                accepted=False,
                consolidated=False,
                stored=False,
                reason=consolidation.reason,
            )


        intelligence = self.governor.evaluate(
            memory_id=memory.id,
            content=memory.content,
            importance=memory.importance,
            source=memory.source_identity,
            existing_content=existing_content,
        )


        if intelligence.confidence.value < 0.5:
            return MemoryPipelineResult(
                memory=memory,
                accepted=False,
                consolidated=True,
                stored=False,
                reason=(
                    "memory rejected by confidence evaluation"
                ),
            )


        result = self.memory_service.process(
            memory
        )


        return MemoryPipelineResult(
            memory=memory,
            accepted=True,
            consolidated=True,
            stored=result.stored,
            reason=(
                f"{consolidation.reason}; "
                f"retention={intelligence.score.retention.value}; "
                f"confidence={intelligence.confidence.value}"
            ),
        )
