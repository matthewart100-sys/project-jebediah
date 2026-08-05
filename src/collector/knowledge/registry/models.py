from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeVar


_T = TypeVar("_T")


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")


def _require_aware(value: datetime, field_name: str) -> None:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ValueError(f"{field_name} must be timezone-aware")


def _require_optional_aware(
    value: datetime | None,
    field_name: str,
) -> None:
    if value is not None:
        _require_aware(value, field_name)


def _validate_unique_strings(
    values: tuple[str, ...],
    field_name: str,
    *,
    required: bool,
) -> None:
    if required and not values:
        raise ValueError(f"{field_name} cannot be empty")

    for value in values:
        _require_non_empty(value, field_name)

    if len(set(values)) != len(values):
        raise ValueError(f"{field_name} cannot contain duplicates")


def _normalize_collection(
    values: Iterable[_T],
    field_name: str,
) -> tuple[_T, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be a collection")

    try:
        return tuple(values)
    except TypeError as error:
        raise ValueError(
            f"{field_name} must be an iterable collection"
        ) from error


class FreshnessState(str, Enum):
    CURRENT = "current"
    AGING = "aging"
    STALE = "stale"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class UncertaintyState(str, Enum):
    BOUNDED = "bounded"
    INCOMPLETE = "incomplete"
    CONFLICTING = "conflicting"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class HumanReviewState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class KnowledgeLifecycleState(str, Enum):
    REGISTERED = "registered"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"
    INVALIDATED = "invalidated"


@dataclass(frozen=True)
class SourceReference:
    source_id: str
    authority_scope: str
    source_revision: str | None = None
    observed_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_non_empty(self.source_id, "source_id")
        _require_non_empty(self.authority_scope, "authority_scope")

        if self.source_revision is not None:
            _require_non_empty(self.source_revision, "source_revision")
        _require_optional_aware(self.observed_at, "observed_at")

        if self.source_revision is None and self.observed_at is None:
            raise ValueError(
                "source reference requires a revision or observation time"
            )


@dataclass(frozen=True)
class TransformationReference:
    transformation_id: str
    transformation_version: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.transformation_id,
            "transformation_id",
        )
        _require_non_empty(
            self.transformation_version,
            "transformation_version",
        )


@dataclass(frozen=True)
class EvidenceReference:
    evidence_id: str

    def __post_init__(self) -> None:
        _require_non_empty(self.evidence_id, "evidence_id")


@dataclass(frozen=True, init=False)
class KnowledgeProvenance:
    producer_id: str
    created_at: datetime
    source_references: tuple[SourceReference, ...]
    transformation: TransformationReference
    evidence_references: tuple[EvidenceReference, ...]

    def __init__(
        self,
        *,
        producer_id: str,
        created_at: datetime,
        source_references: Iterable[SourceReference],
        transformation: TransformationReference,
        evidence_references: Iterable[EvidenceReference],
    ) -> None:
        object.__setattr__(self, "producer_id", producer_id)
        object.__setattr__(self, "created_at", created_at)
        object.__setattr__(
            self,
            "source_references",
            _normalize_collection(
                source_references,
                "source_references",
            ),
        )
        object.__setattr__(self, "transformation", transformation)
        object.__setattr__(
            self,
            "evidence_references",
            _normalize_collection(
                evidence_references,
                "evidence_references",
            ),
        )
        self.__post_init__()

    def __post_init__(self) -> None:
        _require_non_empty(self.producer_id, "producer_id")
        _require_aware(self.created_at, "created_at")

        if not self.source_references:
            raise ValueError("source_references cannot be empty")
        if not all(
            isinstance(item, SourceReference)
            for item in self.source_references
        ):
            raise ValueError(
                "source_references must contain SourceReference values"
            )
        source_ids = tuple(
            item.source_id for item in self.source_references
        )
        if len(set(source_ids)) != len(source_ids):
            raise ValueError(
                "source_references cannot contain duplicate source_id values"
            )

        if not isinstance(
            self.transformation,
            TransformationReference,
        ):
            raise ValueError(
                "transformation must be a TransformationReference"
            )

        if not self.evidence_references:
            raise ValueError("evidence_references cannot be empty")
        if not all(
            isinstance(item, EvidenceReference)
            for item in self.evidence_references
        ):
            raise ValueError(
                "evidence_references must contain EvidenceReference values"
            )
        evidence_ids = tuple(
            item.evidence_id for item in self.evidence_references
        )
        if len(set(evidence_ids)) != len(evidence_ids):
            raise ValueError(
                "evidence_references cannot contain duplicate evidence_id values"
            )


