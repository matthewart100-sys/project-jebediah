from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .authorization import SyntheticReceiptVerifier, sign_receipt, synthetic_signing_key
from .durable_repository import Phase3BDurableRepository
from .interfaces import Phase3BDocumentAdmissionRuntime
from .lifecycle import Phase3BLifecycleService
from .models import (
    Phase3BRecoveryReport,
    Phase3BSubmissionDetail,
    Phase3BWorkspaceSnapshot,
    ReviewDecision,
    SignedSourceAuthorizationReceipt,
    SourceAuthorizationReceipt,
)
from .pdf_pipeline import Phase3BPDFPipeline
from .policies import phase3b_policy_bundle
from .review import Phase3BReviewService


class SyntheticPhase3BDocumentAdmissionRuntime(Phase3BDocumentAdmissionRuntime):
    def __init__(
        self,
        root_dir: str | Path,
        passphrase: str,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._policy = phase3b_policy_bundle()
        signing_key = synthetic_signing_key()
        self._signing_key = signing_key
        self._public_keys: dict[str, Ed25519PublicKey] = {
            "synthetic-phase3b-signer": signing_key.public_key()
        }
        self._verifier = SyntheticReceiptVerifier(self._public_keys)
        self._repository = Phase3BDurableRepository(root_dir, passphrase)
        self._pipeline = Phase3BPDFPipeline(self._policy)
        self._review = Phase3BReviewService(self._repository)
        self._lifecycle = Phase3BLifecycleService(self._repository)

    def build_demo_receipt(
        self,
        *,
        receipt_id: str,
        expected_payload: bytes | None = None,
    ) -> SignedSourceAuthorizationReceipt:
        now = self._clock()
        expected_sha256 = None
        if expected_payload is not None:
            from .crypto import hash_content_identity

            expected_sha256 = hash_content_identity(expected_payload).digest_hex
        receipt = SourceAuthorizationReceipt(
            receipt_id=receipt_id,
            organization_id="synthetic-phase3b-authority",
            source_record_id="synthetic-phase3b-source-record",
            authority_role="synthetic-phase3b-authority-role",
            principal_id="synthetic_phase3b_operator",
            purpose="phase3b_synthetic_intake_validation",
            classification="internal-governance-limited-personal-data",
            allowed_operation="phase3b.synthetic.intake",
            retention_profile_id=self._policy.policy_id,
            environment="synthetic-local-only",
            issued_at=now,
            expires_at=now + timedelta(hours=1),
            signer_key_id="synthetic-phase3b-signer",
            expected_sha256=expected_sha256,
            single_use=True,
        )
        return sign_receipt(receipt, self._signing_key)

    def admit_signed_pdf(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        media_type: str,
        payload: bytes,
    ) -> Phase3BSubmissionDetail:
        checked_at = self._clock()
        verified = self._verifier.verify(signed_receipt, checked_at)
        record = self._repository.admit(
            verified,
            media_type,
            payload,
            checked_at,
        )
        artifact = self._pipeline.inspect_payload(
            record.submission_id,
            media_type,
            payload,
            checked_at,
        )
        self._repository.store_inspection(record.submission_id, artifact, checked_at)
        return self._repository.submission_detail(record.submission_id)

    def review_submission(
        self,
        submission_id: str,
        decision: ReviewDecision,
        note: str,
    ) -> Phase3BSubmissionDetail:
        return self._review.apply(
            submission_id,
            decision,
            note,
            self._clock(),
        )

    def delete_submission(self, submission_id: str) -> Phase3BSubmissionDetail:
        return self._lifecycle.delete(
            submission_id,
            self._clock(),
            reason_code="operator_deleted_submission",
        )

    def workspace_snapshot(self) -> Phase3BWorkspaceSnapshot:
        return self._repository.workspace_snapshot(self._clock())

    def submission_detail(self, submission_id: str) -> Phase3BSubmissionDetail:
        return self._repository.submission_detail(submission_id)

    def recover(self) -> Phase3BRecoveryReport:
        return self._lifecycle.recover(self._clock())
