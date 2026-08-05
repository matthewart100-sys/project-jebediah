# Knowledge Manager 1.0 Phase 2 Synthetic Implementation Activation

**Status:** Proposed

**Date:** 2026-08-05

**Canonical planning base:**
`92e4b8c7353f6d47097e7eaf6c743c78f39c8e10`

**Decision owner:** Chief Architect

**Implementation owner:** Codex - Implementation Engineer

**Independent reviewer:** Work Mode

**Authorization state:** Documentation-only activation proposal. No
implementation is authorized unless the exact remote head receives independent
Work Mode approval, the Chief Architect adopts the proposed authorization
record for that exact head, and the reviewed package is merged to canonical
`main`.

## Purpose

This package converts the accepted
[Phase 2 Document Inspection Plan](KNOWLEDGE_MANAGER_1_PHASE_2_DOCUMENT_INSPECTION_PLAN.md)
and
[Phase 2 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_2_VALIDATION_REQUIREMENTS.md)
into one exact, bounded implementation candidate.

The candidate asks only:

> Can Project Jebediah enforce document-admission contracts with generated
> synthetic bytes, immutable evidence, process-local reference adapters, and
> deterministic failure behavior without creating a real document path?

The answer remains unproven until implementation and exact-head implementation
review complete. This proposal creates no parser, service, durable store,
runtime consumer, or real-information authority.

## Repository Verified

- Phase 1 Knowledge Registry implementation and closeout are canonical.
- Pull request #50 established the accepted Phase 2 architecture and validation
  baseline at canonical commit
  `92e4b8c7353f6d47097e7eaf6c743c78f39c8e10`.
- The accepted admission states, transformation states, quarantine boundary,
  consumer-eligibility rule, and authority model remain owned by ADR 0013.
- The repository has no `collector.document_admission` package, parser,
  quarantine runtime, document upload path, or real document authorization.
- No active implementation sprint is authorized at this proposal stage.

## Exact implementation objective

Implement a standard-library-only `collector.document_admission` package that:

1. Represents immutable synthetic submission, quarantine, evaluation,
   inspection, transition, cleanup, and audit evidence.
2. Enforces the accepted admission and transformation transition graphs.
3. Computes and verifies byte identity for generated synthetic bytes with one
   explicitly synthetic digest profile.
4. Defines storage-neutral detector, security-evaluator, isolated-inspector,
   eligibility, quarantine, evidence-journal, and cleanup interfaces.
5. Provides process-local in-memory quarantine and evidence reference adapters.
6. Coordinates only injected synthetic test doubles; it selects no parser,
   scanner, sandbox, external binary, or network service.
7. Produces deterministic typed failures and sanitized evidence.
8. Proves through synthetic tests that no registry, memory, Qdrant, retrieval,
   service, API, UI, deployment, or real-information path exists.

## Authorized scope

The proposed authorization is limited to:

- immutable document-admission metadata models;
- immutable quarantine and byte-integrity evidence;
- immutable admission and transformation attempt records;
- exact state-transition enforcement;
- resource, retention, consumer, digest, and inspection policy models;
- typed failures;
- storage-neutral abstract interfaces;
- a SHA-256 synthetic byte-integrity verifier using `hashlib`;
- process-local in-memory quarantine and append-only evidence adapters;
- orchestration over injected detector, evaluator, inspector, and eligibility
  interfaces;
- generated synthetic byte builders and scripted test doubles;
- deterministic unit, contract, boundary, and regression tests; and
- documentation directly required to describe the implementation candidate.

The package name is repository organization inside the accepted Collector
boundary. It does not create a new component or transfer source, information,
Knowledge Vault, registry, memory, runtime, or action authority.

## Explicit exclusions

The implementation must not add or perform:

- access to, copying of, hashing of, inspection of, parsing of, or ingestion of
  any real VBA or organizational document;
- filesystem discovery, watched folders, uploads, drag-and-drop, APIs, CLIs,
  queues, services, scheduled jobs, or user interfaces;
- a production quarantine, source-artifact store, database, migration, backup,
  restore mechanism, or retention service;
- a real PDF, DOCX, TXT, or Markdown parser;
- OCR, malware scanning, macro inspection, archive extraction, external fetch,
  subprocess sandbox, container sandbox, or operating-system isolation;
- Qdrant, embeddings, models, summaries, Memory Service, Knowledge Registry
  writes, retrieval, indexing, ranking, or promotion;
- Open WebUI, n8n, FastAPI, Docker, deployment, or network access;
- autonomous admission, human-approval substitution, factual verification,
  source correction, consumer authorization, or action authority;
- dependency or lock-file changes; or
- modification of the legacy `collector.adapters.file` path or any existing
  runtime composition.

Any need for an excluded capability invalidates this plan and stops
implementation for revised architecture review.

## Component and package boundaries

The accepted responsibility remains inside the existing Collector Engine
boundary. The implementation creates a disconnected repository package:

