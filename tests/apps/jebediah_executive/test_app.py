"""Layer 4/5/7 - application, workflow, and failure-injection tests.

These tests exercise the WSGI application end to end without binding a socket:
method and query validation, security headers, HEAD mirroring, sanitized
errors, cookie/session/persistence absence, Host/Origin neutrality, sanitized
logging, the six executive workflows, and the failure-injection matrix.
"""

from __future__ import annotations

import io
import logging
import re
import socket
import threading
from datetime import datetime, timezone
from wsgiref.simple_server import make_server

import pytest

from apps.jebediah_executive.app import (
    LOOPBACK_HOST,
    SanitizedRequestHandler,
    create_app,
    validate_port,
)
from apps.jebediah_executive.fixtures import (
    SyntheticBriefingProvider,
    build_briefing,
)
from apps.jebediah_executive.models import ExecutiveBriefing
from apps.jebediah_executive.models import (
    Phase3BReviewEntryView,
    Phase3BSubmissionDetailView,
    Phase3BSubmissionState,
    Phase3BSubmissionSummary,
    Phase3BWorkspaceView,
)


class _ExplodingInput:
    """A wsgi.input replacement that fails if the body is ever read."""

    def read(self, *args: object, **kwargs: object) -> bytes:
        raise AssertionError("request body must never be read")

    def readline(self, *args: object, **kwargs: object) -> bytes:
        raise AssertionError("request body must never be read")

    def __iter__(self):  # pragma: no cover - defensive
        raise AssertionError("request body must never be read")


class Client:
    def __init__(self, app=None) -> None:
        self.app = app or create_app()

    def request(self, method: str, path: str, query: str = "", **extra: str):
        captured: dict[str, object] = {}

        def start_response(status: str, headers):
            captured["status"] = status
            captured["headers"] = list(headers)

        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": query,
            "wsgi.input": _ExplodingInput(),
            "SERVER_NAME": "127.0.0.1",
            "SERVER_PORT": "8765",
        }
        environ.update(extra)
        body = b"".join(self.app(environ, start_response))
        headers = {k: v for k, v in captured["headers"]}
        return str(captured["status"]), headers, body


class FakeWorkspaceService:
    def __init__(self) -> None:
        self.detail = Phase3BSubmissionDetailView(
            summary=Phase3BSubmissionSummary(
                submission_id="demo-submission-1",
                title="Synthetic roster PDF",
                state=Phase3BSubmissionState.READY_FOR_REVIEW,
                received_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                sha256_hex="a" * 64,
                byte_count=128,
                duplicate_of=None,
                warnings=("native_text_unavailable",),
            ),
            native_text_sufficient=False,
            page_count=2,
            review_entries=(),
            warnings=("native_text_unavailable",),
            limitations=("Synthetic only.",),
        )
        self.last_admitted_payload = b""

    def workspace_page(self) -> Phase3BWorkspaceView:
        return Phase3BWorkspaceView(
            generated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            submissions=(self.detail.summary,),
            recent_events=("submission_accepted",),
            limitations=("Synthetic only.",),
        )

    def submission_page(self, submission_id: str) -> Phase3BSubmissionDetailView | None:
        return self.detail if submission_id == self.detail.summary.submission_id else None

    def admit_pdf(
        self,
        *,
        receipt_id: str,
        filename: str,
        media_type: str,
        payload: bytes,
    ) -> Phase3BSubmissionDetailView:
        assert receipt_id == "synthetic-receipt-1"
        assert filename == "synthetic.pdf"
        assert media_type == "application/pdf"
        self.last_admitted_payload = payload
        return self.detail

    def review_submission(
        self,
        *,
        submission_id: str,
        decision: str,
        note: str,
    ) -> Phase3BSubmissionDetailView:
        assert submission_id == self.detail.summary.submission_id
        self.detail = Phase3BSubmissionDetailView(
            summary=self.detail.summary,
            native_text_sufficient=self.detail.native_text_sufficient,
            page_count=self.detail.page_count,
            review_entries=(
                Phase3BReviewEntryView(
                    decision=decision,
                    note=note,
                    created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                ),
            ),
            warnings=self.detail.warnings,
            limitations=self.detail.limitations,
        )
        return self.detail

    def delete_submission(self, submission_id: str) -> Phase3BSubmissionDetailView:
        assert submission_id == self.detail.summary.submission_id
        self.detail = Phase3BSubmissionDetailView(
            summary=Phase3BSubmissionSummary(
                submission_id=self.detail.summary.submission_id,
                title=self.detail.summary.title,
                state=Phase3BSubmissionState.DELETED,
                received_at=self.detail.summary.received_at,
                sha256_hex=self.detail.summary.sha256_hex,
                byte_count=self.detail.summary.byte_count,
                duplicate_of=self.detail.summary.duplicate_of,
                warnings=self.detail.summary.warnings,
            ),
            native_text_sufficient=self.detail.native_text_sufficient,
            page_count=self.detail.page_count,
            review_entries=self.detail.review_entries,
            warnings=self.detail.warnings,
            limitations=self.detail.limitations,
        )
        return self.detail

    def recover(self) -> None:
        return None


