from datetime import datetime, timezone

from collector.models import CollectorRecord
from collector.policy import (
    StorageDecision,
    StoragePolicy,
)


def make_record(revision="1"):
    now = datetime.now(timezone.utc)

    return CollectorRecord(
        source_type="text",
        source_id="test-001",
        content="hello",
        observed_at=now,
        submitted_at=now,
        revision=revision,
        metadata={},
    )


def test_accepts_new_record():

    result = StoragePolicy().evaluate(
        incoming=make_record()
    )

    assert result.decision == StorageDecision.ACCEPT


def test_detects_duplicate():

    record = make_record()

    result = StoragePolicy().evaluate(
        incoming=record,
        existing=record,
    )

    assert result.decision == StorageDecision.DUPLICATE


def test_detects_new_revision():

    result = StoragePolicy().evaluate(
        incoming=make_record("2"),
        existing=make_record("1"),
    )

    assert result.decision == StorageDecision.UPDATE