from datetime import datetime, timedelta, timezone

import pytest

from collector.document_admission.authorization import (
    SyntheticReceiptVerifier,
    sign_receipt,
    synthetic_signing_key,
)
from collector.document_admission.failures import PolicyViolation
from collector.document_admission.models import SourceAuthorizationReceipt


def _receipt(*, receipt_id: str, expires_at: datetime) -> SourceAuthorizationReceipt:
    return SourceAuthorizationReceipt(
        receipt_id=receipt_id,
        organization_id="synthetic-org",
        source_record_id="synthetic-source",
        authority_role="synthetic-authority",
        principal_id="synthetic-principal",
        purpose="phase3b_test",
        classification="internal-governance-limited-personal-data",
        allowed_operation="phase3b.synthetic.intake",
        retention_profile_id="phase3b",
        environment="synthetic-local-only",
        issued_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        expires_at=expires_at,
        signer_key_id="synthetic-phase3b-signer",
        expected_sha256=None,
        single_use=True,
    )


def test_receipt_verifier_accepts_known_signature() -> None:
    signing_key = synthetic_signing_key()
    verifier = SyntheticReceiptVerifier(
        {"synthetic-phase3b-signer": signing_key.public_key()}
    )
    signed = sign_receipt(
        _receipt(
            receipt_id="receipt-1",
            expires_at=datetime(2025, 1, 1, tzinfo=timezone.utc)
            + timedelta(hours=1),
        ),
        signing_key,
    )
    assert verifier.verify(
        signed,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    ) == signed


def test_receipt_verifier_rejects_unknown_signer() -> None:
    signing_key = synthetic_signing_key()
    signed = sign_receipt(
        _receipt(
            receipt_id="receipt-2",
            expires_at=datetime(2025, 1, 1, tzinfo=timezone.utc)
            + timedelta(hours=1),
        ),
        signing_key,
    )
    verifier = SyntheticReceiptVerifier({"different": signing_key.public_key()})
    with pytest.raises(PolicyViolation, match="unknown_signer"):
        verifier.verify(signed, datetime(2025, 1, 1, tzinfo=timezone.utc))


def test_receipt_verifier_rejects_expired_receipt() -> None:
    signing_key = synthetic_signing_key()
    verifier = SyntheticReceiptVerifier(
        {"synthetic-phase3b-signer": signing_key.public_key()}
    )
    signed = sign_receipt(
        _receipt(
            receipt_id="receipt-3",
            expires_at=datetime(2025, 1, 1, tzinfo=timezone.utc)
            + timedelta(seconds=1),
        ),
        signing_key,
    )
    with pytest.raises(PolicyViolation, match="expired_receipt"):
        verifier.verify(
            signed,
            datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=1),
        )
