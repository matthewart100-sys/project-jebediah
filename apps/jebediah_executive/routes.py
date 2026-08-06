"""Fixed route resolution for the Executive Product Shell.

This module maps an exact, decoded request path to a route identity and a
renderer. It knows nothing about HTTP methods, headers, queries, sockets, or
logging. Only the fixed route table and allowlisted subroute identifiers
resolve; every other path returns ``None`` for a safe 404.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .models import ExecutiveBriefing
from .rendering import (
    STATE_ROUTE_TO_ENUM,
    render_administration,
    render_attention,
    render_audit,
    render_demo_walkthrough,
    render_ask_index,
    render_ask_response,
    render_board,
    render_governance,
    render_knowledge,
    render_knowledge_manager,
    render_next,
    render_organizational_intelligence,
    render_organizational_memory,
    render_overview,
    render_state_detail,
    render_states_gallery,
    render_workspace,
)

ALLOWLISTED_PRESET_IDS: tuple[str, ...] = (
    "grounded-priorities",
    "insufficient-program-outcomes",
    "failed-source-review",
)

ALLOWLISTED_STATE_IDS: tuple[str, ...] = tuple(STATE_ROUTE_TO_ENUM.keys())

STATIC_STYLESHEET_PATH = "/static/styles.css"

PRODUCT_ROUTES: tuple[str, ...] = (
    "/",
    "/demo",
    "/knowledge-manager",
    "/organizational-intelligence",
    "/organizational-memory",
    "/governance",
    "/audit",
    "/administration",
    "/attention",
    "/knowledge",
    "/next",
    "/workspace",
    "/ask",
    "/board",
    "/states",
    STATIC_STYLESHEET_PATH,
)

Renderer = Callable[[ExecutiveBriefing], str]


@dataclass(frozen=True)
class RouteResolution:
    """A resolved allowlisted route."""

    route_id: str
    is_static: bool
    render: Renderer | None


_SIMPLE_ROUTES: dict[str, tuple[str, Renderer]] = {
    "/": ("overview", render_overview),
    "/demo": ("demo", render_demo_walkthrough),
    "/knowledge-manager": ("knowledge-manager", render_knowledge_manager),
    "/organizational-intelligence": (
        "organizational-intelligence",
        render_organizational_intelligence,
    ),
    "/organizational-memory": ("organizational-memory", render_organizational_memory),
    "/governance": ("governance", render_governance),
    "/audit": ("audit", render_audit),
    "/administration": ("administration", render_administration),
    "/attention": ("attention", render_attention),
    "/knowledge": ("knowledge", render_knowledge),
    "/next": ("next", render_next),
    "/workspace": ("workspace", render_workspace),
    "/ask": ("ask", render_ask_index),
    "/board": ("board", render_board),
    "/states": ("states", render_states_gallery),
}

_ASK_PREFIX = "/ask/"
_STATE_PREFIX = "/states/"


def _render_ask_preset(question_id: str) -> Renderer:
    def render(briefing: ExecutiveBriefing) -> str:
        response = briefing.ask_response(question_id)
        if response is None:  # pragma: no cover - guarded by allowlist
            raise KeyError(question_id)
        return render_ask_response(briefing, response)

    return render


def _render_state_detail(route_id: str) -> Renderer:
    def render(briefing: ExecutiveBriefing) -> str:
        return render_state_detail(briefing, route_id)

    return render


def resolve(path: str) -> RouteResolution | None:
    """Resolve an exact decoded path to a route, or ``None`` for a safe 404."""
    if path in _SIMPLE_ROUTES:
        route_id, renderer = _SIMPLE_ROUTES[path]
        return RouteResolution(route_id=route_id, is_static=False, render=renderer)

    if path == STATIC_STYLESHEET_PATH:
        return RouteResolution(route_id="styles", is_static=True, render=None)

    if path.startswith(_ASK_PREFIX):
        preset = path[len(_ASK_PREFIX):]
        if preset in ALLOWLISTED_PRESET_IDS:
            return RouteResolution(
                route_id="ask-preset",
                is_static=False,
                render=_render_ask_preset(preset),
            )
        return None

    if path.startswith(_STATE_PREFIX):
        state_id = path[len(_STATE_PREFIX):]
        if state_id in ALLOWLISTED_STATE_IDS:
            return RouteResolution(
                route_id="state-detail",
                is_static=False,
                render=_render_state_detail(state_id),
            )
        return None

    return None
