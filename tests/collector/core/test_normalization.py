from collector.core.normalization import (
    normalize_content,
    normalize_metadata,
)


def test_content_normalization_removes_extra_whitespace():
    result = normalize_content(
        "  Project     Jebediah  "
    )

    assert result == "Project Jebediah"


def test_metadata_normalization_sorts_keys():
    result = normalize_metadata(
        {
            "b": "2",
            "a": "1",
        }
    )

    assert list(result.keys()) == [
        "a",
        "b",
    ]