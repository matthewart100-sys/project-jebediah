from ..models import MemoryItem
from ..intelligence.scoring import MemoryScorer
from ..intelligence.confidence import ConfidenceEvaluator
from ..intelligence.deduplication import MemoryDeduplicator

from .models import (
    ConsolidationAction,
    ConsolidationDecision,
)


class MemoryConsolidationEngine:
    """
    Coordinates memory intelligence decisions.

    Responsibilities:
    - calculate importance score
    - calculate confidence
    - detect duplicates
    - produce final consolidation decision

    This layer does not:
    - store memories
    - use databases
    - call Qdrant
    - call Ollama
    """


    def __init__(
        self,
        scorer=None,
        confidence=None,
        deduplicator=None,
    ):
        self.scorer = scorer or MemoryScorer()
        self.confidence = confidence or ConfidenceEvaluator()
        self.deduplicator = deduplicator or MemoryDeduplicator()


    def evaluate(
        self,
        memory: MemoryItem,
        existing_content: str | None = None,
    ) -> ConsolidationDecision:

        score_result = self.scorer.score(
            memory.importance
        )

        confidence_result = self.confidence.evaluate(
            source=memory.source_identity
        )

        duplicate = False

        if existing_content:
            duplicate = self.deduplicator.evaluate(
                existing_content,
                memory.content,
            ).duplicate


        score = score_result.importance
        confidence = confidence_result.value


        if duplicate:
            return ConsolidationDecision(
                action=ConsolidationAction.MERGE,
                score=score,
                confidence=confidence,
                duplicate=True,
                reason="memory duplicate detected",
            )


        if score < 0.5:
            return ConsolidationDecision(
                action=ConsolidationAction.REJECT,
                score=score,
                confidence=confidence,
                duplicate=False,
                reason="memory score below threshold",
            )


        if confidence < 0.5:
            return ConsolidationDecision(
                action=ConsolidationAction.REJECT,
                score=score,
                confidence=confidence,
                duplicate=False,
                reason="memory confidence below threshold",
            )


        return ConsolidationDecision(
            action=ConsolidationAction.PROMOTE,
            score=score,
            confidence=confidence,
            duplicate=False,
            reason="memory passed consolidation checks",
        )