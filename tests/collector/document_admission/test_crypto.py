from datetime import datetime, timezone

from collector.document_admission.crypto import (
    audit_hmac_hex,
    create_master_key_envelope,
    decrypt_object,
    encrypt_object,
    hash_content_identity,
    unlock_master_key,
)


def test_master_key_envelope_round_trips() -> None:
    envelope, master_key = create_master_key_envelope("phase3b-passphrase")
    assert unlock_master_key("phase3b-passphrase", envelope) == master_key


def test_encrypt_object_round_trips_and_hashes_deterministically() -> None:
    _, master_key = create_master_key_envelope("phase3b-passphrase")
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    encrypted = encrypt_object(
        master_key,
        object_id="object-1",
        kind="source_pdf",
        payload=payload,
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert decrypt_object(master_key, encrypted) == payload
    assert hash_content_identity(payload).digest_hex == hash_content_identity(
        payload
    ).digest_hex


def test_audit_hmac_is_deterministic_for_same_payload() -> None:
    _, master_key = create_master_key_envelope("phase3b-passphrase")
    payload = b"synthetic-audit-entry"
    assert audit_hmac_hex(master_key, payload) == audit_hmac_hex(master_key, payload)
