from ..errors import CollectorValidationError


def validate_content(content: str) -> None:
    """
    Validate Collector content requirements.
    """

    if not content or not content.strip():
        raise CollectorValidationError(
            "content cannot be empty"
        )


def validate_source(
    source_type: str,
    source_id: str,
) -> None:
    """
    Validate Collector source identity.
    """

    if not source_type.strip():
        raise CollectorValidationError(
            "source_type cannot be empty"
        )

    if not source_id.strip():
        raise CollectorValidationError(
            "source_id cannot be empty"
        )


def validate_record(
    source_type: str,
    source_id: str,
    content: str,
) -> None:
    """
    Validate core Collector record requirements.
    """

    validate_source(source_type, source_id)
    validate_content(content)