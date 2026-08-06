from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence

from collector.embeddings import EmbeddingIdentity

from ..models import MemoryItem
from ..retrieval import RetrievalCandidate


@dataclass(frozen=True)
class MemoryIndexWriteResult:
    memory_id: str
    point_id: str
    vector_dimensions: int
    payload: dict
    reconciled: bool = False


class SemanticMemoryRepository(Protocol):
    """Combined durable-memory and semantic-index contract from ADR 0003."""

    def index(
        self,
        memory: MemoryItem,
        vector: Sequence[float],
        embedding_identity: EmbeddingIdentity,
    ) -> MemoryIndexWriteResult: ...

    def find(self, memory_id: str) -> MemoryItem | None: ...

    def contains(self, memory_id: str) -> bool: ...

    def search(
        self,
        query_vector: Sequence[float],
        embedding_identity: EmbeddingIdentity,
        limit: int,
        metadata_filter: Mapping[str, str] | None = None,
    ) -> list[RetrievalCandidate]: ...


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