```text
src/collector/document_admission/
    __init__.py
    failures.py
    models.py
    policies.py
    interfaces.py
    state_transitions.py
    in_memory_adapters.py
    orchestration.py
```

The package:

- may import only the Python standard library and modules inside its own
  boundary;
- must not import `collector.memory`, `collector.knowledge.registry`, existing
  Collector pipelines or adapters, service modules, Qdrant, Ollama, FastAPI, or
  network clients;
- must not be imported by an existing source or service module;
- exposes no runtime entry point or ordinary content reader; and
- treats all bytes held by its in-memory quarantine as synthetic,
  process-local, and test-only.

## Exact state vocabularies

### Admission state

`AdmissionState` contains exactly:

- `received`
- `quarantined`
- `validating`
- `accepted`
- `rejected`
- `held`
- `evaluation_failed`

Allowed transitions are exactly:

```text
received -> quarantined
quarantined -> validating
validating -> accepted
validating -> rejected
validating -> held
validating -> evaluation_failed
```

`accepted`, `rejected`, `held`, and `evaluation_failed` are terminal for one
attempt. A terminal attempt is never mutated. Review or retry creates a new
attempt with a `prior_attempt_id`.

### Transformation state

`TransformationState` contains exactly:

- `processing`
- `ready`
- `processing_failed`

Allowed transitions are exactly:

```text
processing -> ready
processing -> processing_failed
```

`ready` and `processing_failed` are terminal for one attempt. `ready` requires
`ExtractionQuality.complete` and an eligible decision for the exact synthetic
consumer. Ordinary and runtime eligibility remain false.

### Supporting vocabularies

| Type | Exact values |
| --- | --- |
| `DocumentFormat` | `pdf`, `docx`, `txt`, `markdown` |
| `FormatDetectionState` | `detected`, `unsupported`, `ambiguous`, `unavailable` |
| `EvaluationOutcome` | `pass`, `reject`, `hold`, `unavailable` |
| `ExtractionQuality` | `complete`, `partial`, `none` |
| `ConsumerEligibilityOutcome` | `eligible`, `ineligible`, `unavailable` |
| `CleanupOutcome` | `deleted`, `retained`, `legal_hold`, `failed` |
| `RetentionDisposition` | `delete`, `retain_temporarily`, `legal_hold` |
| `RetryKind` | `dependency_restored`, `authorized_review`, `corrected_resubmission` |

An unknown enum value is a validation failure. No enum value means truth,
general approval, source authority, registry eligibility, memory eligibility,
ordinary retrieval eligibility, or action authority.

## Exact immutable domain records

All records use frozen dataclasses. Identifiers and reason codes are non-empty
opaque strings. Times are timezone-aware and supplied by the caller. Collections
normalize to tuples and reject duplicate stable identities. Constructors do not
read current time, generate identities, inspect a filesystem, infer authority,
or perform I/O.

### Byte and quarantine records

| Record | Required fields and invariants |
| --- | --- |
| `DigestPolicy` | `policy_id`, `policy_version`, `algorithm`; the authorized synthetic instance is exactly `synthetic-sha256` version `1` with algorithm `sha256` |
| `ContentIdentity` | `digest_policy_id`, `digest_policy_version`, `algorithm`, lowercase `digest_hex`, and non-negative `byte_count`; synthetic SHA-256 requires exactly 64 hexadecimal characters |
| `QuarantineReceipt` | `quarantine_id`, `submission_id`, `admission_attempt_id`, `content_identity`, `adapter_id`, `adapter_version`, `placed_at`, and `integrity_evidence_id` |
| `IntegrityVerification` | `verification_id`, `quarantine_id`, expected and observed `ContentIdentity`, `verifier_id`, `verifier_version`, `checked_at`, and `matches` |

No record contains document bytes or extracted text. Bytes exist only inside the
process-local quarantine adapter and inside a bounded method call.

### Submission and policy records

