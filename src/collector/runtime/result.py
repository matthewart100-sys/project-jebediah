from pydantic import BaseModel, field_validator

from ..models import CollectorRecord
from ..policy.decisions import StorageDecision
from ..policy.storage_policy import StoragePolicyResult


class CollectorResult(BaseModel):
    record: CollectorRecord
    decision: StoragePolicyResult
    stored: bool

    @field_validator("decision", mode="before")
    @classmethod
    def normalize_decision(cls, value):

        if isinstance(value, StoragePolicyResult):
            return value

        if isinstance(value, StorageDecision):
            return StoragePolicyResult(
                decision=value,
                reason=value.reason,
            )

        return value