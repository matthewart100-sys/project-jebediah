import pytest

from collector.document_admission.failures import DocumentAdmissionValidationError
from collector.document_admission.worker_protocol import coerce_worker_result


def test_worker_protocol_accepts_strict_payload() -> None:
    result = coerce_worker_result(
        "inspector",
        {
            "status": "reviewable",
            "pages": (
                {"page_number": 1, "method": "native", "text": "Synthetic page"},
            ),
            "warnings": (),
            "findings": (),
            "native_text_sufficient": True,
        },
        created_at=__import__("datetime").datetime(
            2025, 1, 1, tzinfo=__import__("datetime").timezone.utc
        ),
    )
    assert result.pages[0].page_number == 1


def test_worker_protocol_rejects_extra_fields() -> None:
    with pytest.raises(
        DocumentAdmissionValidationError,
        match="invalid_worker_payload_shape",
    ):
        coerce_worker_result(
            "scanner",
            {
                "status": "clean",
                "pages": (),
                "warnings": (),
                "findings": (),
                "native_text_sufficient": False,
                "extra": "denied",
            },
            created_at=__import__("datetime").datetime(
                2025, 1, 1, tzinfo=__import__("datetime").timezone.utc
            ),
        )
