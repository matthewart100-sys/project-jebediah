from datetime import datetime, timezone

from pydantic import BaseModel, Field


class CollectorProvenance(BaseModel):
    """
    Tracks the origin of collected information.
    """

    source_type: str = Field(min_length=1)
    source_id: str = Field(min_length=1)

    collector_version: str = "1.0"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )