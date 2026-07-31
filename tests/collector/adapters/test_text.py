from collector.adapters import adapt_text_record


def test_text_adapter_creates_processed_record():

    result = adapt_text_record(
        source_id="chat-001",
        content="  Hello   Jebediah ",
        revision="2",
        metadata={
            "source": "chat",
        },
    )

    assert result.record.source_type == "text"
    assert result.record.source_id == "chat-001"
    assert result.record.content == "Hello Jebediah"
    assert result.record.metadata["source"] == "chat"
    assert result.record.revision == "2"

    assert result.provenance.source_type == "text"
    assert result.identity