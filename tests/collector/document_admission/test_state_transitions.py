import pytest

from collector.document_admission import (
    AdmissionState,
    DocumentAdmissionValidationError,
    TransformationState,
)
from collector.document_admission.state_transitions import (
    is_admission_terminal,
    is_transformation_terminal,
    validate_admission_transition,
    validate_transformation_transition,
)


@pytest.mark.parametrize(
    ("prior", "next_state"),
    [
        (AdmissionState.RECEIVED, AdmissionState.QUARANTINED),
        (AdmissionState.QUARANTINED, AdmissionState.VALIDATING),
        (AdmissionState.VALIDATING, AdmissionState.ACCEPTED),
        (AdmissionState.VALIDATING, AdmissionState.REJECTED),
        (AdmissionState.VALIDATING, AdmissionState.HELD),
        (
            AdmissionState.VALIDATING,
            AdmissionState.EVALUATION_FAILED,
        ),
    ],
)
def test_all_admission_transitions_are_allowed(prior, next_state):
    validate_admission_transition(prior, next_state)


@pytest.mark.parametrize(
    ("prior", "next_state"),
    [
        (AdmissionState.RECEIVED, AdmissionState.ACCEPTED),
        (AdmissionState.VALIDATING, AdmissionState.VALIDATING),
        (AdmissionState.ACCEPTED, AdmissionState.VALIDATING),
        (AdmissionState.REJECTED, AdmissionState.RECEIVED),
        (AdmissionState.HELD, AdmissionState.ACCEPTED),
        (
            AdmissionState.EVALUATION_FAILED,
            AdmissionState.ACCEPTED,
        ),
    ],
)
def test_skipped_self_reversed_and_terminal_transitions_fail(
    prior,
    next_state,
):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_admission_transition",
    ):
        validate_admission_transition(prior, next_state)


@pytest.mark.parametrize(
    "state",
    [
        AdmissionState.ACCEPTED,
        AdmissionState.REJECTED,
        AdmissionState.HELD,
        AdmissionState.EVALUATION_FAILED,
    ],
)
def test_exact_admission_terminal_states(state):
    assert is_admission_terminal(state) is True


@pytest.mark.parametrize(
    "state",
    [
        AdmissionState.RECEIVED,
        AdmissionState.QUARANTINED,
        AdmissionState.VALIDATING,
    ],
)
def test_in_progress_admission_states_are_not_terminal(state):
    assert is_admission_terminal(state) is False


@pytest.mark.parametrize(
    "next_state",
    [
        TransformationState.READY,
        TransformationState.PROCESSING_FAILED,
    ],
)
def test_exact_transformation_transitions(next_state):
    validate_transformation_transition(
        TransformationState.PROCESSING,
        next_state,
    )
    assert is_transformation_terminal(next_state) is True


@pytest.mark.parametrize(
    ("prior", "next_state"),
    [
        (
            TransformationState.PROCESSING,
            TransformationState.PROCESSING,
        ),
        (
            TransformationState.READY,
            TransformationState.PROCESSING,
        ),
        (
            TransformationState.PROCESSING_FAILED,
            TransformationState.READY,
        ),
    ],
)
def test_invalid_transformation_transitions_fail(prior, next_state):
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_transformation_transition",
    ):
        validate_transformation_transition(prior, next_state)
