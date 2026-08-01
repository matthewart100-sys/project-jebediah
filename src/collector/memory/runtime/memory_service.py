from ..models import MemoryItem
from ..governance import ensure_memory_governance
from ..policy import MemoryPolicy

from ..persistence.memory_repository import (
    InMemoryMemoryRepository,
)

from .result import MemoryServiceResult


class MemoryService:
    """
    Runtime coordinator for memory decisions.

    Responsibilities:
    - receive memory candidates
    - apply memory policy
    - persist approved memories

    The default in-memory repository remains a reference implementation.
    Durable semantic persistence is explicitly composed by the memory
    application service; this coordinator never fabricates a Qdrant vector.
    """

    def __init__(
        self,
        repository=None,
        policy=None,
    ):

        self.policy = policy or MemoryPolicy()

        self.repository = repository or InMemoryMemoryRepository()


    def process(
        self,
        memory: MemoryItem,
        persist: bool = True,
    ) -> MemoryServiceResult:

        intelligence = memory.metadata.get(
            "intelligence",
            {},
        )
        confidence_basis = (
            intelligence.get("confidence_reason")
            if isinstance(intelligence, dict)
            else None
        )
        governed_memory = ensure_memory_governance(
            memory,
            confidence_basis=confidence_basis,
        )

        decision = self.policy.evaluate(
            governed_memory
        )

        stored = False

        if decision.accepted and persist:

            self.repository.save(
                governed_memory
            )

            stored = True


        return MemoryServiceResult(
            memory=governed_memory,
            promoted=decision.accepted,
            stored=stored,
        )
