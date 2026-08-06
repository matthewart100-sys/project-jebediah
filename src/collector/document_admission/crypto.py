from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass

from .failures import CustodyFailure
from .models import ContentIdentity
from .policies import CustodyPolicy

_NONCE_BYTES = 16
_MASTER_KEY_BYTES = 32
_KDF_ITERATIONS = 200_000
_WRAPPED_KEY_VERSION = 1


def _require_bytes(value: bytes, name: str) -> None:
    if not isinstance(value, bytes) or not value:
        raise CustodyFailure(f"invalid_{name}")


def _require_hex(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or not value
        or value != value.lower()
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise CustodyFailure(f"invalid_{name}")


def _xor_bytes(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right))


def _derive_stream(
    *,
    key: bytes,
    nonce: bytes,
    object_kind: str,
    object_id: str,
    policy: CustodyPolicy,
    length: int,
) -> bytes:
    material = bytearray()
    counter = 0
    while len(material) < length:
        counter_bytes = counter.to_bytes(8, "big")
        block = hashlib.sha256(
            key
            + nonce
            + counter_bytes
            + object_kind.encode("utf-8")
            + object_id.encode("utf-8")
            + policy.policy_id.encode("utf-8")
            + policy.policy_version.encode("utf-8")
        ).digest()
        material.extend(block)
        counter += 1
    return bytes(material[:length])


def _authenticated_tag(
    key: bytes,
    header_version: int,
    object_kind: str,
    object_id: str,
    nonce: bytes,
    ciphertext: bytes,
) -> str:
    payload = (
        str(header_version).encode("utf-8")
        + b"|"
        + object_kind.encode("utf-8")
        + b"|"
        + object_id.encode("utf-8")
        + b"|"
        + nonce
        + b"|"
        + ciphertext
    )
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


