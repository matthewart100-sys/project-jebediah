# Collector 1.0 Specification

**Status:** Proposed

**Component maturity:** Defined candidate

**Implementation status:** Not authorized

**Last reviewed:** 2026-07-31

## Review warning

This document proposes the Collector 1.0 contract. It is not current runtime
architecture and does not authorize server, workflow, database, model, or
deployment changes.

## Responsibility

Collector 1.0 accepts one bounded text record, validates and normalizes its
contract fields, derives deterministic identity, preserves provenance, and
produces an idempotent storage request plus a structured result.

Collector 1.0 does not decide whether submitted content is true.

## Inputs

A Collector 1.0 request contains:

| Field | Required | Meaning |
| --- | --- | --- |
| `source_type` | Yes | Bounded source category, such as `manual`, `chat`, or `document` |
| `source_id` | Yes | Stable identifier assigned by the source or submitting adapter |
| `content` | Yes | UTF-8 plain text to collect |
| `observed_at` | Yes | Time the source content was observed |
| `submitted_at` | Yes | Time the Collector received the request |
| `revision` | Yes | Source revision or deterministic revision token |
| `metadata` | No | Bounded non-secret attributes permitted by policy |
| `correlation_id` | No | Request trace identifier; not part of record identity |

The initial contract accepts plain text only.

## Normalization

Normalization may:

- Validate UTF-8 text
- Normalize line endings to `LF`
- Trim transport-only leading or trailing whitespace
- Canonicalize approved field names
- Canonicalize timestamps to UTC RFC 3339 form
- Sort metadata keys for hashing

Normalization must not paraphrase, summarize, translate, correct, or otherwise
change the semantic content.

## Identity

The logical record key is derived from:

```text
source_type + source_id
```

The immutable revision identity is derived from:

```text
source_type + source_id + revision + normalized-content digest
```

The implementation must use a documented cryptographic digest. Identity must
not depend on an embedding vector, similarity score, database-generated ID,
current time, workflow execution ID, or model output.

## Duplicate and update behavior

Collector 1.0 distinguishes:

- **Exact retry:** Same logical key, revision, and content digest. Return the
  existing successful result without creating another record.
- **Revision update:** Same logical key with a new revision or changed content.
  Create or replace the approved current revision according to the storage
  adapter contract while retaining sufficient revision evidence for audit.
- **Identity conflict:** Same logical key and revision but different content.
  Reject as a conflict. Do not silently overwrite.
- **Semantically similar content:** Not a duplicate unless deterministic
  identity says it is the same logical source record.

## Provenance

Every accepted record must preserve:

- Source type
- Source identifier
- Source revision
- Observation time
- Submission time
- Normalized-content digest
- Collector contract version
- Adapter identity
- Processing result
- Storage identity
- Embedding model identifier when an embedding is produced

Provenance must be queryable without reconstructing it from logs.

## Validation

The Collector rejects requests when:

- A required field is missing
- Content is empty after allowed normalization
- A timestamp is invalid
- A source type is unsupported
- A source identifier or revision violates bounded format rules
- Metadata exceeds allowed keys, sizes, or classifications
- The same logical key and revision conflicts with different content
- Required downstream guarantees cannot be met safely

Validation fails closed.

## Storage boundary

The Collector contract produces a storage request containing:

- Deterministic record and revision identities
- Normalized content or an approved content reference
- Provenance payload
- Optional embedding vector
- Contract and schema versions

Qdrant is a proposed vector-search adapter. It is not the authoritative source
of the original external information merely because it stores a payload.

A future implementation must document whether normalized text is stored in
Qdrant, another durable store, or both before deployment.

## Embedding boundary

Embedding is optional from the component-contract perspective.

When enabled:

- Embedding occurs only after validation and identity derivation.
- Model name and version are recorded.
- Embedding failure must not be reported as successful collection.
- A model change must not alter logical source identity.
- Re-embedding is a derived-data operation, not a new source revision.
- Raw content must never be inferred from the vector.

Ollama is a proposed local embedding adapter, not a permanent contract
dependency.

## Results

A successful result includes:

- `status`
- `record_id`
- `revision_id`
- `operation` with one of `created`, `updated`, or `unchanged`
- `stored_at`
- `correlation_id` when supplied

A failure result includes:

- `status`
- Stable error code
- Safe human-readable message
- Retry classification
- `correlation_id` when supplied

Failure results must not expose secrets, credentials, private endpoints, stack
traces, or submitted sensitive content.

## Retry behavior

- Exact retries must be idempotent.
- Validation failures are not automatically retried.
- Conflicts require source or human resolution.
- Transient adapter failures may be retried with bounded attempts and backoff.
- Exhausted retries return a structured failure.
- A timed-out caller must be able to retry safely.

## Health and observability

Collector health must distinguish:

- Contract validation availability
- Embedding adapter availability
- Storage adapter availability
- Degraded operation
- Last successful collection time
- Error counts by stable category

Health must not expose submitted content, credentials, private addresses, or
sensitive topology.

## Security and privacy

Collector 1.0 must:

- Apply least privilege to each adapter
- Reject credentials and secrets in metadata fields
- Avoid logging full submitted content by default
- Use synthetic data in public tests
- Preserve source classification and deletion requirements when defined
- Avoid autonomous collection or action
- Require explicit configuration for allowed source types
- Fail safely when classification or authority is unknown

## Component boundaries

Collector 1.0 owns:

- Request validation
- Allowed normalization
- Deterministic identity
- Idempotency decision
- Provenance assembly
- Adapter orchestration
- Structured results

Submitting adapters own:

- Source access
- Authentication to the source
- Extraction from source-specific formats
- Stable source identifiers and revisions

Embedding adapters own:

- Conversion of approved text to a vector
- Model-specific request and response handling

Storage adapters own:

- Durable write semantics
- Database-specific schema and query mechanics
- Adapter health

Collector 1.0 does not depend on JCS.

## Acceptance tests

An implementation is conformant only when tests demonstrate:

1. A valid record is accepted.
2. Missing required fields are rejected.
3. Empty normalized content is rejected.
4. An exact retry returns `unchanged` without a second record.
5. A new revision produces `updated`.
6. Conflicting content for the same revision is rejected.
7. Semantically similar but differently identified sources remain distinct.
8. Embedding failure returns failure rather than false success.
9. Storage failure returns a retry-safe structured failure.
10. Model changes do not change logical record identity.
11. Logs and errors do not expose submitted content or secrets.
12. Health distinguishes healthy, degraded, and unavailable dependencies.
13. All public fixtures contain synthetic information.
14. No JCS dependency is required.

## Deferred decisions

Collector 1.0 does not yet select:

- Application language or framework
- Permanent embedding model
- Final Qdrant collection schema
- Permanent authoritative content store
- Public API protocol
- Deployment packaging
- Retention periods
- Data classifications for real information
- Multi-record transactions
- Binary or multimodal ingestion
- Autonomous source polling

These decisions require separate evidence and review.
