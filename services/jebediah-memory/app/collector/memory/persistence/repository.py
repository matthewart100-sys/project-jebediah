from abc import ABC, abstractmethod

from ..models import MemoryItem


class MemoryRepository(ABC):
    """
    Persistence contract for promoted memories.

    Implementations may use:
    - memory
    - databases
    - vector stores
    - remote services

    Memory domain depends only on this contract.
    """

    @abstractmethod
    def save(
        self,
        memory: MemoryItem,
    ) -> str:
        raise NotImplementedError


    @abstractmethod
    def find(
        self,
        memory_id: str,
    ) -> MemoryItem | None:
        raise NotImplementedError


    @abstractmethod
    def contains(
        self,
        memory_id: str,
    ) -> bool:
        raise NotImplementedError