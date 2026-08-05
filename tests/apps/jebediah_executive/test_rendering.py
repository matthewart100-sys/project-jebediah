"""Layer 3 - rendering tests for the Executive Product Shell.

These tests prove that every rendered document is a complete, escaped, semantic
page: one level-one heading, ordered headings, language, charset, viewport,
skip link, header, navigation, main landmark, and footer; that the synthetic,
no-action, fixed-clock, coverage, limitations, and disconnected boundaries are
visible on every page; that evidence, freshness, uncertainty, and authority are
shown; that source references are local disclosures; that no score, percentage,
or unsupported verification label appears; and that all dynamic values are
HTML-escaped.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from apps.jebediah_executive import rendering as r
from apps.jebediah_executive.fixtures import build_briefing
from apps.jebediah_executive.rendering import (
    DISCONNECTED_STATEMENT,
    NO_ACTION_STATEMENT,
    STATE_ROUTE_TO_ENUM,
    SYNTHETIC_BADGE,
    render_ask_index,
    render_ask_response,
    render_attention,
    render_board,
    render_error,
    render_knowledge,
    render_next,
    render_overview,
    render_state_detail,
    render_states_gallery,
    render_workspace,
)

BRIEFING = build_briefing()


def _core_pages() -> list[tuple[str, str]]:
    return [
        ("overview", render_overview(BRIEFING)),
        ("attention", render_attention(BRIEFING)),
        ("knowledge", render_knowledge(BRIEFING)),
        ("next", render_next(BRIEFING)),
        ("workspace", render_workspace(BRIEFING)),
        ("ask", render_ask_index(BRIEFING)),
        ("board", render_board(BRIEFING)),
        ("states", render_states_gallery(BRIEFING)),
    ]


def _all_pages() -> list[tuple[str, str]]:
    pages = _core_pages()
    for response in BRIEFING.ask_responses:
        pages.append((f"ask-{response.question_id}", render_ask_response(BRIEFING, response)))
    for route_id in STATE_ROUTE_TO_ENUM:
        pages.append((f"state-{route_id}", render_state_detail(BRIEFING, route_id)))
    pages.append(("error", render_error(BRIEFING, status_label="404 Not Found", message="x")))
    return pages


@pytest.mark.parametrize("name,html", _all_pages())
def test_document_skeleton(name: str, html: str) -> None:
    assert html.startswith("<!DOCTYPE html>"), name
    assert "<html lang=\"en\">" in html, name
    assert "<meta charset=\"utf-8\">" in html, name
    assert "name=\"viewport\"" in html, name
    assert "<link rel=\"stylesheet\" href=\"/static/styles.css\">" in html, name
    assert "class=\"skip-link\" href=\"#main-content\"" in html, name
    assert "<header" in html and "</header>" in html, name
    assert "<nav" in html and "</nav>" in html, name
    assert "<main id=\"main-content\">" in html, name
    assert "<footer" in html and "</footer>" in html, name


@pytest.mark.parametrize("name,html", _all_pages())
def test_exactly_one_h1_and_ordered_headings(name: str, html: str) -> None:
    assert html.count("<h1>") == 1, name
    levels = [int(m) for m in re.findall(r"<h([1-4])[ >]", html)]
    assert levels[0] == 1, name
    # No heading level jumps by more than one from the previous maximum seen.
    seen_max = 0
    for level in levels:
        assert level <= seen_max + 1, (name, levels)
        seen_max = max(seen_max, level)


@pytest.mark.parametrize("name,html", _all_pages())
def test_boundary_labels_on_every_page(name: str, html: str) -> None:
    assert SYNTHETIC_BADGE in html, name
    assert NO_ACTION_STATEMENT in html, name
    assert DISCONNECTED_STATEMENT in html, name
    # Fixed synthetic clock and coverage scope from the header.
    assert "Fixed synthetic clock:" in html, name
    assert "Coverage scope:" in html, name
    # Footer material limitations list.
    assert "Material limitations" in html, name


@pytest.mark.parametrize("name,html", _core_pages())
def test_no_external_resources_or_scripts(name: str, html: str) -> None:
    assert "http://" not in html, name
    assert "https://" not in html, name
    assert "<script" not in html, name
    assert "<img" not in html, name
    assert "onerror=" not in html and "onclick=" not in html, name


@pytest.mark.parametrize("name,html", _all_pages())
def test_no_score_percentage_or_confidence(name: str, html: str) -> None:
    lowered = html.lower()
    assert "confidence" not in lowered, name
    assert "probability" not in lowered, name
    assert not re.search(r"\d\s*%", html), name


def test_current_navigation_is_programmatic() -> None:
    html = render_attention(BRIEFING)
    assert "aria-current=\"page\"" in html
    assert "class=\"current\"" in html


def test_overview_shows_derived_counts() -> None:
    html = render_overview(BRIEFING)
    counts = BRIEFING.summary_counts
    assert f"<dd>{counts.priority_count}</dd>" in html
    assert f"<dd>{counts.eligible_source_count}</dd>" in html


def test_items_show_evidence_freshness_and_uncertainty() -> None:
    html = render_attention(BRIEFING)
    assert "Uncertainty" in html
    assert "Evidence" in html or "evidence" in html
    # A freshness label appears.
    assert any(label in html for label in ("Current", "Aging", "Stale", "Unknown"))


def test_attention_remains_informational_and_links_next_kind() -> None:
    html = render_attention(BRIEFING)
    # Attention items reference a separately linked next-item kind.
    assert "Related next step" in html
    # The attention section never claims its own next_kind heading label of a
    # decision; it defers to the linked next item.
    assert "informational attention" in html.lower()


def test_attention_related_links_are_topically_coherent() -> None:
    # The related next-step links on the attention page name next items that
    # genuinely correspond to their attention topic, not unrelated items.
    html = render_attention(BRIEFING)
    grant_next = BRIEFING.item_by_id("demo-item-next-grant-extension")
    cash_next = BRIEFING.item_by_id("demo-item-next-cash-reconciliation")
    assert grant_next.title in html
    assert cash_next.title in html
    # The disproven mismatch topics (downtown lease / conflict-of-interest
    # disclosure tracker) no longer appear as linked next items.
    assert "downtown" not in html.lower()
    assert "conflict-of-interest" not in html.lower()


def test_source_references_are_local_disclosures() -> None:
    html = render_knowledge(BRIEFING)
    assert "<details class=\"reference\">" in html
    # No reference is an anchor to an external or absolute resource.
    assert "href=\"http" not in html


def test_workspace_has_table_and_no_input_controls() -> None:
    html = render_workspace(BRIEFING)
    assert "<table class=\"workspace-table\">" in html
    for control in ("<form", "<input", "<textarea", "<button", "type=\"file\""):
        assert control not in html, control


def test_workspace_table_cells_carry_responsive_data_labels() -> None:
    # Every non-header body cell names its column via a data-label so the
    # responsive card layout at 320 CSS pixels loses no content.
    html = render_workspace(BRIEFING)
    for label in (
        "Kind",
        "State",
        "Briefing eligibility",
        "Source references",
        "Last changed",
        "Limitations",
    ):
        assert f"data-label=\"{label}\"" in html, label


def test_workspace_shows_last_changed_and_activity_source_refs() -> None:
    html = render_workspace(BRIEFING)
    # The workspace last-changed timestamp is present for a known record.
    assert "data-label=\"Last changed\"" in html
    assert "UTC" in html  # formatted timezone-aware capture time
    # Each activity names its safe source reference IDs or an explicit absence.
    assert "source references" in html
    assert "demo-src-" in html or "none claimed" in html


def test_ask_index_has_no_free_form_input() -> None:
    html = render_ask_index(BRIEFING)
    for control in ("<form", "<input", "<textarea", "<button"):
        assert control not in html, control
    assert "/ask/grounded-priorities" in html


def test_ask_response_states_and_boundaries() -> None:
    grounded = render_ask_response(BRIEFING, BRIEFING.ask_response("grounded-priorities"))
    assert "Grounded" in grounded
    assert "Grounded means" in grounded  # limited to cited fabricated records
    assert "Uncertainty" in grounded
    assert SYNTHETIC_BADGE in grounded

    insufficient = render_ask_response(
        BRIEFING, BRIEFING.ask_response("insufficient-program-outcomes")
    )
    assert "Insufficient" in insufficient
    assert "No answer is fabricated" in insufficient

    failed = render_ask_response(BRIEFING, BRIEFING.ask_response("failed-source-review"))
    assert "Failed" in failed


def test_states_gallery_and_details_distinguish_without_color() -> None:
    gallery = render_states_gallery(BRIEFING)
    for route_id, state in STATE_ROUTE_TO_ENUM.items():
        assert f"/states/{route_id}" in gallery
        # The exact enum value is visible as text (not color-encoded).
        assert state.value in gallery
        detail = render_state_detail(BRIEFING, route_id)
        assert state.value in detail
        # A decorative glyph accompanies the text label.
        assert "aria-hidden=\"true\"" in detail


def test_each_state_detail_shows_substantive_fixed_content() -> None:
    coverage = BRIEFING.coverage
    counts = BRIEFING.summary_counts

    loading = render_state_detail(BRIEFING, "loading")
    assert "class=\"skeleton\"" in loading
    assert "skeleton-line" in loading
    assert "No background fetch" in loading

    empty = render_state_detail(BRIEFING, "empty")
    for subject in coverage.covered_subjects:
        assert subject in empty
    assert "<dd>0</dd>" in empty
    assert "never means" in empty

    partial = render_state_detail(BRIEFING, "partial")
    assert "Affected sections" in partial
    assert "Unavailable synthetic inputs" in partial
    for subject in coverage.missing_subjects:
        assert subject in partial

    stale = render_state_detail(BRIEFING, "stale")
    assert "Captured at" in stale
    for subject in coverage.stale_subjects:
        assert subject in stale

    insufficient = render_state_detail(BRIEFING, "insufficient-evidence")
    assert "Missing evidence requirements" in insufficient
    assert "No fabricated answer is produced" in insufficient
    for subject in coverage.missing_subjects:
        assert subject in insufficient

    held = render_state_detail(BRIEFING, "held")
    assert coverage.held_subjects[0] in held
    assert "human or policy gate" in held
    assert "no ordinary eligibility" in held

    failed = render_state_detail(BRIEFING, "failed")
    assert "Sanitized failure" in failed
    assert "No internal detail" in failed

    unauthorized = render_state_detail(BRIEFING, "unauthorized")
    assert "No synthetic data" in unauthorized

    unavailable = render_state_detail(BRIEFING, "unavailable")
    assert "cannot be assembled safely" in unavailable

    disconnected = render_state_detail(BRIEFING, "disconnected")
    assert "No connection to" in disconnected

    ready = render_state_detail(BRIEFING, "ready")
    assert f"<dd>{coverage.eligible_item_count}</dd>" in ready
    assert f"<dd>{coverage.source_reference_count}</dd>" in ready
    assert f"<dd>{counts.priority_count}</dd>" in ready
    assert "Examples of eligible items" in ready


def test_state_detail_is_render_only_and_does_not_mutate_fixture() -> None:
    for route_id in STATE_ROUTE_TO_ENUM:
        render_state_detail(BRIEFING, route_id)
    # The module-level briefing remains value-equal to a fresh build.
    assert BRIEFING == build_briefing()


def test_evidence_meta_shows_lifecycle_and_current_state() -> None:
    html = render_attention(BRIEFING)
    assert "<dt>Lifecycle</dt>" in html
    assert "active" in html  # enum value visible
    assert "<dt>Current state</dt>" in html
    assert "Ordinary and eligible for the briefing" in html


def test_coverage_block_shows_derived_counts() -> None:
    html = render_overview(BRIEFING)
    coverage = BRIEFING.coverage
    assert "Coverage counts (derived)" in html
    assert f"<dd>{coverage.eligible_item_count}</dd>" in html
    assert f"<dd>{coverage.source_reference_count}</dd>" in html


def test_dynamic_values_are_escaped() -> None:
    # The error renderer escapes an injected unsafe message literally.
    html = render_error(
        BRIEFING,
        status_label="400 Bad Request",
        message="<script>alert('x')</script> & \"quote\"",
    )
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
    assert "&amp;" in html


def test_error_page_reflects_no_request_content() -> None:
    html = render_error(BRIEFING, status_label="404 Not Found", message="Not here")
    assert "No request content is echoed" in html
    assert "takes no action" in html


def test_stylesheet_is_local_and_has_required_rules() -> None:
    css_path = Path(r.__file__).with_name("static") / "styles.css"
    css = css_path.read_text(encoding="utf-8")
    assert ":focus-visible" in css
    assert "@media" in css
    assert "prefers-reduced-motion" in css
    assert "@media print" in css
    # No external references in the stylesheet.
    assert "http://" not in css and "https://" not in css
    assert "url(" not in css
