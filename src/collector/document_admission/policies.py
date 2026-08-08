from dataclasses import dataclass, fields
from datetime import datetime

from .models import (
    DocumentFormat,
    RESOURCE_LIMIT_FIELDS,
    RetentionDisposition,
    SubmissionEnvelope,
    _invalid,
    _normalize_tuple,
    _require_aware,
    _require_instance,
    _require_non_empty,
    _require_positive,
)


SYNTHETIC_FORMATS = (
    DocumentFormat.PDF,
    DocumentFormat.DOCX,
    DocumentFormat.XLSX,
    DocumentFormat.PPTX,
    DocumentFormat.CSV,
    DocumentFormat.TXT,
    DocumentFormat.MARKDOWN,
)
SYNTHETIC_REQUIRED_OUTPUTS = ("synthetic_inspection_evidence",)
SYNTHETIC_RESOURCE_LIMITS = {
    "max_input_bytes": 65_536,
    "max_result_bytes": 131_072,
    "max_temporary_bytes": 262_144,
    "max_wall_clock_milliseconds": 1_000,
    "max_cpu_milliseconds": 1_000,
    "max_process_memory_bytes": 16_777_216,
    "max_warning_count": 16,
    "max_finding_count": 32,
    "max_decoded_characters": 32_768,
    "max_text_lines": 1_000,
    "max_text_line_length": 4_096,
    "max_links_or_directives": 64,
    "max_pdf_pages": 8,
    "max_pdf_objects": 512,
    "max_pdf_object_depth": 16,
    "max_pdf_stream_bytes": 65_536,
    "max_pdf_embedded_objects": 0,
    "max_pdf_fonts": 16,
    "max_pdf_extracted_characters": 32_768,
    "max_docx_archive_entries": 128,
    "max_docx_expanded_bytes": 262_144,
    "max_docx_per_entry_bytes": 65_536,
    "max_docx_compression_ratio": 20,
    "max_docx_relationships": 128,
    "max_docx_xml_depth": 32,
    "max_docx_extracted_characters": 32_768,
}


@dataclass(frozen=True)
class AuthorizationPolicy:
    policy_id: str
    policy_version: str
    required_purpose: str
    required_classification: str
    required_operation: str
    trusted_signer_key_ids: tuple[str, ...]
    max_receipt_lifetime_seconds: int
    requires_single_use: bool

    def __post_init__(self) -> None:
        expected = {
            "policy_id": "synthetic-authorization-policy",
            "policy_version": "1",
            "required_purpose": "synthetic_document_admission",
            "required_classification": "synthetic_non_sensitive",
            "required_operation": "admit_synthetic_document",
        }
        for name, value in expected.items():
            if getattr(self, name) != value:
                raise _invalid(name)
        signer_ids = _normalize_tuple(
            self.trusted_signer_key_ids,
            "trusted_signer_key_ids",
            required=True,
        )
        if not all(
            isinstance(signer_id, str) and signer_id.strip()
            for signer_id in signer_ids
        ):
            raise _invalid("trusted_signer_key_ids")
        object.__setattr__(self, "trusted_signer_key_ids", signer_ids)
        _require_positive(
            self.max_receipt_lifetime_seconds,
            "max_receipt_lifetime_seconds",
        )
        if self.requires_single_use is not True:
            raise _invalid("requires_single_use")


@dataclass(frozen=True)
class CustodyPolicy:
    policy_id: str
    policy_version: str
    encryption_algorithm: str
    header_version: int
    key_derivation_id: str
    required_object_kind: str
    requires_authenticated_encryption: bool
    allows_plaintext_persistence: bool
    max_ciphertext_expansion_bytes: int

    def __post_init__(self) -> None:
        expected_strings = {
            "policy_id": "synthetic-custody-policy",
            "policy_version": "1",
            "encryption_algorithm": "synthetic-xor-stream-v1",
            "key_derivation_id": "synthetic-hkdf-sha256-v1",
            "required_object_kind": "source",
        }
        for name, value in expected_strings.items():
            if getattr(self, name) != value:
                raise _invalid(name)
        _require_positive(self.header_version, "header_version")
        _require_non_empty(self.required_object_kind, "required_object_kind")
        if self.requires_authenticated_encryption is not True:
            raise _invalid("requires_authenticated_encryption")
        if self.allows_plaintext_persistence is not False:
            raise _invalid("allows_plaintext_persistence")
        _require_positive(
            self.max_ciphertext_expansion_bytes,
            "max_ciphertext_expansion_bytes",
        )


