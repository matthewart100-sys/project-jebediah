from datetime import datetime, timedelta, timezone

from collector.document_admission import (
    Ed25519ReceiptVerifier,
    generate_synthetic_signing_key,
    sign_synthetic_receipt,
    synthetic_authorization_policy,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def test_receipt_verification_accepts_valid_signed_receipt():
    key = generate_synthetic_signing_key()
    signer_id = "synthetic-signer-1"
    policy = synthetic_authorization_policy((signer_id,))
    verifier = Ed25519ReceiptVerifier({signer_id: key.public_key()})
    now = _now()
    receipt = sign_synthetic_receipt(
        receipt_id="receipt-1",
        organization_domain_id="synthetic-org",
        source_record_id="source-1",
        source_authority_role="Synthetic Authority",
        principal_id="operator-1",
        purpose=policy.required_purpose,
        classification=policy.required_classification,
        allowed_operation=policy.required_operation,
        retention_profile_id="retention-1",
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(minutes=5),
        signer_key_id=signer_id,
        private_key=key,
    )

    verification = verifier.verify(
        receipt,
        policy,
        "verification-1",
        now,
    )

    assert verification.verified is True
    assert verification.reason_code is None


def test_receipt_verification_fails_closed_on_operation_mismatch():
    key = generate_synthetic_signing_key()
    signer_id = "synthetic-signer-1"
    policy = synthetic_authorization_policy((signer_id,))
    verifier = Ed25519ReceiptVerifier({signer_id: key.public_key()})
    now = _now()
    receipt = sign_synthetic_receipt(
        receipt_id="receipt-2",
        organization_domain_id="synthetic-org",
        source_record_id="source-2",
        source_authority_role="Synthetic Authority",
        principal_id="operator-1",
        purpose=policy.required_purpose,
        classification=policy.required_classification,
        allowed_operation="wrong_operation",
        retention_profile_id="retention-1",
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(minutes=5),
        signer_key_id=signer_id,
        private_key=key,
    )

    verification = verifier.verify(
        receipt,
        policy,
        "verification-2",
        now,
    )

    assert verification.verified is False
    assert verification.reason_code == "operation_not_allowed"