| Record | Required fields and invariants |
| --- | --- |
| `SubmissionEnvelope` | `submission_id`, `source_authority_id`, `safe_source_reference`, `producer_id`, `submitter_id`, `information_domain`, `intended_use`, `consumer_id`, `consumer_policy_id`, `consumer_policy_version`, `supplied_name`, `safe_name`, `claimed_media_type`, `classification`, `retention_policy_id`, `retention_policy_version`, `deletion_policy_id`, `deletion_policy_version`, `resource_policy_id`, `resource_policy_version`, non-empty `provenance_evidence_ids`, `received_at`, and `correlation_id` |
| `SyntheticConsumerPolicy` | `consumer_id`, `policy_id`, `policy_version`, `intended_use`, `classification`, non-empty `permitted_formats`, non-empty `required_output_kinds`, `effective_at`, `expires_at`, and `runtime_access_allowed`, `api_access_allowed`, `registry_access_allowed`, `memory_access_allowed`, `retrieval_access_allowed`, `model_access_allowed`, `interface_access_allowed`, and `real_information_access_allowed`, all exactly false |
| `RetentionPolicy` | `policy_id`, `policy_version`, `deletion_policy_id`, `deletion_policy_version`, positive `temporary_retention_seconds` and `held_retention_seconds`, exact `received_disposition`, `quarantined_disposition`, `validating_disposition`, `accepted_disposition`, `rejected_disposition`, `held_disposition`, `evaluation_failed_disposition`, `ready_output_disposition`, and `processing_failed_output_disposition`, `legal_hold_enabled`, `cleanup_required`, `accountable_owner_role`, and `custody_role`; each disposition is a `RetentionDisposition`, legal hold is valid only when enabled and separately evidenced, and no disposition is implicit |
| `ResourceLimitPolicy` | `policy_id`, `policy_version`, every exact `max_*` field below, and `execution_allowed`, `network_allowed`, `external_fetch_allowed`, `macro_allowed`, `embedded_payload_allowed`, and `ocr_allowed`, all exactly false |
| `InspectionPolicy` | `policy_id`, `policy_version`, non-empty `allowed_formats`, `inspector_id`, `inspector_version`, `configuration_id`, `configuration_version`, `code_identity`, `code_version`, `isolation_policy_id`, `isolation_policy_version`, non-empty `required_output_kinds`, `resource_policy_id`, and `resource_policy_version` |
| `AdmissionPolicies` | `digest`, `consumer`, `retention`, and `resources`; the fields contain the exact policy records above, every identity/version must match the envelope, and none is optional |
| `AdmissionOperationContext` | `admission_attempt_id`, `quarantine_id`, `integrity_evidence_id`, `integrity_verification_id`, `format_detection_id`, `security_evaluation_id`, `policy_evaluation_id`, exactly three ordered `transition_ids`, exactly three ordered `audit_event_ids`, `quarantined_at`, `validating_at`, `checked_at`, and `completed_at`; identities are caller-supplied and unique, times are timezone-aware and caller-supplied, and times are non-decreasing from `SubmissionEnvelope.received_at` |
| `InspectionOperationContext` | `transformation_attempt_id`, `inspection_result_id`, `consumer_eligibility_decision_id`, `transition_id`, `audit_event_id`, `started_at`, `decided_at`, and `completed_at`; identities are caller-supplied and unique, times are timezone-aware and caller-supplied, and times are non-decreasing |
| `CleanupOperationContext` | `cleanup_id`, `audit_event_id`, `requested_at`, and `completed_at`; identities are caller-supplied and unique, times are timezone-aware and caller-supplied, and completion is not earlier than request |
| `RetryEvidence` | `retry_id`, `prior_attempt_id`, `retry_kind`, `authorized_role`, `reason_code`, non-empty `evidence_ids`, and `decided_at`; held attempts require `authorized_review`, unavailable dependencies require `dependency_restored`, rejected attempts may use only a `corrected_resubmission` with a new `submission_id`, and retry never mutates the prior attempt |

The only authorized fixture values for the envelope authority and scope fields
are:

```text
source_authority_id = synthetic_fixture_authority
safe_source_reference = generated_in_test
producer_id = synthetic_fixture_builder
submitter_id = synthetic_test_caller
information_domain = synthetic_document_inspection
intended_use = synthetic_contract_validation
consumer_id = synthetic_validation_consumer
classification = synthetic_non_sensitive
```

The exact policy profile identities are:

```text
consumer policy = synthetic-consumer-policy version 1
retention policy = synthetic-retention-policy version 1
deletion policy = synthetic-deletion-policy version 1
resource policy = synthetic-resource-limits version 1
inspection policy = synthetic-inspection-policy version 1
```

Different values fail validation. These are test-policy identifiers, not a real
domain, source, person, user, consumer, or policy authorization.

The exact `synthetic-consumer-policy` version `1` permits all four
`DocumentFormat` values, requires only `synthetic_inspection_evidence`, has
caller-supplied aware effective and expiry times with expiry after effect, and
sets every access flag false.

The exact `synthetic-retention-policy` version `1` uses deletion policy
`synthetic-deletion-policy` version `1`, 60-second temporary retention,
300-second held retention, and these dispositions:

```text
received = retain_temporarily
quarantined = retain_temporarily
validating = retain_temporarily
accepted = delete
rejected = delete
held = retain_temporarily
evaluation_failed = retain_temporarily
ready output = delete
processing_failed output = delete
```

Cleanup is required. Synthetic legal-hold behavior is enabled only to validate
that separate typed hold evidence overrides covered deletion and cannot create
general retention authority. `accountable_owner_role` and `custody_role` are
both exactly `Codex - Implementation Engineer` for process-local synthetic
execution. The only permitted synthetic `LegalHoldEvidence.authority_role` is
`Chief Architect`; the fixture proves enforcement only and records no real
hold.

The exact `synthetic-inspection-policy` version `1` allows all four candidate
formats, uses inspector `synthetic-scripted-inspector` version `1`,
configuration `synthetic-scripted-inspector-config` version `1`, code identity
`synthetic-scripted-inspector-code` version `1`, isolation policy
`synthetic-interface-isolation` version `1`, requires only
`synthetic_inspection_evidence`, and references `synthetic-resource-limits`
version `1`. The isolation identity names an interface contract, not an
operating-system sandbox.

