from datetime import timedelta

import pytest

from collector.document_admission import (
    AdmissionState,
    CleanupFailed,
    DocumentAdmissionConflict,
    DocumentAdmissionNotFound,
    DocumentAdmissionValidationError,
    EvaluatorUnavailable,
    InspectionFailed,
    PolicyViolation,
    QuarantineFailure,
    ResourceLimitExceeded,
    RetryKind,
    TransformationState,
    UnknownOutcome,
    synthetic_inspection_policy,
)

from .synthetic_fixtures import (
    AMBIGUOUS,
    DETECTOR_UNAVAILABLE,
    NOW,
    UNSUPPORTED,
    VALID_TXT,
    build_admission_context,
    build_envelope,
    build_inspection_context,
    build_policies,
    build_retry,
    build_system,
    submit_valid,
)


def test_held_admission_retry_creates_linked_immutable_attempt():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(),
    )
    retry = build_retry(
        prior.admission_attempt_id,
        retry_kind=RetryKind.AUTHORIZED_REVIEW,
    )
    retried = system.orchestrator.retry_admission(
        prior,
        retry,
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(
            "2",
            base_time=NOW + timedelta(seconds=6),
        ),
    )
    assert prior.state is AdmissionState.HELD
    assert retried.state is AdmissionState.HELD
    assert (
        retried.prior_admission_attempt_id
        == prior.admission_attempt_id
    )
    assert retried.retry_evidence == retry
    assert (
        retried.authorized_review_evidence_id
        == retry.evidence_ids[0]
    )


def test_unavailable_dependency_retry_uses_new_attempt_identity():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        DETECTOR_UNAVAILABLE,
        build_policies(),
        build_admission_context(),
    )
    retried = system.orchestrator.retry_admission(
        prior,
        build_retry(
            prior.admission_attempt_id,
            retry_kind=RetryKind.DEPENDENCY_RESTORED,
        ),
        build_envelope(),
        DETECTOR_UNAVAILABLE,
        build_policies(),
        build_admission_context(
            "2",
            base_time=NOW + timedelta(seconds=6),
        ),
    )
    assert prior.state is AdmissionState.EVALUATION_FAILED
    assert retried.state is AdmissionState.EVALUATION_FAILED
    assert retried.admission_attempt_id != prior.admission_attempt_id


def test_rejected_retry_requires_corrected_new_submission():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        UNSUPPORTED,
        build_policies(),
        build_admission_context(),
    )
    new_envelope = build_envelope(
        submission_id="synthetic-submission-corrected",
        received_at=NOW + timedelta(seconds=6),
    )
    retried = system.orchestrator.retry_admission(
        prior,
        build_retry(
            prior.admission_attempt_id,
            retry_kind=RetryKind.CORRECTED_RESUBMISSION,
        ),
        new_envelope,
        VALID_TXT,
        build_policies(),
        build_admission_context(
            "2",
            base_time=NOW + timedelta(seconds=6),
        ),
    )
    assert prior.state is AdmissionState.REJECTED
    assert retried.state is AdmissionState.ACCEPTED
    assert retried.submission_id != prior.submission_id


def test_corrected_resubmission_cannot_reuse_submission_id():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        UNSUPPORTED,
        build_policies(),
        build_admission_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="corrected_resubmission_requires_new_submission",
    ):
        system.orchestrator.retry_admission(
            prior,
            build_retry(
                prior.admission_attempt_id,
                retry_kind=RetryKind.CORRECTED_RESUBMISSION,
            ),
            build_envelope(),
            VALID_TXT,
            build_policies(),
            build_admission_context(
                "2",
                base_time=NOW + timedelta(seconds=6),
            ),
        )


def test_accepted_attempt_cannot_be_retried():
    system = build_system()
    prior = submit_valid(system)
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_retry_kind",
    ):
        system.orchestrator.retry_admission(
            prior,
            build_retry(
                prior.admission_attempt_id,
                retry_kind=RetryKind.AUTHORIZED_REVIEW,
            ),
            build_envelope(),
            VALID_TXT,
            build_policies(),
            build_admission_context(
                "2",
                base_time=NOW + timedelta(seconds=6),
            ),
        )


def test_stale_retry_identity_is_rejected():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(),
    )
    stale = build_retry(
        "different-prior-attempt",
        retry_kind=RetryKind.AUTHORIZED_REVIEW,
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="retry_prior_attempt_mismatch",
    ):
        system.orchestrator.retry_admission(
            prior,
            stale,
            build_envelope(),
            AMBIGUOUS,
            build_policies(),
            build_admission_context(
                "2",
                base_time=NOW + timedelta(seconds=6),
            ),
        )


