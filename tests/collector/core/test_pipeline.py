from collector.core.pipeline import process_record


def test_pipeline_processes_record():

    result = process_record(
        source_type="chat",
        source_id="test-001",
        content="  Hello   Jebediah ",
        revision="1",
        metadata={
            "b": "2",
            "a": "1",
        },
    )

    assert result.record.content == "Hello Jebediah"
    assert result.record.metadata == {
        "a": "1",
        "b": "2",
    }

    assert result.provenance.source_id == "test-001"
    assert len(result.identity) == 64
