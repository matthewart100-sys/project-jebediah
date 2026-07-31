from abc import ABC, abstractmethod

from ...core.pipeline import ProcessedCollectorRecord


class RecordRepository(ABC):
    """
    Persistence contract for collector records.

    Implementations may use:
    - memory
    - databases
    - vector stores
    - remote services

    The collector runtime should only depend
    on this contract.
    """

    @abstractmethod
    def save(
        self,
        record: ProcessedCollectorRecord,
    ) -> str:
        """
        Persist a processed collector record.

        Returns:
            Persistent record identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def find(
        self,
        identity: str,
    ) -> ProcessedCollectorRecord | None:
        """
        Retrieve a record by identity.
        """
        raise NotImplementedError

    @abstractmethod
    def contains(
        self,
        identity: str,
    ) -> bool:
        """
        Determine whether a record exists.
        """
        raise NotImplementedError