### Evaluation records

| Record | Required fields and invariants |
| --- | --- |
| `FormatDetectionResult` | `detection_id`, `submission_id`, `admission_attempt_id`, `detector_id`, `detector_version`, `resource_policy_id`, `resource_policy_version`, `state`, optional `detected_format`, `supplied_media_type`, `safe_filename_suffix`, `reason_code`, immutable `finding_codes`, and `checked_at`; only `detected` has a format |
| `SecurityEvaluation` | `evaluation_id`, `submission_id`, `admission_attempt_id`, `evaluator_id`, `evaluator_version`, `resource_policy_id`, `resource_policy_version`, `outcome`, `reason_code`, immutable `evidence_references`, and `checked_at` |
| `PolicyEvaluation` | `evaluation_id`, `submission_id`, `admission_attempt_id`, `evaluator_id`, `evaluator_version`, `consumer_policy_id`, `consumer_policy_version`, `retention_policy_id`, `retention_policy_version`, `deletion_policy_id`, `deletion_policy_version`, `resource_policy_id`, `resource_policy_version`, `outcome`, `reason_code`, immutable `evidence_references`, and `checked_at` |
| `ConsumerEligibilityDecision` | `decision_id`, `transformation_attempt_id`, `consumer_id`, `consumer_policy_id`, `consumer_policy_version`, `intended_use`, `classification`, `outcome`, `reason_code`, immutable `evidence_references`, and `decided_at`; only the exact synthetic consumer may be `eligible` |
| `ResourceObservation` | `observation_id`, `resource_policy_id`, `resource_policy_version`, one non-negative `observed_*` field corresponding exactly to every numeric `max_*` field below, immutable `exceeded_limit_names`, and `observed_at`; exceeded names must be members of the policy field vocabulary |

### State and result records

| Record | Required fields and invariants |
| --- | --- |
| `AdmissionTransition` | `transition_id`, `submission_id`, `admission_attempt_id`, `prior_state`, `next_state`, `occurred_at`, `actor_id`, `component_id`, `reason_code`, `policy_id`, `policy_version`, and `correlation_id`; transition must be in the exact graph |
| `TransformationTransition` | `transition_id`, `submission_id`, `transformation_attempt_id`, `prior_state`, `next_state`, `occurred_at`, `actor_id`, `component_id`, `reason_code`, `policy_id`, `policy_version`, and `correlation_id`; transition must be in the exact graph |
| `AdmissionAttemptRecord` | `admission_attempt_id`, `submission_id`, optional `prior_admission_attempt_id`, optional `retry_evidence`, `state`, optional `quarantine_receipt`, optional `integrity_verification`, ordered `transitions`, optional `format_detection`, optional `security_evaluation`, optional `policy_evaluation`, `started_at`, optional `completed_at`, optional `authorized_review_evidence_id`, `disposition_reason_code`, and `correlation_id`; transitions are empty only at `received`, completion is present exactly for terminal states, evidence presence must match the reached state, and all nested identities must agree |
| `OutputIdentity` | `output_id`, `output_version`, `output_content_identity`, `output_kind`, and exact `input_content_identity`; it does not contain output bytes or text |
| `InspectionResult` | `inspection_result_id`, `submission_id`, `transformation_attempt_id`, `input_content_identity`, `inspector_id`, `inspector_version`, `configuration_id`, `configuration_version`, `code_identity`, `code_version`, `policy_id`, `policy_version`, `started_at`, `completed_at`, `detected_format`, optional `output_identity`, `extraction_quality`, `location_map_available`, non-negative `unit_count` and `extracted_character_count`, immutable `warning_codes`, `omission_codes`, and `reached_limit_names`, optional `failure_kind`, and `resource_observation`; it contains no eligibility decision because eligibility is evaluated from the completed result |
| `TransformationAttemptRecord` | `transformation_attempt_id`, `submission_id`, `admission_attempt_id`, optional `prior_transformation_attempt_id`, optional `retry_evidence`, `state`, ordered `transitions`, optional `inspection_result`, optional `consumer_eligibility_decision`, `started_at`, optional `completed_at`, `disposition_reason_code`, and `correlation_id`; transitions are empty only at initial `processing`, completion is present exactly for terminal states, only `ready` contains an eligible decision, and every nested identity must agree |
| `LegalHoldEvidence` | `legal_hold_id`, `quarantine_id`, `authority_role`, `retention_policy_id`, `retention_policy_version`, `scope`, `reason_code`, non-empty `evidence_references`, `effective_at`, and optional `expires_at`; expiry must follow effect and the hold covers only its exact scope |
| `CleanupEvidence` | `cleanup_id`, `quarantine_id`, `retention_policy_id`, `retention_policy_version`, `deletion_policy_id`, `deletion_policy_version`, `admission_attempt_id`, `outcome`, `scope`, `actor_id`, `component_id`, `reason_code`, `requested_at`, optional `completed_at`, and optional `unresolved_obligation_reference` |
| `AuditEvent` | `event_id`, `correlation_id`, `subject_id`, optional `admission_attempt_id`, optional `transformation_attempt_id`, `event_kind`, `actor_id`, `component_id`, `reason_code`, `policy_id`, `policy_version`, `recorded_at`, and immutable `safe_evidence_references` |

