from .models import IntelligenceResult
from .scoring import MemoryScorer
from .confidence import ConfidenceEvaluator
from .deduplication import MemoryDeduplicator


class MemoryGovernor:
    """
    Central decision layer for memory intelligence.

    The governor does not store memories. It evaluates incoming memories and
    produces intelligence about how they should be treated.
    """

    def __init__(self):
        self.scorer = MemoryScorer()
        self.confidence = ConfidenceEvaluator()
        self.deduplicator = MemoryDeduplicator()

    def evaluate(
        self,
        memory_id: str,
        content: str,
        importance: float,
        source: str = "user",
        repeated: bool = False,
        existing_content: str | None = None,
    ) -> IntelligenceResult:
        score = self.scorer.score(
            importance=importance
        )

        confidence = self.confidence.evaluate(
            source=source,
            repeated=repeated,
        )

        if existing_content:
            duplicate = self.deduplicator.evaluate(
                existing_content,
                content,
            )

            if duplicate.duplicate:
                confidence = self.confidence.evaluate(
                    source="system",
                    repeated=True,
                )

        return IntelligenceResult(
            memory_id=memory_id,
            score=score,
            confidence=confidence,
        )
