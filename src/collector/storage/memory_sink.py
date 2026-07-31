from ..core.pipeline import ProcessedCollectorRecord
from .interface import StorageSink


class InMemorySink(StorageSink):
    """
    Simple in-memory Collector storage.

    Used for testing contracts before adding
    persistent backends.
    """

    def __init__(self):
        self._records: dict[str, ProcessedCollectorRecord] = {}

    def store(
        self,
        record: ProcessedCollectorRecord,
    ) -> str:

        self._records[record.identity] = record

        return record.identity

    def get(
        self,
        identity: str,
    ) -> ProcessedCollectorRecord | None:

        return self._records.get(identity)

    def exists(
        self,
        identity: str,
    ) -> bool:

        return identity in self._records