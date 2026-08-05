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
    Phase3BInspectionArtifact,
    Phase3BRecoveryReport,
    Phase3BReviewAnnotation,
    Phase3BSubmissionDetail,
    Phase3BSubmissionRecord,
    Phase3BWorkspaceSnapshot,
    SignedSourceAuthorizationReceipt,
    ReviewDecision,
)
from .policies import (
    AdmissionPolicies,
    DigestPolicy,
    InspectionPolicy,
    ResourceLimitPolicy,
    RetentionPolicy,
    SyntheticConsumerPolicy,
)


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


class SourceAuthorizationVerifier(ABC):
    @abstractmethod
    def verify(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        checked_at: datetime,
    ) -> SignedSourceAuthorizationReceipt:
        raise NotImplementedError


class DurableCustodyRepository(ABC):
    @abstractmethod
    def admit(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        media_type: str,
        payload: bytes,
        admitted_at: datetime,
    ) -> Phase3BSubmissionRecord:
        raise NotImplementedError

    @abstractmethod
    def store_inspection(
        self,
        submission_id: str,
        artifact: Phase3BInspectionArtifact,
        stored_at: datetime,
    ) -> Phase3BSubmissionRecord:
        raise NotImplementedError

    @abstractmethod
    def append_review(
        self,
        submission_id: str,
        decision: ReviewDecision,
        note: str,
        reviewed_at: datetime,
    ) -> Phase3BReviewAnnotation:
        raise NotImplementedError

    @abstractmethod
    def delete_submission(
        self,
        submission_id: str,
        deleted_at: datetime,
        reason_code: str,
    ) -> Phase3BSubmissionRecord:
        raise NotImplementedError

    @abstractmethod
    def workspace_snapshot(
        self,
        generated_at: datetime,
    ) -> Phase3BWorkspaceSnapshot:
        raise NotImplementedError

    @abstractmethod
    def submission_detail(self, submission_id: str) -> Phase3BSubmissionDetail:
        raise NotImplementedError

    @abstractmethod
    def recover(self, recovered_at: datetime) -> Phase3BRecoveryReport:
        raise NotImplementedError


class Phase3BDocumentAdmissionRuntime(ABC):
    @abstractmethod
    def admit_signed_pdf(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        media_type: str,
        payload: bytes,
    ) -> Phase3BSubmissionDetail:
        raise NotImplementedError

    @abstractmethod
    def review_submission(
        self,
        submission_id: str,
        decision: ReviewDecision,
        note: str,
    ) -> Phase3BSubmissionDetail:
        raise NotImplementedError

    @abstractmethod
    def delete_submission(self, submission_id: str) -> Phase3BSubmissionDetail:
        raise NotImplementedError

    @abstractmethod
    def workspace_snapshot(self) -> Phase3BWorkspaceSnapshot:
        raise NotImplementedError
