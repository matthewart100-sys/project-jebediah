"""Escaped semantic HTML rendering for the Executive Product Shell.

Every dynamic value is HTML-escaped before output. The renderer manufactures no
domain values, performs no input, and emits no external resource, script, image,
remote font, or absolute link. Enumerations are presented in plain language while
their exact machine value remains visible for transparency.
"""

from __future__ import annotations

from datetime import datetime
from html import escape

from .models import (
    AskResponse,
    AskState,
    BriefingItem,
    BriefingSection,
    BriefingState,
    CoverageSummary,
    EvidenceClassification,
    ExecutiveBriefing,
    FreshnessState,
    KnowledgeKind,
    LifecycleState,
    NextContext,
    NextItemKind,
    PermittedNextStep,
    SourceReference,
    UncertaintyState,
    WorkspaceKind,
    WorkspaceMode,
    WorkspaceRecord,
    WorkspaceState,
)

SYNTHETIC_BADGE = "Governed intelligence"
NO_ACTION_STATEMENT = (
    "Human governance approval remains required for organizational decisions."
)
DISCONNECTED_STATEMENT = (
    "Local runtime scope only \u2014 governed state is limited to this runtime instance."
)

_NAV = (
    ("executive-dashboard", "/", "Dashboard"),
    ("knowledge-manager", "/knowledge-manager", "Knowledge Manager"),
    (
        "organizational-intelligence",
        "/organizational-intelligence",
        "Ask Jebediah",
    ),
    ("organizational-memory", "/organizational-memory", "Approved Knowledge"),
    ("governance", "/governance", "Governance"),
    ("audit", "/audit", "Audit Trail"),
    ("administration", "/administration", "Administration"),
)

_SECTION_LABELS = {
    BriefingSection.HAPPENING: "What is happening",
    BriefingSection.ATTENTION: "Needs attention",
    BriefingSection.KNOW: "What Jebediah knows",
    BriefingSection.NEXT: "What happens next",
}

_EVIDENCE_LABELS = {
    EvidenceClassification.VERIFIED_FACT: "Verified fact",
    EvidenceClassification.REPORTED_FACT: "Reported fact",
    EvidenceClassification.WORKING_ASSUMPTION: "Working assumption",
    EvidenceClassification.OPEN_QUESTION: "Open question",
    EvidenceClassification.DERIVED_SUMMARY: "Derived summary",
}

_FRESHNESS_LABELS = {
    FreshnessState.CURRENT: "Current",
    FreshnessState.AGING: "Aging",
    FreshnessState.STALE: "Stale",
    FreshnessState.UNKNOWN: "Unknown",
    FreshnessState.NOT_APPLICABLE: "Not applicable",
}

_UNCERTAINTY_LABELS = {
    UncertaintyState.BOUNDED: "Bounded",
    UncertaintyState.INCOMPLETE: "Incomplete",
    UncertaintyState.CONFLICTING: "Conflicting",
    UncertaintyState.UNKNOWN: "Unknown",
    UncertaintyState.NOT_APPLICABLE: "Not applicable",
}

_KNOWLEDGE_LABELS = {
    KnowledgeKind.MATERIAL_CHANGE: "Material change",
    KnowledgeKind.DECISION: "Decision",
    KnowledgeKind.RISK: "Risk",
    KnowledgeKind.OPPORTUNITY: "Opportunity",
    KnowledgeKind.KNOWLEDGE_GAP: "Knowledge gap",
}

_NEXT_KIND_LABELS = {
    NextItemKind.DECISION_REQUIRED: "Decision required",
    NextItemKind.ORGANIZATIONAL_GATE: "Organizational gate",
    NextItemKind.ACTION_CANDIDATE: "Action candidate",
    NextItemKind.INFORMATIONAL_ATTENTION: "Informational attention",
}

_NEXT_CONTEXT_LABELS = {
    NextContext.APPROVED_PLAN: "Approved plan",
    NextContext.UNRESOLVED_GATE: "Unresolved gate",
    NextContext.DECISION_REQUEST: "Decision request",
    NextContext.POSSIBLE_ACTION_CANDIDATE: "Possible action candidate",
    NextContext.INFORMATION_GATHERING_NEED: "Information-gathering need",
}

_STEP_LABELS = {
    PermittedNextStep.NAVIGATE: "Navigate to related detail",
    PermittedNextStep.HUMAN_REVIEW: "Human review required",
}

_LIFECYCLE_LABELS = {
    LifecycleState.ACTIVE: "Active",
    LifecycleState.SUPERSEDED: "Superseded",
    LifecycleState.ARCHIVED: "Archived",
}

_ASK_STATE_LABELS = {
    AskState.GROUNDED: "Evidence-backed",
    AskState.INSUFFICIENT: "Insufficient evidence",
    AskState.FAILED: "Failed",
}

_ASK_STATE_SYMBOLS = {
    AskState.GROUNDED: "\u25c6",
    AskState.INSUFFICIENT: "\u25cb",
    AskState.FAILED: "\u2716",
}

STATE_ROUTE_TO_ENUM = {
    "ready": BriefingState.READY,
    "loading": BriefingState.LOADING,
    "empty": BriefingState.EMPTY,
    "partial": BriefingState.PARTIAL,
    "stale": BriefingState.STALE,
    "insufficient-evidence": BriefingState.INSUFFICIENT_EVIDENCE,
    "held": BriefingState.HELD,
    "failed": BriefingState.FAILED,
    "unauthorized": BriefingState.UNAUTHORIZED,
    "unavailable": BriefingState.UNAVAILABLE,
    "disconnected": BriefingState.DISCONNECTED,
}

_STATE_LABELS = {
    BriefingState.READY: "Ready",
    BriefingState.LOADING: "Loading",
    BriefingState.EMPTY: "Empty",
    BriefingState.PARTIAL: "Partial",
    BriefingState.STALE: "Stale",
    BriefingState.INSUFFICIENT_EVIDENCE: "Insufficient evidence",
    BriefingState.HELD: "Held",
    BriefingState.FAILED: "Failed",
    BriefingState.UNAUTHORIZED: "Unauthorized",
    BriefingState.UNAVAILABLE: "Unavailable",
    BriefingState.DISCONNECTED: "Disconnected",
}

_STATE_SYMBOLS = {
    BriefingState.READY: "\u25c9",
    BriefingState.LOADING: "\u25cc",
    BriefingState.EMPTY: "\u25cb",
    BriefingState.PARTIAL: "\u25d0",
    BriefingState.STALE: "\u25d1",
    BriefingState.INSUFFICIENT_EVIDENCE: "\u25c7",
    BriefingState.HELD: "\u25a0",
    BriefingState.FAILED: "\u2716",
    BriefingState.UNAUTHORIZED: "\u2298",
    BriefingState.UNAVAILABLE: "\u2205",
    BriefingState.DISCONNECTED: "\u25ac",
}

_STATE_DESCRIPTIONS = {
    BriefingState.READY: "Eligible synthetic evidence is shown together with its "
    "limitations.",
    BriefingState.LOADING: "A skeleton structure is shown. No background fetch is "
    "occurring in this disconnected demonstration.",
    BriefingState.EMPTY: "The covered synthetic scope is shown with zero eligible "
    "items. This never means that nothing is happening.",
    BriefingState.PARTIAL: "Only some sections are available. Affected sections and "
    "the unavailable synthetic inputs are named.",
    BriefingState.STALE: "The fabricated capture time, the stale evidence, and the "
    "limitation are shown together.",
    BriefingState.INSUFFICIENT_EVIDENCE: "The missing evidence requirement is named "
    "and no fabricated answer is produced.",
    BriefingState.HELD: "A human or policy gate applies. The information has no "
    "ordinary eligibility and its content is not shown.",
    BriefingState.FAILED: "A sanitized failure is shown while the synthetic and "
    "no-action boundary is retained.",
    BriefingState.UNAUTHORIZED: "Access would be required in a future live system. No "
    "data is shown here.",
    BriefingState.UNAVAILABLE: "The briefing cannot be assembled safely, so no "
    "partial values are presented as ready.",
    BriefingState.DISCONNECTED: "No service connection exists by design in this "
    "Phase 3A synthetic preview.",
}


def _fmt(value: datetime | None) -> str:
    """Format an absolute timezone-aware timestamp or an explicit absence."""
    if value is None:
        return "not recorded"
    return value.strftime("%Y-%m-%d %H:%M %Z") or value.isoformat()


def _enum_label(label: str, value: str) -> str:
    """Render a plain-language label while keeping the exact enum value visible."""
    return (
        f"{escape(label)} "
        f"<code class=\"enum-value\">{escape(value)}</code>"
    )


def _limitation_list(limitations: tuple[str, ...], heading: str) -> str:
    items = "".join(f"<li>{escape(entry)}</li>" for entry in limitations)
    return (
        f"<div class=\"limitations\"><h3>{escape(heading)}</h3>"
        f"<ul>{items}</ul></div>"
    )


