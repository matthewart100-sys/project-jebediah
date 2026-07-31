from collector.memory.runtime import MemoryServiceResult
from collector.memory import MemoryItem, MemoryType


def test_memory_service_result_contract():

    item = MemoryItem(
        id="memory-1",
        source_identity="test-source",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    result = MemoryServiceResult(
        memory=item,
        promoted=True,
        stored=True,
    )

    assert result.promoted is True
    assert result.stored is True