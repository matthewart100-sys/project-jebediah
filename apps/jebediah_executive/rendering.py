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
    Phase3BSubmissionDetailView,
    Phase3BSubmissionState,
    Phase3BWorkspaceView,
    SourceReference,
    UncertaintyState,
    WorkspaceRecord,
)

SYNTHETIC_BADGE = "Synthetic demonstration"
NO_ACTION_STATEMENT = (
    "This preview takes no organizational action and records no decision."
)
DISCONNECTED_STATEMENT = (
    "Local, disconnected preview \u2014 no live service connection exists by design."
)

_NAV = (
    ("overview", "/", "Overview"),
    ("attention", "/attention", "Needs attention"),
    ("knowledge", "/knowledge", "What Jebediah knows"),
    ("next", "/next", "What happens next"),
    ("workspace", "/workspace", "Knowledge workspace"),
    ("ask", "/ask", "Ask Jebediah"),
    ("board", "/board", "Board view"),
    ("states", "/states", "State gallery"),
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
    AskState.GROUNDED: "Grounded",
    AskState.INSUFFICIENT: "Insufficient evidence",
    AskState.FAILED: "Failed",
}

_ASK_STATE_SYMBOLS = {
    AskState.GROUNDED: "\u25c6",
    AskState.INSUFFICIENT: "\u25cb",
    AskState.FAILED: "\u2716",
}

