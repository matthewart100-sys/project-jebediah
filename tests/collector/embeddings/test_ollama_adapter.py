from types import SimpleNamespace

import pytest

from collector.embeddings import (
    APPROVED_EMBEDDING_DIGEST,
    APPROVED_EMBEDDING_MODEL,
    EmbeddingConfigurationError,
    EmbeddingVectorError,
    OllamaEmbeddingProvider,
)


class FakeOllamaClient:
    def __init__(
        self,
        *,
        digest=APPROVED_EMBEDDING_DIGEST.removeprefix("sha256:"),
        vector=None,
    ):
        self.digest = digest
        self.vector = vector or [2.0] * 768
        self.embed_calls = []
        self.list_calls = 0

    def list(self):
        self.list_calls += 1
        return {
            "models": [
                {
                    "name": APPROVED_EMBEDDING_MODEL,
                    "model": APPROVED_EMBEDDING_MODEL,
                    "modified_at": "2026-07-31T00:00:00Z",
                    "size": 1,
                    "digest": self.digest,
                    "details": {},
                }
            ]
        }

    def embed(self, **kwargs):
        self.embed_calls.append(kwargs)
        return {"embeddings": [self.vector]}


def test_ollama_provider_verifies_digest_and_preserves_vector():
    client = FakeOllamaClient()
    provider = OllamaEmbeddingProvider(client=client)

    vector = provider.embed("Synthetic embedding input.")

    assert vector == [2.0] * 768
    assert client.embed_calls == [
        {
            "model": APPROVED_EMBEDDING_MODEL,
            "input": "Synthetic embedding input.",
        }
    ]
    assert client.list_calls == 1
    provider.ensure_ready()
    assert client.list_calls == 2
    assert provider.identity.manifest_digest == APPROVED_EMBEDDING_DIGEST


@pytest.mark.parametrize(
    "digest",
    [
        None,
        "",
        "not-a-digest",
        "a" * 63,
        "a" * 65,
        "sha512:" + "a" * 64,
        "f" * 64,
    ],
)
def test_ollama_provider_rejects_invalid_api_digest_before_embedding(digest):
    client = FakeOllamaClient(digest=digest)
    provider = OllamaEmbeddingProvider(client=client)

    with pytest.raises(EmbeddingConfigurationError):
        provider.embed("Synthetic embedding input.")

    assert client.list_calls == 1
    assert not client.embed_calls


def test_ollama_provider_rechecks_digest_before_every_embedding():
    client = FakeOllamaClient()
    provider = OllamaEmbeddingProvider(client=client)

    provider.ensure_ready()
    client.digest = "f" * 64

    with pytest.raises(EmbeddingConfigurationError):
        provider.embed("Synthetic embedding input.")

    assert client.list_calls == 2
    assert not client.embed_calls


def test_ollama_provider_rejects_mutable_model_before_client_use():
    client = FakeOllamaClient()

    with pytest.raises(EmbeddingConfigurationError):
        OllamaEmbeddingProvider(
            model="nomic-embed-text:latest",
            client=client,
        )

    assert client.list_calls == 0


def test_ollama_provider_rejects_digest_mismatch_before_embedding():
    client = FakeOllamaClient(digest="f" * 64)
    provider = OllamaEmbeddingProvider(client=client)

    with pytest.raises(EmbeddingConfigurationError):
        provider.embed("Synthetic embedding input.")

    assert not client.embed_calls


def test_ollama_provider_rejects_missing_model_before_embedding():
    client = FakeOllamaClient()
    client.list = lambda: SimpleNamespace(models=[])
    provider = OllamaEmbeddingProvider(client=client)

    with pytest.raises(EmbeddingConfigurationError):
        provider.embed("Synthetic embedding input.")

    assert not client.embed_calls


def test_ollama_provider_rejects_invalid_vector():
    client = FakeOllamaClient(vector=[0.0] * 768)
    provider = OllamaEmbeddingProvider(client=client)

    with pytest.raises(EmbeddingVectorError):
        provider.embed("Synthetic embedding input.")
