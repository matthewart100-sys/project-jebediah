from dataclasses import asdict, dataclass
import math
from numbers import Real
from typing import Any, Sequence


APPROVED_EMBEDDING_PROVIDER = "ollama"
APPROVED_EMBEDDING_MODEL = "nomic-embed-text:v1.5"
APPROVED_EMBEDDING_DIGEST = (
    "sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f"
)
APPROVED_VECTOR_DIMENSIONS = 768
APPROVED_NORMALIZATION = "none"


class EmbeddingError(RuntimeError):
    """Base error for embedding configuration and generation failures."""


class EmbeddingConfigurationError(EmbeddingError):
    """The configured provider or model does not match the approved identity."""


class EmbeddingCompatibilityError(EmbeddingError):
    """An embedding identity is missing or incompatible."""


class EmbeddingVectorError(EmbeddingError, ValueError):
    """A provider vector is not valid under the approved geometry contract."""


@dataclass(frozen=True)
class EmbeddingIdentity:
    provider: str
    model: str
    manifest_digest: str
    dimensions: int
    normalization: str

    @classmethod
    def approved(cls) -> "EmbeddingIdentity":
        return cls(
            provider=APPROVED_EMBEDDING_PROVIDER,
            model=APPROVED_EMBEDDING_MODEL,
            manifest_digest=APPROVED_EMBEDDING_DIGEST,
            dimensions=APPROVED_VECTOR_DIMENSIONS,
            normalization=APPROVED_NORMALIZATION,
        )

    @classmethod
    def from_payload(cls, payload: object) -> "EmbeddingIdentity | None":
        if payload is None:
            return None
        if not isinstance(payload, dict):
            raise EmbeddingCompatibilityError(
                "embedding identity payload must be an object"
            )

        try:
            identity = cls(
                provider=str(payload["provider"]),
                model=str(payload["model"]),
                manifest_digest=str(payload["manifest_digest"]),
                dimensions=int(payload["dimensions"]),
                normalization=str(payload["normalization"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise EmbeddingCompatibilityError(
                "embedding identity payload is incomplete"
            ) from exc

        identity.require_approved()
        return identity

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def compatibility_key(self) -> tuple[str, str, str, int, str]:
        return (
            self.provider,
            self.model,
            self.manifest_digest,
            self.dimensions,
            self.normalization,
        )

    def require_approved(self) -> None:
        if self.compatibility_key != self.approved().compatibility_key:
            raise EmbeddingCompatibilityError(
                "embedding identity does not match the approved contract"
            )


def validate_embedding_vector(
    vector: Sequence[Real],
) -> list[Real]:
    """Validate geometry without changing, normalizing, or fabricating values."""
    if len(vector) != APPROVED_VECTOR_DIMENSIONS:
        raise EmbeddingVectorError(
            f"embedding vector must contain {APPROVED_VECTOR_DIMENSIONS} values"
        )

    validated: list[Real] = []
    for value in vector:
        if isinstance(value, bool) or not isinstance(value, Real):
            raise EmbeddingVectorError(
                "embedding vector values must be numeric"
            )
        if not math.isfinite(float(value)):
            raise EmbeddingVectorError(
                "embedding vector values must be finite"
            )
        validated.append(value)

    if all(value == 0 for value in validated):
        raise EmbeddingVectorError(
            "zero placeholder vectors are not compatible embeddings"
        )

    return validated
