from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from collector.document_admission import (
    DocumentCustodyRuntime,
    Ed25519ReceiptVerifier,
    SqliteDurableRepository,
    derive_audit_key,
    generate_master_key,
    generate_salt,
    generate_synthetic_signing_key,
    sign_synthetic_receipt,
    synthetic_authorization_policy,
    synthetic_custody_policy,
    synthetic_retention_policy,
)
from collector.organizational_intelligence import (
    AnswerState,
    Gate2RetrievalDenied,
    Gate2ReviewRejected,
    Phase3CBridge,
)


def _build_runtime(tmp_path: Path):
    master_key = generate_master_key()
    audit_key = derive_audit_key(master_key, generate_salt())
    repository = SqliteDurableRepository(
        runtime_directory=tmp_path,
        master_key=master_key,
        audit_key=audit_key,
        custody_policy=synthetic_custody_policy(),
    )
    signer_key = generate_synthetic_signing_key()
    signer_id = "synthetic-signer-bridge"
    verifier = Ed25519ReceiptVerifier({signer_id: signer_key.public_key()})
    runtime = DocumentCustodyRuntime(
        repository=repository,
        receipt_verifier=verifier,
        authorization_policy=synthetic_authorization_policy((signer_id,)),
        retention_policy=synthetic_retention_policy(),
        custody_policy=synthetic_custody_policy(),
        max_admission_bytes=4096,
    )
    return runtime, repository, signer_id, signer_key


def _build_receipt(*, signer_id: str, signer_key, now: datetime, receipt_id: str):
    policy = synthetic_authorization_policy((signer_id,))
    return sign_synthetic_receipt(
        receipt_id=receipt_id,
        organization_domain_id="synthetic-org-bridge",
        source_record_id="source-record-bridge",
        source_authority_role="Synthetic Source Authority",
        principal_id="operator-bridge",
        purpose=policy.required_purpose,
        classification=policy.required_classification,
        allowed_operation=policy.required_operation,
        retention_profile_id="retention-profile-bridge",
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(minutes=10),
        signer_key_id=signer_id,
        private_key=signer_key,
    )


def _synthetic_pdf_bytes() -> bytes:
    return (
        b"%PDF-1.7\n"
        b"SYNTHETIC ORGANIZATIONAL NOTE: Treasury committee observed conflicting "
        b"cash figures across two reports and requires reconciliation.\n"
        b"%%EOF"
    )


def test_knowledge_promotion_requires_approved_review(tmp_path: Path):
    now = datetime(2026, 8, 5, tzinfo=timezone.utc)
    runtime, repository, signer_id, signer_key = _build_runtime(tmp_path)
    bridge = Phase3CBridge(
        runtime=runtime,
        repository=repository,
        allowed_consumer_ids=("executive-consumer",),
        allowed_uses=("executive_question_answering",),
    )
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-review-required",
    )
    candidate = bridge.admit_for_review(
        correlation_id="corr-review-required",
        receipt=receipt,
        payload=_synthetic_pdf_bytes(),
        admission_attempt_id="attempt-review-required",
        object_id="object-review-required",
        admitted_at=now,
    )

    with pytest.raises(Gate2ReviewRejected):
        bridge.promote_candidate(
            candidate_id=candidate.candidate_id,
            reviewer_id="reviewer-1",
            rationale="Not approved in this test",
            approved=False,
            title="Synthetic cash reconciliation memo",
            promoted_at=now + timedelta(minutes=1),
        )

    repository.close()


def test_retrieval_boundaries_deny_unauthorized_consumer_and_use(tmp_path: Path):
    now = datetime(2026, 8, 5, tzinfo=timezone.utc)
    runtime, repository, signer_id, signer_key = _build_runtime(tmp_path)
    bridge = Phase3CBridge(
        runtime=runtime,
        repository=repository,
        allowed_consumer_ids=("executive-consumer",),
        allowed_uses=("executive_question_answering",),
    )
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-retrieval-boundary",
    )
    candidate = bridge.admit_for_review(
        correlation_id="corr-retrieval-boundary",
        receipt=receipt,
        payload=_synthetic_pdf_bytes(),
        admission_attempt_id="attempt-retrieval-boundary",
        object_id="object-retrieval-boundary",
        admitted_at=now,
    )
    bridge.promote_candidate(
        candidate_id=candidate.candidate_id,
        reviewer_id="reviewer-1",
        rationale="Approved for synthetic bridge testing",
        approved=True,
        title="Synthetic cash reconciliation memo",
        promoted_at=now + timedelta(minutes=1),
    )

    with pytest.raises(Gate2RetrievalDenied):
        bridge.ask(
            correlation_id="corr-retrieval-boundary",
            question_id="q-denied-consumer",
            question="What should leadership do about cash reconciliation?",
            consumer_id="unauthorized-consumer",
            intended_use="executive_question_answering",
            asked_at=now + timedelta(minutes=2),
        )
    with pytest.raises(Gate2RetrievalDenied):
        bridge.ask(
            correlation_id="corr-retrieval-boundary",
            question_id="q-denied-use",
            question="What should leadership do about cash reconciliation?",
            consumer_id="executive-consumer",
            intended_use="unsupported_use",
            asked_at=now + timedelta(minutes=3),
        )

    repository.close()


