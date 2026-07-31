from collector.memory.models import (
    MemoryItem,
    MemoryType,
)

from collector.memory.consolidation.engine import (
    MemoryConsolidationEngine,
)

from collector.memory.consolidation.models import (
    ConsolidationAction,
)


def test_memory_consolidation_promotes_good_memory():

    engine = MemoryConsolidationEngine()

    memory = MemoryItem(
        id="memory-1",
        source_identity="test",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    decision = engine.evaluate(memory)

    assert decision.action == ConsolidationAction.PROMOTE
    assert decision.duplicate is False


def test_memory_consolidation_detects_duplicate():

    engine = MemoryConsolidationEngine()

    memory = MemoryItem(
        id="memory-2",
        source_identity="test",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    decision = engine.evaluate(
        memory,
        existing_content="User prefers red",
    )

    assert decision.action == ConsolidationAction.MERGE
    assert decision.duplicate is True