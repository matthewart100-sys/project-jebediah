from ..interface import StorageSink
from ..persistence.repository import RecordRepository
from ...core.pipeline import ProcessedCollectorRecord


class RepositoryAdapter(StorageSink):
    """
    Adapter that exposes a persistence repository
    through the Collector storage contract.
    """

    def __init__(
        self,
        repository: RecordRepository,
    ):
        self.repository = repository

    def store(
        self,
        record: ProcessedCollectorRecord,
    ) -> str:
        return self.repository.save(record)

    def get(
        self,
        identity: str,
    ) -> ProcessedCollectorRecord | None:
        return self.repository.find(identity)

    def exists(
        self,
        identity: str,
    ) -> bool:
        return self.repository.contains(identity)