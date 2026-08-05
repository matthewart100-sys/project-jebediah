# ADR 0013: Governed Organizational Document Admission Boundary

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-04

**Decision owner:** Chief Architect

**Reviewers:** Work Mode architecture review, then Chief Architect final review

## Decision summary

Extend the Collector boundary conceptually with a quarantine-first document
admission pipeline for PDF, DOCX, TXT, and Markdown submissions. Preserve
source and content identity, provenance, time, validation, state, and
transformation lineage while keeping every derived output non-authoritative
for the source facts.

## Context

The existing Collector implementation candidate accepts bounded TXT and
Markdown records. The requested organizational-intelligence foundation needs
additional document families and visible processing state. The repository has
no accepted contract for binary document admission, retention, parser
isolation, transformation lineage, or Knowledge Vault ingestion.

Implementing parsers or upload routes first would decide security, authority,
state, retention, and recovery through code. ADR 0011 proposes that the
Knowledge Vault govern derived representations only, but it is not accepted
and does not authorize information acquisition or use.

### Verified facts

- The Collector file adapter currently supports `.txt` and `.md` input only.
- The Collector candidate already separates validation, identity, provenance,
  normalization, and persistence responsibilities for bounded text records.
- Reviewed `main` contains no PDF or DOCX parser, upload lifecycle, quarantine
  store, Knowledge Vault implementation, or live source authorization.
- ADR 0011 is Proposed and the Knowledge Vault remains **Named**.
- No active sprint or external information use is authorized.

### Reported facts

- The implementation directive identifies PDF, DOCX, TXT, and Markdown as the
  initial required document families.
- No representative live document inventory or information-owner approval has
  been supplied as repository evidence.

### Working assumptions

- Extending the Collector responsibility is more coherent than introducing an
  unnamed ingestion service. The component decision must be confirmed before
  implementation.
- Synthetic fixtures can validate format and state contracts without using
  organizational information.

### Open questions

- The first source domain, authority, producer, submitter, consumer, intended
  use, classification, retention, deletion, and operational owner are unknown.
- Required malware controls, parser isolation, persistence, transport,
  scanning, and recovery mechanisms are undecided.

These questions block affected implementation and live use. The admission and
authority boundary can still be reviewed independently of technology.

## Scope

- Admission responsibility for PDF, DOCX, TXT, and Markdown submissions
- Submission and content identity, provenance, time, validation, state, retry,
  and transformation lineage
- Quarantine and ordinary-retrieval eligibility
- Authority separation among original sources, submitted snapshots, derived
  knowledge, and indexes

## Non-goals

- Parser, storage, queue, API, model, vector, or deployment selection
- OCR, spreadsheets, presentations, email, archives, images, audio, executable
  formats, or macro-enabled documents
- Live organizational information authorization
- Factual verification, knowledge significance, or action authority
- Records-management, legal-hold, external publication, or editing workflows

## Decision drivers

- Untrusted document content must not reach ordinary retrieval before bounded
  admission checks.
- Source and derived identities must remain traceable and distinct.
- Processing and failure state must be auditable without implying truth.
- Duplicate receipt, retry, partial extraction, deletion, and recovery need
  explicit semantics.
- The design must preserve ADR 0011's proposed non-authoritative derived-
  knowledge boundary.
- Implementation technology must remain open until source and threat evidence
  are approved.

## Considered alternatives

### Add parsers to the existing file adapter

The simplest code change would add PDF and DOCX branches beside current text
reading. This hides quarantine, byte limits, active-content handling, state,
retention, and transformation lineage inside one adapter and cannot support a
governed organizational submission boundary.

### Let the Knowledge Vault receive documents directly

A future Knowledge Vault could accept and transform source documents itself.
This collapses acquisition, admission, knowledge derivation, and retrieval and
risks granting the derived repository implicit source authority.

### Quarantine-first Collector admission with separate transformation

The Collector can own the untrusted-input boundary and emit only admitted
source representations to separately approved consumers. This preserves
existing responsibility direction and makes the transition to derived
knowledge reviewable.

### Retain the current design

The project could continue to support only bounded TXT and Markdown records.
This avoids binary parser risk but does not satisfy the stated PDF and DOCX
foundation and leaves processing-state semantics undefined.

## Decision

Select a quarantine-first document-admission responsibility within the
Collector boundary for PDF, DOCX, TXT, and Markdown candidates.

Every attempt receives a stable submission identity. A versioned cryptographic
digest identifies exact content; supplied names and media types remain
untrusted metadata. Repeated equal content preserves distinct submission
occurrences. Changed content creates a new content identity.

The minimum state vocabulary is `received`, `quarantined`, `validating`,
`accepted`, `rejected`, `processing`, `ready`, and `failed`. Transitions are
append-only and record prior state, next state, time, actor or component,
reason, and correlation. Reprocessing creates a linked attempt rather than
rewriting history.