@dataclass(frozen=True)
class EncryptedObject:
    header_version: int
    object_kind: str
    object_id: str
    nonce_hex: str
    ciphertext_hex: str
    auth_tag_hex: str

    def __post_init__(self) -> None:
        if type(self.header_version) is not int or self.header_version <= 0:
            raise CustodyFailure("invalid_header_version")
        if not self.object_kind or not isinstance(self.object_kind, str):
            raise CustodyFailure("invalid_object_kind")
        if not self.object_id or not isinstance(self.object_id, str):
            raise CustodyFailure("invalid_object_id")
        _require_hex(self.nonce_hex, "nonce_hex")
        _require_hex(self.ciphertext_hex, "ciphertext_hex")
        _require_hex(self.auth_tag_hex, "auth_tag_hex")
        if len(self.auth_tag_hex) != 64:
            raise CustodyFailure("invalid_auth_tag_hex")

    def to_bytes(self) -> bytes:
        payload = {
            "header_version": self.header_version,
            "object_kind": self.object_kind,
            "object_id": self.object_id,
            "nonce_hex": self.nonce_hex,
            "ciphertext_hex": self.ciphertext_hex,
            "auth_tag_hex": self.auth_tag_hex,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )

    @classmethod
    def from_bytes(cls, payload: bytes) -> "EncryptedObject":
        _require_bytes(payload, "encrypted_payload")
        try:
            data = json.loads(payload.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise CustodyFailure("invalid_encrypted_object") from error
        if not isinstance(data, dict):
            raise CustodyFailure("invalid_encrypted_object")
        try:
            return cls(
                header_version=data["header_version"],
                object_kind=data["object_kind"],
                object_id=data["object_id"],
                nonce_hex=data["nonce_hex"],
                ciphertext_hex=data["ciphertext_hex"],
                auth_tag_hex=data["auth_tag_hex"],
            )
        except KeyError as error:
            raise CustodyFailure("invalid_encrypted_object") from error


@dataclass(frozen=True)
class WrappedMasterKey:
    version: int
    salt_hex: str
    nonce_hex: str
    wrapped_key_hex: str
    auth_tag_hex: str
    iterations: int

    def __post_init__(self) -> None:
        if self.version != _WRAPPED_KEY_VERSION:
            raise CustodyFailure("invalid_wrap_version")
        _require_hex(self.salt_hex, "salt_hex")
        _require_hex(self.nonce_hex, "nonce_hex")
        _require_hex(self.wrapped_key_hex, "wrapped_key_hex")
        _require_hex(self.auth_tag_hex, "auth_tag_hex")
        if type(self.iterations) is not int or self.iterations < 100_000:
            raise CustodyFailure("invalid_iterations")
        if len(self.auth_tag_hex) != 64:
            raise CustodyFailure("invalid_auth_tag_hex")


def generate_master_key() -> bytes:
    return secrets.token_bytes(_MASTER_KEY_BYTES)


def generate_salt() -> bytes:
    return secrets.token_bytes(_NONCE_BYTES)


def derive_audit_key(master_key: bytes, salt: bytes) -> bytes:
    _require_bytes(master_key, "master_key")
    _require_bytes(salt, "salt")
    return hashlib.pbkdf2_hmac(
        "sha256",
        master_key,
        salt + b"|audit",
        _KDF_ITERATIONS,
        dklen=32,
    )


def wrap_master_key(
    master_key: bytes,
    passphrase: str,
    salt: bytes | None = None,
) -> WrappedMasterKey:
    _require_bytes(master_key, "master_key")
    if len(master_key) != _MASTER_KEY_BYTES:
        raise CustodyFailure("invalid_master_key_length")
    if not isinstance(passphrase, str) or not passphrase:
        raise CustodyFailure("invalid_passphrase")
    chosen_salt = salt if salt is not None else generate_salt()
    _require_bytes(chosen_salt, "salt")
    nonce = secrets.token_bytes(_NONCE_BYTES)
    wrapping_key = hashlib.pbkdf2_hmac(
        "sha256",
        passphrase.encode("utf-8"),
        chosen_salt,
        _KDF_ITERATIONS,
        dklen=_MASTER_KEY_BYTES,
    )
    wrapped = _xor_bytes(master_key, wrapping_key)
    auth_tag = hmac.new(
        wrapping_key,
        nonce + wrapped,
        hashlib.sha256,
    ).hexdigest()
    return WrappedMasterKey(
        version=_WRAPPED_KEY_VERSION,
        salt_hex=chosen_salt.hex(),
        nonce_hex=nonce.hex(),
        wrapped_key_hex=wrapped.hex(),
        auth_tag_hex=auth_tag,
        iterations=_KDF_ITERATIONS,
    )


def unwrap_master_key(wrapped: WrappedMasterKey, passphrase: str) -> bytes:
    if not isinstance(wrapped, WrappedMasterKey):
        raise CustodyFailure("invalid_wrapped_master_key")
    if not isinstance(passphrase, str) or not passphrase:
        raise CustodyFailure("invalid_passphrase")
    salt = bytes.fromhex(wrapped.salt_hex)
    nonce = bytes.fromhex(wrapped.nonce_hex)
    wrapped_key = bytes.fromhex(wrapped.wrapped_key_hex)
    wrapping_key = hashlib.pbkdf2_hmac(
        "sha256",
        passphrase.encode("utf-8"),
        salt,
        wrapped.iterations,
        dklen=len(wrapped_key),
    )
    expected_tag = hmac.new(
        wrapping_key,
        nonce + wrapped_key,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected_tag, wrapped.auth_tag_hex):
        raise CustodyFailure("invalid_wrapped_key_authentication")
    return _xor_bytes(wrapped_key, wrapping_key)


def content_identity_for(
    payload: bytes,
    digest_policy_id: str,
    digest_policy_version: str,
) -> ContentIdentity:
    _require_bytes(payload, "payload")
    digest = hashlib.sha256(payload).hexdigest()
    return ContentIdentity(
        digest_policy_id=digest_policy_id,
        digest_policy_version=digest_policy_version,
        algorithm="sha256",
        digest_hex=digest,
        byte_count=len(payload),
    )


def audit_event_hmac_hex(audit_key: bytes, payload: bytes) -> str:
    _require_bytes(audit_key, "audit_key")
    _require_bytes(payload, "payload")
    return hmac.new(audit_key, payload, hashlib.sha256).hexdigest()


def encrypt_object(
    payload: bytes,
    master_key: bytes,
    object_kind: str,
    object_id: str,
    policy: CustodyPolicy,
) -> EncryptedObject:
    _require_bytes(payload, "payload")
    _require_bytes(master_key, "master_key")
    if not isinstance(policy, CustodyPolicy):
        raise CustodyFailure("invalid_custody_policy")
    if object_kind != policy.required_object_kind:
        raise CustodyFailure("invalid_object_kind")
    if not isinstance(object_id, str) or not object_id:
        raise CustodyFailure("invalid_object_id")
    nonce = secrets.token_bytes(_NONCE_BYTES)
    stream = _derive_stream(
        key=master_key,
        nonce=nonce,
        object_kind=object_kind,
        object_id=object_id,
        policy=policy,
        length=len(payload),
    )
    ciphertext = _xor_bytes(payload, stream)
    auth_tag = _authenticated_tag(
        master_key,
        policy.header_version,
        object_kind,
        object_id,
        nonce,
        ciphertext,
    )
    return EncryptedObject(
        header_version=policy.header_version,
        object_kind=object_kind,
        object_id=object_id,
        nonce_hex=nonce.hex(),
        ciphertext_hex=ciphertext.hex(),
        auth_tag_hex=auth_tag,
    )


def decrypt_object(
    encrypted: EncryptedObject,
    master_key: bytes,
    object_kind: str,
    object_id: str,
) -> bytes:
    if not isinstance(encrypted, EncryptedObject):
        raise CustodyFailure("invalid_encrypted_object")
    _require_bytes(master_key, "master_key")
    if encrypted.object_kind != object_kind or encrypted.object_id != object_id:
        raise CustodyFailure("invalid_object_binding")
    nonce = bytes.fromhex(encrypted.nonce_hex)
    ciphertext = bytes.fromhex(encrypted.ciphertext_hex)
    expected_auth_tag = _authenticated_tag(
        master_key,
        encrypted.header_version,
        object_kind,
        object_id,
        nonce,
        ciphertext,
    )
    if not hmac.compare_digest(expected_auth_tag, encrypted.auth_tag_hex):
        raise CustodyFailure("invalid_object_authentication")
    stream = _derive_stream(
        key=master_key,
        nonce=nonce,
        object_kind=object_kind,
        object_id=object_id,
        policy=CustodyPolicy(
            policy_id="synthetic-custody-policy",
            policy_version="1",
            encryption_algorithm="synthetic-xor-stream-v1",
            header_version=encrypted.header_version,
            key_derivation_id="synthetic-hkdf-sha256-v1",
            required_object_kind=object_kind,
            requires_authenticated_encryption=True,
            allows_plaintext_persistence=False,
            max_ciphertext_expansion_bytes=128,
        ),
        length=len(ciphertext),
    )
    return _xor_bytes(ciphertext, stream)