def test_retry_kind_must_match_terminal_disposition():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_retry_kind",
    ):
        system.orchestrator.retry_admission(
            prior,
            build_retry(
                prior.admission_attempt_id,
                retry_kind=RetryKind.DEPENDENCY_RESTORED,
            ),
            build_envelope(),
            AMBIGUOUS,
            build_policies(),
            build_admission_context(
                "2",
                base_time=NOW + timedelta(seconds=6),
            ),
        )


def test_admission_retry_requires_new_attempt_identity():
    system = build_system()
    prior = system.orchestrator.submit(
        build_envelope(),
        AMBIGUOUS,
        build_policies(),
        build_admission_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="retry_requires_new_attempt_identity",
    ):
        system.orchestrator.retry_admission(
            prior,
            build_retry(
                prior.admission_attempt_id,
                retry_kind=RetryKind.AUTHORIZED_REVIEW,
            ),
            build_envelope(),
            AMBIGUOUS,
            build_policies(),
            build_admission_context(),
        )


def test_failed_inspection_retry_can_become_ready():
    system = build_system(inspector_mode="partial")
    admission = submit_valid(system)
    prior = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    system.inspector.mode = "complete"
    retried = system.orchestrator.retry_inspection(
        admission,
        prior,
        build_retry(
            prior.transformation_attempt_id,
            retry_kind=RetryKind.DEPENDENCY_RESTORED,
        ),
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(
            "2",
            base_time=NOW + timedelta(seconds=8),
        ),
    )
    assert prior.state is TransformationState.PROCESSING_FAILED
    assert retried.state is TransformationState.READY
    assert (
        retried.prior_transformation_attempt_id
        == prior.transformation_attempt_id
    )


def test_inspection_retry_requires_new_attempt_identity():
    system = build_system(inspector_mode="none")
    admission = submit_valid(system)
    prior = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="retry_requires_new_attempt_identity",
    ):
        system.orchestrator.retry_inspection(
            admission,
            prior,
            build_retry(
                prior.transformation_attempt_id,
                retry_kind=RetryKind.DEPENDENCY_RESTORED,
            ),
            synthetic_inspection_policy(),
            build_policies().consumer,
            build_inspection_context(),
        )


def test_ready_transformation_cannot_be_retried():
    system = build_system()
    admission = submit_valid(system)
    ready = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="prior_transformation_not_failed",
    ):
        system.orchestrator.retry_inspection(
            admission,
            ready,
            build_retry(
                ready.transformation_attempt_id,
                retry_kind=RetryKind.DEPENDENCY_RESTORED,
            ),
            synthetic_inspection_policy(),
            build_policies().consumer,
            build_inspection_context(
                "2",
                base_time=NOW + timedelta(seconds=8),
            ),
        )


def test_corrected_resubmission_is_not_inspection_retry():
    system = build_system(inspector_mode="none")
    admission = submit_valid(system)
    failed = system.orchestrator.inspect(
        admission,
        synthetic_inspection_policy(),
        build_policies().consumer,
        build_inspection_context(),
    )
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_retry_kind",
    ):
        system.orchestrator.retry_inspection(
            admission,
            failed,
            build_retry(
                failed.transformation_attempt_id,
                retry_kind=RetryKind.CORRECTED_RESUBMISSION,
            ),
            synthetic_inspection_policy(),
            build_policies().consumer,
            build_inspection_context(
                "2",
                base_time=NOW + timedelta(seconds=8),
            ),
        )


@pytest.mark.parametrize(
    "failure_type",
    [
        DocumentAdmissionValidationError,
        DocumentAdmissionConflict,
        DocumentAdmissionNotFound,
        EvaluatorUnavailable,
        PolicyViolation,
        ResourceLimitExceeded,
        InspectionFailed,
        QuarantineFailure,
        CleanupFailed,
        UnknownOutcome,
    ],
)
def test_typed_failures_expose_only_safe_reason_and_identifiers(
    failure_type,
):
    failure = failure_type("synthetic_reason", "safe-attempt-id")
    assert failure.reason_code == "synthetic_reason"
    assert failure.safe_identifiers == ("safe-attempt-id",)
    assert str(failure) == "synthetic_reason: safe-attempt-id"
    assert "SYNTHETIC-TXT" not in str(failure)
