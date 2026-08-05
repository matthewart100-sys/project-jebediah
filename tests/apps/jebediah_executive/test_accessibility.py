"""Layer 6 - accessibility and usability tests for the Executive Product Shell.

These tests provide bounded engineering evidence (not WCAG certification) that
the shell exposes semantic regions and ordered headings, a keyboard-reachable
skip link and navigation, programmatic current-page state, descriptive link and
disclosure names, status and error text independent of color, fixed design
tokens whose documented contrast ratios meet 4.5:1 (normal text) and 3:1 (large
text and non-text indicators), 44x44 CSS-pixel targets, zoom- and
reduced-motion-friendly styling, narrow and wide layout rules, and a board
print rule that retains evidence, limitations, and the synthetic label.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from apps.jebediah_executive import rendering as r
from apps.jebediah_executive.fixtures import build_briefing
from apps.jebediah_executive.rendering import (
    STATE_ROUTE_TO_ENUM,
    render_ask_response,
    render_attention,
    render_board,
    render_knowledge,
    render_overview,
    render_state_detail,
)

BRIEFING = build_briefing()
CSS = (Path(r.__file__).with_name("static") / "styles.css").read_text(encoding="utf-8")


def _tokens() -> dict[str, str]:
    return dict(re.findall(r"(--color-[a-z-]+):\s*(#[0-9a-fA-F]{6})", CSS))


def _relative_luminance(hex_color: str) -> float:
    hex_color = hex_color.lstrip("#")
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a: str, b: str) -> float:
    la, lb = _relative_luminance(a), _relative_luminance(b)
    high, low = max(la, lb), min(la, lb)
    return (high + 0.05) / (low + 0.05)


# ---------------------------------------------------------------------------
# Semantic structure and keyboard reachability
# ---------------------------------------------------------------------------

def test_skip_link_targets_main_content() -> None:
    html = render_overview(BRIEFING)
    assert "<a class=\"skip-link\" href=\"#main-content\">Skip to main content</a>" in html
    assert "<main id=\"main-content\">" in html


def test_landmarks_present() -> None:
    html = render_overview(BRIEFING)
    assert "<header" in html
    assert "<nav class=\"primary-nav\" aria-label=\"Primary\">" in html
    assert "<main" in html
    assert "<footer" in html


def test_current_page_is_programmatic() -> None:
    html = render_knowledge(BRIEFING)
    assert "aria-current=\"page\"" in html


def test_links_and_disclosures_have_descriptive_names() -> None:
    html = render_knowledge(BRIEFING)
    # Disclosure summaries name the source reference, not a bare "here".
    for summary in re.findall(r"<summary>(.*?)</summary>", html):
        assert summary.strip()
        assert "click here" not in summary.lower()
    # No empty anchors.
    for anchor in re.findall(r"<a [^>]*>(.*?)</a>", html):
        assert anchor.strip()


def test_status_and_error_text_independent_of_color() -> None:
    # Ask response state is conveyed by a text label and enum value, not color.
    grounded = render_ask_response(BRIEFING, BRIEFING.ask_response("grounded-priorities"))
    assert "State: Grounded" in grounded
    assert "grounded" in grounded
    # Each briefing state detail names the state textually.
    for route_id, state in STATE_ROUTE_TO_ENUM.items():
        detail = render_state_detail(BRIEFING, route_id)
        assert state.value in detail


# ---------------------------------------------------------------------------
# Design tokens and contrast
# ---------------------------------------------------------------------------

def test_documented_tokens_exist() -> None:
    tokens = _tokens()
    for name in (
        "--color-text",
        "--color-bg",
        "--color-surface",
        "--color-accent",
        "--color-attention",
        "--color-failure",
        "--color-focus",
    ):
        assert name in tokens, name


def test_normal_text_contrast_meets_4_5() -> None:
    tokens = _tokens()
    assert _contrast(tokens["--color-text"], tokens["--color-bg"]) >= 4.5
    assert _contrast(tokens["--color-text"], tokens["--color-surface"]) >= 4.5
    assert _contrast(tokens["--color-muted"], tokens["--color-surface"]) >= 4.5
    assert _contrast(tokens["--color-accent"], tokens["--color-surface"]) >= 4.5
    assert _contrast(tokens["--color-failure"], tokens["--color-surface"]) >= 4.5


def test_reverse_and_nontext_contrast_meets_thresholds() -> None:
    tokens = _tokens()
    # White text on accent and attention badge backgrounds (normal text).
    assert _contrast("#ffffff", tokens["--color-accent"]) >= 4.5
    assert _contrast("#ffffff", tokens["--color-attention"]) >= 4.5
    # Focus indicator is a non-text indicator; needs at least 3:1.
    assert _contrast(tokens["--color-focus"], tokens["--color-surface"]) >= 3.0


# ---------------------------------------------------------------------------
# CSS behavior rules
# ---------------------------------------------------------------------------

def test_visible_focus_rule_present() -> None:
    assert ":focus-visible" in CSS
    assert "outline" in CSS


def test_targets_are_at_least_44px() -> None:
    assert "--target-min: 44px" in CSS
    assert "min-height: var(--target-min)" in CSS
    assert re.search(
        r"\.skip-link\s*\{[^}]*min-height:\s*var\(--target-min\)",
        CSS,
        re.DOTALL,
    )


def test_zoom_friendly_text_sizing() -> None:
    # Body text is expressed in rem so 200% zoom scales it.
    assert re.search(r"body\s*\{[^}]*font-size:\s*1rem", CSS, re.DOTALL)


def test_narrow_and_wide_layout_rules() -> None:
    # A narrow breakpoint supports 320 CSS pixels.
    assert re.search(r"@media\s*\(max-width:\s*30rem\)", CSS)
    # A bounded max width keeps line length reasonable at 1280 pixels.
    assert "--max-width" in CSS
    assert "max-width: var(--max-width)" in CSS


def test_reduced_motion_rule_present() -> None:
    assert "prefers-reduced-motion: reduce" in CSS


def test_board_print_retains_evidence_limitations_and_label() -> None:
    print_block = CSS[CSS.index("@media print") :]
    # Only chrome (nav and skip link) is hidden in print.
    hidden = re.search(r"\.primary-nav,\s*\.skip-link\s*\{\s*display: none;", print_block)
    assert hidden is not None
    # Footer, limitations, references, and evidence are explicitly kept visible.
    assert re.search(
        r"\.footer-limitations,[\s\S]*?\.references,[\s\S]*?\.evidence-meta,"
        r"[\s\S]*?\.limitations\s*\{\s*display: block;",
        print_block,
    )
    # The synthetic badge remains visible (re-styled, not removed) in print.
    assert ".badge.synthetic" in print_block
    # A rendered board page keeps evidence and limitations content.
    board = render_board(BRIEFING)
    assert "Material limitations" in board
    assert "Coverage and boundaries" in board


def test_no_two_dimensional_scroll_forced() -> None:
    # No fixed pixel width larger than 320 is imposed on the body or main.
    assert not re.search(r"(body|main)\s*\{[^}]*width:\s*\d{3,}px", CSS, re.DOTALL)


def test_responsive_workspace_table_collapses_to_cards() -> None:
    # Within the 320-pixel breakpoint, the workspace table collapses to stacked
    # cards whose cells expose their column name via data-label, so no required
    # content is lost and no page-wide horizontal scroll is forced.
    narrow = CSS[CSS.index("@media (max-width: 30rem)") :]
    narrow = narrow[: narrow.index("@media", 5)] if "@media" in narrow[5:] else narrow
    assert ".workspace-table td" in narrow
    assert "display: block" in narrow
    assert "content: attr(data-label)" in narrow
    # The header row is visually hidden but preserved for assistive technology.
    assert ".workspace-table thead" in narrow


def test_workspace_cells_carry_data_labels_for_responsive_layout() -> None:
    from apps.jebediah_executive.rendering import render_workspace

    html = render_workspace(BRIEFING)
    for label in ("Kind", "State", "Source references", "Last changed", "Limitations"):
        assert f"data-label=\"{label}\"" in html, label
