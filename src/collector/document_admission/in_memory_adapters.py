import hashlib
from datetime import datetime

from .failures import (
    DocumentAdmissionConflict,
    DocumentAdmissionNotFound,
    DocumentAdmissionValidationError,
    PolicyViolation,
    QuarantineFailure,
)
from .interfaces import (
    ByteIntegrityVerifier,
    EvidenceJournal,
    QuarantineRepository,
)
from .models import (
    AdmissionTransition,
    AuditEvent,
    CleanupEvidence,
    CleanupOperationContext,
    CleanupOutcome,
    ContentIdentity,
    IntegrityVerification,
    LegalHoldEvidence,
    QuarantineReceipt,
    SubmissionEnvelope,
    TransformationTransition,
)
from .policies import DigestPolicy, RetentionPolicy


def _require_bytes(payload: bytes) -> None:
    if not isinstance(payload, bytes):
        raise DocumentAdmissionValidationError("invalid_payload_type")


def _require_identifier(value: str, reason_code: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise DocumentAdmissionValidationError(reason_code)


class Sha256ByteIntegrityVerifier(ByteIntegrityVerifier):
    """Synthetic SHA-256 identity implementation with no persistence."""

    verifier_id = "synthetic-sha256-verifier"
    verifier_version = "1"

    def identify(
        self,
        payload: bytes,
        policy: DigestPolicy,
    ) -> ContentIdentity:
        _require_bytes(payload)
        if not isinstance(policy, DigestPolicy):
            raise DocumentAdmissionValidationError(
                "invalid_digest_policy"
            )
        return ContentIdentity(
            digest_policy_id=policy.policy_id,
            digest_policy_version=policy.policy_version,
            algorithm=policy.algorithm,
            digest_hex=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
        )

    def verify(
        self,
        payload: bytes,
        expected: ContentIdentity,
        verification_id: str,
        checked_at: datetime,
    ) -> IntegrityVerification:
        _require_bytes(payload)
        if not isinstance(expected, ContentIdentity):
            raise DocumentAdmissionValidationError(
                "invalid_expected_identity"
            )
        _require_identifier(
            verification_id,
            "invalid_verification_id",
        )
        observed = self.identify(
            payload,
            DigestPolicy(
                expected.digest_policy_id,
                expected.digest_policy_version,
                expected.algorithm,
            ),
        )
        return IntegrityVerification(
            verification_id=verification_id,
            quarantine_id="synthetic-unbound-quarantine",
            expected=expected,
            observed=observed,
            verifier_id=self.verifier_id,
            verifier_version=self.verifier_version,
            checked_at=checked_at,
            matches=observed == expected,
        )


class InMemoryQuarantineRepository(QuarantineRepository):
    """Process-local synthetic byte custody with no ordinary read surface."""

    adapter_id = "synthetic-in-memory-quarantine"
    adapter_version = "1"

    def __init__(self, verifier: ByteIntegrityVerifier) -> None:
        if not isinstance(verifier, ByteIntegrityVerifier):
            raise DocumentAdmissionValidationError(
                "invalid_integrity_verifier"
            )
        self._verifier = verifier
        self._payloads: dict[str, bytes] = {}
        self._receipts: dict[str, QuarantineReceipt] = {}
        self._deleted_receipts: dict[str, QuarantineReceipt] = {}
        self._cleanup: dict[str, CleanupEvidence] = {}

    def place(
        self,
        envelope: SubmissionEnvelope,
        admission_attempt_id: str,
        quarantine_id: str,
        integrity_evidence_id: str,
        payload: bytes,
        identity: ContentIdentity,
        placed_at: datetime,
    ) -> QuarantineReceipt:
        if not isinstance(envelope, SubmissionEnvelope):
            raise DocumentAdmissionValidationError("invalid_envelope")
        for value, reason in (
            (admission_attempt_id, "invalid_admission_attempt_id"),
            (quarantine_id, "invalid_quarantine_id"),
            (integrity_evidence_id, "invalid_integrity_evidence_id"),
        ):
            _require_identifier(value, reason)
        _require_bytes(payload)
        if not isinstance(identity, ContentIdentity):
            raise DocumentAdmissionValidationError(
                "invalid_content_identity"
            )
        if quarantine_id in self._deleted_receipts:
            raise DocumentAdmissionConflict(
                "quarantine_identity_conflict",
                quarantine_id,
            )

        observed = self._verifier.identify(
            payload,
            DigestPolicy(
                identity.digest_policy_id,
                identity.digest_policy_version,
                identity.algorithm,
            ),
        )
        if observed != identity:
            raise QuarantineFailure(
                "integrity_mismatch",
                quarantine_id,
            )

        receipt = QuarantineReceipt(
            quarantine_id=quarantine_id,
            submission_id=envelope.submission_id,
            admission_attempt_id=admission_attempt_id,
            content_identity=identity,
            adapter_id=self.adapter_id,
            adapter_version=self.adapter_version,
            placed_at=placed_at,
            integrity_evidence_id=integrity_evidence_id,
        )
        existing = self._receipts.get(quarantine_id)
        if existing is not None:
            if existing == receipt and self._payloads[quarantine_id] == payload:
                return existing
            raise DocumentAdmissionConflict(
                "quarantine_identity_conflict",
                quarantine_id,
            )

        self._receipts[quarantine_id] = receipt
        self._payloads[quarantine_id] = bytes(payload)
        return receipt

    def open_for_evaluation(
        self,
        receipt: QuarantineReceipt,
    ) -> bytes:
        stored_receipt = self._stored_receipt(receipt)
        return bytes(self._payloads[stored_receipt.quarantine_id])

    def verify(
        self,
        receipt: QuarantineReceipt,
        verification_id: str,
        checked_at: datetime,
    ) -> IntegrityVerification:
        stored_receipt = self._stored_receipt(receipt)
        verification = self._verifier.verify(
            self._payloads[stored_receipt.quarantine_id],
            stored_receipt.content_identity,
            verification_id,
            checked_at,
        )
        return IntegrityVerification(
            verification_id=verification.verification_id,
            quarantine_id=stored_receipt.quarantine_id,
            expected=verification.expected,
            observed=verification.observed,
            verifier_id=verification.verifier_id,
            verifier_version=verification.verifier_version,
            checked_at=verification.checked_at,
            matches=verification.matches,
        )

    def delete(
        self,
        receipt: QuarantineReceipt,
        policy: RetentionPolicy,
        legal_hold: LegalHoldEvidence | None,
        context: CleanupOperationContext,
    ) -> CleanupEvidence:
        if not isinstance(receipt, QuarantineReceipt):
            raise DocumentAdmissionValidationError(
                "invalid_quarantine_receipt"
            )
        if not isinstance(policy, RetentionPolicy):
            raise DocumentAdmissionValidationError(
                "invalid_retention_policy"
            )
        if not isinstance(context, CleanupOperationContext):
            raise DocumentAdmissionValidationError(
                "invalid_cleanup_context"
            )

        existing = self._cleanup.get(context.cleanup_id)
        if existing is not None:
            known_receipt = self._receipts.get(
                receipt.quarantine_id
            ) or self._deleted_receipts.get(receipt.quarantine_id)
            if known_receipt != receipt:
                raise DocumentAdmissionConflict(
                    "quarantine_receipt_conflict",
                    receipt.quarantine_id,
                )
            evidence = self._build_cleanup_evidence(
                receipt,
                policy,
                legal_hold,
                context,
            )
            if existing == evidence:
                return existing
            raise DocumentAdmissionConflict(
                "cleanup_identity_conflict",
                context.cleanup_id,
            )

        stored_receipt = self._stored_receipt(receipt)
        evidence = self._build_cleanup_evidence(
            stored_receipt,
            policy,
            legal_hold,
            context,
        )
        self._cleanup[context.cleanup_id] = evidence

        if evidence.outcome is CleanupOutcome.DELETED:
            del self._payloads[stored_receipt.quarantine_id]
            del self._receipts[stored_receipt.quarantine_id]
            self._deleted_receipts[
                stored_receipt.quarantine_id
            ] = stored_receipt
        return evidence

    def _build_cleanup_evidence(
        self,
        receipt: QuarantineReceipt,
        policy: RetentionPolicy,
        legal_hold: LegalHoldEvidence | None,
        context: CleanupOperationContext,
    ) -> CleanupEvidence:
        if legal_hold is not None:
            if not isinstance(legal_hold, LegalHoldEvidence):
                raise DocumentAdmissionValidationError(
                    "invalid_legal_hold"
                )
            if (
                not policy.legal_hold_enabled
                or legal_hold.quarantine_id != receipt.quarantine_id
                or legal_hold.retention_policy_id != policy.policy_id
                or legal_hold.retention_policy_version
                != policy.policy_version
                or legal_hold.effective_at > context.requested_at
                or (
                    legal_hold.expires_at is not None
                    and legal_hold.expires_at <= context.requested_at
                )
            ):
                raise PolicyViolation(
                    "invalid_legal_hold",
                    receipt.quarantine_id,
                )
            outcome = CleanupOutcome.LEGAL_HOLD
            reason_code = "synthetic_legal_hold"
        else:
            outcome = CleanupOutcome.DELETED
            reason_code = "synthetic_cleanup_completed"

        return CleanupEvidence(
            cleanup_id=context.cleanup_id,
            quarantine_id=receipt.quarantine_id,
            retention_policy_id=policy.policy_id,
            retention_policy_version=policy.policy_version,
            deletion_policy_id=policy.deletion_policy_id,
            deletion_policy_version=policy.deletion_policy_version,
            admission_attempt_id=receipt.admission_attempt_id,
            outcome=outcome,
            scope="synthetic_quarantine_payload",
            actor_id="synthetic_cleanup_actor",
            component_id="collector.document_admission",
            reason_code=reason_code,
            requested_at=context.requested_at,
            completed_at=context.completed_at,
            unresolved_obligation_reference=None,
        )

    def _stored_receipt(
        self,
        receipt: QuarantineReceipt,
    ) -> QuarantineReceipt:
        if not isinstance(receipt, QuarantineReceipt):
            raise DocumentAdmissionValidationError(
                "invalid_quarantine_receipt"
            )
        stored = self._receipts.get(receipt.quarantine_id)
        if stored is None:
            raise DocumentAdmissionNotFound(
                "quarantine_not_found",
                receipt.quarantine_id,
            )
        if stored != receipt:
            raise DocumentAdmissionConflict(
                "quarantine_receipt_conflict",
                receipt.quarantine_id,
            )
        return stored


class InMemoryEvidenceJournal(EvidenceJournal):
    """Append-only process-local transition and audit evidence."""

    def __init__(self) -> None:
        self._admission: dict[str, AdmissionTransition] = {}
        self._transformation: dict[str, TransformationTransition] = {}
        self._audit: dict[str, AuditEvent] = {}
        self._admission_attempts: dict[str, list[AdmissionTransition]] = {}
        self._transformation_attempts: dict[
            str,
            list[TransformationTransition],
        ] = {}

    def append_admission_transition(
        self,
        transition: AdmissionTransition,
    ) -> None:
        if not isinstance(transition, AdmissionTransition):
            raise DocumentAdmissionValidationError(
                "invalid_admission_transition"
            )
        if self._append(
            self._admission,
            transition.transition_id,
            transition,
        ):
            self._admission_attempts.setdefault(
                transition.admission_attempt_id,
                [],
            ).append(transition)

    def append_transformation_transition(
        self,
        transition: TransformationTransition,
    ) -> None:
        if not isinstance(transition, TransformationTransition):
            raise DocumentAdmissionValidationError(
                "invalid_transformation_transition"
            )
        if self._append(
            self._transformation,
            transition.transition_id,
            transition,
        ):
            self._transformation_attempts.setdefault(
                transition.transformation_attempt_id,
                [],
            ).append(transition)

    def append_audit_event(self, event: AuditEvent) -> None:
        if not isinstance(event, AuditEvent):
            raise DocumentAdmissionValidationError("invalid_audit_event")
        self._append(self._audit, event.event_id, event)

    def admission_history(
        self,
        attempt_id: str,
    ) -> tuple[AdmissionTransition, ...]:
        _require_identifier(attempt_id, "invalid_admission_attempt_id")
        history = self._admission_attempts.get(attempt_id)
        if history is None:
            raise DocumentAdmissionNotFound(
                "admission_history_not_found",
                attempt_id,
            )
        return tuple(history)

    def transformation_history(
        self,
        attempt_id: str,
    ) -> tuple[TransformationTransition, ...]:
        _require_identifier(
            attempt_id,
            "invalid_transformation_attempt_id",
        )
        history = self._transformation_attempts.get(attempt_id)
        if history is None:
            raise DocumentAdmissionNotFound(
                "transformation_history_not_found",
                attempt_id,
            )
        return tuple(history)

    @staticmethod
    def _append(
        records: dict[str, object],
        identity: str,
        record: object,
    ) -> bool:
        existing = records.get(identity)
        if existing is None:
            records[identity] = record
            return True
        if existing != record:
            raise DocumentAdmissionConflict(
                "evidence_identity_conflict",
                identity,
            )
        return False
