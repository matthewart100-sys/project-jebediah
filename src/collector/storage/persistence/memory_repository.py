from .repository import RecordRepository
from ...core.pipeline import ProcessedCollectorRecord


class MemoryRepository(RecordRepository):
    """
    In-memory persistence implementation.

    This exists as the reference implementation
    for the RecordRepository contract before
    external persistence systems are introduced.
    """

    def __init__(self):
        self._records: dict[str, ProcessedCollectorRecord] = {}

    def save(
        self,
        record: ProcessedCollectorRecord,
    ) -> str:
        self._records[record.identity] = record

        return record.identity

    def find(
        self,
        identity: str,
    ) -> ProcessedCollectorRecord | None:
        return self._records.get(identity)

    def contains(
        self,
        identity: str,
    ) -> bool:
        return identity in self._records