from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from collector.document_admission import (
    ExpiredContent,
    SqliteDurableRepository,
    delete_submission,
    deny_if_expired,
    derive_audit_key,
    expire_and_cleanup,
    generate_master_key,
    generate_salt,
    synthetic_custody_policy,
    synthetic_retention_policy,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _repository(tmp_path: Path) -> SqliteDurableRepository:
    master_key = generate_master_key()
    audit_key = derive_audit_key(master_key, generate_salt())
    return SqliteDurableRepository(
        runtime_directory=tmp_path,
        master_key=master_key,
        audit_key=audit_key,
        custody_policy=synthetic_custody_policy(),
    )


def _store_sample(
    repository: SqliteDurableRepository,
    *,
    receipt_id: str,
    object_id: str,
    attempt_id: str,
    created_at: datetime,
) -> None:
    repository.reserve_receipt(receipt_id, created_at)
    repository.store(
        object_id=object_id,
        admission_attempt_id=attempt_id,
        receipt_id=receipt_id,
        plaintext=b"%PDF-1.7\n%%EOF",
        policy=synthetic_custody_policy(),
        retention=synthetic_retention_policy(),
        created_at=created_at,
    )


def test_deny_if_expired_raises_for_expired_record(tmp_path: Path):
    now = _now()
    with _repository(tmp_path) as repository:
        _store_sample(
            repository,
            receipt_id="receipt-1",
            object_id="object-1",
            attempt_id="attempt-1",
            created_at=now,
        )
        record = repository.get("object-1")
        assert record is not None

        with pytest.raises(ExpiredContent, match="retention_deadline_passed"):
            deny_if_expired(record, now + timedelta(seconds=61))


def test_expire_and_cleanup_tombstones_expired_records(tmp_path: Path):
    now = _now()
    with _repository(tmp_path) as repository:
        _store_sample(
            repository,
            receipt_id="receipt-2",
            object_id="object-2",
            attempt_id="attempt-2",
            created_at=now,
        )
        outcomes = expire_and_cleanup(
            repository,
            synthetic_retention_policy(),
            now + timedelta(seconds=61),
        )
        record = repository.get("object-2")

    assert outcomes and outcomes[0].deleted is True
    assert record is not None
    assert record.tombstoned_at is not None


def test_delete_submission_deletes_every_active_object(tmp_path: Path):
    now = _now()
    with _repository(tmp_path) as repository:
        _store_sample(
            repository,
            receipt_id="receipt-3",
            object_id="object-3",
            attempt_id="attempt-3",
            created_at=now,
        )
        _store_sample(
            repository,
            receipt_id="receipt-4",
            object_id="object-4",
            attempt_id="attempt-3",
            created_at=now + timedelta(seconds=1),
        )
        outcomes = delete_submission(
            repository,
            "attempt-3",
            now + timedelta(seconds=2),
        )
        remaining = repository.list_active()

    assert len(outcomes) == 2
    assert all(outcome.deleted for outcome in outcomes)
    assert remaining == ()
