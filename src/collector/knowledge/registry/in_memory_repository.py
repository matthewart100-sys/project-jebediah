from .models import KnowledgeRegistryRecord
from .repository import (
    KnowledgeRegistryConflict,
    KnowledgeRegistryRepository,
    _validate_object_id,
)


class InMemoryKnowledgeRegistryRepository(
    KnowledgeRegistryRepository
):
    """Process-local reference adapter with no durability guarantee."""

    def __init__(self) -> None:
        self._records: dict[str, KnowledgeRegistryRecord] = {}

    def register(self, record: KnowledgeRegistryRecord) -> None:
        if not isinstance(record, KnowledgeRegistryRecord):
            raise TypeError(
                "record must be a KnowledgeRegistryRecord"
            )

        existing = self._records.get(record.object_id)
        if existing is None:
            self._records[record.object_id] = record
            return

        if existing != record:
            raise KnowledgeRegistryConflict(record.object_id)

    def find(
        self,
        object_id: str,
    ) -> KnowledgeRegistryRecord | None:
        _validate_object_id(object_id)
        return self._records.get(object_id)

    def contains(self, object_id: str) -> bool:
        _validate_object_id(object_id)
        return object_id in self._records
