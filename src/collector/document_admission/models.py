import base64
from collections.abc import Iterable
from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from typing import TypeVar

from .failures import DocumentAdmissionValidationError


_T = TypeVar("_T")
MAX_SAFE_NAME_LENGTH = 255


def _invalid(field_name: str) -> DocumentAdmissionValidationError:
    return DocumentAdmissionValidationError(f"invalid_{field_name}")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise _invalid(field_name)


def _require_aware(value: datetime, field_name: str) -> None:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise _invalid(field_name)


def _require_optional_aware(
    value: datetime | None,
    field_name: str,
) -> None:
    if value is not None:
        _require_aware(value, field_name)


def _require_non_negative(value: int, field_name: str) -> None:
    if type(value) is not int or value < 0:
        raise _invalid(field_name)


def _require_positive(value: int, field_name: str) -> None:
    if type(value) is not int or value <= 0:
        raise _invalid(field_name)


def _normalize_tuple(
    values: Iterable[_T],
    field_name: str,
    *,
    required: bool = False,
) -> tuple[_T, ...]:
    if isinstance(values, (str, bytes)):
        raise _invalid(field_name)
    try:
        normalized = tuple(values)
    except TypeError as error:
        raise _invalid(field_name) from error
    if required and not normalized:
        raise _invalid(field_name)
    return normalized


def _normalize_string_tuple(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool = False,
) -> tuple[str, ...]:
    normalized = _normalize_tuple(values, field_name, required=required)
    for value in normalized:
        _require_non_empty(value, field_name)
    if len(set(normalized)) != len(normalized):
        raise _invalid(field_name)
    return normalized


def _require_instance(
    value: object,
    expected_type: type[object],
    field_name: str,
) -> None:
    if not isinstance(value, expected_type):
        raise _invalid(field_name)


class AdmissionState(str, Enum):
    RECEIVED = "received"
    QUARANTINED = "quarantined"
    VALIDATING = "validating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HELD = "held"
    EVALUATION_FAILED = "evaluation_failed"


