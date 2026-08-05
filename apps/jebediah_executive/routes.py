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
    render_attention,
    render_ask_index,
    render_ask_response,
    render_board,
    render_knowledge,
    render_next,
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
WORKSPACE_INTAKE_PATH = "/workspace/intake"
WORKSPACE_RECOVER_PATH = "/workspace/recover"

PRODUCT_ROUTES: tuple[str, ...] = (
    "/",
    "/attention",
    "/knowledge",
    "/next",
    "/workspace",
    "/ask",
    "/board",
    "/states",
    STATIC_STYLESHEET_PATH,
)

WORKSPACE_MUTATION_ROUTES: tuple[str, ...] = (
    WORKSPACE_INTAKE_PATH,
    WORKSPACE_RECOVER_PATH,
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
_WORKSPACE_SUBMISSIONS_PREFIX = "/workspace/submissions/"


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


def submission_detail_id(path: str) -> str | None:
    if not path.startswith(_WORKSPACE_SUBMISSIONS_PREFIX):
        return None
    submission_id = path[len(_WORKSPACE_SUBMISSIONS_PREFIX):]
    if (
        not submission_id
        or "/" in submission_id
        or "\\" in submission_id
        or "\x00" in submission_id
    ):
        return None
    return submission_id


def submission_review_id(path: str) -> str | None:
    detail = submission_detail_id(path.removesuffix("/review"))
    if detail is None or not path.endswith("/review"):
        return None
    return detail


def submission_delete_id(path: str) -> str | None:
    detail = submission_detail_id(path.removesuffix("/delete"))
    if detail is None or not path.endswith("/delete"):
        return None
    return detail
