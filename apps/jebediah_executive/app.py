"""WSGI application, request validation, headers, and loopback server factory.

The application serves allowlisted GET and HEAD routes and bounded POST workflow
actions for governed Knowledge Manager and Organizational Intelligence flows. It
rejects query strings, sets restrictive security headers, serves one reviewed local
stylesheet, and logs only a sanitized method, route identity, status, and duration.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from email.parser import BytesParser
from email.policy import default as email_policy
from importlib.resources import files
import os
from pathlib import Path
from time import perf_counter
from urllib.parse import parse_qs
from typing import Protocol, runtime_checkable
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from .auth import AuthRuntime, AuthSession
from .fixtures import SyntheticBriefingProvider
from .models import ExecutiveBriefing
from .rendering import render_error
from .routes import RouteResolution, resolve

LOOPBACK_HOST = "127.0.0.1"
MIN_PORT = 1024
MAX_PORT = 65535
_STYLESHEET_RESOURCE = "styles.css"
_SUPPORTED_METHODS = frozenset({"GET", "HEAD"})
_SESSION_COOKIE_NAME = "bonsaai_session"
_AUTH_PUBLIC_GET_ROUTES = frozenset(
    {"/login", "/password-reset", "/password-reset/complete", "/health"}
)
_AUTH_PUBLIC_POST_ROUTES = frozenset(
    {"/login", "/password-reset", "/password-reset/complete", "/logout"}
)

logger = logging.getLogger("apps.jebediah_executive")

_SECURITY_HEADERS: tuple[tuple[str, str], ...] = (
    (
        "Content-Security-Policy",
        "default-src 'none'; style-src 'self'; base-uri 'none'; "
        "form-action 'self'; frame-ancestors 'none'",
    ),
    ("Referrer-Policy", "no-referrer"),
    ("X-Content-Type-Options", "nosniff"),
    ("Cache-Control", "no-store"),
)

WSGIEnviron = dict[str, object]
StartResponse = Callable[[str, list[tuple[str, str]]], object]


class BriefingProvider(Protocol):
    """Provides one immutable executive briefing to the presentation shell."""

    def briefing(self) -> ExecutiveBriefing:
        """Return the provider's immutable briefing."""


@runtime_checkable
class InteractiveProvider(BriefingProvider, Protocol):
    def admit_submission(
        self,
        *,
        payload: bytes,
        source_record_id: str,
        file_name: str,
        media_type: str,
    ) -> None:
        """Admit one uploaded submission through governed runtime boundaries."""

    def admit_document(self, document_text: str, source_record_id: str) -> None:
        """Admit one document through governed runtime boundaries."""

    def promote_latest_candidate(self) -> None:
        """Approve the latest pending candidate when available."""

    def reject_latest_candidate(self, reason: str = "human_review_rejected") -> None:
        """Reject the latest pending candidate when available."""

    def ask_question(self, question: str) -> None:
        """Run one governed executive question."""

    def select_workspace(self, mode: str) -> None:
        """Select one operational workspace mode."""

    def select_organization(self, organization_id: str) -> None:
        """Select one configured organization profile."""

    def reset_demo_workspace(self) -> None:
        """Reset demonstration workspace state to pristine synthetic fixtures."""


def _load_stylesheet() -> bytes:
    """Read the exact package-local reviewed stylesheet a single time."""
    resource = files(__package__).joinpath("static").joinpath(_STYLESHEET_RESOURCE)
    return resource.read_bytes()


def _headers_for_html(body: bytes) -> list[tuple[str, str]]:
    headers = [("Content-Type", "text/html; charset=utf-8")]
    headers.extend(_SECURITY_HEADERS)
    headers.append(("Content-Length", str(len(body))))
    return headers


def _headers_for_css(body: bytes) -> list[tuple[str, str]]:
    headers = [("Content-Type", "text/css; charset=utf-8")]
    headers.extend(_SECURITY_HEADERS)
    headers.append(("Content-Length", str(len(body))))
    return headers


