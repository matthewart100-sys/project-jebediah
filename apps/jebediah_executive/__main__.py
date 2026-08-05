"""Command-line entry point for the local synthetic preview server.

Usage::

    python -B -m apps.jebediah_executive --port <1024..65535>

The server binds only to loopback ``127.0.0.1``. There is no host, address,
interface, environment, data-source, file, service, or credential option. A
bind failure is reported visibly and exits non-zero. Ctrl+C shuts the server
down cleanly.
"""

from __future__ import annotations

import argparse
import sys

from .app import LOOPBACK_HOST, MAX_PORT, MIN_PORT, build_server, validate_port


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apps.jebediah_executive",
        description=(
            "Local synthetic preview of the Jebediah Executive Product Shell. "
            "Serves fabricated demonstration content on loopback only. This is "
            "not a deployment and connects to no real data or service."
        ),
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        metavar=f"{{{MIN_PORT}..{MAX_PORT}}}",
        help="TCP port on 127.0.0.1 to bind (inclusive range %d-%d)."
        % (MIN_PORT, MAX_PORT),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, start the loopback server, and serve until interrupted."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        port = validate_port(args.port)
    except ValueError as exc:
        parser.error(str(exc))
        return 2  # pragma: no cover - argparse.error raises SystemExit

    try:
        server = build_server(port)
    except OSError as exc:
        print(
            f"Failed to bind {LOOPBACK_HOST}:{port}: {exc}",
            file=sys.stderr,
        )
        return 1

    print(
        f"Jebediah Executive Product Shell (synthetic preview) is serving on "
        f"http://{LOOPBACK_HOST}:{port}/",
    )
    print(
        "Synthetic demonstration only. Disconnected and non-operational. "
        "No real data, service, deployment, or action authority. "
        "Press Ctrl+C to stop.",
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down synthetic preview.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
