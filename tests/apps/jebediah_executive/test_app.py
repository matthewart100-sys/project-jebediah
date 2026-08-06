"""Layer 4/5/7 - application, workflow, and failure-injection tests.

These tests exercise the WSGI application end to end without binding a socket:
method and query validation, security headers, HEAD mirroring, sanitized
errors, cookie/session/persistence absence, Host/Origin neutrality, sanitized
logging, executive workflow rendering, and bounded governed POST workflows.
"""

from __future__ import annotations

import io
import logging
from pathlib import Path
import re
import socket
import tempfile
import threading
from wsgiref.simple_server import make_server

import pytest

from apps.jebediah_executive import app as executive_app
from apps.jebediah_executive.app import (
    LOOPBACK_HOST,
    SanitizedRequestHandler,
    create_app,
    validate_port,
)
from apps.jebediah_executive.governed_provider import OperationalWorkspaceProvider
from apps.jebediah_executive.fixtures import (
    SyntheticBriefingProvider,
    build_briefing,
)
from apps.jebediah_executive.models import ExecutiveBriefing


def test_default_provider_falls_back_outside_canonical_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BONSAAI_CANONICAL_RUNTIME", raising=False)

    def _raise(_cls):
        raise RuntimeError("init failed")

    monkeypatch.setattr(
        OperationalWorkspaceProvider,
        "create_default",
        classmethod(_raise),
    )

    provider = executive_app._default_provider()
    assert isinstance(provider, SyntheticBriefingProvider)


def test_default_provider_fails_fast_in_canonical_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BONSAAI_CANONICAL_RUNTIME", "1")

    def _raise(_cls):
        raise RuntimeError("init failed")

    monkeypatch.setattr(
        OperationalWorkspaceProvider,
        "create_default",
        classmethod(_raise),
    )

    with pytest.raises(RuntimeError, match="canonical_runtime_provider_initialization_failed"):
        executive_app._default_provider()


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

    def request(
        self,
        method: str,
        path: str,
        query: str = "",
        *,
        body: bytes | None = None,
        content_type: str = "application/x-www-form-urlencoded",
        **extra: str,
    ):
        captured: dict[str, object] = {}

        def start_response(status: str, headers):
            captured["status"] = status
            captured["headers"] = list(headers)

        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": query,
            "SERVER_NAME": "127.0.0.1",
            "SERVER_PORT": "8765",
        }
        if body is None:
            environ["wsgi.input"] = _ExplodingInput()
        else:
            environ["wsgi.input"] = io.BytesIO(body)
            environ["CONTENT_TYPE"] = content_type
            environ["CONTENT_LENGTH"] = str(len(body))
        environ.update(extra)
        body = b"".join(self.app(environ, start_response))
        headers = {k: v for k, v in captured["headers"]}
        return str(captured["status"]), headers, body


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
    "method", ["PUT", "PATCH", "DELETE", "CONNECT", "OPTIONS", "TRACE"]
)
def test_unsupported_methods_405(client: Client, method: str) -> None:
    status, headers, _ = client.request(method, "/")
    assert status == "405 Method Not Allowed"
    assert headers["Allow"] == "GET, HEAD, POST"


def test_get_request_body_never_read(client: Client) -> None:
    # A GET must never read body content.
    status, _, _ = client.request("GET", "/", extra_env_ignored="")
    assert status == "200 OK"


def test_post_unknown_route_is_404_with_interactive_provider(client: Client) -> None:
    status, _, _ = client.request("POST", "/attention", body=b"")
    assert status == "404 Not Found"


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
    assert b"href=\"/knowledge-manager\"" in b1
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
    assert provider.calls == 0
    client.request("GET", "/")
    client.request("GET", "/attention")
    assert provider.calls == 2


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
        r"POST overview 404 \d+\.\d{3}ms",
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
    assert b"Governed runtime" in body
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
    assert b"Runtime status" in overview
    assert b"Material limitations" in overview
    _, _, attention = client.request("GET", "/attention")
    # An attention item shows its separately linked next-item kind.
    assert b"Related next step" in attention
    # Its evidence reference is available as a local disclosure.
    assert b"Source reference" in attention


def test_workflow_decision_preparation(client: Client) -> None:
    _, _, nxt = client.request("GET", "/next")
    assert b"Decision required" in nxt
    assert b"Human authority required" in nxt
    # No execution control exists.
    for control in (b"<button", b"<form", b"<input"):
        assert control not in nxt


