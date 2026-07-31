from dataclasses import dataclass
from enum import Enum


class RetentionLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class MemoryScore:
    """
    Represents the calculated importance
    of a memory.
    """

    importance: float
    retention: RetentionLevel


@dataclass(frozen=True)
class ConfidenceScore:
    """
    Represents how trustworthy a memory is.
    """

    value: float
    reason: str


@dataclass(frozen=True)
class IntelligenceResult:
    """
    Combined output from the intelligence layer.
    """

    memory_id: str
    score: MemoryScore
    confidence: ConfidenceScore