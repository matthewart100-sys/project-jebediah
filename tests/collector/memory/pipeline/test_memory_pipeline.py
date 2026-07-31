from collector.memory import (
    MemoryItem,
    MemoryType,
)

from collector.memory.pipeline.memory_pipeline import (
    MemoryPipeline,
)


def test_memory_pipeline_promotes_memory():

    pipeline = MemoryPipeline()

    memory = MemoryItem(
        id="memory-1",
        source_identity="test",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    result = pipeline.process(memory)

    assert result.accepted is True
    assert result.consolidated is True
    assert result.stored is True


def test_memory_pipeline_rejects_duplicate():

    pipeline = MemoryPipeline()

    memory = MemoryItem(
        id="memory-2",
        source_identity="test",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    result = pipeline.process(
        memory,
        existing_content="User prefers red",
    )

    assert result.accepted is False
    assert result.stored is False