@dataclass(frozen=True)
class DigestPolicy:
    policy_id: str
    policy_version: str
    algorithm: str

    def __post_init__(self) -> None:
        for name in ("policy_id", "policy_version", "algorithm"):
            _require_non_empty(getattr(self, name), name)
        if (
            self.policy_id != "synthetic-sha256"
            or self.policy_version != "1"
            or self.algorithm != "sha256"
        ):
            raise _invalid("digest_policy")


@dataclass(frozen=True)
class SyntheticConsumerPolicy:
    consumer_id: str
    policy_id: str
    policy_version: str
    intended_use: str
    classification: str
    permitted_formats: tuple[DocumentFormat, ...]
    required_output_kinds: tuple[str, ...]
    effective_at: datetime
    expires_at: datetime
    runtime_access_allowed: bool
    api_access_allowed: bool
    registry_access_allowed: bool
    memory_access_allowed: bool
    retrieval_access_allowed: bool
    model_access_allowed: bool
    interface_access_allowed: bool
    real_information_access_allowed: bool

    def __post_init__(self) -> None:
        exact = {
            "consumer_id": "synthetic_validation_consumer",
            "policy_id": "synthetic-consumer-policy",
            "policy_version": "1",
            "intended_use": "synthetic_contract_validation",
            "classification": "synthetic_non_sensitive",
        }
        for name, expected in exact.items():
            if getattr(self, name) != expected:
                raise _invalid(name)
        formats = _normalize_tuple(
            self.permitted_formats,
            "permitted_formats",
            required=True,
        )
        if formats != SYNTHETIC_FORMATS:
            raise _invalid("permitted_formats")
        object.__setattr__(self, "permitted_formats", formats)
        outputs = tuple(self.required_output_kinds)
        if outputs != SYNTHETIC_REQUIRED_OUTPUTS:
            raise _invalid("required_output_kinds")
        object.__setattr__(self, "required_output_kinds", outputs)
        _require_aware(self.effective_at, "effective_at")
        _require_aware(self.expires_at, "expires_at")
        if self.expires_at <= self.effective_at:
            raise _invalid("expires_at")
        for name in (
            "runtime_access_allowed",
            "api_access_allowed",
            "registry_access_allowed",
            "memory_access_allowed",
            "retrieval_access_allowed",
            "model_access_allowed",
            "interface_access_allowed",
            "real_information_access_allowed",
        ):
            if getattr(self, name) is not False:
                raise _invalid(name)


@dataclass(frozen=True)
class RetentionPolicy:
    policy_id: str
    policy_version: str
    deletion_policy_id: str
    deletion_policy_version: str
    temporary_retention_seconds: int
    held_retention_seconds: int
    received_disposition: RetentionDisposition
    quarantined_disposition: RetentionDisposition
    validating_disposition: RetentionDisposition
    accepted_disposition: RetentionDisposition
    rejected_disposition: RetentionDisposition
    held_disposition: RetentionDisposition
    evaluation_failed_disposition: RetentionDisposition
    ready_output_disposition: RetentionDisposition
    processing_failed_output_disposition: RetentionDisposition
    legal_hold_enabled: bool
    cleanup_required: bool
    accountable_owner_role: str
    custody_role: str

    def __post_init__(self) -> None:
        exact_strings = {
            "policy_id": "synthetic-retention-policy",
            "policy_version": "1",
            "deletion_policy_id": "synthetic-deletion-policy",
            "deletion_policy_version": "1",
            "accountable_owner_role": "Codex - Implementation Engineer",
            "custody_role": "Codex - Implementation Engineer",
        }
        for name, expected in exact_strings.items():
            if getattr(self, name) != expected:
                raise _invalid(name)
        if (
            self.temporary_retention_seconds != 60
            or self.held_retention_seconds != 300
        ):
            raise _invalid("retention_seconds")
        expected_dispositions = {
            "received_disposition": RetentionDisposition.RETAIN_TEMPORARILY,
            "quarantined_disposition": RetentionDisposition.RETAIN_TEMPORARILY,
            "validating_disposition": RetentionDisposition.RETAIN_TEMPORARILY,
            "accepted_disposition": RetentionDisposition.DELETE,
            "rejected_disposition": RetentionDisposition.DELETE,
            "held_disposition": RetentionDisposition.RETAIN_TEMPORARILY,
            "evaluation_failed_disposition": RetentionDisposition.RETAIN_TEMPORARILY,
            "ready_output_disposition": RetentionDisposition.DELETE,
            "processing_failed_output_disposition": RetentionDisposition.DELETE,
        }
        for name, expected in expected_dispositions.items():
            if getattr(self, name) is not expected:
                raise _invalid(name)
        if self.legal_hold_enabled is not True:
            raise _invalid("legal_hold_enabled")
        if self.cleanup_required is not True:
            raise _invalid("cleanup_required")