def _csrf_input(briefing: ExecutiveBriefing) -> str:
    token = briefing.workspace_context.csrf_token
    if not token:
        return ""
    return (
        f"<input type=\"hidden\" name=\"csrf_token\" value=\"{escape(token)}\">"
    )


def _references_block(references: tuple[SourceReference, ...]) -> str:
    if not references:
        return (
            "<p class=\"no-evidence\">No source reference is claimed; this is not a "
            "supported statement.</p>"
        )
    rows = []
    for reference in references:
        observed = _fmt(reference.observed_at)
        rows.append(
            "<details class=\"reference\">"
            f"<summary>{escape(reference.label)}</summary>"
            "<dl>"
            f"<dt>Source ID</dt><dd>{escape(reference.source_id)}</dd>"
            "<dt>Evidence classification</dt><dd>"
            + _enum_label(
                _EVIDENCE_LABELS[reference.evidence_classification],
                reference.evidence_classification.value,
            )
            + "</dd>"
            f"<dt>Authority scope</dt><dd>{escape(reference.authority_scope)}</dd>"
            f"<dt>Observed at</dt><dd>{escape(observed)}</dd>"
            "</dl></details>"
        )
    return (
        "<div class=\"references\"><h3>Evidence used</h3>"
        + "".join(rows)
        + "</div>"
    )


def _evidence_meta(item: BriefingItem) -> str:
    parts = [
        "<dt>Evidence classification</dt><dd>"
        + _enum_label(
            _EVIDENCE_LABELS[item.evidence_classification],
            item.evidence_classification.value,
        )
        + "</dd>",
        f"<dt>Evidence basis</dt><dd>{escape(item.evidence_basis)}</dd>",
        "<dt>Freshness</dt><dd>"
        + _enum_label(_FRESHNESS_LABELS[item.freshness], item.freshness.value)
        + f" (observed {escape(_fmt(item.source_observed_at))})</dd>",
        "<dt>Uncertainty</dt><dd>"
        + _enum_label(_UNCERTAINTY_LABELS[item.uncertainty], item.uncertainty.value)
        + f" \u2014 {escape(item.uncertainty_explanation)}</dd>",
        "<dt>Lifecycle</dt><dd>"
        + _enum_label(_LIFECYCLE_LABELS[item.lifecycle], item.lifecycle.value)
        + "</dd>",
        "<dt>Current state</dt><dd>"
        + escape(
            "Ordinary and eligible for the briefing"
            if item.is_ordinary
            else "Not an ordinary eligible item"
        )
        + "</dd>",
    ]
    if item.review_due_at is not None:
        parts.append(
            f"<dt>Synthetic review due</dt><dd>{escape(_fmt(item.review_due_at))}</dd>"
        )
    return "<dl class=\"evidence-meta\">" + "".join(parts) + "</dl>"


def _authority_meta(item: BriefingItem) -> str:
    parts: list[str] = []
    if item.priority_basis is not None:
        parts.append(
            f"<dt>Priority basis</dt><dd>{escape(item.priority_basis)}</dd>"
        )
    if item.authority_requirement is not None:
        parts.append(
            "<dt>Human authority required</dt><dd>"
            f"{escape(item.authority_requirement)}</dd>"
        )
    owner = item.decision_owner if item.decision_owner else "Not yet assigned"
    if item.section in (BriefingSection.NEXT,):
        parts.append(f"<dt>Decision owner</dt><dd>{escape(owner)}</dd>")
    if item.permitted_next_step is not None:
        parts.append(
            "<dt>Permitted next step</dt><dd>"
            + _enum_label(
                _STEP_LABELS[item.permitted_next_step],
                item.permitted_next_step.value,
            )
            + "</dd>"
        )
    if not parts:
        return ""
    return "<dl class=\"authority-meta\">" + "".join(parts) + "</dl>"


def _related_next(item: BriefingItem, briefing: ExecutiveBriefing) -> str:
    related_next = [
        briefing.item_by_id(identity)
        for identity in item.related_item_ids
    ]
    fragments = []
    for related in related_next:
        if related is None or related.section is not BriefingSection.NEXT:
            continue
        fragments.append(
            "<p class=\"related-next\">Related next step "
            f"<a href=\"/next#{escape(related.item_id)}\">{escape(related.title)}</a>"
            " \u2014 kind "
            + _enum_label(
                _NEXT_KIND_LABELS[related.next_kind], related.next_kind.value
            )
            + ". This attention item stays informational; its kind and authority "
            "remain on the separate next item.</p>"
        )
    return "".join(fragments)


def _item_article(item: BriefingItem, briefing: ExecutiveBriefing) -> str:
    body = [
        f"<article class=\"card\" id=\"{escape(item.item_id)}\">",
        f"<h3>{escape(item.title)}</h3>",
        f"<p class=\"statement\">{escape(item.statement)}</p>",
    ]
    if item.section is BriefingSection.KNOW and item.knowledge_kind is not None:
        body.append(
            "<p class=\"kind\">Knowledge kind: "
            + _enum_label(
                _KNOWLEDGE_LABELS[item.knowledge_kind], item.knowledge_kind.value
            )
            + "</p>"
        )
    if item.section is BriefingSection.NEXT and item.next_kind is not None:
        body.append(
            "<p class=\"kind\">Next kind: "
            + _enum_label(_NEXT_KIND_LABELS[item.next_kind], item.next_kind.value)
            + " \u00b7 Context: "
            + _enum_label(
                _NEXT_CONTEXT_LABELS[item.next_context], item.next_context.value
            )
            + "</p>"
        )
    if item.section is BriefingSection.ATTENTION:
        body.append(
            "<p class=\"kind\">Role: informational attention "
            "<code class=\"enum-value\">informational_attention</code></p>"
        )
        body.append(_related_next(item, briefing))
    body.append(_evidence_meta(item))
    authority = _authority_meta(item)
    if authority:
        body.append(authority)
    body.append(_references_block(item.source_references))
    body.append(_limitation_list(item.limitations, "Limitations"))
    body.append("</article>")
    return "".join(body)


def _section_block(
    briefing: ExecutiveBriefing, section: BriefingSection
) -> str:
    items = briefing.items_in_section(section)
    heading = _SECTION_LABELS[section]
    if not items:
        return (
            f"<section aria-label=\"{escape(heading)}\"><h2>{escape(heading)}</h2>"
            "<p class=\"empty\">No eligible synthetic items in this section. The "
            "covered scope still applies.</p></section>"
        )
    articles = "".join(_item_article(item, briefing) for item in items)
    return (
        f"<section aria-label=\"{escape(heading)}\"><h2>{escape(heading)}</h2>"
        f"{articles}</section>"
    )


def _coverage_block(coverage: CoverageSummary) -> str:
    def named(values: tuple[str, ...], empty: str) -> str:
        if not values:
            return f"<p class=\"none\">{escape(empty)}</p>"
        return "<ul>" + "".join(f"<li>{escape(v)}</li>" for v in values) + "</ul>"

    return (
        "<section aria-label=\"Coverage\"><h2>Coverage and boundaries</h2>"
        f"<p class=\"scope\">{escape(coverage.scope_statement)}</p>"
        "<h3>Covered synthetic subjects</h3>"
        + named(coverage.covered_subjects, "None covered in this fixture.")
        + "<h3>Missing information</h3>"
        + named(coverage.missing_subjects, "No missing subjects recorded.")
        + "<h3>Conflicting information</h3>"
        + named(coverage.conflicting_subjects, "No conflicts recorded.")
        + "<h3>Stale information</h3>"
        + named(coverage.stale_subjects, "No stale subjects recorded.")
        + "<h3>Held or unapproved information (sanitized labels only)</h3>"
        + named(coverage.held_subjects, "No held subjects recorded.")
        + "<h3>Coverage counts (derived)</h3>"
        + "<dl class=\"coverage-counts\">"
        + f"<dt>Eligible synthetic items</dt><dd>{coverage.eligible_item_count}</dd>"
        + "<dt>Eligible synthetic source references</dt>"
        + f"<dd>{coverage.source_reference_count}</dd>"
        + "</dl>"
        + "<p class=\"bounded\">Coverage is bounded synthetic demonstration data, "
        "not omniscience.</p>"
        + _limitation_list(coverage.limitations, "Coverage limitations")
        + "</section>"
    )


