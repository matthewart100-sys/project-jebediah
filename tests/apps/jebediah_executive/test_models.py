"""Layer 1 - model contract tests for the Executive Product Shell.

These tests prove the frozen view-model contract in
``apps.jebediah_executive.models``: immutability, exact enum vocabularies,
evidence and freshness rules, the workspace kind-state matrix, briefing
eligibility, relationship invariants, derived counts, and the safety guards
that reject URLs, paths, free HTML, executable authority language, score
language, and non-synthetic identities.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta, timezone

import pytest

from apps.jebediah_executive import models as m
from apps.jebediah_executive.models import (
    ActivityEntry,
    ActivityKind,
    AskResponse,
    AskState,
    BriefingItem,
    BriefingSection,
    BriefingState,
    ContractError,
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
    SummaryCounts,
    UncertaintyState,
    WorkspaceKind,
    WorkspaceRecord,
    WorkspaceState,
    derive_freshness,
    derive_summary_counts,
    unique_source_references,
    PERMITTED_NEXT_CONTEXT_TO_KIND,
    WORKSPACE_KIND_STATES,
    ALLOWLISTED_ASK_QUESTION_IDS,
)

CLOCK = datetime(2026, 5, 15, 14, 0, tzinfo=timezone.utc)


def _ref(**overrides: object) -> SourceReference:
    kwargs: dict[str, object] = dict(
        source_id="demo-src-alpha",
        label="Synthetic grant ledger extract",
        evidence_classification=EvidenceClassification.REPORTED_FACT,
        authority_scope="Board finance committee (fabricated)",
        observed_at=CLOCK - timedelta(days=2),
    )
    kwargs.update(overrides)
    return SourceReference(**kwargs)  # type: ignore[arg-type]


def _item(**overrides: object) -> BriefingItem:
    kwargs: dict[str, object] = dict(
        item_id="demo-item-alpha",
        section=BriefingSection.HAPPENING,
        display_order=1,
        title="Synthetic happening item",
        statement="A fabricated event summary with no real content.",
        evidence_classification=EvidenceClassification.REPORTED_FACT,
        assembled_at=CLOCK,
        freshness=FreshnessState.CURRENT,
        evidence_basis="Derived from a fabricated ledger record.",
        uncertainty=UncertaintyState.BOUNDED,
        uncertainty_explanation="Bounded to the synthetic scenario only.",
        limitations=("Synthetic demonstration content only.",),
        source_references=(_ref(),),
        source_observed_at=CLOCK - timedelta(days=2),
    )
    kwargs.update(overrides)
    return BriefingItem(**kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Immutability and enum vocabularies
# ---------------------------------------------------------------------------

def test_records_are_frozen() -> None:
    ref = _ref()
    with pytest.raises(dataclasses.FrozenInstanceError):
        ref.label = "changed"  # type: ignore[misc]
    item = _item()
    with pytest.raises(dataclasses.FrozenInstanceError):
        item.title = "changed"  # type: ignore[misc]


def test_collections_are_tuples() -> None:
    item = _item()
    assert isinstance(item.source_references, tuple)
    assert isinstance(item.limitations, tuple)
    assert isinstance(item.related_item_ids, tuple)


def test_section_vocabulary_is_exact() -> None:
    assert {s.value for s in BriefingSection} == {
        "happening",
        "attention",
        "know",
        "next",
    }


def test_evidence_vocabulary_is_exact() -> None:
    assert {e.value for e in EvidenceClassification} == {
        "verified_fact",
        "reported_fact",
        "working_assumption",
        "open_question",
        "derived_summary",
    }


def test_freshness_vocabulary_is_exact() -> None:
    assert {f.value for f in FreshnessState} == {
        "current",
        "aging",
        "stale",
        "unknown",
        "not_applicable",
    }


def test_uncertainty_vocabulary_is_exact() -> None:
    assert {u.value for u in UncertaintyState} == {
        "bounded",
        "incomplete",
        "conflicting",
        "unknown",
        "not_applicable",
    }


def test_lifecycle_vocabulary_is_exact() -> None:
    assert {lifecycle.value for lifecycle in LifecycleState} == {
        "active",
        "superseded",
        "archived",
    }


def test_knowledge_next_and_step_vocabularies() -> None:
    assert {k.value for k in KnowledgeKind} == {
        "material_change",
        "decision",
        "risk",
        "opportunity",
        "knowledge_gap",
    }
    assert {k.value for k in NextItemKind} == {
        "decision_required",
        "organizational_gate",
        "action_candidate",
        "informational_attention",
    }
    assert {s.value for s in PermittedNextStep} == {"navigate", "human_review"}
    assert {s.value for s in AskState} == {"grounded", "insufficient", "failed"}


def test_briefing_state_vocabulary_is_exact() -> None:
    assert {s.value for s in BriefingState} == {
        "ready",
        "loading",
        "empty",
        "partial",
        "stale",
        "insufficient_evidence",
        "held",
        "failed",
        "unauthorized",
        "unavailable",
        "disconnected",
    }


def test_enum_fields_reject_unknown_values() -> None:
    with pytest.raises(ContractError):
        _item(section="happening")  # type: ignore[arg-type]
    with pytest.raises(ContractError):
        _item(evidence_classification="reported_fact")  # type: ignore[arg-type]
    with pytest.raises(ContractError):
        _item(freshness="current")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Section-specific field rules
# ---------------------------------------------------------------------------

def test_knowledge_kind_required_only_for_know() -> None:
    know = _item(
        section=BriefingSection.KNOW,
        knowledge_kind=KnowledgeKind.RISK,
    )
    assert know.knowledge_kind is KnowledgeKind.RISK
    with pytest.raises(ContractError):
        _item(section=BriefingSection.KNOW)  # missing knowledge_kind
    with pytest.raises(ContractError):
        _item(knowledge_kind=KnowledgeKind.RISK)  # not a know item


def test_next_kind_and_context_required_only_for_next() -> None:
    nxt = _item(
        section=BriefingSection.NEXT,
        display_order=1,
        next_kind=NextItemKind.DECISION_REQUIRED,
        next_context=NextContext.DECISION_REQUEST,
        priority_basis="Fabricated board urgency.",
        authority_requirement="Requires board approval (fabricated).",
        permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
    )
    assert nxt.next_kind is NextItemKind.DECISION_REQUIRED
    with pytest.raises(ContractError):
        _item(section=BriefingSection.NEXT, priority_basis="x",
              authority_requirement="y",
              permitted_next_step=PermittedNextStep.NAVIGATE)  # no next_kind
    with pytest.raises(ContractError):
        _item(next_kind=NextItemKind.DECISION_REQUIRED)  # not a next item


def test_next_context_must_match_permitted_table() -> None:
    with pytest.raises(ContractError):
        _item(
            section=BriefingSection.NEXT,
            next_kind=NextItemKind.DECISION_REQUIRED,
            next_context=NextContext.UNRESOLVED_GATE,  # mismatched
            priority_basis="x",
            authority_requirement="y",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        )
    # Every table entry is internally consistent.
    for context, kind in PERMITTED_NEXT_CONTEXT_TO_KIND.items():
        item = _item(
            section=BriefingSection.NEXT,
            next_kind=kind,
            next_context=context,
            priority_basis="Fabricated basis.",
            authority_requirement="Fabricated authority.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        )
        assert item.next_context is context


def test_priority_basis_and_authority_required_for_attention_and_next() -> None:
    with pytest.raises(ContractError):
        _item(section=BriefingSection.ATTENTION)  # missing priority_basis
    attention = _item(
        section=BriefingSection.ATTENTION,
        priority_basis="Fabricated urgency.",
        authority_requirement="Requires board approval (fabricated).",
        permitted_next_step=PermittedNextStep.NAVIGATE,
    )
    assert attention.permitted_next_step is PermittedNextStep.NAVIGATE
    with pytest.raises(ContractError):
        _item(priority_basis="only permitted for attention/next")


def test_display_order_positive_and_review_deadline_aware() -> None:
    with pytest.raises(ContractError):
        _item(display_order=0)
    with pytest.raises(ContractError):
        _item(review_due_at=datetime(2026, 6, 1, 12, 0))  # naive


def test_decision_owner_optional() -> None:
    item = _item(
        section=BriefingSection.NEXT,
        next_kind=NextItemKind.DECISION_REQUIRED,
        next_context=NextContext.DECISION_REQUEST,
        priority_basis="x",
        authority_requirement="y",
        permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        decision_owner=None,
    )
    assert item.decision_owner is None


# ---------------------------------------------------------------------------
# Evidence, freshness, and derivation
# ---------------------------------------------------------------------------

def test_evidence_claims_require_references() -> None:
    with pytest.raises(ContractError):
        _item(
            evidence_classification=EvidenceClassification.VERIFIED_FACT,
            source_references=(),
        )


def test_open_question_requires_no_references() -> None:
    item = _item(
        evidence_classification=EvidenceClassification.OPEN_QUESTION,
        source_references=(),
    )
    assert item.source_references == ()


def test_derived_summary_requires_transformation_id() -> None:
    with pytest.raises(ContractError):
        _item(evidence_classification=EvidenceClassification.DERIVED_SUMMARY)
    ok = _item(
        evidence_classification=EvidenceClassification.DERIVED_SUMMARY,
        transformation_id="demo-transform-1",
    )
    assert ok.transformation_id == "demo-transform-1"
    with pytest.raises(ContractError):
        _item(transformation_id="demo-transform-1")  # not derived


def test_derive_freshness_from_fixed_clock() -> None:
    assert derive_freshness(CLOCK - timedelta(days=3), CLOCK) is FreshnessState.CURRENT
    assert derive_freshness(CLOCK - timedelta(days=20), CLOCK) is FreshnessState.AGING
    assert derive_freshness(CLOCK - timedelta(days=90), CLOCK) is FreshnessState.STALE
    assert derive_freshness(None, CLOCK) is FreshnessState.UNKNOWN
    assert (
        derive_freshness(CLOCK, CLOCK, applicable=False)
        is FreshnessState.NOT_APPLICABLE
    )
    # Wall-clock independence: derivation depends only on supplied timestamps.
    future_assembled = CLOCK + timedelta(days=365)
    assert (
        derive_freshness(future_assembled - timedelta(days=1), future_assembled)
        is FreshnessState.CURRENT
    )


def test_item_freshness_must_match_its_timestamps() -> None:
    with pytest.raises(ContractError):
        _item(freshness=FreshnessState.AGING)
    with pytest.raises(ContractError):
        _item(freshness=FreshnessState.NOT_APPLICABLE)
    item = _item(
        freshness=FreshnessState.NOT_APPLICABLE,
        source_observed_at=None,
    )
    assert item.freshness is FreshnessState.NOT_APPLICABLE


def test_briefing_requires_one_fixed_assembly_clock() -> None:
    briefing = _build_minimal_briefing()
    item = briefing.items[0]
    assert item.source_observed_at is not None
    shifted = dataclasses.replace(
        item,
        assembled_at=CLOCK + timedelta(days=1),
        source_observed_at=item.source_observed_at + timedelta(days=1),
    )
    with pytest.raises(ContractError):
        dataclasses.replace(
            briefing,
            items=(shifted, *briefing.items[1:]),
        )


def test_timestamps_must_be_timezone_aware() -> None:
    with pytest.raises(ContractError):
        _item(assembled_at=datetime(2026, 5, 15, 14, 0))  # naive


def test_limitations_and_uncertainty_must_be_nonempty() -> None:
    with pytest.raises(ContractError):
        _item(limitations=())
    with pytest.raises(ContractError):
        _item(uncertainty_explanation="   ")


def test_score_language_is_rejected() -> None:
    with pytest.raises(ContractError):
        _item(evidence_basis="87% confidence in this claim")
    with pytest.raises(ContractError):
        _item(uncertainty_explanation="probability is high")


# ---------------------------------------------------------------------------
# Safety guards
# ---------------------------------------------------------------------------

def test_source_reference_rejects_paths_urls_and_unsafe_ids() -> None:
    with pytest.raises(ContractError):
        _ref(source_id="not-demo-prefixed")
    with pytest.raises(ContractError):
        _ref(label="See https://example.com/report")
    with pytest.raises(ContractError):
        _ref(label="C:\\secret\\path.txt")
    with pytest.raises(ContractError):
        _ref(authority_scope="../../etc/passwd")


def test_free_html_and_self_action_language_rejected() -> None:
    with pytest.raises(ContractError):
        _item(statement="<script>alert(1)</script>")
    with pytest.raises(ContractError):
        _item(statement="Jebediah approved the grant and sent the funds.")


def test_null_bytes_and_control_chars_rejected() -> None:
    with pytest.raises(ContractError):
        _item(statement="bad\x00null")
    with pytest.raises(ContractError):
        _item(title="bad\x07bell")


# ---------------------------------------------------------------------------
# Workspace matrix and briefing eligibility
# ---------------------------------------------------------------------------

def test_workspace_kind_state_matrix_enforced() -> None:
    # A permitted pair builds; a forbidden pair raises.
    ok = WorkspaceRecord(
        record_id="demo-ws-1",
        kind=WorkspaceKind.SOURCE_RECORD,
        title="Synthetic source",
        state=WorkspaceState.ELIGIBLE,
        source_references=(),
        last_changed_at=CLOCK,
        eligible_for_briefing=True,
        limitations=("Synthetic only.",),
    )
    assert ok.eligible_for_briefing is True
    with pytest.raises(ContractError):
        WorkspaceRecord(
            record_id="demo-ws-2",
            kind=WorkspaceKind.SOURCE_RECORD,
            title="Bad state",
            state=WorkspaceState.RECEIVED,  # document-only state
            source_references=(),
            last_changed_at=CLOCK,
            eligible_for_briefing=False,
            limitations=("Synthetic only.",),
        )


def test_eligibility_exact_pairs_only() -> None:
    # knowledge_object eligible -> may be eligible
    ok = WorkspaceRecord(
        record_id="demo-ws-ko",
        kind=WorkspaceKind.KNOWLEDGE_OBJECT,
        title="Synthetic knowledge object",
        state=WorkspaceState.ELIGIBLE,
        source_references=(),
        last_changed_at=CLOCK,
        eligible_for_briefing=True,
        limitations=("Synthetic only.",),
    )
    assert ok.eligible_for_briefing is True
    # review_approved is not an eligible pair -> eligibility must be False.
    with pytest.raises(ContractError):
        WorkspaceRecord(
            record_id="demo-ws-rev",
            kind=WorkspaceKind.REVIEW,
            title="Approved review",
            state=WorkspaceState.REVIEW_APPROVED,
            source_references=(),
            last_changed_at=CLOCK,
            eligible_for_briefing=True,  # not permitted
            limitations=("Synthetic only.",),
        )


def test_every_matrix_pair_constructs() -> None:
    for kind, states in WORKSPACE_KIND_STATES.items():
        for state in states:
            expected = (kind, state) in {
                (WorkspaceKind.SOURCE_RECORD, WorkspaceState.ELIGIBLE),
                (WorkspaceKind.KNOWLEDGE_OBJECT, WorkspaceState.ELIGIBLE),
            }
            record = WorkspaceRecord(
                record_id="demo-ws-x",
                kind=kind,
                title="Synthetic record",
                state=state,
                source_references=(),
                last_changed_at=CLOCK,
                eligible_for_briefing=expected,
                limitations=("Synthetic only.",),
            )
            assert record.eligible_for_briefing == expected


def test_activity_entry_uses_fabricated_labels_and_states() -> None:
    entry = ActivityEntry(
        activity_id="demo-act-1",
        kind=ActivityKind.EVIDENCE_ADDED,
        summary="Synthetic evidence added",
        occurred_at=CLOCK - timedelta(days=1),
        actor_label="Reviewer role (fabricated)",
        source_references=(_ref(),),
        result_state=WorkspaceState.ACCEPTED,
    )
    assert entry.result_state is WorkspaceState.ACCEPTED


# ---------------------------------------------------------------------------
# Ask responses
# ---------------------------------------------------------------------------

def test_ask_ids_are_the_three_presets() -> None:
    assert ALLOWLISTED_ASK_QUESTION_IDS == {
        "grounded-priorities",
        "insufficient-program-outcomes",
        "failed-source-review",
    }
    with pytest.raises(ContractError):
        AskResponse(
            question_id="not-allowlisted",
            question="?",
            state=AskState.FAILED,
            coverage_statement="x",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="x",
            limitations=("Synthetic only.",),
        )


def test_grounded_requires_evidence_and_insufficient_has_no_answer() -> None:
    with pytest.raises(ContractError):
        AskResponse(
            question_id="grounded-priorities",
            question="?",
            state=AskState.GROUNDED,
            coverage_statement="x",
            uncertainty=UncertaintyState.BOUNDED,
            uncertainty_explanation="x",
            limitations=("Synthetic only.",),
            statement="A grounded claim",
            source_references=(),  # missing evidence
        )
    with pytest.raises(ContractError):
        AskResponse(
            question_id="insufficient-program-outcomes",
            question="?",
            state=AskState.INSUFFICIENT,
            coverage_statement="x",
            uncertainty=UncertaintyState.INCOMPLETE,
            uncertainty_explanation="x",
            limitations=("Synthetic only.",),
            statement="fabricated answer",  # forbidden
        )
    with pytest.raises(ContractError):
        AskResponse(
            question_id="failed-source-review",
            question="?",
            state=AskState.FAILED,
            coverage_statement="x",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="x",
            limitations=("Synthetic only.",),
            source_references=(_ref(),),  # failed must present no evidence
        )


# ---------------------------------------------------------------------------
# Coverage and derived counts
# ---------------------------------------------------------------------------

def test_coverage_sets_must_be_sorted_unique() -> None:
    with pytest.raises(ContractError):
        CoverageSummary(
            scope_statement="Synthetic scope.",
            covered_subjects=("b", "a"),  # unsorted
            missing_subjects=(),
            conflicting_subjects=(),
            stale_subjects=(),
            held_subjects=(),
            eligible_item_count=0,
            source_reference_count=0,
            limitations=("Synthetic only.",),
        )


def test_summary_counts_reject_bool_and_negative() -> None:
    with pytest.raises(ContractError):
        SummaryCounts(
            priority_count=True,  # type: ignore[arg-type]
            unresolved_decision_count=0,
            organizational_gate_count=0,
            upcoming_deadline_count=0,
            recent_evidence_update_count=0,
            eligible_source_count=0,
        )


def test_coverage_counts_reject_bool_and_non_int() -> None:
    for bad in (True, 1.0, "1"):
        with pytest.raises(ContractError):
            CoverageSummary(
                scope_statement="Synthetic scope.",
                covered_subjects=("a",),
                missing_subjects=(),
                conflicting_subjects=(),
                stale_subjects=(),
                held_subjects=(),
                eligible_item_count=bad,  # type: ignore[arg-type]
                source_reference_count=0,
                limitations=("Synthetic only.",),
            )
        with pytest.raises(ContractError):
            CoverageSummary(
                scope_statement="Synthetic scope.",
                covered_subjects=("a",),
                missing_subjects=(),
                conflicting_subjects=(),
                stale_subjects=(),
                held_subjects=(),
                eligible_item_count=0,
                source_reference_count=bad,  # type: ignore[arg-type]
                limitations=("Synthetic only.",),
            )


def test_display_order_rejects_bool() -> None:
    with pytest.raises(ContractError):
        _item(display_order=True)  # type: ignore[arg-type]


def test_derive_freshness_rejects_naive_timestamps() -> None:
    naive = datetime(2026, 5, 1, 12, 0)
    aware = CLOCK
    with pytest.raises(ContractError):
        derive_freshness(naive, aware)
    with pytest.raises(ContractError):
        derive_freshness(aware, naive)


def test_scenario_id_must_be_allowlisted() -> None:
    assert m.ALLOWLISTED_SCENARIO_ID == "synthetic-nonprofit-demo-v1"
    with pytest.raises(ContractError):
        _build_minimal_briefing(scenario_id="synthetic-other-demo-v9")


def test_briefing_rejects_duplicate_workspace_record_ids() -> None:
    record = WorkspaceRecord(
        record_id="demo-ws-dup",
        kind=WorkspaceKind.SOURCE_RECORD,
        title="Synthetic duplicate source record",
        state=WorkspaceState.ELIGIBLE,
        source_references=(_ref(),),
        last_changed_at=CLOCK - timedelta(days=3),
        eligible_for_briefing=True,
        limitations=("Synthetic only.",),
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(workspace_records=(record, record))


def test_briefing_rejects_duplicate_activity_ids() -> None:
    activity = ActivityEntry(
        activity_id="demo-act-dup",
        kind=ActivityKind.EVIDENCE_ADDED,
        summary="Synthetic duplicate activity",
        occurred_at=CLOCK - timedelta(days=1),
        actor_label="Reviewer role (fabricated)",
        source_references=(),
        result_state=WorkspaceState.ACCEPTED,
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(activities=(activity, activity))


def test_briefing_rejects_duplicate_ask_presets() -> None:
    def _resp(qid: str) -> AskResponse:
        return AskResponse(
            question_id=qid,
            question="Synthetic preset question?",
            state=AskState.FAILED,
            coverage_statement="Synthetic coverage.",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="Bounded synthetic uncertainty.",
            limitations=("Synthetic only.",),
        )

    # Four responses: one preset repeated, a third missing -> rejected.
    duplicated = (
        _resp("grounded-priorities"),
        _resp("grounded-priorities"),
        _resp("insufficient-program-outcomes"),
        _resp("failed-source-review"),
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(ask_responses=duplicated)


def _build_minimal_briefing(**overrides: object) -> ExecutiveBriefing:
    items = (
        _item(item_id="demo-h1", section=BriefingSection.HAPPENING, display_order=1),
        _item(
            item_id="demo-a1",
            section=BriefingSection.ATTENTION,
            display_order=1,
            priority_basis="Fabricated urgency.",
            authority_requirement="Requires board approval (fabricated).",
            permitted_next_step=PermittedNextStep.NAVIGATE,
            related_item_ids=("demo-n1",),
            review_due_at=CLOCK + timedelta(days=10),
        ),
        _item(
            item_id="demo-n1",
            section=BriefingSection.NEXT,
            display_order=1,
            next_kind=NextItemKind.DECISION_REQUIRED,
            next_context=NextContext.DECISION_REQUEST,
            priority_basis="Fabricated basis.",
            authority_requirement="Requires board approval (fabricated).",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
    )
    activities = (
        ActivityEntry(
            activity_id="demo-act-1",
            kind=ActivityKind.EVIDENCE_ADDED,
            summary="Synthetic evidence added",
            occurred_at=CLOCK - timedelta(days=2),
            actor_label="Reviewer role (fabricated)",
            source_references=(),
            result_state=WorkspaceState.ACCEPTED,
        ),
    )
    counts = derive_summary_counts(items, activities, CLOCK)
    coverage = CoverageSummary(
        scope_statement="Synthetic scope.",
        covered_subjects=("alpha",),
        missing_subjects=(),
        conflicting_subjects=(),
        stale_subjects=(),
        held_subjects=(),
        eligible_item_count=len(items),
        source_reference_count=len(unique_source_references(items)),
        limitations=("Synthetic only.",),
    )
    ask = tuple(
        AskResponse(
            question_id=qid,
            question="Synthetic preset question?",
            state=AskState.FAILED,
            coverage_statement="Synthetic coverage.",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="Bounded synthetic uncertainty.",
            limitations=("Synthetic only.",),
        )
        for qid in ALLOWLISTED_ASK_QUESTION_IDS
    )
    kwargs: dict[str, object] = dict(
        briefing_id="demo-brief-1",
        scenario_id="synthetic-nonprofit-demo-v1",
        scenario_label="Synthetic scenario (fabricated)",
        state=BriefingState.READY,
        assembled_at=CLOCK,
        coverage=coverage,
        items=items,
        workspace_records=(),
        activities=activities,
        ask_responses=ask,
        summary_counts=counts,
        limitations=("Synthetic demonstration only.",),
    )
    kwargs.update(overrides)
    return ExecutiveBriefing(**kwargs)  # type: ignore[arg-type]


def test_briefing_rejects_fixture_entered_counts() -> None:
    wrong = SummaryCounts(
        priority_count=99,
        unresolved_decision_count=0,
        organizational_gate_count=0,
        upcoming_deadline_count=0,
        recent_evidence_update_count=0,
        eligible_source_count=0,
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(summary_counts=wrong)


def test_briefing_counts_are_derived() -> None:
    briefing = _build_minimal_briefing()
    assert briefing.summary_counts.priority_count == 1
    assert briefing.summary_counts.unresolved_decision_count == 1
    assert briefing.summary_counts.upcoming_deadline_count == 1
    assert briefing.summary_counts.recent_evidence_update_count == 1


def test_relationships_reject_self_reference_and_cycles() -> None:
    with pytest.raises(ContractError):
        _item(item_id="demo-x", related_item_ids=("demo-x",))
    with pytest.raises(ContractError):
        _item(related_item_ids=("demo-dup", "demo-dup"))
    # Mutual relationship rejected at briefing level.
    items = (
        _item(item_id="demo-a", related_item_ids=("demo-b",)),
        _item(item_id="demo-b", display_order=2, related_item_ids=("demo-a",)),
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(items=items)


def test_briefing_requires_exactly_three_ask_presets() -> None:
    partial = (
        AskResponse(
            question_id="grounded-priorities",
            question="?",
            state=AskState.FAILED,
            coverage_statement="x",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="x",
            limitations=("Synthetic only.",),
        ),
    )
    with pytest.raises(ContractError):
        _build_minimal_briefing(ask_responses=partial)


def test_superseded_items_rejected_at_briefing_level() -> None:
    bad = _item(item_id="demo-old", lifecycle=LifecycleState.SUPERSEDED)
    with pytest.raises(ContractError):
        _build_minimal_briefing(items=(bad,))


def test_unique_source_references_sorted_and_deduplicated() -> None:
    items = (
        _item(item_id="demo-1", source_references=(_ref(source_id="demo-b"),)),
        _item(
            item_id="demo-2",
            display_order=2,
            source_references=(_ref(source_id="demo-a"), _ref(source_id="demo-b")),
        ),
    )
    refs = unique_source_references(items)
    assert [r.source_id for r in refs] == ["demo-a", "demo-b"]