@dataclass(frozen=True, init=False)
class GovernanceScope:
    information_owner_id: str
    information_domain: str
    classification: str
    permitted_consumer_ids: tuple[str, ...]
    permitted_uses: tuple[str, ...]
    retention_policy_id: str
    deletion_policy_id: str
    freshness_policy_id: str
    invalidation_policy_id: str

    def __init__(
        self,
        *,
        information_owner_id: str,
        information_domain: str,
        classification: str,
        permitted_consumer_ids: Iterable[str],
        permitted_uses: Iterable[str],
        retention_policy_id: str,
        deletion_policy_id: str,
        freshness_policy_id: str,
        invalidation_policy_id: str,
    ) -> None:
        object.__setattr__(
            self,
            "information_owner_id",
            information_owner_id,
        )
        object.__setattr__(
            self,
            "information_domain",
            information_domain,
        )
        object.__setattr__(self, "classification", classification)
        object.__setattr__(
            self,
            "permitted_consumer_ids",
            _normalize_collection(
                permitted_consumer_ids,
                "permitted_consumer_ids",
            ),
        )
        object.__setattr__(
            self,
            "permitted_uses",
            _normalize_collection(
                permitted_uses,
                "permitted_uses",
            ),
        )
        object.__setattr__(
            self,
            "retention_policy_id",
            retention_policy_id,
        )
        object.__setattr__(
            self,
            "deletion_policy_id",
            deletion_policy_id,
        )
        object.__setattr__(
            self,
            "freshness_policy_id",
            freshness_policy_id,
        )
        object.__setattr__(
            self,
            "invalidation_policy_id",
            invalidation_policy_id,
        )
        self.__post_init__()

    def __post_init__(self) -> None:
        _require_non_empty(
            self.information_owner_id,
            "information_owner_id",
        )
        _require_non_empty(
            self.information_domain,
            "information_domain",
        )
        _require_non_empty(self.classification, "classification")
        _validate_unique_strings(
            self.permitted_consumer_ids,
            "permitted_consumer_ids",
            required=True,
        )
        _validate_unique_strings(
            self.permitted_uses,
            "permitted_uses",
            required=True,
        )
        _require_non_empty(
            self.retention_policy_id,
            "retention_policy_id",
        )
        _require_non_empty(
            self.deletion_policy_id,
            "deletion_policy_id",
        )
        _require_non_empty(
            self.freshness_policy_id,
            "freshness_policy_id",
        )
        _require_non_empty(
            self.invalidation_policy_id,
            "invalidation_policy_id",
        )


@dataclass(frozen=True)
class TemporalContext:
    freshness_state: FreshnessState
    freshness_evaluated_at: datetime
    effective_at: datetime | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.freshness_state, FreshnessState):
            raise ValueError(
                "freshness_state must be a FreshnessState"
            )
        _require_aware(
            self.freshness_evaluated_at,
            "freshness_evaluated_at",
        )
        _require_optional_aware(self.effective_at, "effective_at")
        _require_optional_aware(self.expires_at, "expires_at")


@dataclass(frozen=True, init=False)
class UncertaintyAssessment:
    state: UncertaintyState
    explanation: str
    evidence_ids: tuple[str, ...]
    limitations: tuple[str, ...]

    def __init__(
        self,
        *,
        state: UncertaintyState,
        explanation: str,
        evidence_ids: Iterable[str] = (),
        limitations: Iterable[str] = (),
    ) -> None:
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "explanation", explanation)
        object.__setattr__(
            self,
            "evidence_ids",
            _normalize_collection(evidence_ids, "evidence_ids"),
        )
        object.__setattr__(
            self,
            "limitations",
            _normalize_collection(limitations, "limitations"),
        )
        self.__post_init__()

    def __post_init__(self) -> None:
        if not isinstance(self.state, UncertaintyState):
            raise ValueError("state must be an UncertaintyState")
        _require_non_empty(self.explanation, "explanation")
        _validate_unique_strings(
            self.evidence_ids,
            "evidence_ids",
            required=False,
        )
        _validate_unique_strings(
            self.limitations,
            "limitations",
            required=False,
        )

        if (
            self.state is UncertaintyState.BOUNDED
            and not self.evidence_ids
        ):
            raise ValueError(
                "bounded uncertainty requires supporting evidence"
            )
        if (
            self.state is UncertaintyState.INCOMPLETE
            and not self.limitations
        ):
            raise ValueError(
                "incomplete uncertainty requires a missing-evidence limitation"
            )
        if (
            self.state is UncertaintyState.CONFLICTING
            and len(self.evidence_ids) < 2
        ):
            raise ValueError(
                "conflicting uncertainty requires at least two evidence references"
            )
        if (
            self.state is UncertaintyState.UNKNOWN
            and not self.limitations
        ):
            raise ValueError(
                "unknown uncertainty requires an explanatory limitation"
            )
        if (
            self.state is UncertaintyState.NOT_APPLICABLE
            and (self.evidence_ids or self.limitations)
        ):
            raise ValueError(
                "not-applicable uncertainty cannot claim evidence or limitations"
            )


