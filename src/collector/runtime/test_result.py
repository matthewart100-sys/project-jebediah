from datetime import datetime, timezone

from collector.models import CollectorRecord
from collector.policy.decisions import StorageDecision
from collector.policy.storage_policy import StoragePolicyResult
from collector.runtime.result import CollectorResult


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
        decision=StoragePolicyResult(
            decision=StorageDecision.ACCEPT,
            reason="new record",
        ),
        stored=True,
    )

    assert result.stored is True
    assert result.decision.decision == StorageDecision.ACCEPT