def _multipart(parts: list[tuple[str, str | bytes, str | None, str | None]]) -> tuple[str, bytes]:
    boundary = "phase3b-boundary"
    body = bytearray()
    for name, value, filename, content_type in parts:
        body.extend(f"--{boundary}\r\n".encode("ascii"))
        disposition = f"Content-Disposition: form-data; name=\"{name}\""
        if filename is not None:
            disposition += f"; filename=\"{filename}\""
        body.extend((disposition + "\r\n").encode("utf-8"))
        if content_type is not None:
            body.extend(f"Content-Type: {content_type}\r\n".encode("ascii"))
        body.extend(b"\r\n")
        body.extend(value if isinstance(value, bytes) else value.encode("utf-8"))
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("ascii"))
    return f"multipart/form-data; boundary={boundary}", bytes(body)


@pytest.fixture()
def client() -> Client:
    return Client()


def _raw_request(request: bytes) -> bytes:
    server = make_server(
        LOOPBACK_HOST,
        0,
        create_app(),
        handler_class=SanitizedRequestHandler,
    )
    server.timeout = 2
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    try:
        with socket.create_connection(server.server_address, timeout=2) as connection:
            connection.sendall(request)
            connection.shutdown(socket.SHUT_WR)
            chunks: list[bytes] = []
            while chunk := connection.recv(8192):
                chunks.append(chunk)
    finally:
        thread.join(timeout=2)
        server.server_close()
    assert not thread.is_alive()
    return b"".join(chunks)


# ---------------------------------------------------------------------------
# Security headers and content types
# ---------------------------------------------------------------------------

REQUIRED_SECURITY = {
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
    "Cache-Control": "no-store",
}


def test_security_headers_present_on_pages(client: Client) -> None:
    status, headers, _ = client.request("GET", "/")
    assert status == "200 OK"
    csp = headers["Content-Security-Policy"]
    assert "default-src 'none'" in csp
    assert "style-src 'self'" in csp
    assert "base-uri 'none'" in csp
    assert "form-action 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    for key, value in REQUIRED_SECURITY.items():
        assert headers[key] == value
    # No permissive CORS or cookies.
    assert not any(k.lower() == "access-control-allow-origin" for k in headers)
    assert not any(k.lower() == "set-cookie" for k in headers)


@pytest.mark.parametrize(
    ("request_bytes", "status"),
    [
        (
            b"GET /" + (b"x" * 70_000) + b" HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
            b"414",
        ),
        (b"malformed request\r\n\r\n", b"400"),
    ],
    ids=("uri-too-long", "malformed-request"),
)
def test_pre_wsgi_parser_errors_use_hardened_envelope(
    request_bytes: bytes, status: bytes
) -> None:
    response = _raw_request(request_bytes)
    assert response.startswith(b"HTTP/1.0 " + status + b" ")
    for header in (
        b"Content-Security-Policy: default-src 'none'",
        b"Referrer-Policy: no-referrer",
        b"X-Content-Type-Options: nosniff",
        b"Cache-Control: no-store",
        b"Connection: close",
    ):
        assert header in response
    for landmark in (
        b"class=\"skip-link\"",
        b"<header",
        b"<nav",
        b"<main",
        b"<footer",
    ):
        assert landmark in response
    assert b"malformed request" not in response.lower()