def _document(
    *, title: str, nav_current: str | None, heading: str, main_html: str,
    briefing: ExecutiveBriefing, body_class: str = "",
) -> str:
    context = briefing.workspace_context
    banner_class = f"workspace-banner tone-{context.banner_tone.value}"
    org_name = context.profile.name
    is_demo = context.mode is WorkspaceMode.DEMONSTRATION
    auth_status = (
        "<div class=\"account-context\" aria-label=\"Authentication status\">"
        f"<span>Signed in as {escape(context.authenticated_user_display)}</span>"
        "<form method=\"post\" action=\"/logout\" class=\"workflow-form inline-form\">"
        + _csrf_input(briefing)
        + "<button type=\"submit\" class=\"button-quiet\">Sign out</button></form>"
        "</div>"
        if context.authenticated
        else "<div class=\"account-context\" aria-label=\"Authentication status\">"
        "<span>Guest access</span><a href=\"/login\">Sign in</a></div>"
    )
    demo_callout = (
        "<aside class=\"demo-guide-callout\" aria-label=\"Guided demonstration\">"
        "<p><strong>Demonstration workspace</strong> · Follow the complete governed "
        "journey from document to evidence-backed answer. "
        "<a href=\"/demo\">Start guided walkthrough</a></p>"
        "</aside>"
        if is_demo
        else ""
    )
    nav_links = []
    for key, href, label in _NAV:
        if key == nav_current:
            nav_links.append(
                f"<li><a href=\"{escape(href)}\" aria-current=\"page\" "
                f"class=\"current\">{escape(label)}</a></li>"
            )
        else:
            nav_links.append(f"<li><a href=\"{escape(href)}\">{escape(label)}</a></li>")
    footer_limits = "".join(
        f"<li>{escape(entry)}</li>" for entry in briefing.limitations
    )
    time_label = "Demonstration data captured" if is_demo else "Knowledge view updated"
    workspace_detail = (
        "<details class=\"context-disclosure\"><summary>Workspace details</summary>"
        "<dl>"
        f"<dt>Organization</dt><dd>{escape(org_name)}</dd>"
        f"<dt>Workspace</dt><dd>{escape(context.mode.value.title())}</dd>"
        f"<dt>Runtime</dt><dd>{escape(context.runtime_name)}</dd>"
        f"<dt>Knowledge view</dt><dd>{escape(_fmt(briefing.assembled_at))}</dd>"
        f"<dt>Coverage</dt><dd>{escape(briefing.coverage.scope_statement)}</dd>"
        "</dl></details>"
    )
    footer_status = (
        "This demonstration uses fabricated records and performs no organizational action."
        if is_demo
        else "Bonsaai presents approved evidence for human decisions and performs no autonomous organizational action."
    )
    body_attr = f" class=\"{escape(body_class)}\"" if body_class else ""
    return (
        "<!DOCTYPE html>"
        "<html lang=\"en\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{escape(title)} \u2014 Bonsaai</title>"
        "<link rel=\"stylesheet\" href=\"/static/styles.css\">"
        "</head>"
        f"<body{body_attr}>"
        "<a class=\"skip-link\" href=\"#main-content\">Skip to main content</a>"
        "<header class=\"site-header\">"
        "<div class=\"header-primary\"><div class=\"brand\">"
        "<span class=\"brand-mark\" aria-hidden=\"true\">B</span>"
        "<span class=\"brand-copy\"><span class=\"product-title\">Bonsaai</span>"
        "<span class=\"product-subtitle\">Governed organizational intelligence</span>"
        "</span>"
        "</div>"
        f"{auth_status}"
        "</div>"
        "</header>"
        "<nav class=\"primary-nav\" aria-label=\"Primary\">"
        f"<ul>{''.join(nav_links)}</ul>"
        "</nav>"
        f"<aside class=\"{escape(banner_class)}\" aria-label=\"Workspace banner\">"
        f"<div><strong>{escape(context.banner_label)}</strong> "
        f"<span>{escape(org_name)}</span></div>"
        f"<span class=\"badge synthetic\">{escape(SYNTHETIC_BADGE)}</span></aside>"
        "<div class=\"product-context\">"
        f"<p><strong>{escape(time_label)}:</strong> {escape(_fmt(briefing.assembled_at))}</p>"
        f"{workspace_detail}</div>"
        f"{demo_callout}"
        "<main id=\"main-content\">"
        f"<h1>{escape(heading)}</h1>"
        f"{main_html}"
        "</main>"
        "<footer class=\"site-footer\">"
        f"<p class=\"no-action\">{escape(NO_ACTION_STATEMENT)} {escape(footer_status)}</p>"
        "<details class=\"footer-limitations\"><summary>Material limitations</summary>"
        f"<ul>{footer_limits}</ul></details>"
        "</footer>"
        "</body></html>"
    )


def _workspace_selector_section(briefing: ExecutiveBriefing) -> str:
    context = briefing.workspace_context
    workspace_options = "".join(
        (
            f"<option value=\"{escape(mode_id)}\" selected>"
            if mode_id == context.mode.value
            else f"<option value=\"{escape(mode_id)}\">"
        )
        + f"{escape(mode_id.title())}</option>"
        for mode_id in context.available_workspace_modes
    )
    organization_options = "".join(
        (
            f"<option value=\"{escape(org_id)}\" selected>"
            if org_id == context.profile.organization_id
            else f"<option value=\"{escape(org_id)}\">"
        )
        + f"{escape(org_id)}</option>"
        for org_id in context.available_organization_ids
    )
    recent = "".join(
        f"<li>{escape(org_id)}</li>" for org_id in context.recent_organization_ids
    )
    csrf_input = _csrf_input(briefing)
    return (
        "<section aria-label=\"Workspace selector\">"
        "<h2>Operational workspace</h2>"
        "<p>Select workspace and organization without redeploying.</p>"
        "<form method=\"post\" action=\"/workspace/select\" class=\"workflow-form\">"
        f"{csrf_input}"
        "<p><label for=\"workspace_mode\">Workspace mode</label><br>"
        f"<select id=\"workspace_mode\" name=\"workspace_mode\">{workspace_options}</select></p>"
        "<p><button type=\"submit\">Switch workspace</button></p>"
        "</form>"
        "<form method=\"post\" action=\"/workspace/select-organization\" class=\"workflow-form\">"
        f"{csrf_input}"
        "<p><label for=\"organization_id\">Organization</label><br>"
        f"<select id=\"organization_id\" name=\"organization_id\">{organization_options}</select></p>"
        "<p><button type=\"submit\">Switch organization</button></p>"
        "</form>"
        "<h3>Recent organizations</h3>"
        f"<ul>{recent}</ul>"
        "</section>"
    )


def _executive_preview(
    briefing: ExecutiveBriefing,
    section: BriefingSection,
    *,
    href: str,
    link_label: str,
) -> str:
    items = briefing.items_in_section(section)
    cards = []
    for item in items[:2]:
        source_count = len(item.source_references)
        cards.append(
            "<article class=\"overview-card\">"
            f"<h3>{escape(item.title)}</h3>"
            f"<p>{escape(item.statement)}</p>"
            "<p class=\"evidence-summary\">"
            f"{escape(_EVIDENCE_LABELS[item.evidence_classification])} \u00b7 "
            f"{source_count} {('source' if source_count == 1 else 'sources')} \u00b7 "
            f"{escape(_FRESHNESS_LABELS[item.freshness])}</p>"
            "</article>"
        )
    empty = (
        "<p class=\"empty\">No eligible items are available in this covered scope.</p>"
        if not cards
        else ""
    )
    return (
        "<section class=\"overview-section\" "
        f"aria-label=\"{escape(_SECTION_LABELS[section])}\">"
        f"<div class=\"section-heading\"><h2>{escape(_SECTION_LABELS[section])}</h2>"
        f"<a href=\"{escape(href)}\">{escape(link_label)}</a></div>"
        f"<div class=\"overview-grid\">{''.join(cards)}</div>{empty}</section>"
    )