Admission evaluates approved source and use authorization, envelope, detected
format, integrity, classification, resource limits, active content, duplicate
policy, and required provenance. `accepted` means admissible for one approved
use; it never means factually verified, current, or eligible for every
consumer.

Every transformation identifies its exact input content, versioned behavior,
times, outputs, omissions, and failure. Extracted text, chunks, summaries,
entities, relationships, embeddings, and indexes are derived. They cannot
overwrite or impersonate the original source or admitted submission record.

Only `ready` outputs that also satisfy the approved domain, intended use,
classification, lifecycle, retention, and consumer policy may reach ordinary
retrieval. Quarantined, rejected, failed, partial, unauthorized, superseded,
archived, or deleted content is excluded.

The decision defines no parser, persistence, interface, model, scanning, or
deployment mechanism. Those choices require accepted prerequisites and
separate review.

## Consequences

### Positive

- Unsafe input is isolated before parsing and ordinary retrieval.
- Source, submission, processing, derivation, and index identities remain
  traceable.
- Admission, factual truth, knowledge derivation, and consumer eligibility are
  not conflated.
- Duplicate and retry behavior can be deterministic and audited.
- Parser and storage technologies remain replaceable.

### Negative

- Quarantine, transition history, lineage, and recovery require durable
  operational design.
- PDF and DOCX handling adds a substantial parser and resource-exhaustion
  threat surface.
- Information-owner, retention, deletion, and operational decisions are
  prerequisites rather than implementation follow-ups.
- A useful pipeline has more visible failure and partial states than a direct
  text-extraction script.

### Neutral

- The content digest identifies submitted bytes, not document meaning or
  factual truth.
- The same admitted content may have multiple separately versioned derived
  representations.

## Data and provenance impact

Original sources retain authority within approved domains. Submitted bytes are
cached evidentiary snapshots or temporary quarantine material under a later
retention decision. Admission records are operational records. Extracted
content, knowledge records, embeddings, and indexes are derived.

Every derived record keeps the submission and content identity plus the
transformation identity. Source, submission, admission, processing, and state
transition times retain distinct semantics.

Correction and deletion must propagate under an approved information-owner
policy without rewriting audit history or leaving ordinary retrieval entries
that point to ineligible material.

## Security and privacy impact

This decision introduces a high-risk untrusted-document boundary. Threat
review must address malicious structure, parser defects, decompression abuse,
path traversal, active content, external fetching, prompt injection, denial of
service, temporary files, logs, and sensitive-content leakage.

Tests use synthetic fixtures. No live document, personal data, private
locator, credential, or exploitable topology enters the public repository.
Runtime access later follows least privilege and approved secret handling.

## Operations and recovery impact

The implementation design must assign ownership for quarantine, state
transitions, capacity, backpressure, timeouts, retries, sanitized observability,
backup, restore, reconciliation, migration, and rollback. Recovery must
preserve the separation between quarantine and ordinary retrieval.

An unknown durable outcome is reconciled before retry. A failed transformation
cannot erase the admitted source record or make a partial output ready. Derived
indexes must be rebuildable from eligible records.

## Compatibility and migration

The existing bounded text-record contract and memory APIs remain unchanged by
this proposal. Later implementation must characterize and preserve accepted
Collector behavior or explicitly version a new document-submission contract.

No live binary-document consumer or stored organizational dataset exists in
reviewed repository evidence, so no data migration is authorized. Future
migration requires an accepted source, retention, backup, validation, cutover,
and rollback plan.

## Validation

The proposal is validated by the
[Organizational Intelligence Validation Requirements](../ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md).
Synthetic implementation tests must cover format detection, malformed and
resource-unsafe inputs, identity, provenance, time, state transitions,
duplicates, retry, partial failure, derivation lineage, retrieval exclusion,
deletion, and recovery.

Reconsider the Collector placement if an accepted source inventory proves that
the responsibility requires an independently operated trust or scaling
boundary.

## Follow-up work

- Approve the first domain, source authority, producer, submitter, consumer,
  use, classification, retention, and deletion policy.
- Complete the parser and processing threat review.
- Specify component ownership, persistence, interface, operations, and
  recovery.
- Choose parser and processing technologies only after the preceding gates.
- Define a bounded implementation sprint using synthetic information first.

## Related documents

- [Organizational Document Ingestion Specification](../ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
- [Organizational Intelligence Validation Requirements](../ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md)
- [Collector 1.0 Specification](../COLLECTOR_1_SPECIFICATION.md)
- [Current Architecture](../ARCHITECTURE.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md)
- [Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

No review decision has been recorded. Work Mode must review the exact proposal
head before the Chief Architect accepts, rejects, or requires revisions.
