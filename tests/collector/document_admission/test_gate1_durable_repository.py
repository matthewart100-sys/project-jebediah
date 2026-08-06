from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from collector.document_admission import (
    DocumentAdmissionConflict,
    ReconciliationOutcome,
    SqliteDurableRepository,
    derive_audit_key,
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


def test_reserve_receipt_rejects_replay(tmp_path: Path):
    now = _now()
    with _repository(tmp_path) as repository:
        repository.reserve_receipt("receipt-1", now)
        with pytest.raises(
            DocumentAdmissionConflict,
            match="receipt_already_used",
        ):
            repository.reserve_receipt("receipt-1", now + timedelta(seconds=1))


def test_store_and_retrieve_round_trip(tmp_path: Path):
    now = _now()
    payload = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF"
    with _repository(tmp_path) as repository:
        repository.reserve_receipt("receipt-2", now)
        record = repository.store(
            object_id="object-1",
            admission_attempt_id="attempt-1",
            receipt_id="receipt-2",
            plaintext=payload,
            policy=synthetic_custody_policy(),
            retention=synthetic_retention_policy(),
            created_at=now,
        )
        restored = repository.retrieve_plaintext(record.object_id)

    assert restored == payload


def test_reconcile_holds_tampered_objects(tmp_path: Path):
    now = _now()
    payload = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF"
    with _repository(tmp_path) as repository:
        repository.reserve_receipt("receipt-3", now)
        repository.store(
            object_id="object-2",
            admission_attempt_id="attempt-2",
            receipt_id="receipt-3",
            plaintext=payload,
            policy=synthetic_custody_policy(),
            retention=synthetic_retention_policy(),
            created_at=now,
        )
        object_path = tmp_path / "objects" / "object-2.enc"
        object_path.write_bytes(object_path.read_bytes() + b"tamper")

        findings = repository.reconcile(now + timedelta(seconds=2))

    assert findings
    assert findings[0].outcome is ReconciliationOutcome.HELD_INTEGRITY_FAILURE
