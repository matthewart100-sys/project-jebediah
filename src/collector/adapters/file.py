from pathlib import Path

from .text import adapt_text_record
from ..core.pipeline import ProcessedCollectorRecord


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
}


def adapt_file_record(
    source_id: str,
    file_path: str,
    revision: str = "1",
    metadata: dict | None = None,
) -> ProcessedCollectorRecord:
    """
    Convert a supported file into a Collector record.

    File contents are extracted and delegated to the
    text adapter so all ingestion follows the same path.
    """

    path = Path(file_path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {path.suffix}"
        )

    content = path.read_text(
        encoding="utf-8"
    )

    file_metadata = {
        "file_name": path.name,
        "file_extension": path.suffix.lower(),
    }

    if metadata:
        file_metadata.update(metadata)

    return adapt_text_record(
        source_id=source_id,
        content=content,
        revision=revision,
        metadata=file_metadata,
    )