from dataclasses import dataclass

from ..models import MemoryItem


@dataclass(frozen=True)
class MemoryPipelineResult:
    """
    Result returned by the memory pipeline.

    Represents the complete outcome of a memory
    candidate moving through intelligence,
    consolidation, and persistence.
    """

    memory: MemoryItem
    accepted: bool
    consolidated: bool
    stored: bool
    reason: str