def test_stylesheet_has_fixed_content_type(client: Client) -> None:
    status, headers, body = client.request("GET", "/static/styles.css")
    assert status == "200 OK"
    assert headers["Content-Type"] == "text/css; charset=utf-8"
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert b":focus-visible" in body


def test_stylesheet_cannot_select_another_file(client: Client) -> None:
    status, _, _ = client.request("GET", "/static/other.css")
    assert status == "404 Not Found"
    status, _, _ = client.request("GET", "/static/../app.py")
    assert status == "404 Not Found"


# ---------------------------------------------------------------------------
# Methods and body handling
# ---------------------------------------------------------------------------

def test_get_returns_expected_content(client: Client) -> None:
    status, headers, body = client.request("GET", "/attention")
    assert status == "200 OK"
    assert headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"Needs attention" in body


def test_head_mirrors_get(client: Client) -> None:
    for path in ("/", "/board", "/static/styles.css", "/states/ready"):
        gstatus, gheaders, gbody = client.request("GET", path)
        hstatus, hheaders, hbody = client.request("HEAD", path)
        assert hstatus == gstatus, path
        assert hbody == b"", path
        assert hheaders["Content-Length"] == gheaders["Content-Length"], path
        assert hheaders["Content-Type"] == gheaders["Content-Type"], path


@pytest.mark.parametrize(
    "method", ["POST", "PUT", "PATCH", "DELETE", "CONNECT", "OPTIONS", "TRACE"]
)
def test_unsupported_methods_405(client: Client, method: str) -> None:
    status, headers, _ = client.request(method, "/")
    assert status == "405 Method Not Allowed"
    expected_allow = "GET, HEAD" if method == "POST" else "GET, HEAD, POST"
    assert headers["Allow"] == expected_allow


def test_request_body_never_read(client: Client) -> None:
    # _ExplodingInput raises if read; a POST must still return 405 cleanly.
    status, _, _ = client.request("POST", "/attention")
    assert status == "405 Method Not Allowed"
    # A GET must also not read the body.
    status, _, _ = client.request("GET", "/", extra_env_ignored="")
    assert status == "200 OK"


def test_phase3b_workspace_routes_support_post_and_detail_get() -> None:
    service = FakeWorkspaceService()
    client = Client(create_app(workspace_service=service))
    status, _, body = client.request("GET", "/workspace")
    assert status == "200 OK"
    assert b"Synthetic PDF intake and custody workspace" in body

    status, _, body = client.request("GET", "/workspace/submissions/demo-submission-1")
    assert status == "200 OK"
    assert b"Synthetic PDF submission detail" in body


def test_phase3b_intake_post_redirects_without_echoing_payload() -> None:
    service = FakeWorkspaceService()
    client = Client(create_app(workspace_service=service))
    content_type, body = _multipart(
        [
            ("receipt_id", "synthetic-receipt-1", None, None),
            ("pdf", b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n", "synthetic.pdf", "application/pdf"),
        ]
    )
    status, headers, response_body = client.request(
        "POST",
        "/workspace/intake",
        CONTENT_TYPE=content_type,
        CONTENT_LENGTH=str(len(body)),
        **{"wsgi.input": io.BytesIO(body)},
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/workspace/submissions/demo-submission-1"
    assert b"SYNTHETIC-TEXT" not in response_body
    assert service.last_admitted_payload.startswith(b"%PDF-1.7")


# ---------------------------------------------------------------------------
# Query rejection
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "query",
    ["x=1", "state=ready", "path=/etc", "prompt=hello", "id=demo-item"],
)
def test_every_query_string_is_400(client: Client, query: str) -> None:
    status, _, body = client.request("GET", "/", query=query)
    assert status == "400 Bad Request"
    assert b"Query strings are not accepted" in body
    # The raw query is never reflected in the body.
    assert query.encode() not in body


# ---------------------------------------------------------------------------
# Not found and safe traversal handling
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "path",
    [
        "/unknown",
        "/attention/",
        "/ask/unknown",
        "/states/unknown",
        "/../etc/passwd",
        "//attention",
        "\\attention",
        "/next\x00",
    ],
)
def test_unknown_and_traversal_404(client: Client, path: str) -> None:
    status, _, body = client.request("GET", path)
    assert status == "404 Not Found"
    # No path reflection.
    assert path.encode() not in body
    assert b"not part of this synthetic preview" in body