`AuditEvent`, failures, and reason fields reject bytes, extracted text, stack
traces, private paths, credentials, personal information, and arbitrary metadata
maps.

## Synthetic resource policy

The implementation includes one deliberately small profile,
`synthetic-resource-limits` version `1`. It is test evidence only and must never
be represented as a production default.

| Dimension | Exact field | Exact synthetic limit |
| --- | --- | ---: |
| Input bytes | `max_input_bytes` | 65,536 |
| Result bytes | `max_result_bytes` | 131,072 |
| Temporary bytes | `max_temporary_bytes` | 262,144 |
| Wall-clock milliseconds | `max_wall_clock_milliseconds` | 1,000 |
| CPU milliseconds | `max_cpu_milliseconds` | 1,000 |
| Process memory bytes | `max_process_memory_bytes` | 16,777,216 |
| Warning count | `max_warning_count` | 16 |
| Finding count | `max_finding_count` | 32 |
| Decoded characters | `max_decoded_characters` | 32,768 |
| Text lines | `max_text_lines` | 1,000 |
| Text line length | `max_text_line_length` | 4,096 |
| Links or directives | `max_links_or_directives` | 64 |
| PDF pages | `max_pdf_pages` | 8 |
| PDF objects | `max_pdf_objects` | 512 |
| PDF object depth | `max_pdf_object_depth` | 16 |
| PDF stream bytes | `max_pdf_stream_bytes` | 65,536 |
| PDF embedded objects | `max_pdf_embedded_objects` | 0 |
| PDF fonts | `max_pdf_fonts` | 16 |
| PDF extracted characters | `max_pdf_extracted_characters` | 32,768 |
| DOCX archive entries | `max_docx_archive_entries` | 128 |
| DOCX expanded bytes | `max_docx_expanded_bytes` | 262,144 |
| DOCX per-entry bytes | `max_docx_per_entry_bytes` | 65,536 |
| DOCX compression ratio | `max_docx_compression_ratio` | 20 |
| DOCX relationships | `max_docx_relationships` | 128 |
| DOCX XML depth | `max_docx_xml_depth` | 32 |
| DOCX extracted characters | `max_docx_extracted_characters` | 32,768 |

All limits are mandatory positive integers except explicitly prohibited
capabilities, whose allowances are exactly zero. Tests use observations and
scripted outcomes; the candidate does not implement a PDF/DOCX parser or
operating-system resource sandbox.

## Exact interfaces

All interfaces are abstract base classes. Implementations must return typed
records or raise one of the typed failures below. They must not return
success-shaped fallbacks.

### `ByteIntegrityVerifier`

```text
identify(payload: bytes, policy: DigestPolicy) -> ContentIdentity
verify(payload: bytes, expected: ContentIdentity, verification_id: str,
       checked_at: datetime)
    -> IntegrityVerification
```

Only the synthetic SHA-256 implementation is authorized.

### `QuarantineRepository`

```text
place(envelope: SubmissionEnvelope, admission_attempt_id: str,
      quarantine_id: str, integrity_evidence_id: str, payload: bytes,
      identity: ContentIdentity,
      placed_at: datetime) -> QuarantineReceipt
open_for_evaluation(receipt: QuarantineReceipt) -> bytes
verify(receipt: QuarantineReceipt, verification_id: str,
       checked_at: datetime)
    -> IntegrityVerification
delete(receipt: QuarantineReceipt, policy: RetentionPolicy,
       legal_hold: LegalHoldEvidence | None,
       context: CleanupOperationContext) -> CleanupEvidence
```

`open_for_evaluation` is an internal evaluator boundary. The interface has no
ordinary read, list, search, path, export, update, or consumer method.

### `EvidenceJournal`

```text
append_admission_transition(transition: AdmissionTransition) -> None
append_transformation_transition(transition: TransformationTransition) -> None
append_audit_event(event: AuditEvent) -> None
admission_history(attempt_id: str) -> tuple[AdmissionTransition, ...]
transformation_history(attempt_id: str)
    -> tuple[TransformationTransition, ...]
```

Equal repeated append is idempotent. Different evidence under an existing
identity raises `DocumentAdmissionConflict`. Existing evidence is never
overwritten or deleted.

### Evaluation interfaces

