from datetime import datetime, timezone

from collector.identity import generate_revision_id
from collector.models import CollectorRecord


def build_record(metadata=None):
    return CollectorRecord(
        source_type="chat",
        source_id="identity-test",
        content="Deterministic identity test.",
        observed_at=datetime(
            2026,
            7,
            31,
            tzinfo=timezone.utc,
        ),
        submitted_at=datetime(
            2026,
            7,
            31,
            tzinfo=timezone.utc,
        ),
        revision="1",
        metadata=metadata or {},
    )


def test_same_record_generates_same_identity():
    first = generate_revision_id(build_record())
    second = generate_revision_id(build_record())

    assert first == second


def test_metadata_order_does_not_change_identity():
    first = generate_revision_id(
        build_record(
            {
                "a": "1",
                "b": "2",
            }
        )
    )

    second = generate_revision_id(
        build_record(
            {
                "b": "2",
                "a": "1",
            }
        )
    )

    assert first == second


def test_revision_change_changes_identity():
    first = generate_revision_id(build_record())

    changed = build_record()
    changed.revision = "2"

    second = generate_revision_id(changed)

    assert first != second