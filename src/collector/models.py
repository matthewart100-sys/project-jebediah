from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class CollectorRecord(BaseModel):
    """
    Canonical Collector 1.0 input record.
    """

    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    content: str = Field(min_length=1)

    observed_at: datetime
    submitted_at: datetime

    revision: str = Field(min_length=1)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("content cannot be empty")

        return cleaned