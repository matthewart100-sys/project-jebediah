class DocumentAdmissionError(RuntimeError):
    """Base failure carrying only a reason code and safe correlation IDs."""

    def __init__(
        self,
        reason_code: str,
        *safe_identifiers: str,
    ) -> None:
        if not isinstance(reason_code, str) or not reason_code.strip():
            raise ValueError("reason_code cannot be empty")
        for identifier in safe_identifiers:
            if not isinstance(identifier, str) or not identifier.strip():
                raise ValueError("safe identifiers cannot be empty")

        self.reason_code = reason_code
        self.safe_identifiers = tuple(safe_identifiers)
        message = reason_code
        if safe_identifiers:
            message = f"{reason_code}: {', '.join(safe_identifiers)}"
        super().__init__(message)


class DocumentAdmissionValidationError(DocumentAdmissionError):
    """Raised when a model, policy, transition, or invariant is invalid."""


class DocumentAdmissionConflict(DocumentAdmissionError):
    """Raised when one immutable evidence identity is reused differently."""


class DocumentAdmissionNotFound(DocumentAdmissionError):
    """Raised when required process-local evidence is absent."""


class EvaluatorUnavailable(DocumentAdmissionError):
    """Raised when a required injected evaluator is unavailable."""


class PolicyViolation(DocumentAdmissionError):
    """Raised for a conclusive synthetic policy failure."""


class ResourceLimitExceeded(DocumentAdmissionError):
    """Raised when a named synthetic resource limit is exceeded."""


class InspectionFailed(DocumentAdmissionError):
    """Raised when scripted isolated inspection does not complete safely."""


class QuarantineFailure(DocumentAdmissionError):
    """Raised when process-local quarantine or integrity handling fails."""


class CleanupFailed(DocumentAdmissionError):
    """Raised when required synthetic cleanup does not complete."""


class UnknownOutcome(DocumentAdmissionError):
    """Raised when an indeterminate operation requires reconciliation."""
