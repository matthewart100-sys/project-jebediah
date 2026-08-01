from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..governance import (
    MemoryLifecycleState,
    lifecycle_from_payload,
)


@dataclass(frozen=True)
class RetrievalSignals:
    semantic_relevance: float
    confidence: float | None
    importance: float | None
    created_at: datetime | None
    lifecycle_state: MemoryLifecycleState


@dataclass(frozen=True)
class RetrievalCandidate:
    memory_id: str | None
    content: str | None
    metadata: dict[str, Any]
    signals: RetrievalSignals

    @classmethod
    def from_payload(
        cls,
        semantic_relevance: float,
        payload: dict[str, Any],
    ) -> "RetrievalCandidate":
        metadata = payload.get("metadata", {})
        intelligence = (
            metadata.get("intelligence", {})
            if isinstance(metadata, dict)
            else {}
        )

        confidence = _optional_number(
            intelligence.get("confidence")
        )
        importance = _optional_number(
            payload.get("importance")
        )
        created_at = _optional_datetime(
            payload.get("created_at")
        )
        lifecycle = lifecycle_from_payload(
            payload.get("lifecycle")
        )
        memory_id = payload.get("memory_id")

        return cls(
            memory_id=(
                str(memory_id)
                if memory_id is not None
                else None
            ),
            content=payload.get("content"),
            metadata=dict(payload),
            signals=RetrievalSignals(
                semantic_relevance=float(semantic_relevance),
                confidence=confidence,
                importance=importance,
                created_at=created_at,
                lifecycle_state=lifecycle.state,
            ),
        )


def _optional_number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None

    return float(value)


def _optional_datetime(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None
