from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .models import MemoryItem


class VerificationState(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    DISPUTED = "disputed"


class MemoryLifecycleState(str, Enum):
    ACTIVE = "active"
    REINFORCED = "reinforced"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class MemoryProvenance:
    source: str
    creator: str | None = None
    creation_context: str | None = None
    confidence_basis: str | None = None
    verification_state: VerificationState = VerificationState.UNVERIFIED
    supporting_evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class MemoryLifecycle:
    state: MemoryLifecycleState = MemoryLifecycleState.ACTIVE
    reinforcement_count: int = 0
    superseded_by: str | None = None
    changed_at: datetime | None = None


def ensure_memory_governance(
    memory: "MemoryItem",
    confidence_basis: str | None = None,
) -> "MemoryItem":
    provenance = memory.provenance

    if provenance is None:
        provenance = MemoryProvenance(
            source=memory.source_identity,
            confidence_basis=confidence_basis,
        )
    else:
        changes: dict[str, Any] = {}

        if not provenance.source:
            changes["source"] = memory.source_identity

        if confidence_basis and not provenance.confidence_basis:
            changes["confidence_basis"] = confidence_basis

        if changes:
            provenance = replace(provenance, **changes)

    return replace(memory, provenance=provenance)


def provenance_to_payload(
    provenance: MemoryProvenance | None,
    source_identity: str,
) -> dict[str, Any]:
    effective = provenance or MemoryProvenance(
        source=source_identity,
    )

    return {
        "source": effective.source or source_identity,
        "creator": effective.creator,
        "creation_context": effective.creation_context,
        "confidence_basis": effective.confidence_basis,
        "verification_state": effective.verification_state.value,
        "supporting_evidence": list(effective.supporting_evidence),
    }


def provenance_from_payload(
    payload: object,
    source_identity: str,
) -> MemoryProvenance:
    if payload is None:
        return MemoryProvenance(source=source_identity)

    if not isinstance(payload, dict):
        raise ValueError("memory provenance payload must be an object")

    evidence = payload.get("supporting_evidence", ())

    if not isinstance(evidence, (list, tuple)) or not all(
        isinstance(item, str) for item in evidence
    ):
        raise ValueError("supporting evidence must contain string references")

    return MemoryProvenance(
        source=payload.get("source") or source_identity,
        creator=payload.get("creator"),
        creation_context=payload.get("creation_context"),
        confidence_basis=payload.get("confidence_basis"),
        verification_state=VerificationState(
            payload.get(
                "verification_state",
                VerificationState.UNVERIFIED.value,
            )
        ),
        supporting_evidence=tuple(evidence),
    )


def lifecycle_to_payload(
    lifecycle: MemoryLifecycle,
) -> dict[str, Any]:
    return {
        "state": lifecycle.state.value,
        "reinforcement_count": lifecycle.reinforcement_count,
        "superseded_by": lifecycle.superseded_by,
        "changed_at": (
            lifecycle.changed_at.isoformat()
            if lifecycle.changed_at
            else None
        ),
    }


def lifecycle_from_payload(
    payload: object,
) -> MemoryLifecycle:
    if payload is None:
        return MemoryLifecycle()

    if not isinstance(payload, dict):
        raise ValueError("memory lifecycle payload must be an object")

    changed_at = payload.get("changed_at")

    if changed_at is not None and not isinstance(changed_at, datetime):
        changed_at = datetime.fromisoformat(changed_at)

    return MemoryLifecycle(
        state=MemoryLifecycleState(
            payload.get(
                "state",
                MemoryLifecycleState.ACTIVE.value,
            )
        ),
        reinforcement_count=int(
            payload.get("reinforcement_count", 0)
        ),
        superseded_by=payload.get("superseded_by"),
        changed_at=changed_at,
    )
