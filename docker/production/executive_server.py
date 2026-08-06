from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from wsgiref.simple_server import WSGIServer, make_server

from apps.jebediah_executive.app import SanitizedRequestHandler, create_app, validate_port


def _health_payload() -> bytes:
    return json.dumps(
        {
            "status": "online",
            "service": "bonsaai-executive-shell",
            "time": datetime.now(timezone.utc).isoformat(),
        }
    ).encode("utf-8")


def _app_with_health():
    app = create_app()

    def application(environ, start_response):
        path = str(environ.get("PATH_INFO") or "")
        method = str(environ.get("REQUEST_METHOD") or "GET").upper()
        if method == "GET" and path in {"/health", "/healthz"}:
            body = _health_payload()
            headers = [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(body))),
                ("Cache-Control", "no-store"),
            ]
            start_response("200 OK", headers)
            return [body]
        return app(environ, start_response)

    return application


def _build_server() -> WSGIServer:
    host = os.getenv("EXECUTIVE_BIND_HOST", "0.0.0.0").strip() or "0.0.0.0"
    port_raw = os.getenv("EXECUTIVE_PORT", "8080").strip()
    port = validate_port(int(port_raw))
    return make_server(
        host,
        port,
        _app_with_health(),
        handler_class=SanitizedRequestHandler,
    )


def main() -> int:
    server = _build_server()
    print(
        "Bonsaai Executive Shell runtime serving at "
        f"http://{server.server_address[0]}:{server.server_address[1]}/"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
