import math

import pytest

from collector.embeddings import (
    APPROVED_EMBEDDING_DIGEST,
    APPROVED_EMBEDDING_MODEL,
    EmbeddingCompatibilityError,
    EmbeddingIdentity,
    EmbeddingVectorError,
    validate_embedding_vector,
)


def test_approved_embedding_identity_round_trips_exactly():
    identity = EmbeddingIdentity.approved()

    assert identity.to_payload() == {
        "provider": "ollama",
        "model": "nomic-embed-text:v1.5",
        "manifest_digest": APPROVED_EMBEDDING_DIGEST,
        "dimensions": 768,
        "normalization": "none",
    }
    assert EmbeddingIdentity.from_payload(identity.to_payload()) == identity


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("provider", "other"),
        ("model", "nomic-embed-text:latest"),
        ("manifest_digest", "sha256:other"),
        ("dimensions", 1),
        ("normalization", "l2"),
    ],
)
def test_embedding_identity_rejects_any_compatibility_mismatch(field, value):
    payload = EmbeddingIdentity.approved().to_payload()
    payload[field] = value

    with pytest.raises(EmbeddingCompatibilityError):
        EmbeddingIdentity.from_payload(payload)


@pytest.mark.parametrize(
    "vector",
    [
        [],
        [1.0] * 767,
        [1.0] * 769,
        [0.0] * 768,
        [1.0] * 767 + [math.inf],
        [1.0] * 767 + [math.nan],
        [1.0] * 767 + ["invalid"],
        [1.0] * 767 + [True],
    ],
)
def test_embedding_vector_validation_rejects_incompatible_geometry(vector):
    with pytest.raises(EmbeddingVectorError):
        validate_embedding_vector(vector)


def test_embedding_vector_validation_preserves_raw_values():
    vector = [2.5] * 768

    assert validate_embedding_vector(vector) == vector


def test_approved_constants_match_the_accepted_artifact():
    identity = EmbeddingIdentity.approved()

    assert identity.model == APPROVED_EMBEDDING_MODEL
    assert identity.manifest_digest == APPROVED_EMBEDDING_DIGEST