def render_overview(briefing: ExecutiveBriefing) -> str:
    counts = briefing.summary_counts
    context = briefing.workspace_context
    hero = (
        "<section class=\"product-hero\" aria-label=\"Bonsaai introduction\">"
        "<p class=\"eyebrow\">Governed organizational intelligence</p>"
        "<h2>Turn approved knowledge into decisions you can defend.</h2>"
        "<p class=\"hero-copy\">Bonsaai helps leadership understand what is "
        "happening, what needs attention, and what to do next. Jebediah answers "
        "only from knowledge your organization has reviewed and approved.</p>"
        "<div class=\"hero-actions\"><a class=\"button-link primary\" "
        "href=\"/knowledge-manager\">Add organizational knowledge</a>"
        "<a class=\"button-link secondary\" href=\"/organizational-intelligence\">"
        "Ask Jebediah</a></div>"
        "<ul class=\"trust-points\"><li>Human-approved knowledge</li>"
        "<li>Evidence on every supported answer</li>"
        "<li>Workspace-isolated by design</li></ul></section>"
    )
    learning = (
        "<section aria-label=\"How Jebediah learns\"><div class=\"section-heading\">"
        "<div><p class=\"eyebrow\">A governed learning loop</p>"
        "<h2>How Jebediah learns</h2></div>"
        "<a href=\"/knowledge-manager\">Open Knowledge Manager</a></div>"
        "<ol class=\"learning-steps\"><li><strong>1. Add knowledge</strong>"
        "<span>Upload a supported business document for validation and extraction.</span></li>"
        "<li><strong>2. A human approves it</strong>"
        "<span>Review the candidate before it becomes available knowledge.</span></li>"
        "<li><strong>3. Ask with evidence</strong>"
        "<span>Jebediah answers from approved knowledge and shows its sources.</span></li>"
        "</ol></section>"
    )
    trust = (
        "<section class=\"trust-panel\" aria-label=\"Why trust Bonsaai\">"
        "<div><p class=\"eyebrow\">Trust is visible</p><h2>Why trust the answer?</h2>"
        "<p>Every supported answer carries citations, source identity, freshness, "
        "uncertainty, and limitations. If approved evidence is missing, Jebediah "
        "says so instead of filling the gap.</p></div>"
        "<a class=\"button-link secondary\" href=\"/governance\">See governance controls</a>"
        "</section>"
    )
    summary = (
        "<section aria-label=\"Executive summary\"><div class=\"section-heading\">"
        "<div><p class=\"eyebrow\">Current briefing</p><h2>At a glance</h2></div>"
        "<span class=\"status-chip status-ready\">Ready</span></div>"
        "<dl class=\"metric-grid\">"
        f"<div><dt>Needs attention</dt><dd>{counts.priority_count}</dd></div>"
        f"<div><dt>Decisions open</dt><dd>{counts.unresolved_decision_count}</dd></div>"
        f"<div><dt>Governance gates</dt><dd>{counts.organizational_gate_count}</dd></div>"
        f"<div><dt>Approved sources</dt><dd>{counts.eligible_source_count}</dd></div>"
        "</dl><p class=\"derived-note\">Counts reflect eligible records in the "
        "active workspace.</p></section>"
    )
    operational_details = (
        "<details class=\"progressive-disclosure\"><summary>Workspace and system settings</summary>"
        + _workspace_selector_section(briefing)
        + "<section aria-label=\"System safeguards\"><h2>System safeguards</h2>"
        "<dl class=\"summary-counts\"><dt>Runtime</dt>"
        f"<dd>{escape(context.runtime_name)}</dd><dt>Model</dt>"
        f"<dd>{escape(context.model_name)}</dd><dt>Diagnostics</dt>"
        f"<dd>{'Enabled' if context.diagnostics_enabled else 'Off'}</dd>"
        f"<dt>Governance policy</dt><dd>{escape(context.profile.governance_policy)}</dd>"
        "</dl></section></details>"
    )
    main = (
        hero
        + learning
        + summary
        + _executive_preview(
            briefing,
            BriefingSection.HAPPENING,
            href="/organizational-memory",
            link_label="View current context",
        )
        + _executive_preview(
            briefing,
            BriefingSection.ATTENTION,
            href="/attention",
            link_label="View all attention items",
        )
        + _executive_preview(
            briefing,
            BriefingSection.KNOW,
            href="/knowledge",
            link_label="Explore approved knowledge",
        )
        + _executive_preview(
            briefing,
            BriefingSection.NEXT,
            href="/next",
            link_label="Review next decisions",
        )
        + trust
        + "<details class=\"progressive-disclosure\"><summary>Coverage and evidence limits</summary>"
        + _coverage_block(briefing.coverage)
        + "</details>"
        + operational_details
    )
    return _document(
        title="Executive Dashboard",
        nav_current="executive-dashboard",
        heading="Executive Dashboard",
        main_html=main,
        briefing=briefing,
    )


def render_attention(briefing: ExecutiveBriefing) -> str:
    main = _section_block(briefing, BriefingSection.ATTENTION)
    return _document(
        title="Needs attention",
        nav_current="executive-dashboard",
        heading="Needs attention",
        main_html=main,
        briefing=briefing,
    )


def render_knowledge(briefing: ExecutiveBriefing) -> str:
    main = (
        _coverage_block(briefing.coverage)
        + _section_block(briefing, BriefingSection.KNOW)
    )
    return _document(
        title="What Jebediah knows",
        nav_current="organizational-memory",
        heading="What Jebediah knows",
        main_html=main,
        briefing=briefing,
    )


def render_next(briefing: ExecutiveBriefing) -> str:
    main = _section_block(briefing, BriefingSection.NEXT)
    return _document(
        title="What happens next",
        nav_current="executive-dashboard",
        heading="What should happen next",
        main_html=main,
        briefing=briefing,
    )


def _workspace_row(record: WorkspaceRecord) -> str:
    references = (
        ", ".join(escape(ref.source_id) for ref in record.source_references)
        or "none"
    )
    eligible = "Eligible for briefing" if record.eligible_for_briefing else "Not eligible"
    limits = "; ".join(escape(entry) for entry in record.limitations)
    return (
        "<tr>"
        f"<th scope=\"row\">{escape(record.title)}</th>"
        f"<td data-label=\"Kind\">{escape(record.kind.value)}</td>"
        f"<td data-label=\"State\">{escape(record.state.value)}</td>"
        f"<td data-label=\"Briefing eligibility\">{escape(eligible)}</td>"
        f"<td data-label=\"Source references\">{references}</td>"
        f"<td data-label=\"Last changed\">{escape(_fmt(record.last_changed_at))}</td>"
        f"<td data-label=\"Limitations\">{limits}</td>"
        "</tr>"
    )


def _workspace_main(briefing: ExecutiveBriefing) -> str:
    rows = "".join(_workspace_row(record) for record in briefing.workspace_records)
    activities = "".join(
        "<li>"
        f"<strong>{escape(activity.summary)}</strong> "
        f"({escape(activity.kind.value)}, {escape(_fmt(activity.occurred_at))}) "
        f"\u2014 actor {escape(activity.actor_label)}; "
        f"result {escape(activity.result_state.value)}; "
        "source references "
        + (
            ", ".join(escape(ref.source_id) for ref in activity.source_references)
            or "none claimed"
        )
        + "</li>"
        for activity in briefing.activities
    )
    main = (
        "<section aria-label=\"Workspace records\"><h2>Governed workspace metadata</h2>"
        "<p>Only governed metadata is shown. Source content remains protected while "
        "lifecycle, governance, and traceability state remains visible.</p>"
        "<table class=\"workspace-table\"><caption>Synthetic source, document, "
        "quarantine, review, lineage, and knowledge-object status</caption>"
        "<thead><tr><th scope=\"col\">Record</th><th scope=\"col\">Kind</th>"
        "<th scope=\"col\">State</th><th scope=\"col\">Briefing eligibility</th>"
        "<th scope=\"col\">Source references</th><th scope=\"col\">Last changed</th>"
        "<th scope=\"col\">Limitations</th>"
        "</tr></thead>"
        f"<tbody>{rows}</tbody></table></section>"
        "<section aria-label=\"Recent activity\"><h2>Recent governed activity</h2>"
        f"<ul class=\"activity\">{activities}</ul></section>"
    )
    return main


def render_workspace(briefing: ExecutiveBriefing) -> str:
    reset = ""
    if briefing.workspace_context.demo_reset_available:
        reset = (
            "<section aria-label=\"Demo reset\">"
            "<h2>Reset demonstration</h2>"
            "<p>Restore demonstration documents, knowledge, governance, audit, and memory to a pristine synthetic baseline.</p>"
            "<form method=\"post\" action=\"/workspace/reset-demo\" class=\"workflow-form\">"
            + _csrf_input(briefing)
            + "<p><button type=\"submit\">Reset Demo</button></p>"
            + "</form>"
            + "</section>"
        )
    main = _workspace_selector_section(briefing) + reset + _workspace_main(briefing)
    return _document(
        title="Knowledge workspace",
        nav_current="knowledge-manager",
        heading="Knowledge workspace",
        main_html=main,
        briefing=briefing,
    )


def _ask_index_main(briefing: ExecutiveBriefing) -> str:
    links = []
    for response in briefing.ask_responses:
        links.append(
            "<li class=\"question-card\">"
            f"<a href=\"/ask/{escape(response.question_id)}\">"
            f"{escape(response.question)}</a>"
            f"<span>{escape(_ASK_STATE_LABELS[response.state])} example</span>"
            "</li>"
        )
    return (
        "<section aria-label=\"Prepared questions\"><h2>Prepared questions</h2>"
        "<p>Use these examples to see how Bonsaai responds when evidence is "
        "sufficient, incomplete, or unavailable.</p>"
        f"<ul class=\"ask-list question-grid\">{''.join(links)}</ul></section>"
    )


def render_ask_index(briefing: ExecutiveBriefing) -> str:
    main = _ask_index_main(briefing)
    return _document(
        title="Ask Jebediah",
        nav_current="organizational-intelligence",
        heading="Ask Jebediah",
        main_html=main,
        briefing=briefing,
    )


