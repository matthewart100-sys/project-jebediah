from dataclasses import dataclass


@dataclass(frozen=True)
class DuplicateDecision:
    """
    Result of evaluating whether two memories
    represent the same underlying information.
    """

    duplicate: bool
    similarity: float
    reason: str


class MemoryDeduplicator:
    """
    Determines whether an incoming memory
    duplicates an existing memory.

    Version 1 intentionally avoids:
    - embeddings
    - Qdrant
    - Ollama
    - external similarity models

    Future versions can replace the similarity
    engine without changing the contract.
    """

    def __init__(
        self,
        threshold: float = 0.75,
    ):
        self.threshold = threshold


    def evaluate(
        self,
        existing_content: str,
        incoming_content: str,
    ) -> DuplicateDecision:

        existing = self._normalize(existing_content)
        incoming = self._normalize(incoming_content)

        if not existing or not incoming:
            return DuplicateDecision(
                duplicate=False,
                similarity=0.0,
                reason="empty content cannot be compared",
            )

        if existing == incoming:
            return DuplicateDecision(
                duplicate=True,
                similarity=1.0,
                reason="exact normalized match",
            )

        similarity = self._keyword_similarity(
            existing,
            incoming,
        )

        return DuplicateDecision(
            duplicate=similarity >= self.threshold,
            similarity=similarity,
            reason=(
                "keyword overlap exceeds threshold"
                if similarity >= self.threshold
                else "memories considered distinct"
            ),
        )


    def _normalize(
        self,
        value: str,
    ) -> str:

        return " ".join(
            value.lower()
            .strip()
            .split()
        )


    def _keyword_similarity(
        self,
        left: str,
        right: str,
    ) -> float:

        left_words = set(left.split())
        right_words = set(right.split())

        if not left_words or not right_words:
            return 0.0

        intersection = left_words & right_words
        union = left_words | right_words

        return len(intersection) / len(union)