@dataclass(frozen=True)
class ResourceLimitPolicy:
    policy_id: str
    policy_version: str
    max_input_bytes: int
    max_result_bytes: int
    max_temporary_bytes: int
    max_wall_clock_milliseconds: int
    max_cpu_milliseconds: int
    max_process_memory_bytes: int
    max_warning_count: int
    max_finding_count: int
    max_decoded_characters: int
    max_text_lines: int
    max_text_line_length: int
    max_links_or_directives: int
    max_pdf_pages: int
    max_pdf_objects: int
    max_pdf_object_depth: int
    max_pdf_stream_bytes: int
    max_pdf_embedded_objects: int
    max_pdf_fonts: int
    max_pdf_extracted_characters: int
    max_docx_archive_entries: int
    max_docx_expanded_bytes: int
    max_docx_per_entry_bytes: int
    max_docx_compression_ratio: int
    max_docx_relationships: int
    max_docx_xml_depth: int
    max_docx_extracted_characters: int
    execution_allowed: bool
    network_allowed: bool
    external_fetch_allowed: bool
    macro_allowed: bool
    embedded_payload_allowed: bool
    ocr_allowed: bool

    def __post_init__(self) -> None:
        if (
            self.policy_id != "synthetic-resource-limits"
            or self.policy_version != "1"
        ):
            raise _invalid("resource_policy")
        for name in RESOURCE_LIMIT_FIELDS:
            value = getattr(self, name)
            if value != SYNTHETIC_RESOURCE_LIMITS[name]:
                raise _invalid(name)
            if name == "max_pdf_embedded_objects":
                if value != 0:
                    raise _invalid(name)
            else:
                _require_positive(value, name)
        for name in (
            "execution_allowed",
            "network_allowed",
            "external_fetch_allowed",
            "macro_allowed",
            "embedded_payload_allowed",
            "ocr_allowed",
        ):
            if getattr(self, name) is not False:
                raise _invalid(name)


@dataclass(frozen=True)
class InspectionPolicy:
    policy_id: str
    policy_version: str
    allowed_formats: tuple[DocumentFormat, ...]
    inspector_id: str
    inspector_version: str
    configuration_id: str
    configuration_version: str
    code_identity: str
    code_version: str
    isolation_policy_id: str
    isolation_policy_version: str
    required_output_kinds: tuple[str, ...]
    resource_policy_id: str
    resource_policy_version: str

    def __post_init__(self) -> None:
        exact = {
            "policy_id": "synthetic-inspection-policy",
            "policy_version": "1",
            "inspector_id": "synthetic-scripted-inspector",
            "inspector_version": "1",
            "configuration_id": "synthetic-scripted-inspector-config",
            "configuration_version": "1",
            "code_identity": "synthetic-scripted-inspector-code",
            "code_version": "1",
            "isolation_policy_id": "synthetic-interface-isolation",
            "isolation_policy_version": "1",
            "resource_policy_id": "synthetic-resource-limits",
            "resource_policy_version": "1",
        }
        for name, expected in exact.items():
            if getattr(self, name) != expected:
                raise _invalid(name)
        formats = _normalize_tuple(
            self.allowed_formats,
            "allowed_formats",
            required=True,
        )
        if formats != SYNTHETIC_FORMATS:
            raise _invalid("allowed_formats")
        object.__setattr__(self, "allowed_formats", formats)
        outputs = tuple(self.required_output_kinds)
        if outputs != SYNTHETIC_REQUIRED_OUTPUTS:
            raise _invalid("required_output_kinds")
        object.__setattr__(self, "required_output_kinds", outputs)


@dataclass(frozen=True)
class AdmissionPolicies:
    digest: DigestPolicy
    consumer: SyntheticConsumerPolicy
    retention: RetentionPolicy
    resources: ResourceLimitPolicy

    def __post_init__(self) -> None:
        for name, expected_type in (
            ("digest", DigestPolicy),
            ("consumer", SyntheticConsumerPolicy),
            ("retention", RetentionPolicy),
            ("resources", ResourceLimitPolicy),
        ):
            _require_instance(getattr(self, name), expected_type, name)

    def validate_envelope(self, envelope: SubmissionEnvelope) -> None:
        _require_instance(envelope, SubmissionEnvelope, "envelope")
        pairs = (
            (envelope.consumer_policy_id, self.consumer.policy_id),
            (
                envelope.consumer_policy_version,
                self.consumer.policy_version,
            ),
            (envelope.retention_policy_id, self.retention.policy_id),
            (
                envelope.retention_policy_version,
                self.retention.policy_version,
            ),
            (
                envelope.deletion_policy_id,
                self.retention.deletion_policy_id,
            ),
            (
                envelope.deletion_policy_version,
                self.retention.deletion_policy_version,
            ),
            (envelope.resource_policy_id, self.resources.policy_id),
            (
                envelope.resource_policy_version,
                self.resources.policy_version,
            ),
        )
        if any(actual != expected for actual, expected in pairs):
            raise _invalid("envelope_policy_identity")


