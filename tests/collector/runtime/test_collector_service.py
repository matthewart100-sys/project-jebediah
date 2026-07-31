from collector.runtime import CollectorService
from collector.policy.decisions import StorageDecision


def test_collector_service_ingests_record():

    service = CollectorService()

    result = service.ingest(
        source_type="text",
        source_id="hello.txt",
        content="  Hello Jebediah ",
        revision="1",
    )

    assert result.stored is True
    assert result.record.content == "Hello Jebediah"
    assert result.decision.decision == StorageDecision.ACCEPT