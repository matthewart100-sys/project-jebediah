from dataclasses import dataclass

from ..models import MemoryItem


@dataclass
class MemoryServiceResult:
    """
    Result returned from memory runtime operations.
    """

    memory: MemoryItem
    promoted: bool
    stored: bool