"""Governed runtime provider for the Executive Shell.

Builds ExecutiveBriefing data from governed runtime admission, promotion,
retrieval, provenance, and audit evidence without using synthetic fixture
providers for operational pages.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
import hashlib
import json
from math import sqrt
import os
from pathlib import Path
import tempfile
from typing import Any
import urllib.error
import urllib.request

from collector.document_admission import (
    DocumentFormat,
    DocumentCustodyRuntime,
    Ed25519ReceiptVerifier,
    SqliteDurableRepository,
    derive_audit_key,
    generate_master_key,
    generate_salt,
    generate_synthetic_signing_key,
    sign_synthetic_receipt,
    synthetic_authorization_policy,
    synthetic_custody_policy,
    synthetic_retention_policy,
)
from collector.embeddings import (
    APPROVED_VECTOR_DIMENSIONS,
    EmbeddingIdentity,
    OllamaEmbeddingProvider,
)
from collector.memory import MemoryItem, MemoryType
from collector.memory.governance import (
    MemoryLifecycleState,
    lifecycle_to_payload,
    provenance_to_payload,
)
from collector.memory.persistence import MemoryIndexWriteResult, QdrantMemoryRepository
from collector.memory.retrieval import RetrievalCandidate
from collector.memory.runtime.application_service import MemoryApplicationService
from collector.organizational_intelligence import (
    AnswerState,
    ExplainableAnswer,
    Gate2ReviewRejected,
    Phase3CBridge,
    PromotedKnowledge,
)

from .models import (
    ALLOWLISTED_SCENARIO_ID,
    ActivityEntry,
    ActivityKind,
    AskResponse,
    AskState,
    BriefingItem,
    BriefingSection,
    BriefingState,
    CoverageSummary,
    EvidenceClassification,
    ExecutiveBriefing,
    KnowledgeKind,
    NextContext,
    NextItemKind,
    PermittedNextStep,
    SourceReference,
    UncertaintyState,
    WorkspaceBannerTone,
    WorkspaceKind,
    WorkspaceContext,
    WorkspaceMode,
    OrganizationProfile,
    WorkspaceRecord,
    WorkspaceState,
    derive_freshness,
    derive_summary_counts,
    unique_source_references,
)
from .fixtures import SyntheticBriefingProvider


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_demo_id(prefix: str, value: str) -> str:
    cleaned = "".join(
        character
        for character in value.lower()
        if character.isalnum() or character == "-"
    )
    cleaned = cleaned.strip("-") or "entry"
    return f"demo-{prefix}-{cleaned}"


def _sorted_unique(values: list[str]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _normalize_runtime_statement(value: object) -> str:
    """Collapse transport-safe model whitespace for the shell text contract."""
    if not isinstance(value, str):
        return ""
    without_controls = "".join(
        character if ord(character) >= 32 else " " for character in value
    )
    return " ".join(without_controls.split())


@dataclass
class _StagedSubmission:
    submission_id: str
    source_record_id: str
    file_name: str
    media_type: str
    byte_count: int
    digest_hex: str
    admitted_at: datetime
    governance_state: str
    reason: str
    candidate_id: str | None = None


@dataclass(frozen=True)
class _GovernanceEvent:
    subject_id: str
    action: str
    before_state: str
    after_state: str
    reason: str
    actor: str
    occurred_at: datetime


@dataclass(frozen=True)
class _QuestionRuntimeResult:
    trace_id: str
    asked_at: datetime
    candidate_count: int
    selected_count: int
    stale_count: int
    conflicting_sources: tuple[str, ...]
    recommendation: str
    insufficient_reason: str | None = None


@dataclass(frozen=True)
class _ExternalAskAnswer:
    state: AnswerState
    statement: str | None


@dataclass(frozen=True)
class _RuntimeServiceStatus:
    service: str
    state: str
    detail: str
    observed_at: datetime


def _unavailable_runtime_health(*, detail: str) -> tuple[_RuntimeServiceStatus, ...]:
    observed = _now()
    services = ("interaction", "memory", "qdrant", "ollama")
    return tuple(
        _RuntimeServiceStatus(
            service=service,
            state="unavailable",
            detail=detail,
            observed_at=observed,
        )
        for service in services
    )


class _CanonicalRuntimeClient:
    """HTTP client for existing canonical governed runtime services."""

    def __init__(self) -> None:
        self._interaction_base_url = (
            os.getenv("BONSAAI_INTERACTION_API_URL", "").strip()
            or "http://jebediah-interaction:8001"
        ).rstrip("/")
        self._interaction_service_token = os.getenv(
            "BONSAAI_INTERACTION_SERVICE_TOKEN", ""
        ).strip()
        self._memory_base_url = (
            os.getenv("BONSAAI_MEMORY_API_URL", "").strip()
            or "http://jebediah-memory:8000"
        ).rstrip("/")
        self._qdrant_url = (
            os.getenv("QDRANT_URL", "").strip()
            or os.getenv("BONSAAI_QDRANT_URL", "").strip()
            or "http://qdrant:6333"
        ).rstrip("/")
        self._ollama_url = (
            os.getenv("OLLAMA_URL", "").strip()
            or os.getenv("BONSAAI_OLLAMA_URL", "").strip()
            or "http://ollama:11434"
        ).rstrip("/")
        self._timeout_seconds = int(
            os.getenv("BONSAAI_RUNTIME_TIMEOUT_SECONDS", "300")
        )
        self._health_timeout_seconds = int(
            os.getenv("BONSAAI_HEALTH_TIMEOUT_SECONDS", "2")
        )
        self._question_timeout_seconds = int(
            os.getenv("BONSAAI_QUESTION_TIMEOUT_SECONDS", "85")
        )

    def _url(self, base: str, path_env: str, default_path: str) -> str:
        raw = os.getenv(path_env, "").strip()
        path = raw if raw else default_path
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{base}{path}"

    def _request_json(
        self,
        *,
        method: str,
        url: str,
        operation: str,
        payload: dict[str, Any] | None = None,
        allow_non_json: bool = False,
        bearer_token: str | None = None,
        timeout_seconds: int | None = None,
    ) -> dict[str, Any]:
        data: bytes | None = None
        headers: dict[str, str] = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        request = urllib.request.Request(
            url=url,
            data=data,
            headers=headers,
            method=method,
        )
        effective_timeout = (
            self._timeout_seconds if timeout_seconds is None else timeout_seconds
        )
        try:
            with urllib.request.urlopen(request, timeout=effective_timeout) as response:
                body = response.read()

        except urllib.error.HTTPError as error:
            raise RuntimeError(
                f"runtime_request_failed: {operation}: http_status_{error.code}"
            ) from error

        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
            raise RuntimeError(f"runtime_request_failed: {operation}") from error
        if not body:
            return {}
        try:
            decoded = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            if allow_non_json:
                return {}
            raise RuntimeError(f"runtime_response_invalid_json: {operation}") from error
        if not isinstance(decoded, dict):
            if allow_non_json:
                return {}
            raise RuntimeError(f"runtime_response_invalid_shape: {operation}")
        return decoded

    def _request_available(self, *, url: str, timeout_seconds: int) -> bool:
        request = urllib.request.Request(
            url=url,
            headers={"Accept": "*/*"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds):
                return True
        except (urllib.error.URLError, TimeoutError, ValueError, OSError):
            return False

    def runtime_health(self) -> tuple[_RuntimeServiceStatus, ...]:
        checks: list[tuple[str, str]] = [
            ("interaction", self._url(self._interaction_base_url, "BONSAAI_INTERACTION_HEALTH_PATH", "/health")),
            ("memory", self._url(self._memory_base_url, "BONSAAI_MEMORY_HEALTH_PATH", "/health")),
            ("qdrant", f"{self._qdrant_url}/healthz"),
            ("ollama", f"{self._ollama_url}/api/tags"),
        ]
        statuses: list[_RuntimeServiceStatus] = []
        observed = _now()
        for service_name, url in checks:
            try:
                payload = self._request_json(
                    method="GET",
                    url=url,
                    operation=f"{service_name}_health",
                    timeout_seconds=self._health_timeout_seconds,
                )
                detail = str(payload.get("status", "online")).strip() or "online"
                statuses.append(
                    _RuntimeServiceStatus(
                        service=service_name,
                        state="ready",
                        detail=detail,
                        observed_at=observed,
                    )
                )
            except RuntimeError:
                if self._request_available(
                    url=url,
                    timeout_seconds=self._health_timeout_seconds,
                ):
                    statuses.append(
                        _RuntimeServiceStatus(
                            service=service_name,
                            state="ready",
                            detail="online",
                            observed_at=observed,
                        )
                    )
                else:
                    statuses.append(
                        _RuntimeServiceStatus(
                            service=service_name,
                            state="unavailable",
                            detail="connection_failed",
                            observed_at=observed,
                        )
                    )
        return tuple(statuses)

    def submit_admission(
        self,
        *,
        source_record_id: str,
        file_name: str,
        media_type: str,
        payload_b64: str,
        byte_count: int,
        workspace_mode: str,
        organization_id: str,
    ) -> dict[str, Any]:
        url = self._url(
            self._interaction_base_url,
            "BONSAAI_INTERACTION_ADMISSION_PATH",
            "/admission/submit",
        )
        return self._request_json(
            method="POST",
            url=url,
            operation="interaction_admission",
            payload={
                "source_record_id": source_record_id,
                "file_name": file_name,
                "media_type": media_type,
                "payload_base64": payload_b64,
                "byte_count": byte_count,
                "workspace_mode": workspace_mode,
                "organization_id": organization_id,
            },
            allow_non_json=True,
            bearer_token=self._interaction_service_token,
        )

    def ask_question(
        self,
        *,
        question: str,
        workspace_mode: str,
        organization_id: str,
    ) -> dict[str, Any]:
        url = self._url(
            self._interaction_base_url,
            "BONSAAI_INTERACTION_ASK_PATH",
            "/questions/ask",
        )
        return self._request_json(
            method="POST",
            url=url,
            operation="interaction_question",
            payload={
                "question": question,
                "workspace_mode": workspace_mode,
                "organization_id": organization_id,
            },
            bearer_token=self._interaction_service_token,
            timeout_seconds=self._question_timeout_seconds,
        )

    def promote_admission(
        self,
        *,
        candidate_id: str,
        workspace_mode: str,
        organization_id: str,
    ) -> dict[str, Any]:
        url = self._url(
            self._interaction_base_url,
            "BONSAAI_INTERACTION_PROMOTION_PATH",
            "/admission/promote",
        )
        return self._request_json(
            method="POST",
            url=url,
            operation="interaction_promotion",
            payload={
                "candidate_id": candidate_id,
                "workspace_mode": workspace_mode,
                "organization_id": organization_id,
            },
            bearer_token=self._interaction_service_token,
        )

    def reject_admission(
        self,
        *,
        candidate_id: str,
        reason: str,
        workspace_mode: str,
        organization_id: str,
    ) -> dict[str, Any]:
        url = self._url(
            self._interaction_base_url,
            "BONSAAI_INTERACTION_REJECTION_PATH",
            "/admission/reject",
        )
        return self._request_json(
            method="POST",
            url=url,
            operation="interaction_rejection",
            payload={
                "candidate_id": candidate_id,
                "reason": reason,
                "workspace_mode": workspace_mode,
                "organization_id": organization_id,
            },
            bearer_token=self._interaction_service_token,
        )

    def memory_context(
        self,
        *,
        question: str,
        workspace_mode: str,
        organization_id: str,
    ) -> dict[str, Any]:
        url = self._url(
            self._memory_base_url,
            "BONSAAI_MEMORY_CONTEXT_PATH",
            "/memory/context",
        )
        return self._request_json(
            method="POST",
            url=url,
            operation="memory_context",
            payload={
                "source_identity": "executive-shell",
                "content": question,
                "memory_type": "context",
                "importance": 0.7,
                "organization_id": organization_id,
                "workspace_mode": workspace_mode,
                "approved_only": True,
            },
        )


class _DeterministicEmbeddingProvider:
    """Deterministic in-process embedding fallback for disconnected runtimes."""

    @property
    def identity(self) -> EmbeddingIdentity:
        return EmbeddingIdentity.approved()

    def ensure_ready(self) -> None:
        return

    def embed(self, text: str) -> list[float]:
        tokens = [token for token in text.lower().split() if token.strip()]
        vector = [0.0] * APPROVED_VECTOR_DIMENSIONS
        for token in tokens:
            slot = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:8], 16)
            vector[slot % APPROVED_VECTOR_DIMENSIONS] += 1.0
        if not any(vector):
            vector[0] = 1.0
        return vector


class _InProcessSemanticRepository:
    """Local semantic repository used only when Qdrant runtime is unavailable."""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[MemoryItem, list[float], dict[str, Any]]] = {}

    def verify_vector_space(self) -> None:
        return

    def index(
        self,
        memory: MemoryItem,
        vector: list[float],
        embedding_identity: EmbeddingIdentity,
    ) -> MemoryIndexWriteResult:
        embedding_identity.require_approved()
        payload = {
            "memory_id": memory.id,
            "source_identity": memory.source_identity,
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "importance": memory.importance,
            "metadata": memory.metadata,
            "provenance": provenance_to_payload(memory.provenance, memory.source_identity),
            "lifecycle": lifecycle_to_payload(memory.lifecycle),
            "created_at": memory.created_at.isoformat(),
            "embedding_identity": embedding_identity.to_payload(),
        }
        self._entries[memory.id] = (memory, list(vector), payload)
        return MemoryIndexWriteResult(
            memory_id=memory.id,
            point_id=f"local-point-{memory.id}",
            vector_dimensions=len(vector),
            payload=payload,
        )

    def find(self, memory_id: str) -> MemoryItem | None:
        entry = self._entries.get(memory_id)
        return entry[0] if entry is not None else None

    def contains(self, memory_id: str) -> bool:
        return memory_id in self._entries

    def search(
        self,
        query_vector: list[float],
        embedding_identity: EmbeddingIdentity,
        limit: int,
    ) -> list[RetrievalCandidate]:
        embedding_identity.require_approved()
        scored: list[tuple[float, dict[str, Any]]] = []
        for _, vector, payload in self._entries.values():
            similarity = _cosine_similarity(query_vector, vector)
            if similarity <= 0.0:
                continue
            scored.append((similarity, payload))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [
            RetrievalCandidate.from_payload(semantic_relevance=score, payload=payload)
            for score, payload in scored[:limit]
        ]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


class GovernedRuntimeBriefingProvider:
    """Governed provider that keeps the ExecutiveBriefing UI contract stable."""

    def __init__(
        self,
        runtime_directory: Path,
        *,
        qdrant_enabled: bool | None = None,
        collection_name: str | None = None,
        canonical_runtime: bool | None = None,
        organization_id: str = "demo-organization",
        workspace_mode: WorkspaceMode = WorkspaceMode.PRODUCTION,
    ) -> None:
        self._runtime_directory = runtime_directory
        self._qdrant_enabled = qdrant_enabled
        self._collection_name = collection_name
        self._organization_id = organization_id
        self._workspace_mode = workspace_mode
        self._canonical_runtime_enabled = (
            canonical_runtime
            if canonical_runtime is not None
            else os.getenv("BONSAAI_CANONICAL_RUNTIME", "").strip().lower()
            in {"1", "true", "yes"}
        )
        self._runtime_client = (
            _CanonicalRuntimeClient() if self._canonical_runtime_enabled else None
        )
        self._repository: SqliteDurableRepository | None = None
        self._runtime: DocumentCustodyRuntime | None = None
        self._bridge: Phase3CBridge | None = None
        self._signer_key = None
        self._signer_id = "synthetic-governed-signer"
        if not self._canonical_runtime_enabled:
            master_key = generate_master_key()
            audit_key = derive_audit_key(master_key, generate_salt())
            self._repository = SqliteDurableRepository(
                runtime_directory=runtime_directory,
                master_key=master_key,
                audit_key=audit_key,
                custody_policy=synthetic_custody_policy(),
            )
            signer_key = generate_synthetic_signing_key()
            self._signer_id = "synthetic-governed-signer"
            self._runtime = DocumentCustodyRuntime(
                repository=self._repository,
                receipt_verifier=Ed25519ReceiptVerifier(
                    {self._signer_id: signer_key.public_key()}
                ),
                authorization_policy=synthetic_authorization_policy((self._signer_id,)),
                retention_policy=synthetic_retention_policy(),
                custody_policy=synthetic_custody_policy(),
                max_admission_bytes=1_000_000,
            )
            self._bridge = Phase3CBridge(
                runtime=self._runtime,
                repository=self._repository,
                allowed_consumer_ids=("executive-consumer",),
                allowed_uses=("executive_question_answering",),
            )
            self._signer_key = signer_key
        self._sequence = 0
        self._last_answer: ExplainableAnswer | _ExternalAskAnswer | None = None
        self._last_semantic_candidates: tuple[RetrievalCandidate, ...] = ()
        self._last_question_result: _QuestionRuntimeResult | None = None
        self._last_question = "What should leadership decide next?"
        self._staged_submissions: list[_StagedSubmission] = []
        self._seen_content_digests: set[str] = set()
        self._canonical_submission_state_path = (
            self._runtime_directory / "canonical-submissions.json"
        )
        if self._canonical_runtime_enabled:
            self._load_canonical_submissions()
        self._governance_events: list[_GovernanceEvent] = []
        self._runtime_health: tuple[_RuntimeServiceStatus, ...] = ()
        self._memory_runtime_mode = "uninitialized"
        self._memory_runtime_issue: str | None = None
        self._memory_indexed_knowledge: set[str] = set()
        self._memory_runtime = None
        if self._canonical_runtime_enabled:
            self._memory_runtime_mode = "external_canonical_runtime"
        else:
            self._memory_runtime = self._create_memory_runtime()

    def _load_canonical_submissions(self) -> None:
        if not self._canonical_submission_state_path.exists():
            return
        try:
            with self._canonical_submission_state_path.open(
                "r", encoding="utf-8"
            ) as state_file:
                payload = json.load(state_file)
            if not isinstance(payload, list):
                raise ValueError("submission state must be a list")
            submissions = [
                _StagedSubmission(
                    submission_id=str(item["submission_id"]),
                    source_record_id=str(item["source_record_id"]),
                    file_name=str(item["file_name"]),
                    media_type=str(item["media_type"]),
                    byte_count=int(item["byte_count"]),
                    digest_hex=str(item["digest_hex"]),
                    admitted_at=datetime.fromisoformat(str(item["admitted_at"])),
                    governance_state=str(item["governance_state"]),
                    reason=str(item["reason"]),
                    candidate_id=(
                        str(item["candidate_id"]) if item.get("candidate_id") else None
                    ),
                )
                for item in payload
                if isinstance(item, dict)
            ]
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            raise RuntimeError("canonical_submission_state_invalid") from error
        self._staged_submissions = submissions
        self._seen_content_digests = {
            submission.digest_hex for submission in submissions
        }
        sequence_numbers = [
            int(submission.submission_id.removeprefix("submission-"))
            for submission in submissions
            if submission.submission_id.removeprefix("submission-").isdigit()
        ]
        self._sequence = max(sequence_numbers, default=0)

    def _persist_canonical_submissions(self) -> None:
        payload = [
            {
                "submission_id": submission.submission_id,
                "source_record_id": submission.source_record_id,
                "file_name": submission.file_name,
                "media_type": submission.media_type,
                "byte_count": submission.byte_count,
                "digest_hex": submission.digest_hex,
                "admitted_at": submission.admitted_at.isoformat(),
                "governance_state": submission.governance_state,
                "reason": submission.reason,
                "candidate_id": submission.candidate_id,
            }
            for submission in self._staged_submissions
        ]
        temporary_path = self._canonical_submission_state_path.with_suffix(".tmp")
        try:
            with temporary_path.open("w", encoding="utf-8") as state_file:
                json.dump(payload, state_file, separators=(",", ":"))
            temporary_path.replace(self._canonical_submission_state_path)
        except OSError as error:
            raise RuntimeError("canonical_submission_state_write_failed") from error

    @classmethod
    def create_default(cls) -> "GovernedRuntimeBriefingProvider":
        configured_root = os.getenv("JEBEDIAH_RUNTIME_ROOT", "").strip()
        if configured_root:
            runtime_root = Path(configured_root).resolve()
            runtime_root.mkdir(parents=True, exist_ok=True)
        else:
            runtime_root = Path(tempfile.mkdtemp(prefix="bonsaai-governed-runtime-"))
        return cls(runtime_root)

    @property
    def runtime_directory(self) -> Path:
        return self._runtime_directory

    @property
    def memory_runtime_mode(self) -> str:
        return self._memory_runtime_mode

    @property
    def memory_runtime_issue(self) -> str | None:
        return self._memory_runtime_issue

    def _create_memory_runtime(self) -> MemoryApplicationService:
        qdrant_enabled = self._qdrant_enabled
        if qdrant_enabled is None:
            qdrant_enabled = (
                os.getenv("JEBEDIAH_QDRANT_RUNTIME", "").strip().lower()
                in {"1", "true", "yes"}
            )
        if not qdrant_enabled:
            self._memory_runtime_mode = "local_semantic_runtime_fallback"
            self._memory_runtime_issue = (
                "Qdrant runtime is not enabled; set JEBEDIAH_QDRANT_RUNTIME=1 to enable."
            )
            fallback = MemoryApplicationService(
                embedding_provider=_DeterministicEmbeddingProvider(),
                repository=_InProcessSemanticRepository(),
            )
            fallback.ensure_ready()
            return fallback
        try:
            service = MemoryApplicationService(
                embedding_provider=OllamaEmbeddingProvider(),
                repository=QdrantMemoryRepository(
                    collection_name=self._collection_name
                ),
            )
            service.ensure_ready()
            self._memory_runtime_mode = "qdrant_semantic_runtime"
            return service
        except (
            ModuleNotFoundError,
            ImportError,
            OSError,
            RuntimeError,
            ValueError,
        ) as error:
            self._memory_runtime_mode = "local_semantic_runtime_fallback"
            self._memory_runtime_issue = str(error)
            fallback = MemoryApplicationService(
                embedding_provider=_DeterministicEmbeddingProvider(),
                repository=_InProcessSemanticRepository(),
            )
            fallback.ensure_ready()
            return fallback

    def _resolve_document_format(
        self,
        file_name: str,
        media_type: str,
    ) -> DocumentFormat | None:
        suffix = Path(file_name).suffix.lower()
        normalized_type = media_type.lower().split(";", 1)[0].strip()
        if normalized_type.startswith("image/"):
            return None
        allowed: dict[str, tuple[DocumentFormat, frozenset[str]]] = {
            ".pdf": (
                DocumentFormat.PDF,
                frozenset({"application/pdf", "application/octet-stream"}),
            ),
            ".docx": (
                DocumentFormat.DOCX,
                frozenset(
                    {
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "application/octet-stream",
                    }
                ),
            ),
            ".xlsx": (
                DocumentFormat.XLSX,
                frozenset(
                    {
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "application/octet-stream",
                    }
                ),
            ),
            ".pptx": (
                DocumentFormat.PPTX,
                frozenset(
                    {
                        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        "application/octet-stream",
                    }
                ),
            ),
            ".csv": (
                DocumentFormat.CSV,
                frozenset(
                    {
                        "text/csv",
                        "application/csv",
                        "application/vnd.ms-excel",
                        "text/plain",
                        "application/octet-stream",
                    }
                ),
            ),
            ".txt": (
                DocumentFormat.TXT,
                frozenset({"text/plain", "application/octet-stream"}),
            ),
            ".md": (
                DocumentFormat.MARKDOWN,
                frozenset(
                    {
                        "text/markdown",
                        "text/x-markdown",
                        "text/plain",
                        "application/octet-stream",
                    }
                ),
            ),
            ".markdown": (
                DocumentFormat.MARKDOWN,
                frozenset(
                    {
                        "text/markdown",
                        "text/x-markdown",
                        "text/plain",
                        "application/octet-stream",
                    }
                ),
            ),
        }
        selection = allowed.get(suffix)
        if selection is None or normalized_type not in selection[1]:
            raise ValueError("unsupported_document_format")
        return selection[0]

    def _record_governance_event(
        self,
        *,
        subject_id: str,
        action: str,
        before_state: str,
        after_state: str,
        reason: str,
        actor: str,
        occurred_at: datetime,
    ) -> None:
        self._governance_events.append(
            _GovernanceEvent(
                subject_id=subject_id,
                action=action,
                before_state=before_state,
                after_state=after_state,
                reason=reason,
                actor=actor,
                occurred_at=occurred_at,
            )
        )

    @staticmethod
    def _admission_result(submission: _StagedSubmission) -> dict[str, object]:
        """Return safe presentation metadata for one governed admission attempt."""
        return {
            "submission_id": submission.submission_id,
            "source_record_id": submission.source_record_id,
            "file_name": submission.file_name,
            "byte_count": submission.byte_count,
            "sha256": submission.digest_hex,
            "admission_state": submission.governance_state,
            "reason": submission.reason,
            "submitted_at": submission.admitted_at.isoformat(),
        }

    def admit_submission(
        self,
        *,
        payload: bytes,
        source_record_id: str,
        file_name: str,
        media_type: str,
    ) -> dict[str, object]:
        if not isinstance(payload, bytes) or not payload:
            raise ValueError("payload cannot be empty")
        if len(payload) > 1_000_000:
            raise ValueError("payload_exceeds_admission_limit")

        now = _now()
        normalized_source_id = (source_record_id or "").strip() or "source-record"
        normalized_file_name = (file_name or "").strip() or "uploaded-document"
        normalized_media_type = (media_type or "").strip() or "application/octet-stream"
        digest_hex = hashlib.sha256(payload).hexdigest()

        if self._canonical_runtime_enabled:
            self._sequence += 1
            submission_id = f"submission-{self._sequence}"
            self._record_governance_event(
                subject_id=submission_id,
                action="admission.requested",
                before_state="pending",
                after_state="submitted",
                reason="forwarded_to_canonical_runtime",
                actor="executive-shell",
                occurred_at=now,
            )
            if self._runtime_client is None:
                raise RuntimeError("canonical_runtime_client_unavailable")
            try:
                response = self._runtime_client.submit_admission(
                    source_record_id=normalized_source_id,
                    file_name=normalized_file_name,
                    media_type=normalized_media_type,
                    payload_b64=base64.b64encode(payload).decode("ascii"),
                    byte_count=len(payload),
                    workspace_mode=self._workspace_mode.value,
                    organization_id=self._organization_id,
                )
            except RuntimeError as error:
                failure_reason = str(error)
                staged = _StagedSubmission(
                    submission_id=submission_id,
                    source_record_id=normalized_source_id,
                    file_name=normalized_file_name,
                    media_type=normalized_media_type,
                    byte_count=len(payload),
                    digest_hex=digest_hex,
                    admitted_at=now,
                    governance_state="failed",
                    reason=failure_reason,
                )
                self._staged_submissions.append(staged)
                self._persist_canonical_submissions()
                self._record_governance_event(
                    subject_id=submission_id,
                    action="admission.failed",
                    before_state="submitted",
                    after_state="failed",
                    reason=failure_reason,
                    actor="executive-shell",
                    occurred_at=now,
                )
                return self._admission_result(staged)
            runtime_state = str(response.get("state", "review_pending")).strip().lower()
            state_mapping = {
                "review_pending": "review_pending",
                "pending_review": "review_pending",
                "approved": "approved",
                "promoted": "approved",
                "rejected": "rejected",
                "held": "needs_evidence",
                "needs_evidence": "needs_evidence",
                "quarantined": "review_pending",
            }
            governance_state = state_mapping.get(runtime_state, "review_pending")
            candidate_id = str(response.get("candidate_id", "")).strip() or None
            runtime_reason = (
                str(response.get("reason", "")).strip()
                or "canonical_runtime_submission_recorded"
            )
            staged = _StagedSubmission(
                submission_id=submission_id,
                source_record_id=normalized_source_id,
                file_name=normalized_file_name,
                media_type=normalized_media_type,
                byte_count=len(payload),
                digest_hex=digest_hex,
                admitted_at=now,
                governance_state=governance_state,
                reason=runtime_reason,
                candidate_id=candidate_id,
            )
            self._staged_submissions.append(staged)
            self._seen_content_digests.add(digest_hex)
            self._persist_canonical_submissions()
            self._record_governance_event(
                subject_id=submission_id,
                action="admission.recorded",
                before_state="submitted",
                after_state=governance_state,
                reason=runtime_reason,
                actor="canonical-runtime",
                occurred_at=now,
            )
            return self._admission_result(staged)

        self._sequence += 1
        submission_id = f"submission-{self._sequence}"
        self._record_governance_event(
            subject_id=submission_id,
            action="admission.received",
            before_state="pending",
            after_state="received",
            reason="upload_received",
            actor="knowledge-manager-operator",
            occurred_at=now,
        )

        if digest_hex in self._seen_content_digests:
            self._staged_submissions.append(
                _StagedSubmission(
                    submission_id=submission_id,
                    source_record_id=normalized_source_id,
                    file_name=normalized_file_name,
                    media_type=normalized_media_type,
                    byte_count=len(payload),
                    digest_hex=digest_hex,
                    admitted_at=now,
                    governance_state="rejected",
                    reason="duplicate_content_hash",
                )
            )
            self._record_governance_event(
                subject_id=submission_id,
                action="governance.rejected",
                before_state="received",
                after_state="rejected",
                reason="duplicate_content_hash",
                actor="governance-runtime",
                occurred_at=now,
            )
            raise ValueError("duplicate_content_hash")

        document_format = self._resolve_document_format(
            normalized_file_name,
            normalized_media_type,
        )
        self._record_governance_event(
            subject_id=submission_id,
            action="admission.validated",
            before_state="received",
            after_state="ready_for_review",
            reason="format_size_hash_validated",
            actor="governance-runtime",
            occurred_at=now,
        )

        if document_format is None:
            staged = _StagedSubmission(
                submission_id=submission_id,
                source_record_id=normalized_source_id,
                file_name=normalized_file_name,
                media_type=normalized_media_type,
                byte_count=len(payload),
                digest_hex=digest_hex,
                admitted_at=now,
                governance_state="needs_evidence",
                reason="ocr_boundary_not_enabled",
            )
            self._staged_submissions.append(staged)
            self._seen_content_digests.add(digest_hex)
            self._record_governance_event(
                subject_id=submission_id,
                action="governance.needs_evidence",
                before_state="ready_for_review",
                after_state="needs_evidence",
                reason="image_ingestion_requires_ocr_boundary",
                actor="governance-runtime",
                occurred_at=now,
            )
            return self._admission_result(staged)

        attempt_id = f"attempt-{self._sequence}"
        object_id = f"object-{self._sequence}"
        correlation_id = f"corr-{self._sequence}"
        policy = synthetic_authorization_policy((self._signer_id,))
        if self._signer_key is None or self._bridge is None:
            raise RuntimeError("local_governed_runtime_unavailable")
        receipt = sign_synthetic_receipt(
            receipt_id=f"receipt-{self._sequence}",
            organization_domain_id="governed-org-runtime",
            source_record_id=normalized_source_id,
            source_authority_role="Governed Source Authority",
            principal_id="knowledge-manager-operator",
            purpose=policy.required_purpose,
            classification=policy.required_classification,
            allowed_operation=policy.required_operation,
            retention_profile_id="governed-retention-profile",
            issued_at=now,
            expires_at=now + timedelta(minutes=10),
            signer_key_id=self._signer_id,
            private_key=self._signer_key,
        )
        candidate = self._bridge.admit_for_review(
            correlation_id=correlation_id,
            receipt=receipt,
            payload=payload,
            admission_attempt_id=attempt_id,
            object_id=object_id,
            admitted_at=now,
            document_format=document_format,
        )
        staged = _StagedSubmission(
            submission_id=submission_id,
            source_record_id=normalized_source_id,
            file_name=normalized_file_name,
            media_type=normalized_media_type,
            byte_count=len(payload),
            digest_hex=digest_hex,
            admitted_at=now,
            governance_state="review_pending",
            reason="admission_completed",
            candidate_id=candidate.candidate_id,
        )
        self._staged_submissions.append(staged)
        self._seen_content_digests.add(digest_hex)
        self._record_governance_event(
            subject_id=submission_id,
            action="governance.pending_review",
            before_state="ready_for_review",
            after_state="review_pending",
            reason="awaiting_human_review",
            actor="governance-runtime",
            occurred_at=now,
        )
        return self._admission_result(staged)

    def admit_document(self, document_text: str, source_record_id: str) -> None:
        text = (document_text or "").strip()
        if not text:
            raise ValueError("document_text cannot be empty")
        payload = (
            "%PDF-1.7\n"
            "GOVERNED ORGANIZATIONAL DOCUMENT\n"
            f"{text}\n"
            "%%EOF"
        ).encode("utf-8")
        self.admit_submission(
            payload=payload,
            source_record_id=source_record_id,
            file_name="admission-note.pdf",
            media_type="application/pdf",
        )

    def _latest_review_candidate(self):
        candidates = getattr(self._bridge, "_candidates")
        if not candidates:
            return None
        promoted = getattr(self._bridge, "_promoted")
        promoted_candidate_ids = {item.candidate_id for item in promoted.values()}
        pending = [
            candidate
            for candidate in candidates.values()
            if candidate.candidate_id not in promoted_candidate_ids
        ]
        if not pending:
            return None
        pending.sort(key=lambda item: item.candidate_id)
        return pending[-1]

    def promote_latest_candidate(self) -> None:
        if self._canonical_runtime_enabled:
            for staged in reversed(self._staged_submissions):
                if staged.governance_state == "review_pending":
                    if self._runtime_client is None:
                        raise RuntimeError("canonical_runtime_client_unavailable")
                    if staged.candidate_id is None:
                        raise RuntimeError("canonical_runtime_candidate_id_missing")
                    response = self._runtime_client.promote_admission(
                        candidate_id=staged.candidate_id,
                        workspace_mode=self._workspace_mode.value,
                        organization_id=self._organization_id,
                    )
                    if response.get("state") != "promoted":
                        raise RuntimeError("canonical_runtime_promotion_failed")
                    staged.governance_state = "approved"
                    staged.reason = "promoted_by_canonical_runtime"
                    self._persist_canonical_submissions()
                    self._record_governance_event(
                        subject_id=staged.submission_id,
                        action="governance.approved",
                        before_state="review_pending",
                        after_state="approved",
                        reason="promoted_by_canonical_runtime",
                        actor="knowledge-reviewer",
                        occurred_at=_now(),
                    )
                    return
            return
        candidate = self._latest_review_candidate()
        if candidate is None:
            return
        promoted_at = _now()
        promoted = self._bridge.promote_candidate(
            candidate_id=candidate.candidate_id,
            reviewer_id="knowledge-reviewer",
            rationale="Approved by human governance reviewer.",
            approved=True,
            title=f"Governed knowledge from {candidate.source_record_id}",
            promoted_at=promoted_at,
        )
        self._index_promoted_knowledge(promoted)
        for staged in self._staged_submissions:
            if staged.candidate_id == candidate.candidate_id:
                staged.governance_state = "approved"
                staged.reason = "review_approved"
                self._record_governance_event(
                    subject_id=staged.submission_id,
                    action="governance.approved",
                    before_state="review_pending",
                    after_state="approved",
                    reason="human_review_approved",
                    actor="knowledge-reviewer",
                    occurred_at=promoted_at,
                )
                break

    def _index_promoted_knowledge(self, promoted: PromotedKnowledge) -> None:
        if self._memory_runtime is None:
            raise RuntimeError("local_semantic_runtime_not_available")
        if promoted.knowledge_id in self._memory_indexed_knowledge:
            return
        content = f"{promoted.title}. {promoted.excerpt}"
        memory = MemoryItem(
            id=f"memory-{promoted.knowledge_id}",
            source_identity=promoted.provenance.source_record_id,
            content=content,
            memory_type=MemoryType.DECISION,
            importance=0.95,
            metadata={
                "knowledge_id": promoted.knowledge_id,
                "promotion_candidate_id": promoted.candidate_id,
                "source_record_id": promoted.provenance.source_record_id,
                "promotion_receipt_id": promoted.provenance.receipt_id,
                "intelligence": {
                    "confidence": 0.8,
                    "confidence_reason": (
                        "derived from governance-approved promoted evidence and preserved provenance"
                    ),
                },
            },
        )
        result = self._memory_runtime.store(memory)
        if not result.pipeline.stored:
            raise RuntimeError("promoted knowledge failed semantic indexing")
        self._memory_indexed_knowledge.add(promoted.knowledge_id)

    def reject_latest_candidate(self, reason: str = "human_review_rejected") -> None:
        if self._canonical_runtime_enabled:
            for staged in reversed(self._staged_submissions):
                if staged.governance_state == "review_pending":
                    if self._runtime_client is None:
                        raise RuntimeError("canonical_runtime_client_unavailable")
                    if staged.candidate_id is None:
                        raise RuntimeError("canonical_runtime_candidate_id_missing")
                    response = self._runtime_client.reject_admission(
                        candidate_id=staged.candidate_id,
                        reason=reason,
                        workspace_mode=self._workspace_mode.value,
                        organization_id=self._organization_id,
                    )
                    if response.get("state") != "rejected":
                        raise RuntimeError("canonical_runtime_rejection_failed")
                    staged.governance_state = "rejected"
                    staged.reason = reason
                    self._persist_canonical_submissions()
                    self._record_governance_event(
                        subject_id=staged.submission_id,
                        action="governance.rejected",
                        before_state="review_pending",
                        after_state="rejected",
                        reason=reason,
                        actor="knowledge-reviewer",
                        occurred_at=_now(),
                    )
                    return
            return
        candidate = self._latest_review_candidate()
        if candidate is None:
            return
        reviewed_at = _now()
        try:
            self._bridge.promote_candidate(
                candidate_id=candidate.candidate_id,
                reviewer_id="knowledge-reviewer",
                rationale=reason,
                approved=False,
                title=f"Rejected candidate from {candidate.source_record_id}",
                promoted_at=reviewed_at,
            )
        except Gate2ReviewRejected:
            pass
        for staged in self._staged_submissions:
            if staged.candidate_id == candidate.candidate_id:
                staged.governance_state = "rejected"
                staged.reason = reason
                self._record_governance_event(
                    subject_id=staged.submission_id,
                    action="governance.rejected",
                    before_state="review_pending",
                    after_state="rejected",
                    reason=reason,
                    actor="knowledge-reviewer",
                    occurred_at=reviewed_at,
                )
                break

    def ask_question(self, question: str) -> None:
        text = (question or "").strip()
        if not text:
            raise ValueError("question cannot be empty")
        self._last_question = text
        if self._canonical_runtime_enabled:
            self._sequence += 1
            trace_id = f"corr-ask-{self._sequence}"
            asked_at = _now()
            if self._runtime_client is None:
                raise RuntimeError("canonical_runtime_client_unavailable")
            response = self._runtime_client.ask_question(
                question=text,
                workspace_mode=self._workspace_mode.value,
                organization_id=self._organization_id,
            )
            selected_count = 0
            source_ids: list[str] = []
            citations = response.get("citations")
            candidate_count = len(citations) if isinstance(citations, list) else 0

            # The interaction gateway already retrieved and filtered the governed
            # evidence used for generation. Reuse its citations so a completed
            # answer is not held open by a second semantic-memory request.
            if isinstance(citations, list):
                for citation in citations:
                    if not isinstance(citation, dict):
                        continue
                    if citation.get("organization_id") != self._organization_id:
                        continue
                    if citation.get("workspace_mode") != self._workspace_mode.value:
                        continue
                    source_record_id = citation.get("source_record_id")
                    if isinstance(source_record_id, str) and source_record_id.strip():
                        source_ids.append(source_record_id.strip())
                        selected_count += 1

            # Retain compatibility with interaction responses that predate
            # citations, while avoiding the redundant call for current responses.
            if selected_count == 0 and not isinstance(citations, list):
                context = self._runtime_client.memory_context(
                    question=text,
                    workspace_mode=self._workspace_mode.value,
                    organization_id=self._organization_id,
                )
                memories = context.get("memories")
                candidate_count = len(memories) if isinstance(memories, list) else 0
                if isinstance(memories, list):
                    for memory_entry in memories:
                        if not isinstance(memory_entry, dict):
                            continue
                        metadata = memory_entry.get("metadata")
                        if not isinstance(metadata, dict):
                            continue
                        if metadata.get("organization_id") != self._organization_id:
                            continue
                        if metadata.get("workspace_mode") != self._workspace_mode.value:
                            continue
                        if metadata.get("governance_state") != "approved":
                            continue
                        source_record_id = metadata.get("source_record_id")
                        if (
                            not isinstance(source_record_id, str)
                            or not source_record_id.strip()
                        ):
                            source_record_id = "runtime-source"
                        source_ids.append(source_record_id)
                        selected_count += 1

            answer_state = str(response.get("state", "insufficient")).strip().lower()
            statement = _normalize_runtime_statement(response.get("statement"))
            if answer_state == "grounded" and statement:
                self._last_answer = _ExternalAskAnswer(
                    state=AnswerState.GROUNDED,
                    statement=statement,
                )
            else:
                self._last_answer = _ExternalAskAnswer(
                    state=AnswerState.INSUFFICIENT_EVIDENCE,
                    statement=None,
                )
            self._last_semantic_candidates = ()
            self._last_question_result = _QuestionRuntimeResult(
                trace_id=str(response.get("trace_id", "")).strip() or trace_id,
                asked_at=asked_at,
                candidate_count=candidate_count,
                selected_count=selected_count,
                stale_count=0,
                conflicting_sources=tuple(sorted(set(source_ids))),
                recommendation=(
                    str(response.get("recommended_decision", "")).strip()
                    or self._recommended_decision(
                        selected_count=selected_count,
                        stale_count=0,
                    )
                ),
                insufficient_reason=(
                    None
                    if answer_state == "grounded"
                    else str(response.get("reason", "")).strip()
                    or "No governed answer returned from canonical interaction runtime."
                ),
            )
            return

        self._sequence += 1
        asked_at = _now()
        trace_id = f"corr-ask-{self._sequence}"
        self._last_answer = self._bridge.ask(
            correlation_id=trace_id,
            question_id=f"q-{self._sequence}",
            question=text,
            consumer_id="executive-consumer",
            intended_use="executive_question_answering",
            asked_at=asked_at,
        )
        candidates = tuple(self._memory_runtime.context(text, limit=5))
        self._last_semantic_candidates = candidates
        selected = tuple(
            candidate
            for candidate in candidates
            if candidate.signals.lifecycle_state is MemoryLifecycleState.ACTIVE
        )
        stale_count = sum(
            1
            for candidate in candidates
            if candidate.signals.lifecycle_state
            in {MemoryLifecycleState.SUPERSEDED, MemoryLifecycleState.ARCHIVED}
        )
        conflicting_sources = tuple(
            sorted(
                {
                    self._candidate_source_identity(candidate)
                    for candidate in selected
                    if self._candidate_source_identity(candidate)
                }
            )
        )
        recommendation = self._recommended_decision(
            selected_count=len(selected),
            stale_count=stale_count,
        )
        insufficient_reason = None
        if not selected:
            insufficient_reason = (
                "No active promoted knowledge matched this executive question."
            )
        self._last_question_result = _QuestionRuntimeResult(
            trace_id=trace_id,
            asked_at=asked_at,
            candidate_count=len(candidates),
            selected_count=len(selected),
            stale_count=stale_count,
            conflicting_sources=conflicting_sources,
            recommendation=recommendation,
            insufficient_reason=insufficient_reason,
        )

    @staticmethod
    def _candidate_source_identity(candidate: RetrievalCandidate) -> str:
        metadata = candidate.metadata.get("metadata")
        if isinstance(metadata, dict):
            source_record_id = metadata.get("source_record_id")
            if isinstance(source_record_id, str) and source_record_id.strip():
                return source_record_id
        source_identity = candidate.metadata.get("source_identity")
        if isinstance(source_identity, str) and source_identity.strip():
            return source_identity
        if candidate.memory_id is not None:
            return candidate.memory_id
        return "unknown-source"

    @staticmethod
    def _recommended_decision(*, selected_count: int, stale_count: int) -> str:
        if selected_count == 0:
            return "Request additional governed evidence before making this decision."
        if stale_count > 0:
            return (
                "Proceed only after a human reviewer confirms stale evidence does not "
                "change the executive decision."
            )
        return "Proceed with human governance review of this evidence-backed recommendation."

    def briefing(self) -> ExecutiveBriefing:
        assembled_at = _now()
        workspace_records = self._workspace_records()
        activities = self._activities()
        items = self._items(assembled_at, workspace_records)
        coverage = self._coverage(items, workspace_records)
        summary_counts = derive_summary_counts(items, activities, assembled_at)
        ask_responses = self._ask_responses(workspace_records)
        limitations = [
            "Every dashboard and module surface is assembled from governed runtime records.",
            "Demonstration route remains available as a runtime-guided operating mode.",
            f"Semantic retrieval mode: {self._memory_runtime_mode}.",
        ]
        if self._canonical_runtime_enabled:
            limitations.append(
                "Operational data is consumed from canonical runtime services; Executive Shell does not own admission, memory, or model infrastructure."
            )
        if self._memory_runtime_issue is not None:
            limitations.append(
                "Qdrant or embedding runtime was unavailable, so local governed semantic fallback is active."
            )
        return ExecutiveBriefing(
            briefing_id="demo-governed-runtime-briefing",
            scenario_id=ALLOWLISTED_SCENARIO_ID,
            scenario_label="Governed runtime view: Executive Operational Shell",
            state=BriefingState.READY,
            assembled_at=assembled_at,
            coverage=coverage,
            items=items,
            workspace_records=workspace_records,
            activities=activities,
            ask_responses=ask_responses,
            summary_counts=summary_counts,
            limitations=tuple(limitations),
        )

    def _workspace_state_for_submission(self, submission: _StagedSubmission) -> WorkspaceState:
        mapping = {
            "review_pending": WorkspaceState.REVIEW_PENDING,
            "approved": WorkspaceState.ELIGIBLE,
            "rejected": WorkspaceState.REVIEW_REJECTED,
            "needs_evidence": WorkspaceState.HELD,
            "failed": WorkspaceState.PROCESSING_FAILED,
        }
        return mapping.get(submission.governance_state, WorkspaceState.RECEIVED)

    def _workspace_records(self) -> tuple[WorkspaceRecord, ...]:
        records: list[WorkspaceRecord] = []
        if self._canonical_runtime_enabled and self._runtime_client is not None:
            try:
                self._runtime_health = self._runtime_client.runtime_health()
            except RuntimeError as error:
                self._runtime_health = _unavailable_runtime_health(
                    detail=f"health_check_failed:{error}"
                )
            for status in self._runtime_health:
                records.append(
                    WorkspaceRecord(
                        record_id=_safe_demo_id("runtime", status.service),
                        kind=WorkspaceKind.LINEAGE,
                        title=f"Runtime service {status.service}",
                        state=(
                            WorkspaceState.READY
                            if status.state == "ready"
                            else WorkspaceState.UNAVAILABLE
                        ),
                        source_references=(),
                        last_changed_at=status.observed_at,
                        eligible_for_briefing=False,
                        limitations=(
                            f"Runtime status: {status.state}.",
                            f"Detail: {status.detail}.",
                        ),
                    )
                )
        for submission in self._staged_submissions:
            source = SourceReference(
                source_id=_safe_demo_id("src", submission.source_record_id),
                label=f"Source record {submission.source_record_id}",
                evidence_classification=EvidenceClassification.REPORTED_FACT,
                authority_scope="Governed admission and review boundary",
                observed_at=submission.admitted_at,
            )
            state = self._workspace_state_for_submission(submission)
            if state is WorkspaceState.ELIGIBLE:
                kind = WorkspaceKind.KNOWLEDGE_OBJECT
            elif state is WorkspaceState.PROCESSING_FAILED:
                kind = WorkspaceKind.DOCUMENT
            else:
                kind = WorkspaceKind.REVIEW
            records.append(
                WorkspaceRecord(
                    record_id=_safe_demo_id("submission", submission.submission_id),
                    kind=kind,
                    title=(
                        f"{submission.file_name} ({submission.media_type}, "
                        f"{submission.byte_count} bytes)"
                    ),
                    state=state,
                    source_references=(source,),
                    last_changed_at=submission.admitted_at,
                    eligible_for_briefing=state is WorkspaceState.ELIGIBLE,
                    limitations=(
                        f"Governance state: {submission.governance_state}.",
                        f"Reason: {submission.reason}.",
                        f"Content hash: {submission.digest_hex}.",
                    ),
                )
            )
        if self._bridge is not None:
            promoted_by_source: dict[str, list[PromotedKnowledge]] = {}
            for promoted in self._bridge._promoted.values():
                promoted_by_source.setdefault(
                    promoted.provenance.source_record_id, []
                ).append(promoted)
            for source_record_id, promoted_group in promoted_by_source.items():
                promoted_group.sort(key=lambda entry: entry.promoted_at, reverse=True)
                for position, promoted in enumerate(promoted_group):
                    state = (
                        WorkspaceState.ELIGIBLE
                        if position == 0
                        else WorkspaceState.SUPERSEDED
                    )
                    source_reference = SourceReference(
                        source_id=_safe_demo_id("src", source_record_id),
                        label=f"Promoted evidence {source_record_id}",
                        evidence_classification=EvidenceClassification.VERIFIED_FACT,
                        authority_scope="Governed promotion and semantic memory boundary",
                        observed_at=promoted.promoted_at,
                    )
                    records.append(
                        WorkspaceRecord(
                            record_id=_safe_demo_id("knowledge", promoted.knowledge_id),
                            kind=WorkspaceKind.KNOWLEDGE_OBJECT,
                            title=promoted.title,
                            state=state,
                            source_references=(source_reference,),
                            last_changed_at=promoted.promoted_at,
                            eligible_for_briefing=state is WorkspaceState.ELIGIBLE,
                            limitations=(
                                f"Lifecycle state: {'active' if state is WorkspaceState.ELIGIBLE else 'superseded'}.",
                                f"Admission attempt: {promoted.provenance.admission_attempt_id}.",
                                f"Receipt ID: {promoted.provenance.receipt_id}.",
                            ),
                        )
                    )
                    records.append(
                        WorkspaceRecord(
                            record_id=_safe_demo_id("lineage", promoted.knowledge_id),
                            kind=WorkspaceKind.LINEAGE,
                            title=f"Lineage chain for {promoted.knowledge_id}",
                            state=WorkspaceState.READY,
                            source_references=(source_reference,),
                            last_changed_at=promoted.promoted_at,
                            eligible_for_briefing=False,
                            limitations=(
                                f"Object ID: {promoted.provenance.object_id}.",
                                f"Content digest: {promoted.provenance.content_digest_hex}.",
                            ),
                        )
                    )
        if self._repository is not None:
            for custody in self._repository.list_active():
                source = SourceReference(
                    source_id=_safe_demo_id("src", custody.object_id),
                    label=f"Custody object {custody.object_id}",
                    evidence_classification=EvidenceClassification.REPORTED_FACT,
                    authority_scope="Governed encrypted custody boundary",
                    observed_at=custody.created_at,
                )
                records.append(
                    WorkspaceRecord(
                        record_id=_safe_demo_id("document", custody.object_id),
                        kind=WorkspaceKind.DOCUMENT,
                        title=f"Custody object {custody.object_id}",
                        state=WorkspaceState.QUARANTINED,
                        source_references=(source,),
                        last_changed_at=custody.created_at,
                        eligible_for_briefing=False,
                        limitations=(
                            "Custody record is encrypted and tracked with retention deadlines.",
                            f"Retention deadline: {custody.retention_deadline.isoformat()}",
                        ),
                    )
                )
        records.sort(key=lambda record: record.record_id)
        return tuple(records)

    def _activities(self) -> tuple[ActivityEntry, ...]:
        activities: list[ActivityEntry] = []
        if self._bridge is not None:
            for index, event in enumerate(self._bridge.audit_history(), start=1):
                if event.event_kind.startswith("admission"):
                    kind = ActivityKind.EVIDENCE_ADDED
                    state = WorkspaceState.REVIEW_PENDING
                elif event.event_kind.startswith("promotion"):
                    kind = ActivityKind.REVIEW_STATE_CHANGED
                    state = (
                        WorkspaceState.REVIEW_APPROVED
                        if "approved" in event.event_kind
                        else WorkspaceState.REVIEW_REJECTED
                    )
                elif event.event_kind.startswith("answer"):
                    kind = ActivityKind.KNOWLEDGE_STATUS_CHANGED
                    state = WorkspaceState.READY
                else:
                    kind = ActivityKind.LINEAGE_RECORDED
                    state = WorkspaceState.READY
                activities.append(
                    ActivityEntry(
                        activity_id=_safe_demo_id("act", f"{event.event_id}-{index}"),
                        kind=kind,
                        summary=(
                            f"Runtime audit event {event.event_kind} trace {event.correlation_id} "
                            f"subject {event.subject_id} reason {event.reason_code} "
                            f"hash {event.event_hash_hex}."
                        ),
                        occurred_at=event.recorded_at,
                        actor_label="Governed Runtime",
                        source_references=(),
                        result_state=state,
                    )
                )
        elif self._runtime_health:
            for index, status in enumerate(self._runtime_health, start=1):
                activities.append(
                    ActivityEntry(
                        activity_id=_safe_demo_id("runtime", f"{status.service}-{index}"),
                        kind=ActivityKind.KNOWLEDGE_STATUS_CHANGED,
                        summary=(
                            f"Canonical runtime service {status.service} reported "
                            f"{status.state} ({status.detail})."
                        ),
                        occurred_at=status.observed_at,
                        actor_label="Canonical Runtime",
                        source_references=(),
                        result_state=(
                            WorkspaceState.READY
                            if status.state == "ready"
                            else WorkspaceState.HELD
                        ),
                    )
                )
        for index, event in enumerate(self._governance_events, start=1):
            if event.after_state in {"approved", "review_pending"}:
                kind = ActivityKind.REVIEW_STATE_CHANGED
                state = (
                    WorkspaceState.REVIEW_APPROVED
                    if event.after_state == "approved"
                    else WorkspaceState.REVIEW_PENDING
                )
            elif event.after_state in {"rejected", "needs_evidence"}:
                kind = ActivityKind.REVIEW_STATE_CHANGED
                state = (
                    WorkspaceState.REVIEW_REJECTED
                    if event.after_state == "rejected"
                    else WorkspaceState.HELD
                )
            else:
                kind = ActivityKind.EVIDENCE_ADDED
                state = WorkspaceState.RECEIVED
            activities.append(
                ActivityEntry(
                    activity_id=_safe_demo_id("gov", f"{event.subject_id}-{index}"),
                    kind=kind,
                    summary=(
                        f"Governance transition trace {event.subject_id} from "
                        f"{event.before_state} to {event.after_state} with reason {event.reason}."
                    ),
                    occurred_at=event.occurred_at,
                    actor_label=event.actor,
                    source_references=(),
                    result_state=state,
                )
            )
        activities.sort(key=lambda entry: (entry.occurred_at, entry.activity_id))
        return tuple(activities)

    def _base_reference(
        self,
        workspace_records: tuple[WorkspaceRecord, ...],
        assembled_at: datetime,
    ) -> SourceReference:
        if workspace_records and workspace_records[0].source_references:
            return workspace_records[0].source_references[0]
        return SourceReference(
            source_id="demo-src-runtime",
            label="Runtime control reference",
            evidence_classification=EvidenceClassification.REPORTED_FACT,
            authority_scope="Governed runtime telemetry boundary",
            observed_at=assembled_at,
        )

    def _item(
        self,
        *,
        item_id: str,
        section: BriefingSection,
        display_order: int,
        title: str,
        statement: str,
        classification: EvidenceClassification,
        references: tuple[SourceReference, ...],
        observed_at: datetime | None,
        assembled_at: datetime,
        uncertainty: UncertaintyState,
        uncertainty_explanation: str,
        limitations: tuple[str, ...],
        knowledge_kind: KnowledgeKind | None = None,
        next_kind: NextItemKind | None = None,
        next_context: NextContext | None = None,
        priority_basis: str | None = None,
        decision_owner: str | None = None,
        authority_requirement: str | None = None,
        permitted_next_step: PermittedNextStep | None = None,
        related_item_ids: tuple[str, ...] = (),
    ) -> BriefingItem:
        freshness = derive_freshness(observed_at, assembled_at)
        return BriefingItem(
            item_id=item_id,
            section=section,
            display_order=display_order,
            title=title,
            statement=statement,
            evidence_classification=classification,
            assembled_at=assembled_at,
            freshness=freshness,
            evidence_basis="Derived from governed runtime records in this session.",
            uncertainty=uncertainty,
            uncertainty_explanation=uncertainty_explanation,
            limitations=limitations,
            source_references=references,
            source_observed_at=observed_at,
            transformation_id=(
                _safe_demo_id("transform", item_id)
                if classification is EvidenceClassification.DERIVED_SUMMARY
                else None
            ),
            knowledge_kind=knowledge_kind,
            next_kind=next_kind,
            next_context=next_context,
            priority_basis=priority_basis,
            decision_owner=decision_owner,
            authority_requirement=authority_requirement,
            permitted_next_step=permitted_next_step,
            related_item_ids=related_item_ids,
        )

    def _items(
        self,
        assembled_at: datetime,
        workspace_records: tuple[WorkspaceRecord, ...],
    ) -> tuple[BriefingItem, ...]:
        approved = [
            record
            for record in workspace_records
            if record.state is WorkspaceState.ELIGIBLE
        ]
        pending = [
            record
            for record in workspace_records
            if record.state is WorkspaceState.REVIEW_PENDING
        ]
        rejected = [
            record
            for record in workspace_records
            if record.state is WorkspaceState.REVIEW_REJECTED
        ]
        held = [
            record for record in workspace_records if record.state is WorkspaceState.HELD
        ]
        base_reference = self._base_reference(workspace_records, assembled_at)
        observed_at = workspace_records[-1].last_changed_at if workspace_records else assembled_at

        happening = self._item(
            item_id="demo-item-happening-runtime-admissions",
            section=BriefingSection.HAPPENING,
            display_order=1,
            title="Governed admissions observed",
            statement=(
                f"{len(workspace_records)} governed workspace records are available "
                "for lifecycle and review tracking."
            ),
            classification=EvidenceClassification.DERIVED_SUMMARY,
            references=(base_reference,),
            observed_at=observed_at,
            assembled_at=assembled_at,
            uncertainty=UncertaintyState.BOUNDED,
            uncertainty_explanation=(
                "Counts are bounded to records preserved in the current runtime."
            ),
            limitations=("Runtime session scope only.",),
        )

        attention_item_id = "demo-item-attention-review-queue"
        next_item_id = "demo-item-next-governance-decision"

        attention = self._item(
            item_id=attention_item_id,
            section=BriefingSection.ATTENTION,
            display_order=1,
            title="Governance review queue",
            statement=(
                f"{len(pending)} records require review, {len(held)} require evidence, "
                f"and {len(rejected)} are rejected."
            ),
            classification=EvidenceClassification.REPORTED_FACT,
            references=(base_reference,),
            observed_at=observed_at,
            assembled_at=assembled_at,
            uncertainty=UncertaintyState.INCOMPLETE if held else UncertaintyState.BOUNDED,
            uncertainty_explanation=(
                "Queue state is complete for this runtime session; held records require more evidence."
                if held
                else "Queue state is complete for this runtime session."
            ),
            limitations=("Human review remains required before promotion.",),
            priority_basis="Governance queue depth and held records.",
            decision_owner="Knowledge reviewer",
            authority_requirement="Human governance approval required for promotion.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
            related_item_ids=(next_item_id,),
        )

        knowledge_statement = (
            f"{len(approved)} knowledge objects are eligible for executive retrieval."
            if approved
            else "No approved knowledge objects are currently eligible for retrieval."
        )
        know = self._item(
            item_id="demo-item-know-knowledge-state",
            section=BriefingSection.KNOW,
            display_order=1,
            title="Knowledge object lifecycle",
            statement=knowledge_statement,
            classification=(
                EvidenceClassification.REPORTED_FACT
                if approved
                else EvidenceClassification.OPEN_QUESTION
            ),
            references=(base_reference,) if approved else (),
            observed_at=observed_at,
            assembled_at=assembled_at,
            uncertainty=UncertaintyState.BOUNDED if approved else UncertaintyState.INCOMPLETE,
            uncertainty_explanation=(
                "Eligible objects are governed and provenance-linked."
                if approved
                else "Executive retrieval remains insufficient until governance approves evidence."
            ),
            limitations=("Lifecycle and eligibility are governed runtime attributes.",),
            knowledge_kind=(
                KnowledgeKind.MATERIAL_CHANGE if approved else KnowledgeKind.KNOWLEDGE_GAP
            ),
        )

        next_item = self._item(
            item_id=next_item_id,
            section=BriefingSection.NEXT,
            display_order=1,
            title="Next governed decision",
            statement=(
                "Review pending records and either approve or reject promotion "
                "before relying on executive answers."
            ),
            classification=EvidenceClassification.REPORTED_FACT,
            references=(base_reference,),
            observed_at=observed_at,
            assembled_at=assembled_at,
            uncertainty=UncertaintyState.BOUNDED,
            uncertainty_explanation="The next action follows explicit governance workflow requirements.",
            limitations=("No autonomous approval is permitted.",),
            next_kind=NextItemKind.DECISION_REQUIRED,
            next_context=NextContext.DECISION_REQUEST,
            priority_basis="Promotion eligibility depends on explicit review outcome.",
            decision_owner="Knowledge reviewer",
            authority_requirement="Human authority gate required for every promotion decision.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        )

        return (happening, attention, know, next_item)

    def _coverage(
        self,
        items: tuple[BriefingItem, ...],
        workspace_records: tuple[WorkspaceRecord, ...],
    ) -> CoverageSummary:
        approved = sum(
            1 for record in workspace_records if record.state is WorkspaceState.ELIGIBLE
        )
        pending = sum(
            1
            for record in workspace_records
            if record.state is WorkspaceState.REVIEW_PENDING
        )
        held = sum(
            1 for record in workspace_records if record.state is WorkspaceState.HELD
        )
        rejected = sum(
            1
            for record in workspace_records
            if record.state is WorkspaceState.REVIEW_REJECTED
        )
        covered = _sorted_unique(
            [
                "admission custody",
                "governance transitions",
                "knowledge promotion",
                "executive retrieval",
                "audit lineage",
            ]
        )
        missing = _sorted_unique(
            []
            if approved > 0
            else [
                "approved knowledge objects",
                "grounded multi-source evidence set",
            ]
        )
        conflicting = _sorted_unique(
            ["duplicate submissions"]
            if rejected > 0
            else []
        )
        if self._last_question_result and self._last_question_result.conflicting_sources:
            conflicting = _sorted_unique(
                list(conflicting)
                + [
                    f"executive retrieval source variance: {source}"
                    for source in self._last_question_result.conflicting_sources
                ]
            )
        stale = _sorted_unique([])
        if self._last_question_result and self._last_question_result.stale_count > 0:
            stale = _sorted_unique(
                [f"stale or superseded evidence: {self._last_question_result.stale_count}"]
            )
        held_subjects = _sorted_unique(
            ["needs evidence queue"] if held > 0 else []
        )
        return CoverageSummary(
            scope_statement=(
                f"Runtime scope includes {len(workspace_records)} records with "
                f"{pending} pending reviews and {approved} approved knowledge objects."
            ),
            covered_subjects=covered,
            missing_subjects=missing,
            conflicting_subjects=conflicting,
            stale_subjects=stale,
            held_subjects=held_subjects,
            eligible_item_count=len(items),
            source_reference_count=len(unique_source_references(items)),
            limitations=(
                "Coverage represents current runtime session records only.",
                "Cross-session continuity requires persistent runtime deployment.",
                f"Semantic runtime mode is {self._memory_runtime_mode}.",
            ),
        )

    def _ask_responses(
        self,
        workspace_records: tuple[WorkspaceRecord, ...],
    ) -> tuple[AskResponse, ...]:
        approved = any(
            record.state is WorkspaceState.ELIGIBLE for record in workspace_records
        )
        source_refs: tuple[SourceReference, ...] = ()
        statement = None
        selected_candidates = tuple(
            candidate
            for candidate in self._last_semantic_candidates
            if candidate.signals.lifecycle_state is MemoryLifecycleState.ACTIVE
        )
        if selected_candidates:
            source_refs = tuple(
                SourceReference(
                    source_id=_safe_demo_id(
                        "src", self._candidate_source_identity(candidate)
                    ),
                    label=f"Evidence citation {self._candidate_source_identity(candidate)}",
                    evidence_classification=EvidenceClassification.VERIFIED_FACT,
                    authority_scope="Governed semantic retrieval and provenance boundary",
                    observed_at=candidate.signals.created_at,
                )
                for candidate in selected_candidates
            )
        elif self._last_question_result is not None and self._last_question_result.conflicting_sources:
            source_refs = tuple(
                SourceReference(
                    source_id=_safe_demo_id("src", source_id),
                    label=f"Evidence citation {source_id}",
                    evidence_classification=EvidenceClassification.REPORTED_FACT,
                    authority_scope="Canonical retrieval evidence boundary",
                    observed_at=self._last_question_result.asked_at,
                )
                for source_id in self._last_question_result.conflicting_sources
            )
        if (
            self._last_answer is not None
            and self._last_answer.state is AnswerState.GROUNDED
            and self._last_answer.statement is not None
            and (
                selected_candidates
                or (
                    self._last_question_result is not None
                    and self._last_question_result.selected_count > 0
                )
            )
        ):
            grounded_state = AskState.GROUNDED
            top_memory_id = (
                selected_candidates[0].memory_id
                if selected_candidates
                else (
                    self._last_question_result.conflicting_sources[0]
                    if self._last_question_result is not None
                    and self._last_question_result.conflicting_sources
                    else "unidentified-memory"
                )
            )
            statement = (
                f"{self._last_answer.statement} Recommended human decision: "
                f"{self._recommended_decision(selected_count=(len(selected_candidates) if selected_candidates else (self._last_question_result.selected_count if self._last_question_result else 0)), stale_count=(self._last_question_result.stale_count if self._last_question_result else 0))} "
                f"Top evidence memory {top_memory_id}."
            )
            uncertainty = (
                UncertaintyState.CONFLICTING
                if self._last_question_result
                and len(self._last_question_result.conflicting_sources) > 1
                else (
                    UncertaintyState.INCOMPLETE
                    if self._last_question_result and self._last_question_result.stale_count > 0
                    else UncertaintyState.BOUNDED
                )
            )
        else:
            grounded_state = AskState.INSUFFICIENT
            uncertainty = UncertaintyState.INCOMPLETE
            statement = None
        candidate_count = (
            self._last_question_result.candidate_count
            if self._last_question_result is not None
            else 0
        )
        selected_count = (
            self._last_question_result.selected_count
            if self._last_question_result is not None
            else 0
        )
        stale_count = (
            self._last_question_result.stale_count
            if self._last_question_result is not None
            else 0
        )
        trace_id = (
            self._last_question_result.trace_id
            if self._last_question_result is not None
            else "not-recorded"
        )
        recommendation = (
            self._last_question_result.recommendation
            if self._last_question_result is not None
            else "Request additional governed evidence before making this decision."
        )
        insufficiency_reason = (
            self._last_question_result.insufficient_reason
            if self._last_question_result is not None
            and self._last_question_result.insufficient_reason is not None
            else "No governed answer is produced without approved evidence."
        )
        conflicting_sources = (
            ", ".join(self._last_question_result.conflicting_sources)
            if self._last_question_result is not None
            and self._last_question_result.conflicting_sources
            else "none"
        )
        grounded = AskResponse(
            question_id="grounded-priorities",
            question=self._last_question,
            state=grounded_state,
            statement=statement,
            source_references=source_refs,
            coverage_statement=(
                f"Audit trace {trace_id}; governed retrieval selected {selected_count} "
                f"active evidence records from {candidate_count} semantic candidates."
            ),
            uncertainty=uncertainty,
            uncertainty_explanation=(
                "Active promoted evidence is present and traceable."
                if grounded_state is AskState.GROUNDED
                else insufficiency_reason
            ),
            limitations=(
                "Answers are constrained to governed promotion and retrieval boundaries.",
                f"Freshness review flagged {stale_count} stale or superseded records.",
                f"Conflicting evidence sources: {conflicting_sources}.",
                f"Recommended human decision: {recommendation}",
                f"Semantic runtime mode: {self._memory_runtime_mode}.",
            ),
        )
        insufficient = AskResponse(
            question_id="insufficient-program-outcomes",
            question="What funded outcomes are still unverified?",
            state=AskState.INSUFFICIENT,
            statement=None,
            source_references=(),
            coverage_statement=(
                f"Audit trace {trace_id}; insufficient active governed evidence was "
                "retrieved for this question."
            ),
            uncertainty=UncertaintyState.INCOMPLETE,
            uncertainty_explanation=(
                "Additional approved evidence is required before a governed answer is available."
            ),
            limitations=(
                "Insufficient-evidence responses prevent fabricated executive conclusions.",
                "Submit additional governed evidence through Knowledge Manager admission and review.",
            ),
        )
        failed = AskResponse(
            question_id="failed-source-review",
            question="Why was one source denied promotion?",
            state=AskState.FAILED if not approved else AskState.INSUFFICIENT,
            statement=None,
            source_references=(),
            coverage_statement=(
                "Review outcomes are visible in governance and audit history."
            ),
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation=(
                "This prompt reports review posture without fabricating evidence."
            ),
            limitations=(
                "Use Knowledge Manager and Audit pages for detailed review rationale.",
            ),
        )
        return (grounded, insufficient, failed)


class OperationalWorkspaceProvider:
    """Workspace-aware provider that preserves shell UX across demo/dev/prod."""

    def __init__(self, runtime_root: Path) -> None:
        self._runtime_root = runtime_root
        self._runtime_root.mkdir(parents=True, exist_ok=True)
        self._workspace_state_path = self._runtime_root / "workspace-state.json"
        self._synthetic_provider = SyntheticBriefingProvider()
        self._governed_instances: dict[
            tuple[WorkspaceMode, str], GovernedRuntimeBriefingProvider
        ] = {}
        self._organizations = self._organization_profiles()
        self._recent_organization_ids: list[str] = ["demo-organization"]
        self._workspace_mode = WorkspaceMode.DEMONSTRATION
        self._organization_id = "demo-organization"
        self._load_state()

    @classmethod
    def create_default(cls) -> "OperationalWorkspaceProvider":
        configured_root = os.getenv("JEBEDIAH_RUNTIME_ROOT", "").strip()
        if configured_root:
            runtime_root = Path(configured_root).resolve()
        else:
            runtime_root = Path(tempfile.mkdtemp(prefix="bonsaai-workspace-runtime-"))
        return cls(runtime_root)

    def _organization_profiles(self) -> dict[str, OrganizationProfile]:
        return {
            "demo-organization": OrganizationProfile(
                organization_id="demo-organization",
                name="Demo Organization",
                description="Synthetic organization for demonstrations and training.",
                theme="Demonstration",
                logo="DEMO",
                knowledge_root="synthetic demo knowledge root",
                runtime_root="synthetic demo runtime root",
                governance_policy="Synthetic demonstration governance policy",
            ),
            "back-pack-kidz": OrganizationProfile(
                organization_id="back-pack-kidz",
                name="Back Pack Kidz",
                description="Operational workspace for the Back Pack Kidz organization.",
                theme="Community Operations",
                logo="BPK",
                knowledge_root="back pack kidz governed knowledge root",
                runtime_root="back pack kidz governed runtime root",
                governance_policy="Back Pack Kidz governed operational policy",
            ),
            "virginia-b-andes": OrganizationProfile(
                organization_id="virginia-b-andes",
                name="Virginia B. Andes",
                description="Operational workspace for Virginia B. Andes governance records.",
                theme="Board Governance",
                logo="VBA",
                knowledge_root="virginia b andes governed knowledge root",
                runtime_root="virginia b andes governed runtime root",
                governance_policy="Virginia B. Andes governed policy",
            ),
        }

    def _default_workspace_from_env(self) -> WorkspaceMode:
        configured = (
            os.getenv("BONSAAI_WORKSPACE_MODE", "")
            or os.getenv("BONSAAI_DEFAULT_WORKSPACE", "")
        ).strip().lower()
        mapping = {
            WorkspaceMode.DEMONSTRATION.value: WorkspaceMode.DEMONSTRATION,
            WorkspaceMode.DEVELOPMENT.value: WorkspaceMode.DEVELOPMENT,
            WorkspaceMode.PRODUCTION.value: WorkspaceMode.PRODUCTION,
        }
        return mapping.get(configured, WorkspaceMode.DEMONSTRATION)

    def _default_organization_from_env(self) -> str:
        configured = os.getenv("BONSAAI_ORGANIZATION_ID", "").strip().lower()
        if configured in self._organizations:
            return configured
        return "demo-organization"

    def _load_state(self) -> None:
        self._workspace_mode = self._default_workspace_from_env()
        self._organization_id = self._default_organization_from_env()
        if not self._workspace_state_path.exists():
            return
        try:
            payload = json.loads(
                self._workspace_state_path.read_text(encoding="utf-8")
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return
        mode = str(payload.get("workspace_mode", "")).strip().lower()
        organization_id = str(payload.get("organization_id", "")).strip().lower()
        recent = payload.get("recent_organization_ids")
        if mode in {item.value for item in WorkspaceMode}:
            self._workspace_mode = WorkspaceMode(mode)
        if organization_id in self._organizations:
            self._organization_id = organization_id
        if isinstance(recent, list):
            normalized = [
                str(value).strip().lower()
                for value in recent
                if str(value).strip().lower() in self._organizations
            ]
            if normalized:
                self._recent_organization_ids = list(dict.fromkeys(normalized))
        self._remember_organization(self._organization_id)

    def _save_state(self) -> None:
        payload = {
            "workspace_mode": self._workspace_mode.value,
            "organization_id": self._organization_id,
            "recent_organization_ids": tuple(self._recent_organization_ids),
        }
        self._workspace_state_path.write_text(
            json.dumps(payload, sort_keys=True, indent=2),
            encoding="utf-8",
        )

    def _remember_organization(self, organization_id: str) -> None:
        if organization_id in self._recent_organization_ids:
            self._recent_organization_ids.remove(organization_id)
        self._recent_organization_ids.insert(0, organization_id)
        del self._recent_organization_ids[5:]

    def _governed_collection_name(self, organization_id: str, mode: WorkspaceMode) -> str:
        base = os.getenv("COLLECTION_NAME", "jebediah_memory").strip() or "jebediah_memory"
        suffix = organization_id.replace("-", "_")
        return f"{base}_{suffix}_{mode.value}"

    def _governed_provider(
        self, *, organization_id: str, mode: WorkspaceMode
    ) -> GovernedRuntimeBriefingProvider:
        key = (mode, organization_id)
        provider = self._governed_instances.get(key)
        if provider is not None:
            return provider
        runtime_directory = self._runtime_root / organization_id / mode.value
        runtime_directory.mkdir(parents=True, exist_ok=True)
        qdrant_enabled = (
            os.getenv("JEBEDIAH_QDRANT_RUNTIME", "").strip().lower()
            in {"1", "true", "yes"}
        )
        provider = GovernedRuntimeBriefingProvider(
            runtime_directory,
            qdrant_enabled=qdrant_enabled,
            collection_name=self._governed_collection_name(organization_id, mode),
            canonical_runtime=(
                os.getenv("BONSAAI_CANONICAL_RUNTIME", "").strip().lower()
                in {"1", "true", "yes"}
            ),
            organization_id=organization_id,
            workspace_mode=mode,
        )
        self._governed_instances[key] = provider
        return provider

    def _workspace_context(
        self,
        *,
        mode: WorkspaceMode,
        profile: OrganizationProfile,
        runtime_name: str,
        model_name: str,
    ) -> WorkspaceContext:
        banner_map = {
            WorkspaceMode.DEMONSTRATION: (
                "Demonstration Mode",
                WorkspaceBannerTone.BLUE,
            ),
            WorkspaceMode.DEVELOPMENT: (
                "Development Environment",
                WorkspaceBannerTone.ORANGE,
            ),
            WorkspaceMode.PRODUCTION: ("Production Workspace", WorkspaceBannerTone.GREEN),
        }
        banner_label, banner_tone = banner_map[mode]
        return WorkspaceContext(
            mode=mode,
            banner_label=banner_label,
            banner_tone=banner_tone,
            runtime_name=runtime_name,
            model_name=model_name,
            profile=profile,
            recent_organization_ids=tuple(self._recent_organization_ids),
            available_organization_ids=tuple(self._organizations.keys()),
            available_workspace_modes=(
                WorkspaceMode.DEMONSTRATION.value,
                WorkspaceMode.DEVELOPMENT.value,
                WorkspaceMode.PRODUCTION.value,
            ),
            diagnostics_enabled=mode is WorkspaceMode.DEVELOPMENT,
            demo_reset_available=mode is WorkspaceMode.DEMONSTRATION,
        )

    def briefing(self) -> ExecutiveBriefing:
        profile = self._organizations[self._organization_id]
        if self._workspace_mode is WorkspaceMode.DEMONSTRATION:
            briefing = self._synthetic_provider.briefing()
            context = self._workspace_context(
                mode=self._workspace_mode,
                profile=profile,
                runtime_name="Synthetic demonstration runtime",
                model_name="none",
            )
            return replace(
                briefing,
                scenario_label=f"{profile.name}: Demonstration workspace",
                workspace_context=context,
            )
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        briefing = provider.briefing()
        runtime_name = (
            "Canonical governed runtime (external services)"
            if provider.memory_runtime_mode == "external_canonical_runtime"
            else (
                "Governed runtime (Qdrant semantic retrieval)"
                if provider.memory_runtime_mode == "qdrant_semantic_runtime"
                else "Governed runtime (local semantic fallback)"
            )
        )
        context = self._workspace_context(
            mode=self._workspace_mode,
            profile=profile,
            runtime_name=runtime_name,
            model_name=os.getenv("EMBEDDING_MODEL", "nomic-embed-text:v1.5").strip()
            or "nomic-embed-text:v1.5",
        )
        scenario = (
            f"{profile.name}: Development governed workspace"
            if self._workspace_mode is WorkspaceMode.DEVELOPMENT
            else f"{profile.name}: Production governed workspace"
        )
        return replace(
            briefing,
            scenario_label=scenario,
            workspace_context=context,
        )

    def select_workspace(self, mode: str) -> None:
        normalized = (mode or "").strip().lower()
        mapping = {
            WorkspaceMode.DEMONSTRATION.value: WorkspaceMode.DEMONSTRATION,
            WorkspaceMode.DEVELOPMENT.value: WorkspaceMode.DEVELOPMENT,
            WorkspaceMode.PRODUCTION.value: WorkspaceMode.PRODUCTION,
        }
        selected = mapping.get(normalized)
        if selected is None:
            raise ValueError("unsupported_workspace_mode")
        self._workspace_mode = selected
        self._save_state()

    def select_organization(self, organization_id: str) -> None:
        normalized = (organization_id or "").strip().lower()
        if normalized not in self._organizations:
            raise ValueError("unsupported_organization")
        self._organization_id = normalized
        self._remember_organization(normalized)
        self._save_state()

    def reset_demo_workspace(self) -> None:
        self._synthetic_provider = SyntheticBriefingProvider()
        if self._workspace_mode is WorkspaceMode.DEMONSTRATION:
            self._save_state()

    def _require_governed_workspace(self) -> None:
        if self._workspace_mode is WorkspaceMode.DEMONSTRATION:
            raise RuntimeError("demonstration_workspace_disallows_live_runtime_mutation")

    def admit_submission(
        self,
        *,
        payload: bytes,
        source_record_id: str,
        file_name: str,
        media_type: str,
    ) -> dict[str, object]:
        self._require_governed_workspace()
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        return provider.admit_submission(
            payload=payload,
            source_record_id=source_record_id,
            file_name=file_name,
            media_type=media_type,
        )

    def admit_document(self, document_text: str, source_record_id: str) -> None:
        self._require_governed_workspace()
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        provider.admit_document(document_text, source_record_id)

    def promote_latest_candidate(self) -> None:
        self._require_governed_workspace()
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        provider.promote_latest_candidate()

    def reject_latest_candidate(self, reason: str = "human_review_rejected") -> None:
        self._require_governed_workspace()
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        provider.reject_latest_candidate(reason)

    def ask_question(self, question: str) -> None:
        self._require_governed_workspace()
        provider = self._governed_provider(
            organization_id=self._organization_id,
            mode=self._workspace_mode,
        )
        provider.ask_question(question)
