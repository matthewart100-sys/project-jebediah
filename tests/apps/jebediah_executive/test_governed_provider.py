from __future__ import annotations

import tempfile
from io import BytesIO
from pathlib import Path
import json
import urllib.error

import pytest

from collector.document_admission import DocumentFormat

from apps.jebediah_executive.governed_provider import (
    GovernedRuntimeBriefingProvider,
    OperationalWorkspaceProvider,
    _CanonicalRuntimeClient,
)
from apps.jebediah_executive.models import (
    AskState,
    WorkspaceKind,
    WorkspaceMode,
    WorkspaceState,
)


def _provider() -> GovernedRuntimeBriefingProvider:
    runtime_dir = Path(tempfile.mkdtemp(prefix="gov-provider-test-"))
    return GovernedRuntimeBriefingProvider(runtime_dir)


def test_governed_provider_starts_with_synthetic_defaults() -> None:
    provider = _provider()
    briefing = provider.briefing()
    assert briefing.scenario_id == "synthetic-nonprofit-demo-v1"
    assert any("governed runtime records" in item for item in briefing.limitations)


@pytest.mark.parametrize(
    ("file_name", "media_type", "expected"),
    [
        ("evidence.pdf", "application/pdf", DocumentFormat.PDF),
        (
            "evidence.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            DocumentFormat.DOCX,
        ),
        (
            "evidence.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            DocumentFormat.XLSX,
        ),
        (
            "evidence.pptx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            DocumentFormat.PPTX,
        ),
        ("evidence.csv", "text/csv", DocumentFormat.CSV),
        ("evidence.txt", "text/plain", DocumentFormat.TXT),
        ("evidence.md", "text/markdown", DocumentFormat.MARKDOWN),
        ("evidence.markdown", "text/plain", DocumentFormat.MARKDOWN),
    ],
)
def test_governed_provider_resolves_approved_document_formats(
    file_name: str,
    media_type: str,
    expected: DocumentFormat,
) -> None:
    assert _provider()._resolve_document_format(file_name, media_type) is expected


def test_governed_provider_rejects_extension_media_type_mismatch() -> None:
    with pytest.raises(ValueError, match="unsupported_document_format"):
        _provider()._resolve_document_format("evidence.xlsx", "application/pdf")


def test_governed_provider_admission_promotion_and_grounded_ask() -> None:
    provider = _provider()
    provider.admit_submission(
        payload=b"Leadership reconciled the final cash variance and approved closure.",
        source_record_id="source-record-009",
        file_name="board-update.txt",
        media_type="text/plain",
    )
    provider.promote_latest_candidate()
    provider.ask_question("What decision should leadership make next?")

    briefing = provider.briefing()
    assert any(record.kind is WorkspaceKind.DOCUMENT for record in briefing.workspace_records)
    assert any(
        record.state is WorkspaceState.ELIGIBLE for record in briefing.workspace_records
    )
    grounded = briefing.ask_response("grounded-priorities")
    assert grounded.state is AskState.GROUNDED
    assert grounded.statement is not None
    assert grounded.source_references
    assert any("answer.grounded" in activity.summary for activity in briefing.activities)


def test_governed_provider_returns_insufficient_when_no_promoted_knowledge() -> None:
    provider = _provider()
    provider.ask_question("What is the cash outlook?")
    briefing = provider.briefing()
    grounded = briefing.ask_response("grounded-priorities")
    assert grounded.state is AskState.INSUFFICIENT
    assert grounded.statement is None


def test_governed_provider_stages_image_as_needs_evidence() -> None:
    provider = _provider()
    provider.admit_submission(
        payload=b"\x89PNG\r\n\x1a\nsynthetic",
        source_record_id="source-record-100",
        file_name="scan.png",
        media_type="image/png",
    )
    briefing = provider.briefing()
    assert any(record.state is WorkspaceState.HELD for record in briefing.workspace_records)


def test_workspace_provider_defaults_to_demonstration_mode() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    briefing = provider.briefing()
    assert briefing.workspace_context.mode.value == "demonstration"
    assert briefing.workspace_context.banner_label == "Demonstration Mode"
    assert briefing.workspace_context.demo_reset_available is True


def test_workspace_provider_switches_modes_and_organizations() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    provider.select_organization("virginia-b-andes")
    provider.select_workspace("development")
    briefing = provider.briefing()
    assert briefing.workspace_context.mode.value == "development"
    assert briefing.workspace_context.profile.name == "Virginia B. Andes"

    provider.select_workspace("production")
    production = provider.briefing()
    assert production.workspace_context.mode.value == "production"
    assert production.workspace_context.banner_label == "Production Workspace"


