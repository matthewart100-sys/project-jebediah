from .interface import EmbeddingProvider
from .identity import (
    APPROVED_EMBEDDING_DIGEST,
    APPROVED_EMBEDDING_MODEL,
    APPROVED_EMBEDDING_PROVIDER,
    APPROVED_NORMALIZATION,
    APPROVED_VECTOR_DIMENSIONS,
    EmbeddingCompatibilityError,
    EmbeddingConfigurationError,
    EmbeddingError,
    EmbeddingIdentity,
    EmbeddingVectorError,
    validate_embedding_vector,
)
from .ollama_adapter import OllamaEmbeddingProvider

__all__ = [
    "EmbeddingProvider",
    "EmbeddingIdentity",
    "EmbeddingError",
    "EmbeddingConfigurationError",
    "EmbeddingCompatibilityError",
    "EmbeddingVectorError",
    "OllamaEmbeddingProvider",
    "APPROVED_EMBEDDING_PROVIDER",
    "APPROVED_EMBEDDING_MODEL",
    "APPROVED_EMBEDDING_DIGEST",
    "APPROVED_VECTOR_DIMENSIONS",
    "APPROVED_NORMALIZATION",
    "validate_embedding_vector",
]
