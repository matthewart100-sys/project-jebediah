from dataclasses import dataclass, field


@dataclass(frozen=True)
class MemoryCandidateEvent:
    """
    Represents a piece of information produced by the collector
    that may become persistent memory.

    This is an integration event.
    It does not decide whether something becomes memory.
    """

    source_identity: str
    content: str
    metadata: dict = field(default_factory=dict)