def test_workspace_provider_blocks_live_mutation_in_demo_mode() -> None:
    runtime_dir = Path(tempfile.mkdtemp(prefix="workspace-provider-test-"))
    provider = OperationalWorkspaceProvider(runtime_dir)
    with pytest.raises(RuntimeError):
        provider.admit_document("Synthetic text", "source-record-001")


def test_governed_provider_canonical_runtime_mode_uses_external_services(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        method = request.get_method()
        if url.endswith(("/admission/submit", "/admission/promote", "/questions/ask")):
            assert request.get_header("Authorization") == "Bearer service-token"
        if url.endswith("/admission/submit") and method == "POST":
            return _FakeResponse(
                {
                    "state": "review_pending",
                    "candidate_id": "candidate-001",
                    "reason": "admitted",
                }
            )
        if url.endswith("/admission/promote") and method == "POST":
            return _FakeResponse(
                {
                    "state": "promoted",
                    "candidate_id": "candidate-001",
                    "knowledge_id": "memory-001",
                }
            )
        if url.endswith("/questions/ask") and method == "POST":
            return _FakeResponse(
                {
                    "state": "grounded",
                    "statement": "Leadership should prioritize grant closeout.",
                    "trace_id": "trace-001",
                    "recommended_decision": "Proceed with documented reviewer approval.",
                }
            )
        if url.endswith("/memory/context") and method == "POST":
            return _FakeResponse(
                {
                    "memories": [
                        {
                            "metadata": {
                                "source_record_id": "source-record-009",
                                "organization_id": "virginia-b-andes",
                                "workspace_mode": "production",
                                "governance_state": "approved",
                            }
                        },
                    ]
                }
            )
        if url.endswith("/health") or url.endswith("/healthz") or url.endswith("/api/tags"):
            return _FakeResponse({"status": "online"})
        raise AssertionError(f"unexpected request: {method} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    monkeypatch.setenv("BONSAAI_INTERACTION_SERVICE_TOKEN", "service-token")
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    provider.admit_submission(
        payload=b"Board approved governance closeout package.",
        source_record_id="source-record-009",
        file_name="board-update.txt",
        media_type="text/plain",
    )
    provider.promote_latest_candidate()
    provider.ask_question("What decision should leadership make next?")
    briefing = provider.briefing()
    grounded = briefing.ask_response("grounded-priorities")
    assert grounded.state is AskState.GROUNDED
    assert grounded.source_references
    assert any(
        record.record_id.startswith("demo-runtime-") for record in briefing.workspace_records
    )


def test_canonical_grounded_answer_does_not_repeat_memory_retrieval(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    requests: list[str] = []

    def _fake_urlopen(request, timeout=0):
        del timeout
        requests.append(request.full_url)
        if request.full_url.endswith("/questions/ask"):
            return _FakeResponse(
                {
                    "state": "grounded",
                    "statement": (
                        "The uploaded document contains the board packet.\n\n"
                        "It includes governed organizational evidence.\t"
                    ),
                    "trace_id": "trace-single-question-call",
                    "citations": [
                        {
                            "source_record_id": "source-uploaded-pdf",
                            "candidate_id": "candidate-uploaded-pdf",
                            "organization_id": "virginia-b-andes",
                            "workspace_mode": "production",
                        }
                    ],
                }
            )
        raise AssertionError(f"unexpected request: {request.full_url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider._CanonicalRuntimeClient.runtime_health",
        lambda self: (),
    )
    provider = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )

    provider.ask_question("What is contained in the uploaded document?")

    assert requests == ["http://jebediah-interaction:8001/questions/ask"]
    answer = provider.briefing().ask_response("grounded-priorities")
    assert answer.state is AskState.GROUNDED
    assert answer.statement is not None
    assert answer.statement.startswith(
        "The uploaded document contains the board packet. It includes governed "
        "organizational evidence."
    )
    assert all(ord(character) >= 32 for character in answer.statement)
    assert tuple(reference.source_id for reference in answer.source_references) == (
        "demo-src-source-uploaded-pdf",
    )


def test_canonical_question_timeout_uses_bounded_safe_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}

    def _timeout(request, timeout=0):
        observed["url"] = request.full_url
        observed["timeout"] = timeout
        raise TimeoutError("synthetic bounded timeout")

    monkeypatch.setenv("BONSAAI_QUESTION_TIMEOUT_SECONDS", "85")
    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _timeout,
    )
    client = _CanonicalRuntimeClient()

    with pytest.raises(RuntimeError, match="runtime_request_failed: interaction_question"):
        client.ask_question(
            question="What is contained in the uploaded document?",
            workspace_mode="production",
            organization_id="virginia-b-andes",
        )

    assert observed == {
        "url": "http://jebediah-interaction:8001/questions/ask",
        "timeout": 85,
    }