def synthetic_digest_policy() -> DigestPolicy:
    return DigestPolicy("synthetic-sha256", "1", "sha256")


def synthetic_consumer_policy(
    *,
    effective_at: datetime,
    expires_at: datetime,
) -> SyntheticConsumerPolicy:
    return SyntheticConsumerPolicy(
        consumer_id="synthetic_validation_consumer",
        policy_id="synthetic-consumer-policy",
        policy_version="1",
        intended_use="synthetic_contract_validation",
        classification="synthetic_non_sensitive",
        permitted_formats=SYNTHETIC_FORMATS,
        required_output_kinds=SYNTHETIC_REQUIRED_OUTPUTS,
        effective_at=effective_at,
        expires_at=expires_at,
        runtime_access_allowed=False,
        api_access_allowed=False,
        registry_access_allowed=False,
        memory_access_allowed=False,
        retrieval_access_allowed=False,
        model_access_allowed=False,
        interface_access_allowed=False,
        real_information_access_allowed=False,
    )


def synthetic_retention_policy() -> RetentionPolicy:
    return RetentionPolicy(
        policy_id="synthetic-retention-policy",
        policy_version="1",
        deletion_policy_id="synthetic-deletion-policy",
        deletion_policy_version="1",
        temporary_retention_seconds=60,
        held_retention_seconds=300,
        received_disposition=RetentionDisposition.RETAIN_TEMPORARILY,
        quarantined_disposition=RetentionDisposition.RETAIN_TEMPORARILY,
        validating_disposition=RetentionDisposition.RETAIN_TEMPORARILY,
        accepted_disposition=RetentionDisposition.DELETE,
        rejected_disposition=RetentionDisposition.DELETE,
        held_disposition=RetentionDisposition.RETAIN_TEMPORARILY,
        evaluation_failed_disposition=RetentionDisposition.RETAIN_TEMPORARILY,
        ready_output_disposition=RetentionDisposition.DELETE,
        processing_failed_output_disposition=RetentionDisposition.DELETE,
        legal_hold_enabled=True,
        cleanup_required=True,
        accountable_owner_role="Codex - Implementation Engineer",
        custody_role="Codex - Implementation Engineer",
    )


def synthetic_resource_limit_policy() -> ResourceLimitPolicy:
    return ResourceLimitPolicy(
        policy_id="synthetic-resource-limits",
        policy_version="1",
        **SYNTHETIC_RESOURCE_LIMITS,
        execution_allowed=False,
        network_allowed=False,
        external_fetch_allowed=False,
        macro_allowed=False,
        embedded_payload_allowed=False,
        ocr_allowed=False,
    )


def synthetic_inspection_policy() -> InspectionPolicy:
    return InspectionPolicy(
        policy_id="synthetic-inspection-policy",
        policy_version="1",
        allowed_formats=SYNTHETIC_FORMATS,
        inspector_id="synthetic-scripted-inspector",
        inspector_version="1",
        configuration_id="synthetic-scripted-inspector-config",
        configuration_version="1",
        code_identity="synthetic-scripted-inspector-code",
        code_version="1",
        isolation_policy_id="synthetic-interface-isolation",
        isolation_policy_version="1",
        required_output_kinds=SYNTHETIC_REQUIRED_OUTPUTS,
        resource_policy_id="synthetic-resource-limits",
        resource_policy_version="1",
    )


def synthetic_authorization_policy(
    signer_key_ids: tuple[str, ...],
) -> AuthorizationPolicy:
    return AuthorizationPolicy(
        policy_id="synthetic-authorization-policy",
        policy_version="1",
        required_purpose="synthetic_document_admission",
        required_classification="synthetic_non_sensitive",
        required_operation="admit_synthetic_document",
        trusted_signer_key_ids=signer_key_ids,
        max_receipt_lifetime_seconds=900,
        requires_single_use=True,
    )


def synthetic_custody_policy() -> CustodyPolicy:
    return CustodyPolicy(
        policy_id="synthetic-custody-policy",
        policy_version="1",
        encryption_algorithm="synthetic-xor-stream-v1",
        header_version=1,
        key_derivation_id="synthetic-hkdf-sha256-v1",
        required_object_kind="source",
        requires_authenticated_encryption=True,
        allows_plaintext_persistence=False,
        max_ciphertext_expansion_bytes=128,
    )
