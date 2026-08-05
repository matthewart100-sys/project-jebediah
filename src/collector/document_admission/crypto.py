from __future__ import annotations

import hashlib
import hmac
import json
import os
from base64 import b64decode, b64encode
from dataclasses import asdict, dataclass
from datetime import datetime

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from .models import ContentIdentity


MASTER_KEY_AAD = b"phase3b-master-key"
OBJECT_WRAP_AAD_PREFIX = b"phase3b-object-wrap:"
OBJECT_DATA_AAD_PREFIX = b"phase3b-object-data:"


@dataclass(frozen=True)
class MasterKeyEnvelope:
    salt_b64: str
    nonce_b64: str
    ciphertext_b64: str
    iterations: int
    lanes: int
    memory_cost: int


@dataclass(frozen=True)
class EncryptedObject:
    object_id: str
    kind: str
    created_at: str
    payload_digest_hex: str
    payload_size: int
    wrap_nonce_b64: str
    wrapped_dek_b64: str
    data_nonce_b64: str
    ciphertext_b64: str


def hash_content_identity(payload: bytes) -> ContentIdentity:
    return ContentIdentity(
        digest_policy_id="phase3b-sha256",
        digest_policy_version="1",
        algorithm="sha256",
        digest_hex=hashlib.sha256(payload).hexdigest(),
        byte_count=len(payload),
    )


def _derive_kek(
    passphrase: str,
    salt: bytes,
    *,
    iterations: int,
    lanes: int,
    memory_cost: int,
) -> bytes:
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=iterations,
        lanes=lanes,
        memory_cost=memory_cost,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def create_master_key_envelope(
    passphrase: str,
) -> tuple[MasterKeyEnvelope, bytes]:
    master_key = os.urandom(32)
    salt = os.urandom(16)
    nonce = os.urandom(12)
    iterations = 2
    lanes = 4
    memory_cost = 64 * 1024
    kek = _derive_kek(
        passphrase,
        salt,
        iterations=iterations,
        lanes=lanes,
        memory_cost=memory_cost,
    )
    ciphertext = AESGCM(kek).encrypt(nonce, master_key, MASTER_KEY_AAD)
    return (
        MasterKeyEnvelope(
            salt_b64=b64encode(salt).decode("ascii"),
            nonce_b64=b64encode(nonce).decode("ascii"),
            ciphertext_b64=b64encode(ciphertext).decode("ascii"),
            iterations=iterations,
            lanes=lanes,
            memory_cost=memory_cost,
        ),
        master_key,
    )


def unlock_master_key(passphrase: str, envelope: MasterKeyEnvelope) -> bytes:
    kek = _derive_kek(
        passphrase,
        b64decode(envelope.salt_b64.encode("ascii")),
        iterations=envelope.iterations,
        lanes=envelope.lanes,
        memory_cost=envelope.memory_cost,
    )
    return AESGCM(kek).decrypt(
        b64decode(envelope.nonce_b64.encode("ascii")),
        b64decode(envelope.ciphertext_b64.encode("ascii")),
        MASTER_KEY_AAD,
    )


def envelope_to_dict(envelope: MasterKeyEnvelope) -> dict[str, object]:
    return asdict(envelope)


def envelope_from_dict(values: dict[str, object]) -> MasterKeyEnvelope:
    return MasterKeyEnvelope(
        salt_b64=str(values["salt_b64"]),
        nonce_b64=str(values["nonce_b64"]),
        ciphertext_b64=str(values["ciphertext_b64"]),
        iterations=int(values["iterations"]),
        lanes=int(values["lanes"]),
        memory_cost=int(values["memory_cost"]),
    )


def encrypt_object(
    master_key: bytes,
    *,
    object_id: str,
    kind: str,
    payload: bytes,
    created_at: datetime,
) -> EncryptedObject:
    dek = os.urandom(32)
    wrap_nonce = os.urandom(12)
    data_nonce = os.urandom(12)
    wrapped_dek = AESGCM(master_key).encrypt(
        wrap_nonce,
        dek,
        OBJECT_WRAP_AAD_PREFIX + object_id.encode("utf-8"),
    )
    ciphertext = AESGCM(dek).encrypt(
        data_nonce,
        payload,
        OBJECT_DATA_AAD_PREFIX + f"{object_id}:{kind}".encode("utf-8"),
    )
    return EncryptedObject(
        object_id=object_id,
        kind=kind,
        created_at=created_at.isoformat(),
        payload_digest_hex=hashlib.sha256(payload).hexdigest(),
        payload_size=len(payload),
        wrap_nonce_b64=b64encode(wrap_nonce).decode("ascii"),
        wrapped_dek_b64=b64encode(wrapped_dek).decode("ascii"),
        data_nonce_b64=b64encode(data_nonce).decode("ascii"),
        ciphertext_b64=b64encode(ciphertext).decode("ascii"),
    )


def decrypt_object(master_key: bytes, encrypted: EncryptedObject) -> bytes:
    dek = AESGCM(master_key).decrypt(
        b64decode(encrypted.wrap_nonce_b64.encode("ascii")),
        b64decode(encrypted.wrapped_dek_b64.encode("ascii")),
        OBJECT_WRAP_AAD_PREFIX + encrypted.object_id.encode("utf-8"),
    )
    payload = AESGCM(dek).decrypt(
        b64decode(encrypted.data_nonce_b64.encode("ascii")),
        b64decode(encrypted.ciphertext_b64.encode("ascii")),
        OBJECT_DATA_AAD_PREFIX
        + f"{encrypted.object_id}:{encrypted.kind}".encode("utf-8"),
    )
    if hashlib.sha256(payload).hexdigest() != encrypted.payload_digest_hex:
        raise ValueError("payload digest mismatch")
    return payload


def encrypted_object_to_json(encrypted: EncryptedObject) -> str:
    return json.dumps(asdict(encrypted), sort_keys=True, separators=(",", ":"))


def encrypted_object_from_json(payload: str) -> EncryptedObject:
    values = json.loads(payload)
    return EncryptedObject(**values)


def derive_audit_hmac_key(master_key: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"phase3b-audit-hmac",
    ).derive(master_key)


def audit_hmac_hex(master_key: bytes, payload: bytes) -> str:
    return hmac.new(
        derive_audit_hmac_key(master_key),
        payload,
        hashlib.sha256,
    ).hexdigest()
