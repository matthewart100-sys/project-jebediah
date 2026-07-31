import hashlib
import json

from .models import CollectorRecord


def generate_revision_id(record: CollectorRecord) -> str:
    """
    Generate deterministic identity for a Collector revision.
    """

    canonical = {
        "source_type": record.source_type,
        "source_id": record.source_id,
        "revision": record.revision,
        "content": record.content,
        "metadata": record.metadata,
    }

    serialized = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()