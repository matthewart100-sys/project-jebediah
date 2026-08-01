import os
import re
from typing import Any

from .interface import EmbeddingProvider
from .identity import (
    APPROVED_EMBEDDING_DIGEST,
    APPROVED_EMBEDDING_MODEL,
    EmbeddingConfigurationError,
    EmbeddingIdentity,
    EmbeddingVectorError,
    validate_embedding_vector,
)


class OllamaEmbeddingProvider(
    EmbeddingProvider
):
    """
    Ollama-backed embedding provider.
    """


    def __init__(
        self,
        model: str | None = None,
        client: Any | None = None,
    ):
        self.model = (
            model
            or os.getenv(
                "EMBEDDING_MODEL",
                APPROVED_EMBEDDING_MODEL,
            )
        )
        if self.model != APPROVED_EMBEDDING_MODEL or ":latest" in self.model:
            raise EmbeddingConfigurationError(
                "configured embedding model does not match the approved model"
            )

        if client is None:
            import ollama

            client = ollama.Client(
                host=os.getenv("OLLAMA_URL", "http://ollama:11434")
            )

        self.client = client

    @property
    def identity(self) -> EmbeddingIdentity:
        return EmbeddingIdentity.approved()

    def ensure_ready(self) -> None:
        try:
            models = _read_models(self.client.list())
        except Exception as exc:
            raise EmbeddingConfigurationError(
                "unable to verify the approved embedding model"
            ) from exc

        for model in models:
            name = _field(model, "model") or _field(model, "name")
            digest = _field(model, "digest")
            if name == self.model:
                canonical_digest = _canonicalize_manifest_digest(digest)
                if canonical_digest != APPROVED_EMBEDDING_DIGEST:
                    raise EmbeddingConfigurationError(
                        "installed embedding model digest is incompatible"
                    )
                return

        raise EmbeddingConfigurationError(
            "approved embedding model is not installed"
        )


    def embed(
        self,
        text: str,
    ) -> list[float]:
        self.ensure_ready()

        try:
            if hasattr(self.client, "embed"):
                response = self.client.embed(
                    model=self.model,
                    input=text,
                )
                embeddings = _field(response, "embeddings")
                vector = embeddings[0] if embeddings else None
            else:
                response = self.client.embeddings(
                    model=self.model,
                    prompt=text,
                )
                vector = _field(response, "embedding")
        except Exception as exc:
            raise EmbeddingVectorError(
                "embedding generation failed"
            ) from exc

        if not isinstance(vector, (list, tuple)):
            raise EmbeddingVectorError(
                "embedding provider returned no vector"
            )

        return list(validate_embedding_vector(vector))


def _read_models(response: object) -> list[object]:
    models = _field(response, "models")
    if not isinstance(models, (list, tuple)):
        raise EmbeddingConfigurationError(
            "embedding model inventory response is invalid"
        )
    return list(models)


def _canonicalize_manifest_digest(digest: object) -> str:
    """Normalize Ollama's bare SHA-256 digest to the persistence contract."""
    if not isinstance(digest, str):
        raise EmbeddingConfigurationError(
            "installed embedding model digest is missing or malformed"
        )

    hexadecimal = (
        digest.removeprefix("sha256:")
        if digest.startswith("sha256:")
        else digest
    )
    if re.fullmatch(r"[0-9a-fA-F]{64}", hexadecimal) is None:
        raise EmbeddingConfigurationError(
            "installed embedding model digest is missing or malformed"
        )
    return f"sha256:{hexadecimal.lower()}"


def _field(value: object, name: str) -> Any:
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)
