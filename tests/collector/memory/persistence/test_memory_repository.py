from collector.memory import (
    MemoryItem,
    MemoryType,
)

from collector.memory.persistence import (
    InMemoryMemoryRepository,
)


def test_memory_repository_stores_and_retrieves():

    repository = InMemoryMemoryRepository()

    memory = MemoryItem(
        id="memory-1",
        source_identity="record-1",
        content="Jebediah prefers deterministic design.",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    identity = repository.save(memory)

    assert identity == "memory-1"

    retrieved = repository.find(identity)

    assert retrieved is not None
    assert retrieved.content == memory.content


def test_memory_repository_checks_existence():

    repository = InMemoryMemoryRepository()

    assert repository.contains(
        "missing"
    ) is False