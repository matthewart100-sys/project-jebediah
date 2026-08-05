from datetime import datetime, timezone
from pathlib import Path

from collector.document_admission.runtime import SyntheticPhase3BDocumentAdmissionRuntime
from collector.document_admission.models import ReviewDecision


def test_review_records_prior_annotation_link(tmp_path: Path) -> None:
    runtime = SyntheticPhase3BDocumentAdmissionRuntime(
        tmp_path,
        "phase3b-passphrase",
        clock=lambda: datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    detail = runtime.admit_signed_pdf(
        runtime.build_demo_receipt(
            receipt_id="review-receipt",
            expected_payload=payload,
        ),
        "application/pdf",
        payload,
    )
    first = runtime.review_submission(
        detail.record.submission_id,
        ReviewDecision.CORRECT,
        "Needs correction",
    )
    second = runtime.review_submission(
        detail.record.submission_id,
        ReviewDecision.APPROVE,
        "Correction verified",
    )
    assert first.review_annotations[-1].prior_annotation_id is None
    assert second.review_annotations[-1].prior_annotation_id == first.review_annotations[-1].annotation_id
