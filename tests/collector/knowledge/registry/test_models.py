from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
from typing import cast

import pytest

from collector.knowledge.registry import (
    EvidenceReference,
    FreshnessState,
    GovernanceScope,
    HumanReview,
    HumanReviewState,
    KnowledgeLifecycle,
    KnowledgeLifecycleState,
    KnowledgeProvenance,
    KnowledgeRegistryRecord,
    SourceReference,
    TemporalContext,
    TransformationReference,
    UncertaintyAssessment,
    UncertaintyState,
)


NOW = datetime(2026, 8, 4, tzinfo=timezone.utc)


def build_provenance(
    *,
    source_references=None,
    evidence_references=None,
) -> KnowledgeProvenance:
    return KnowledgeProvenance(
        producer_id="synthetic-producer",
        created_at=NOW,
        source_references=(
            [
                SourceReference(
                    source_id="synthetic-source",
                    authority_scope="synthetic-tests",
                    source_revision="revision-1",
                )
            ]
            if source_references is None
            else source_references
        ),
        transformation=TransformationReference(
            transformation_id="synthetic-transform",
            transformation_version="version-1",
        ),
        evidence_references=(
            [
                EvidenceReference("evidence-1"),
                EvidenceReference("evidence-2"),
            ]
            if evidence_references is None
            else evidence_references
        ),
    )


def build_scope(**overrides) -> GovernanceScope:
    values = {
        "information_owner_id": "synthetic-owner",
        "information_domain": "synthetic-tests",
        "classification": "synthetic",
        "permitted_consumer_ids": ["synthetic-consumer"],
        "permitted_uses": ["unit-test"],
        "retention_policy_id": "retention-policy",
        "deletion_policy_id": "deletion-policy",
        "freshness_policy_id": "freshness-policy",
        "invalidation_policy_id": "invalidation-policy",
    }
    values.update(overrides)
    return GovernanceScope(**values)


def build_record(**overrides) -> KnowledgeRegistryRecord:
    values = {
        "object_id": "knowledge-object-1",
        "object_kind": "synthetic-derived-record",
        "provenance": build_provenance(),
        "governance_scope": build_scope(),
        "temporal_context": TemporalContext(
            freshness_state=FreshnessState.CURRENT,
            freshness_evaluated_at=NOW,
        ),
        "uncertainty": UncertaintyAssessment(
            state=UncertaintyState.BOUNDED,
            explanation="Synthetic evidence is bounded to this test.",
            evidence_ids=["evidence-1"],
            limitations=["Synthetic fixtures do not establish real facts."],
        ),
        "human_review": HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.PENDING,
        ),
        "lifecycle": KnowledgeLifecycle(
            state=KnowledgeLifecycleState.REGISTERED,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic registry construction.",
        ),
    }
    values.update(overrides)
    return KnowledgeRegistryRecord(**values)


@pytest.mark.parametrize(
    ("source_revision", "observed_at"),
    [
        ("revision-1", None),
        (None, NOW),
        ("revision-1", NOW),
    ],
)
def test_source_reference_accepts_versioned_observation_context(
    source_revision,
    observed_at,
):
    reference = SourceReference(
        source_id="synthetic-source",
        authority_scope="synthetic-tests",
        source_revision=source_revision,
        observed_at=observed_at,
    )

    assert reference.source_revision == source_revision
    assert reference.observed_at == observed_at


def test_source_reference_requires_revision_or_observation():
    with pytest.raises(
        ValueError,
        match="requires a revision or observation time",
    ):
        SourceReference(
            source_id="synthetic-source",
            authority_scope="synthetic-tests",
        )


