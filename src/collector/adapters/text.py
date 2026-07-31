from ..core.pipeline import ProcessedCollectorRecord
from ..core.pipeline import process_record


def adapt_text_record(
    source_id: str,
    content: str,
    revision: str = "1",
    metadata: dict | None = None,
) -> ProcessedCollectorRecord:
    """
    Convert raw text input into a processed Collector record.

    This adapter delegates normalization, validation,
    provenance, and identity generation to the core pipeline.
    """

    return process_record(
        source_type="text",
        source_id=source_id,
        content=content,
        revision=revision,
        metadata=metadata,
    )