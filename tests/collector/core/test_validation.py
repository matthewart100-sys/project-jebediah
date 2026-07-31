import pytest

from collector.core.validation import (
    validate_content,
    validate_source,
)
from collector.errors import CollectorValidationError


def test_valid_content_passes():
    validate_content(
        "valid content"
    )


def test_empty_content_fails():
    with pytest.raises(CollectorValidationError):
        validate_content("")


def test_empty_source_fails():
    with pytest.raises(CollectorValidationError):
        validate_source(
            "",
            "source-id",
        )