from datetime import datetime, timezone

from pydantic import BaseModel

from ..identity import generate_revision_id
from ..models import CollectorRecord
from .normalization import (
    normalize_content,
    normalize_metadata,
)
from .provenance import CollectorProvenance
from .validation import validate_record


class ProcessedCollectorRecord(BaseModel):
    record: CollectorRecord
    provenance: CollectorProvenance
    identity: str


def process_record(
    source_type: str,
    source_id: str,
    content: str,
    revision: str,
    metadata: dict | None = None,
) -> ProcessedCollectorRecord:

    metadata = metadata or {}

    normalized_content = normalize_content(content)
    normalized_metadata = normalize_metadata(metadata)

    validate_record(
        source_type,
        source_id,
        normalized_content,
    )

    record = CollectorRecord(
        source_type=source_type,
        source_id=source_id,
        content=normalized_content,
        observed_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc),
        revision=revision,
        metadata=normalized_metadata,
    )

    provenance = CollectorProvenance(
        source_type=source_type,
        source_id=source_id,
    )

    identity = generate_revision_id(record)

    return ProcessedCollectorRecord(
        record=record,
        provenance=provenance,
        identity=identity,
    )