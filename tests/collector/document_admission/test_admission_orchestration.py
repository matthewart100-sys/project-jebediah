from dataclasses import FrozenInstanceError

import pytest

from collector.document_admission import (
    AdmissionState,
    EvaluationOutcome,
    FormatDetectionState,
)

from .synthetic_fixtures import (
    AMBIGUOUS,
    DETECTOR_UNAVAILABLE,
    TRUNCATED,
    UNSUPPORTED,
    VALID_TXT,
    build_admission_context,
    build_envelope,
    build_policies,
    build_system,
)


def test_valid_submission_records_exact_transition_chain():
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is AdmissionState.ACCEPTED
    assert tuple(
        (item.prior_state, item.next_state)
        for item in result.transitions
    ) == (
        (AdmissionState.RECEIVED, AdmissionState.QUARANTINED),
        (AdmissionState.QUARANTINED, AdmissionState.VALIDATING),
        (AdmissionState.VALIDATING, AdmissionState.ACCEPTED),
    )
    assert not hasattr(result, "runtime_eligible")
    assert not hasattr(result, "registry_write_allowed")
    assert not hasattr(result, "memory_write_allowed")


@pytest.mark.parametrize(
    ("payload", "expected_state", "reason_code"),
    [
        (UNSUPPORTED, AdmissionState.REJECTED, "unsupported_format"),
        (TRUNCATED, AdmissionState.REJECTED, "truncated_input"),
        (AMBIGUOUS, AdmissionState.HELD, "ambiguous_format"),
        (
            DETECTOR_UNAVAILABLE,
            AdmissionState.EVALUATION_FAILED,
            "detector_unavailable",
        ),
    ],
)
def test_detection_dispositions_are_fail_closed(
    payload,
    expected_state,
    reason_code,
):
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(),
        payload,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is expected_state
    assert result.disposition_reason_code == reason_code
    assert not hasattr(result, "runtime_eligible")


@pytest.mark.parametrize(
    ("outcome", "expected_state"),
    [
        (EvaluationOutcome.REJECT, AdmissionState.REJECTED),
        (EvaluationOutcome.HOLD, AdmissionState.HELD),
        (
            EvaluationOutcome.UNAVAILABLE,
            AdmissionState.EVALUATION_FAILED,
        ),
    ],
)
def test_policy_outcomes_are_not_silently_promoted(
    outcome,
    expected_state,
):
    system = build_system(policy_outcome=outcome)
    result = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        build_admission_context(),
    )
    assert result.state is expected_state
    assert result.policy_evaluation.outcome is outcome


def test_admission_attempt_and_evidence_history_are_immutable():
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        build_admission_context(),
    )
    with pytest.raises(FrozenInstanceError):
        result.state = AdmissionState.REJECTED
    assert system.journal.admission_history(
        result.admission_attempt_id
    ) == result.transitions


def test_equal_submission_operation_is_idempotent():
    system = build_system()
    context = build_admission_context()
    first = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        context,
    )
    second = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        context,
    )
    assert second == first
    assert len(
        system.journal.admission_history(first.admission_attempt_id)
    ) == 3


def test_format_detection_is_bound_to_exact_attempt():
    system = build_system()
    result = system.orchestrator.submit(
        build_envelope(),
        VALID_TXT,
        build_policies(),
        build_admission_context(),
    )
    assert result.format_detection.state is FormatDetectionState.DETECTED
    assert (
        result.format_detection.admission_attempt_id
        == result.admission_attempt_id
    )