```text
FormatDetector.detect(payload: bytes, envelope: SubmissionEnvelope,
                      admission_attempt_id: str,
                      detection_id: str,
                      policy: ResourceLimitPolicy,
                      checked_at: datetime) -> FormatDetectionResult

SecurityEvaluator.evaluate(payload: bytes, envelope: SubmissionEnvelope,
                          detected: FormatDetectionResult,
                          evaluation_id: str,
                          policy: ResourceLimitPolicy,
                          checked_at: datetime) -> SecurityEvaluation

PolicyEvaluator.evaluate(envelope: SubmissionEnvelope,
                         detected: FormatDetectionResult,
                         security: SecurityEvaluation,
                         evaluation_id: str,
                         consumer: SyntheticConsumerPolicy,
                         retention: RetentionPolicy,
                         resources: ResourceLimitPolicy,
                         checked_at: datetime) -> PolicyEvaluation

IsolatedInspector.inspect(payload: bytes, admission: AdmissionAttemptRecord,
                          transformation_attempt_id: str,
                          inspection_result_id: str,
                          policy: InspectionPolicy,
                          started_at: datetime,
                          completed_at: datetime) -> InspectionResult

ConsumerEligibilityEvaluator.evaluate(
    result: InspectionResult,
    consumer: SyntheticConsumerPolicy,
    decision_id: str,
    decided_at: datetime,
) -> ConsumerEligibilityDecision
```

Only interfaces and injected scripted test doubles are authorized for detector,
security evaluator, policy evaluator, inspector, and eligibility evaluator.
No real parser, scanner, process isolation, or external evaluator implementation
is authorized.

### `DocumentAdmissionOrchestrator`

```text
submit(envelope: SubmissionEnvelope, payload: bytes,
       policies: AdmissionPolicies,
       context: AdmissionOperationContext) -> AdmissionAttemptRecord
inspect(admission: AdmissionAttemptRecord,
        policy: InspectionPolicy,
        consumer: SyntheticConsumerPolicy,
        context: InspectionOperationContext) -> TransformationAttemptRecord
retry_admission(prior: AdmissionAttemptRecord,
                retry: RetryEvidence,
                envelope: SubmissionEnvelope,
                payload: bytes,
                policies: AdmissionPolicies,
                context: AdmissionOperationContext) -> AdmissionAttemptRecord
retry_inspection(admission: AdmissionAttemptRecord,
                 prior: TransformationAttemptRecord,
                 retry: RetryEvidence,
                 policy: InspectionPolicy,
                 consumer: SyntheticConsumerPolicy,
                 context: InspectionOperationContext)
    -> TransformationAttemptRecord
cleanup(receipt: QuarantineReceipt,
        policy: RetentionPolicy,
        legal_hold: LegalHoldEvidence | None,
        context: CleanupOperationContext) -> CleanupEvidence
```

The orchestrator:

- receives synthetic bytes directly from the test caller only;
- quarantines and verifies bytes before invoking another boundary;
- creates append-only transitions;
- maps conclusive failure to `rejected`, judgment to `held`, and unavailable or
  indeterminate evaluation to `evaluation_failed`;
- starts inspection only from an accepted admission attempt;
- maps complete and exactly eligible output to `ready`;
- maps partial, absent, invalid, ineligible, unavailable, crash, timeout, or
  unknown output to `processing_failed`;
- never retries a rejected attempt automatically; and
- has no service, CLI, watcher, filesystem adapter, or runtime composition.

## Typed failures

`failures.py` defines:

| Failure | Meaning |
| --- | --- |
| `DocumentAdmissionError` | Base for all package failures |
| `DocumentAdmissionValidationError` | Invalid type, identity, enum, timestamp, policy, transition, or invariant |
| `DocumentAdmissionConflict` | One stable evidence identity was reused for different immutable evidence |
| `DocumentAdmissionNotFound` | Required process-local quarantine or evidence identity is absent |
| `EvaluatorUnavailable` | A required detector, evaluator, policy, or eligibility result is unavailable |
| `PolicyViolation` | A conclusive authorization, format, provenance, classification, retention, or policy failure |
| `ResourceLimitExceeded` | A named synthetic resource limit was exceeded |
| `InspectionFailed` | Scripted isolated inspection crashed, timed out, returned malformed evidence, or produced an invalid result |
| `QuarantineFailure` | Placement, integrity, or process-local quarantine access failed |
| `CleanupFailed` | Required synthetic cleanup failed or remained partial |
| `UnknownOutcome` | A durable-looking operation has indeterminate outcome and must be reconciled before retry |

Every failure includes only a stable reason code and safe identifiers needed for
correlation. Failures contain no payload, extracted text, supplied sensitive
metadata, private path, raw parser output, or stack-local content.

## Synthetic fixture policy

Fixtures are constructed in Python from explicit byte literals or deterministic
builders. No fixture is copied from a local or remote document.

Permitted fixture families:

- bounded UTF-8 and UTF-8-with-BOM text;
- inert Markdown links, HTML-like text, directives, and model-like instructions;
- minimal non-executable byte markers representing PDF and DOCX outcomes for
  scripted detectors and inspectors;
- malformed, truncated, ambiguous, encrypted-marker, traversal-marker,
  macro-marker, oversized, timeout, crash, and cleanup-failure cases; and
