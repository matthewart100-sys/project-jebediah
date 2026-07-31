from collector.runtime.result import CollectorResult
from collector.policy.decisions import StorageDecision
from collector.models import CollectorRecord
from datetime import datetime, timezone


def test_collector_result_creation():

    record = CollectorRecord(
        source_type="text",
        source_id="test",
        content="hello",
        observed_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc),
        revision="1",
        metadata={},
    )

    result = CollectorResult(
        record=record,
        decision=StorageDecision(
            action="store",
            reason="new record",
        ),
        stored=True,
    )

    assert result.stored is True