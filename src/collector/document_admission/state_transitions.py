from .failures import DocumentAdmissionValidationError
from .models import (
    ADMISSION_TERMINAL_STATES,
    ADMISSION_TRANSITIONS,
    TRANSFORMATION_TERMINAL_STATES,
    TRANSFORMATION_TRANSITIONS,
    AdmissionState,
    TransformationState,
)


def validate_admission_transition(
    prior_state: AdmissionState,
    next_state: AdmissionState,
) -> None:
    if not isinstance(prior_state, AdmissionState) or not isinstance(
        next_state,
        AdmissionState,
    ):
        raise DocumentAdmissionValidationError(
            "invalid_admission_transition"
        )
    if (prior_state, next_state) not in ADMISSION_TRANSITIONS:
        raise DocumentAdmissionValidationError(
            "invalid_admission_transition",
            prior_state.value,
            next_state.value,
        )


def validate_transformation_transition(
    prior_state: TransformationState,
    next_state: TransformationState,
) -> None:
    if not isinstance(
        prior_state,
        TransformationState,
    ) or not isinstance(next_state, TransformationState):
        raise DocumentAdmissionValidationError(
            "invalid_transformation_transition"
        )
    if (prior_state, next_state) not in TRANSFORMATION_TRANSITIONS:
        raise DocumentAdmissionValidationError(
            "invalid_transformation_transition",
            prior_state.value,
            next_state.value,
        )


def is_admission_terminal(state: AdmissionState) -> bool:
    if not isinstance(state, AdmissionState):
        raise DocumentAdmissionValidationError("invalid_admission_state")
    return state in ADMISSION_TERMINAL_STATES


def is_transformation_terminal(state: TransformationState) -> bool:
    if not isinstance(state, TransformationState):
        raise DocumentAdmissionValidationError(
            "invalid_transformation_state"
        )
    return state in TRANSFORMATION_TERMINAL_STATES
