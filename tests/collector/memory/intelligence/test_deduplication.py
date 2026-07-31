from collector.memory.intelligence.deduplication import (
    MemoryDeduplicator,
)


def test_exact_memory_duplicate():

    deduplicator = MemoryDeduplicator()

    decision = deduplicator.evaluate(
        "User prefers red",
        "User prefers red",
    )

    assert decision.duplicate is True
    assert decision.similarity == 1.0


def test_similar_memory_detection():

    deduplicator = MemoryDeduplicator()

    decision = deduplicator.evaluate(
        "User prefers the color red",
        "User prefers red",
    )

    assert decision.similarity > 0.5


def test_distinct_memories():

    deduplicator = MemoryDeduplicator()

    decision = deduplicator.evaluate(
        "User prefers red",
        "User enjoys hiking",
    )

    assert decision.duplicate is False