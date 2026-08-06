from abc import ABC, abstractmethod
from datetime import datetime

from .models import (
    AdmissionAttemptRecord,
    AdmissionOperationContext,
    AdmissionTransition,
    AuditEvent,
    CleanupEvidence,
    CleanupOperationContext,
    ConsumerEligibilityDecision,
    ContentIdentity,
    FormatDetectionResult,
    InspectionOperationContext,
    InspectionResult,
    IntegrityVerification,
    LegalHoldEvidence,
    PolicyEvaluation,
    QuarantineReceipt,
    RetryEvidence,
    SecurityEvaluation,
    SubmissionEnvelope,
    TransformationAttemptRecord,
    TransformationTransition,
    AuthorizationReceipt,
    ReceiptVerification,
    CustodyObjectRecord,
    CustodyAuditEvent,
    ReconciliationFinding,
)
from .policies import (
    AdmissionPolicies,
    AuthorizationPolicy,
    CustodyPolicy,
    DigestPolicy,
    InspectionPolicy,
    ResourceLimitPolicy,
    RetentionPolicy,
    SyntheticConsumerPolicy,
)


class AuthorizationVerifier(ABC):
    @abstractmethod
    def verify(
        self,
        receipt: AuthorizationReceipt,
        policy: AuthorizationPolicy,
        verification_id: str,
        checked_at: datetime,
    ) -> ReceiptVerification:
        raise NotImplementedError


class ByteIntegrityVerifier(ABC):
    @abstractmethod
    def identify(
        self,
        payload: bytes,
        policy: DigestPolicy,
    ) -> ContentIdentity:
        raise NotImplementedError

    @abstractmethod
    def verify(
        self,
        payload: bytes,
        expected: ContentIdentity,
        verification_id: str,
        checked_at: datetime,
    ) -> IntegrityVerification:
        raise NotImplementedError


class QuarantineRepository(ABC):
    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def open_for_evaluation(
        self,
        receipt: QuarantineReceipt,
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def verify(
        self,
        receipt: QuarantineReceipt,
        verification_id: str,
        checked_at: datetime,
    ) -> IntegrityVerification:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        receipt: QuarantineReceipt,
        policy: RetentionPolicy,
        legal_hold: LegalHoldEvidence | None,
        context: CleanupOperationContext,
    ) -> CleanupEvidence:
        raise NotImplementedError


class EvidenceJournal(ABC):
    @abstractmethod
    def append_admission_transition(
        self,
        transition: AdmissionTransition,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def append_transformation_transition(
        self,
        transition: TransformationTransition,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def append_audit_event(self, event: AuditEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def admission_history(
        self,
        attempt_id: str,
    ) -> tuple[AdmissionTransition, ...]:
        raise NotImplementedError

    @abstractmethod
    def transformation_history(
        self,
        attempt_id: str,
    ) -> tuple[TransformationTransition, ...]:
        raise NotImplementedError


class FormatDetector(ABC):
    @abstractmethod
    def detect(
        self,
        payload: bytes,
        envelope: SubmissionEnvelope,
        admission_attempt_id: str,
        detection_id: str,
        policy: ResourceLimitPolicy,
        checked_at: datetime,
    ) -> FormatDetectionResult:
        raise NotImplementedError


class SecurityEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        payload: bytes,
        envelope: SubmissionEnvelope,
        detected: FormatDetectionResult,
        evaluation_id: str,
        policy: ResourceLimitPolicy,
        checked_at: datetime,
    ) -> SecurityEvaluation:
        raise NotImplementedError


class PolicyEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        envelope: SubmissionEnvelope,
        detected: FormatDetectionResult,
        security: SecurityEvaluation,
        evaluation_id: str,
        consumer: SyntheticConsumerPolicy,
        retention: RetentionPolicy,
        resources: ResourceLimitPolicy,
        checked_at: datetime,
    ) -> PolicyEvaluation:
        raise NotImplementedError


class IsolatedInspector(ABC):
    @abstractmethod
    def inspect(
        self,
        payload: bytes,
        admission: AdmissionAttemptRecord,
        transformation_attempt_id: str,
        inspection_result_id: str,
        policy: InspectionPolicy,
        started_at: datetime,
        completed_at: datetime,
    ) -> InspectionResult:
        raise NotImplementedError


class ConsumerEligibilityEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self,
        result: InspectionResult,
        consumer: SyntheticConsumerPolicy,
        decision_id: str,
        decided_at: datetime,
    ) -> ConsumerEligibilityDecision:
        raise NotImplementedError


class DocumentAdmissionOrchestrator(ABC):
    @abstractmethod
    def submit(
        self,
        envelope: SubmissionEnvelope,
        payload: bytes,
        policies: AdmissionPolicies,
        context: AdmissionOperationContext,
    ) -> AdmissionAttemptRecord:
        raise NotImplementedError

    @abstractmethod
    def inspect(
        self,
        admission: AdmissionAttemptRecord,
        policy: InspectionPolicy,
        consumer: SyntheticConsumerPolicy,
        context: InspectionOperationContext,
    ) -> TransformationAttemptRecord:
        raise NotImplementedError

    @abstractmethod
    def retry_admission(
        self,
        prior: AdmissionAttemptRecord,
        retry: RetryEvidence,
        envelope: SubmissionEnvelope,
        payload: bytes,
        policies: AdmissionPolicies,
        context: AdmissionOperationContext,
    ) -> AdmissionAttemptRecord:
        raise NotImplementedError

    @abstractmethod
    def retry_inspection(
        self,
        admission: AdmissionAttemptRecord,
        prior: TransformationAttemptRecord,
        retry: RetryEvidence,
        policy: InspectionPolicy,
        consumer: SyntheticConsumerPolicy,
        context: InspectionOperationContext,
    ) -> TransformationAttemptRecord:
        raise NotImplementedError

    @abstractmethod
    def cleanup(
        self,
        receipt: QuarantineReceipt,
        policy: RetentionPolicy,
        legal_hold: LegalHoldEvidence | None,
        context: CleanupOperationContext,
    ) -> CleanupEvidence:
        raise NotImplementedError


class DurableObjectCustody(ABC):
    @abstractmethod
    def reserve_receipt(self, receipt_id: str, reserved_at: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def store(
        self,
        object_id: str,
        admission_attempt_id: str,
        receipt_id: str,
        plaintext: bytes,
        policy: CustodyPolicy,
        retention: RetentionPolicy,
        created_at: datetime,
    ) -> CustodyObjectRecord:
        raise NotImplementedError

    @abstractmethod
    def get(self, object_id: str) -> CustodyObjectRecord | None:
        raise NotImplementedError

    @abstractmethod
    def list_active(self) -> tuple[CustodyObjectRecord, ...]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_plaintext(self, object_id: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def tombstone(
        self,
        object_id: str,
        reason_code: str,
        tombstoned_at: datetime,
    ) -> CustodyObjectRecord:
        raise NotImplementedError

    @abstractmethod
    def append_audit_event(
        self,
        event_id: str,
        subject_id: str,
        object_id: str | None,
        event_kind: str,
        reason_code: str,
        recorded_at: datetime,
    ) -> CustodyAuditEvent:
        raise NotImplementedError

    @abstractmethod
    def audit_history(self, subject_id: str) -> tuple[CustodyAuditEvent, ...]:
        raise NotImplementedError


class CustodyReconciler(ABC):
    @abstractmethod
    def reconcile(self, checked_at: datetime) -> tuple[ReconciliationFinding, ...]:
        raise NotImplementedError