@pytest.mark.parametrize(
    "value",
    ["", "   "],
)
def test_required_identifiers_reject_empty_values(value):
    constructors = (
        lambda: SourceReference(
            source_id=value,
            authority_scope="synthetic-tests",
            source_revision="revision-1",
        ),
        lambda: SourceReference(
            source_id="synthetic-source",
            authority_scope=value,
            source_revision="revision-1",
        ),
        lambda: TransformationReference(
            transformation_id=value,
            transformation_version="version-1",
        ),
        lambda: TransformationReference(
            transformation_id="synthetic-transform",
            transformation_version=value,
        ),
        lambda: EvidenceReference(value),
        lambda: replace(build_provenance(), producer_id=value),
        lambda: build_scope(information_owner_id=value),
        lambda: build_scope(information_domain=value),
        lambda: build_scope(classification=value),
        lambda: build_scope(retention_policy_id=value),
        lambda: build_scope(deletion_policy_id=value),
        lambda: build_scope(freshness_policy_id=value),
        lambda: build_scope(invalidation_policy_id=value),
        lambda: build_scope(permitted_consumer_ids=[value]),
        lambda: build_scope(permitted_uses=[value]),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.UNKNOWN,
            explanation=value,
            limitations=["Synthetic uncertainty limitation."],
        ),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.BOUNDED,
            explanation="Synthetic uncertainty explanation.",
            evidence_ids=[value],
        ),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.UNKNOWN,
            explanation="Synthetic uncertainty explanation.",
            limitations=[value],
        ),
        lambda: HumanReview(
            review_policy_id=value,
            state=HumanReviewState.PENDING,
        ),
        lambda: HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.APPROVED,
            reviewer_id=value,
            decided_at=NOW,
            rationale="Approved for a synthetic test.",
        ),
        lambda: HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.APPROVED,
            reviewer_id="synthetic-human",
            decided_at=NOW,
            rationale=value,
        ),
        lambda: KnowledgeLifecycle(
            state=KnowledgeLifecycleState.REGISTERED,
            recorded_by=value,
            recorded_at=NOW,
            reason="Synthetic registry construction.",
        ),
        lambda: KnowledgeLifecycle(
            state=KnowledgeLifecycleState.REGISTERED,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason=value,
        ),
        lambda: KnowledgeLifecycle(
            state=KnowledgeLifecycleState.SUPERSEDED,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic supersession.",
            successor_object_id=value,
        ),
        lambda: replace(build_record(), object_id=value),
        lambda: replace(build_record(), object_kind=value),
    )

    for constructor in constructors:
        with pytest.raises(ValueError):
            constructor()


@pytest.mark.parametrize(
    "field_name",
    [
        "permitted_consumer_ids",
        "permitted_uses",
    ],
)
def test_governance_scope_requires_non_empty_collections(field_name):
    with pytest.raises(ValueError, match="cannot be empty"):
        build_scope(**{field_name: []})


@pytest.mark.parametrize(
    ("field_name", "values"),
    [
        (
            "permitted_consumer_ids",
            ["synthetic-consumer", "synthetic-consumer"],
        ),
        ("permitted_uses", ["unit-test", "unit-test"]),
    ],
)
def test_governance_scope_rejects_duplicate_identifiers(
    field_name,
    values,
):
    with pytest.raises(ValueError, match="duplicates"):
        build_scope(**{field_name: values})


def test_provenance_normalizes_collections_to_tuples():
    provenance = build_provenance()
    scope = build_scope()

    assert isinstance(provenance.source_references, tuple)
    assert isinstance(provenance.evidence_references, tuple)
    assert isinstance(scope.permitted_consumer_ids, tuple)
    assert isinstance(scope.permitted_uses, tuple)


def test_provenance_requires_source_and_evidence_references():
    with pytest.raises(ValueError, match="source_references"):
        build_provenance(source_references=[])

    with pytest.raises(ValueError, match="evidence_references"):
        build_provenance(evidence_references=[])


def test_provenance_rejects_duplicate_reference_identities():
    source = SourceReference(
        source_id="synthetic-source",
        authority_scope="synthetic-tests",
        source_revision="revision-1",
    )
    evidence = EvidenceReference("evidence-1")

    with pytest.raises(ValueError, match="duplicate source_id"):
        build_provenance(source_references=[source, source])

    with pytest.raises(ValueError, match="duplicate evidence_id"):
        build_provenance(
            evidence_references=[evidence, evidence],
        )


