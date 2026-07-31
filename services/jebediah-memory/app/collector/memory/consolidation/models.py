from dataclasses import dataclass
from enum import Enum


class ConsolidationAction(str, Enum):
    PROMOTE = "promote"
    REJECT = "reject"
    MERGE = "merge"


@dataclass(frozen=True)
class ConsolidationDecision:
    """
    Final decision produced by the consolidation engine.
    """

    action: ConsolidationAction
    score: float
    confidence: float
    duplicate: bool
    reason: str