from collector.memory.intelligence import (
    MemoryScorer,
    RetentionLevel,
)


def test_high_importance_memory_gets_high_retention():

    scorer = MemoryScorer()

    result = scorer.score(
        importance=0.9
    )

    assert result.importance == 0.9
    assert result.retention == RetentionLevel.HIGH


def test_medium_importance_memory_gets_medium_retention():

    scorer = MemoryScorer()

    result = scorer.score(
        importance=0.6
    )

    assert result.retention == RetentionLevel.MEDIUM


def test_low_importance_memory_gets_low_retention():

    scorer = MemoryScorer()

    result = scorer.score(
        importance=0.2
    )

    assert result.retention == RetentionLevel.LOW