_PHASE3B_STATE_LABELS = {
    Phase3BSubmissionState.QUARANTINED: "Quarantined",
    Phase3BSubmissionState.ACCEPTED: "Accepted",
    Phase3BSubmissionState.READY_FOR_REVIEW: "Ready for review",
    Phase3BSubmissionState.REVIEW_APPROVED: "Review approved",
    Phase3BSubmissionState.REVIEW_REJECTED: "Review rejected",
    Phase3BSubmissionState.REVIEW_CORRECTION_REQUESTED: "Correction requested",
    Phase3BSubmissionState.EXPIRED: "Expired",
    Phase3BSubmissionState.DELETED: "Deleted",
    Phase3BSubmissionState.CLEANUP_FAILED: "Cleanup failed",
    Phase3BSubmissionState.SUPERSEDED: "Superseded",
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


def _references_block(references: tuple[SourceReference, ...]) -> str:
    if not references:
        return (
            "<p class=\"no-evidence\">No source reference is claimed; this is not a "
            "grounded statement.</p>"
        )
    rows = []
    for reference in references:
        observed = _fmt(reference.observed_at)
        rows.append(
            "<details class=\"reference\">"
            f"<summary>Source reference: {escape(reference.label)}</summary>"
            "<dl>"
            f"<dt>Synthetic identity</dt><dd>{escape(reference.source_id)}</dd>"
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
        "<div class=\"references\"><h3>Source references (local disclosure)</h3>"
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
    body_attr = f" class=\"{escape(body_class)}\"" if body_class else ""
    return (
        "<!DOCTYPE html>"
        "<html lang=\"en\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{escape(title)} \u2014 Jebediah Executive Product Shell</title>"
        "<link rel=\"stylesheet\" href=\"/static/styles.css\">"
        "</head>"
        f"<body{body_attr}>"
        "<a class=\"skip-link\" href=\"#main-content\">Skip to main content</a>"
        "<header class=\"site-header\">"
        "<div class=\"brand\">"
        "<span class=\"product-title\">Jebediah Executive Product Shell</span>"
        f"<span class=\"badge synthetic\">{escape(SYNTHETIC_BADGE)}</span>"
        "</div>"
        f"<p class=\"disconnected\">{escape(DISCONNECTED_STATEMENT)}</p>"
        f"<p class=\"clock\">Fixed synthetic clock: {escape(_fmt(briefing.assembled_at))}"
        "</p>"
        f"<p class=\"scenario\">{escape(briefing.scenario_label)}</p>"
        f"<p class=\"scope-scope\">Coverage scope: "
        f"{escape(briefing.coverage.scope_statement)}</p>"
        "</header>"
        "<nav class=\"primary-nav\" aria-label=\"Primary\">"
        f"<ul>{''.join(nav_links)}</ul>"
        "</nav>"
        "<main id=\"main-content\">"
        f"<h1>{escape(heading)}</h1>"
        f"{main_html}"
        "</main>"
        "<footer class=\"site-footer\">"
        f"<p class=\"no-action\">{escape(NO_ACTION_STATEMENT)} It is non-operational.</p>"
        f"<p class=\"badge synthetic\">{escape(SYNTHETIC_BADGE)}</p>"
        "<div class=\"footer-limitations\"><h2>Material limitations</h2>"
        f"<ul>{footer_limits}</ul></div>"
        "</footer>"
        "</body></html>"
    )


def render_overview(briefing: ExecutiveBriefing) -> str:
    counts = briefing.summary_counts
    summary = (
        "<section aria-label=\"Executive summary\"><h2>Executive summary</h2>"
        "<p class=\"status-banner\"><span aria-hidden=\"true\">\u25c9</span> "
        "Synthetic status: a bounded fabricated briefing is ready for review.</p>"
        "<dl class=\"summary-counts\">"
        f"<dt>Priorities needing attention</dt><dd>{counts.priority_count}</dd>"
        f"<dt>Unresolved decisions</dt><dd>{counts.unresolved_decision_count}</dd>"
        f"<dt>Organizational gates</dt><dd>{counts.organizational_gate_count}</dd>"
        f"<dt>Upcoming synthetic deadlines (30 days)</dt>"
        f"<dd>{counts.upcoming_deadline_count}</dd>"
        f"<dt>Recent evidence updates (30 days)</dt>"
        f"<dd>{counts.recent_evidence_update_count}</dd>"
        f"<dt>Eligible synthetic sources</dt><dd>{counts.eligible_source_count}</dd>"
        "</dl>"
        "<p class=\"derived-note\">Every count is derived from this fabricated "
        "fixture, not entered directly.</p></section>"
    )
    questions = "".join(
        _section_block(briefing, section)
        for section in (
            BriefingSection.HAPPENING,
            BriefingSection.ATTENTION,
            BriefingSection.KNOW,
            BriefingSection.NEXT,
        )
    )
    main = summary + questions + _coverage_block(briefing.coverage)
    return _document(
        title="Overview",
        nav_current="overview",
        heading="Executive overview",
        main_html=main,
        briefing=briefing,
    )


def render_attention(briefing: ExecutiveBriefing) -> str:
    main = _section_block(briefing, BriefingSection.ATTENTION)
    return _document(
        title="Needs attention",
        nav_current="attention",
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
        nav_current="knowledge",
        heading="What Jebediah knows",
        main_html=main,
        briefing=briefing,
    )


def render_next(briefing: ExecutiveBriefing) -> str:
    main = _section_block(briefing, BriefingSection.NEXT)
    return _document(
        title="What happens next",
        nav_current="next",
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


def _phase3b_submission_row(workspace: Phase3BWorkspaceView) -> str:
    rows: list[str] = []
    for submission in workspace.submissions:
        duplicate = (
            escape(submission.duplicate_of)
            if submission.duplicate_of is not None
            else "none"
        )
        warnings = "; ".join(escape(value) for value in submission.warnings) or "none"
        rows.append(
            "<tr>"
            f"<th scope=\"row\"><a href=\"/workspace/submissions/{escape(submission.submission_id)}\">"
            f"{escape(submission.title)}</a></th>"
            f"<td data-label=\"State\">{escape(_PHASE3B_STATE_LABELS[submission.state])} "
            f"<code class=\"enum-value\">{escape(submission.state.value)}</code></td>"
            f"<td data-label=\"SHA-256\">{escape(submission.sha256_hex)}</td>"
            f"<td data-label=\"Bytes\">{submission.byte_count}</td>"
            f"<td data-label=\"Duplicate of\">{duplicate}</td>"
            f"<td data-label=\"Warnings\">{warnings}</td>"
            f"<td data-label=\"Received at\">{escape(_fmt(submission.received_at))}</td>"
            "</tr>"
        )
    return "".join(rows)


def _phase3b_workspace_section(workspace: Phase3BWorkspaceView) -> str:
    recent = "".join(
        f"<li>{escape(entry)}</li>" for entry in workspace.recent_events
    ) or "<li>No synthetic audit events recorded yet.</li>"
    return (
        "<section aria-label=\"Synthetic PDF intake\">"
        "<h2>Synthetic PDF intake and custody workspace</h2>"
        "<p>Submit one synthetic PDF fixture at a time. Browser-pushed bytes are "
        "accepted only through this loopback form; no server-side path, URL, or "
        "remote fetch is available.</p>"
        "<form class=\"intake-form\" method=\"post\" action=\"/workspace/intake\" "
        "enctype=\"multipart/form-data\">"
        "<label for=\"receipt-id\">Receipt ID</label>"
        "<input id=\"receipt-id\" name=\"receipt_id\" type=\"text\" required>"
        "<label for=\"pdf-upload\">Synthetic PDF fixture</label>"
        "<input id=\"pdf-upload\" name=\"pdf\" type=\"file\" accept=\"application/pdf\" required>"
        "<button type=\"submit\">Admit synthetic PDF</button>"
        "</form>"
        "<form class=\"recover-form\" method=\"post\" action=\"/workspace/recover\" "
        "enctype=\"multipart/form-data\">"
        "<button type=\"submit\">Run recovery sweep</button>"
        "</form>"
        "</section>"
        "<section aria-label=\"Phase 3B submissions\">"
        "<h2>Current synthetic submissions</h2>"
        "<table class=\"workspace-table phase3b-table\"><caption>Sanitized synthetic "
        "PDF submissions under custody</caption><thead><tr>"
        "<th scope=\"col\">Submission</th><th scope=\"col\">State</th>"
        "<th scope=\"col\">SHA-256</th><th scope=\"col\">Bytes</th>"
        "<th scope=\"col\">Duplicate of</th><th scope=\"col\">Warnings</th>"
        "<th scope=\"col\">Received at</th></tr></thead>"
        f"<tbody>{_phase3b_submission_row(workspace)}</tbody></table>"
        + _limitation_list(workspace.limitations, "Phase 3B workspace limitations")
        + "</section>"
        "<section aria-label=\"Recent custody activity\"><h2>Recent custody activity</h2>"
        f"<ul class=\"activity\">{recent}</ul></section>"
    )


def render_workspace(
    briefing: ExecutiveBriefing,
    workspace: Phase3BWorkspaceView | None = None,
) -> str:
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
        "<section aria-label=\"Workspace records\"><h2>Synthetic workspace metadata</h2>"
        "<p>Only sanitized synthetic metadata is shown. No source content, upload "
        "control, document viewer, or file locator exists.</p>"
        "<table class=\"workspace-table\"><caption>Synthetic source, document, "
        "quarantine, review, lineage, and knowledge-object status</caption>"
        "<thead><tr><th scope=\"col\">Record</th><th scope=\"col\">Kind</th>"
        "<th scope=\"col\">State</th><th scope=\"col\">Briefing eligibility</th>"
        "<th scope=\"col\">Source references</th><th scope=\"col\">Last changed</th>"
        "<th scope=\"col\">Limitations</th>"
        "</tr></thead>"
        f"<tbody>{rows}</tbody></table></section>"
        "<section aria-label=\"Recent activity\"><h2>Recent synthetic activity</h2>"
        f"<ul class=\"activity\">{activities}</ul></section>"
    )
    if workspace is not None:
        main += _phase3b_workspace_section(workspace)
    return _document(
        title="Knowledge workspace",
        nav_current="workspace",
        heading="Knowledge workspace",
        main_html=main,
        briefing=briefing,
    )


def render_phase3b_submission_detail(
    briefing: ExecutiveBriefing,
    detail: Phase3BSubmissionDetailView,
) -> str:
    review_entries = "".join(
        "<li>"
        f"{escape(entry.decision)} at {escape(_fmt(entry.created_at))} — "
        f"{escape(entry.note)}</li>"
        for entry in detail.review_entries
    ) or "<li>No review entries recorded yet.</li>"
    warnings = "; ".join(escape(entry) for entry in detail.warnings) or "none"
    main = (
        "<section aria-label=\"Submission detail\">"
        f"<h2>{escape(detail.summary.title)}</h2>"
        f"<p class=\"status-banner\"><span aria-hidden=\"true\">&#9673;</span> "
        f"State: {escape(_PHASE3B_STATE_LABELS[detail.summary.state])} "
        f"<code class=\"enum-value\">{escape(detail.summary.state.value)}</code></p>"
        "<dl class=\"evidence-meta\">"
        f"<dt>Submission ID</dt><dd>{escape(detail.summary.submission_id)}</dd>"
        f"<dt>SHA-256</dt><dd>{escape(detail.summary.sha256_hex)}</dd>"
        f"<dt>Bytes</dt><dd>{detail.summary.byte_count}</dd>"
        f"<dt>Received at</dt><dd>{escape(_fmt(detail.summary.received_at))}</dd>"
        f"<dt>Page count</dt><dd>{detail.page_count}</dd>"
        f"<dt>Native text sufficient</dt><dd>{escape(str(detail.native_text_sufficient).lower())}</dd>"
        f"<dt>Warnings</dt><dd>{warnings}</dd>"
        "</dl>"
        + _limitation_list(detail.limitations, "Submission limitations")
        + "</section>"
        "<section aria-label=\"Review history\"><h2>Review history</h2>"
        f"<ul class=\"activity\">{review_entries}</ul>"
        "<form class=\"review-form\" method=\"post\" "
        f"action=\"/workspace/submissions/{escape(detail.summary.submission_id)}/review\" "
        "enctype=\"multipart/form-data\">"
        "<label for=\"review-note\">Review note</label>"
        "<input id=\"review-note\" name=\"note\" type=\"text\" required>"
        "<label for=\"review-decision\">Decision</label>"
        "<select id=\"review-decision\" name=\"decision\">"
        "<option value=\"approve\">Approve</option>"
        "<option value=\"reject\">Reject</option>"
        "<option value=\"correct\">Request correction</option>"
        "<option value=\"supersede\">Supersede</option>"
        "</select>"
        "<button type=\"submit\">Record review decision</button>"
        "</form>"
        "<form class=\"delete-form\" method=\"post\" "
        f"action=\"/workspace/submissions/{escape(detail.summary.submission_id)}/delete\" "
        "enctype=\"multipart/form-data\">"
        "<button type=\"submit\">Delete submission</button>"
        "</form>"
        "</section>"
    )
    return _document(
        title=detail.summary.title,
        nav_current="workspace",
        heading="Synthetic PDF submission detail",
        main_html=main,
        briefing=briefing,
    )


def render_ask_index(briefing: ExecutiveBriefing) -> str:
    links = []
    for response in briefing.ask_responses:
        links.append(
            "<li>"
            f"<a href=\"/ask/{escape(response.question_id)}\">"
            f"{escape(response.question)}</a> "
            f"<span class=\"badge\">Preset {escape(response.question_id)}</span>"
            "</li>"
        )
    main = (
        "<section aria-label=\"Ask presets\"><h2>Preset synthetic questions</h2>"
        "<p>This surface offers preset synthetic question links only. There is no "
        "text input, prompt box, model, or free-form field.</p>"
        f"<ul class=\"ask-list\">{''.join(links)}</ul></section>"
    )
    return _document(
        title="Ask Jebediah",
        nav_current="ask",
        heading="Ask Jebediah",
        main_html=main,
        briefing=briefing,
    )


def render_ask_response(briefing: ExecutiveBriefing, response: AskResponse) -> str:
    symbol = _ASK_STATE_SYMBOLS[response.state]
    label = _ASK_STATE_LABELS[response.state]
    body = [
        "<section aria-label=\"Ask response\">",
        "<p class=\"badge synthetic\">Synthetic response</p>",
        f"<h2>{escape(response.question)}</h2>",
        f"<p class=\"ask-state\"><span aria-hidden=\"true\">{symbol}</span> "
        f"State: {escape(label)} "
        f"<code class=\"enum-value\">{escape(response.state.value)}</code></p>",
    ]
    if response.state is AskState.GROUNDED and response.statement:
        body.append(f"<p class=\"statement\">{escape(response.statement)}</p>")
    else:
        body.append(
            "<p class=\"no-answer\">No answer is fabricated for this state. The "
            "preset reports its evidence position honestly.</p>"
        )
    body.append(f"<p class=\"coverage\">{escape(response.coverage_statement)}</p>")
    body.append(
        "<p class=\"uncertainty\">Uncertainty: "
        + _enum_label(
            _UNCERTAINTY_LABELS[response.uncertainty], response.uncertainty.value
        )
        + f" \u2014 {escape(response.uncertainty_explanation)}</p>"
    )
    body.append(_references_block(response.source_references))
    body.append(_limitation_list(response.limitations, "Limitations"))
    if response.state is AskState.GROUNDED:
        body.append(
            "<p class=\"grounded-note\">Grounded means only that cited eligible "
            "fabricated-fixture records support this preset. It is not real-world "
            "verification, completeness, or safety for action.</p>"
        )
    body.append("</section>")
    return _document(
        title=f"Ask: {response.question_id}",
        nav_current="ask",
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
            return "<p class=\"none\">None recorded in this fixture.</p>"
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
        "<section aria-label=\"Board status\"><h2>Organizational status (synthetic)</h2>"
        "<p class=\"status-banner\"><span aria-hidden=\"true\">\u25c9</span> "
        f"A fabricated briefing is ready with {counts.priority_count} priorities and "
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
        nav_current="board",
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
        nav_current="states",
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
        nav_current="states",
        heading=f"State: {_STATE_LABELS[state]}",
        main_html=main,
        briefing=briefing,
    )


def render_error(
    briefing: ExecutiveBriefing, *, status_label: str, message: str
) -> str:
    main = (
        "<section aria-label=\"Request problem\"><h2>Request could not be served</h2>"
        f"<p class=\"error-status\">{escape(status_label)}</p>"
        f"<p class=\"error-message\">{escape(message)}</p>"
        "<p class=\"boundary\">No request content is echoed. This synthetic preview "
        "takes no action.</p>"
        "<p><a href=\"/\">Return to the synthetic overview</a></p></section>"
    )
    return _document(
        title=status_label,
        nav_current=None,
        heading="Request problem",
        main_html=main,
        briefing=briefing,
    )
