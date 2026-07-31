from dataclasses import dataclass

from .models import MemoryItem, MemoryType


@dataclass(frozen=True)
class MemoryDecision:
    accepted: bool
    reason: str
    memory: MemoryItem | None = None


class MemoryPolicy:
    """
    Determines whether collected information
    should become persistent memory.

    This layer does not know about:
    - Qdrant
    - embeddings
    - Ollama
    - APIs
    - databases
    """

    MIN_IMPORTANCE = 0.5

    def evaluate(
        self,
        memory: MemoryItem,
    ) -> MemoryDecision:

        if memory.importance < self.MIN_IMPORTANCE:
            return MemoryDecision(
                accepted=False,
                reason="importance below threshold",
            )

        if not memory.content.strip():
            return MemoryDecision(
                accepted=False,
                reason="empty memory content",
            )

        return MemoryDecision(
            accepted=True,
            reason="memory meets promotion criteria",
            memory=memory,
        )