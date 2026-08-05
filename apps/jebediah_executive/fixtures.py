"""Compiled synthetic briefing provider and preset Ask responses.

This module builds exactly one obviously fabricated scenario,
``synthetic-nonprofit-demo-v1``, using a fixed timezone-aware clock. It reads no
file, environment value, network resource, database, service, model, or current
runtime record. Every identity is a stable ``demo-`` value and every timestamp
derives from the fixed clock, so construction is deterministic and independent
of system time.

None of this content describes a real organization, person, or current
organizational state. It is a demonstration artifact only.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import (
    ActivityEntry,
    ActivityKind,
    ALLOWLISTED_SCENARIO_ID,
    ALLOWLISTED_SCENARIO_IDS,
    AskResponse,
    AskState,
    BriefingItem,
    BriefingSection,
    BriefingState,
    CoverageSummary,
    EvidenceClassification,
    ExecutiveBriefing,
    KnowledgeKind,
    NextContext,
    NextItemKind,
    PermittedNextStep,
    SourceReference,
    UncertaintyState,
    WorkspaceKind,
    WorkspaceRecord,
    WorkspaceState,
    derive_freshness,
    derive_summary_counts,
    unique_source_references,
)

# SYNTHETIC scenario identity. All data below is fabricated. The identity is
# owned by the models module and reused here so there is one source of truth.
SCENARIO_ID = ALLOWLISTED_SCENARIO_ID
SCENARIO_LABEL = "Synthetic scenario: Meridian Community Trust (fabricated demonstration)"
ALLOWED_SCENARIOS: frozenset[str] = ALLOWLISTED_SCENARIO_IDS

# Fixed synthetic assembly clock; never wall-clock time.
CLOCK = datetime(2026, 5, 15, 14, 0, tzinfo=timezone.utc)


def _ago(days: int) -> datetime:
    """Return a fixed timestamp before the synthetic clock."""
    return CLOCK - timedelta(days=days)


def _ahead(days: int) -> datetime:
    """Return a fixed timestamp after the synthetic clock."""
    return CLOCK + timedelta(days=days)


def _reference(
    source_id: str,
    label: str,
    classification: EvidenceClassification,
    authority_scope: str,
    observed_days_ago: int | None,
) -> SourceReference:
    observed = None if observed_days_ago is None else _ago(observed_days_ago)
    return SourceReference(
        source_id=source_id,
        label=label,
        evidence_classification=classification,
        authority_scope=authority_scope,
        observed_at=observed,
    )


# --- Shared synthetic source references -------------------------------------

_REF_GALA = _reference(
    "demo-src-gala",
    "Synthetic spring gala reconciliation note",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated fundraising events domain only",
    3,
)
_REF_LEDGER = _reference(
    "demo-src-ledger",
    "Synthetic quarter-to-date giving ledger extract",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated finance summary domain only",
    20,
)
_REF_GRANT = _reference(
    "demo-src-grant",
    "Synthetic capacity grant reporting schedule",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated grants administration domain only",
    3,
)
_REF_BANK_A = _reference(
    "demo-src-bank-a",
    "Synthetic operating account statement A",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated cash position domain only",
    18,
)
_REF_BANK_B = _reference(
    "demo-src-bank-b",
    "Synthetic operating account statement B",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated cash position domain only",
    12,
)
_REF_INSURANCE = _reference(
    "demo-src-insurance",
    "Synthetic liability insurance certificate note",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated risk and insurance domain only",
    90,
)
_REF_POLICY = _reference(
    "demo-src-policy",
    "Synthetic operating reserve policy record",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated governance policy domain only",
    5,
)
_REF_BUDGET = _reference(
    "demo-src-budget",
    "Synthetic approved annual budget summary",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated board decisions domain only",
    9,
)
_REF_FUNDING = _reference(
    "demo-src-funding",
    "Synthetic funder concentration analysis note",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated funding risk domain only",
    16,
)
_REF_OPP = _reference(
    "demo-src-opp",
    "Synthetic capacity-building grant opportunity note",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated opportunities domain only",
    4,
)
_REF_DONORS = _reference(
    "demo-src-donors",
    "Synthetic lapsed-donor stewardship list summary",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated development outreach domain only",
    7,
)
_REF_COMMS = _reference(
    "demo-src-comms",
    "Synthetic communications plan status note",
    EvidenceClassification.REPORTED_FACT,
    "Fabricated communications domain only",
    5,
)
_REF_PARTIAL = _reference(
    "demo-src-partial",
    "Synthetic partial program-activity note",
    EvidenceClassification.WORKING_ASSUMPTION,
    "Fabricated program tracking domain only",
    22,
)


def _item(
    item_id: str,
    section: BriefingSection,
    display_order: int,
    title: str,
    statement: str,
    classification: EvidenceClassification,
    evidence_basis: str,
    uncertainty: UncertaintyState,
    uncertainty_explanation: str,
    limitations: tuple[str, ...],
    *,
    references: tuple[SourceReference, ...] = (),
    observed_days_ago: int | None = None,
    freshness_applicable: bool = True,
    priority_basis: str | None = None,
    review_due_days: int | None = None,
    transformation_id: str | None = None,
    knowledge_kind: KnowledgeKind | None = None,
    next_kind: NextItemKind | None = None,
    next_context: NextContext | None = None,
    decision_owner: str | None = None,
    authority_requirement: str | None = None,
    permitted_next_step: PermittedNextStep | None = None,
    related_item_ids: tuple[str, ...] = (),
) -> BriefingItem:
    observed = None if observed_days_ago is None else _ago(observed_days_ago)
    freshness = derive_freshness(observed, CLOCK, applicable=freshness_applicable)
    review_due_at = None if review_due_days is None else _ahead(review_due_days)
    return BriefingItem(
        item_id=item_id,
        section=section,
        display_order=display_order,
        title=title,
        statement=statement,
        evidence_classification=classification,
        assembled_at=CLOCK,
        freshness=freshness,
        evidence_basis=evidence_basis,
        uncertainty=uncertainty,
        uncertainty_explanation=uncertainty_explanation,
        limitations=limitations,
        source_references=references,
        source_observed_at=observed,
        priority_basis=priority_basis,
        review_due_at=review_due_at,
        transformation_id=transformation_id,
        knowledge_kind=knowledge_kind,
        next_kind=next_kind,
        next_context=next_context,
        decision_owner=decision_owner,
        authority_requirement=authority_requirement,
        permitted_next_step=permitted_next_step,
        related_item_ids=related_item_ids,
    )


def _build_items() -> tuple[BriefingItem, ...]:
    happening = (
        _item(
            "demo-item-happening-gala",
            BriefingSection.HAPPENING,
            1,
            "Spring fundraising gala reconciled",
            "The synthetic spring gala results have been reconciled against the "
            "fabricated events note for this demonstration.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated reconciliation note supports the summary figure.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because a single synthetic reconciliation "
            "note is the only basis.",
            ("Reflects one fabricated note, not audited financial results.",),
            references=(_REF_GALA,),
            observed_days_ago=3,
        ),
        _item(
            "demo-item-happening-giving",
            BriefingSection.HAPPENING,
            2,
            "Quarter-to-date giving summary",
            "A synthetic quarter-to-date giving total is summarized from the "
            "fabricated ledger extract.",
            EvidenceClassification.DERIVED_SUMMARY,
            "Derived from one fabricated ledger extract for demonstration only.",
            UncertaintyState.INCOMPLETE,
            "Uncertainty is incomplete because later synthetic gifts are not yet "
            "included in the fabricated ledger.",
            ("Summary excludes pledged but unrecorded synthetic gifts.",),
            references=(_REF_LEDGER,),
            observed_days_ago=20,
            transformation_id="demo-transform-giving-summary",
        ),
    )

    attention = (
        _item(
            "demo-item-attention-grant",
            BriefingSection.ATTENTION,
            1,
            "Capacity grant report due soon",
            "A synthetic capacity grant report is approaching its fabricated "
            "reporting deadline and needs human attention.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated reporting schedule shows the upcoming synthetic date.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because the fabricated schedule states one "
            "clear synthetic date.",
            ("Deadline is fabricated and carries no real grant obligation.",),
            references=(_REF_GRANT,),
            observed_days_ago=3,
            priority_basis="Ranked first because its fabricated deadline is nearest.",
            review_due_days=10,
            authority_requirement="Requires program staff to prepare the report; "
            "no system action is taken.",
            permitted_next_step=PermittedNextStep.NAVIGATE,
            related_item_ids=("demo-item-next-grant-extension",),
        ),
        _item(
            "demo-item-attention-cash",
            BriefingSection.ATTENTION,
            2,
            "Cash balance figures disagree",
            "Two synthetic operating account statements report different "
            "fabricated cash balances and need reconciliation.",
            EvidenceClassification.REPORTED_FACT,
            "Two fabricated account statements provide conflicting synthetic totals.",
            UncertaintyState.CONFLICTING,
            "Uncertainty is conflicting because the two fabricated statements do "
            "not agree.",
            ("Neither synthetic figure is confirmed; this is not audited data.",),
            references=(_REF_BANK_A, _REF_BANK_B),
            observed_days_ago=12,
            priority_basis="Elevated because two fabricated sources conflict.",
            authority_requirement="Requires finance committee reconciliation before "
            "any conclusion.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
            related_item_ids=("demo-item-next-cash-reconciliation",),
        ),
        _item(
            "demo-item-attention-insurance",
            BriefingSection.ATTENTION,
            3,
            "Insurance certificate not refreshed",
            "A synthetic liability insurance certificate has aged beyond the "
            "fabricated freshness window in this demonstration.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated certificate note is the only, and now stale, basis.",
            UncertaintyState.INCOMPLETE,
            "Uncertainty is incomplete because no newer fabricated certificate "
            "note exists in the fixture.",
            ("Certificate status is fabricated and not a real coverage statement.",),
            references=(_REF_INSURANCE,),
            observed_days_ago=90,
            priority_basis="Flagged because its fabricated evidence is stale.",
            review_due_days=5,
            authority_requirement="Requires operations staff to refresh the record; "
            "no system action is taken.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
    )

    know = (
        _item(
            "demo-item-know-reserve",
            BriefingSection.KNOW,
            1,
            "Operating reserve policy adopted",
            "The synthetic board adopted a fabricated multi-year operating "
            "reserve policy in this scenario.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated policy record documents the synthetic adoption.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because one fabricated policy record is cited.",
            ("Policy is fabricated and does not bind any real organization.",),
            references=(_REF_POLICY,),
            observed_days_ago=5,
            knowledge_kind=KnowledgeKind.MATERIAL_CHANGE,
        ),
        _item(
            "demo-item-know-budget",
            BriefingSection.KNOW,
            2,
            "Annual budget decision recorded",
            "The synthetic board recorded a fabricated approved annual budget for "
            "the demonstration fiscal year.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated budget summary documents the synthetic decision.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because one fabricated budget summary is cited.",
            ("Budget figures are fabricated and not financial guidance.",),
            references=(_REF_BUDGET,),
            observed_days_ago=9,
            knowledge_kind=KnowledgeKind.DECISION,
        ),
        _item(
            "demo-item-know-funding-risk",
            BriefingSection.KNOW,
            3,
            "Funder concentration risk noted",
            "A synthetic analysis notes fabricated reliance on a small number of "
            "funders in this scenario.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated analysis note describes the synthetic concentration.",
            UncertaintyState.INCOMPLETE,
            "Uncertainty is incomplete because future fabricated funding is not "
            "modeled.",
            ("Risk is illustrative and fabricated, not a forecast.",),
            references=(_REF_FUNDING,),
            observed_days_ago=16,
            knowledge_kind=KnowledgeKind.RISK,
        ),
        _item(
            "demo-item-know-opportunity",
            BriefingSection.KNOW,
            4,
            "Capacity-building grant opportunity",
            "A synthetic capacity-building grant opportunity is described in the "
            "fabricated opportunities note.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated opportunity note describes the synthetic prospect.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because one fabricated opportunity note is "
            "cited.",
            ("Opportunity is fabricated and confers no real eligibility.",),
            references=(_REF_OPP,),
            observed_days_ago=4,
            knowledge_kind=KnowledgeKind.OPPORTUNITY,
        ),
        _item(
            "demo-item-know-gap",
            BriefingSection.KNOW,
            5,
            "Program outcome data missing",
            "The fixture has no eligible synthetic evidence for two fabricated "
            "program outcomes, so no claim is made about them.",
            EvidenceClassification.OPEN_QUESTION,
            "No fabricated outcome evidence exists, so this remains an open "
            "question.",
            UncertaintyState.UNKNOWN,
            "Uncertainty is unknown because the fixture contains no outcome "
            "evidence to weigh.",
            ("Absence of evidence is stated plainly; no outcome is inferred.",),
            observed_days_ago=None,
            freshness_applicable=False,
            knowledge_kind=KnowledgeKind.KNOWLEDGE_GAP,
        ),
    )

    nxt = (
        _item(
            "demo-item-next-grant-extension",
            BriefingSection.NEXT,
            1,
            "Decide on capacity grant report response",
            "The synthetic board must decide how to respond to the approaching "
            "fabricated capacity grant reporting deadline before it passes.",
            EvidenceClassification.REPORTED_FACT,
            "The same fabricated capacity grant reporting schedule frames the "
            "synthetic decision.",
            UncertaintyState.BOUNDED,
            "Uncertainty is bounded because the fabricated schedule states one "
            "clear synthetic reporting date.",
            ("The shell records no decision; the board decides outside it.",),
            references=(_REF_GRANT,),
            observed_days_ago=3,
            priority_basis="Time-ordered by its fabricated grant reporting deadline.",
            review_due_days=15,
            next_kind=NextItemKind.DECISION_REQUIRED,
            next_context=NextContext.DECISION_REQUEST,
            decision_owner="Synthetic Board Chair (fabricated role)",
            authority_requirement="Requires a full synthetic board vote; the shell "
            "cannot decide or record it.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
        _item(
            "demo-item-next-cash-reconciliation",
            BriefingSection.NEXT,
            2,
            "Reconcile conflicting cash balances",
            "The synthetic finance committee must reconcile the two fabricated "
            "operating account statements before any cash conclusion is drawn.",
            EvidenceClassification.REPORTED_FACT,
            "The same two fabricated operating account statements frame the "
            "synthetic reconciliation gate.",
            UncertaintyState.INCOMPLETE,
            "Uncertainty is incomplete because the two fabricated statements are "
            "not yet reconciled.",
            ("The shell cannot clear a gate; finance staff must reconcile.",),
            references=(_REF_BANK_A, _REF_BANK_B),
            observed_days_ago=12,
            priority_basis="Grouped as a finance gate awaiting fabricated "
            "reconciliation.",
            next_kind=NextItemKind.ORGANIZATIONAL_GATE,
            next_context=NextContext.UNRESOLVED_GATE,
            decision_owner="Synthetic Finance Committee (fabricated role)",
            authority_requirement="Requires finance committee reconciliation; no "
            "gate is cleared by the shell.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
        _item(
            "demo-item-next-donors",
            BriefingSection.NEXT,
            3,
            "Consider lapsed-donor outreach",
            "A synthetic outreach to fabricated lapsed donors is a possible action "
            "for human consideration only.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated stewardship summary suggests the synthetic candidates.",
            UncertaintyState.INCOMPLETE,
            "Uncertainty is incomplete because donor intent is not modeled in the "
            "fixture.",
            ("No outreach is prepared or sent; this is a fabricated suggestion.",),
            references=(_REF_DONORS,),
            observed_days_ago=7,
            priority_basis="Listed as an optional action candidate for review.",
            next_kind=NextItemKind.ACTION_CANDIDATE,
            next_context=NextContext.POSSIBLE_ACTION_CANDIDATE,
            decision_owner="Synthetic Development Director (fabricated role)",
            authority_requirement="Requires development director decision before any "
            "outreach; the shell performs none.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
        _item(
            "demo-item-next-comms",
            BriefingSection.NEXT,
            4,
            "Communications plan on track",
            "The fabricated communications plan is noted as on track for synthetic "
            "human awareness only.",
            EvidenceClassification.REPORTED_FACT,
            "One fabricated status note supports the synthetic awareness item.",
            UncertaintyState.NOT_APPLICABLE,
            "Uncertainty is not applicable because this is a fabricated status "
            "note, not a claim requiring judgement.",
            ("Awareness only; the shell takes no communications action.",),
            references=(_REF_COMMS,),
            observed_days_ago=5,
            priority_basis="Kept last as informational awareness, not a task.",
            next_kind=NextItemKind.INFORMATIONAL_ATTENTION,
            next_context=NextContext.APPROVED_PLAN,
            authority_requirement="No decision required; fabricated human awareness "
            "only.",
            permitted_next_step=PermittedNextStep.NAVIGATE,
        ),
        _item(
            "demo-item-next-volunteers",
            BriefingSection.NEXT,
            5,
            "Gather updated volunteer counts",
            "Updated fabricated volunteer counts are needed before the synthetic "
            "capacity picture can be completed.",
            EvidenceClassification.OPEN_QUESTION,
            "No fabricated volunteer count is current, so information gathering is "
            "needed.",
            UncertaintyState.UNKNOWN,
            "Uncertainty is unknown because the fixture holds no current volunteer "
            "count.",
            ("The shell gathers nothing; program staff supply the counts.",),
            observed_days_ago=None,
            priority_basis="Listed as an information-gathering need without a date.",
            next_kind=NextItemKind.INFORMATIONAL_ATTENTION,
            next_context=NextContext.INFORMATION_GATHERING_NEED,
            decision_owner="Synthetic Program Team (fabricated role)",
            authority_requirement="Requires program staff to provide fabricated "
            "counts; the shell cannot collect them.",
            permitted_next_step=PermittedNextStep.HUMAN_REVIEW,
        ),
    )

    return happening + attention + know + nxt


def _build_workspace_records() -> tuple[WorkspaceRecord, ...]:
    return (
        WorkspaceRecord(
            record_id="demo-ws-source-ledger",
            kind=WorkspaceKind.SOURCE_RECORD,
            title="Synthetic finance source register",
            state=WorkspaceState.ELIGIBLE,
            source_references=(_REF_LEDGER,),
            last_changed_at=_ago(20),
            eligible_for_briefing=True,
            limitations=("Metadata only; no source content is stored or shown.",),
        ),
        WorkspaceRecord(
            record_id="demo-ws-source-held",
            kind=WorkspaceKind.SOURCE_RECORD,
            title="Synthetic major-donor pledge register (held)",
            state=WorkspaceState.HELD,
            source_references=(),
            last_changed_at=_ago(14),
            eligible_for_briefing=False,
            limitations=(
                "Held by a fabricated policy gate; its content cannot appear as "
                "ordinary evidence.",
            ),
        ),
        WorkspaceRecord(
            record_id="demo-ws-document-gala",
            kind=WorkspaceKind.DOCUMENT,
            title="Synthetic gala reconciliation document",
            state=WorkspaceState.ACCEPTED,
            source_references=(_REF_GALA,),
            last_changed_at=_ago(3),
            eligible_for_briefing=False,
            limitations=(
                "Accepted status is synthetic metadata and does not establish "
                "truth or eligibility.",
            ),
        ),
        WorkspaceRecord(
            record_id="demo-ws-quarantine-attach",
            kind=WorkspaceKind.QUARANTINE,
            title="Synthetic quarantined attachment",
            state=WorkspaceState.QUARANTINED,
            source_references=(),
            last_changed_at=_ago(8),
            eligible_for_briefing=False,
            limitations=("Quarantined synthetic item; excluded from ordinary claims.",),
        ),
        WorkspaceRecord(
            record_id="demo-ws-review-budget",
            kind=WorkspaceKind.REVIEW,
            title="Synthetic budget review record",
            state=WorkspaceState.REVIEW_PENDING,
            source_references=(_REF_BUDGET,),
            last_changed_at=_ago(9),
            eligible_for_briefing=False,
            limitations=("Review status is fabricated metadata, not an approval.",),
        ),
        WorkspaceRecord(
            record_id="demo-ws-lineage-giving",
            kind=WorkspaceKind.LINEAGE,
            title="Synthetic giving-summary lineage",
            state=WorkspaceState.READY,
            source_references=(_REF_LEDGER,),
            last_changed_at=_ago(20),
            eligible_for_briefing=False,
            limitations=("Lineage metadata only; no derivation is executed here.",),
        ),
        WorkspaceRecord(
            record_id="demo-ws-knowledge-reserve",
            kind=WorkspaceKind.KNOWLEDGE_OBJECT,
            title="Synthetic operating reserve knowledge object",
            state=WorkspaceState.ELIGIBLE,
            source_references=(_REF_POLICY,),
            last_changed_at=_ago(5),
            eligible_for_briefing=True,
            limitations=("Eligibility is fabricated and confers no real authority.",),
        ),
        WorkspaceRecord(
            record_id="demo-ws-knowledge-unauth",
            kind=WorkspaceKind.KNOWLEDGE_OBJECT,
            title="Synthetic restricted knowledge object (unauthorized)",
            state=WorkspaceState.UNAUTHORIZED,
            source_references=(),
            last_changed_at=_ago(30),
            eligible_for_briefing=False,
            limitations=(
                "Unauthorized in the fabricated scenario; no content is shown.",
            ),
        ),
    )


def _build_activities() -> tuple[ActivityEntry, ...]:
    steward = "Synthetic Evidence Steward (fabricated role)"
    reviewer = "Synthetic Review Steward (fabricated role)"
    return (
        ActivityEntry(
            activity_id="demo-act-evidence-gala",
            kind=ActivityKind.EVIDENCE_ADDED,
            summary="Synthetic gala reconciliation note added to the fixture.",
            occurred_at=_ago(5),
            actor_label=steward,
            source_references=(_REF_GALA,),
            result_state=WorkspaceState.ACCEPTED,
        ),
        ActivityEntry(
            activity_id="demo-act-evidence-ledger",
            kind=ActivityKind.EVIDENCE_ADDED,
            summary="Synthetic giving ledger extract added to the fixture.",
            occurred_at=_ago(12),
            actor_label=steward,
            source_references=(_REF_LEDGER,),
            result_state=WorkspaceState.READY,
        ),
        ActivityEntry(
            activity_id="demo-act-review-budget",
            kind=ActivityKind.REVIEW_STATE_CHANGED,
            summary="Synthetic budget record moved to review pending.",
            occurred_at=_ago(8),
            actor_label=reviewer,
            source_references=(_REF_BUDGET,),
            result_state=WorkspaceState.REVIEW_PENDING,
        ),
        ActivityEntry(
            activity_id="demo-act-lineage-giving",
            kind=ActivityKind.LINEAGE_RECORDED,
            summary="Synthetic giving-summary lineage recorded as ready.",
            occurred_at=_ago(10),
            actor_label=steward,
            source_references=(_REF_LEDGER,),
            result_state=WorkspaceState.READY,
        ),
        ActivityEntry(
            activity_id="demo-act-knowledge-reserve",
            kind=ActivityKind.KNOWLEDGE_STATUS_CHANGED,
            summary="Synthetic reserve knowledge object marked eligible.",
            occurred_at=_ago(6),
            actor_label=reviewer,
            source_references=(_REF_POLICY,),
            result_state=WorkspaceState.ELIGIBLE,
        ),
        ActivityEntry(
            activity_id="demo-act-evidence-old",
            kind=ActivityKind.EVIDENCE_ADDED,
            summary="Synthetic archival note added before the recent window.",
            occurred_at=_ago(45),
            actor_label=steward,
            source_references=(_REF_INSURANCE,),
            result_state=WorkspaceState.ACCEPTED,
        ),
    )


def _build_ask_responses() -> tuple[AskResponse, ...]:
    return (
        AskResponse(
            question_id="grounded-priorities",
            question="What are the current top synthetic priorities?",
            state=AskState.GROUNDED,
            statement="Within this fabricated fixture, the two highest synthetic "
            "priorities are the approaching capacity grant report and the "
            "conflicting operating cash balances.",
            source_references=(_REF_GRANT, _REF_BANK_A, _REF_BANK_B),
            coverage_statement="Coverage is limited to the fabricated priorities in "
            "the synthetic-nonprofit-demo-v1 fixture.",
            uncertainty=UncertaintyState.BOUNDED,
            uncertainty_explanation="Uncertainty is bounded because both priorities "
            "cite explicit fabricated fixture records.",
            limitations=(
                "Grounded means only that cited fabricated records support this "
                "preset; it is not real-world verification, completeness, or "
                "action safety.",
            ),
        ),
        AskResponse(
            question_id="insufficient-program-outcomes",
            question="What are the measured synthetic program outcomes?",
            state=AskState.INSUFFICIENT,
            source_references=(_REF_PARTIAL,),
            coverage_statement="The fixture holds only a partial fabricated activity "
            "note and no eligible outcome evidence.",
            uncertainty=UncertaintyState.INCOMPLETE,
            uncertainty_explanation="Uncertainty is incomplete because the available "
            "fabricated basis does not measure outcomes.",
            limitations=(
                "No answer is fabricated; the preset reports insufficient evidence "
                "and names the missing basis.",
            ),
        ),
        AskResponse(
            question_id="failed-source-review",
            question="What did the latest synthetic source review conclude?",
            state=AskState.FAILED,
            coverage_statement="No fabricated source review result is available for "
            "this demonstration preset.",
            uncertainty=UncertaintyState.UNKNOWN,
            uncertainty_explanation="Uncertainty is unknown because the fabricated "
            "review could not be assembled in this preset.",
            limitations=(
                "The preset fails visibly and presents no evidence or conclusion.",
            ),
        ),
    )


def _build_coverage(items: tuple[BriefingItem, ...]) -> CoverageSummary:
    ordinary = tuple(item for item in items if item.is_ordinary)
    return CoverageSummary(
        scope_statement="This fabricated Meridian Community Trust scenario covers a "
        "bounded synthetic slice of governance, finance, fundraising, and program "
        "topics; it is not a complete or current picture of any organization.",
        covered_subjects=(
            "Board decisions",
            "Communications",
            "Fundraising events",
            "Grants administration",
            "Operating reserves",
        ),
        missing_subjects=(
            "Program outcomes",
            "Volunteer capacity",
        ),
        conflicting_subjects=("Operating cash balance",),
        stale_subjects=("Liability insurance coverage",),
        held_subjects=("Major-donor pledge details",),
        eligible_item_count=len(ordinary),
        source_reference_count=len(unique_source_references(items)),
        limitations=(
            "Coverage is a curated fabricated demonstration and does not measure "
            "real organizational completeness.",
            "Held, unauthorized, and stale subjects are named but their content is "
            "not shown as ordinary evidence.",
        ),
    )


def build_briefing() -> ExecutiveBriefing:
    """Construct the immutable synthetic executive briefing."""
    items = _build_items()
    activities = _build_activities()
    coverage = _build_coverage(items)
    summary_counts = derive_summary_counts(items, activities, CLOCK)
    return ExecutiveBriefing(
        briefing_id="demo-briefing-nonprofit-v1",
        scenario_id=SCENARIO_ID,
        scenario_label=SCENARIO_LABEL,
        state=BriefingState.READY,
        assembled_at=CLOCK,
        coverage=coverage,
        items=items,
        workspace_records=_build_workspace_records(),
        activities=activities,
        ask_responses=_build_ask_responses(),
        summary_counts=summary_counts,
        limitations=(
            "All content is fabricated synthetic demonstration data, not real, "
            "current, verified, or organization-specific information.",
            "The preview is disconnected and non-operational; it records no "
            "decision and takes no organizational action.",
        ),
    )


class SyntheticBriefingProvider:
    """Returns the one compiled synthetic briefing for allowlisted scenarios."""

    def __init__(self, scenario_id: str = SCENARIO_ID) -> None:
        if scenario_id not in ALLOWED_SCENARIOS:
            raise ValueError("scenario_id is not an allowlisted synthetic scenario")
        self._scenario_id = scenario_id

    @property
    def scenario_id(self) -> str:
        return self._scenario_id

    def briefing(self) -> ExecutiveBriefing:
        """Build a fresh, value-equal immutable synthetic briefing."""
        return build_briefing()
