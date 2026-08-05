from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import inspect

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
    KnowledgeRegistryConflict,
    KnowledgeRegistryRecord,
    KnowledgeRegistryRepository,
    SourceReference,
    TemporalContext,
    TransformationReference,
    UncertaintyAssessment,
    UncertaintyState,
)
from collector.knowledge.registry.in_memory_repository import (
    InMemoryKnowledgeRegistryRepository,
)


NOW = datetime(2026, 8, 4, tzinfo=timezone.utc)


def build_record(
    object_id: str = "knowledge-object-1",
) -> KnowledgeRegistryRecord:
    return KnowledgeRegistryRecord(
        object_id=object_id,
        object_kind="synthetic-derived-record",
        provenance=KnowledgeProvenance(
            producer_id="synthetic-producer",
            created_at=NOW,
            source_references=[
                SourceReference(
                    source_id="synthetic-source",
                    authority_scope="synthetic-tests",
                    source_revision="revision-1",
                )
            ],
            transformation=TransformationReference(
                transformation_id="synthetic-transform",
                transformation_version="version-1",
            ),
            evidence_references=[
                EvidenceReference("evidence-1")
            ],
        ),
        governance_scope=GovernanceScope(
            information_owner_id="synthetic-owner",
            information_domain="synthetic-tests",
            classification="synthetic",
            permitted_consumer_ids=["synthetic-consumer"],
            permitted_uses=["unit-test"],
            retention_policy_id="retention-policy",
            deletion_policy_id="deletion-policy",
            freshness_policy_id="freshness-policy",
            invalidation_policy_id="invalidation-policy",
        ),
        temporal_context=TemporalContext(
            freshness_state=FreshnessState.UNKNOWN,
            freshness_evaluated_at=NOW,
        ),
        uncertainty=UncertaintyAssessment(
            state=UncertaintyState.UNKNOWN,
            explanation="Synthetic evidence cannot establish another state.",
            limitations=["No real evidence is used in unit tests."],
        ),
        human_review=HumanReview(
            review_policy_id="human-review-policy",
            state=HumanReviewState.PENDING,
        ),
        lifecycle=KnowledgeLifecycle(
            state=KnowledgeLifecycleState.REGISTERED,
            recorded_by="synthetic-recorder",
            recorded_at=NOW,
            reason="Synthetic registry construction.",
        ),
    )


def test_repository_contract_exposes_only_reviewed_operations():
    public_methods = {
        name
        for name, member in inspect.getmembers(
            KnowledgeRegistryRepository,
            predicate=inspect.isfunction,
        )
        if not name.startswith("_")
    }

    assert public_methods == {"register", "find", "contains"}

    with pytest.raises(TypeError):
        KnowledgeRegistryRepository()


def test_register_find_and_contains_round_trip():
    repository = InMemoryKnowledgeRegistryRepository()
    record = build_record()
    original = build_record()

    repository.register(record)

    assert repository.contains(record.object_id)
    assert repository.find(record.object_id) == record
    assert record == original


def test_missing_identity_returns_no_record():
    repository = InMemoryKnowledgeRegistryRepository()

    assert repository.find("missing-object") is None
    assert not repository.contains("missing-object")


def test_equal_repeated_registration_is_idempotent():
    repository = InMemoryKnowledgeRegistryRepository()
    record = build_record()

    repository.register(record)
    repository.register(record)
    repository.register(build_record())

    assert repository.find(record.object_id) == record


def test_conflicting_registration_is_visible_and_preserves_original():
    repository = InMemoryKnowledgeRegistryRepository()
    original = build_record()
    conflicting = replace(
        original,
        object_kind="different-synthetic-kind",
    )
    repository.register(original)

    with pytest.raises(
        KnowledgeRegistryConflict,
        match=original.object_id,
    ) as error:
        repository.register(conflicting)

    assert error.value.object_id == original.object_id
    assert repository.find(original.object_id) == original


@pytest.mark.parametrize("object_id", ["", "   "])
def test_lookup_rejects_empty_identity(object_id):
    repository = InMemoryKnowledgeRegistryRepository()

    with pytest.raises(ValueError, match="object_id cannot be empty"):
        repository.find(object_id)

    with pytest.raises(ValueError, match="object_id cannot be empty"):
        repository.contains(object_id)


def test_registration_preserves_review_lifecycle_and_freshness():
    repository = InMemoryKnowledgeRegistryRepository()
    record = build_record()

    repository.register(record)
    stored = repository.find(record.object_id)

    assert stored is not None
    assert stored.human_review.state is HumanReviewState.PENDING
    assert (
        stored.lifecycle.state
        is KnowledgeLifecycleState.REGISTERED
    )
    assert (
        stored.temporal_context.freshness_state
        is FreshnessState.UNKNOWN
    )


def test_returned_record_cannot_mutate_repository_state():
    repository = InMemoryKnowledgeRegistryRepository()
    record = build_record()
    repository.register(record)
    stored = repository.find(record.object_id)

    assert stored is not None
    with pytest.raises(FrozenInstanceError):
        stored.object_kind = "changed"

    assert repository.find(record.object_id) == record


def test_adapter_has_no_mutation_or_retrieval_surface():
    repository = InMemoryKnowledgeRegistryRepository()

    for method_name in (
        "update",
        "delete",
        "list",
        "search",
        "retrieve",
        "review",
        "promote",
        "transition",
    ):
        assert not hasattr(repository, method_name)
