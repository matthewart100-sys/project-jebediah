from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone

import pytest

from collector.document_admission import (
    AdmissionOperationContext,
    ConsumerEligibilityDecision,
    ConsumerEligibilityOutcome,
    ContentIdentity,
    DocumentAdmissionValidationError,
    FormatDetectionResult,
    FormatDetectionState,
    Phase3BPageCapture,
    Phase3BSubmissionRecord,
    Phase3BState,
    ReviewDecision,
    SignedSourceAuthorizationReceipt,
    SourceAuthorizationReceipt,
    RetryKind,
    SubmissionEnvelope,
)

from .synthetic_fixtures import (
    NOW,
    build_admission_context,
    build_envelope,
    build_retry,
)


def test_submission_envelope_is_immutable_and_deterministic():
    envelope = build_envelope()

    assert envelope == build_envelope()
    assert hash(envelope) == hash(build_envelope())
    with pytest.raises(FrozenInstanceError):
        envelope.submission_id = "changed"


@pytest.mark.parametrize(
    "field_name",
    [
        "submission_id",
        "consumer_policy_id",
        "retention_policy_id",
        "deletion_policy_id",
        "resource_policy_id",
        "correlation_id",
    ],
)
def test_submission_envelope_rejects_missing_identifiers(field_name):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match=f"invalid_{field_name}",
    ):
        build_envelope(**{field_name: " "})


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("source_authority_id", "real-source"),
        ("safe_source_reference", "local-path"),
        ("producer_id", "real-producer"),
        ("submitter_id", "real-user"),
        ("information_domain", "organizational"),
        ("intended_use", "production"),
        ("consumer_id", "runtime"),
        ("classification", "private"),
    ],
)
def test_submission_scope_is_synthetic_only(field_name, value):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match=f"invalid_{field_name}",
    ):
        build_envelope(**{field_name: value})


def test_phase3b_signed_receipt_requires_base64_signature() -> None:
    receipt = SourceAuthorizationReceipt(
        receipt_id="synthetic-receipt-1",
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
        expires_at=datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(hours=1),
        signer_key_id="synthetic-signer",
        expected_sha256=None,
        single_use=True,
    )
    with pytest.raises(DocumentAdmissionValidationError, match="invalid_signature_b64"):
        SignedSourceAuthorizationReceipt(receipt=receipt, signature_b64="not-base64")


def test_phase3b_submission_record_tracks_state_and_review_decision() -> None:
    record = Phase3BSubmissionRecord(
        submission_id="submission-1",
        receipt_id="receipt-1",
        state=Phase3BState.READY_FOR_REVIEW,
        content_identity=ContentIdentity(
            digest_policy_id="phase3b-sha256",
            digest_policy_version="1",
            algorithm="sha256",
            digest_hex="a" * 64,
            byte_count=32,
        ),
        media_type="application/pdf",
        byte_count=32,
        duplicate_of=None,
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        expires_at=datetime(2025, 1, 2, tzinfo=timezone.utc),
        updated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        deleted_at=None,
        latest_review_decision=ReviewDecision.APPROVE,
    )
    assert record.state is Phase3BState.READY_FOR_REVIEW
    assert record.latest_review_decision is ReviewDecision.APPROVE


def test_phase3b_page_capture_rejects_blank_text() -> None:
    with pytest.raises(DocumentAdmissionValidationError, match="invalid_text"):
        Phase3BPageCapture(
            page_number=1,
            method="native",
            text=" ",
            warnings=(),
            limitations=(),
        )


@pytest.mark.parametrize(
    "safe_name",
    [
        "../synthetic.txt",
        "folder/synthetic.txt",
        "folder\\synthetic.txt",
        "synthetic\x00.txt",
        "x" * 256,
        ".",
        "..",
    ],
)
def test_safe_name_rejects_unsafe_values(safe_name):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_safe_name",
    ):
        build_envelope(safe_name=safe_name)


def test_envelope_requires_aware_timestamp():
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_received_at",
    ):
        build_envelope(received_at=datetime(2026, 8, 5))


def test_envelope_normalizes_provenance_and_rejects_duplicates():
    envelope = build_envelope(
        provenance_evidence_ids=["evidence-1", "evidence-2"]
    )
    assert envelope.provenance_evidence_ids == (
        "evidence-1",
        "evidence-2",
    )

    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_provenance_evidence_ids",
    ):
        build_envelope(
            provenance_evidence_ids=["evidence-1", "evidence-1"]
        )


def test_content_identity_requires_exact_sha256_shape():
    valid = ContentIdentity(
        digest_policy_id="synthetic-sha256",
        digest_policy_version="1",
        algorithm="sha256",
        digest_hex="0" * 64,
        byte_count=0,
    )
    assert valid.byte_count == 0

    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_digest_hex",
    ):
        replace(valid, digest_hex="ABC")


def test_admission_context_requires_unique_exact_identity_counts():
    context = build_admission_context()
    assert len(context.transition_ids) == 3
    assert len(context.audit_event_ids) == 3

    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_admission_operation_identity_count",
    ):
        replace(context, transition_ids=("only-one",))
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_admission_operation_identities",
    ):
        replace(
            context,
            integrity_evidence_id=context.quarantine_id,
        )


def test_admission_context_rejects_reversed_times():
    context = build_admission_context()
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_admission_operation_times",
    ):
        replace(
            context,
            validating_at=context.completed_at,
        )


def test_retry_evidence_is_immutable_and_requires_evidence():
    retry = build_retry(
        "attempt-1",
        retry_kind=RetryKind.AUTHORIZED_REVIEW,
    )
    assert retry.evidence_ids == ("retry-evidence-1",)
    with pytest.raises(FrozenInstanceError):
        retry.reason_code = "changed"
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_evidence_ids",
    ):
        replace(retry, evidence_ids=())


def test_detection_result_requires_format_only_when_detected():
    result = FormatDetectionResult(
        detection_id="detection-1",
        submission_id="submission-1",
        admission_attempt_id="attempt-1",
        detector_id="detector",
        detector_version="1",
        resource_policy_id="synthetic-resource-limits",
        resource_policy_version="1",
        state=FormatDetectionState.UNSUPPORTED,
        detected_format=None,
        supplied_media_type="application/octet-stream",
        safe_filename_suffix=".bin",
        reason_code="unsupported",
        finding_codes=(),
        checked_at=NOW,
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_detected_format",
    ):
        replace(
            result,
            state=FormatDetectionState.DETECTED,
        )


def test_eligible_decision_cannot_target_runtime_consumer():
    decision = ConsumerEligibilityDecision(
        decision_id="decision-1",
        transformation_attempt_id="transformation-1",
        consumer_id="synthetic_validation_consumer",
        consumer_policy_id="synthetic-consumer-policy",
        consumer_policy_version="1",
        intended_use="synthetic_contract_validation",
        classification="synthetic_non_sensitive",
        outcome=ConsumerEligibilityOutcome.ELIGIBLE,
        reason_code="eligible",
        evidence_references=(),
        decided_at=NOW,
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_eligible_consumer",
    ):
        replace(decision, consumer_id="runtime")


def test_domain_records_have_no_content_body_fields():
    prohibited = {
        "content",
        "body",
        "document_bytes",
        "extracted_text",
        "raw_output",
        "prompt",
    }
    assert prohibited.isdisjoint(
        field.name for field in fields(SubmissionEnvelope)
    )