- deterministic consumer, policy, state, retry, and eligibility evidence.

No fixture contains functional malware, executable macros, copyrighted source
material, real names, organizational records, credentials, private addresses,
or operational values. Fixture builders label every payload
`synthetic_non_sensitive`.

## Test inventory

```text
tests/collector/document_admission/
    __init__.py
    synthetic_fixtures.py
    test_models.py
    test_policies.py
    test_state_transitions.py
    test_byte_integrity.py
    test_quarantine.py
    test_format_detection.py
    test_security_dispositions.py
    test_resource_limits.py
    test_inspection_results.py
    test_admission_orchestration.py
    test_failure_and_retry.py
    test_cleanup.py
    test_package_boundaries.py
```

The tests cover:

- valid synthetic submissions and all immutable record invariants;
- invalid identity, malformed metadata, duplicate evidence, invalid enums, and
  naive timestamps;
- unsupported, spoofed, mismatched, ambiguous, encrypted-marker, macro-marker,
  traversal-marker, malformed, and truncated format outcomes;
- integrity mismatch and quarantine placement, verification, isolation,
  not-found, conflict, unknown-outcome, and cleanup behavior;
- exact admission and transformation transition graphs and terminal-state
  immutability;
- held, rejected, evaluation-failed, retry, review-evidence, and prior-attempt
  semantics;
- every synthetic resource limit below, at, and above its value without
  exhausting the development machine;
- scripted inspector crash, timeout, malformed result, partial output, absent
  output, and failed eligibility;
- exact synthetic-consumer authorization and ordinary/runtime eligibility fixed
  false;
- deterministic equality, failure isolation, cleanup, and no shared mutable
  state;
- sanitized failures and audit evidence;
- no external service, network, filesystem discovery, production persistence,
  content persistence, registry write, Qdrant, memory, model, retrieval, API,
  UI, or deployment dependency; and
- no real-information fixture or path.

The empty test `__init__.py` is only a package marker preventing existing test
basename collisions.

## Dependencies

The detailed decision is in the
[Phase 2 Dependency Assessment](KNOWLEDGE_MANAGER_1_PHASE_2_DEPENDENCY_ASSESSMENT.md).
The implementation adds no dependency and changes no manifest or lock file.

Required capabilities use:

- Python 3.12-or-newer standard library;
- existing `pytest>=8.0` for tests; and
- existing repository documentation and lock validation.

Parser libraries, scanner products, external binaries, process/container
isolation, network clients, and production persistence are deferred and
unauthorized.

## Threat model

The complete required matrix is in the
[Phase 2 Threat Model](KNOWLEDGE_MANAGER_1_PHASE_2_THREAT_MODEL.md). Every named
threat has prevention, detection, failure default, sanitized audit evidence,
test evidence, and a canonical owner.

Controls implemented in this candidate are limited to model invariants,
transition enforcement, byte identity, process-local quarantine, injected
interface boundaries, scripted failure behavior, sanitized evidence, resource
policy models, and package-boundary tests. The package must not claim that an
interface or fake provides operating-system isolation, malware detection, or
safe parsing.

## Ownership assignments

| Responsibility | Assigned canonical role or state | Boundary |
| --- | --- | --- |
| Collector Engine component ownership | **Maintainer accountable**, as already recorded in the Component Registry | Existing component responsibility only; no new component is created |
| Architecture, scope, exceptions, sprint authorization, and final decisions | Chief Architect | Final authority under the Project Coordination Protocol |
| Bounded package implementation, local synthetic execution, fixture construction, cleanup, rollback, and evidence handoff | Codex - Implementation Engineer | Repository candidate only; no runtime or live-information authority |
| Independent architecture, security-quality, implementation, and test-evidence review | Work Mode | Must be a distinct instance that did not author or modify the reviewed artifact |
| Canonical post-merge evidence reconciliation | Documentation Suite | Documentation closeout only after an approved implementation merge |
| Runtime consumption and operations | Jebediah Runtime has no authority in this phase | No runtime is created; future operational ownership remains a blocker for deployment and real information |
| Evidence custody | GitHub engineering memory; Codex supplies the handoff and Documentation Suite records merged sanitized evidence | No private or sensitive raw evidence is required because all fixtures are synthetic |

No role gains source, information-owner, consumer, operational, or action
authority through this assignment. A future runtime operator, live information
owner, real producer, real submitter, real consumer, and evidence custodian
remain unresolved and block real-document work, but they do not block this
process-local synthetic candidate.

## Recovery and rollback

The candidate creates no durable or external state.

During tests:

- each in-memory adapter is created per test;
- cleanup deletes process-local synthetic bytes and records `CleanupEvidence`;
- teardown fails if process-local quarantine is non-empty unless a test
  explicitly verifies synthetic legal-hold behavior;
- failed cleanup is visible and never reported as success; and
- no test may recover bytes from logs, audit events, indexes, caches, or another
  test.

Implementation rollback is a reviewed revert of the bounded source, test, and
directly required documentation files. No data migration, service shutdown,
credential rotation, backup restore, registry cleanup, Qdrant cleanup, memory
cleanup, or deployment action applies.

