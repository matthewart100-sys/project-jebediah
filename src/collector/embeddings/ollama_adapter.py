import os

import ollama

from .interface import EmbeddingProvider


class OllamaEmbeddingProvider(
    EmbeddingProvider
):
    """
    Ollama-backed embedding provider.
    """


    def __init__(
        self,
        model: str | None = None,
    ):

        self.model = (
            model
            or os.getenv(
                "EMBEDDING_MODEL",
                "nomic-embed-text",
            )
        )


    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = ollama.embeddings(
            model=self.model,
            prompt=text,
        )

        return response["embedding"]
