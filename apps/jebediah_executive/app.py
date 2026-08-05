"""WSGI application, request validation, headers, and loopback server factory.

The application accepts GET and HEAD for allowlisted routes only, never reads a
request body, rejects every query string, sets restrictive security headers,
serves one reviewed local stylesheet, and logs only a sanitized method, route
identity, status, and duration. It stores no state, sets no cookie, and imports no
Collector, registry, memory, model, service, or external-integration package.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from importlib.resources import files
from time import perf_counter
from typing import Protocol
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

from .fixtures import SyntheticBriefingProvider
from .models import ExecutiveBriefing
from .rendering import render_error
from .routes import RouteResolution, resolve

LOOPBACK_HOST = "127.0.0.1"
MIN_PORT = 1024
MAX_PORT = 65535
_STYLESHEET_RESOURCE = "styles.css"
_SUPPORTED_METHODS = frozenset({"GET", "HEAD"})

logger = logging.getLogger("apps.jebediah_executive")

_SECURITY_HEADERS: tuple[tuple[str, str], ...] = (
    (
        "Content-Security-Policy",
        "default-src 'none'; style-src 'self'; base-uri 'none'; "
        "form-action 'none'; frame-ancestors 'none'",
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
    """Return a WSGI application over one immutable synthetic provider."""
    active_provider = (
        provider if provider is not None else SyntheticBriefingProvider()
    )
    briefing = _safe_briefing(active_provider)
    stylesheet = _load_stylesheet()

    def application(
        environ: WSGIEnviron, start_response: StartResponse
    ) -> Iterable[bytes]:
        started_at = perf_counter()
        requested_method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        method = (
            requested_method
            if requested_method in _SUPPORTED_METHODS
            else "unsupported"
        )
        path = str(environ.get("PATH_INFO", ""))
        query = str(environ.get("QUERY_STRING", ""))

        resolution = resolve(path)
        route_id = resolution.route_id if resolution is not None else "unrecognized"

        def logged_start_response(
            status: str, headers: list[tuple[str, str]]
        ) -> object:
            duration_ms = max(0.0, (perf_counter() - started_at) * 1000)
            logger.info(
                "%s %s %s %.3fms",
                method,
                route_id,
                status.split(" ", 1)[0],
                duration_ms,
            )
            return start_response(status, headers)

        if method == "unsupported":
            return _method_not_allowed(logged_start_response, method, briefing)
        if query:
            return _bad_request(logged_start_response, method, briefing)
        if resolution is None:
            return _not_found(logged_start_response, method, briefing)
        if resolution.is_static:
            return _serve_css(logged_start_response, method, stylesheet)
        return _serve_page(
            logged_start_response, method, resolution, briefing
        )

    return application


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
    "<title>Request problem \u2014 Jebediah Executive Product Shell</title>"
    "<link rel=\"stylesheet\" href=\"/static/styles.css\"></head><body>"
    "<a class=\"skip-link\" href=\"#main-content\">Skip to main content</a>"
    "<header class=\"site-header\"><div class=\"brand\">"
    "<span class=\"product-title\">Jebediah Executive Product Shell</span>"
    "<span class=\"badge synthetic\">Synthetic demonstration</span></div>"
    "<p class=\"disconnected\">Local, disconnected preview \u2014 no live "
    "service connection exists by design.</p></header>"
    "<nav class=\"primary-nav\" aria-label=\"Primary\"><ul>"
    "<li><a href=\"/\">Overview</a></li></ul></nav>"
    "<main id=\"main-content\"><h1>Request problem</h1>"
    "<p>This synthetic preview could not serve the request. No request content "
    "is echoed and no organizational action is taken.</p>"
    "<p>Synthetic demonstration only.</p></main>"
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
        message="Only GET and HEAD are supported by this synthetic preview.",
        extra_headers=(("Allow", "GET, HEAD"),),
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
