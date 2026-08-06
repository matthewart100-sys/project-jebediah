"""Frozen view-model contracts, validation, and derived summaries.

Every record in this module is an immutable frozen dataclass with tuple
collections. Enumerations reject unknown values. Construction fails closed when
a contract, evidence, authority, freshness, uncertainty, lifecycle, identity, or
safety rule is violated. No record stores a truth probability, model confidence,
retrieval score, file path, external URL, source content, executable action, or
mutable approval.

This module knows nothing about HTTP, files, networks, or rendering.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# ---------------------------------------------------------------------------
# Closed vocabularies
# ---------------------------------------------------------------------------


class BriefingState(str, Enum):
    """One top-level state for an assembled briefing."""

    READY = "ready"
    LOADING = "loading"
    EMPTY = "empty"
    PARTIAL = "partial"
    STALE = "stale"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    HELD = "held"
    FAILED = "failed"
    UNAUTHORIZED = "unauthorized"
    UNAVAILABLE = "unavailable"
    DISCONNECTED = "disconnected"


class BriefingSection(str, Enum):
    """The four accepted executive sections."""

    HAPPENING = "happening"
    ATTENTION = "attention"
    KNOW = "know"
    NEXT = "next"


class EvidenceClassification(str, Enum):
    """Accepted evidence categories; never a numeric score."""

    VERIFIED_FACT = "verified_fact"
    REPORTED_FACT = "reported_fact"
    WORKING_ASSUMPTION = "working_assumption"
    OPEN_QUESTION = "open_question"
    DERIVED_SUMMARY = "derived_summary"


class FreshnessState(str, Enum):
    """Qualitative freshness derived from the fixed briefing clock."""

    CURRENT = "current"
    AGING = "aging"
    STALE = "stale"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class UncertaintyState(str, Enum):
    """Qualitative uncertainty; never a truth probability."""

    BOUNDED = "bounded"
    INCOMPLETE = "incomplete"
    CONFLICTING = "conflicting"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class LifecycleState(str, Enum):
    """Record lifecycle state."""

    ACTIVE = "active"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class KnowledgeKind(str, Enum):
    """Knowledge classification required only for ``know`` items."""

    MATERIAL_CHANGE = "material_change"
    DECISION = "decision"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    KNOWLEDGE_GAP = "knowledge_gap"


class NextItemKind(str, Enum):
    """Accepted next-step kind required only for ``next`` items."""

    DECISION_REQUIRED = "decision_required"
    ORGANIZATIONAL_GATE = "organizational_gate"
    ACTION_CANDIDATE = "action_candidate"
    INFORMATIONAL_ATTENTION = "informational_attention"


class NextContext(str, Enum):
    """Accepted next-step context required only for ``next`` items."""

    APPROVED_PLAN = "approved_plan"
    UNRESOLVED_GATE = "unresolved_gate"
    DECISION_REQUEST = "decision_request"
    POSSIBLE_ACTION_CANDIDATE = "possible_action_candidate"
    INFORMATION_GATHERING_NEED = "information_gathering_need"


class PermittedNextStep(str, Enum):
    """The only permitted interaction outcomes."""

    NAVIGATE = "navigate"
    HUMAN_REVIEW = "human_review"


class AskState(str, Enum):
    """Preset synthetic Ask response state."""

    GROUNDED = "grounded"
    INSUFFICIENT = "insufficient"
    FAILED = "failed"


class WorkspaceKind(str, Enum):
    """Synthetic workspace record kind."""

    SOURCE_RECORD = "source_record"
    DOCUMENT = "document"
    QUARANTINE = "quarantine"
    REVIEW = "review"
    LINEAGE = "lineage"
    KNOWLEDGE_OBJECT = "knowledge_object"


class WorkspaceState(str, Enum):
    """Synthetic workspace metadata state."""

    RECEIVED = "received"
    QUARANTINED = "quarantined"
    VALIDATING = "validating"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    HELD = "held"
    EVALUATION_FAILED = "evaluation_failed"
    PROCESSING = "processing"
    READY = "ready"
    PROCESSING_FAILED = "processing_failed"
    REVIEW_PENDING = "review_pending"
    REVIEW_APPROVED = "review_approved"
    REVIEW_REJECTED = "review_rejected"
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    UNAUTHORIZED = "unauthorized"
    UNAVAILABLE = "unavailable"
    DELETED = "deleted"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class ActivityKind(str, Enum):
    """Synthetic activity metadata kind."""

    EVIDENCE_ADDED = "evidence_added"
    REVIEW_STATE_CHANGED = "review_state_changed"
    LINEAGE_RECORDED = "lineage_recorded"
    KNOWLEDGE_STATUS_CHANGED = "knowledge_status_changed"


class WorkspaceMode(str, Enum):
    """Operational workspace profile mode."""

    DEMONSTRATION = "demonstration"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class WorkspaceBannerTone(str, Enum):
    """Visual banner tone for persistent workspace labeling."""

    BLUE = "blue"
    ORANGE = "orange"
    GREEN = "green"


# ---------------------------------------------------------------------------
# Permitted relationships and matrices
# ---------------------------------------------------------------------------

PERMITTED_NEXT_CONTEXT_TO_KIND: dict[NextContext, NextItemKind] = {
    NextContext.APPROVED_PLAN: NextItemKind.INFORMATIONAL_ATTENTION,
    NextContext.UNRESOLVED_GATE: NextItemKind.ORGANIZATIONAL_GATE,
    NextContext.DECISION_REQUEST: NextItemKind.DECISION_REQUIRED,
    NextContext.POSSIBLE_ACTION_CANDIDATE: NextItemKind.ACTION_CANDIDATE,
    NextContext.INFORMATION_GATHERING_NEED: NextItemKind.INFORMATIONAL_ATTENTION,
}

WORKSPACE_KIND_STATES: dict[WorkspaceKind, frozenset[WorkspaceState]] = {
    WorkspaceKind.SOURCE_RECORD: frozenset(
        {
            WorkspaceState.ELIGIBLE,
            WorkspaceState.INELIGIBLE,
            WorkspaceState.HELD,
            WorkspaceState.UNAUTHORIZED,
            WorkspaceState.UNAVAILABLE,
            WorkspaceState.DELETED,
            WorkspaceState.SUPERSEDED,
            WorkspaceState.ARCHIVED,
        }
    ),
    WorkspaceKind.DOCUMENT: frozenset(
        {
            WorkspaceState.RECEIVED,
            WorkspaceState.QUARANTINED,
            WorkspaceState.VALIDATING,
            WorkspaceState.ACCEPTED,
            WorkspaceState.REJECTED,
            WorkspaceState.HELD,
            WorkspaceState.EVALUATION_FAILED,
            WorkspaceState.DELETED,
        }
    ),
    WorkspaceKind.QUARANTINE: frozenset(
        {
            WorkspaceState.QUARANTINED,
            WorkspaceState.VALIDATING,
            WorkspaceState.ACCEPTED,
            WorkspaceState.REJECTED,
            WorkspaceState.HELD,
            WorkspaceState.EVALUATION_FAILED,
            WorkspaceState.DELETED,
        }
    ),
    WorkspaceKind.REVIEW: frozenset(
        {
            WorkspaceState.REVIEW_PENDING,
            WorkspaceState.REVIEW_APPROVED,
            WorkspaceState.REVIEW_REJECTED,
            WorkspaceState.HELD,
            WorkspaceState.UNAVAILABLE,
            WorkspaceState.ARCHIVED,
        }
    ),
    WorkspaceKind.LINEAGE: frozenset(
        {
            WorkspaceState.PROCESSING,
            WorkspaceState.READY,
            WorkspaceState.PROCESSING_FAILED,
            WorkspaceState.UNAVAILABLE,
            WorkspaceState.DELETED,
            WorkspaceState.SUPERSEDED,
            WorkspaceState.ARCHIVED,
        }
    ),
    WorkspaceKind.KNOWLEDGE_OBJECT: frozenset(
        {
            WorkspaceState.PROCESSING,
            WorkspaceState.READY,
            WorkspaceState.PROCESSING_FAILED,
            WorkspaceState.REVIEW_PENDING,
            WorkspaceState.REVIEW_APPROVED,
            WorkspaceState.REVIEW_REJECTED,
            WorkspaceState.ELIGIBLE,
            WorkspaceState.INELIGIBLE,
            WorkspaceState.HELD,
            WorkspaceState.UNAUTHORIZED,
            WorkspaceState.UNAVAILABLE,
            WorkspaceState.DELETED,
            WorkspaceState.SUPERSEDED,
            WorkspaceState.ARCHIVED,
        }
    ),
}

_BRIEFING_ELIGIBLE_PAIRS: frozenset[tuple[WorkspaceKind, WorkspaceState]] = frozenset(
    {
        (WorkspaceKind.SOURCE_RECORD, WorkspaceState.ELIGIBLE),
        (WorkspaceKind.KNOWLEDGE_OBJECT, WorkspaceState.ELIGIBLE),
    }
)

ALLOWLISTED_ASK_QUESTION_IDS: frozenset[str] = frozenset(
    {
        "grounded-priorities",
        "insufficient-program-outcomes",
        "failed-source-review",
    }
)

# The single accepted synthetic scenario identity. This constant is the sole
# source of truth; the fixture module reuses it rather than redefining it, so a
# briefing can never claim an unlisted scenario.
ALLOWLISTED_SCENARIO_ID = "synthetic-nonprofit-demo-v1"
ALLOWLISTED_SCENARIO_IDS: frozenset[str] = frozenset({ALLOWLISTED_SCENARIO_ID})

_EVIDENCE_REQUIRING_REFERENCES: frozenset[EvidenceClassification] = frozenset(
    {
        EvidenceClassification.VERIFIED_FACT,
        EvidenceClassification.REPORTED_FACT,
        EvidenceClassification.DERIVED_SUMMARY,
    }
)

_FRESHNESS_CURRENT_DAYS = 7
_FRESHNESS_AGING_DAYS = 30
_UPCOMING_DEADLINE_DAYS = 30
_RECENT_EVIDENCE_DAYS = 30

_INELIGIBLE_LIFECYCLES: frozenset[LifecycleState] = frozenset(
    {LifecycleState.SUPERSEDED, LifecycleState.ARCHIVED}
)


# ---------------------------------------------------------------------------
# Safety guards
# ---------------------------------------------------------------------------

_IDENTITY_PATTERN = re.compile(r"^demo-[a-z0-9-]+$")
_URL_SCHEME_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+.-]*://")
_SELF_ACTION_PATTERN = re.compile(
    r"(?i)\b(jebediah|the system|the shell|the tool)\b[^.]*\b"
    r"(approved|executed|sent|submitted|decided|commanded|"
    r"changed|completed|deployed|deleted|mutated|applied)\b"
)
_SCORE_TOKEN_PATTERN = re.compile(r"(?i)\b(confidence|probability|likelihood|score)\b")


class ContractError(ValueError):
    """Raised when a view-model contract is violated."""


def _reject_unsafe_text(value: str, field_name: str) -> None:
    """Reject URLs, paths, markup, control characters, and action claims."""
    if "\x00" in value:
        raise ContractError(f"{field_name} must not contain a null byte")
    if any(ord(character) < 32 for character in value):
        raise ContractError(f"{field_name} must not contain control characters")
    if "<" in value or ">" in value:
        raise ContractError(f"{field_name} must not contain raw HTML markup")
    if "\\" in value:
        raise ContractError(f"{field_name} must not contain a backslash path")
    if ".." in value:
        raise ContractError(f"{field_name} must not contain a traversal sequence")
    if "//" in value or _URL_SCHEME_PATTERN.search(value):
        raise ContractError(f"{field_name} must not contain a URL or locator")
    if "www." in value.lower():
        raise ContractError(f"{field_name} must not contain a web locator")
    if _SELF_ACTION_PATTERN.search(value):
        raise ContractError(
            f"{field_name} must not claim the system took an organizational action"
        )


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field_name} must be non-empty text")
    _reject_unsafe_text(value, field_name)
    return value


def _reject_score_language(value: str, field_name: str) -> None:
    if "%" in value:
        raise ContractError(f"{field_name} must not express a percentage")
    if _SCORE_TOKEN_PATTERN.search(value):
        raise ContractError(f"{field_name} must not express a numeric score")


def _require_identity(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not _IDENTITY_PATTERN.match(value):
        raise ContractError(
            f"{field_name} must be a synthetic 'demo-' identity, got {value!r}"
        )
    return value


def _require_aware(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise ContractError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ContractError(f"{field_name} must be timezone-aware")
    return value


def _require_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ContractError(f"{field_name} must be a tuple")
    if not values:
        raise ContractError(f"{field_name} must be non-empty")
    for entry in values:
        _require_text(entry, f"{field_name} entry")
    return values


def _require_sorted_unique(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ContractError(f"{field_name} must be a tuple")
    for entry in values:
        _require_text(entry, f"{field_name} entry")
    if list(values) != sorted(values):
        raise ContractError(f"{field_name} must be sorted")
    if len(set(values)) != len(values):
        raise ContractError(f"{field_name} must be unique")
    return values


# ---------------------------------------------------------------------------
# Supporting records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrganizationProfile:
    """Configured organization metadata for workspace context."""

    organization_id: str
    name: str
    description: str
    theme: str
    logo: str
    knowledge_root: str
    runtime_root: str
    governance_policy: str

    def __post_init__(self) -> None:
        _require_text(self.organization_id, "organization_id")
        _require_text(self.name, "organization_name")
        _require_text(self.description, "organization_description")
        _require_text(self.theme, "organization_theme")
        _require_text(self.logo, "organization_logo")
        _require_text(self.knowledge_root, "organization_knowledge_root")
        _require_text(self.runtime_root, "organization_runtime_root")
        _require_text(self.governance_policy, "organization_governance_policy")


@dataclass(frozen=True)
class WorkspaceContext:
    """Operational workspace and organization selection context."""

    mode: WorkspaceMode
    banner_label: str
    banner_tone: WorkspaceBannerTone
    runtime_name: str
    model_name: str
    profile: OrganizationProfile
    recent_organization_ids: tuple[str, ...]
    available_organization_ids: tuple[str, ...]
    available_workspace_modes: tuple[str, ...]
    diagnostics_enabled: bool
    demo_reset_available: bool
    csrf_token: str = ""
    auth_required: bool = False
    authenticated: bool = False
    authenticated_user_display: str = "anonymous"
    authenticated_user_role: str = "viewer"
    active_session_count: int = 0
    locked_account_count: int = 0

    @staticmethod
    def demonstration_default() -> "WorkspaceContext":
        return WorkspaceContext(
            mode=WorkspaceMode.DEMONSTRATION,
            banner_label="Demonstration Mode",
            banner_tone=WorkspaceBannerTone.BLUE,
            runtime_name="Synthetic demonstration runtime",
            model_name="none",
            profile=OrganizationProfile(
                organization_id="demo-organization",
                name="Demo Organization",
                description="Synthetic organization for demonstrations and training.",
                theme="Executive demonstration",
                logo="DEMO",
                knowledge_root="synthetic demo knowledge root",
                runtime_root="synthetic demo runtime root",
                governance_policy="Synthetic demo governance policy",
            ),
            recent_organization_ids=("demo-organization",),
            available_organization_ids=("demo-organization",),
            available_workspace_modes=(
                WorkspaceMode.DEMONSTRATION.value,
                WorkspaceMode.DEVELOPMENT.value,
                WorkspaceMode.PRODUCTION.value,
            ),
            diagnostics_enabled=False,
            demo_reset_available=True,
            csrf_token="",
            auth_required=False,
            authenticated=False,
            authenticated_user_display="anonymous",
            authenticated_user_role="viewer",
            active_session_count=0,
            locked_account_count=0,
        )

    def __post_init__(self) -> None:
        if not isinstance(self.mode, WorkspaceMode):
            raise ContractError("workspace mode must be a WorkspaceMode")
        _require_text(self.banner_label, "workspace_banner_label")
        if not isinstance(self.banner_tone, WorkspaceBannerTone):
            raise ContractError("workspace banner tone must be a WorkspaceBannerTone")
        _require_text(self.runtime_name, "workspace_runtime_name")
        _require_text(self.model_name, "workspace_model_name")
        if not isinstance(self.profile, OrganizationProfile):
            raise ContractError("workspace profile must be an OrganizationProfile")
        _require_text_tuple(
            self.recent_organization_ids, "workspace recent organization ids"
        )
        _require_text_tuple(
            self.available_organization_ids, "workspace available organization ids"
        )
        _require_text_tuple(
            self.available_workspace_modes, "workspace available mode ids"
        )
        if self.mode.value not in self.available_workspace_modes:
            raise ContractError("workspace mode must exist in available workspace modes")
        if self.profile.organization_id not in self.available_organization_ids:
            raise ContractError(
                "workspace profile organization_id must exist in available organizations"
            )
        if not isinstance(self.diagnostics_enabled, bool):
            raise ContractError("workspace diagnostics_enabled must be a bool")
        if not isinstance(self.demo_reset_available, bool):
            raise ContractError("workspace demo_reset_available must be a bool")
        if not isinstance(self.csrf_token, str):
            raise ContractError("workspace csrf_token must be text")
        if not isinstance(self.auth_required, bool):
            raise ContractError("workspace auth_required must be a bool")
        if not isinstance(self.authenticated, bool):
            raise ContractError("workspace authenticated must be a bool")
        _require_text(self.authenticated_user_display, "workspace user display")
        _require_text(self.authenticated_user_role, "workspace user role")
        if (
            not isinstance(self.active_session_count, int)
            or isinstance(self.active_session_count, bool)
            or self.active_session_count < 0
        ):
            raise ContractError("workspace active_session_count must be non-negative int")
        if (
            not isinstance(self.locked_account_count, int)
            or isinstance(self.locked_account_count, bool)
            or self.locked_account_count < 0
        ):
            raise ContractError("workspace locked_account_count must be non-negative int")


@dataclass(frozen=True)
class SourceReference:
    """A safe synthetic evidence reference; never a real locator."""

    source_id: str
    label: str
    evidence_classification: EvidenceClassification
    authority_scope: str
    observed_at: datetime | None = None

    def __post_init__(self) -> None:
        _require_identity(self.source_id, "source_id")
        _require_text(self.label, "label")
        if not isinstance(self.evidence_classification, EvidenceClassification):
            raise ContractError("evidence_classification must be an EvidenceClassification")
        _require_text(self.authority_scope, "authority_scope")
        _require_aware(self.observed_at, "observed_at")


@dataclass(frozen=True)
class CoverageSummary:
    """Bounded synthetic coverage of the fabricated scenario."""

    scope_statement: str
    covered_subjects: tuple[str, ...]
    missing_subjects: tuple[str, ...]
    conflicting_subjects: tuple[str, ...]
    stale_subjects: tuple[str, ...]
    held_subjects: tuple[str, ...]
    eligible_item_count: int
    source_reference_count: int
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.scope_statement, "scope_statement")
        _require_sorted_unique(self.covered_subjects, "covered_subjects")
        _require_sorted_unique(self.missing_subjects, "missing_subjects")
        _require_sorted_unique(self.conflicting_subjects, "conflicting_subjects")
        _require_sorted_unique(self.stale_subjects, "stale_subjects")
        _require_sorted_unique(self.held_subjects, "held_subjects")
        for _count_name in ("eligible_item_count", "source_reference_count"):
            _count = getattr(self, _count_name)
            if not isinstance(_count, int) or isinstance(_count, bool) or _count < 0:
                raise ContractError(f"{_count_name} must be a non-negative integer")
        _require_text_tuple(self.limitations, "coverage limitations")


@dataclass(frozen=True)
class WorkspaceRecord:
    """Synthetic workspace metadata; never source content."""

    record_id: str
    kind: WorkspaceKind
    title: str
    state: WorkspaceState
    source_references: tuple[SourceReference, ...]
    last_changed_at: datetime
    eligible_for_briefing: bool
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identity(self.record_id, "record_id")
        if not isinstance(self.kind, WorkspaceKind):
            raise ContractError("kind must be a WorkspaceKind")
        _require_text(self.title, "title")
        if not isinstance(self.state, WorkspaceState):
            raise ContractError("state must be a WorkspaceState")
        if self.state not in WORKSPACE_KIND_STATES[self.kind]:
            raise ContractError(
                f"state {self.state.value} is not permitted for kind {self.kind.value}"
            )
        if not isinstance(self.source_references, tuple):
            raise ContractError("source_references must be a tuple")
        for reference in self.source_references:
            if not isinstance(reference, SourceReference):
                raise ContractError("source_references must contain SourceReference")
        _require_aware(self.last_changed_at, "last_changed_at")
        if self.last_changed_at is None:
            raise ContractError("last_changed_at is required")
        if not isinstance(self.eligible_for_briefing, bool):
            raise ContractError("eligible_for_briefing must be a bool")
        expected = (self.kind, self.state) in _BRIEFING_ELIGIBLE_PAIRS
        if self.eligible_for_briefing != expected:
            raise ContractError(
                "eligible_for_briefing may be true only for an eligible "
                "source_record or knowledge_object"
            )
        _require_text_tuple(self.limitations, "workspace limitations")


@dataclass(frozen=True)
class ActivityEntry:
    """Synthetic activity metadata event."""

    activity_id: str
    kind: ActivityKind
    summary: str
    occurred_at: datetime
    actor_label: str
    source_references: tuple[SourceReference, ...]
    result_state: WorkspaceState

    def __post_init__(self) -> None:
        _require_identity(self.activity_id, "activity_id")
        if not isinstance(self.kind, ActivityKind):
            raise ContractError("kind must be an ActivityKind")
        _require_text(self.summary, "summary")
        _require_aware(self.occurred_at, "occurred_at")
        if self.occurred_at is None:
            raise ContractError("occurred_at is required")
        _require_text(self.actor_label, "actor_label")
        if not isinstance(self.source_references, tuple):
            raise ContractError("source_references must be a tuple")
        for reference in self.source_references:
            if not isinstance(reference, SourceReference):
                raise ContractError("source_references must contain SourceReference")
        if not isinstance(self.result_state, WorkspaceState):
            raise ContractError("result_state must be a WorkspaceState")


@dataclass(frozen=True)
class AskResponse:
    """A preset synthetic Ask response; never a model answer."""

    question_id: str
    question: str
    state: AskState
    coverage_statement: str
    uncertainty: UncertaintyState
    uncertainty_explanation: str
    limitations: tuple[str, ...]
    statement: str | None = None
    source_references: tuple[SourceReference, ...] = ()

    def __post_init__(self) -> None:
        if self.question_id not in ALLOWLISTED_ASK_QUESTION_IDS:
            raise ContractError(
                f"question_id must be an allowlisted preset, got {self.question_id!r}"
            )
        _require_text(self.question, "question")
        if not isinstance(self.state, AskState):
            raise ContractError("state must be an AskState")
        _require_text(self.coverage_statement, "coverage_statement")
        if not isinstance(self.uncertainty, UncertaintyState):
            raise ContractError("uncertainty must be an UncertaintyState")
        _require_text(self.uncertainty_explanation, "uncertainty_explanation")
        _reject_score_language(self.uncertainty_explanation, "uncertainty_explanation")
        _require_text_tuple(self.limitations, "ask limitations")
        if not isinstance(self.source_references, tuple):
            raise ContractError("source_references must be a tuple")
        for reference in self.source_references:
            if not isinstance(reference, SourceReference):
                raise ContractError("source_references must contain SourceReference")

        if self.state is AskState.GROUNDED:
            if not self.statement or not self.statement.strip():
                raise ContractError("grounded responses require a statement")
            _require_text(self.statement, "statement")
            if not self.source_references:
                raise ContractError("grounded responses require evidence references")
        else:
            if self.statement is not None:
                raise ContractError(
                    "insufficient or failed responses must not fabricate an answer"
                )
            if self.state is AskState.FAILED and self.source_references:
                raise ContractError("failed responses must not present evidence")


@dataclass(frozen=True)
class BriefingItem:
    """One evidence-bearing executive briefing item."""

    item_id: str
    section: BriefingSection
    display_order: int
    title: str
    statement: str
    evidence_classification: EvidenceClassification
    assembled_at: datetime
    freshness: FreshnessState
    evidence_basis: str
    uncertainty: UncertaintyState
    uncertainty_explanation: str
    limitations: tuple[str, ...]
    source_references: tuple[SourceReference, ...] = ()
    source_observed_at: datetime | None = None
    priority_basis: str | None = None
    review_due_at: datetime | None = None
    lifecycle: LifecycleState = LifecycleState.ACTIVE
    transformation_id: str | None = None
    knowledge_kind: KnowledgeKind | None = None
    next_kind: NextItemKind | None = None
    next_context: NextContext | None = None
    decision_owner: str | None = None
    authority_requirement: str | None = None
    permitted_next_step: PermittedNextStep | None = None
    related_item_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_identity(self.item_id, "item_id")
        if not isinstance(self.section, BriefingSection):
            raise ContractError("section must be a BriefingSection")
        if (
            not isinstance(self.display_order, int)
            or isinstance(self.display_order, bool)
            or self.display_order <= 0
        ):
            raise ContractError("display_order must be a positive integer")
        _require_text(self.title, "title")
        _require_text(self.statement, "statement")
        if not isinstance(self.evidence_classification, EvidenceClassification):
            raise ContractError("evidence_classification must be an EvidenceClassification")
        _require_aware(self.assembled_at, "assembled_at")
        if self.assembled_at is None:
            raise ContractError("assembled_at is required")
        if not isinstance(self.freshness, FreshnessState):
            raise ContractError("freshness must be a FreshnessState")
        _require_text(self.evidence_basis, "evidence_basis")
        _reject_score_language(self.evidence_basis, "evidence_basis")
        if not isinstance(self.uncertainty, UncertaintyState):
            raise ContractError("uncertainty must be an UncertaintyState")
        _require_text(self.uncertainty_explanation, "uncertainty_explanation")
        _reject_score_language(self.uncertainty_explanation, "uncertainty_explanation")
        _require_text_tuple(self.limitations, "item limitations")

        if not isinstance(self.source_references, tuple):
            raise ContractError("source_references must be a tuple")
        for reference in self.source_references:
            if not isinstance(reference, SourceReference):
                raise ContractError("source_references must contain SourceReference")
        _require_aware(self.source_observed_at, "source_observed_at")
        _require_aware(self.review_due_at, "review_due_at")
        if self.freshness is FreshnessState.NOT_APPLICABLE:
            if self.source_observed_at is not None:
                raise ContractError(
                    "not_applicable freshness requires missing source_observed_at"
                )
        else:
            derived_freshness = derive_freshness(
                self.source_observed_at,
                self.assembled_at,
            )
            if self.freshness is not derived_freshness:
                raise ContractError(
                    "freshness must match source_observed_at and assembled_at"
                )

        if self.evidence_classification in _EVIDENCE_REQUIRING_REFERENCES:
            if not self.source_references:
                raise ContractError(
                    "evidence claims require one or more safe source references"
                )
        if not isinstance(self.lifecycle, LifecycleState):
            raise ContractError("lifecycle must be a LifecycleState")

        if self.evidence_classification is EvidenceClassification.DERIVED_SUMMARY:
            if self.transformation_id is None:
                raise ContractError("derived summaries require a transformation_id")
            _require_identity(self.transformation_id, "transformation_id")
        elif self.transformation_id is not None:
            raise ContractError(
                "transformation_id is only permitted for derived summaries"
            )

        self._validate_section_fields()
        self._validate_relationships()

    def _validate_section_fields(self) -> None:
        is_attention = self.section is BriefingSection.ATTENTION
        is_next = self.section is BriefingSection.NEXT

        if self.section is BriefingSection.KNOW:
            if not isinstance(self.knowledge_kind, KnowledgeKind):
                raise ContractError("know items require a knowledge_kind")
        elif self.knowledge_kind is not None:
            raise ContractError("knowledge_kind is only permitted for know items")

        if is_next:
            if not isinstance(self.next_kind, NextItemKind):
                raise ContractError("next items require a next_kind")
            if not isinstance(self.next_context, NextContext):
                raise ContractError("next items require a next_context")
            if PERMITTED_NEXT_CONTEXT_TO_KIND[self.next_context] is not self.next_kind:
                raise ContractError(
                    "next_context and next_kind must be a permitted pair"
                )
        else:
            if self.next_kind is not None:
                raise ContractError("next_kind is only permitted for next items")
            if self.next_context is not None:
                raise ContractError("next_context is only permitted for next items")

        if is_attention or is_next:
            if self.priority_basis is None:
                raise ContractError(
                    "priority_basis is required for attention and next items"
                )
            _require_text(self.priority_basis, "priority_basis")
            if self.authority_requirement is None:
                raise ContractError(
                    "authority_requirement is required for attention and next items"
                )
            _require_text(self.authority_requirement, "authority_requirement")
            if not isinstance(self.permitted_next_step, PermittedNextStep):
                raise ContractError(
                    "permitted_next_step is required for attention and next items"
                )
        else:
            if self.priority_basis is not None:
                raise ContractError(
                    "priority_basis is only permitted for attention and next items"
                )
            if self.permitted_next_step is not None:
                raise ContractError(
                    "permitted_next_step is only permitted for attention and next items"
                )

        if self.decision_owner is not None:
            _require_text(self.decision_owner, "decision_owner")

    def _validate_relationships(self) -> None:
        if not isinstance(self.related_item_ids, tuple):
            raise ContractError("related_item_ids must be a tuple")
        for related in self.related_item_ids:
            _require_identity(related, "related_item_id")
        if self.item_id in self.related_item_ids:
            raise ContractError("related_item_ids must not reference the item itself")
        if len(set(self.related_item_ids)) != len(self.related_item_ids):
            raise ContractError("related_item_ids must not contain duplicates")

    @property
    def is_ordinary(self) -> bool:
        """Whether the item is an active, ordinarily eligible item."""
        return self.lifecycle is LifecycleState.ACTIVE


@dataclass(frozen=True)
class SummaryCounts:
    """Derived overview counts; never fixture-entered."""

    priority_count: int
    unresolved_decision_count: int
    organizational_gate_count: int
    upcoming_deadline_count: int
    recent_evidence_update_count: int
    eligible_source_count: int

    def __post_init__(self) -> None:
        for name in (
            "priority_count",
            "unresolved_decision_count",
            "organizational_gate_count",
            "upcoming_deadline_count",
            "recent_evidence_update_count",
            "eligible_source_count",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ContractError(f"{name} must be a non-negative integer")


def derive_freshness(
    source_observed_at: datetime | None,
    assembled_at: datetime,
    *,
    applicable: bool = True,
) -> FreshnessState:
    """Derive freshness from the fixed briefing clock, not wall time."""
    if assembled_at is None:
        raise ContractError("assembled_at is required to derive freshness")
    _require_aware(assembled_at, "assembled_at")
    if not applicable:
        return FreshnessState.NOT_APPLICABLE
    if source_observed_at is None:
        return FreshnessState.UNKNOWN
    _require_aware(source_observed_at, "source_observed_at")
    age = assembled_at - source_observed_at
    if age < timedelta(0):
        return FreshnessState.UNKNOWN
    if age <= timedelta(days=_FRESHNESS_CURRENT_DAYS):
        return FreshnessState.CURRENT
    if age <= timedelta(days=_FRESHNESS_AGING_DAYS):
        return FreshnessState.AGING
    return FreshnessState.STALE


def unique_source_references(
    items: tuple[BriefingItem, ...],
) -> tuple[SourceReference, ...]:
    """Return references from active ordinary items, unique by identity."""
    seen: dict[str, SourceReference] = {}
    for item in items:
        if not item.is_ordinary:
            continue
        for reference in item.source_references:
            seen.setdefault(reference.source_id, reference)
    return tuple(seen[key] for key in sorted(seen))


def derive_summary_counts(
    items: tuple[BriefingItem, ...],
    activities: tuple[ActivityEntry, ...],
    assembled_at: datetime,
) -> SummaryCounts:
    """Compute overview counts from ordinary items and activities."""
    ordinary = tuple(item for item in items if item.is_ordinary)

    priority_count = sum(
        1 for item in ordinary if item.section is BriefingSection.ATTENTION
    )
    unresolved_decision_count = sum(
        1
        for item in ordinary
        if item.section is BriefingSection.NEXT
        and item.next_kind is NextItemKind.DECISION_REQUIRED
    )
    organizational_gate_count = sum(
        1
        for item in ordinary
        if item.section is BriefingSection.NEXT
        and item.next_kind is NextItemKind.ORGANIZATIONAL_GATE
    )

    deadline_window_end = assembled_at + timedelta(days=_UPCOMING_DEADLINE_DAYS)
    upcoming_deadline_count = sum(
        1
        for item in ordinary
        if item.section in (BriefingSection.ATTENTION, BriefingSection.NEXT)
        and item.review_due_at is not None
        and assembled_at <= item.review_due_at <= deadline_window_end
    )

    evidence_window_start = assembled_at - timedelta(days=_RECENT_EVIDENCE_DAYS)
    recent_evidence_update_count = sum(
        1
        for activity in activities
        if activity.kind is ActivityKind.EVIDENCE_ADDED
        and evidence_window_start <= activity.occurred_at <= assembled_at
    )

    eligible_source_count = len(unique_source_references(items))

    return SummaryCounts(
        priority_count=priority_count,
        unresolved_decision_count=unresolved_decision_count,
        organizational_gate_count=organizational_gate_count,
        upcoming_deadline_count=upcoming_deadline_count,
        recent_evidence_update_count=recent_evidence_update_count,
        eligible_source_count=eligible_source_count,
    )


@dataclass(frozen=True)
class ExecutiveBriefing:
    """One immutable synthetic executive briefing."""

    briefing_id: str
    scenario_id: str
    scenario_label: str
    state: BriefingState
    assembled_at: datetime
    coverage: CoverageSummary
    items: tuple[BriefingItem, ...]
    workspace_records: tuple[WorkspaceRecord, ...]
    activities: tuple[ActivityEntry, ...]
    ask_responses: tuple[AskResponse, ...]
    summary_counts: SummaryCounts
    limitations: tuple[str, ...]
    workspace_context: WorkspaceContext = field(
        default_factory=WorkspaceContext.demonstration_default
    )

    def __post_init__(self) -> None:
        _require_identity(self.briefing_id, "briefing_id")
        _require_text(self.scenario_id, "scenario_id")
        if self.scenario_id not in ALLOWLISTED_SCENARIO_IDS:
            raise ContractError(
                "scenario_id must be the allowlisted synthetic scenario, "
                f"got {self.scenario_id!r}"
            )
        _require_text(self.scenario_label, "scenario_label")
        if not isinstance(self.state, BriefingState):
            raise ContractError("state must be a BriefingState")
        _require_aware(self.assembled_at, "assembled_at")
        if self.assembled_at is None:
            raise ContractError("assembled_at is required")
        if not isinstance(self.coverage, CoverageSummary):
            raise ContractError("coverage must be a CoverageSummary")
        if not isinstance(self.items, tuple):
            raise ContractError("items must be a tuple")
        if not isinstance(self.workspace_records, tuple):
            raise ContractError("workspace_records must be a tuple")
        if not isinstance(self.activities, tuple):
            raise ContractError("activities must be a tuple")
        if not isinstance(self.ask_responses, tuple):
            raise ContractError("ask_responses must be a tuple")
        _require_text_tuple(self.limitations, "briefing limitations")
        if not isinstance(self.workspace_context, WorkspaceContext):
            raise ContractError("workspace_context must be a WorkspaceContext")

        self._validate_items()
        self._validate_workspace()
        self._validate_ask_responses()
        self._validate_derived_counts()

    def _validate_items(self) -> None:
        identities: set[str] = set()
        for item in self.items:
            if not isinstance(item, BriefingItem):
                raise ContractError("items must contain BriefingItem")
            if item.assembled_at != self.assembled_at:
                raise ContractError(
                    "item assembled_at must match briefing assembled_at"
                )
            if item.lifecycle is not LifecycleState.ACTIVE:
                raise ContractError("every ordinary briefing item must be active")
            if item.item_id in identities:
                raise ContractError(f"duplicate item_id {item.item_id}")
            identities.add(item.item_id)

        order_by_section: dict[BriefingSection, set[int]] = {}
        for item in self.items:
            seen_orders = order_by_section.setdefault(item.section, set())
            if item.display_order in seen_orders:
                raise ContractError(
                    f"duplicate display_order in section {item.section.value}"
                )
            seen_orders.add(item.display_order)

        for item in self.items:
            for related in item.related_item_ids:
                if related not in identities:
                    raise ContractError(
                        f"related_item_id {related} does not exist in the briefing"
                    )
        self._reject_relationship_cycles()

    def _reject_relationship_cycles(self) -> None:
        edges = {item.item_id: set(item.related_item_ids) for item in self.items}
        for source, targets in edges.items():
            for target in targets:
                if source in edges.get(target, set()):
                    raise ContractError(
                        "related_item relationships must be one-way, not mutual"
                    )
        visiting: set[str] = set()
        visited: set[str] = set()

        def walk(node: str) -> None:
            if node in visiting:
                raise ContractError("related_item relationships must not form a cycle")
            if node in visited:
                return
            visiting.add(node)
            for target in edges.get(node, set()):
                walk(target)
            visiting.discard(node)
            visited.add(node)

        for node in edges:
            walk(node)

    def _validate_workspace(self) -> None:
        record_ids: set[str] = set()
        for record in self.workspace_records:
            if not isinstance(record, WorkspaceRecord):
                raise ContractError("workspace_records must contain WorkspaceRecord")
            if record.record_id in record_ids:
                raise ContractError(
                    f"duplicate workspace record_id {record.record_id}"
                )
            record_ids.add(record.record_id)
        activity_ids: set[str] = set()
        for activity in self.activities:
            if not isinstance(activity, ActivityEntry):
                raise ContractError("activities must contain ActivityEntry")
            if activity.activity_id in activity_ids:
                raise ContractError(
                    f"duplicate activity_id {activity.activity_id}"
                )
            activity_ids.add(activity.activity_id)

    def _validate_ask_responses(self) -> None:
        seen_ids: list[str] = []
        for response in self.ask_responses:
            if not isinstance(response, AskResponse):
                raise ContractError("ask_responses must contain AskResponse")
            if response.question_id in seen_ids:
                raise ContractError(
                    f"ask_responses must not repeat preset {response.question_id}"
                )
            seen_ids.append(response.question_id)
        if set(seen_ids) != set(ALLOWLISTED_ASK_QUESTION_IDS) or len(
            seen_ids
        ) != len(ALLOWLISTED_ASK_QUESTION_IDS):
            raise ContractError(
                "ask_responses must contain exactly the three allowlisted presets, "
                "each exactly once"
            )

    def _validate_derived_counts(self) -> None:
        expected_counts = derive_summary_counts(
            self.items, self.activities, self.assembled_at
        )
        if self.summary_counts != expected_counts:
            raise ContractError("summary_counts must be derived from the briefing")

        ordinary = tuple(item for item in self.items if item.is_ordinary)
        if self.coverage.eligible_item_count != len(ordinary):
            raise ContractError(
                "coverage eligible_item_count must equal the active ordinary items"
            )
        if self.coverage.source_reference_count != len(
            unique_source_references(self.items)
        ):
            raise ContractError(
                "coverage source_reference_count must equal unique source references"
            )

    def items_in_section(self, section: BriefingSection) -> tuple[BriefingItem, ...]:
        """Return active ordinary items in a section ordered by display order."""
        selected = [
            item
            for item in self.items
            if item.section is section and item.is_ordinary
        ]
        selected.sort(key=lambda item: item.display_order)
        return tuple(selected)

    def item_by_id(self, item_id: str) -> BriefingItem | None:
        """Return the item with a given identity, if present."""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def ask_response(self, question_id: str) -> AskResponse | None:
        """Return the preset Ask response for an allowlisted identity."""
        for response in self.ask_responses:
            if response.question_id == question_id:
                return response
        return None