def render_knowledge_manager(briefing: ExecutiveBriefing) -> str:
    is_demo = briefing.workspace_context.mode is WorkspaceMode.DEMONSTRATION
    pending_review = next(
        (
            record
            for record in briefing.workspace_records
            if record.kind is WorkspaceKind.REVIEW
            and record.state is WorkspaceState.REVIEW_PENDING
        ),
        None,
    )
    has_pending_review = pending_review is not None
    available_knowledge = sum(
        1
        for record in briefing.workspace_records
        if record.kind is WorkspaceKind.KNOWLEDGE_OBJECT
        and record.state is WorkspaceState.ELIGIBLE
    )
    active_stage = 5 if has_pending_review else (7 if available_knowledge else 1)
    flow_labels = (
        ("Upload", "Choose a supported business document."),
        ("Validation", "Format, size, and safety checks run first."),
        ("Processing", "Text is extracted into a review candidate."),
        ("Review pending", "Candidate evidence waits outside approved knowledge."),
        ("Human approval", "An authorized person approves or rejects it."),
        ("Available knowledge", "Approved content becomes eligible for retrieval."),
        ("Ask Jebediah", "Answers use only eligible knowledge and show evidence."),
    )
    flow_items = "".join(
        "<li class=\"flow-step "
        + ("is-complete" if index < active_stage else "")
        + (" is-current" if index == active_stage else "")
        + "\">"
        f"<span class=\"flow-number\">{index}</span><div><strong>{escape(label)}</strong>"
        f"<span>{escape(description)}</span></div></li>"
        for index, (label, description) in enumerate(flow_labels, start=1)
    )
    promote_form = (
        "<div class=\"approval-grid\"><form method=\"post\" "
        "action=\"/knowledge-manager/promote-latest\" class=\"workflow-form approval-card\">"
        + _csrf_input(briefing)
        + "<h3>Approve candidate</h3><p>Make the reviewed extraction eligible "
        + "for governed retrieval in this workspace.</p>"
        + "<button type=\"submit\">Approve for Jebediah</button></form>"
        + "<form method=\"post\" action=\"/knowledge-manager/reject-latest\" "
        + "class=\"workflow-form approval-card rejection-card\">"
        + _csrf_input(briefing)
        + "<h3>Reject candidate</h3><p>Keep this extraction out of approved "
        + "knowledge and record why.</p>"
        + "<p><label for=\"rejection_reason\">Reason for rejection</label><br>"
        + "<input id=\"rejection_reason\" name=\"reason\" type=\"text\" "
        + "value=\"Evidence is not sufficient for approved knowledge\" required></p>"
        + "<button type=\"submit\" class=\"button-danger\">Reject candidate</button>"
        + "</form></div>"
        if pending_review is not None
        else "<div class=\"empty-state\"><h3>No document is waiting for approval</h3>"
        "<p>Upload a document to create a review candidate, or ask Jebediah "
        "from knowledge that is already approved.</p></div>"
    )
    admission_form = (
        "<form method=\"post\" action=\"/knowledge-manager/admit\" "
        "enctype=\"multipart/form-data\" class=\"workflow-form upload-form\" "
        "id=\"governed-upload-form\" data-upload-form "
        "data-max-file-size=\"1000000\">"
        + _csrf_input(briefing)
        + "<p><label for=\"source_record_id\">Source reference</label><br>"
        + "<input id=\"source_record_id\" name=\"source_record_id\" type=\"text\" "
        + "value=\"source-record-001\" maxlength=\"200\" "
        + "aria-describedby=\"source-record-help\" required>"
        + "<br><span class=\"field-help\" id=\"source-record-help\">"
        + "Use a stable internal reference for the source. It is applied to "
        + "every file in this batch and appears with later evidence."
        + "</span></p>"
        + "<div class=\"upload-control\"><p class=\"field-label\" "
        + "id=\"document-file-label\">Documents</p>"
        + "<input id=\"document_file\" name=\"document_file\" type=\"file\" "
        + "accept=\".pdf,.docx,.xlsx,.pptx,.csv,.txt,.md,.markdown,application/pdf,"
        + "application/vnd.openxmlformats-officedocument.wordprocessingml.document,"
        + "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        + "application/vnd.openxmlformats-officedocument.presentationml.presentation,"
        + "text/csv,text/plain,text/markdown\" aria-labelledby=\"document-file-label\" "
        + "aria-describedby=\"upload-help upload-errors\" multiple required>"
        + "<button class=\"upload-dropzone\" id=\"upload-dropzone\" type=\"button\" "
        + "aria-describedby=\"upload-help\" hidden>"
        + "<span class=\"upload-symbol\" aria-hidden=\"true\">↑</span>"
        + "<strong>Drop supported business documents here</strong>"
        + "<span>or choose files from this device</span></button>"
        + "<p class=\"field-help\" id=\"upload-help\">PDF, DOCX, XLSX, PPTX, "
        + "CSV, TXT, and Markdown are supported. Maximum 1 MB per file. "
        + "Macro-enabled files, images, and ZIP archives are not accepted.</p></div>"
        + "<p class=\"field-help\">Each file shows validation, upload, admission, "
        + "and review status. A successful upload still requires human approval.</p>"
        + "<div class=\"upload-errors\" id=\"upload-errors\" role=\"alert\" "
        + "aria-live=\"assertive\" tabindex=\"-1\" hidden></div>"
        + "<ul class=\"upload-queue\" id=\"upload-queue\" "
        + "aria-label=\"Files selected for governed admission\" "
        + "aria-live=\"polite\"></ul>"
        + "<p class=\"upload-summary\" id=\"upload-summary\" "
        + "aria-live=\"polite\">No files queued.</p>"
        + "<p><button id=\"upload-submit\" type=\"submit\">"
        + "Validate and submit documents</button></p>"
        + "<noscript><p class=\"boundary\">Choose one file and submit it. "
        + "Drag-and-drop, batch progress, and inline results require JavaScript.</p>"
        + "</noscript>"
        + "</form>"
        if not is_demo
        else "<p class=\"boundary\">Demonstration workspace uses fixed synthetic records. Switch to development or production workspace for live admission.</p>"
    )
    guide = (
        "<section class=\"knowledge-intro\" aria-label=\"Knowledge Manager introduction\">"
        "<p class=\"eyebrow\">Governed knowledge lifecycle</p>"
        "<h2>Teach Jebediah without giving up control.</h2>"
        "<p>Documents enter a protected review workflow. Extraction never becomes "
        "available knowledge until an authorized person approves it.</p>"
        "<ol class=\"knowledge-flow\">"
        + flow_items
        + "</ol></section>"
        "<section aria-label=\"Supported document formats\"><div class=\"section-heading\">"
        "<div><p class=\"eyebrow\">Step 1</p><h2>Upload documents</h2></div>"
        "<span class=\"status-chip\">1 MB per file</span></div>"
        "<p>Use ordinary business documents. Bonsaai validates the format and "
        "extracts text without executing macros, formulas, links, or embedded content.</p>"
        "<ul class=\"format-list\"><li>PDF</li><li>DOCX</li><li>XLSX</li>"
        "<li>PPTX</li><li>CSV</li><li>TXT</li><li>Markdown</li></ul>"
        + admission_form
        + "</section>"
        "<section aria-label=\"Human knowledge approval\"><div class=\"section-heading\">"
        "<div><p class=\"eyebrow\">Step 2</p><h2>Human review and approval</h2></div>"
        + (
            "<span class=\"status-chip status-pending\">Decision required</span>"
            if has_pending_review
            else "<span class=\"status-chip\">No pending review</span>"
        )
        + "</div><p>Approval means the reviewed extraction may support answers in "
        "this workspace. It does not verify every fact in the source or authorize an action.</p>"
        + (
            f"<p class=\"candidate-summary\"><strong>Candidate:</strong> "
            f"{escape(pending_review.title)}</p>"
            if pending_review is not None
            else ""
        )
        + (
            promote_form
            if not is_demo
            else "<div class=\"empty-state\"><h3>Controls are protected in the demonstration</h3>"
            "<p>Use the guided walkthrough to see the fixed review states, or switch "
            "to an authorized development or production workspace.</p></div>"
        )
        + "</section>"
        "<section class=\"knowledge-ready\" aria-label=\"Available knowledge\">"
        "<div><p class=\"eyebrow\">Step 3</p><h2>Available knowledge</h2>"
        f"<p><strong>{available_knowledge}</strong> approved knowledge "
        f"{('record is' if available_knowledge == 1 else 'records are')} eligible "
        "in this workspace.</p></div>"
        "<a class=\"button-link primary\" href=\"/organizational-intelligence\">"
        "Ask Jebediah</a></section>"
    )
    main = guide + (
        "<details class=\"progressive-disclosure inventory-disclosure\">"
        "<summary>View knowledge inventory and audit activity</summary>"
        + _workspace_main(briefing)
        + "</details>"
    ) + (
        "<script src=\"/static/upload.js\" defer></script>" if not is_demo else ""
    )
    return _document(
        title="Knowledge Manager",
        nav_current="knowledge-manager",
        heading="Knowledge Manager",
        main_html=main,
        briefing=briefing,
    )


