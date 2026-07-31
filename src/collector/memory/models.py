from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class MemoryType(str, Enum):
    FACT = "fact"
    PREFERENCE = "preference"
    DECISION = "decision"
    EVENT = "event"
    CONTEXT = "context"


@dataclass(frozen=True)
class MemoryItem:
    """
    Represents information that has been promoted
    from collected data into persistent memory.
    """

    id: str
    source_identity: str
    content: str
    memory_type: MemoryType
    importance: float
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict = field(default_factory=dict)