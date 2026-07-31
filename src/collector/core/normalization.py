from typing import Any


def normalize_content(content: str) -> str:
    """
    Normalize text content into a deterministic representation.
    """

    return " ".join(content.split())


def normalize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize metadata by returning keys in deterministic order.
    """

    return dict(sorted(metadata.items()))