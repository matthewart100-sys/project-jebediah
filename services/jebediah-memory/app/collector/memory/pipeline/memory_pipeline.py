from dataclasses import replace

from ..models import MemoryItem
from ..consolidation.engine import MemoryConsolidationEngine
from ..consolidation.models import ConsolidationAction
from ..governance import ensure_memory_governance
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
    Intelligence Metadata Attachment
        |
        v
    Memory Service
        |
        v
    Repository
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


        source = (
            memory.provenance.source
            if memory.provenance
            else memory.source_identity
        )

        intelligence = self.governor.evaluate(
            memory_id=memory.id,
            content=memory.content,
            importance=memory.importance,
            source=source,
            existing_content=existing_content,
        )


        if intelligence.confidence.value < 0.5:
            return MemoryPipelineResult(
                memory=memory,
                accepted=False,
                consolidated=True,
                stored=False,
                reason="memory rejected by confidence evaluation",
            )


        intelligence_metadata = {
            **memory.metadata,
            "intelligence": {
                "retention": (
                    intelligence.score.retention.value
                ),
                "confidence": (
                    intelligence.confidence.value
                ),
                "confidence_reason": (
                    intelligence.confidence.reason
                ),
            },
        }


        enriched_memory = replace(
            memory,
            metadata=intelligence_metadata,
        )


        governed_memory = ensure_memory_governance(
            enriched_memory,
            confidence_basis=(
                intelligence.confidence.reason
            ),
        )


        result = self.memory_service.process(
            governed_memory
        )


        return MemoryPipelineResult(
            memory=result.memory,
            accepted=True,
            consolidated=True,
            stored=result.stored,
            reason=(
                f"{consolidation.reason}; "
                f"retention="
                f"{intelligence.score.retention.value}; "
                f"confidence="
                f"{intelligence.confidence.value}"
            ),
        )
