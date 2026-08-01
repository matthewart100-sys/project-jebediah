from abc import ABC, abstractmethod

from .identity import EmbeddingIdentity


class EmbeddingProvider(ABC):
    """
    Contract for text embedding providers.

    Implementations may use:
    - Ollama
    - cloud APIs
    - local models

    Memory logic should not depend
    on a specific embedding backend.
    """

    @property
    @abstractmethod
    def identity(self) -> EmbeddingIdentity:
        raise NotImplementedError

    @abstractmethod
    def ensure_ready(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> list[float]:
        raise NotImplementedError
