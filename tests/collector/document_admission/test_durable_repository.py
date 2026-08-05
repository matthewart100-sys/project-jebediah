from datetime import datetime, timezone
from pathlib import Path

from collector.document_admission.authorization import sign_receipt, synthetic_signing_key
from collector.document_admission.durable_repository import Phase3BDurableRepository
from collector.document_admission.models import (
    ExtractionQuality,
    Phase3BInspectionArtifact,
    Phase3BPageCapture,
    ReviewDecision,
    SourceAuthorizationReceipt,
)


def _signed_receipt(receipt_id: str):
    key = synthetic_signing_key()
    receipt = SourceAuthorizationReceipt(
        receipt_id=receipt_id,
        organization_id="synthetic-org",
        source_record_id="synthetic-source",
        authority_role="synthetic-authority",
        principal_id="synthetic-principal",
        purpose="phase3b_test",
        classification="internal-governance-limited-personal-data",
        allowed_operation="phase3b.synthetic.intake",
        retention_profile_id="phase3b",
        environment="synthetic-local-only",
        issued_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        expires_at=datetime(2025, 1, 2, tzinfo=timezone.utc),
        signer_key_id="synthetic-phase3b-signer",
        expected_sha256=None,
        single_use=True,
    )
    return sign_receipt(receipt, key)


def _artifact(submission_id: str) -> Phase3BInspectionArtifact:
    return Phase3BInspectionArtifact(
        artifact_id=f"artifact-{submission_id}",
        submission_id=submission_id,
        extraction_quality=ExtractionQuality.COMPLETE,
        pages=(
            Phase3BPageCapture(
                page_number=1,
                method="native",
                text="Synthetic page",
                warnings=(),
                limitations=(),
            ),
        ),
        warnings=(),
        omissions=("phase3c_consumer_absent",),
        limitations=("Synthetic only.",),
        native_text_sufficient=True,
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )


def test_repository_admits_duplicate_and_persists_detail(tmp_path: Path) -> None:
    repository = Phase3BDurableRepository(tmp_path, "phase3b-passphrase")
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    first = repository.admit(
        _signed_receipt("receipt-1"),
        "application/pdf",
        payload,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    repository.store_inspection(
        first.submission_id,
        _artifact(first.submission_id),
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    second = repository.admit(
        _signed_receipt("receipt-2"),
        "application/pdf",
        payload,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert second.duplicate_of == first.submission_id
    detail = repository.submission_detail(first.submission_id)
    assert detail.inspection_artifact is not None
    annotation = repository.append_review(
        first.submission_id,
        ReviewDecision.APPROVE,
        "Looks good",
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    assert annotation.decision is ReviewDecision.APPROVE


def test_repository_recovery_marks_missing_object_cleanup_failed(tmp_path: Path) -> None:
    repository = Phase3BDurableRepository(tmp_path, "phase3b-passphrase")
    payload = b"%PDF-1.7\nSYNTHETIC-TEXT[1]:Hello\n%%EOF\n"
    record = repository.admit(
        _signed_receipt("receipt-3"),
        "application/pdf",
        payload,
        datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    object_path = tmp_path / "objects" / "object-receipt-3.json"
    object_path.unlink()
    report = repository.recover(datetime(2025, 1, 1, tzinfo=timezone.utc))
    assert record.submission_id in report.cleanup_failed_submission_ids
