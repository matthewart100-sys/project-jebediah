from collector.adapters import adapt_text_record
from collector.storage import InMemorySink


def test_memory_sink_stores_and_retrieves_record():

    record = adapt_text_record(
        source_id="memory-test",
        content="Hello storage",
        revision="1",
    )

    sink = InMemorySink()

    identity = sink.store(record)

    assert sink.exists(identity)

    retrieved = sink.get(identity)

    assert retrieved is not None
    assert retrieved.record.content == "Hello storage"