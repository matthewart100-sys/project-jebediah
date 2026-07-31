from collector.memory import MemoryItem, MemoryType
from collector.memory.pipeline.result import MemoryPipelineResult


def test_memory_pipeline_result_contract():

    memory = MemoryItem(
        id="memory-1",
        source_identity="test",
        content="User prefers red",
        memory_type=MemoryType.PREFERENCE,
        importance=0.9,
    )

    result = MemoryPipelineResult(
        memory=memory,
        accepted=True,
        consolidated=True,
        stored=True,
        reason="memory stored",
    )

    assert result.memory == memory
    assert result.accepted is True
    assert result.consolidated is True
    assert result.stored is True