def render_organizational_intelligence(briefing: ExecutiveBriefing) -> str:
    is_demo = briefing.workspace_context.mode is WorkspaceMode.DEMONSTRATION
    ask_form = (
        "<form method=\"post\" action=\"/organizational-intelligence/ask\" "
        "class=\"workflow-form governed-question-form\" data-question-form>"
        + _csrf_input(briefing)
        + "<p><label for=\"question\">What would you like to understand?</label><br>"
        + "<textarea id=\"question\" name=\"question\" rows=\"4\" cols=\"70\" required>"
        + "What should leadership decide next based on the currently approved governance evidence?"
        + "</textarea></p>"
        + "<p><button type=\"submit\" class=\"question-submit\">"
        + "<span class=\"question-submit-ready\">Run governed question</span>"
        + "<span class=\"question-submit-processing\">Processing approved evidence…</span>"
        + "</button><span class=\"question-processing-status\" role=\"status\">"
        + "Retrieving approved evidence and preparing a governed answer…</span></p>"
        + "</form>"
        if not is_demo
        else "<p class=\"boundary\">Demonstration workspace uses preset synthetic questions. Switch to development or production for live governed questions.</p>"
    )
    lead = (
        "<section class=\"ask-hero\" aria-label=\"Ask Jebediah\">"
        "<p class=\"eyebrow\">Executive intelligence</p><h2>Ask your organization. "
        "See the evidence.</h2><p>Jebediah searches only approved knowledge in the "
        "active workspace. Every supported answer names the evidence it used and "
        "keeps human decision authority visible.</p>"
        "<ul class=\"trust-points\"><li>Approved knowledge only</li>"
        "<li>Citations included</li><li>No answer when evidence is insufficient</li></ul>"
        "<div class=\"question-focus\">"
        "<h3>Ask Jebediah</h3>"
        + ask_form +
        "</div></section>"
    )
    main = lead + _ask_index_main(briefing) + (
        "<script src=\"/static/upload.js\" defer></script>" if not is_demo else ""
    )
    return _document(
        title="Ask Jebediah",
        nav_current="organizational-intelligence",
        heading="Ask Jebediah",
        main_html=main,
        briefing=briefing,
    )


def render_organizational_memory(briefing: ExecutiveBriefing) -> str:
    main = (
        "<section aria-label=\"Organizational Memory\"><h2>Curated organizational "
        "memory view</h2><p>This view summarizes governed knowledge and "
        "material changes retained for executive context.</p></section>"
        + _section_block(briefing, BriefingSection.HAPPENING)
        + _section_block(briefing, BriefingSection.KNOW)
    )
    return _document(
        title="Organizational Memory",
        nav_current="organizational-memory",
        heading="Organizational Memory",
        main_html=main,
        briefing=briefing,
    )


def render_governance(briefing: ExecutiveBriefing) -> str:
    main = (
        "<section aria-label=\"Governance controls\"><h2>Governance controls and "
        "boundaries</h2><p>Every governed claim is bounded by evidence "
        "classification, freshness, uncertainty, lifecycle, and disclosure limits."
        "</p><ul><li>No governance-pass, no eligible evidence.</li><li>No eligible "
        "evidence, no evidence-backed answer.</li><li>Held or unauthorized subjects remain "
        "excluded from ordinary claims.</li></ul></section>"
        + _coverage_block(briefing.coverage)
    )
    return _document(
        title="Governance",
        nav_current="governance",
        heading="Governance",
        main_html=main,
        briefing=briefing,
    )


def render_audit(briefing: ExecutiveBriefing) -> str:
    kind_counts: dict[str, int] = {}
    state_counts: dict[str, int] = {}
    rows = []
    for activity in briefing.activities:
        kind_counts[activity.kind.value] = kind_counts.get(activity.kind.value, 0) + 1
        state_counts[activity.result_state.value] = (
            state_counts.get(activity.result_state.value, 0) + 1
        )
        rows.append(
            "<tr>"
            f"<td data-label=\"Time\">{escape(_fmt(activity.occurred_at))}</td>"
            f"<td data-label=\"Activity\">{escape(activity.summary)}</td>"
            f"<td data-label=\"Kind\">{escape(activity.kind.value)}</td>"
            f"<td data-label=\"Actor\">{escape(activity.actor_label)}</td>"
            f"<td data-label=\"Result state\">{escape(activity.result_state.value)}</td>"
            f"<td data-label=\"Source references\">"
            + (
                ", ".join(escape(reference.source_id) for reference in activity.source_references)
                or "none claimed"
            )
            + "</td></tr>"
        )
    kind_filters = "".join(
        f"<li>{escape(kind)}: {count}</li>"
        for kind, count in sorted(kind_counts.items())
    )
    state_filters = "".join(
        f"<li>{escape(state)}: {count}</li>"
        for state, count in sorted(state_counts.items())
    )
    export_rows = "".join(
        f"{escape(_fmt(activity.occurred_at))},{escape(activity.activity_id)},"
        f"{escape(activity.kind.value)},{escape(activity.result_state.value)},"
        f"{escape(activity.actor_label)}\n"
        for activity in briefing.activities
    )
    main = (
        "<section aria-label=\"Audit history\"><h2>Governed audit history</h2>"
        "<p>This timeline exposes governance-relevant runtime events and safe "
        "references. It intentionally omits operational secrets and raw content."
        "</p><div class=\"journey-step\"><h3>Event filters and search facets</h3>"
        "<p>Use kind, result state, and source reference values in each row for "
        "manual filtering and targeted drill-down.</p>"
        f"<p><strong>Kinds:</strong></p><ul>{kind_filters or '<li>none</li>'}</ul>"
        f"<p><strong>Result states:</strong></p><ul>{state_filters or '<li>none</li>'}</ul>"
        "</div><table class=\"workspace-table\"><caption>Admission, review, lineage, "
        "and knowledge-status events</caption><thead><tr><th scope=\"col\">Time</th>"
        "<th scope=\"col\">Activity</th><th scope=\"col\">Kind</th><th scope=\"col\">Actor</th>"
        "<th scope=\"col\">Result state</th><th scope=\"col\">Source references</th>"
        "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
        "<h3>Audit export snapshot</h3>"
        "<p>Copy this CSV snapshot for external review tooling.</p>"
        f"<pre class=\"audit-export\">time,activity_id,kind,result_state,actor\n{export_rows}</pre>"
        "</section>"
    )
    return _document(
        title="Audit",
        nav_current="audit",
        heading="Audit",
        main_html=main,
        briefing=briefing,
    )


def render_demo_walkthrough(briefing: ExecutiveBriefing) -> str:
    reset = (
        "<form method=\"post\" action=\"/workspace/reset-demo\" class=\"workflow-form\">"
        + _csrf_input(briefing)
        + "<p><button type=\"submit\">Reset Demo</button></p>"
        + "</form>"
        if briefing.workspace_context.demo_reset_available
        else ""
    )
    main = (
        "<section class=\"product-hero\" aria-label=\"Demonstration walkthrough\">"
        "<p class=\"eyebrow\">Repeatable executive demonstration</p>"
        "<h2>Bonsaai in five minutes</h2>"
        "<p class=\"hero-copy\">Show how a document becomes approved knowledge, "
        "how Jebediah answers from that knowledge, and how leadership verifies "
        "the evidence behind the answer.</p>"
        "<ol class=\"demo-steps\">"
        "<li><strong>1. Start with the outcome</strong><span> "
        "<a href=\"/\">Open the Dashboard</a> and explain what Bonsaai is.</span></li>"
        "<li><strong>2. Show how Jebediah learns</strong><span> "
        "<a href=\"/knowledge-manager\">Open Knowledge Manager</a> and follow the "
        "governed document lifecycle.</span></li>"
        "<li><strong>3. Confirm the human gate</strong><span> "
        "<a href=\"/governance\">Open Governance</a> and show that approval never "
        "verifies source truth or authorizes action.</span></li>"
        "<li><strong>4. Ask the organization</strong><span> "
        "<a href=\"/organizational-intelligence\">Ask Jebediah</a> using a prepared "
        "executive question.</span></li>"
        "<li><strong>5. Verify the answer</strong><span> "
        "<a href=\"/ask/grounded-priorities\">Open an evidence-backed answer</a> and "
        "inspect its citations, uncertainty, and limits.</span></li>"
        "<li><strong>6. Close with accountability</strong><span> "
        "<a href=\"/audit\">Open the Audit Trail</a> and show the governed history.</span></li>"
        "</ol>"
        + reset +
        "<p class=\"boundary\">This workspace uses fixed fabricated records. Live "
        "upload and approval controls remain available only in an authorized "
        "development or production workspace.</p>"
        "</section>"
        + _coverage_block(briefing.coverage)
    )
    return _document(
        title="Demonstration Mode",
        nav_current="executive-dashboard",
        heading="Demonstration Mode",
        main_html=main,
        briefing=briefing,
    )


