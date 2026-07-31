import os

from ..models import MemoryItem
from ..policy import MemoryPolicy

from ..persistence.memory_repository import (
    InMemoryMemoryRepository,
)

from ..persistence.qdrant_repository import (
    QdrantMemoryRepository,
)

from .result import MemoryServiceResult


class MemoryService:
    """
    Runtime coordinator for memory decisions.

    Responsibilities:
    - receive memory candidates
    - apply memory policy
    - persist approved memories

    Storage backend can be selected through:
    MEMORY_BACKEND=memory
    MEMORY_BACKEND=qdrant
    """

    def __init__(
        self,
        repository=None,
        policy=None,
    ):

        self.policy = policy or MemoryPolicy()

        if repository:
            self.repository = repository

        else:
            backend = os.getenv(
                "MEMORY_BACKEND",
                "memory",
            )

            if backend.lower() == "qdrant":
                self.repository = QdrantMemoryRepository()

            else:
                self.repository = InMemoryMemoryRepository()


    def process(
        self,
        memory: MemoryItem,
    ) -> MemoryServiceResult:

        decision = self.policy.evaluate(
            memory
        )

        stored = False

        if decision.accepted:

            self.repository.save(
                memory
            )

            stored = True


        return MemoryServiceResult(
            memory=memory,
            promoted=decision.accepted,
            stored=stored,
        )
