"""Phase 3C demonstration bridge.

This module provides the smallest governed path from Phase 3B synthetic document
admission into explainable, evidence-backed answers with citations,
provenance, and append-only audit records.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
import re

from ..document_admission import AdmissionResult, AuthorizationReceipt, DocumentFormat
from ..document_admission.durable_repository import SqliteDurableRepository
from ..document_admission.runtime import DocumentCustodyRuntime

_GENESIS_HASH = "0" * 64
_TERM_PATTERN = re.compile(r"[a-z0-9]{3,}")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")


def _require_aware(value: datetime, field_name: str) -> None:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ValueError(f"{field_name} must be timezone-aware")


def _normalize_unique(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    normalized: list[str] = []
    for value in values:
        _require_text(value, field_name)
        normalized.append(value)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} cannot contain duplicates")
    return tuple(normalized)


class Gate2ReviewRejected(RuntimeError):
    """Raised when promotion is denied by review."""


class Gate2RetrievalDenied(RuntimeError):
    """Raised when governed retrieval requirements are not met."""


class AnswerState(str, Enum):
    GROUNDED = "grounded"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass(frozen=True)
class BridgeAuditEvent:
    event_id: str
    correlation_id: str
    event_kind: str
    subject_id: str
    reason_code: str
    recorded_at: datetime
    prior_event_hash_hex: str
    event_hash_hex: str

    def __post_init__(self) -> None:
        for name in ("event_id", "correlation_id", "event_kind", "subject_id", "reason_code"):
            _require_text(getattr(self, name), name)
        _require_aware(self.recorded_at, "recorded_at")
        for name in ("prior_event_hash_hex", "event_hash_hex"):
            value = getattr(self, name)
            if (
                len(value) != 64
                or value != value.lower()
                or any(character not in "0123456789abcdef" for character in value)
            ):
                raise ValueError(f"{name} must be a lowercase sha256 hex digest")


@dataclass(frozen=True)
class KnowledgePromotionCandidate:
    candidate_id: str
    correlation_id: str
    object_id: str
    admission_attempt_id: str
    receipt_id: str
    source_record_id: str
    organization_domain_id: str
    classification: str
    content_digest_hex: str
    admitted_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "candidate_id",
            "correlation_id",
            "object_id",
            "admission_attempt_id",
            "receipt_id",
            "source_record_id",
            "organization_domain_id",
            "classification",
            "content_digest_hex",
        ):
            _require_text(getattr(self, name), name)
        _require_aware(self.admitted_at, "admitted_at")


@dataclass(frozen=True)
class SourceCitation:
    citation_id: str
    knowledge_id: str
    source_record_id: str
    excerpt: str

    def __post_init__(self) -> None:
        for name in ("citation_id", "knowledge_id", "source_record_id", "excerpt"):
            _require_text(getattr(self, name), name)


@dataclass(frozen=True)
class SourceProvenance:
    knowledge_id: str
    object_id: str
    admission_attempt_id: str
    receipt_id: str
    source_record_id: str
    content_digest_hex: str
    promoted_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "knowledge_id",
            "object_id",
            "admission_attempt_id",
            "receipt_id",
            "source_record_id",
            "content_digest_hex",
        ):
            _require_text(getattr(self, name), name)
        _require_aware(self.promoted_at, "promoted_at")


@dataclass(frozen=True)
class PromotedKnowledge:
    knowledge_id: str
    candidate_id: str
    title: str
    excerpt: str
    allowed_consumer_ids: tuple[str, ...]
    allowed_uses: tuple[str, ...]
    citation: SourceCitation
    provenance: SourceProvenance
    promoted_at: datetime

    def __post_init__(self) -> None:
        for name in ("knowledge_id", "candidate_id", "title", "excerpt"):
            _require_text(getattr(self, name), name)
        _normalize_unique(self.allowed_consumer_ids, "allowed_consumer_ids")
        _normalize_unique(self.allowed_uses, "allowed_uses")
        if not isinstance(self.citation, SourceCitation):
            raise ValueError("citation must be a SourceCitation")
        if not isinstance(self.provenance, SourceProvenance):
            raise ValueError("provenance must be a SourceProvenance")
        _require_aware(self.promoted_at, "promoted_at")


@dataclass(frozen=True)
class ExplainableAnswer:
    question_id: str
    question: str
    state: AnswerState
    statement: str | None
    citations: tuple[SourceCitation, ...]
    provenance: tuple[SourceProvenance, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.question_id, "question_id")
        _require_text(self.question, "question")
        if not isinstance(self.state, AnswerState):
            raise ValueError("state must be an AnswerState")
        if not isinstance(self.citations, tuple) or not isinstance(self.provenance, tuple):
            raise ValueError("citations and provenance must be tuples")
        for citation in self.citations:
            if not isinstance(citation, SourceCitation):
                raise ValueError("citations must contain SourceCitation entries")
        for entry in self.provenance:
            if not isinstance(entry, SourceProvenance):
                raise ValueError("provenance must contain SourceProvenance entries")
        if not isinstance(self.limitations, tuple) or not self.limitations:
            raise ValueError("limitations must be a non-empty tuple")
        for limitation in self.limitations:
            _require_text(limitation, "limitation")

        if self.state is AnswerState.GROUNDED:
            _require_text(self.statement or "", "statement")
            if not self.citations or not self.provenance:
                raise ValueError("grounded answers require citations and provenance")
        else:
            if self.statement is not None:
                raise ValueError("insufficient-evidence answers cannot include a statement")


class Phase3CBridge:
    """Minimal Gate 2 bridge for governed promotion, retrieval, and explanation."""

    def __init__(
        self,
        *,
        runtime: DocumentCustodyRuntime,
        repository: SqliteDurableRepository,
        allowed_consumer_ids: tuple[str, ...],
        allowed_uses: tuple[str, ...],
    ) -> None:
        self._runtime = runtime
        self._repository = repository
        self._allowed_consumer_ids = _normalize_unique(
            allowed_consumer_ids, "allowed_consumer_ids"
        )
        self._allowed_uses = _normalize_unique(allowed_uses, "allowed_uses")
        self._candidates: dict[str, KnowledgePromotionCandidate] = {}
        self._promoted: dict[str, PromotedKnowledge] = {}
        self._audit_events: list[BridgeAuditEvent] = []
        self._audit_tail_by_correlation: dict[str, str] = {}

    def admit_for_review(
        self,
        *,
        correlation_id: str,
        receipt: AuthorizationReceipt,
        payload: bytes,
        admission_attempt_id: str,
        object_id: str,
        admitted_at: datetime,
        document_format: DocumentFormat = DocumentFormat.PDF,
    ) -> KnowledgePromotionCandidate:
        _require_text(correlation_id, "correlation_id")
        _require_text(admission_attempt_id, "admission_attempt_id")
        _require_text(object_id, "object_id")
        _require_aware(admitted_at, "admitted_at")
        result = self._runtime.admit(
            receipt=receipt,
            payload=payload,
            admission_attempt_id=admission_attempt_id,
            object_id=object_id,
            now=admitted_at,
            document_format=document_format,
        )
        candidate = self._candidate_from_admission(correlation_id, receipt, result)
        self._candidates[candidate.candidate_id] = candidate
        self._append_audit(
            correlation_id=correlation_id,
            event_kind="admission.accepted",
            subject_id=candidate.candidate_id,
            reason_code="synthetic_document_admitted",
            recorded_at=admitted_at,
        )
        return candidate

    def promote_candidate(
        self,
        *,
        candidate_id: str,
        reviewer_id: str,
        rationale: str,
        approved: bool,
        title: str,
        promoted_at: datetime,
    ) -> PromotedKnowledge:
        _require_text(candidate_id, "candidate_id")
        _require_text(reviewer_id, "reviewer_id")
        _require_text(rationale, "rationale")
        _require_text(title, "title")
        _require_aware(promoted_at, "promoted_at")

        candidate = self._candidates.get(candidate_id)
        if candidate is None:
            raise KeyError(f"unknown candidate: {candidate_id}")
        if not approved:
            self._append_audit(
                correlation_id=candidate.correlation_id,
                event_kind="promotion.rejected",
                subject_id=candidate_id,
                reason_code="human_review_rejected",
                recorded_at=promoted_at,
            )
            raise Gate2ReviewRejected("promotion rejected by reviewer")

        knowledge_id = f"knowledge-{candidate.admission_attempt_id}"
        existing = self._promoted.get(knowledge_id)
        if existing is not None:
            return existing

        excerpt = _extract_excerpt(self._repository.retrieve_plaintext(candidate.object_id))
        citation = SourceCitation(
            citation_id=f"citation-{candidate.admission_attempt_id}",
            knowledge_id=knowledge_id,
            source_record_id=candidate.source_record_id,
            excerpt=excerpt,
        )
        provenance = SourceProvenance(
            knowledge_id=knowledge_id,
            object_id=candidate.object_id,
            admission_attempt_id=candidate.admission_attempt_id,
            receipt_id=candidate.receipt_id,
            source_record_id=candidate.source_record_id,
            content_digest_hex=candidate.content_digest_hex,
            promoted_at=promoted_at,
        )
        knowledge = PromotedKnowledge(
            knowledge_id=knowledge_id,
            candidate_id=candidate.candidate_id,
            title=title,
            excerpt=excerpt,
            allowed_consumer_ids=self._allowed_consumer_ids,
            allowed_uses=self._allowed_uses,
            citation=citation,
            provenance=provenance,
            promoted_at=promoted_at,
        )
        self._promoted[knowledge_id] = knowledge
        self._append_audit(
            correlation_id=candidate.correlation_id,
            event_kind="promotion.approved",
            subject_id=knowledge_id,
            reason_code="human_review_approved",
            recorded_at=promoted_at,
        )
        return knowledge

    def ask(
        self,
        *,
        correlation_id: str,
        question_id: str,
        question: str,
        consumer_id: str,
        intended_use: str,
        asked_at: datetime,
    ) -> ExplainableAnswer:
        _require_text(correlation_id, "correlation_id")
        _require_text(question_id, "question_id")
        _require_text(question, "question")
        _require_text(consumer_id, "consumer_id")
        _require_text(intended_use, "intended_use")
        _require_aware(asked_at, "asked_at")
        if consumer_id not in self._allowed_consumer_ids:
            self._append_audit(
                correlation_id=correlation_id,
                event_kind="retrieval.denied",
                subject_id=question_id,
                reason_code="consumer_not_permitted",
                recorded_at=asked_at,
            )
            raise Gate2RetrievalDenied("consumer is not permitted")
        if intended_use not in self._allowed_uses:
            self._append_audit(
                correlation_id=correlation_id,
                event_kind="retrieval.denied",
                subject_id=question_id,
                reason_code="use_not_permitted",
                recorded_at=asked_at,
            )
            raise Gate2RetrievalDenied("intended use is not permitted")

        matches = self._retrieve_matches(question)
        if not matches:
            answer = ExplainableAnswer(
                question_id=question_id,
                question=question,
                state=AnswerState.INSUFFICIENT_EVIDENCE,
                statement=None,
                citations=(),
                provenance=(),
                limitations=(
                    "No promoted synthetic knowledge matched this question within the "
                    "authorized retrieval boundary.",
                ),
            )
            self._append_audit(
                correlation_id=correlation_id,
                event_kind="answer.insufficient",
                subject_id=question_id,
                reason_code="no_matching_promoted_knowledge",
                recorded_at=asked_at,
            )
            return answer

        citations = tuple(match.citation for match in matches)
        provenance = tuple(match.provenance for match in matches)
        top_match = matches[0]
        answer = ExplainableAnswer(
            question_id=question_id,
            question=question,
            state=AnswerState.GROUNDED,
            statement=(
                "Within this synthetic demonstration scope, the strongest promoted "
                f"evidence is '{top_match.title}'."
            ),
            citations=citations,
            provenance=provenance,
            limitations=(
                "This answer is bounded to promoted synthetic records and does not "
                "represent live organizational truth.",
            ),
        )
        self._append_audit(
            correlation_id=correlation_id,
            event_kind="answer.grounded",
            subject_id=question_id,
            reason_code="evidence_assembled",
            recorded_at=asked_at,
        )
        return answer

    def audit_history(self, *, correlation_id: str | None = None) -> tuple[BridgeAuditEvent, ...]:
        if correlation_id is None:
            return tuple(self._audit_events)
        _require_text(correlation_id, "correlation_id")
        return tuple(
            event for event in self._audit_events if event.correlation_id == correlation_id
        )

    def verify_audit_integrity(self, *, correlation_id: str) -> bool:
        _require_text(correlation_id, "correlation_id")
        prior = _GENESIS_HASH
        for event in self.audit_history(correlation_id=correlation_id):
            if event.prior_event_hash_hex != prior:
                return False
            canonical = (
                f"{event.event_id}|{event.correlation_id}|{event.event_kind}|"
                f"{event.subject_id}|{event.reason_code}|"
                f"{event.recorded_at.isoformat()}|{event.prior_event_hash_hex}"
            ).encode("utf-8")
            expected = hashlib.sha256(canonical).hexdigest()
            if event.event_hash_hex != expected:
                return False
            prior = event.event_hash_hex
        return True

    def _retrieve_matches(self, question: str) -> list[PromotedKnowledge]:
        terms = set(_TERM_PATTERN.findall(question.lower()))
        if not terms:
            return []
        scored: list[tuple[int, PromotedKnowledge]] = []
        for knowledge in self._promoted.values():
            corpus = f"{knowledge.title} {knowledge.excerpt}".lower()
            score = sum(1 for term in terms if term in corpus)
            if score > 0:
                scored.append((score, knowledge))
        scored.sort(key=lambda entry: (-entry[0], entry[1].knowledge_id))
        return [entry[1] for entry in scored]

    def _candidate_from_admission(
        self,
        correlation_id: str,
        receipt: AuthorizationReceipt,
        result: AdmissionResult,
    ) -> KnowledgePromotionCandidate:
        return KnowledgePromotionCandidate(
            candidate_id=f"candidate-{result.admission_attempt_id}",
            correlation_id=correlation_id,
            object_id=result.record.object_id,
            admission_attempt_id=result.admission_attempt_id,
            receipt_id=result.receipt_id,
            source_record_id=receipt.source_record_id,
            organization_domain_id=receipt.organization_domain_id,
            classification=receipt.classification,
            content_digest_hex=result.record.content_identity.digest_hex,
            admitted_at=result.record.created_at,
        )

    def _append_audit(
        self,
        *,
        correlation_id: str,
        event_kind: str,
        subject_id: str,
        reason_code: str,
        recorded_at: datetime,
    ) -> BridgeAuditEvent:
        prior_hash = self._audit_tail_by_correlation.get(correlation_id, _GENESIS_HASH)
        event_id = f"{correlation_id}-event-{len(self._audit_events) + 1:04d}"
        canonical = (
            f"{event_id}|{correlation_id}|{event_kind}|{subject_id}|{reason_code}|"
            f"{recorded_at.isoformat()}|{prior_hash}"
        ).encode("utf-8")
        event_hash = hashlib.sha256(canonical).hexdigest()
        event = BridgeAuditEvent(
            event_id=event_id,
            correlation_id=correlation_id,
            event_kind=event_kind,
            subject_id=subject_id,
            reason_code=reason_code,
            recorded_at=recorded_at,
            prior_event_hash_hex=prior_hash,
            event_hash_hex=event_hash,
        )
        self._audit_events.append(event)
        self._audit_tail_by_correlation[correlation_id] = event_hash
        return event


def _extract_excerpt(payload: bytes) -> str:
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    raw_text = payload.decode("utf-8", errors="ignore")
    normalized = " ".join(raw_text.replace("\r", "\n").split())
    if not normalized:
        return "Synthetic promoted evidence with no decodable text."
    return normalized[:280]