def test_invalid_state_and_ask_are_404(client: Client) -> None:
    assert client.request("GET", "/states/nonsense")[0] == "404 Not Found"
    assert client.request("GET", "/ask/nonsense")[0] == "404 Not Found"


# ---------------------------------------------------------------------------
# Host / Origin neutrality and no persistence
# ---------------------------------------------------------------------------

def test_host_and_origin_do_not_affect_response(client: Client) -> None:
    _, h1, b1 = client.request("GET", "/", HTTP_HOST="evil.example", HTTP_ORIGIN="https://evil.example")
    _, h2, b2 = client.request("GET", "/", HTTP_HOST="127.0.0.1:8765")
    assert b1 == b2
    assert h1 == h2
    # Product links remain relative.
    assert b"href=\"/attention\"" in b1
    assert b"href=\"https://" not in b1
    assert b"evil.example" not in b1


def test_no_state_persists_between_requests(client: Client) -> None:
    _, _, first = client.request("GET", "/")
    _, _, second = client.request("GET", "/")
    assert first == second


class _CountingProvider:
    def __init__(self) -> None:
        self.calls = 0

    def briefing(self) -> ExecutiveBriefing:
        self.calls += 1
        return build_briefing()


def test_provider_is_consumed_once_during_app_initialization() -> None:
    provider = _CountingProvider()
    client = Client(create_app(provider))
    assert provider.calls == 1
    client.request("GET", "/")
    client.request("GET", "/attention")
    assert provider.calls == 1


# ---------------------------------------------------------------------------
# Sanitized logging
# ---------------------------------------------------------------------------

def test_logs_are_sanitized(client: Client, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="apps.jebediah_executive"):
        client.request("GET", "/attention")
        client.request("GET", "/secret/leak", query="token=abcd1234")
        client.request("POST", "/")
        client.request("GE\x1b[31mT", "/")
        client.request("X" * 10_000, "/")
    messages = [record.getMessage() for record in caplog.records]
    expected = (
        r"GET attention 200 \d+\.\d{3}ms",
        r"GET unrecognized 400 \d+\.\d{3}ms",
        r"POST overview 405 \d+\.\d{3}ms",
    )
    for pattern in expected:
        assert any(re.fullmatch(pattern, message) for message in messages), pattern
    joined = "\n".join(messages)
    for leak in ("secret", "leak", "token", "abcd1234", "\x1b", "XXXXX"):
        assert leak not in joined
    assert all(len(message) < 80 for message in messages)


# ---------------------------------------------------------------------------
# Internal failure -> sanitized 500
# ---------------------------------------------------------------------------

class _BrokenProvider:
    def briefing(self):
        return object()  # missing every attribute the renderer needs


def test_internal_render_failure_is_sanitized_500() -> None:
    app = create_app(provider=_BrokenProvider())  # type: ignore[arg-type]
    client = Client(app)
    status, headers, body = client.request("GET", "/")
    assert status == "500 Internal Server Error"
    assert b"Traceback" not in body
    assert b"object at 0x" not in body
    # A sanitized page is returned with the synthetic, no-action boundary and
    # no reflected internals.
    assert b"no organizational action is taken" in body
    assert b"Synthetic demonstration" in body
    for landmark in (b"class=\"skip-link\"", b"<header", b"<nav", b"<footer"):
        assert landmark in body