def test_canonical_http_error_does_not_expose_upstream_body(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    confidential_marker = "CONFIDENTIAL SYNTHETIC UPSTREAM DETAIL"

    def _http_error(_request, timeout=0):
        del timeout
        raise urllib.error.HTTPError(
            url="http://jebediah-interaction:8001/questions/ask",
            code=422,
            msg="synthetic error",
            hdrs=None,
            fp=BytesIO(confidential_marker.encode("utf-8")),
        )

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _http_error,
    )
    client = _CanonicalRuntimeClient()

    with pytest.raises(RuntimeError) as raised:
        client.ask_question(
            question="What is contained in the uploaded document?",
            workspace_mode="production",
            organization_id="virginia-b-andes",
        )

    captured = capsys.readouterr()
    assert str(raised.value) == (
        "runtime_request_failed: interaction_question: http_status_422"
    )
    assert confidential_marker not in str(raised.value)
    assert confidential_marker not in captured.out
    assert confidential_marker not in captured.err


def test_canonical_health_probes_use_short_rendering_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def read(self) -> bytes:
            return b'{"status":"online"}'

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    timeouts: list[int] = []

    def _fake_urlopen(_request, timeout=0):
        timeouts.append(timeout)
        return _FakeResponse()

    monkeypatch.setenv("BONSAAI_HEALTH_TIMEOUT_SECONDS", "2")
    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )

    statuses = _CanonicalRuntimeClient().runtime_health()

    assert len(statuses) == 4
    assert timeouts == [2, 2, 2, 2]


