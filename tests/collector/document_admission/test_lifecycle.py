from datetime import datetime, timedelta, timezone
from pathlib import Path

from collector.document_admission.runtime import SyntheticPhase3BDocumentAdmissionRuntime


def test_recovery_expires_old_submission_and_deletes_payload(tmp_path: Path) -> None:
    current_time = datetime(2025, 1, 1, tzinfo=timezone.utc)

    def clock() -> datetime:
        return current_time

    runtime = SyntheticPhase3BDocumentAdmissionRuntime(
        tmp_path,
        "phase3b-passphrase",
        clock=clock,
    )
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    detail = runtime.admit_signed_pdf(
        runtime.build_demo_receipt(
            receipt_id="lifecycle-receipt",
            expected_payload=payload,
        ),
        "application/pdf",
        payload,
    )
    current_time = current_time + timedelta(days=31)
    report = runtime.recover()
    assert detail.record.submission_id in report.expired_submission_ids
