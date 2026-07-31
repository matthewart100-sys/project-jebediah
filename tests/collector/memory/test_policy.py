from collector.memory import (
    MemoryItem,
    MemoryPolicy,
    MemoryType,
)


def make_memory(
    importance=0.9,
    content="Jebediah prefers deterministic architecture.",
):
    return MemoryItem(
        id="memory-1",
        source_identity="record-1",
        content=content,
        memory_type=MemoryType.PREFERENCE,
        importance=importance,
    )


def test_memory_policy_accepts_important_memory():

    result = MemoryPolicy().evaluate(
        make_memory()
    )

    assert result.accepted is True
    assert result.memory is not None


def test_memory_policy_rejects_low_importance():

    result = MemoryPolicy().evaluate(
        make_memory(
            importance=0.1
        )
    )

    assert result.accepted is False
    assert result.reason == "importance below threshold"


def test_memory_policy_rejects_empty_content():

    result = MemoryPolicy().evaluate(
        make_memory(
            content=""
        )
    )

    assert result.accepted is False