from collector.memory import MemoryItem, MemoryType
from collector.memory.runtime import MemoryService


def test_memory_service_promotes_and_stores():

    service = MemoryService()

    memory = MemoryItem(
        id="memory-1",
        source_identity="test-source",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    result = service.process(memory)

    assert result.promoted is True
    assert result.stored is True