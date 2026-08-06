"""Milestone 1 signed, single-use authorization receipt verification.

This module verifies an Ed25519-signed ``AuthorizationReceipt`` against a
trusted signer-key registry. It never issues a real organizational receipt;
every key and receipt exercised by this repository is a generated synthetic
test value. Real key custody, trust-registry rotation, and legal-hold
signature verification remain later-milestone and later-authorization
concerns.

Single-use enforcement (replay denial) is implemented by the durable
repository, which must reserve a receipt identifier before any byte is
admitted.
"""

from __future__ import annotations

import json
from datetime import datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .failures import AuthorizationFailure
from .interfaces import AuthorizationVerifier
from .models import AuthorizationReceipt, ReceiptVerification
from .policies import AuthorizationPolicy


def canonical_receipt_payload(receipt: AuthorizationReceipt) -> bytes:
    """Return the canonical, deterministically ordered signed payload.

    The signature itself is excluded from the canonical payload it covers.
    """

    fields = {
        "receipt_id": receipt.receipt_id,
        "organization_domain_id": receipt.organization_domain_id,
        "source_record_id": receipt.source_record_id,
        "source_authority_role": receipt.source_authority_role,
        "principal_id": receipt.principal_id,
        "purpose": receipt.purpose,
        "classification": receipt.classification,
        "allowed_operation": receipt.allowed_operation,
        "retention_profile_id": receipt.retention_profile_id,
        "issued_at": receipt.issued_at.isoformat(),
        "expires_at": receipt.expires_at.isoformat(),
        "signer_key_id": receipt.signer_key_id,
        "single_use": receipt.single_use,
    }
    return json.dumps(fields, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def generate_synthetic_signing_key() -> Ed25519PrivateKey:
    """Generate a synthetic Ed25519 keypair for deterministic tests only."""

    return Ed25519PrivateKey.generate()


def sign_synthetic_receipt(
    *,
    receipt_id: str,
    organization_domain_id: str,
    source_record_id: str,
    source_authority_role: str,
    principal_id: str,
    purpose: str,
    classification: str,
    allowed_operation: str,
    retention_profile_id: str,
    issued_at: datetime,
    expires_at: datetime,
    signer_key_id: str,
    private_key: Ed25519PrivateKey,
) -> AuthorizationReceipt:
    """Construct and sign one synthetic single-use authorization receipt."""

    unsigned = AuthorizationReceipt(
        receipt_id=receipt_id,
        organization_domain_id=organization_domain_id,
        source_record_id=source_record_id,
        source_authority_role=source_authority_role,
        principal_id=principal_id,
        purpose=purpose,
        classification=classification,
        allowed_operation=allowed_operation,
        retention_profile_id=retention_profile_id,
        issued_at=issued_at,
        expires_at=expires_at,
        signer_key_id=signer_key_id,
        single_use=True,
        signature_hex="0" * 128,
    )
    signature = private_key.sign(canonical_receipt_payload(unsigned))
    return AuthorizationReceipt(
        receipt_id=unsigned.receipt_id,
        organization_domain_id=unsigned.organization_domain_id,
        source_record_id=unsigned.source_record_id,
        source_authority_role=unsigned.source_authority_role,
        principal_id=unsigned.principal_id,
        purpose=unsigned.purpose,
        classification=unsigned.classification,
        allowed_operation=unsigned.allowed_operation,
        retention_profile_id=unsigned.retention_profile_id,
        issued_at=unsigned.issued_at,
        expires_at=unsigned.expires_at,
        signer_key_id=unsigned.signer_key_id,
        single_use=unsigned.single_use,
        signature_hex=signature.hex(),
    )


class Ed25519ReceiptVerifier(AuthorizationVerifier):
    """Verifies signature, trusted signer, and expiry of one receipt.

    ``trusted_public_keys`` maps a ``signer_key_id`` to its trusted
    ``Ed25519PublicKey``. An untrusted, unknown, or revoked signer key
    identifier fails closed.
    """

    def __init__(
        self,
        trusted_public_keys: dict[str, Ed25519PublicKey],
    ) -> None:
        if not isinstance(trusted_public_keys, dict) or not trusted_public_keys:
            raise AuthorizationFailure("invalid_trust_registry")
        self._trusted_public_keys = dict(trusted_public_keys)

    def verify(
        self,
        receipt: AuthorizationReceipt,
        policy: AuthorizationPolicy,
        verification_id: str,
        checked_at: datetime,
    ) -> ReceiptVerification:
        if not isinstance(receipt, AuthorizationReceipt):
            raise AuthorizationFailure("invalid_receipt")
        if not isinstance(policy, AuthorizationPolicy):
            raise AuthorizationFailure("invalid_authorization_policy")
        if not verification_id or not isinstance(verification_id, str):
            raise AuthorizationFailure("invalid_verification_id")
        if checked_at.tzinfo is None:
            raise AuthorizationFailure("invalid_checked_at")

        reason_code: str | None = None
        public_key = self._trusted_public_keys.get(receipt.signer_key_id)
        if public_key is None:
            reason_code = "untrusted_signer_key"
        elif receipt.signer_key_id not in policy.trusted_signer_key_ids:
            reason_code = "signer_not_allowed_by_policy"
        elif receipt.purpose != policy.required_purpose:
            reason_code = "purpose_not_allowed"
        elif receipt.classification != policy.required_classification:
            reason_code = "classification_not_allowed"
        elif receipt.allowed_operation != policy.required_operation:
            reason_code = "operation_not_allowed"
        elif policy.requires_single_use and not receipt.single_use:
            reason_code = "receipt_not_single_use"
        elif (
            int((receipt.expires_at - receipt.issued_at).total_seconds())
            > policy.max_receipt_lifetime_seconds
        ):
            reason_code = "receipt_lifetime_exceeds_policy"
        elif checked_at >= receipt.expires_at:
            reason_code = "expired_receipt"
        elif checked_at < receipt.issued_at:
            reason_code = "receipt_not_yet_effective"
        else:
            try:
                public_key.verify(
                    bytes.fromhex(receipt.signature_hex),
                    canonical_receipt_payload(receipt),
                )
            except (InvalidSignature, ValueError):
                reason_code = "invalid_signature"

        verified = reason_code is None
        return ReceiptVerification(
            verification_id=verification_id,
            receipt_id=receipt.receipt_id,
            signer_key_id=receipt.signer_key_id,
            verified=verified,
            reason_code=reason_code,
            checked_at=checked_at,
        )