def _is_auth_required() -> bool:
    return os.getenv("BONSAAI_REQUIRE_AUTH", "").strip().lower() in {"1", "true", "yes"}


def _allow_demo_anonymous() -> bool:
    return os.getenv("BONSAAI_ALLOW_DEMO_ANONYMOUS", "1").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _runtime_root() -> Path:
    configured = os.getenv("JEBEDIAH_RUNTIME_ROOT", "").strip()
    if configured:
        root = Path(configured).resolve()
        root.mkdir(parents=True, exist_ok=True)
        return root
    root = Path(os.getcwd()).resolve() / ".runtime"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _parse_session_cookie(environ: WSGIEnviron) -> str | None:
    raw = str(environ.get("HTTP_COOKIE", "") or "")
    if not raw:
        return None
    for entry in raw.split(";"):
        segment = entry.strip()
        if "=" not in segment:
            continue
        key, value = segment.split("=", 1)
        if key.strip() != _SESSION_COOKIE_NAME:
            continue
        normalized = value.strip()
        return normalized or None
    return None


def _build_session_cookie(session: AuthSession) -> str:
    secure = os.getenv("BONSAAI_COOKIE_SECURE", "1").strip().lower() in {"1", "true", "yes"}
    parts = [
        f"{_SESSION_COOKIE_NAME}={session.session_id}",
        "Path=/",
        "HttpOnly",
        "SameSite=Lax",
    ]
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


def _expired_cookie() -> str:
    return (
        f"{_SESSION_COOKIE_NAME}=deleted; Path=/; Max-Age=0; "
        "HttpOnly; SameSite=Lax"
    )


def _render_login_page(
    *,
    message: str | None = None,
    csrf_token: str = "",
    include_reset_token_field: bool = False,
) -> bytes:
    notice = (
        f"<p class=\"boundary\">{message}</p>"
        if message
        else "<p class=\"boundary\">Authenticate to access governed runtime workflows.</p>"
    )
    reset_token_field = (
        "<p><label for=\"reset_token\">Reset token</label><br>"
        "<input id=\"reset_token\" name=\"token\" type=\"text\" required></p>"
        if include_reset_token_field
        else ""
    )
    csrf_field = (
        f"<input type=\"hidden\" name=\"csrf_token\" value=\"{csrf_token}\">"
        if csrf_token
        else ""
    )
    html = (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Login — Bonsaai Platform Shell</title>"
        "<link rel=\"stylesheet\" href=\"/static/styles.css\"></head><body>"
        "<main id=\"main-content\"><h1>Bonsaai Login</h1>"
        + notice
        + "<section><h2>Sign in</h2>"
        "<form method=\"post\" action=\"/login\" class=\"workflow-form\">"
        + csrf_field
        + "<p><label for=\"email\">Email</label><br>"
        "<input id=\"email\" name=\"email\" type=\"text\" autocomplete=\"username\" required></p>"
        "<p><label for=\"password\">Password</label><br>"
        "<input id=\"password\" name=\"password\" type=\"password\" autocomplete=\"current-password\" required></p>"
        "<p><label><input name=\"remember_device\" type=\"checkbox\" value=\"yes\"> Remember device</label></p>"
        "<p><button type=\"submit\">Login</button></p></form></section>"
        "<section><h2>Password reset</h2>"
        "<form method=\"post\" action=\"/password-reset\" class=\"workflow-form\">"
        + csrf_field
        + "<p><label for=\"reset_email\">Email</label><br>"
        "<input id=\"reset_email\" name=\"email\" type=\"text\" autocomplete=\"email\" required></p>"
        "<p><button type=\"submit\">Request password reset</button></p>"
        "</form></section>"
        "<section><h2>Reset password</h2>"
        "<form method=\"post\" action=\"/password-reset/complete\" class=\"workflow-form\">"
        + csrf_field
        + reset_token_field
        + "<p><label for=\"new_password\">New password</label><br>"
        "<input id=\"new_password\" name=\"new_password\" type=\"password\" autocomplete=\"new-password\" required></p>"
        "<p><button type=\"submit\">Complete password reset</button></p>"
        "</form></section>"
        "</main></body></html>"
    )
    return html.encode("utf-8")


