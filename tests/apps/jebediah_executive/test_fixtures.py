"""Layer 2 - synthetic fixture tests for the Executive Product Shell.

These tests prove that the single deterministic scenario
``synthetic-nonprofit-demo-v1`` is byte-for-byte stable, uses only visibly
synthetic ``demo-`` identities, exercises every required kind, context,
uncertainty, freshness, and evidence-gap example, derives its overview counts,
and never imports a current runtime package or claims a live organizational
state.
"""

from __future__ import annotations

import re
from datetime import timezone

import pytest

from apps.jebediah_executive import fixtures as fx
from apps.jebediah_executive.fixtures import (
    ALLOWED_SCENARIOS,
    CLOCK,
    SCENARIO_ID,
    SyntheticBriefingProvider,
    build_briefing,
)
from apps.jebediah_executive.models import (
    BriefingSection,
    EvidenceClassification,
    FreshnessState,
    KnowledgeKind,
    NextContext,
    NextItemKind,
    UncertaintyState,
    WorkspaceState,
    unique_source_references,
)

_IDENTITY_RE = re.compile(r"^demo-[a-z0-9-]+$")


def test_only_scenario_is_the_synthetic_nonprofit_demo() -> None:
    assert SCENARIO_ID == "synthetic-nonprofit-demo-v1"
    assert ALLOWED_SCENARIOS == frozenset({SCENARIO_ID})
    with pytest.raises(ValueError):
        SyntheticBriefingProvider("some-other-scenario")


def test_provider_returns_the_scenario_briefing() -> None:
    provider = SyntheticBriefingProvider()
    briefing = provider.briefing()
    assert provider.scenario_id == SCENARIO_ID
    assert briefing.scenario_id == SCENARIO_ID


def test_clock_is_timezone_aware_and_fixed() -> None:
    assert CLOCK.tzinfo is timezone.utc
    a = build_briefing()
    b = build_briefing()
    assert a.assembled_at == b.assembled_at == CLOCK


def test_fixture_is_deterministic() -> None:
    first = build_briefing()
    second = build_briefing()
    # Frozen dataclasses compare by value; equality proves determinism.
    assert first == second


def test_all_identities_are_visibly_synthetic() -> None:
    briefing = build_briefing()
    ids: list[str] = [briefing.briefing_id]
    for item in briefing.items:
        ids.append(item.item_id)
        if item.transformation_id:
            ids.append(item.transformation_id)
        ids.extend(r.source_id for r in item.source_references)
    for record in briefing.workspace_records:
        ids.append(record.record_id)
        ids.extend(r.source_id for r in record.source_references)
    for activity in briefing.activities:
        ids.append(activity.activity_id)
        ids.extend(r.source_id for r in activity.source_references)
    for response in briefing.ask_responses:
        ids.extend(r.source_id for r in response.source_references)
    for identity in ids:
        assert _IDENTITY_RE.match(identity), identity


def test_no_real_looking_locators_or_urls() -> None:
    briefing = build_briefing()
    haystack = repr(briefing)
    for forbidden in ("http://", "https://", "www.", "@", "\\", "://"):
        assert forbidden not in haystack, forbidden


def test_all_four_sections_have_eligible_content() -> None:
    briefing = build_briefing()
    for section in BriefingSection:
        assert briefing.items_in_section(section), section


def test_all_next_kinds_and_contexts_represented() -> None:
    briefing = build_briefing()
    nexts = briefing.items_in_section(BriefingSection.NEXT)
    kinds = {item.next_kind for item in nexts}
    contexts = {item.next_context for item in nexts}
    assert kinds == set(NextItemKind)
    assert contexts == set(NextContext)


def test_all_knowledge_kinds_represented() -> None:
    briefing = build_briefing()
    know = briefing.items_in_section(BriefingSection.KNOW)
    kinds = {item.knowledge_kind for item in know}
    assert kinds == set(KnowledgeKind)


def test_all_uncertainty_and_freshness_states_represented() -> None:
    briefing = build_briefing()
    uncertainties = {item.uncertainty for item in briefing.items}
    freshness = {item.freshness for item in briefing.items}
    assert uncertainties == set(UncertaintyState)
    assert freshness == set(FreshnessState)


def test_attention_links_to_separate_next_without_next_kind() -> None:
    briefing = build_briefing()
    attention = briefing.items_in_section(BriefingSection.ATTENTION)
    linked = [item for item in attention if item.related_item_ids]
    assert linked, "at least one attention item links to a next item"
    for item in linked:
        assert item.next_kind is None
        for related in item.related_item_ids:
            target = briefing.item_by_id(related)
            assert target is not None
            assert target.section is BriefingSection.NEXT