def test_citations_and_provenance_are_returned_for_grounded_answers(tmp_path: Path):
    now = datetime(2026, 8, 5, tzinfo=timezone.utc)
    runtime, repository, signer_id, signer_key = _build_runtime(tmp_path)
    bridge = Phase3CBridge(
        runtime=runtime,
        repository=repository,
        allowed_consumer_ids=("executive-consumer",),
        allowed_uses=("executive_question_answering",),
    )
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-grounded-answer",
    )
    candidate = bridge.admit_for_review(
        correlation_id="corr-grounded-answer",
        receipt=receipt,
        payload=_synthetic_pdf_bytes(),
        admission_attempt_id="attempt-grounded-answer",
        object_id="object-grounded-answer",
        admitted_at=now,
    )
    promoted = bridge.promote_candidate(
        candidate_id=candidate.candidate_id,
        reviewer_id="reviewer-1",
        rationale="Approved for synthetic evidence-backed answering",
        approved=True,
        title="Synthetic cash reconciliation memo",
        promoted_at=now + timedelta(minutes=1),
    )

    answer = bridge.ask(
        correlation_id="corr-grounded-answer",
        question_id="q-grounded-1",
        question="What does the evidence say about cash reconciliation?",
        consumer_id="executive-consumer",
        intended_use="executive_question_answering",
        asked_at=now + timedelta(minutes=2),
    )

    assert answer.state is AnswerState.GROUNDED
    assert answer.statement is not None
    assert answer.citations
    assert answer.provenance
    assert answer.citations[0].knowledge_id == promoted.knowledge_id
    assert (
        answer.provenance[0].admission_attempt_id
        == candidate.admission_attempt_id
    )
    assert answer.provenance[0].receipt_id == candidate.receipt_id

    repository.close()


def test_audit_integrity_and_failure_isolation(tmp_path: Path):
    now = datetime(2026, 8, 5, tzinfo=timezone.utc)
    runtime, repository, signer_id, signer_key = _build_runtime(tmp_path)
    bridge = Phase3CBridge(
        runtime=runtime,
        repository=repository,
        allowed_consumer_ids=("executive-consumer",),
        allowed_uses=("executive_question_answering",),
    )
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-audit-integrity",
    )
    candidate = bridge.admit_for_review(
        correlation_id="corr-audit-integrity",
        receipt=receipt,
        payload=_synthetic_pdf_bytes(),
        admission_attempt_id="attempt-audit-integrity",
        object_id="object-audit-integrity",
        admitted_at=now,
    )
    bridge.promote_candidate(
        candidate_id=candidate.candidate_id,
        reviewer_id="reviewer-1",
        rationale="Approved for audit test",
        approved=True,
        title="Synthetic cash reconciliation memo",
        promoted_at=now + timedelta(minutes=1),
    )

    with pytest.raises(Gate2RetrievalDenied):
        bridge.ask(
            correlation_id="corr-audit-integrity",
            question_id="q-audit-denied",
            question="What is the board decision?",
            consumer_id="forbidden-consumer",
            intended_use="executive_question_answering",
            asked_at=now + timedelta(minutes=2),
        )

    assert bridge.verify_audit_integrity(correlation_id="corr-audit-integrity")
    history = bridge.audit_history(correlation_id="corr-audit-integrity")
    assert any(event.event_kind == "retrieval.denied" for event in history)

    repository.close()


def test_end_to_end_demonstration_workflow(tmp_path: Path):
    now = datetime(2026, 8, 5, tzinfo=timezone.utc)
    runtime, repository, signer_id, signer_key = _build_runtime(tmp_path)
    bridge = Phase3CBridge(
        runtime=runtime,
        repository=repository,
        allowed_consumer_ids=("executive-consumer",),
        allowed_uses=("executive_question_answering",),
    )
    receipt = _build_receipt(
        signer_id=signer_id,
        signer_key=signer_key,
        now=now,
        receipt_id="receipt-end-to-end",
    )

    candidate = bridge.admit_for_review(
        correlation_id="corr-end-to-end",
        receipt=receipt,
        payload=_synthetic_pdf_bytes(),
        admission_attempt_id="attempt-end-to-end",
        object_id="object-end-to-end",
        admitted_at=now,
    )
    bridge.promote_candidate(
        candidate_id=candidate.candidate_id,
        reviewer_id="reviewer-1",
        rationale="Approved for demonstration",
        approved=True,
        title="Synthetic cash reconciliation memo",
        promoted_at=now + timedelta(minutes=1),
    )
    answer = bridge.ask(
        correlation_id="corr-end-to-end",
        question_id="q-end-to-end",
        question="What should executives know about cash reconciliation?",
        consumer_id="executive-consumer",
        intended_use="executive_question_answering",
        asked_at=now + timedelta(minutes=2),
    )

    assert answer.state is AnswerState.GROUNDED
    assert answer.citations
    assert answer.provenance
    assert bridge.verify_audit_integrity(correlation_id="corr-end-to-end")
    assert len(bridge.audit_history(correlation_id="corr-end-to-end")) == 3

    repository.close()
