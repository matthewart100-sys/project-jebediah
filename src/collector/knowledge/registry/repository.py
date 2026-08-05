from abc import ABC, abstractmethod

from .models import KnowledgeRegistryRecord


class KnowledgeRegistryConflict(RuntimeError):
    """Raised when one object identity is reused for different metadata."""

    def __init__(self, object_id: str) -> None:
        self.object_id = object_id
        super().__init__(
            f"knowledge registry identity conflict: {object_id}"
        )


def _validate_object_id(object_id: str) -> None:
    if not isinstance(object_id, str) or not object_id.strip():
        raise ValueError("object_id cannot be empty")


class KnowledgeRegistryRepository(ABC):
    """Storage-neutral contract for immutable registry metadata."""

    @abstractmethod
    def register(self, record: KnowledgeRegistryRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        object_id: str,
    ) -> KnowledgeRegistryRecord | None:
        raise NotImplementedError

    @abstractmethod
    def contains(self, object_id: str) -> bool:
        raise NotImplementedError