@dataclass(frozen=True)
class HumanReview:
    review_policy_id: str
    state: HumanReviewState
    reviewer_id: str | None = None
    decided_at: datetime | None = None
    rationale: str | None = None

    def __post_init__(self) -> None:
        _require_non_empty(
            self.review_policy_id,
            "review_policy_id",
        )
        if not isinstance(self.state, HumanReviewState):
            raise ValueError("state must be a HumanReviewState")

        if self.state is HumanReviewState.PENDING:
            if any(
                value is not None
                for value in (
                    self.reviewer_id,
                    self.decided_at,
                    self.rationale,
                )
            ):
                raise ValueError(
                    "pending review cannot contain decision evidence"
                )
            return

        if self.reviewer_id is None:
            raise ValueError("decided review requires reviewer_id")
        if self.decided_at is None:
            raise ValueError("decided review requires decided_at")
        if self.rationale is None:
            raise ValueError("decided review requires rationale")

        _require_non_empty(self.reviewer_id, "reviewer_id")
        _require_aware(self.decided_at, "decided_at")
        _require_non_empty(self.rationale, "rationale")


@dataclass(frozen=True)
class KnowledgeLifecycle:
    state: KnowledgeLifecycleState
    recorded_by: str
    recorded_at: datetime
    reason: str
    successor_object_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.state, KnowledgeLifecycleState):
            raise ValueError(
                "state must be a KnowledgeLifecycleState"
            )
        _require_non_empty(self.recorded_by, "recorded_by")
        _require_aware(self.recorded_at, "recorded_at")
        _require_non_empty(self.reason, "reason")

        if self.state is KnowledgeLifecycleState.SUPERSEDED:
            if self.successor_object_id is None:
                raise ValueError(
                    "superseded lifecycle requires successor_object_id"
                )
            _require_non_empty(
                self.successor_object_id,
                "successor_object_id",
            )
        elif self.successor_object_id is not None:
            raise ValueError(
                "only superseded lifecycle may identify a successor"
            )


@dataclass(frozen=True)
class KnowledgeRegistryRecord:
    object_id: str
    object_kind: str
    provenance: KnowledgeProvenance
    governance_scope: GovernanceScope
    temporal_context: TemporalContext
    uncertainty: UncertaintyAssessment
    human_review: HumanReview
    lifecycle: KnowledgeLifecycle

    def __post_init__(self) -> None:
        _require_non_empty(self.object_id, "object_id")
        _require_non_empty(self.object_kind, "object_kind")

        expected_types = (
            ("provenance", self.provenance, KnowledgeProvenance),
            ("governance_scope", self.governance_scope, GovernanceScope),
            ("temporal_context", self.temporal_context, TemporalContext),
            ("uncertainty", self.uncertainty, UncertaintyAssessment),
            ("human_review", self.human_review, HumanReview),
            ("lifecycle", self.lifecycle, KnowledgeLifecycle),
        )
        for field_name, value, expected_type in expected_types:
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"{field_name} must be a {expected_type.__name__}"
                )

        known_evidence = {
            reference.evidence_id
            for reference in self.provenance.evidence_references
        }
        if not set(self.uncertainty.evidence_ids).issubset(
            known_evidence
        ):
            raise ValueError(
                "uncertainty evidence must exist in provenance"
            )

        if (
            self.lifecycle.state
            is KnowledgeLifecycleState.SUPERSEDED
            and self.lifecycle.successor_object_id == self.object_id
        ):
            raise ValueError(
                "superseded lifecycle successor must differ from object_id"
            )