Rollback validation reruns the full suite, compilation, frozen-lock,
documentation, package-boundary, whitespace, and sensitive-value checks.

## Validation commands

The future implementation review must run:

```text
python -m pytest -q tests/collector/document_admission
python -m pytest -q
python -m compileall -q src services tests
python scripts/validate_docs.py
uv --system-certs lock --check
git diff --check
```

It must also record:

- changed Python diagnostics;
- exact base and head;
- source/test/document manifest;
- import-boundary and prohibited-symbol scans;
- no dependency or lock change;
- no network, external service, subprocess, container, or production
  persistence use;
- no real or external document read;
- no content, registry, memory, Qdrant, retrieval, API, UI, runtime, or
  deployment integration; and
- independent Work Mode review of the exact remote head.

## Exact future implementation manifest

Implementation may create:

```text
src/collector/document_admission/__init__.py
src/collector/document_admission/failures.py
src/collector/document_admission/models.py
src/collector/document_admission/policies.py
src/collector/document_admission/interfaces.py
src/collector/document_admission/state_transitions.py
src/collector/document_admission/in_memory_adapters.py
src/collector/document_admission/orchestration.py
tests/collector/document_admission/__init__.py
tests/collector/document_admission/synthetic_fixtures.py
tests/collector/document_admission/test_models.py
tests/collector/document_admission/test_policies.py
tests/collector/document_admission/test_state_transitions.py
tests/collector/document_admission/test_byte_integrity.py
tests/collector/document_admission/test_quarantine.py
tests/collector/document_admission/test_format_detection.py
tests/collector/document_admission/test_security_dispositions.py
tests/collector/document_admission/test_resource_limits.py
tests/collector/document_admission/test_inspection_results.py
tests/collector/document_admission/test_admission_orchestration.py
tests/collector/document_admission/test_failure_and_retry.py
tests/collector/document_admission/test_cleanup.py
tests/collector/document_admission/test_package_boundaries.py
```

It may modify only documentation that becomes inaccurate because the candidate
exists, expected initially:

```text
CHANGELOG.md
CURRENT_SPRINT.md
PROJECT_STATUS.md
README.md
docs/ARCHITECTURE.md
docs/KNOWLEDGE_MANAGER_1_PHASE_2_DOCUMENT_INSPECTION_PLAN.md
docs/KNOWLEDGE_MANAGER_1_PHASE_2_VALIDATION_REQUIREMENTS.md
docs/README.md
docs/reference/COMPONENT_REGISTRY.md
```

No other path is authorized without a revised exact-head plan and review.
`pyproject.toml`, `uv.lock`, service, container, workflow, infrastructure,
existing Collector, registry, and memory paths are protected.

## Implementation completion criteria

The synthetic candidate is review-ready only when:

1. Every authorized file and no unauthorized file is present.
2. Exact models, fields, enum values, transitions, methods, and typed failures
   match this package.
3. Every constructor and operation fails closed on invalid or missing evidence.
4. Synthetic bytes are process-local, integrity checked, isolated from ordinary
   consumers, and removed under test policy.
5. Detector, evaluator, inspector, and eligibility behavior comes only from
   injected test doubles; no parser or isolation product is selected.
6. All targeted and full-suite tests pass deterministically.
7. Import, network, service, content, registry, memory, Qdrant, retrieval,
   runtime, deployment, dependency, and real-information negative checks pass.
8. Documentation states **Implemented repository candidate**, not Operational,
   deployed, live, safe for real documents, or ready for a pilot.
9. Rollback requires no migration or external cleanup.
10. Work Mode reviews the exact remote implementation head with no unresolved
    Blocking, High, or Medium finding.
11. The Chief Architect separately decides whether that exact implementation
    head may merge.

## Review and merge gates

This activation package follows:

```text
activation package
-> independent Work Mode architecture and security-quality review
-> Chief Architect exact-head authorization decision
-> controlled activation-package merge
-> bounded implementation
-> independent Work Mode implementation review
-> Chief Architect exact-head implementation merge decision
-> controlled implementation merge
-> Documentation Suite closeout
```

A changed head reopens the applicable review and decision gate. Acceptance of
this package authorizes neither implementation merge nor real information.

## Related records

- [Phase 2 Threat Model](KNOWLEDGE_MANAGER_1_PHASE_2_THREAT_MODEL.md)
- [Phase 2 Dependency Assessment](KNOWLEDGE_MANAGER_1_PHASE_2_DEPENDENCY_ASSESSMENT.md)
- [Proposed Phase 2 Implementation Authorization](governance/KNOWLEDGE_MANAGER_1_PHASE_2_IMPLEMENTATION_AUTHORIZATION.md)
- [ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
- [Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)

## Exact next decision

After one remote exact head exists and receives independent Work Mode review,
the Chief Architect must adopt or reject the proposed authorization record.
Until that exact decision and canonical merge, implementation remains
unauthorized.