def render_administration(briefing: ExecutiveBriefing) -> str:
    pending_reviews = sum(
        1
        for record in briefing.workspace_records
        if record.state is WorkspaceState.REVIEW_PENDING
    )
    held_records = sum(
        1
        for record in briefing.workspace_records
        if record.state is WorkspaceState.HELD
    )
    rejected_reviews = sum(
        1
        for record in briefing.workspace_records
        if record.state is WorkspaceState.REVIEW_REJECTED
    )
    eligible_knowledge = sum(
        1
        for record in briefing.workspace_records
        if record.kind is WorkspaceKind.KNOWLEDGE_OBJECT
        and record.state is WorkspaceState.ELIGIBLE
    )
    main = (
        "<section aria-label=\"Administration\"><h2>Administration and runtime "
        "controls</h2><p>Administration focuses on runtime visibility, queue state, "
        "governance posture, and bounded behavior.</p><ul><li>Loopback-only local runtime.</li>"
        "<li>Human-gated governance and promotion.</li>"
        "<li>No autonomous organizational actions.</li></ul></section>"
        "<section aria-label=\"Operational views\"><h2>Operational views</h2>"
        f"<dl><dt>Knowledge records tracked</dt><dd>{len(briefing.workspace_records)}</dd>"
        f"<dt>Audit events tracked</dt><dd>{len(briefing.activities)}</dd>"
        f"<dt>Eligible knowledge sources</dt><dd>{briefing.summary_counts.eligible_source_count}</dd>"
        f"<dt>Pending governance reviews</dt><dd>{pending_reviews}</dd>"
        f"<dt>Held for evidence</dt><dd>{held_records}</dd>"
        f"<dt>Rejected reviews</dt><dd>{rejected_reviews}</dd>"
        f"<dt>Eligible knowledge objects</dt><dd>{eligible_knowledge}</dd></dl>"
        "<h3>Authentication operations</h3>"
        "<dl>"
        f"<dt>Authentication required</dt><dd>{'yes' if briefing.workspace_context.auth_required else 'no'}</dd>"
        f"<dt>Active sessions</dt><dd>{briefing.workspace_context.active_session_count}</dd>"
        f"<dt>Locked accounts</dt><dd>{briefing.workspace_context.locked_account_count}</dd>"
        "</dl>"
        "<p><a href=\"/demo\">Open guided walkthrough</a> \u00b7 "
        "<a href=\"/states\">Open state gallery</a> \u00b7 "
        "<a href=\"/board\">Open board view</a></p></section>"
    )
    return _document(
        title="Administration",
        nav_current="administration",
        heading="Administration",
        main_html=main,
        briefing=briefing,
    )


def render_ask_response(briefing: ExecutiveBriefing, response: AskResponse) -> str:
    symbol = _ASK_STATE_SYMBOLS[response.state]
    label = _ASK_STATE_LABELS[response.state]
    body = [
        "<section class=\"answer-hero\" aria-label=\"Governed answer\">",
        "<p class=\"eyebrow\">Your question</p>",
        f"<h2>{escape(response.question)}</h2>",
        f"<p class=\"ask-state\"><span aria-hidden=\"true\">{symbol}</span> "
        f"Governance state: {escape(label)}</p>",
        "<section class=\"answer-panel\" aria-label=\"Jebediah response\">"
        "<p class=\"eyebrow\">Jebediah's response</p><h3>Answer</h3>",
    ]
    if response.state is AskState.GROUNDED and response.statement:
        body.append(f"<p class=\"statement\">{escape(response.statement)}</p>")
    else:
        body.append(
            "<p class=\"no-answer\">No answer is fabricated for this state. The "
            "preset reports its evidence position honestly.</p>"
        )
    body.append("</section>")
    body.append(
        "<section class=\"coverage-statement\" aria-label=\"Answer coverage\">"
        "<h3>What this answer covers</h3>"
        f"<p>{escape(response.coverage_statement)}</p></section>"
    )
    posture = {
        UncertaintyState.BOUNDED: "Supported within cited coverage",
        UncertaintyState.INCOMPLETE: "Limited by missing evidence",
        UncertaintyState.CONFLICTING: "Conflicting evidence",
        UncertaintyState.UNKNOWN: "Evidence posture unknown",
        UncertaintyState.NOT_APPLICABLE: "Not applicable",
    }[response.uncertainty]
    body.append(
        "<section class=\"evidence-dossier\" aria-label=\"Evidence and governance\">"
        "<h3>Evidence and governance</h3>"
        "<dl class=\"answer-facts\">"
        f"<dt>Evidence posture</dt><dd>{escape(posture)}</dd>"
        f"<dt>Citations</dt><dd>{len(response.source_references)}</dd>"
        "<dt>Knowledge eligibility</dt><dd>Approved records only</dd>"
        "<dt>Decision authority</dt><dd>Remains with an authorized human</dd>"
        "</dl><p><a href=\"/audit\">Review this workspace's audit trail</a></p>"
        "</section>"
    )
    body.append(
        "<p class=\"uncertainty\">Uncertainty: "
        + _enum_label(
            _UNCERTAINTY_LABELS[response.uncertainty], response.uncertainty.value
        )
        + f" \u2014 {escape(response.uncertainty_explanation)}</p>"
    )
    body.append(
        "<section class=\"citation-panel\" aria-label=\"Citations\"><h3>Citations</h3>"
        "<p>Open each source to inspect its identity, evidence classification, "
        "authority scope, and observation time.</p>"
        + _references_block(response.source_references)
        + "</section>"
    )
    body.append(_limitation_list(response.limitations, "Limitations"))
    if response.state is AskState.GROUNDED:
        body.append(
            "<p class=\"grounded-note\">Evidence-backed means cited approved records "
            "support this answer in the active workspace. It is not automatic authority "
            "for organizational action.</p>"
        )
    body.append(
        "<p class=\"answer-actions\"><a class=\"button-link secondary\" "
        "href=\"/organizational-intelligence\">Ask another question</a> "
        "<a href=\"/knowledge-manager\">Manage approved knowledge</a></p>"
    )
    body.append("</section>")
    return _document(
        title=f"Ask: {response.question_id}",
        nav_current="organizational-intelligence",
        heading="Ask Jebediah",
        main_html="".join(body),
        briefing=briefing,
    )


def render_board(briefing: ExecutiveBriefing) -> str:
    counts = briefing.summary_counts
    priorities = briefing.items_in_section(BriefingSection.ATTENTION)
    know_items = briefing.items_in_section(BriefingSection.KNOW)
    risks = [i for i in know_items if i.knowledge_kind is KnowledgeKind.RISK]
    opportunities = [
        i for i in know_items if i.knowledge_kind is KnowledgeKind.OPPORTUNITY
    ]
    decisions = [
        i
        for i in briefing.items_in_section(BriefingSection.NEXT)
        if i.next_kind is NextItemKind.DECISION_REQUIRED
    ]

    def board_list(items: list[BriefingItem]) -> str:
        if not items:
            return "<p class=\"none\">No records currently available.</p>"
        rows = []
        for item in items:
            refs = ", ".join(
                escape(ref.source_id) for ref in item.source_references
            ) or "no source claimed"
            rows.append(
                f"<li><strong>{escape(item.title)}</strong> \u2014 "
                f"{escape(item.statement)} <span class=\"evidence\">Evidence: "
                f"{escape(_EVIDENCE_LABELS[item.evidence_classification])}; "
                f"sources: {refs}</span></li>"
            )
        return "<ul>" + "".join(rows) + "</ul>"

    main = (
        "<section aria-label=\"Board status\"><h2>Organizational status (runtime)</h2>"
        "<p class=\"status-banner\"><span aria-hidden=\"true\">\u25c9</span> "
        f"A governed runtime briefing is ready with {counts.priority_count} priorities and "
        f"{counts.unresolved_decision_count} unresolved decisions.</p></section>"
        "<section aria-label=\"Key priorities\"><h2>Key priorities</h2>"
        + board_list(list(priorities))
        + "</section>"
        "<section aria-label=\"Risks\"><h2>Risks</h2>"
        + board_list(risks)
        + "</section>"
        "<section aria-label=\"Opportunities\"><h2>Opportunities</h2>"
        + board_list(opportunities)
        + "</section>"
        "<section aria-label=\"Upcoming decisions\"><h2>Upcoming decisions</h2>"
        + board_list(decisions)
        + "</section>"
        + _coverage_block(briefing.coverage)
    )
    return _document(
        title="Board view",
        nav_current="executive-dashboard",
        heading="Board view",
        main_html=main,
        briefing=briefing,
        body_class="board-view",
    )


