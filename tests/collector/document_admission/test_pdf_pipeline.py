from datetime import datetime, timezone

import pytest

from collector.document_admission.failures import PolicyViolation, ResourceLimitExceeded
from collector.document_admission.pdf_pipeline import Phase3BPDFPipeline
from collector.document_admission.policies import phase3b_policy_bundle


SYNTHETIC_PDF_WITH_NATIVE_TEXT = (
    b"%PDF-1.7\n"
    b"SYNTHETIC-TEXT[1]:Board roster fixture\n"
    b"%%EOF\n"
)
SYNTHETIC_PDF_WITHOUT_NATIVE_TEXT = b"%PDF-1.7\n%%EOF\n"


def test_pdf_pipeline_uses_native_text_only() -> None:
    pipeline = Phase3BPDFPipeline(phase3b_policy_bundle())
    artifact = pipeline.inspect_payload(
        "submission-1",
        "application/pdf",
        SYNTHETIC_PDF_WITH_NATIVE_TEXT,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert artifact.pages[0].method == "native"
    assert artifact.pages[-1].text == "Board roster fixture"
    assert artifact.native_text_sufficient is True


def test_pdf_pipeline_records_placeholder_when_native_text_missing() -> None:
    pipeline = Phase3BPDFPipeline(phase3b_policy_bundle())
    artifact = pipeline.inspect_payload(
        "submission-1",
        "application/pdf",
        SYNTHETIC_PDF_WITHOUT_NATIVE_TEXT,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert artifact.pages[0].text == "native text unavailable in synthetic fixture"
    assert "native_text_unavailable" in artifact.warnings
    assert artifact.native_text_sufficient is False


def test_pdf_pipeline_rejects_non_pdf_signature() -> None:
    pipeline = Phase3BPDFPipeline(phase3b_policy_bundle())
    with pytest.raises(PolicyViolation, match="invalid_pdf_signature"):
        pipeline.inspect_payload(
            "submission-2",
            "application/pdf",
            b"NOT_PDF",
            datetime(2025, 1, 1, tzinfo=timezone.utc),
        )


def test_pdf_pipeline_rejects_payloads_over_limit() -> None:
    policy = phase3b_policy_bundle()
    pipeline = Phase3BPDFPipeline(policy)
    with pytest.raises(ResourceLimitExceeded, match="max_pdf_bytes_exceeded"):
        pipeline.inspect_payload(
            "submission-3",
            "application/pdf",
            b"%PDF-" + (b"x" * policy.max_pdf_bytes),
            datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
