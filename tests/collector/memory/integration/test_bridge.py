from collector.memory.integration.events import MemoryCandidateEvent
from collector.memory.integration.collector_memory_bridge import (
    CollectorMemoryBridge,
)
from collector.memory.models import MemoryType


def test_collector_memory_bridge_promotes_memory():

    bridge = CollectorMemoryBridge()

    event = MemoryCandidateEvent(
        source_identity="collector-test",
        content="User prefers red",
    )

    result = bridge.process(
        event,
        importance=0.9,
        memory_type=MemoryType.PREFERENCE,
    )

    assert result.accepted is True
    assert result.consolidated is True
    assert result.stored is True
    assert result.memory.content == "User prefers red"



def test_collector_memory_bridge_rejects_duplicate():

    bridge = CollectorMemoryBridge()

    event = MemoryCandidateEvent(
        source_identity="collector-test",
        content="User prefers red",
    )

    result = bridge.process(
        event,
        importance=0.9,
        memory_type=MemoryType.PREFERENCE,
        existing_content="User prefers red",
    )

    assert result.accepted is False
    assert result.consolidated is False
    assert result.stored is False