def render_states_gallery(briefing: ExecutiveBriefing) -> str:
    rows = []
    for route_id, state in STATE_ROUTE_TO_ENUM.items():
        rows.append(
            "<li>"
            f"<a href=\"/states/{escape(route_id)}\">"
            f"<span aria-hidden=\"true\">{_STATE_SYMBOLS[state]}</span> "
            f"{escape(_STATE_LABELS[state])}</a> "
            f"<code class=\"enum-value\">{escape(state.value)}</code>"
            "</li>"
        )
    main = (
        "<section aria-label=\"State gallery\"><h2>Demonstration state gallery</h2>"
        "<p>Each state is a fixed synthetic presentation and does not change the "
        "underlying fixture. Every state keeps the synthetic and no-action "
        "boundary.</p>"
        f"<ul class=\"state-list\">{''.join(rows)}</ul></section>"
    )
    return _document(
        title="State gallery",
        nav_current="administration",
        heading="State gallery and disconnected behavior",
        main_html=main,
        briefing=briefing,
    )


def _state_detail_body(briefing: ExecutiveBriefing, state: BriefingState) -> str:
    """Substantive fixed synthetic presentation for one accepted state.

    The underlying fixture is never mutated. Each branch presents only the
    fabricated briefing and coverage fields that the accepted state permits,
    and every dynamic value is escaped.
    """
    coverage = briefing.coverage
    capture = escape(_fmt(briefing.assembled_at))

    def subjects(values: tuple[str, ...], empty: str) -> str:
        if not values:
            return f"<p class=\"none\">{escape(empty)}</p>"
        return "<ul>" + "".join(f"<li>{escape(v)}</li>" for v in values) + "</ul>"

    if state is BriefingState.LOADING:
        return (
            "<h3>Skeleton placeholder</h3>"
            "<p>A skeleton structure stands in for content that a future live "
            "system would assemble. No values are shown as if they were ready.</p>"
            "<ul class=\"skeleton\" aria-hidden=\"true\">"
            "<li class=\"skeleton-line\"></li>"
            "<li class=\"skeleton-line\"></li>"
            "<li class=\"skeleton-line\"></li>"
            "</ul>"
            "<p class=\"no-fetch\">No background fetch, request, or network call is "
            "occurring in this disconnected demonstration; the skeleton never "
            "resolves to live data.</p>"
        )
    if state is BriefingState.EMPTY:
        return (
            "<h3>Covered synthetic scope</h3>"
            f"<p class=\"scope\">{escape(coverage.scope_statement)}</p>"
            + subjects(coverage.covered_subjects, "None covered in this fixture.")
            + "<h3>Eligible items in the empty state</h3>"
            "<dl class=\"state-counts\">"
            "<dt>Eligible synthetic items presented</dt><dd>0</dd>"
            "</dl>"
            "<p class=\"boundary\">Zero eligible items are shown, which never means "
            "that nothing is happening in a real organization.</p>"
        )
    if state is BriefingState.PARTIAL:
        return (
            "<h3>Affected sections</h3>"
            "<ul>"
            "<li>What Jebediah knows (partially available)</li>"
            "<li>What happens next (partially available)</li>"
            "</ul>"
            "<h3>Unavailable synthetic inputs</h3>"
            + subjects(
                coverage.missing_subjects, "No unavailable inputs recorded."
            )
            + "<p class=\"boundary\">Only some fabricated sections are available. The "
            "unavailable synthetic inputs are named rather than silently omitted.</p>"
        )
    if state is BriefingState.STALE:
        return (
            "<h3>Fabricated capture time</h3>"
            f"<p class=\"capture\">Captured at {capture}. No newer synthetic "
            "evidence exists in this fixture.</p>"
            "<h3>Stale evidence subjects</h3>"
            + subjects(coverage.stale_subjects, "No stale subjects recorded.")
            + "<p class=\"boundary\">Stale evidence is shown with its capture time and "
            "limitation together, never presented as current.</p>"
        )
    if state is BriefingState.INSUFFICIENT_EVIDENCE:
        return (
            "<h3>Missing evidence requirements</h3>"
            + subjects(
                coverage.missing_subjects, "No missing requirements recorded."
            )
            + "<p class=\"no-answer\">No fabricated answer is produced. The state "
            "names the missing synthetic evidence rather than guessing.</p>"
        )
    if state is BriefingState.HELD:
        held_subject = (
            escape(coverage.held_subjects[0])
            if coverage.held_subjects
            else "a sanitized held subject"
        )
        return (
            "<h3>Held subject (sanitized label only)</h3>"
            f"<p class=\"held\">A human or policy gate applies to {held_subject}. "
            "Only the sanitized label is named.</p>"
            "<h3>Gate and eligibility</h3>"
            "<p class=\"boundary\">A human or policy gate governs this information. It "
            "has no ordinary eligibility and its content is not shown.</p>"
        )
    if state is BriefingState.FAILED:
        return (
            "<h3>Sanitized failure</h3>"
            "<p class=\"failed\">A fabricated failure occurred while assembling this "
            "synthetic state. No internal detail, path, or trace is shown.</p>"
            "<p class=\"boundary\">The synthetic and no-action boundary is retained "
            "even when a state fails.</p>"
        )
    if state is BriefingState.UNAUTHORIZED:
        return (
            "<h3>No data shown</h3>"
            "<p class=\"boundary\">Access would be required in a future live system. "
            "No synthetic data, subject, or count is shown in this state.</p>"
        )
    if state is BriefingState.UNAVAILABLE:
        return (
            "<h3>Fails safely</h3>"
            "<p class=\"boundary\">The synthetic briefing cannot be assembled safely, "
            "so no partial fabricated values are presented as if they were ready.</p>"
        )
    if state is BriefingState.DISCONNECTED:
        return (
            "<h3>No connection by design</h3>"
            f"<p class=\"boundary\">{escape(DISCONNECTED_STATEMENT)} No connection to "
            "any service, collector, model, or data source is opened.</p>"
        )
    # READY
    counts = briefing.summary_counts
    ready_titles = [item.title for item in briefing.items if item.is_ordinary][:3]
    listed = (
        "<ul>" + "".join(f"<li>{escape(t)}</li>" for t in ready_titles) + "</ul>"
    )
    return (
        "<h3>Eligible synthetic evidence</h3>"
        "<dl class=\"state-counts\">"
        f"<dt>Eligible synthetic items</dt><dd>{coverage.eligible_item_count}</dd>"
        "<dt>Eligible synthetic source references</dt>"
        f"<dd>{coverage.source_reference_count}</dd>"
        f"<dt>Priorities needing attention</dt><dd>{counts.priority_count}</dd>"
        "</dl>"
        "<h3>Examples of eligible items</h3>"
        + listed
        + f"<p class=\"capture\">Captured at {capture}.</p>"
        "<p class=\"boundary\">Eligible fabricated evidence is shown together with "
        "its limitations, never as complete or action-ready truth.</p>"
    )


def render_state_detail(briefing: ExecutiveBriefing, route_id: str) -> str:
    state = STATE_ROUTE_TO_ENUM[route_id]
    main = (
        f"<section aria-label=\"State {escape(_STATE_LABELS[state])}\">"
        f"<h2><span aria-hidden=\"true\">{_STATE_SYMBOLS[state]}</span> "
        f"{escape(_STATE_LABELS[state])} "
        f"<code class=\"enum-value\">{escape(state.value)}</code></h2>"
        f"<p class=\"state-description\">{escape(_STATE_DESCRIPTIONS[state])}</p>"
        + _state_detail_body(briefing, state)
        + "<p class=\"boundary\">This state view is synthetic, disconnected, and takes "
        "no organizational action.</p>"
        + _limitation_list(briefing.limitations, "Retained limitations")
        + "</section>"
    )
    return _document(
        title=f"State: {route_id}",
        nav_current="administration",
        heading=f"State: {_STATE_LABELS[state]}",
        main_html=main,
        briefing=briefing,
    )


def render_error(
    briefing: ExecutiveBriefing, *, status_label: str, message: str
) -> str:
    if status_label.startswith("404"):
        title = "We could not find that page"
        guidance = "Check the address or return to the dashboard."
    elif status_label.startswith("503"):
        title = "Bonsaai is temporarily unavailable"
        guidance = "Your governed state is unchanged. Wait a moment and try again."
    elif status_label.startswith("401") or status_label.startswith("403"):
        title = "Access is required"
        guidance = "Sign in with an authorized account or return to the dashboard."
    else:
        title = "We could not complete that request"
        guidance = "Review the information shown below and try the request again."
    main = (
        "<section class=\"error-panel\" aria-label=\"Request problem\">"
        f"<p class=\"error-status\">{escape(status_label)}</p><h2>What happened</h2>"
        f"<p class=\"error-message\">{escape(message)}</p>"
        f"<p>{escape(guidance)}</p>"
        "<p class=\"boundary\">No request content is echoed, no answer is fabricated, "
        "and no organizational action is taken.</p>"
        "<p class=\"hero-actions\"><a class=\"button-link primary\" href=\"/\">"
        "Return to dashboard</a><a class=\"button-link secondary\" "
        "href=\"/organizational-intelligence\">Ask Jebediah</a></p></section>"
    )
    return _document(
        title=status_label,
        nav_current=None,
        heading=title,
        main_html=main,
        briefing=briefing,
    )
