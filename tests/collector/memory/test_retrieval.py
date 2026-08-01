from collector.memory.governance import MemoryLifecycleState
from collector.memory.retrieval import (
    RetrievalCandidate,
    SemanticRetrievalRanker,
)


def test_retrieval_candidate_exposes_future_ranking_signals():
    candidate = RetrievalCandidate.from_payload(
        semantic_relevance=0.72,
        payload={
            "memory_id": "memory-1",
            "content": "Synthetic retrieval candidate.",
            "importance": 0.9,
            "created_at": "2026-07-31T12:00:00+00:00",
            "metadata": {
                "intelligence": {
                    "confidence": 0.8,
                }
            },
            "lifecycle": {
                "state": "reinforced",
                "reinforcement_count": 1,
            },
        },
    )

    assert candidate.signals.semantic_relevance == 0.72
    assert candidate.signals.confidence == 0.8
    assert candidate.signals.importance == 0.9
    assert candidate.signals.created_at is not None
    assert (
        candidate.signals.lifecycle_state
        == MemoryLifecycleState.REINFORCED
    )


def test_semantic_ranker_preserves_current_relevance_order():
    lower_relevance = RetrievalCandidate.from_payload(
        semantic_relevance=0.2,
        payload={
            "memory_id": "important",
            "importance": 1.0,
            "lifecycle": {"state": "reinforced"},
        },
    )
    higher_relevance = RetrievalCandidate.from_payload(
        semantic_relevance=0.9,
        payload={
            "memory_id": "semantic",
            "importance": 0.1,
            "lifecycle": {"state": "archived"},
        },
    )

    ranked = SemanticRetrievalRanker().rank(
        [lower_relevance, higher_relevance]
    )

    assert [candidate.memory_id for candidate in ranked] == [
        "semantic",
        "important",
    ]


def test_legacy_retrieval_payload_defaults_to_active():
    candidate = RetrievalCandidate.from_payload(
        semantic_relevance=0.5,
        payload={"content": "Legacy synthetic memory."},
    )

    assert candidate.signals.confidence is None
    assert candidate.signals.importance is None
    assert candidate.signals.created_at is None
    assert candidate.signals.lifecycle_state == MemoryLifecycleState.ACTIVE
