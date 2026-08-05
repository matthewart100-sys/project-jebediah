from dataclasses import replace

import pytest

from collector.document_admission import (
    DocumentAdmissionConflict,
    DocumentAdmissionNotFound,
    InMemoryQuarantineRepository,
    QuarantineFailure,
    Sha256ByteIntegrityVerifier,
)

from .synthetic_fixtures import (
    NOW,
    VALID_TXT,
    build_cleanup_context,
    build_envelope,
    build_policies,
)


def place_synthetic_payload():
    verifier = Sha256ByteIntegrityVerifier()
    repository = InMemoryQuarantineRepository(verifier)
    envelope = build_envelope()
    identity = verifier.identify(VALID_TXT, build_policies().digest)
    receipt = repository.place(
        envelope,
        "attempt-1",
        "quarantine-1",
        "integrity-1",
        VALID_TXT,
        identity,
        NOW,
    )
    return verifier, repository, receipt


def test_quarantine_round_trip_is_process_local_and_read_copy():
    _, repository, receipt = place_synthetic_payload()

    first = repository.open_for_evaluation(receipt)
    second = repository.open_for_evaluation(receipt)

    assert first == VALID_TXT
    assert second == VALID_TXT
    assert isinstance(first, bytes)


def test_quarantine_place_is_idempotent_for_equal_evidence():
    verifier, repository, receipt = place_synthetic_payload()
    repeated = repository.place(
        build_envelope(),
        "attempt-1",
        "quarantine-1",
        "integrity-1",
        VALID_TXT,
        verifier.identify(VALID_TXT, build_policies().digest),
        NOW,
    )
    assert repeated == receipt


def test_quarantine_rejects_identity_conflict():
    verifier, repository, _ = place_synthetic_payload()
    changed = verifier.identify(
        VALID_TXT + b"-different",
        build_policies().digest,
    )
    with pytest.raises(
        DocumentAdmissionConflict,
        match="quarantine_identity_conflict",
    ):
        repository.place(
            build_envelope(),
            "attempt-1",
            "quarantine-1",
            "integrity-2",
            VALID_TXT + b"-different",
            changed,
            NOW,
        )


def test_quarantine_rejects_payload_identity_mismatch():
    verifier = Sha256ByteIntegrityVerifier()
    repository = InMemoryQuarantineRepository(verifier)
    wrong_identity = verifier.identify(
        VALID_TXT + b"-different",
        build_policies().digest,
    )
    with pytest.raises(
        QuarantineFailure,
        match="integrity_mismatch",
    ):
        repository.place(
            build_envelope(),
            "attempt-1",
            "quarantine-1",
            "integrity-1",
            VALID_TXT,
            wrong_identity,
            NOW,
        )


def test_quarantine_verifies_stored_payload():
    _, repository, receipt = place_synthetic_payload()
    verification = repository.verify(
        receipt,
        "verification-1",
        NOW,
    )
    assert verification.matches is True
    assert verification.quarantine_id == receipt.quarantine_id


def test_quarantine_rejects_changed_receipt():
    _, repository, receipt = place_synthetic_payload()
    with pytest.raises(
        DocumentAdmissionConflict,
        match="quarantine_receipt_conflict",
    ):
        repository.open_for_evaluation(
            replace(receipt, integrity_evidence_id="different")
        )


def test_quarantine_delete_removes_synthetic_bytes():
    _, repository, receipt = place_synthetic_payload()
    result = repository.delete(
        receipt,
        build_policies().retention,
        None,
        build_cleanup_context(),
    )
    assert result.outcome.value == "deleted"
    with pytest.raises(
        DocumentAdmissionNotFound,
        match="quarantine_not_found",
    ):
        repository.open_for_evaluation(receipt)