class TransformationState(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    PROCESSING_FAILED = "processing_failed"


class DocumentFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "markdown"


class FormatDetectionState(str, Enum):
    DETECTED = "detected"
    UNSUPPORTED = "unsupported"
    AMBIGUOUS = "ambiguous"
    UNAVAILABLE = "unavailable"


class EvaluationOutcome(str, Enum):
    PASS = "pass"
    REJECT = "reject"
    HOLD = "hold"
    UNAVAILABLE = "unavailable"


class ExtractionQuality(str, Enum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    NONE = "none"


class ConsumerEligibilityOutcome(str, Enum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    UNAVAILABLE = "unavailable"


class CleanupOutcome(str, Enum):
    DELETED = "deleted"
    RETAINED = "retained"
    LEGAL_HOLD = "legal_hold"
    FAILED = "failed"


class RetentionDisposition(str, Enum):
    DELETE = "delete"
    RETAIN_TEMPORARILY = "retain_temporarily"
    LEGAL_HOLD = "legal_hold"


class RetryKind(str, Enum):
    DEPENDENCY_RESTORED = "dependency_restored"
    AUTHORIZED_REVIEW = "authorized_review"
    CORRECTED_RESUBMISSION = "corrected_resubmission"


ADMISSION_TRANSITIONS = frozenset(
    {
        (AdmissionState.RECEIVED, AdmissionState.QUARANTINED),
        (AdmissionState.QUARANTINED, AdmissionState.VALIDATING),
        (AdmissionState.VALIDATING, AdmissionState.ACCEPTED),
        (AdmissionState.VALIDATING, AdmissionState.REJECTED),
        (AdmissionState.VALIDATING, AdmissionState.HELD),
        (
            AdmissionState.VALIDATING,
            AdmissionState.EVALUATION_FAILED,
        ),
    }
)
ADMISSION_TERMINAL_STATES = frozenset(
    {
        AdmissionState.ACCEPTED,
        AdmissionState.REJECTED,
        AdmissionState.HELD,
        AdmissionState.EVALUATION_FAILED,
    }
)
TRANSFORMATION_TRANSITIONS = frozenset(
    {
        (TransformationState.PROCESSING, TransformationState.READY),
        (
            TransformationState.PROCESSING,
            TransformationState.PROCESSING_FAILED,
        ),
    }
)
TRANSFORMATION_TERMINAL_STATES = frozenset(
    {
        TransformationState.READY,
        TransformationState.PROCESSING_FAILED,
    }
)


@dataclass(frozen=True)
class ContentIdentity:
    digest_policy_id: str
    digest_policy_version: str
    algorithm: str
    digest_hex: str
    byte_count: int

    def __post_init__(self) -> None:
        for name in (
            "digest_policy_id",
            "digest_policy_version",
            "algorithm",
            "digest_hex",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_non_negative(self.byte_count, "byte_count")
        if (
            self.algorithm != "sha256"
            or len(self.digest_hex) != 64
            or self.digest_hex != self.digest_hex.lower()
            or any(character not in "0123456789abcdef" for character in self.digest_hex)
        ):
            raise _invalid("digest_hex")


@dataclass(frozen=True)
class QuarantineReceipt:
    quarantine_id: str
    submission_id: str
    admission_attempt_id: str
    content_identity: ContentIdentity
    adapter_id: str
    adapter_version: str
    placed_at: datetime
    integrity_evidence_id: str

    def __post_init__(self) -> None:
        for name in (
            "quarantine_id",
            "submission_id",
            "admission_attempt_id",
            "adapter_id",
            "adapter_version",
            "integrity_evidence_id",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(
            self.content_identity,
            ContentIdentity,
            "content_identity",
        )
        _require_aware(self.placed_at, "placed_at")


@dataclass(frozen=True)
class IntegrityVerification:
    verification_id: str
    quarantine_id: str
    expected: ContentIdentity
    observed: ContentIdentity
    verifier_id: str
    verifier_version: str
    checked_at: datetime
    matches: bool

    def __post_init__(self) -> None:
        for name in (
            "verification_id",
            "quarantine_id",
            "verifier_id",
            "verifier_version",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(self.expected, ContentIdentity, "expected")
        _require_instance(self.observed, ContentIdentity, "observed")
        _require_aware(self.checked_at, "checked_at")
        if type(self.matches) is not bool:
            raise _invalid("matches")
        if self.matches != (self.expected == self.observed):
            raise _invalid("matches")


@dataclass(frozen=True)
class SubmissionEnvelope:
    submission_id: str
    source_authority_id: str
    safe_source_reference: str
    producer_id: str
    submitter_id: str
    information_domain: str
    intended_use: str
    consumer_id: str
    consumer_policy_id: str
    consumer_policy_version: str
    supplied_name: str
    safe_name: str
    claimed_media_type: str
    classification: str
    retention_policy_id: str
    retention_policy_version: str
    deletion_policy_id: str
    deletion_policy_version: str
    resource_policy_id: str
    resource_policy_version: str
    provenance_evidence_ids: tuple[str, ...]
    received_at: datetime
    correlation_id: str

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {"provenance_evidence_ids", "received_at"}:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        if (
            len(self.safe_name) > MAX_SAFE_NAME_LENGTH
            or self.safe_name in {".", ".."}
            or any(character in self.safe_name for character in ("/", "\\"))
            or any(ord(character) < 32 for character in self.safe_name)
        ):
            raise _invalid("safe_name")
        object.__setattr__(
            self,
            "provenance_evidence_ids",
            _normalize_string_tuple(
                self.provenance_evidence_ids,
                "provenance_evidence_ids",
                required=True,
            ),
        )
        _require_aware(self.received_at, "received_at")
        exact_values = {
            "source_authority_id": "synthetic_fixture_authority",
            "safe_source_reference": "generated_in_test",
            "producer_id": "synthetic_fixture_builder",
            "submitter_id": "synthetic_test_caller",
            "information_domain": "synthetic_document_inspection",
            "intended_use": "synthetic_contract_validation",
            "consumer_id": "synthetic_validation_consumer",
            "classification": "synthetic_non_sensitive",
        }
        for field_name, expected in exact_values.items():
            if getattr(self, field_name) != expected:
                raise _invalid(field_name)


@dataclass(frozen=True)
class AdmissionOperationContext:
    admission_attempt_id: str
    quarantine_id: str
    integrity_evidence_id: str
    integrity_verification_id: str
    format_detection_id: str
    security_evaluation_id: str
    policy_evaluation_id: str
    transition_ids: tuple[str, ...]
    audit_event_ids: tuple[str, ...]
    quarantined_at: datetime
    validating_at: datetime
    checked_at: datetime
    completed_at: datetime

    def __post_init__(self) -> None:
        scalar_ids = (
            self.admission_attempt_id,
            self.quarantine_id,
            self.integrity_evidence_id,
            self.integrity_verification_id,
            self.format_detection_id,
            self.security_evaluation_id,
            self.policy_evaluation_id,
        )
        for value in scalar_ids:
            _require_non_empty(value, "admission_operation_identity")
        transition_ids = _normalize_string_tuple(
            self.transition_ids,
            "transition_ids",
            required=True,
        )
        audit_event_ids = _normalize_string_tuple(
            self.audit_event_ids,
            "audit_event_ids",
            required=True,
        )
        if len(transition_ids) != 3 or len(audit_event_ids) != 3:
            raise _invalid("admission_operation_identity_count")
        all_ids = scalar_ids + transition_ids + audit_event_ids
        if len(set(all_ids)) != len(all_ids):
            raise _invalid("admission_operation_identities")
        object.__setattr__(self, "transition_ids", transition_ids)
        object.__setattr__(self, "audit_event_ids", audit_event_ids)
        times = (
            self.quarantined_at,
            self.validating_at,
            self.checked_at,
            self.completed_at,
        )
        for value in times:
            _require_aware(value, "admission_operation_time")
        if tuple(sorted(times)) != times:
            raise _invalid("admission_operation_times")


@dataclass(frozen=True)
class InspectionOperationContext:
    transformation_attempt_id: str
    inspection_result_id: str
    consumer_eligibility_decision_id: str
    transition_id: str
    audit_event_id: str
    started_at: datetime
    decided_at: datetime
    completed_at: datetime

    def __post_init__(self) -> None:
        identities = (
            self.transformation_attempt_id,
            self.inspection_result_id,
            self.consumer_eligibility_decision_id,
            self.transition_id,
            self.audit_event_id,
        )
        for value in identities:
            _require_non_empty(value, "inspection_operation_identity")
        if len(set(identities)) != len(identities):
            raise _invalid("inspection_operation_identities")
        times = (self.started_at, self.decided_at, self.completed_at)
        for value in times:
            _require_aware(value, "inspection_operation_time")
        if tuple(sorted(times)) != times:
            raise _invalid("inspection_operation_times")


@dataclass(frozen=True)
class CleanupOperationContext:
    cleanup_id: str
    audit_event_id: str
    requested_at: datetime
    completed_at: datetime

    def __post_init__(self) -> None:
        _require_non_empty(self.cleanup_id, "cleanup_id")
        _require_non_empty(self.audit_event_id, "audit_event_id")
        if self.cleanup_id == self.audit_event_id:
            raise _invalid("cleanup_operation_identities")
        _require_aware(self.requested_at, "requested_at")
        _require_aware(self.completed_at, "completed_at")
        if self.completed_at < self.requested_at:
            raise _invalid("completed_at")


@dataclass(frozen=True)
class RetryEvidence:
    retry_id: str
    prior_attempt_id: str
    retry_kind: RetryKind
    authorized_role: str
    reason_code: str
    evidence_ids: tuple[str, ...]
    decided_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "retry_id",
            "prior_attempt_id",
            "authorized_role",
            "reason_code",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(self.retry_kind, RetryKind, "retry_kind")
        object.__setattr__(
            self,
            "evidence_ids",
            _normalize_string_tuple(
                self.evidence_ids,
                "evidence_ids",
                required=True,
            ),
        )
        _require_aware(self.decided_at, "decided_at")


@dataclass(frozen=True)
class FormatDetectionResult:
    detection_id: str
    submission_id: str
    admission_attempt_id: str
    detector_id: str
    detector_version: str
    resource_policy_id: str
    resource_policy_version: str
    state: FormatDetectionState
    detected_format: DocumentFormat | None
    supplied_media_type: str
    safe_filename_suffix: str
    reason_code: str
    finding_codes: tuple[str, ...]
    checked_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "detection_id",
            "submission_id",
            "admission_attempt_id",
            "detector_id",
            "detector_version",
            "resource_policy_id",
            "resource_policy_version",
            "supplied_media_type",
            "safe_filename_suffix",
            "reason_code",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(self.state, FormatDetectionState, "state")
        if (self.state is FormatDetectionState.DETECTED) != (
            self.detected_format is not None
        ):
            raise _invalid("detected_format")
        if self.detected_format is not None:
            _require_instance(
                self.detected_format,
                DocumentFormat,
                "detected_format",
            )
        object.__setattr__(
            self,
            "finding_codes",
            _normalize_string_tuple(self.finding_codes, "finding_codes"),
        )
        _require_aware(self.checked_at, "checked_at")


@dataclass(frozen=True)
class SecurityEvaluation:
    evaluation_id: str
    submission_id: str
    admission_attempt_id: str
    evaluator_id: str
    evaluator_version: str
    resource_policy_id: str
    resource_policy_version: str
    outcome: EvaluationOutcome
    reason_code: str
    evidence_references: tuple[str, ...]
    checked_at: datetime

    def __post_init__(self) -> None:
        _validate_evaluation(self)


@dataclass(frozen=True)
class PolicyEvaluation:
    evaluation_id: str
    submission_id: str
    admission_attempt_id: str
    evaluator_id: str
    evaluator_version: str
    consumer_policy_id: str
    consumer_policy_version: str
    retention_policy_id: str
    retention_policy_version: str
    deletion_policy_id: str
    deletion_policy_version: str
    resource_policy_id: str
    resource_policy_version: str
    outcome: EvaluationOutcome
    reason_code: str
    evidence_references: tuple[str, ...]
    checked_at: datetime

    def __post_init__(self) -> None:
        _validate_evaluation(self)


def _validate_evaluation(value: SecurityEvaluation | PolicyEvaluation) -> None:
    for field in fields(value):
        if field.name in {"outcome", "evidence_references", "checked_at"}:
            continue
        _require_non_empty(getattr(value, field.name), field.name)
    _require_instance(value.outcome, EvaluationOutcome, "outcome")
    object.__setattr__(
        value,
        "evidence_references",
        _normalize_string_tuple(
            value.evidence_references,
            "evidence_references",
        ),
    )
    _require_aware(value.checked_at, "checked_at")


@dataclass(frozen=True)
class ConsumerEligibilityDecision:
    decision_id: str
    transformation_attempt_id: str
    consumer_id: str
    consumer_policy_id: str
    consumer_policy_version: str
    intended_use: str
    classification: str
    outcome: ConsumerEligibilityOutcome
    reason_code: str
    evidence_references: tuple[str, ...]
    decided_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "decision_id",
            "transformation_attempt_id",
            "consumer_id",
            "consumer_policy_id",
            "consumer_policy_version",
            "intended_use",
            "classification",
            "reason_code",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(
            self.outcome,
            ConsumerEligibilityOutcome,
            "outcome",
        )
        object.__setattr__(
            self,
            "evidence_references",
            _normalize_string_tuple(
                self.evidence_references,
                "evidence_references",
            ),
        )
        _require_aware(self.decided_at, "decided_at")
        if self.outcome is ConsumerEligibilityOutcome.ELIGIBLE:
            exact = (
                self.consumer_id == "synthetic_validation_consumer"
                and self.consumer_policy_id == "synthetic-consumer-policy"
                and self.consumer_policy_version == "1"
                and self.intended_use == "synthetic_contract_validation"
                and self.classification == "synthetic_non_sensitive"
            )
            if not exact:
                raise _invalid("eligible_consumer")


RESOURCE_LIMIT_FIELDS = (
    "max_input_bytes",
    "max_result_bytes",
    "max_temporary_bytes",
    "max_wall_clock_milliseconds",
    "max_cpu_milliseconds",
    "max_process_memory_bytes",
    "max_warning_count",
    "max_finding_count",
    "max_decoded_characters",
    "max_text_lines",
    "max_text_line_length",
    "max_links_or_directives",
    "max_pdf_pages",
    "max_pdf_objects",
    "max_pdf_object_depth",
    "max_pdf_stream_bytes",
    "max_pdf_embedded_objects",
    "max_pdf_fonts",
    "max_pdf_extracted_characters",
    "max_docx_archive_entries",
    "max_docx_expanded_bytes",
    "max_docx_per_entry_bytes",
    "max_docx_compression_ratio",
    "max_docx_relationships",
    "max_docx_xml_depth",
    "max_docx_extracted_characters",
)
OBSERVED_RESOURCE_FIELDS = tuple(
    field_name.replace("max_", "observed_", 1)
    for field_name in RESOURCE_LIMIT_FIELDS
)


@dataclass(frozen=True)
class ResourceObservation:
    observation_id: str
    resource_policy_id: str
    resource_policy_version: str
    observed_input_bytes: int
    observed_result_bytes: int
    observed_temporary_bytes: int
    observed_wall_clock_milliseconds: int
    observed_cpu_milliseconds: int
    observed_process_memory_bytes: int
    observed_warning_count: int
    observed_finding_count: int
    observed_decoded_characters: int
    observed_text_lines: int
    observed_text_line_length: int
    observed_links_or_directives: int
    observed_pdf_pages: int
    observed_pdf_objects: int
    observed_pdf_object_depth: int
    observed_pdf_stream_bytes: int
    observed_pdf_embedded_objects: int
    observed_pdf_fonts: int
    observed_pdf_extracted_characters: int
    observed_docx_archive_entries: int
    observed_docx_expanded_bytes: int
    observed_docx_per_entry_bytes: int
    observed_docx_compression_ratio: int
    observed_docx_relationships: int
    observed_docx_xml_depth: int
    observed_docx_extracted_characters: int
    exceeded_limit_names: tuple[str, ...]
    observed_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "observation_id",
            "resource_policy_id",
            "resource_policy_version",
        ):
            _require_non_empty(getattr(self, name), name)
        for name in OBSERVED_RESOURCE_FIELDS:
            _require_non_negative(getattr(self, name), name)
        exceeded = _normalize_string_tuple(
            self.exceeded_limit_names,
            "exceeded_limit_names",
        )
        if not set(exceeded).issubset(RESOURCE_LIMIT_FIELDS):
            raise _invalid("exceeded_limit_names")
        object.__setattr__(self, "exceeded_limit_names", exceeded)
        _require_aware(self.observed_at, "observed_at")


@dataclass(frozen=True)
class AdmissionTransition:
    transition_id: str
    submission_id: str
    admission_attempt_id: str
    prior_state: AdmissionState
    next_state: AdmissionState
    occurred_at: datetime
    actor_id: str
    component_id: str
    reason_code: str
    policy_id: str
    policy_version: str
    correlation_id: str

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {"prior_state", "next_state", "occurred_at"}:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        _require_instance(self.prior_state, AdmissionState, "prior_state")
        _require_instance(self.next_state, AdmissionState, "next_state")
        _require_aware(self.occurred_at, "occurred_at")
        if (self.prior_state, self.next_state) not in ADMISSION_TRANSITIONS:
            raise _invalid("admission_transition")


@dataclass(frozen=True)
class TransformationTransition:
    transition_id: str
    submission_id: str
    transformation_attempt_id: str
    prior_state: TransformationState
    next_state: TransformationState
    occurred_at: datetime
    actor_id: str
    component_id: str
    reason_code: str
    policy_id: str
    policy_version: str
    correlation_id: str

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {"prior_state", "next_state", "occurred_at"}:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        _require_instance(
            self.prior_state,
            TransformationState,
            "prior_state",
        )
        _require_instance(
            self.next_state,
            TransformationState,
            "next_state",
        )
        _require_aware(self.occurred_at, "occurred_at")
        if (
            self.prior_state,
            self.next_state,
        ) not in TRANSFORMATION_TRANSITIONS:
            raise _invalid("transformation_transition")


@dataclass(frozen=True)
class AdmissionAttemptRecord:
    admission_attempt_id: str
    submission_id: str
    prior_admission_attempt_id: str | None
    retry_evidence: RetryEvidence | None
    state: AdmissionState
    quarantine_receipt: QuarantineReceipt | None
    integrity_verification: IntegrityVerification | None
    transitions: tuple[AdmissionTransition, ...]
    format_detection: FormatDetectionResult | None
    security_evaluation: SecurityEvaluation | None
    policy_evaluation: PolicyEvaluation | None
    started_at: datetime
    completed_at: datetime | None
    authorized_review_evidence_id: str | None
    disposition_reason_code: str
    correlation_id: str

    def __post_init__(self) -> None:
        for name in (
            "admission_attempt_id",
            "submission_id",
            "disposition_reason_code",
            "correlation_id",
        ):
            _require_non_empty(getattr(self, name), name)
        for name in (
            "prior_admission_attempt_id",
            "authorized_review_evidence_id",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_non_empty(value, name)
        _require_instance(self.state, AdmissionState, "state")
        _require_aware(self.started_at, "started_at")
        _require_optional_aware(self.completed_at, "completed_at")
        transitions = _normalize_tuple(self.transitions, "transitions")
        if not all(
            isinstance(item, AdmissionTransition) for item in transitions
        ):
            raise _invalid("transitions")
        object.__setattr__(self, "transitions", transitions)
        if self.state is AdmissionState.RECEIVED:
            if transitions or self.completed_at is not None:
                raise _invalid("received_state")
        else:
            if not transitions:
                raise _invalid("transitions")
            expected_prior = AdmissionState.RECEIVED
            for transition in transitions:
                if (
                    transition.submission_id != self.submission_id
                    or transition.admission_attempt_id
                    != self.admission_attempt_id
                    or transition.prior_state is not expected_prior
                ):
                    raise _invalid("transitions")
                expected_prior = transition.next_state
            if expected_prior is not self.state:
                raise _invalid("state")
        terminal = self.state in ADMISSION_TERMINAL_STATES
        if terminal != (self.completed_at is not None):
            raise _invalid("completed_at")
        if self.retry_evidence is not None:
            _require_instance(
                self.retry_evidence,
                RetryEvidence,
                "retry_evidence",
            )
            if (
                self.prior_admission_attempt_id is None
                or self.retry_evidence.prior_attempt_id
                != self.prior_admission_attempt_id
            ):
                raise _invalid("retry_evidence")
        elif self.prior_admission_attempt_id is not None:
            raise _invalid("retry_evidence")
        if self.quarantine_receipt is not None:
            _require_instance(
                self.quarantine_receipt,
                QuarantineReceipt,
                "quarantine_receipt",
            )
            if (
                self.quarantine_receipt.submission_id != self.submission_id
                or self.quarantine_receipt.admission_attempt_id
                != self.admission_attempt_id
            ):
                raise _invalid("quarantine_receipt")
        if self.integrity_verification is not None:
            _require_instance(
                self.integrity_verification,
                IntegrityVerification,
                "integrity_verification",
            )
        for name, expected_type in (
            ("format_detection", FormatDetectionResult),
            ("security_evaluation", SecurityEvaluation),
            ("policy_evaluation", PolicyEvaluation),
        ):
            value = getattr(self, name)
            if value is not None:
                _require_instance(value, expected_type, name)
                if (
                    value.submission_id != self.submission_id
                    or value.admission_attempt_id
                    != self.admission_attempt_id
                ):
                    raise _invalid(name)
        if self.state in {
            AdmissionState.QUARANTINED,
            AdmissionState.VALIDATING,
        } | ADMISSION_TERMINAL_STATES:
            if self.quarantine_receipt is None:
                raise _invalid("quarantine_receipt")
        if self.state in {
            AdmissionState.VALIDATING,
        } | ADMISSION_TERMINAL_STATES:
            if (
                self.integrity_verification is None
                or not self.integrity_verification.matches
            ):
                raise _invalid("integrity_verification")
        if self.state is AdmissionState.ACCEPTED:
            if (
                self.format_detection is None
                or self.format_detection.state
                is not FormatDetectionState.DETECTED
                or self.security_evaluation is None
                or self.security_evaluation.outcome
                is not EvaluationOutcome.PASS
                or self.policy_evaluation is None
                or self.policy_evaluation.outcome
                is not EvaluationOutcome.PASS
            ):
                raise _invalid("accepted_evidence")


@dataclass(frozen=True)
class OutputIdentity:
    output_id: str
    output_version: str
    output_content_identity: ContentIdentity
    output_kind: str
    input_content_identity: ContentIdentity

    def __post_init__(self) -> None:
        for name in ("output_id", "output_version", "output_kind"):
            _require_non_empty(getattr(self, name), name)
        _require_instance(
            self.output_content_identity,
            ContentIdentity,
            "output_content_identity",
        )
        _require_instance(
            self.input_content_identity,
            ContentIdentity,
            "input_content_identity",
        )


@dataclass(frozen=True)
class InspectionResult:
    inspection_result_id: str
    submission_id: str
    transformation_attempt_id: str
    input_content_identity: ContentIdentity
    inspector_id: str
    inspector_version: str
    configuration_id: str
    configuration_version: str
    code_identity: str
    code_version: str
    policy_id: str
    policy_version: str
    started_at: datetime
    completed_at: datetime
    detected_format: DocumentFormat
    output_identity: OutputIdentity | None
    extraction_quality: ExtractionQuality
    location_map_available: bool
    unit_count: int
    extracted_character_count: int
    warning_codes: tuple[str, ...]
    omission_codes: tuple[str, ...]
    reached_limit_names: tuple[str, ...]
    failure_kind: str | None
    resource_observation: ResourceObservation

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {
                "input_content_identity",
                "started_at",
                "completed_at",
                "detected_format",
                "output_identity",
                "extraction_quality",
                "location_map_available",
                "unit_count",
                "extracted_character_count",
                "warning_codes",
                "omission_codes",
                "reached_limit_names",
                "failure_kind",
                "resource_observation",
            }:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        _require_instance(
            self.input_content_identity,
            ContentIdentity,
            "input_content_identity",
        )
        _require_aware(self.started_at, "started_at")
        _require_aware(self.completed_at, "completed_at")
        if self.completed_at < self.started_at:
            raise _invalid("completed_at")
        _require_instance(
            self.detected_format,
            DocumentFormat,
            "detected_format",
        )
        _require_instance(
            self.extraction_quality,
            ExtractionQuality,
            "extraction_quality",
        )
        if type(self.location_map_available) is not bool:
            raise _invalid("location_map_available")
        _require_non_negative(self.unit_count, "unit_count")
        _require_non_negative(
            self.extracted_character_count,
            "extracted_character_count",
        )
        for name in (
            "warning_codes",
            "omission_codes",
            "reached_limit_names",
        ):
            object.__setattr__(
                self,
                name,
                _normalize_string_tuple(getattr(self, name), name),
            )
        if self.failure_kind is not None:
            _require_non_empty(self.failure_kind, "failure_kind")
        _require_instance(
            self.resource_observation,
            ResourceObservation,
            "resource_observation",
        )
        if self.output_identity is not None:
            _require_instance(
                self.output_identity,
                OutputIdentity,
                "output_identity",
            )
            if (
                self.output_identity.input_content_identity
                != self.input_content_identity
            ):
                raise _invalid("output_identity")
        if self.extraction_quality is ExtractionQuality.COMPLETE:
            if self.output_identity is None or self.failure_kind is not None:
                raise _invalid("complete_inspection")
        elif self.output_identity is not None:
            raise _invalid("incomplete_output_identity")


@dataclass(frozen=True)
class TransformationAttemptRecord:
    transformation_attempt_id: str
    submission_id: str
    admission_attempt_id: str
    prior_transformation_attempt_id: str | None
    retry_evidence: RetryEvidence | None
    state: TransformationState
    transitions: tuple[TransformationTransition, ...]
    inspection_result: InspectionResult | None
    consumer_eligibility_decision: ConsumerEligibilityDecision | None
    started_at: datetime
    completed_at: datetime | None
    disposition_reason_code: str
    correlation_id: str

    def __post_init__(self) -> None:
        for name in (
            "transformation_attempt_id",
            "submission_id",
            "admission_attempt_id",
            "disposition_reason_code",
            "correlation_id",
        ):
            _require_non_empty(getattr(self, name), name)
        if self.prior_transformation_attempt_id is not None:
            _require_non_empty(
                self.prior_transformation_attempt_id,
                "prior_transformation_attempt_id",
            )
        _require_instance(self.state, TransformationState, "state")
        _require_aware(self.started_at, "started_at")
        _require_optional_aware(self.completed_at, "completed_at")
        transitions = _normalize_tuple(self.transitions, "transitions")
        if not all(
            isinstance(item, TransformationTransition)
            for item in transitions
        ):
            raise _invalid("transitions")
        object.__setattr__(self, "transitions", transitions)
        if self.state is TransformationState.PROCESSING:
            if transitions or self.completed_at is not None:
                raise _invalid("processing_state")
        else:
            if len(transitions) != 1:
                raise _invalid("transitions")
            transition = transitions[0]
            if (
                transition.submission_id != self.submission_id
                or transition.transformation_attempt_id
                != self.transformation_attempt_id
                or transition.prior_state
                is not TransformationState.PROCESSING
                or transition.next_state is not self.state
            ):
                raise _invalid("transitions")
        terminal = self.state in TRANSFORMATION_TERMINAL_STATES
        if terminal != (self.completed_at is not None):
            raise _invalid("completed_at")
        if self.retry_evidence is not None:
            _require_instance(
                self.retry_evidence,
                RetryEvidence,
                "retry_evidence",
            )
            if (
                self.prior_transformation_attempt_id is None
                or self.retry_evidence.prior_attempt_id
                != self.prior_transformation_attempt_id
            ):
                raise _invalid("retry_evidence")
        elif self.prior_transformation_attempt_id is not None:
            raise _invalid("retry_evidence")
        if self.inspection_result is not None:
            _require_instance(
                self.inspection_result,
                InspectionResult,
                "inspection_result",
            )
            if (
                self.inspection_result.submission_id != self.submission_id
                or self.inspection_result.transformation_attempt_id
                != self.transformation_attempt_id
            ):
                raise _invalid("inspection_result")
        if self.consumer_eligibility_decision is not None:
            _require_instance(
                self.consumer_eligibility_decision,
                ConsumerEligibilityDecision,
                "consumer_eligibility_decision",
            )
            if (
                self.consumer_eligibility_decision.transformation_attempt_id
                != self.transformation_attempt_id
            ):
                raise _invalid("consumer_eligibility_decision")
        if self.state is TransformationState.READY:
            if (
                self.inspection_result is None
                or self.inspection_result.extraction_quality
                is not ExtractionQuality.COMPLETE
                or self.consumer_eligibility_decision is None
                or self.consumer_eligibility_decision.outcome
                is not ConsumerEligibilityOutcome.ELIGIBLE
            ):
                raise _invalid("ready_evidence")


@dataclass(frozen=True)
class LegalHoldEvidence:
    legal_hold_id: str
    quarantine_id: str
    authority_role: str
    retention_policy_id: str
    retention_policy_version: str
    scope: str
    reason_code: str
    evidence_references: tuple[str, ...]
    effective_at: datetime
    expires_at: datetime | None

    def __post_init__(self) -> None:
        for name in (
            "legal_hold_id",
            "quarantine_id",
            "authority_role",
            "retention_policy_id",
            "retention_policy_version",
            "scope",
            "reason_code",
        ):
            _require_non_empty(getattr(self, name), name)
        if self.authority_role != "Chief Architect":
            raise _invalid("authority_role")
        object.__setattr__(
            self,
            "evidence_references",
            _normalize_string_tuple(
                self.evidence_references,
                "evidence_references",
                required=True,
            ),
        )
        _require_aware(self.effective_at, "effective_at")
        _require_optional_aware(self.expires_at, "expires_at")
        if self.expires_at is not None and self.expires_at <= self.effective_at:
            raise _invalid("expires_at")


@dataclass(frozen=True)
class CleanupEvidence:
    cleanup_id: str
    quarantine_id: str
    retention_policy_id: str
    retention_policy_version: str
    deletion_policy_id: str
    deletion_policy_version: str
    admission_attempt_id: str
    outcome: CleanupOutcome
    scope: str
    actor_id: str
    component_id: str
    reason_code: str
    requested_at: datetime
    completed_at: datetime | None
    unresolved_obligation_reference: str | None

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {
                "outcome",
                "requested_at",
                "completed_at",
                "unresolved_obligation_reference",
            }:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        _require_instance(self.outcome, CleanupOutcome, "outcome")
        _require_aware(self.requested_at, "requested_at")
        _require_optional_aware(self.completed_at, "completed_at")
        if (
            self.completed_at is not None
            and self.completed_at < self.requested_at
        ):
            raise _invalid("completed_at")
        if self.unresolved_obligation_reference is not None:
            _require_non_empty(
                self.unresolved_obligation_reference,
                "unresolved_obligation_reference",
            )
        if (
            self.outcome is CleanupOutcome.FAILED
            and self.unresolved_obligation_reference is None
        ):
            raise _invalid("unresolved_obligation_reference")
        if (
            self.outcome is not CleanupOutcome.FAILED
            and self.completed_at is None
        ):
            raise _invalid("completed_at")


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    correlation_id: str
    subject_id: str
    admission_attempt_id: str | None
    transformation_attempt_id: str | None
    event_kind: str
    actor_id: str
    component_id: str
    reason_code: str
    policy_id: str
    policy_version: str
    recorded_at: datetime
    safe_evidence_references: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in fields(self):
            if field.name in {
                "admission_attempt_id",
                "transformation_attempt_id",
                "recorded_at",
                "safe_evidence_references",
            }:
                continue
            _require_non_empty(getattr(self, field.name), field.name)
        for name in (
            "admission_attempt_id",
            "transformation_attempt_id",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_non_empty(value, name)
        _require_aware(self.recorded_at, "recorded_at")
        object.__setattr__(
            self,
            "safe_evidence_references",
            _normalize_string_tuple(
                self.safe_evidence_references,
                "safe_evidence_references",
            ),
        )


class Phase3BState(str, Enum):
    STAGED = "staged"
    QUARANTINED = "quarantined"
    ACCEPTED = "accepted"
    READY_FOR_REVIEW = "ready_for_review"
    REVIEW_APPROVED = "review_approved"
    REVIEW_REJECTED = "review_rejected"
    REVIEW_CORRECTION_REQUESTED = "review_correction_requested"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    DELETED = "deleted"
    CLEANUP_FAILED = "cleanup_failed"


class ReviewDecision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    CORRECT = "correct"
    SUPERSEDE = "supersede"


def _require_base64(value: str, field_name: str) -> None:
    _require_non_empty(value, field_name)
    try:
        base64.b64decode(value.encode("ascii"), validate=True)
    except Exception as error:  # pragma: no cover - defensive
        raise _invalid(field_name) from error


@dataclass(frozen=True)
class SourceAuthorizationReceipt:
    receipt_id: str
    organization_id: str
    source_record_id: str
    authority_role: str
    principal_id: str
    purpose: str
    classification: str
    allowed_operation: str
    retention_profile_id: str
    environment: str
    issued_at: datetime
    expires_at: datetime
    signer_key_id: str
    expected_sha256: str | None = None
    single_use: bool = True

    def __post_init__(self) -> None:
        for name in (
            "receipt_id",
            "organization_id",
            "source_record_id",
            "authority_role",
            "principal_id",
            "purpose",
            "classification",
            "allowed_operation",
            "retention_profile_id",
            "environment",
            "signer_key_id",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_aware(self.issued_at, "issued_at")
        _require_aware(self.expires_at, "expires_at")
        if self.expires_at <= self.issued_at:
            raise _invalid("expires_at")
        if self.allowed_operation != "phase3b.synthetic.intake":
            raise _invalid("allowed_operation")
        if type(self.single_use) is not bool or self.single_use is not True:
            raise _invalid("single_use")
        if self.expected_sha256 is not None:
            _require_non_empty(self.expected_sha256, "expected_sha256")
            if (
                len(self.expected_sha256) != 64
                or self.expected_sha256 != self.expected_sha256.lower()
                or any(
                    character not in "0123456789abcdef"
                    for character in self.expected_sha256
                )
            ):
                raise _invalid("expected_sha256")


@dataclass(frozen=True)
class SignedSourceAuthorizationReceipt:
    receipt: SourceAuthorizationReceipt
    signature_b64: str

    def __post_init__(self) -> None:
        _require_instance(self.receipt, SourceAuthorizationReceipt, "receipt")
        _require_base64(self.signature_b64, "signature_b64")


@dataclass(frozen=True)
class Phase3BPageCapture:
    page_number: int
    method: str
    text: str
    warnings: tuple[str, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_positive(self.page_number, "page_number")
        if self.method not in {"native", "ocr"}:
            raise _invalid("method")
        _require_non_empty(self.text, "text")
        object.__setattr__(
            self,
            "warnings",
            _normalize_string_tuple(self.warnings, "warnings"),
        )
        object.__setattr__(
            self,
            "limitations",
            _normalize_string_tuple(self.limitations, "limitations"),
        )


@dataclass(frozen=True)
class Phase3BInspectionArtifact:
    artifact_id: str
    submission_id: str
    extraction_quality: ExtractionQuality
    pages: tuple[Phase3BPageCapture, ...]
    warnings: tuple[str, ...]
    omissions: tuple[str, ...]
    limitations: tuple[str, ...]
    native_text_sufficient: bool
    created_at: datetime

    def __post_init__(self) -> None:
        for name in ("artifact_id", "submission_id"):
            _require_non_empty(getattr(self, name), name)
        _require_instance(
            self.extraction_quality,
            ExtractionQuality,
            "extraction_quality",
        )
        pages = _normalize_tuple(self.pages, "pages", required=True)
        if not all(isinstance(page, Phase3BPageCapture) for page in pages):
            raise _invalid("pages")
        object.__setattr__(self, "pages", pages)
        for name in ("warnings", "omissions", "limitations"):
            object.__setattr__(
                self,
                name,
                _normalize_string_tuple(getattr(self, name), name),
            )
        if type(self.native_text_sufficient) is not bool:
            raise _invalid("native_text_sufficient")
        _require_aware(self.created_at, "created_at")


@dataclass(frozen=True)
class Phase3BAuditEntry:
    event_id: str
    submission_id: str
    event_kind: str
    prior_state: Phase3BState | None
    next_state: Phase3BState | None
    reason_code: str
    recorded_at: datetime

    def __post_init__(self) -> None:
        for name in ("event_id", "submission_id", "event_kind", "reason_code"):
            _require_non_empty(getattr(self, name), name)
        for name in ("prior_state", "next_state"):
            value = getattr(self, name)
            if value is not None:
                _require_instance(value, Phase3BState, name)
        _require_aware(self.recorded_at, "recorded_at")


@dataclass(frozen=True)
class Phase3BReviewAnnotation:
    annotation_id: str
    submission_id: str
    decision: ReviewDecision
    actor_id: str
    reason_code: str
    note: str
    created_at: datetime
    prior_annotation_id: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "annotation_id",
            "submission_id",
            "actor_id",
            "reason_code",
            "note",
        ):
            _require_non_empty(getattr(self, name), name)
        _require_instance(self.decision, ReviewDecision, "decision")
        _require_aware(self.created_at, "created_at")
        if self.prior_annotation_id is not None:
            _require_non_empty(self.prior_annotation_id, "prior_annotation_id")


@dataclass(frozen=True)
class Phase3BSubmissionRecord:
    submission_id: str
    receipt_id: str
    state: Phase3BState
    content_identity: ContentIdentity
    media_type: str
    byte_count: int
    duplicate_of: str | None
    created_at: datetime
    expires_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    latest_review_decision: ReviewDecision | None = None

    def __post_init__(self) -> None:
        for name in ("submission_id", "receipt_id", "media_type"):
            _require_non_empty(getattr(self, name), name)
        _require_instance(self.state, Phase3BState, "state")
        _require_instance(self.content_identity, ContentIdentity, "content_identity")
        _require_non_negative(self.byte_count, "byte_count")
        if self.duplicate_of is not None:
            _require_non_empty(self.duplicate_of, "duplicate_of")
        for name in ("created_at", "expires_at", "updated_at"):
            _require_aware(getattr(self, name), name)
        _require_optional_aware(self.deleted_at, "deleted_at")
        if self.expires_at <= self.created_at:
            raise _invalid("expires_at")
        if self.updated_at < self.created_at:
            raise _invalid("updated_at")
        if self.deleted_at is not None and self.deleted_at < self.created_at:
            raise _invalid("deleted_at")
        if self.latest_review_decision is not None:
            _require_instance(
                self.latest_review_decision,
                ReviewDecision,
                "latest_review_decision",
            )


@dataclass(frozen=True)
class Phase3BSubmissionDetail:
    record: Phase3BSubmissionRecord
    inspection_artifact: Phase3BInspectionArtifact | None
    review_annotations: tuple[Phase3BReviewAnnotation, ...]
    audit_entries: tuple[Phase3BAuditEntry, ...]

    def __post_init__(self) -> None:
        _require_instance(self.record, Phase3BSubmissionRecord, "record")
        if self.inspection_artifact is not None:
            _require_instance(
                self.inspection_artifact,
                Phase3BInspectionArtifact,
                "inspection_artifact",
            )
            if self.inspection_artifact.submission_id != self.record.submission_id:
                raise _invalid("inspection_artifact")
        annotations = _normalize_tuple(
            self.review_annotations,
            "review_annotations",
        )
        if not all(
            isinstance(annotation, Phase3BReviewAnnotation)
            for annotation in annotations
        ):
            raise _invalid("review_annotations")
        if any(
            annotation.submission_id != self.record.submission_id
            for annotation in annotations
        ):
            raise _invalid("review_annotations")
        object.__setattr__(self, "review_annotations", annotations)
        entries = _normalize_tuple(self.audit_entries, "audit_entries")
        if not all(isinstance(entry, Phase3BAuditEntry) for entry in entries):
            raise _invalid("audit_entries")
        if any(entry.submission_id != self.record.submission_id for entry in entries):
            raise _invalid("audit_entries")
        object.__setattr__(self, "audit_entries", entries)


@dataclass(frozen=True)
class Phase3BWorkspaceSnapshot:
    submissions: tuple[Phase3BSubmissionRecord, ...]
    recent_audit_entries: tuple[Phase3BAuditEntry, ...]
    warnings: tuple[str, ...]
    generated_at: datetime

    def __post_init__(self) -> None:
        submissions = _normalize_tuple(self.submissions, "submissions")
        if not all(
            isinstance(submission, Phase3BSubmissionRecord)
            for submission in submissions
        ):
            raise _invalid("submissions")
        object.__setattr__(self, "submissions", submissions)
        entries = _normalize_tuple(
            self.recent_audit_entries,
            "recent_audit_entries",
        )
        if not all(isinstance(entry, Phase3BAuditEntry) for entry in entries):
            raise _invalid("recent_audit_entries")
        object.__setattr__(self, "recent_audit_entries", entries)
        object.__setattr__(
            self,
            "warnings",
            _normalize_string_tuple(self.warnings, "warnings"),
        )
        _require_aware(self.generated_at, "generated_at")


@dataclass(frozen=True)
class Phase3BRecoveryReport:
    reconciled_submission_ids: tuple[str, ...]
    cleanup_failed_submission_ids: tuple[str, ...]
    expired_submission_ids: tuple[str, ...]
    recovered_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "reconciled_submission_ids",
            "cleanup_failed_submission_ids",
            "expired_submission_ids",
        ):
            object.__setattr__(
                self,
                name,
                _normalize_string_tuple(getattr(self, name), name),
            )
        _require_aware(self.recovered_at, "recovered_at")
