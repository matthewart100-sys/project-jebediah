from abc import ABC, abstractmethod

from ..core.pipeline import ProcessedCollectorRecord


class StorageSink(ABC):
    """
    Contract for Collector storage destinations.

    Storage implementations must be able to store
    and retrieve processed collector records.
    """

    @abstractmethod
    def store(
        self,
        record: ProcessedCollectorRecord,
    ) -> str:
        """
        Store a processed record.

        Returns:
            Storage identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        identity: str,
    ) -> ProcessedCollectorRecord | None:
        """
        Retrieve a record by identity.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        identity: str,
    ) -> bool:
        """
        Check whether a record exists.
        """
        raise NotImplementedError