from .interface import EmbeddingProvider
from .ollama_adapter import OllamaEmbeddingProvider

__all__ = [
    "EmbeddingProvider",
    "OllamaEmbeddingProvider",
]