@pytest.mark.parametrize(
    "factory",
    [
        lambda: build_provenance(
            source_references=[EvidenceReference("evidence-1")]
        ),
        lambda: build_provenance(
            evidence_references=[
                SourceReference(
                    source_id="synthetic-source",
                    authority_scope="synthetic-tests",
                    source_revision="revision-1",
                )
            ]
        ),
        lambda: build_scope(permitted_consumer_ids=[None]),
        lambda: build_scope(permitted_uses=[None]),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.BOUNDED,
            explanation="Synthetic uncertainty explanation.",
            evidence_ids=[None],
        ),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.UNKNOWN,
            explanation="Synthetic uncertainty explanation.",
            limitations=[None],
        ),
    ],
)
def test_collections_reject_invalid_items(factory):
    with pytest.raises(ValueError):
        factory()


@pytest.mark.parametrize(
    "factory",
    [
        lambda: build_scope(
            permitted_consumer_ids="synthetic-consumer"
        ),
        lambda: build_scope(permitted_uses="unit-test"),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.BOUNDED,
            explanation="Synthetic uncertainty explanation.",
            evidence_ids="evidence-1",
        ),
        lambda: UncertaintyAssessment(
            state=UncertaintyState.UNKNOWN,
            explanation="Synthetic uncertainty explanation.",
            limitations="Synthetic uncertainty limitation.",
        ),
    ],
)
def test_string_values_are_not_treated_as_collections(factory):
    with pytest.raises(ValueError, match="must be a collection"):
        factory()


@pytest.mark.parametrize(
    "factory",
    [
        lambda: SourceReference(
            source_id="synthetic-source",
            authority_scope="synthetic-tests",
            observed_at=datetime(2026, 8, 4),
        ),
        lambda: replace(
            build_provenance(),
            created_at=datetime(2026, 8, 4),
        ),
        lambda: TemporalContext(
            freshness_state=FreshnessState.CURRENT,
            freshness_evaluated_at=datetime(2026, 8, 4),
        ),
        lambda: TemporalContext(
            freshness_state=FreshnessState.CURRENT,
            freshness_evaluated_at=NOW,
            effective_at=datetime(2026, 8, 4),
        ),
        lambda: TemporalContext(
            freshness_state=FreshnessState.CURRENT,
            freshness_evaluated_at=NOW,
            expires_at=datetime(2026, 8, 4),
        ),
        lambda: HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.APPROVED,
            reviewer_id="synthetic-human",
            decided_at=datetime(2026, 8, 4),
            rationale="Approved for a synthetic test.",
        ),
        lambda: KnowledgeLifecycle(
            state=KnowledgeLifecycleState.REGISTERED,
            recorded_by="synthetic-recorder",
            recorded_at=datetime(2026, 8, 4),
            reason="Synthetic registry construction.",
        ),
    ],
)
def test_retained_times_must_be_timezone_aware(factory):
    with pytest.raises(ValueError, match="timezone-aware"):
        factory()


def test_temporal_context_does_not_infer_policy_ordering():
    context = TemporalContext(
        freshness_state=FreshnessState.AGING,
        freshness_evaluated_at=NOW,
        effective_at=datetime(
            2026,
            8,
            6,
            tzinfo=timezone.utc,
        ),
        expires_at=datetime(
            2026,
            8,
            5,
            tzinfo=timezone.utc,
        ),
    )

    assert context.effective_at > context.expires_at


@pytest.mark.parametrize("state", list(FreshnessState))
def test_freshness_states_retain_exact_values(state):
    context = TemporalContext(
        freshness_state=state,
        freshness_evaluated_at=NOW,
    )

    assert context.freshness_state is state


@pytest.mark.parametrize(
    "factory",
    [
        lambda: TemporalContext(
            freshness_state=cast(FreshnessState, "current"),
            freshness_evaluated_at=NOW,
        ),
        lambda: UncertaintyAssessment(
            state=cast(UncertaintyState, "unknown"),
            explanation="Synthetic uncertainty explanation.",
            limitations=["Synthetic uncertainty limitation."],
        ),
        lambda: HumanReview(
            review_policy_id="human-review-policy",
            state=cast(HumanReviewState, "pending"),
        ),
        lambda: KnowledgeLifecycle(
            state=cast(
                KnowledgeLifecycleState,
                "registered",
            ),
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic registry construction.",
        ),
    ],
)
def test_state_fields_reject_non_enum_values(factory):
    with pytest.raises(ValueError, match="must be"):
        factory()


