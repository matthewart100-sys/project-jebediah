from typing import Protocol, Sequence

from .models import RetrievalCandidate


class RetrievalRanker(Protocol):
    def rank(
        self,
        candidates: Sequence[RetrievalCandidate],
    ) -> list[RetrievalCandidate]: ...


class SemanticRetrievalRanker:
    """
    Preserves the current semantic-relevance ordering.

    Future rankers can consume the other retrieval signals without coupling
    the public API to a ranking formula in Sprint 004.
    """

    def rank(
        self,
        candidates: Sequence[RetrievalCandidate],
    ) -> list[RetrievalCandidate]:
        return sorted(
            candidates,
            key=lambda item: item.signals.semantic_relevance,
            reverse=True,
        )
