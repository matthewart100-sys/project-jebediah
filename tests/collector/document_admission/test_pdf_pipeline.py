from datetime import datetime, timezone

import pytest

from collector.document_admission.failures import PolicyViolation, ResourceLimitExceeded
from collector.document_admission.pdf_pipeline import (
    InProcessSyntheticWorkerRunner,
    Phase3BPDFPipeline,
)
from collector.document_admission.policies import phase3b_policy_bundle


def test_pdf_pipeline_prefers_native_text_and_tracks_ocr_fallback() -> None:
    pipeline = Phase3BPDFPipeline(
        phase3b_policy_bundle(),
        InProcessSyntheticWorkerRunner(),
    )
    artifact = pipeline.inspect_payload(
        "submission-1",
        "application/pdf",
        b"%PDF-1.7\nSYNTHETIC-OCR[2]:Fallback\n%%EOF\n",
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert artifact.pages[0].method == "ocr"
    assert artifact.pages[-1].text == "Fallback"


def test_pdf_pipeline_rejects_non_pdf_signature() -> None:
    pipeline = Phase3BPDFPipeline(
        phase3b_policy_bundle(),
        InProcessSyntheticWorkerRunner(),
    )
    with pytest.raises(PolicyViolation, match="invalid_pdf_signature"):
        pipeline.inspect_payload(
            "submission-2",
            "application/pdf",
            b"NOT_PDF",
            datetime(2025, 1, 1, tzinfo=timezone.utc),
        )


def test_pdf_pipeline_rejects_payloads_over_limit() -> None:
    policy = phase3b_policy_bundle()
    pipeline = Phase3BPDFPipeline(policy, InProcessSyntheticWorkerRunner())
    with pytest.raises(ResourceLimitExceeded, match="max_pdf_bytes_exceeded"):
        pipeline.inspect_payload(
            "submission-3",
            "application/pdf",
            b"%PDF-" + (b"x" * policy.max_pdf_bytes),
            datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
