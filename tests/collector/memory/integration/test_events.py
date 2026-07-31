from collector.memory.integration.events import MemoryCandidateEvent


def test_memory_candidate_event_contract():

    event = MemoryCandidateEvent(
        source_identity="collector-test",
        content="User prefers red",
    )

    assert event.source_identity == "collector-test"
    assert event.content == "User prefers red"
    assert event.metadata == {}