@pytest.mark.parametrize(
    ("state", "evidence_ids", "limitations"),
    [
        (UncertaintyState.BOUNDED, ["evidence-1"], []),
        (
            UncertaintyState.INCOMPLETE,
            [],
            ["Expected synthetic evidence is absent."],
        ),
        (
            UncertaintyState.CONFLICTING,
            ["evidence-1", "evidence-2"],
            [],
        ),
        (
            UncertaintyState.UNKNOWN,
            [],
            ["Synthetic evidence cannot establish another state."],
        ),
        (UncertaintyState.NOT_APPLICABLE, [], []),
    ],
)
def test_uncertainty_states_retain_bounded_evidence_contract(
    state,
    evidence_ids,
    limitations,
):
    assessment = UncertaintyAssessment(
        state=state,
        explanation="Synthetic uncertainty explanation.",
        evidence_ids=evidence_ids,
        limitations=limitations,
    )

    assert assessment.state is state
    assert assessment.evidence_ids == tuple(evidence_ids)
    assert assessment.limitations == tuple(limitations)


@pytest.mark.parametrize(
    ("state", "evidence_ids", "limitations", "message"),
    [
        (
            UncertaintyState.BOUNDED,
            [],
            [],
            "requires supporting evidence",
        ),
        (
            UncertaintyState.INCOMPLETE,
            [],
            [],
            "requires a missing-evidence limitation",
        ),
        (
            UncertaintyState.CONFLICTING,
            ["evidence-1"],
            [],
            "at least two evidence",
        ),
        (
            UncertaintyState.UNKNOWN,
            [],
            [],
            "requires an explanatory limitation",
        ),
        (
            UncertaintyState.NOT_APPLICABLE,
            ["evidence-1"],
            [],
            "cannot claim evidence",
        ),
    ],
)
def test_uncertainty_states_reject_insufficient_or_invalid_basis(
    state,
    evidence_ids,
    limitations,
    message,
):
    with pytest.raises(ValueError, match=message):
        UncertaintyAssessment(
            state=state,
            explanation="Synthetic uncertainty explanation.",
            evidence_ids=evidence_ids,
            limitations=limitations,
        )


def test_record_requires_uncertainty_evidence_in_provenance():
    with pytest.raises(
        ValueError,
        match="must exist in provenance",
    ):
        build_record(
            uncertainty=UncertaintyAssessment(
                state=UncertaintyState.BOUNDED,
                explanation="Synthetic evidence basis.",
                evidence_ids=["missing-evidence"],
            )
        )


@pytest.mark.parametrize(
    ("state", "reviewer_id", "decided_at", "rationale"),
    [
        (HumanReviewState.PENDING, None, None, None),
        (
            HumanReviewState.APPROVED,
            "synthetic-human",
            NOW,
            "Approved for a synthetic test.",
        ),
        (
            HumanReviewState.REJECTED,
            "synthetic-human",
            NOW,
            "Rejected for a synthetic test.",
        ),
    ],
)
def test_human_review_retains_explicit_state_and_decision_evidence(
    state,
    reviewer_id,
    decided_at,
    rationale,
):
    review = HumanReview(
        review_policy_id="human-review-policy",
        state=state,
        reviewer_id=reviewer_id,
        decided_at=decided_at,
        rationale=rationale,
    )

    assert review.state is state
    assert review.reviewer_id == reviewer_id


@pytest.mark.parametrize(
    ("reviewer_id", "decided_at", "rationale"),
    [
        ("synthetic-human", None, None),
        (None, NOW, None),
        (None, None, "Unexpected decision evidence."),
    ],
)
def test_pending_review_rejects_decision_evidence(
    reviewer_id,
    decided_at,
    rationale,
):
    with pytest.raises(
        ValueError,
        match="cannot contain decision evidence",
    ):
        HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.PENDING,
            reviewer_id=reviewer_id,
            decided_at=decided_at,
            rationale=rationale,
        )


