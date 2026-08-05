from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from collector.document_admission import (
    CleanupFailed,
    CleanupOutcome,
    DocumentAdmissionConflict,
    DocumentAdmissionNotFound,
    LegalHoldEvidence,
    PolicyViolation,
    SyntheticPhase3BDocumentAdmissionRuntime,
)

from .synthetic_fixtures import (
    NOW,
    VALID_TXT,
    build_cleanup_context,
    build_envelope,
    build_policies,
    build_system,
    submit_valid,
)


def build_legal_hold(quarantine_id, *, expires_at=None):
    return LegalHoldEvidence(
        legal_hold_id="synthetic-legal-hold-1",
        quarantine_id=quarantine_id,
        authority_role="Chief Architect",
        retention_policy_id="synthetic-retention-policy",
        retention_policy_version="1",
        scope="synthetic_quarantine_payload",
        reason_code="synthetic_review_hold",
        evidence_references=("synthetic-hold-evidence",),
        effective_at=NOW + timedelta(seconds=5),
        expires_at=expires_at,
    )


def test_cleanup_deletes_process_local_payload():
    system = build_system()
    admission = submit_valid(system)
    evidence = system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        None,
        build_cleanup_context(),
    )
    assert evidence.outcome is CleanupOutcome.DELETED
    with pytest.raises(
        DocumentAdmissionNotFound,
        match="quarantine_not_found",
    ):
        system.quarantine.open_for_evaluation(
            admission.quarantine_receipt
        )


def test_successful_cleanup_is_idempotent_without_restoring_bytes():
    system = build_system()
    admission = submit_valid(system)
    context = build_cleanup_context()
    first = system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        None,
        context,
    )
    second = system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        None,
        context,
    )
    assert second == first
    with pytest.raises(DocumentAdmissionNotFound):
        system.quarantine.open_for_evaluation(
            admission.quarantine_receipt
        )


def test_phase3b_runtime_delete_submission(tmp_path: Path) -> None:
    base_time = datetime(2025, 1, 1, tzinfo=timezone.utc)
    runtime = SyntheticPhase3BDocumentAdmissionRuntime(
        tmp_path,
        "phase3b-passphrase",
        clock=lambda: base_time,
    )
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    detail = runtime.admit_signed_pdf(
        runtime.build_demo_receipt(
            receipt_id="cleanup-receipt",
            expected_payload=payload,
        ),
        "application/pdf",
        payload,
    )
    deleted = runtime.delete_submission(detail.record.submission_id)
    assert deleted.record.state.value == "deleted"


def test_cleanup_identity_conflict_is_rejected():
    system = build_system()
    admission = submit_valid(system)
    context = build_cleanup_context()
    system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        None,
        context,
    )
    with pytest.raises(
        DocumentAdmissionConflict,
        match="cleanup_identity_conflict",
    ):
        system.orchestrator.cleanup(
            admission.quarantine_receipt,
            build_policies().retention,
            None,
            replace(
                context,
                completed_at=context.completed_at
                + timedelta(seconds=1),
            ),
        )


def test_legal_hold_retains_process_local_payload():
    system = build_system()
    admission = submit_valid(system)
    evidence = system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        build_legal_hold(admission.quarantine_receipt.quarantine_id),
        build_cleanup_context(),
    )
    assert evidence.outcome is CleanupOutcome.LEGAL_HOLD
    assert (
        system.quarantine.open_for_evaluation(
            admission.quarantine_receipt
        )
        == VALID_TXT
    )


def test_expired_legal_hold_fails_closed():
    system = build_system()
    admission = submit_valid(system)
    with pytest.raises(
        PolicyViolation,
        match="invalid_legal_hold",
    ):
        system.orchestrator.cleanup(
            admission.quarantine_receipt,
            build_policies().retention,
            build_legal_hold(
                admission.quarantine_receipt.quarantine_id,
                expires_at=NOW + timedelta(seconds=7),
            ),
            build_cleanup_context(),
        )


def test_mismatched_legal_hold_fails_closed():
    system = build_system()
    admission = submit_valid(system)
    with pytest.raises(
        PolicyViolation,
        match="invalid_legal_hold",
    ):
        system.orchestrator.cleanup(
            admission.quarantine_receipt,
            build_policies().retention,
            build_legal_hold("different-quarantine"),
            build_cleanup_context(),
        )


def test_cleanup_failure_is_explicit_and_payload_remains(
    monkeypatch,
):
    system = build_system()
    admission = submit_valid(system)

    def fail_cleanup(*_args, **_kwargs):
        raise CleanupFailed(
            "synthetic_cleanup_failed",
            admission.quarantine_receipt.quarantine_id,
        )

    monkeypatch.setattr(system.quarantine, "delete", fail_cleanup)
    with pytest.raises(
        CleanupFailed,
        match="synthetic_cleanup_failed",
    ):
        system.orchestrator.cleanup(
            admission.quarantine_receipt,
            build_policies().retention,
            None,
            build_cleanup_context(),
        )
    assert (
        system.quarantine.open_for_evaluation(
            admission.quarantine_receipt
        )
        == VALID_TXT
    )


def test_deleted_quarantine_identity_cannot_reopen():
    system = build_system()
    admission = submit_valid(system)
    system.orchestrator.cleanup(
        admission.quarantine_receipt,
        build_policies().retention,
        None,
        build_cleanup_context(),
    )
    with pytest.raises(
        DocumentAdmissionConflict,
        match="quarantine_identity_conflict",
    ):
        system.quarantine.place(
            build_envelope(),
            admission.admission_attempt_id,
            admission.quarantine_receipt.quarantine_id,
            "new-integrity-evidence",
            VALID_TXT,
            admission.quarantine_receipt.content_identity,
            NOW + timedelta(seconds=10),
        )