def test_canonical_pending_submission_survives_provider_restart(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    promotion_requests: list[dict[str, object]] = []

    def _fake_urlopen(request, timeout=0):
        del timeout
        if request.full_url.endswith("/admission/submit"):
            return _FakeResponse(
                {
                    "state": "review_pending",
                    "candidate_id": "candidate-restart-001",
                }
            )
        if request.full_url.endswith("/admission/promote"):
            promotion_requests.append(json.loads(request.data))
            return _FakeResponse(
                {
                    "state": "promoted",
                    "candidate_id": "candidate-restart-001",
                    "knowledge_id": "memory-restart-001",
                }
            )
        raise AssertionError(f"unexpected request: {request.full_url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    provider.admit_submission(
        payload=b"Restart-safe governed admission.",
        source_record_id="source-record-restart",
        file_name="restart.pdf",
        media_type="application/pdf",
    )

    restarted = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    restarted.promote_latest_candidate()

    assert promotion_requests == [
        {
            "candidate_id": "candidate-restart-001",
            "workspace_mode": "production",
            "organization_id": "virginia-b-andes",
        }
    ]
    restarted_again = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    restarted_again.promote_latest_candidate()
    assert len(promotion_requests) == 1


def test_canonical_rejection_is_recorded_by_interaction_service(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    requests: list[str] = []

    def _fake_urlopen(request, timeout=0):
        del timeout
        requests.append(request.full_url)
        if request.full_url.endswith("/admission/submit"):
            return _FakeResponse(
                {"state": "review_pending", "candidate_id": "candidate-reject-001"}
            )
        if request.full_url.endswith("/admission/reject"):
            assert json.loads(request.data)["reason"] == "evidence_insufficient"
            return _FakeResponse(
                {"state": "rejected", "candidate_id": "candidate-reject-001"}
            )
        raise AssertionError(f"unexpected request: {request.full_url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    provider.admit_submission(
        payload=b"Governed rejection candidate.",
        source_record_id="source-record-reject",
        file_name="reject.pdf",
        media_type="application/pdf",
    )
    provider.reject_latest_candidate("evidence_insufficient")

    assert requests[-1].endswith("/admission/reject")
    restarted = GovernedRuntimeBriefingProvider(
        tmp_path,
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    restarted.promote_latest_candidate()
    assert len(requests) == 2


def test_governed_provider_canonical_admission_failure_is_recorded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        method = request.get_method()
        if url.endswith("/admission/submit") and method == "POST":
            raise urllib.error.URLError("synthetic transport failure")
        if url.endswith("/health") or url.endswith("/healthz") or url.endswith("/api/tags"):
            return _FakeResponse({"status": "online"})
        raise AssertionError(f"unexpected request: {method} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-failure-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )

    provider.admit_submission(
        payload=b"Board packet upload content.",
        source_record_id="source-record-017",
        file_name="board-packet.pdf",
        media_type="application/pdf",
    )

    briefing = provider.briefing()
    assert any(
        record.kind is WorkspaceKind.DOCUMENT
        and record.state is WorkspaceState.PROCESSING_FAILED
        and "runtime_request_failed: interaction_admission"
        in " ".join(record.limitations)
        for record in briefing.workspace_records
    )


def test_governed_provider_excludes_other_workspace_runtime_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, payload: dict[str, object]) -> None:
            self._bytes = json.dumps(payload).encode("utf-8")

        def read(self) -> bytes:
            return self._bytes

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        if url.endswith("/questions/ask"):
            return _FakeResponse(
                {
                    "state": "grounded",
                    "statement": "Production-only statement.",
                    "trace_id": "trace-isolation",
                    "citations": [
                        {
                            "source_record_id": "source-production",
                            "candidate_id": "candidate-production",
                            "organization_id": "virginia-b-andes",
                            "workspace_mode": "production",
                        }
                    ],
                }
            )
        if url.endswith("/health") or url.endswith("/healthz") or url.endswith("/api/tags"):
            return _FakeResponse({"status": "online"})
        raise AssertionError(f"unexpected request: {request.get_method()} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-isolation-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.DEVELOPMENT,
    )

    provider.ask_question("What should leadership do next?")

    answer = provider.briefing().ask_response("grounded-priorities")
    assert answer.state is AskState.INSUFFICIENT
    assert answer.source_references == ()


def test_governed_provider_canonical_runtime_health_handles_non_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, body: bytes) -> None:
            self._body = body

        def read(self) -> bytes:
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        method = request.get_method()
        if method != "GET":
            raise AssertionError(f"unexpected request: {method} {url}")
        if url.endswith("/healthz"):
            return _FakeResponse(b"healthz check passed")
        if url.endswith("/api/tags"):
            return _FakeResponse(b"{\"models\":[]}")
        if url.endswith("/health"):
            return _FakeResponse(b"{\"status\":\"online\"}")
        raise AssertionError(f"unexpected request: {method} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-health-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    briefing = provider.briefing()
    runtime_records = [
        record for record in briefing.workspace_records if record.record_id.startswith("demo-runtime-")
    ]
    qdrant_records = [record for record in runtime_records if "qdrant" in record.title.lower()]
    assert qdrant_records
    assert all(record.state is WorkspaceState.READY for record in qdrant_records)


def test_governed_provider_canonical_admission_allows_non_json_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, body: bytes) -> None:
            self._body = body

        def read(self) -> bytes:
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        method = request.get_method()
        if url.endswith("/admission/submit") and method == "POST":
            return _FakeResponse(b"accepted")
        if url.endswith("/health") or url.endswith("/healthz") or url.endswith("/api/tags"):
            return _FakeResponse(b"{\"status\":\"online\"}")
        raise AssertionError(f"unexpected request: {method} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-nonjson-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )

    provider.admit_submission(
        payload=b"Board packet upload content.",
        source_record_id="source-record-018",
        file_name="board-packet.pdf",
        media_type="application/pdf",
    )

    briefing = provider.briefing()
    assert any(
        record.state is WorkspaceState.REVIEW_PENDING
        for record in briefing.workspace_records
    )


def test_governed_provider_canonical_runtime_health_handles_oserror(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeResponse:
        def __init__(self, body: bytes) -> None:
            self._body = body

        def read(self) -> bytes:
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def _fake_urlopen(request, timeout=0):
        del timeout
        url = request.full_url
        method = request.get_method()
        if method != "GET":
            raise AssertionError(f"unexpected request: {method} {url}")
        if url.endswith("/healthz"):
            raise OSError("socket closed")
        if url.endswith("/api/tags"):
            return _FakeResponse(b"{\"status\":\"online\"}")
        if url.endswith("/health"):
            return _FakeResponse(b"{\"status\":\"online\"}")
        raise AssertionError(f"unexpected request: {method} {url}")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider.urllib.request.urlopen",
        _fake_urlopen,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-oserror-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    briefing = provider.briefing()
    qdrant_records = [
        record
        for record in briefing.workspace_records
        if record.record_id.startswith("demo-runtime-")
        and "qdrant" in record.title.lower()
    ]
    assert qdrant_records
    assert all(record.state is WorkspaceState.UNAVAILABLE for record in qdrant_records)


def test_governed_provider_canonical_runtime_health_failure_degrades_to_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise_runtime_error(self) -> tuple[object, ...]:
        del self
        raise RuntimeError("runtime_request_failed: synthetic")

    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider._CanonicalRuntimeClient.runtime_health",
        _raise_runtime_error,
    )
    provider = GovernedRuntimeBriefingProvider(
        Path(tempfile.mkdtemp(prefix="gov-provider-canonical-health-fallback-test-")),
        canonical_runtime=True,
        organization_id="virginia-b-andes",
        workspace_mode=WorkspaceMode.PRODUCTION,
    )
    briefing = provider.briefing()
    runtime_records = [
        record
        for record in briefing.workspace_records
        if record.record_id.startswith("demo-runtime-")
    ]
    assert len(runtime_records) == 4
    assert all(record.state is WorkspaceState.UNAVAILABLE for record in runtime_records)
    assert any(
        "health_check_failed:runtime_request_failed: synthetic" in " ".join(record.limitations)
        for record in runtime_records
    )
