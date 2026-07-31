from abc import ABC, abstractmethod


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

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> list[float]:
        raise NotImplementedError
