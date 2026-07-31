from dataclasses import dataclass

from ..identity import generate_revision_id
from ..models import CollectorRecord
from .decisions import StorageDecision


@dataclass(frozen=True)
class StoragePolicyResult:
    decision: StorageDecision
    reason: str


class StoragePolicy:
    """
    Determines what should happen to an incoming CollectorRecord.

    This layer remains independent from:
    - Qdrant
    - databases
    - APIs
    - n8n
    - Ollama
    """

    def evaluate(
        self,
        incoming: CollectorRecord,
        existing: CollectorRecord | None = None,
    ) -> StoragePolicyResult:

        if existing is None:
            return StoragePolicyResult(
                decision=StorageDecision.ACCEPT,
                reason="no existing record found",
            )

        incoming_identity = generate_revision_id(incoming)
        existing_identity = generate_revision_id(existing)

        if incoming_identity == existing_identity:
            return StoragePolicyResult(
                decision=StorageDecision.DUPLICATE,
                reason="record identity already exists",
            )

        if incoming.source_id == existing.source_id:
            if incoming.revision > existing.revision:
                return StoragePolicyResult(
                    decision=StorageDecision.UPDATE,
                    reason="newer revision detected",
                )

            return StoragePolicyResult(
                decision=StorageDecision.REVIEW,
                reason="conflicting record revision",
            )

        return StoragePolicyResult(
            decision=StorageDecision.ACCEPT,
            reason="new independent record",
        )