@pytest.mark.parametrize(
    "state",
    [
        HumanReviewState.APPROVED,
        HumanReviewState.REJECTED,
    ],
)
@pytest.mark.parametrize(
    ("reviewer_id", "decided_at", "rationale"),
    [
        (None, NOW, "Approved for a synthetic test."),
        ("synthetic-human", None, "Approved for a synthetic test."),
        ("synthetic-human", NOW, None),
        ("", NOW, "Approved for a synthetic test."),
        ("synthetic-human", NOW, ""),
    ],
)
def test_decided_review_requires_complete_human_evidence(
    state,
    reviewer_id,
    decided_at,
    rationale,
):
    with pytest.raises(ValueError):
        HumanReview(
            review_policy_id="human-review-policy",
            state=state,
            reviewer_id=reviewer_id,
            decided_at=decided_at,
            rationale=rationale,
        )


@pytest.mark.parametrize(
    ("state", "successor_object_id"),
    [
        (KnowledgeLifecycleState.REGISTERED, None),
        (
            KnowledgeLifecycleState.SUPERSEDED,
            "knowledge-object-2",
        ),
        (KnowledgeLifecycleState.ARCHIVED, None),
        (KnowledgeLifecycleState.INVALIDATED, None),
    ],
)
def test_lifecycle_states_retain_exact_evidence(
    state,
    successor_object_id,
):
    lifecycle = KnowledgeLifecycle(
        state=state,
        recorded_by="synthetic-recorder",
        recorded_at=NOW,
        reason="Synthetic lifecycle state.",
        successor_object_id=successor_object_id,
    )

    assert lifecycle.state is state
    assert lifecycle.recorded_by == "synthetic-recorder"
    assert lifecycle.recorded_at == NOW
    assert lifecycle.reason == "Synthetic lifecycle state."
    assert lifecycle.successor_object_id == successor_object_id


@pytest.mark.parametrize(
    "state",
    [
        KnowledgeLifecycleState.REGISTERED,
        KnowledgeLifecycleState.ARCHIVED,
        KnowledgeLifecycleState.INVALIDATED,
    ],
)
def test_non_superseded_lifecycle_rejects_successor(state):
    with pytest.raises(
        ValueError,
        match="only superseded lifecycle",
    ):
        KnowledgeLifecycle(
            state=state,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic lifecycle state.",
            successor_object_id="knowledge-object-2",
        )


def test_superseded_lifecycle_requires_different_successor():
    with pytest.raises(
        ValueError,
        match="requires successor_object_id",
    ):
        KnowledgeLifecycle(
            state=KnowledgeLifecycleState.SUPERSEDED,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic supersession.",
        )

    with pytest.raises(
        ValueError,
        match="must differ from object_id",
    ):
        build_record(
            lifecycle=KnowledgeLifecycle(
                state=KnowledgeLifecycleState.SUPERSEDED,
                recorded_by="synthetic-recorder",
                recorded_at=NOW,
                reason="Synthetic supersession.",
                successor_object_id="knowledge-object-1",
            )
        )


def test_registry_record_is_deeply_immutable():
    record = build_record()

    with pytest.raises(FrozenInstanceError):
        record.object_kind = "changed"

    with pytest.raises(FrozenInstanceError):
        record.provenance.producer_id = "changed"

    with pytest.raises(TypeError):
        record.governance_scope.permitted_uses[0] = "changed"


def test_equal_registry_records_compare_as_immutable_values():
    first = build_record()
    second = build_record()

    assert first == second
    assert hash(first) == hash(second)


def test_registry_record_contains_no_content_or_authority_shortcuts():
    field_names = {field.name for field in fields(KnowledgeRegistryRecord)}

    assert field_names.isdisjoint(
        {
            "content",
            "metadata",
            "embedding",
            "score",
            "confidence",
            "factual_certainty",
            "model_self_confidence",
            "probability",
            "promotion_authority",
            "truth_probability",
            "retrieval_eligibility",
            "action_authority",
            "source_correction_authority",
        }
    )
