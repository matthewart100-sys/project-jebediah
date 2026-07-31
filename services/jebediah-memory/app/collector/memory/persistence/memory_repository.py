from .repository import MemoryRepository
from ..models import MemoryItem


class InMemoryMemoryRepository(MemoryRepository):
    """
    Reference memory persistence implementation.
    """

    def __init__(self):
        self._memories: dict[str, MemoryItem] = {}


    def save(
        self,
        memory: MemoryItem,
    ) -> str:

        self._memories[memory.id] = memory

        return memory.id


    def find(
        self,
        memory_id: str,
    ) -> MemoryItem | None:

        return self._memories.get(memory_id)


    def contains(
        self,
        memory_id: str,
    ) -> bool:

        return memory_id in self._memories