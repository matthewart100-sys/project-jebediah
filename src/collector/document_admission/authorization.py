from __future__ import annotations

import json
from base64 import b64decode, b64encode
from dataclasses import asdict
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .failures import DocumentAdmissionValidationError, PolicyViolation
from .interfaces import SourceAuthorizationVerifier
from .models import (
    SignedSourceAuthorizationReceipt,
    SourceAuthorizationReceipt,
)


def _receipt_dict(receipt: SourceAuthorizationReceipt) -> dict[str, object]:
    values = asdict(receipt)
    values["issued_at"] = receipt.issued_at.isoformat()
    values["expires_at"] = receipt.expires_at.isoformat()
    return values


def canonical_receipt_payload(receipt: SourceAuthorizationReceipt) -> bytes:
    return json.dumps(
        _receipt_dict(receipt),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sign_receipt(
    receipt: SourceAuthorizationReceipt,
    private_key: Ed25519PrivateKey,
) -> SignedSourceAuthorizationReceipt:
    signature = private_key.sign(canonical_receipt_payload(receipt))
    return SignedSourceAuthorizationReceipt(
        receipt=receipt,
        signature_b64=b64encode(signature).decode("ascii"),
    )


class SyntheticReceiptVerifier(SourceAuthorizationVerifier):
    def __init__(self, public_keys: dict[str, Ed25519PublicKey]) -> None:
        if not public_keys:
            raise DocumentAdmissionValidationError("missing_trust_registry")
        self._public_keys = dict(public_keys)

    def verify(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        checked_at: datetime,
    ) -> SignedSourceAuthorizationReceipt:
        if not isinstance(
            signed_receipt,
            SignedSourceAuthorizationReceipt,
        ):
            raise DocumentAdmissionValidationError("invalid_signed_receipt")
        receipt = signed_receipt.receipt
        key = self._public_keys.get(receipt.signer_key_id)
        if key is None:
            raise PolicyViolation("unknown_signer", receipt.receipt_id)
        key.verify(
            b64decode(signed_receipt.signature_b64.encode("ascii")),
            canonical_receipt_payload(receipt),
        )
        if checked_at >= receipt.expires_at:
            raise PolicyViolation("expired_receipt", receipt.receipt_id)
        return signed_receipt


def synthetic_signing_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