def test_internal_render_failure_with_valid_briefing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from apps.jebediah_executive import app as app_module
    from apps.jebediah_executive.routes import RouteResolution

    def _boom(_briefing):
        raise RuntimeError("synthetic render fault")

    def _fake_resolve(path: str):
        if path == "/":
            return RouteResolution(route_id="overview", is_static=False, render=_boom)
        return None

    monkeypatch.setattr(app_module, "resolve", _fake_resolve)
    client = Client(create_app())
    status, _, body = client.request("GET", "/")
    assert status == "500 Internal Server Error"
    assert b"Traceback" not in body
    assert b"synthetic render fault" not in body
    assert b"internal synthetic rendering error" in body


# ---------------------------------------------------------------------------
# Port validation (Layer 4 entry point)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("port", [1023, 65536, 0, -1])
def test_port_out_of_range_rejected(port: int) -> None:
    with pytest.raises(ValueError):
        validate_port(port)


def test_port_boolean_rejected() -> None:
    with pytest.raises(ValueError):
        validate_port(True)  # type: ignore[arg-type]


@pytest.mark.parametrize("port", [1024, 8765, 65535])
def test_port_in_range_accepted(port: int) -> None:
    assert validate_port(port) == port


# ---------------------------------------------------------------------------
# Layer 5 - executive workflows
# ---------------------------------------------------------------------------

def test_workflow_executive_orientation(client: Client) -> None:
    _, _, overview = client.request("GET", "/")
    assert b"Synthetic status" in overview
    assert b"Material limitations" in overview
    _, _, attention = client.request("GET", "/attention")
    # An attention item shows its separately linked next-item kind.
    assert b"Related next step" in attention
    # Its evidence reference is available as a local disclosure.
    assert b"Source reference" in attention


def test_workflow_decision_preparation(client: Client) -> None:
    _, _, nxt = client.request("GET", "/next")
    assert b"Decision required" in nxt
    assert b"Organizational gate" in nxt
    assert b"Action candidate" in nxt
    assert b"Human authority required" in nxt
    # No execution control exists.
    for control in (b"<button", b"<form", b"<input"):
        assert control not in nxt


def test_workflow_knowledge_boundary(client: Client) -> None:
    _, _, knowledge = client.request("GET", "/knowledge")
    assert b"Knowledge gap" in knowledge or b"knowledge_gap" in knowledge
    _, _, board = client.request("GET", "/board")
    assert b"Missing information" in board
    assert b"Conflicting information" in board
    assert b"Stale information" in board
    _, _, workspace = client.request("GET", "/workspace")
    assert b"lineage" in workspace.lower()


def test_workflow_ask_boundary(client: Client) -> None:
    _, _, index = client.request("GET", "/ask")
    for control in (b"<textarea", b"<input", b"<form"):
        assert control not in index
    _, _, grounded = client.request("GET", "/ask/grounded-priorities")
    assert b"Grounded" in grounded
    _, _, insufficient = client.request("GET", "/ask/insufficient-program-outcomes")
    assert b"No answer is fabricated" in insufficient
    _, _, failed = client.request("GET", "/ask/failed-source-review")
    assert b"Failed" in failed


def test_workflow_board_preparation(client: Client) -> None:
    _, _, board = client.request("GET", "/board")
    for marker in (b"Priorities", b"Risks", b"Opportunities", b"decisions", b"Coverage"):
        assert marker in board or marker.lower() in board.lower()
    # Print rules retain evidence and limitations (present in the CSS and body).
    assert b"Material limitations" in board


def test_workflow_failure_awareness(client: Client) -> None:
    _, _, gallery = client.request("GET", "/states")
    for state_id in (
        "ready",
        "loading",
        "empty",
        "partial",
        "stale",
        "insufficient-evidence",
        "held",
        "failed",
        "unauthorized",
        "unavailable",
        "disconnected",
    ):
        status, _, detail = client.request("GET", f"/states/{state_id}")
        assert status == "200 OK", state_id
        assert b"no organizational action" in detail
        assert b"Synthetic demonstration" in detail
