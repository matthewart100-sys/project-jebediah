from ..models import MemoryItem
from ..policy import MemoryPolicy
from ..persistence.memory_repository import InMemoryMemoryRepository

from .result import MemoryServiceResult


class MemoryService:
    """
    Runtime coordinator for memory decisions.

    Responsibilities:
    - receive memory candidates
    - apply memory policy
    - persist approved memories
    """

    def __init__(
        self,
        repository=None,
        policy=None,
    ):
        self.repository = repository or InMemoryMemoryRepository()
        self.policy = policy or MemoryPolicy()

    def process(
        self,
        memory: MemoryItem,
    ) -> MemoryServiceResult:

        decision = self.policy.evaluate(memory)

        stored = False

        if decision.accepted:
            self.repository.save(memory)
            stored = True

        return MemoryServiceResult(
            memory=memory,
            promoted=decision.accepted,
            stored=stored,
        )