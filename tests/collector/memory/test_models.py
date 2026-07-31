from collector.memory import MemoryItem, MemoryType


def test_memory_item_creation():

    memory = MemoryItem(
        id="memory-1",
        source_identity="record-1",
        content="Jebediah prefers careful architecture decisions.",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    assert memory.id == "memory-1"
    assert memory.memory_type == MemoryType.PREFERENCE
    assert memory.importance == 0.9