def test_attention_links_are_topically_coherent_not_merely_existing() -> None:
    """Each linked next item genuinely corresponds to its attention item.

    Coherence is proven structurally: the attention item and its linked next
    item share at least one synthetic source reference (the same fabricated
    evidence subject), and their titles share a topic keyword.
    """
    briefing = build_briefing()
    attention = briefing.items_in_section(BriefingSection.ATTENTION)
    linked = [item for item in attention if item.related_item_ids]
    assert linked
    checked = 0
    for item in linked:
        source_ids = {ref.source_id for ref in item.source_references}
        assert source_ids, "a linked attention item cites synthetic evidence"
        for related in item.related_item_ids:
            target = briefing.item_by_id(related)
            assert target is not None
            target_ids = {ref.source_id for ref in target.source_references}
            # Genuine correspondence: shared fabricated evidence subject.
            assert source_ids & target_ids, (
                f"{item.item_id} and {related} must share a source reference"
            )
            checked += 1
    assert checked >= 2

    # Explicit topic coherence for the two curated links.
    grant = briefing.item_by_id("demo-item-attention-grant")
    grant_next = briefing.item_by_id("demo-item-next-grant-extension")
    assert "grant" in grant.title.lower()
    assert "grant" in grant_next.title.lower()

    cash = briefing.item_by_id("demo-item-attention-cash")
    cash_next = briefing.item_by_id("demo-item-next-cash-reconciliation")
    assert "cash" in cash.title.lower()
    assert "cash" in cash_next.title.lower()


def test_next_section_retains_one_decision_and_one_gate() -> None:
    briefing = build_briefing()
    nxt = briefing.items_in_section(BriefingSection.NEXT)
    decisions = [i for i in nxt if i.next_kind is NextItemKind.DECISION_REQUIRED]
    gates = [i for i in nxt if i.next_kind is NextItemKind.ORGANIZATIONAL_GATE]
    assert len(decisions) == 1
    assert len(gates) == 1
    assert briefing.summary_counts.unresolved_decision_count == 1
    assert briefing.summary_counts.organizational_gate_count == 1


def test_evidence_gap_examples_present() -> None:
    briefing = build_briefing()
    # Missing evidence -> open_question with no references.
    assert any(
        item.evidence_classification is EvidenceClassification.OPEN_QUESTION
        and not item.source_references
        for item in briefing.items
    )
    # Conflicting evidence -> conflicting uncertainty retaining competing refs.
    conflicting = [
        item
        for item in briefing.items
        if item.uncertainty is UncertaintyState.CONFLICTING
    ]
    assert conflicting
    assert any(len(item.source_references) >= 2 for item in conflicting)
    # Stale evidence example.
    assert any(item.freshness is FreshnessState.STALE for item in briefing.items)


def test_workspace_examples_include_held_and_restricted() -> None:
    briefing = build_briefing()
    states = {record.state for record in briefing.workspace_records}
    # A held record demonstrates the human/policy gate exclusion.
    assert WorkspaceState.HELD in states
    # A restricted record demonstrates non-ordinary eligibility.
    assert WorkspaceState.UNAUTHORIZED in states


def test_coverage_represents_missing_conflicting_stale_and_held() -> None:
    briefing = build_briefing()
    coverage = briefing.coverage
    # Missing, conflicting, stale, held, unavailable, and partial evidence are
    # represented through bounded coverage sets and the briefing limitations.
    assert coverage.missing_subjects
    assert coverage.conflicting_subjects
    assert coverage.stale_subjects
    assert coverage.held_subjects


def test_overview_counts_derive_from_the_fixture() -> None:
    briefing = build_briefing()
    counts = briefing.summary_counts
    # priority_count equals active attention items.
    assert counts.priority_count == len(
        briefing.items_in_section(BriefingSection.ATTENTION)
    )
    assert counts.eligible_source_count == len(
        unique_source_references(briefing.items)
    )
    for value in (
        counts.priority_count,
        counts.unresolved_decision_count,
        counts.organizational_gate_count,
        counts.upcoming_deadline_count,
        counts.recent_evidence_update_count,
        counts.eligible_source_count,
    ):
        assert value >= 0


def test_provider_returns_one_process_start_briefing() -> None:
    provider = SyntheticBriefingProvider()
    first = provider.briefing()
    second = provider.briefing()
    assert first is second
    assert first == build_briefing()


def test_ask_presets_cite_fixture_or_return_insufficient_or_failed() -> None:
    briefing = build_briefing()
    grounded = briefing.ask_response("grounded-priorities")
    insufficient = briefing.ask_response("insufficient-program-outcomes")
    failed = briefing.ask_response("failed-source-review")
    assert grounded is not None and grounded.source_references
    assert insufficient is not None and insufficient.statement is None
    assert failed is not None and failed.statement is None
    assert not failed.source_references


def test_no_current_organizational_state_claim() -> None:
    briefing = build_briefing()
    text = repr(briefing).lower()
    for forbidden in ("as of today", "currently", "live data", "in production"):
        assert forbidden not in text, forbidden


def test_no_runtime_package_imported_by_fixtures() -> None:
    source = fx.__file__
    with open(source, "r", encoding="utf-8") as handle:
        content = handle.read()
    for forbidden in ("import collector", "jebediah_memory", "qdrant", "fastapi"):
        assert forbidden not in content, forbidden
