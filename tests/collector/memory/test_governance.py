from datetime import datetime, timezone

import pytest

from collector.memory import MemoryItem, MemoryType
from collector.memory.governance import (
    MemoryLifecycle,
    MemoryLifecycleState,
    MemoryProvenance,
    VerificationState,
    ensure_memory_governance,
    lifecycle_from_payload,
    lifecycle_to_payload,
    provenance_from_payload,
    provenance_to_payload,
)


def make_memory(**changes):
    values = {
        "id": "memory-1",
        "source_identity": "source-record-1",
        "content": "Synthetic governed memory.",
        "memory_type": MemoryType.FACT,
        "importance": 0.9,
    }
    values.update(changes)
    return MemoryItem(**values)


def test_governance_adds_safe_legacy_defaults():
    memory = ensure_memory_governance(
        make_memory(),
        confidence_basis="explicit user statement",
    )

    assert memory.provenance is not None
    assert memory.provenance.source == "source-record-1"
    assert memory.provenance.confidence_basis == "explicit user statement"
    assert (
        memory.provenance.verification_state
        == VerificationState.UNVERIFIED
    )
    assert memory.lifecycle.state == MemoryLifecycleState.ACTIVE


def test_governance_preserves_supplied_context_and_evidence():
    provenance = MemoryProvenance(
        source="user",
        creator="synthetic-actor",
        creation_context="unit-test fixture",
        supporting_evidence=("fixture:evidence-1",),
    )

    memory = ensure_memory_governance(
        make_memory(provenance=provenance),
        confidence_basis="explicit user statement",
    )

    assert memory.provenance is not None
    assert memory.provenance.creator == "synthetic-actor"
    assert memory.provenance.creation_context == "unit-test fixture"
    assert memory.provenance.supporting_evidence == (
        "fixture:evidence-1",
    )
    assert memory.provenance.confidence_basis == "explicit user statement"


def test_governance_payload_round_trip_supports_requested_states():
    changed_at = datetime(2026, 7, 31, tzinfo=timezone.utc)
    provenance = MemoryProvenance(
        source="system",
        creator="synthetic-service",
        creation_context="synthetic observation",
        confidence_basis="controlled fixture",
        verification_state=VerificationState.VERIFIED,
        supporting_evidence=("fixture:observation-1",),
    )
    lifecycle = MemoryLifecycle(
        state=MemoryLifecycleState.SUPERSEDED,
        reinforcement_count=2,
        superseded_by="memory-2",
        changed_at=changed_at,
    )

    restored_provenance = provenance_from_payload(
        provenance_to_payload(provenance, "source-record-1"),
        "source-record-1",
    )
    restored_lifecycle = lifecycle_from_payload(
        lifecycle_to_payload(lifecycle)
    )

    assert restored_provenance == provenance
    assert restored_lifecycle == lifecycle
    assert {state.value for state in MemoryLifecycleState} == {
        "active",
        "reinforced",
        "superseded",
        "archived",
    }


def test_legacy_payloads_default_to_unverified_and_active():
    provenance = provenance_from_payload(None, "legacy-source")
    lifecycle = lifecycle_from_payload(None)

    assert provenance.source == "legacy-source"
    assert provenance.verification_state == VerificationState.UNVERIFIED
    assert lifecycle.state == MemoryLifecycleState.ACTIVE


def test_invalid_lifecycle_state_fails_visibly():
    with pytest.raises(ValueError):
        lifecycle_from_payload({"state": "unknown"})