class SanitizedRequestHandler(WSGIRequestHandler):
    """WSGI handler with fixed logging and hardened parser-error responses."""

    def handle_one_request(self) -> None:
        """Track each request without retaining or logging request content."""
        self._request_started_at = perf_counter()
        super().handle_one_request()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Suppress the standard raw request log; the app logs safely instead."""
        return

    def log_request(self, code: object = "-", size: object = "-") -> None:
        """Suppress the standard status line; the app logs safely instead."""
        return

    def send_error(
        self,
        code: int,
        message: str | None = None,
        explain: str | None = None,
    ) -> None:
        """Return a fixed hardened envelope for failures before WSGI dispatch."""
        del message, explain
        status_code = code if code in self.responses else 400
        status_phrase = self.responses[status_code][0]

        body = _FALLBACK_ERROR_HTML.encode("utf-8")
        self.request_version = "HTTP/1.0"
        self.send_response_only(status_code, status_phrase)
        for name, value in _headers_for_html(body):
            self.send_header(name, value)
        self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        self.close_connection = True

        started_at = getattr(self, "_request_started_at", perf_counter())
        duration_ms = max(0.0, (perf_counter() - started_at) * 1000)
        logger.info(
            "unsupported unrecognized %s %.3fms",
            status_code,
            duration_ms,
        )


def create_app(
    provider: BriefingProvider | None = None,
) -> Callable[[WSGIEnviron, StartResponse], Iterable[bytes]]:
    """Return a WSGI application over a briefing provider."""
    active_provider = provider if provider is not None else _default_provider()
    stylesheet = _load_stylesheet()
    auth_runtime = AuthRuntime(runtime_root=_runtime_root())
    auth_required = _is_auth_required()
    demo_anonymous_allowed = _allow_demo_anonymous()

    def application(
        environ: WSGIEnviron, start_response: StartResponse
    ) -> Iterable[bytes]:
        started_at = perf_counter()
        requested_method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        method = (
            requested_method
            if requested_method in _SUPPORTED_METHODS or requested_method == "POST"
            else "unsupported"
        )
        path = str(environ.get("PATH_INFO", ""))
        query = str(environ.get("QUERY_STRING", ""))
        session_id = _parse_session_cookie(environ)
        session_resolution = auth_runtime.resolve_session(session_id)
        session = session_resolution.session
        auth_user = session_resolution.user
        renewed_cookie: str | None = None
        clear_expired_cookie = (
            session is None and session_id is not None and session_resolution.expired
        )
        if session is not None:
            session = auth_runtime.renew_session(session)
            renewed_cookie = _build_session_cookie(session)
        briefing = _safe_briefing(active_provider)
        if briefing is not None:
            workspace = briefing.workspace_context
            updated_workspace = replace(
                workspace,
                csrf_token=session.csrf_token if session is not None else "",
                auth_required=auth_required,
                authenticated=session is not None,
                authenticated_user_display=(
                    auth_user.display_name if auth_user is not None else "anonymous"
                ),
                authenticated_user_role=(
                    auth_user.role if auth_user is not None else "viewer"
                ),
                active_session_count=auth_runtime.active_session_count,
                locked_account_count=auth_runtime.locked_account_count,
            )
            briefing = replace(briefing, workspace_context=updated_workspace)
        resolution = resolve(path)
        route_id = resolution.route_id if resolution is not None else "unrecognized"

        def logged_start_response(
            status: str, headers: list[tuple[str, str]]
        ) -> object:
            response_headers = list(headers)
            if renewed_cookie is not None and not any(
                header_name.lower() == "set-cookie"
                for header_name, _ in response_headers
            ):
                response_headers.append(("Set-Cookie", renewed_cookie))
            if clear_expired_cookie and not any(
                header_name.lower() == "set-cookie"
                for header_name, _ in response_headers
            ):
                response_headers.append(("Set-Cookie", _expired_cookie()))
            duration_ms = max(0.0, (perf_counter() - started_at) * 1000)
            logger.info(
                "%s %s %s %.3fms",
                method,
                route_id,
                status.split(" ", 1)[0],
                duration_ms,
            )
            return start_response(status, response_headers)

        anonymous_demo_access = (
            auth_required
            and demo_anonymous_allowed
            and session is None
            and briefing is not None
            and briefing.workspace_context.mode == "demonstration"
        )

        if method == "POST":
            if (
                auth_required
                and path not in _AUTH_PUBLIC_POST_ROUTES
                and session is None
                and not anonymous_demo_access
            ):
                return _redirect(logged_start_response, location="/login")
            if query:
                return _bad_request(logged_start_response, method, briefing)
            return _handle_post(
                logged_start_response,
                environ=environ,
                path=path,
                provider=active_provider,
                briefing=briefing,
                auth_runtime=auth_runtime,
                session=session,
                auth_required=auth_required,
            )

        if method == "unsupported":
            return _method_not_allowed(logged_start_response, method, briefing)
        if query:
            return _bad_request(logged_start_response, method, briefing)
        if path == "/login":
            login_body = _render_login_page(
                csrf_token=session.csrf_token if session is not None else "",
                include_reset_token_field=True,
            )
            return _emit(
                logged_start_response,
                status="200 OK",
                headers=_headers_for_html(login_body),
                body=login_body,
                method=method,
            )
        if path in {"/password-reset", "/password-reset/complete"}:
            login_body = _render_login_page(
                csrf_token=session.csrf_token if session is not None else "",
                include_reset_token_field=True,
            )
            return _emit(
                logged_start_response,
                status="200 OK",
                headers=_headers_for_html(login_body),
                body=login_body,
                method=method,
            )
        if resolution is not None and resolution.is_static:
            return _serve_css(logged_start_response, method, stylesheet)
        if (
            auth_required
            and path not in _AUTH_PUBLIC_GET_ROUTES
            and session is None
            and not anonymous_demo_access
        ):
            return _redirect(logged_start_response, location="/login")
        if resolution is None:
            return _not_found(logged_start_response, method, briefing)
        return _serve_page(
            logged_start_response, method, resolution, briefing
        )

    return application


def _default_provider() -> BriefingProvider:
    canonical_runtime_required = (
        os.getenv("BONSAAI_CANONICAL_RUNTIME", "").strip().lower()
        in {"1", "true", "yes", "on"}
    )
    try:
        from .governed_provider import OperationalWorkspaceProvider

        return OperationalWorkspaceProvider.create_default()
    except Exception as error:  # noqa: BLE001
        if canonical_runtime_required:
            logger.exception(
                "governed provider initialization failed in canonical runtime mode"
            )
            raise RuntimeError(
                "canonical_runtime_provider_initialization_failed"
            ) from error
        logger.error("governed provider initialization failed; falling back to synthetic")
        return SyntheticBriefingProvider()


def _redirect(
    start_response: StartResponse,
    *,
    location: str,
    status: str = "303 See Other",
    extra_headers: tuple[tuple[str, str], ...] = (),
) -> Iterable[bytes]:
    body = b""
    headers = [("Location", location)]
    headers.extend(extra_headers)
    headers.extend(_SECURITY_HEADERS)
    headers.append(("Content-Length", "0"))
    start_response(status, headers)
    return [body]


@dataclass(frozen=True)
class _UploadedFile:
    file_name: str
    media_type: str
    payload: bytes


def _read_request_body(environ: WSGIEnviron) -> tuple[str, bytes]:
    content_type = str(environ.get("CONTENT_TYPE", ""))
    content_length_raw = str(environ.get("CONTENT_LENGTH", "0") or "0")
    try:
        content_length = int(content_length_raw)
    except ValueError as error:
        raise ValueError("invalid_content_length") from error
    if content_length < 0:
        raise ValueError("invalid_content_length")
    payload = environ.get("wsgi.input")
    if payload is None:
        raise ValueError("missing_request_body")
    body = payload.read(content_length)
    return content_type, body


def _read_urlencoded(environ: WSGIEnviron) -> dict[str, str]:
    content_type, body = _read_request_body(environ)
    if not content_type.startswith("application/x-www-form-urlencoded"):
        raise ValueError("unsupported_content_type")
    try:
        decoded_body = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("invalid_encoding") from error
    parsed = parse_qs(decoded_body, keep_blank_values=False)
    return {
        key: values[0]
        for key, values in parsed.items()
        if values and values[0].strip()
    }


def _read_multipart(environ: WSGIEnviron) -> tuple[dict[str, str], _UploadedFile]:
    content_type, body = _read_request_body(environ)
    if not content_type.startswith("multipart/form-data"):
        raise ValueError("unsupported_content_type")
    message_bytes = (
        f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
        + body
    )
    message = BytesParser(policy=email_policy).parsebytes(message_bytes)
    if not message.is_multipart():
        raise ValueError("invalid_multipart_payload")
    fields: dict[str, str] = {}
    uploaded_file: _UploadedFile | None = None
    for part in message.iter_parts():
        field_name = part.get_param("name", header="content-disposition")
        if not field_name:
            continue
        file_name = part.get_filename()
        payload = part.get_payload(decode=True) or b""
        if file_name is not None:
            uploaded_file = _UploadedFile(
                file_name=file_name,
                media_type=part.get_content_type() or "application/octet-stream",
                payload=payload,
            )
            continue
        try:
            value = payload.decode("utf-8").strip()
        except UnicodeDecodeError as error:
            raise ValueError("invalid_encoding") from error
        if value:
            fields[field_name] = value
    if uploaded_file is None:
        raise ValueError("missing_uploaded_file")
    return fields, uploaded_file


def _handle_post(
    start_response: StartResponse,
    *,
    environ: WSGIEnviron,
    path: str,
    provider: BriefingProvider,
    briefing: ExecutiveBriefing | None,
    auth_runtime: AuthRuntime,
    session: AuthSession | None,
    auth_required: bool,
) -> Iterable[bytes]:
    def _assert_csrf(form: dict[str, str]) -> None:
        if session is None:
            raise ValueError("missing_session")
        submitted = form.get("csrf_token", "")
        if not submitted or submitted != session.csrf_token:
            raise ValueError("invalid_csrf")

    if path == "/login":
        form = _read_urlencoded(environ)
        login = auth_runtime.login(
            email=form.get("email", ""),
            password=form.get("password", ""),
            remember_device=form.get("remember_device", "").strip().lower()
            in {"1", "true", "yes", "on"},
        )
        if login.session is None:
            body = _render_login_page(
                message="Invalid credentials or account state prevented login.",
                include_reset_token_field=True,
            )
            return _emit(
                start_response,
                status="401 Unauthorized",
                headers=_headers_for_html(body),
                body=body,
                method="POST",
            )
        return _redirect(
            start_response,
            location="/",
            extra_headers=(("Set-Cookie", _build_session_cookie(login.session)),),
        )

    if path == "/logout":
        form = _read_urlencoded(environ)
        if session is not None:
            try:
                _assert_csrf(form)
            except ValueError:
                logger.error("runtime post operation rejected invalid input")
                return _error_page(
                    start_response,
                    method="POST",
                    briefing=briefing,
                    status="400 Bad Request",
                    message="The platform could not process the submitted workflow input.",
                )
        auth_runtime.logout(_parse_session_cookie(environ))
        return _redirect(
            start_response,
            location="/login",
            extra_headers=(("Set-Cookie", _expired_cookie()),),
        )

    if path == "/password-reset":
        form = _read_urlencoded(environ)
        _ = auth_runtime.request_password_reset(form.get("email", ""))
        body = _render_login_page(
            message=(
                "If an account exists for that email, a reset token was generated by "
                "the runtime administrator workflow."
            ),
            include_reset_token_field=True,
        )
        return _emit(
            start_response,
            status="200 OK",
            headers=_headers_for_html(body),
            body=body,
            method="POST",
        )

    if path == "/password-reset/complete":
        form = _read_urlencoded(environ)
        reset_completed = auth_runtime.reset_password(
            token=form.get("token", ""),
            new_password=form.get("new_password", ""),
        )
        body = _render_login_page(
            message=(
                "Password reset complete. Sign in with your new credentials."
                if reset_completed
                else "Password reset token invalid or expired."
            ),
            include_reset_token_field=True,
        )
        return _emit(
            start_response,
            status="200 OK" if reset_completed else "400 Bad Request",
            headers=_headers_for_html(body),
            body=body,
            method="POST",
        )

    if not isinstance(provider, InteractiveProvider):
        return _error_page(
            start_response,
            method="POST",
            briefing=briefing,
            status="405 Method Not Allowed",
            message="This provider does not allow runtime operations.",
            extra_headers=(("Allow", "GET, HEAD"),),
        )
    try:
        if path == "/knowledge-manager/admit":
            content_type = str(environ.get("CONTENT_TYPE", ""))
            if content_type.startswith("multipart/form-data"):
                form, uploaded = _read_multipart(environ)
                if auth_required and session is not None:
                    _assert_csrf(form)
                provider.admit_submission(
                    payload=uploaded.payload,
                    source_record_id=form.get("source_record_id", "source-record"),
                    file_name=uploaded.file_name,
                    media_type=uploaded.media_type,
                )
            else:
                form = _read_urlencoded(environ)
                if auth_required and session is not None:
                    _assert_csrf(form)
                provider.admit_document(
                    form.get("document_text", ""),
                    form.get("source_record_id", "source-record"),
                )
            return _redirect(start_response, location="/knowledge-manager")
        if path == "/knowledge-manager/promote-latest":
            form = _read_urlencoded(environ)
            if auth_required and session is not None:
                _assert_csrf(form)
            provider.promote_latest_candidate()
            return _redirect(start_response, location="/knowledge-manager")
        if path == "/knowledge-manager/reject-latest":
            form = _read_urlencoded(environ)
            if auth_required and session is not None:
                _assert_csrf(form)
            provider.reject_latest_candidate(
                form.get("reason", "human_review_rejected"),
            )
            return _redirect(start_response, location="/knowledge-manager")
        if path == "/organizational-intelligence/ask":
            form = _read_urlencoded(environ)
            if auth_required and session is not None:
                _assert_csrf(form)
            provider.ask_question(form.get("question", ""))
            return _redirect(start_response, location="/organizational-intelligence")
        if path == "/workspace/select":
            form = _read_urlencoded(environ)
            if auth_required and session is None:
                requested_mode = form.get("workspace_mode", "").strip().lower()
                if requested_mode != "demonstration":
                    raise RuntimeError("workspace_requires_authentication")
                provider.select_workspace(requested_mode)
                return _redirect(start_response, location="/")
            if auth_required and session is not None:
                _assert_csrf(form)
                organization_id = (
                    briefing.workspace_context.organization.organization_id
                    if briefing is not None
                    else session.selected_organization_id
                )
                auth_runtime.update_workspace_selection(
                    session=session,
                    workspace_mode=form.get("workspace_mode", ""),
                    organization_id=organization_id,
                )
            provider.select_workspace(form.get("workspace_mode", ""))
            return _redirect(start_response, location="/")
        if path == "/workspace/select-organization":
            form = _read_urlencoded(environ)
            if auth_required and session is not None:
                _assert_csrf(form)
                workspace_mode = (
                    briefing.workspace_context.mode
                    if briefing is not None
                    else session.selected_workspace_mode
                )
                auth_runtime.update_workspace_selection(
                    session=session,
                    workspace_mode=workspace_mode,
                    organization_id=form.get("organization_id", ""),
                )
            provider.select_organization(form.get("organization_id", ""))
            return _redirect(start_response, location="/")
        if path == "/workspace/reset-demo":
            form = _read_urlencoded(environ)
            if auth_required and session is not None:
                _assert_csrf(form)
            provider.reset_demo_workspace()
            return _redirect(start_response, location="/demo")
        return _error_page(
            start_response,
            method="POST",
            briefing=briefing,
            status="404 Not Found",
            message="The requested route is not part of this platform workflow.",
        )
    except ValueError:
        logger.error("runtime post operation rejected invalid input")
        return _error_page(
            start_response,
            method="POST",
            briefing=briefing,
            status="400 Bad Request",
            message="The platform could not process the submitted workflow input.",
        )
    except RuntimeError:
        logger.error("runtime post operation failed")
        return _error_page(
            start_response,
            method="POST",
            briefing=briefing,
            status="500 Internal Server Error",
            message="A runtime workflow error occurred while processing the request.",
        )


def _safe_briefing(provider: BriefingProvider) -> ExecutiveBriefing | None:
    """Return the provider briefing, or ``None`` if it cannot be produced."""
    try:
        briefing = provider.briefing()
        if not isinstance(briefing, ExecutiveBriefing):
            raise TypeError("provider returned an invalid briefing")
        return briefing
    except Exception:  # noqa: BLE001 - fail closed to a static error page
        logger.error("briefing provider failed")
        return None


def _safe_error_html(
    briefing: ExecutiveBriefing | None, *, status_label: str, message: str
) -> str:
    """Render a sanitized error page, falling back to a static document."""
    if briefing is not None:
        try:
            return render_error(
                briefing, status_label=status_label, message=message
            )
        except Exception:  # noqa: BLE001 - fall through to the static page
            logger.error("error page rendering failed")
    return _FALLBACK_ERROR_HTML


_FALLBACK_ERROR_HTML = (
    "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    "<title>Request problem \u2014 Bonsaai Platform Shell</title>"
    "<link rel=\"stylesheet\" href=\"/static/styles.css\"></head><body>"
    "<a class=\"skip-link\" href=\"#main-content\">Skip to main content</a>"
    "<header class=\"site-header\"><div class=\"brand\">"
    "<span class=\"product-title\">Bonsaai Platform Shell</span>"
    "<span class=\"badge synthetic\">Governed runtime</span></div>"
    "<p class=\"disconnected\">Local runtime scope only \u2014 governed state "
    "is limited to this runtime instance.</p></header>"
    "<nav class=\"primary-nav\" aria-label=\"Primary\"><ul>"
    "<li><a href=\"/\">Executive Dashboard</a></li>"
    "<li><a href=\"/knowledge-manager\">Knowledge Manager</a></li>"
    "<li><a href=\"/organizational-intelligence\">Organizational Intelligence</a></li>"
    "<li><a href=\"/organizational-memory\">Organizational Memory</a></li>"
    "<li><a href=\"/governance\">Governance</a></li>"
    "<li><a href=\"/audit\">Audit</a></li>"
    "<li><a href=\"/administration\">Administration</a></li>"
    "<li><a href=\"/demo\">Demonstration Mode</a></li></ul></nav>"
    "<main id=\"main-content\"><h1>Request problem</h1>"
    "<p>This governed runtime view could not serve the request. No request content "
    "is echoed and no organizational action is taken.</p>"
    "<p>Governed runtime boundary remains active.</p></main>"
    "<footer class=\"site-footer\"><p class=\"no-action\">This preview takes no "
    "organizational action and records no decision. It is non-operational and "
    "is not a deployment.</p><div class=\"footer-limitations\">"
    "<h2>Material limitations</h2><ul><li>No live information or service is "
    "available.</li></ul></div></footer></body></html>"
)


def _emit(
    start_response: StartResponse,
    *,
    status: str,
    headers: list[tuple[str, str]],
    body: bytes,
    method: str,
) -> Iterable[bytes]:
    start_response(status, headers)
    if method == "HEAD":
        return [b""]
    return [body]


def _serve_page(
    start_response: StartResponse,
    method: str,
    resolution: RouteResolution,
    briefing: ExecutiveBriefing | None,
) -> Iterable[bytes]:
    assert resolution.render is not None
    try:
        if briefing is None:
            raise RuntimeError("no briefing available")
        html = resolution.render(briefing)
        status = "200 OK"
    except Exception:  # noqa: BLE001 - fail closed with a sanitized page
        logger.error("render failure for route %s", resolution.route_id)
        html = _safe_error_html(
            briefing,
            status_label="500 Internal Server Error",
            message="An internal synthetic rendering error occurred.",
        )
        status = "500 Internal Server Error"
    body = html.encode("utf-8")
    return _emit(
        start_response,
        status=status,
        headers=_headers_for_html(body),
        body=body,
        method=method,
    )


def _serve_css(
    start_response: StartResponse,
    method: str,
    stylesheet: bytes,
) -> Iterable[bytes]:
    return _emit(
        start_response,
        status="200 OK",
        headers=_headers_for_css(stylesheet),
        body=stylesheet,
        method=method,
    )


def _error_page(
    start_response: StartResponse,
    *,
    method: str,
    briefing: ExecutiveBriefing | None,
    status: str,
    message: str,
    extra_headers: tuple[tuple[str, str], ...] = (),
) -> Iterable[bytes]:
    html = _safe_error_html(briefing, status_label=status, message=message)
    body = html.encode("utf-8")
    headers = _headers_for_html(body)
    headers.extend(extra_headers)
    return _emit(
        start_response,
        status=status,
        headers=headers,
        body=body,
        method=method,
    )


def _method_not_allowed(
    start_response: StartResponse,
    method: str,
    briefing: ExecutiveBriefing | None,
) -> Iterable[bytes]:
    return _error_page(
        start_response,
        method=method,
        briefing=briefing,
        status="405 Method Not Allowed",
        message="Only GET, HEAD, and allowlisted workflow POST requests are supported.",
        extra_headers=(("Allow", "GET, HEAD, POST"),),
    )


def _bad_request(
    start_response: StartResponse,
    method: str,
    briefing: ExecutiveBriefing | None,
) -> Iterable[bytes]:
    return _error_page(
        start_response,
        method=method,
        briefing=briefing,
        status="400 Bad Request",
        message="Query strings are not accepted by this synthetic preview.",
    )


def _not_found(
    start_response: StartResponse,
    method: str,
    briefing: ExecutiveBriefing | None,
) -> Iterable[bytes]:
    return _error_page(
        start_response,
        method=method,
        briefing=briefing,
        status="404 Not Found",
        message="The requested route is not part of this synthetic preview.",
    )


def validate_port(port: int) -> int:
    """Return the port if it is an integer within the allowed loopback range."""
    if isinstance(port, bool) or not isinstance(port, int):
        raise ValueError("port must be an integer")
    if port < MIN_PORT or port > MAX_PORT:
        raise ValueError(
            f"port must be between {MIN_PORT} and {MAX_PORT}, got {port}"
        )
    return port


def build_server(
    port: int, provider: BriefingProvider | None = None
) -> WSGIServer:
    """Build a loopback-only WSGI server bound to literal 127.0.0.1."""
    validate_port(port)
    application = create_app(provider)
    return make_server(
        LOOPBACK_HOST,
        port,
        application,
        handler_class=SanitizedRequestHandler,
    )