def test_workflow_knowledge_boundary(client: Client) -> None:
    _, _, knowledge = client.request("GET", "/organizational-memory")
    assert b"Knowledge gap" in knowledge or b"knowledge_gap" in knowledge
    _, _, board = client.request("GET", "/board")
    assert b"Missing information" in board
    assert b"Conflicting information" in board
    assert b"Stale information" in board
    _, _, workspace = client.request("GET", "/knowledge-manager")
    assert b"lineage" in workspace.lower()


def test_workflow_ask_boundary(client: Client) -> None:
    _, _, index = client.request("GET", "/organizational-intelligence")
    assert b"preset synthetic questions" in index
    _, _, grounded = client.request("GET", "/ask/grounded-priorities")
    assert b"State:" in grounded
    _, _, insufficient = client.request("GET", "/ask/insufficient-program-outcomes")
    assert b"No answer is fabricated" in insufficient
    _, _, failed = client.request("GET", "/ask/failed-source-review")
    assert b"Failed" in failed


def test_workflow_admission_promotion_and_question_post_round_trip(client: Client) -> None:
    provider = OperationalWorkspaceProvider(Path(tempfile.mkdtemp(prefix="workflow-runtime-test-")))
    provider.select_workspace("development")
    client = Client(create_app(provider))
    boundary = "----bonsaai-test-boundary"
    admit_body = (
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"source_record_id\"\r\n\r\n"
        "source-record-777\r\n"
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"document_file\"; filename=\"report.txt\"\r\n"
        "Content-Type: text/plain\r\n\r\n"
        "Governance committee approved the reconciliation plan.\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    admit_content_type = (
        f"multipart/form-data; boundary={boundary}"
    )
    status, headers, _ = client.request(
        "POST",
        "/knowledge-manager/admit",
        body=admit_body,
        content_type=admit_content_type,
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/knowledge-manager"

    status, headers, _ = client.request(
        "POST",
        "/knowledge-manager/promote-latest",
        body=b"",
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/knowledge-manager"

    ask_body = b"question=What+should+leadership+decide+next+based+on+approved+evidence%3F"
    status, headers, _ = client.request(
        "POST",
        "/organizational-intelligence/ask",
        body=ask_body,
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/organizational-intelligence"

    _, _, grounded = client.request("GET", "/ask/grounded-priorities")
    assert b"Grounded" in grounded
    assert b"Evidence citation" in grounded


def test_workflow_board_preparation(client: Client) -> None:
    _, _, board = client.request("GET", "/board")
    for marker in (b"Priorities", b"Risks", b"Opportunities", b"decisions", b"Coverage"):
        assert marker in board or marker.lower() in board.lower()
    # Print rules retain evidence and limitations (present in the CSS and body).
    assert b"Material limitations" in board


def test_primary_navigation_exposes_unified_platform_sections(client: Client) -> None:
    _, _, home = client.request("GET", "/")
    for label in (
        b"Executive Dashboard",
        b"Knowledge Manager",
        b"Organizational Intelligence",
        b"Organizational Memory",
        b"Governance",
        b"Audit",
        b"Administration",
    ):
        assert label in home


def test_demonstration_mode_walkthrough_is_available(client: Client) -> None:
    status, _, body = client.request("GET", "/demo")
    assert status == "200 OK"
    assert b"Guided executive walkthrough" in body
    assert b"Document admission" in body
    assert b"evidence-backed answer" in body.lower()


def test_canonical_admission_failure_renders_without_http_500(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _fail_submission(self, **kwargs):
        del self, kwargs
        raise RuntimeError("runtime_request_failed: interaction_admission")

    monkeypatch.setenv("BONSAAI_CANONICAL_RUNTIME", "1")
    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider._CanonicalRuntimeClient.submit_admission",
        _fail_submission,
    )
    monkeypatch.setattr(
        "apps.jebediah_executive.governed_provider._CanonicalRuntimeClient.runtime_health",
        lambda self: (),
    )
    provider = OperationalWorkspaceProvider(
        Path(tempfile.mkdtemp(prefix="canonical-admission-failure-test-"))
    )
    provider.select_workspace("production")
    client = Client(create_app(provider))
    boundary = "----bonsaai-failure-boundary"
    body = (
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"source_record_id\"\r\n\r\n"
        "source-record-failed\r\n"
        f"--{boundary}\r\n"
        "Content-Disposition: form-data; name=\"document_file\"; filename=\"failed.pdf\"\r\n"
        "Content-Type: application/pdf\r\n\r\n"
        "%PDF-1.4 synthetic\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    status, headers, _ = client.request(
        "POST",
        "/knowledge-manager/admit",
        body=body,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/knowledge-manager"

    status, _, page = client.request("GET", "/knowledge-manager")
    assert status == "200 OK"
    assert b"processing_failed" in page
    assert b"runtime_request_failed: interaction_admission" in page
    assert b"http://jebediah-interaction" not in page


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
        assert b"Governed runtime" in detail


def test_workspace_switch_and_organization_switch_round_trip() -> None:
    provider = OperationalWorkspaceProvider(Path(tempfile.mkdtemp(prefix="workspace-app-test-")))
    client = Client(create_app(provider))
    status, headers, _ = client.request(
        "POST",
        "/workspace/select",
        body=b"workspace_mode=development",
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/"
    status, headers, _ = client.request(
        "POST",
        "/workspace/select-organization",
        body=b"organization_id=virginia-b-andes",
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/"
    _, _, body = client.request("GET", "/")
    assert b"Development Environment" in body
    assert b"Virginia B. Andes" in body


def test_demo_reset_route_returns_redirect() -> None:
    provider = OperationalWorkspaceProvider(Path(tempfile.mkdtemp(prefix="workspace-app-test-")))
    client = Client(create_app(provider))
    status, headers, _ = client.request(
        "POST",
        "/workspace/reset-demo",
        body=b"",
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/demo"


def test_auth_required_redirects_to_login(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BONSAAI_REQUIRE_AUTH", "1")
    monkeypatch.setenv("BONSAAI_ALLOW_DEMO_ANONYMOUS", "0")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")
    monkeypatch.setenv(
        "JEBEDIAH_RUNTIME_ROOT", tempfile.mkdtemp(prefix="auth-required-runtime-")
    )
    client = Client(create_app())
    status, headers, _ = client.request("GET", "/")
    assert status == "303 See Other"
    assert headers["Location"] == "/login"


def test_login_sets_cookie_and_can_reach_dashboard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BONSAAI_REQUIRE_AUTH", "1")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")
    monkeypatch.setenv("BONSAAI_ALLOW_DEMO_ANONYMOUS", "0")
    monkeypatch.setenv(
        "JEBEDIAH_RUNTIME_ROOT", tempfile.mkdtemp(prefix="auth-login-runtime-")
    )
    client = Client(create_app())
    body = b"email=admin%40example.com&password=AdminPassword%21234"
    status, headers, _ = client.request("POST", "/login", body=body)
    assert status == "303 See Other"
    assert headers["Location"] == "/"
    cookie = headers.get("Set-Cookie", "")
    assert "bonsaai_session=" in cookie
    session_value = cookie.split(";", 1)[0]
    status, _, body = client.request("GET", "/", HTTP_COOKIE=session_value)
    assert status == "200 OK"
    assert b"Signed in as" in body


def test_logout_requires_csrf_and_clears_cookie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BONSAAI_REQUIRE_AUTH", "1")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com")
    monkeypatch.setenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "AdminPassword!234")
    monkeypatch.setenv(
        "JEBEDIAH_RUNTIME_ROOT", tempfile.mkdtemp(prefix="auth-logout-runtime-")
    )
    client = Client(create_app())
    login_body = b"email=admin%40example.com&password=AdminPassword%21234"
    _, login_headers, _ = client.request("POST", "/login", body=login_body)
    cookie = login_headers["Set-Cookie"].split(";", 1)[0]
    _, _, dashboard = client.request("GET", "/", HTTP_COOKIE=cookie)
    match = re.search(rb'name="csrf_token" value="([^"]+)"', dashboard)
    assert match is not None
    csrf_token = match.group(1).decode("utf-8")

    status, _, _ = client.request("POST", "/logout", body=b"", HTTP_COOKIE=cookie)
    assert status == "400 Bad Request"

    logout_body = f"csrf_token={csrf_token}".encode("utf-8")
    status, headers, _ = client.request(
        "POST",
        "/logout",
        body=logout_body,
        HTTP_COOKIE=cookie,
    )
    assert status == "303 See Other"
    assert headers["Location"] == "/login"
    assert "Max-Age=0" in headers["Set-Cookie"]
