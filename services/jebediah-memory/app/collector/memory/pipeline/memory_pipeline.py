from ..models import MemoryItem
from ..consolidation.engine import MemoryConsolidationEngine
from ..consolidation.models import ConsolidationAction
from ..runtime.memory_service import MemoryService

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
    Memory Service
        |
        v
    Repository

    This layer coordinates existing contracts.
    It does not make intelligence decisions itself.
    """

    def __init__(
        self,
        consolidation_engine=None,
        memory_service=None,
    ):
        self.consolidation_engine = (
            consolidation_engine
            or MemoryConsolidationEngine()
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

        decision = self.consolidation_engine.evaluate(
            memory,
            existing_content=existing_content,
        )

        if decision.action != ConsolidationAction.PROMOTE:
            return MemoryPipelineResult(
                memory=memory,
                accepted=False,
                consolidated=False,
                stored=False,
                reason=decision.reason,
            )

        result = self.memory_service.process(
            memory
        )

        return MemoryPipelineResult(
            memory=memory,
            accepted=True,
            consolidated=True,
            stored=result.stored,
            reason=decision.reason,
        )