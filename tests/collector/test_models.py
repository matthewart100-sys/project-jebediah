from datetime import datetime, timezone

import pytest

from collector.models import CollectorRecord


def valid_record() -> CollectorRecord:
    return CollectorRecord(
        source_type="chat",
        source_id="test-record-001",
        content="Project Jebediah test memory.",
        observed_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc),
        revision="1",
    )


def test_valid_record_is_created():
    record = valid_record()

    assert record.source_type == "chat"
    assert record.source_id == "test-record-001"
    assert record.content == "Project Jebediah test memory."


def test_empty_content_is_rejected():
    with pytest.raises(ValueError):
        CollectorRecord(
            source_type="chat",
            source_id="test-record-001",
            content="   ",
            observed_at=datetime.now(timezone.utc),
            submitted_at=datetime.now(timezone.utc),
            revision="1",
        )


def test_missing_source_id_is_rejected():
    with pytest.raises(ValueError):
        CollectorRecord(
            source_type="chat",
            source_id="",
            content="valid content",
            observed_at=datetime.now(timezone.utc),
            submitted_at=datetime.now(timezone.utc),
            revision="1",
        )