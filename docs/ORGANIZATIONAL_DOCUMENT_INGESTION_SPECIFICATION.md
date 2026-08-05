# Organizational Document Ingestion Specification

**Status:** Proposed

**Maturity:** Review target only; no implementation, source use, or deployment
authorized

## Purpose

This specification defines a governed foundation for receiving PDF, DOCX, TXT,
and Markdown submissions and producing traceable derived knowledge inputs. It
extends the Collector responsibility conceptually without authorizing code,
parser dependencies, persistence, live organizational documents, or ordinary
retrieval.

Original sources retain their domain authority. A submitted copy, extracted
text, chunk, summary, embedding, index entry, or knowledge record is not made
authoritative by processing or storage.

## Intended outcome

An authorized submission can be traced from receipt through quarantine,
validation, admission, processing, and derived outputs. The system preserves
source identity, content identity, provenance, time semantics, validation
results, processing state, and transformation lineage. Unsafe or unauthorized
content remains unavailable to ordinary consumers.

## Scope

This proposal governs:

- Candidate PDF, DOCX, TXT, and Markdown submissions
- Admission-state semantics and append-only transition evidence
- Source identity, content identity, provenance, timestamps, validation, and
  processing metadata
- Separation of submitted artifacts, extracted representations, derived
  knowledge, semantic indexes, and authoritative sources
- Duplicate, retry, failure, quarantine, and ordinary-retrieval eligibility
- Security, privacy, retention, and recovery requirements that must be
  resolved before implementation or live use

## Non-goals

This proposal does not:

- Select parser libraries, object storage, database schemas, queues, APIs,
  OCR, embedding models, vector stores, chunking strategies, or deployment
  topology
- Authorize any information domain, producer, submitter, consumer, or live
  organizational document
- Establish the truth of a document or its claims
- Make the Knowledge Vault authoritative for source facts
- Support spreadsheets, presentations, email, archives, images, audio,
  executable formats, macro-enabled office formats, or scanned-document OCR
- Define document editing, records management, legal hold, e-discovery, or
  external publication
- Permit prompt instructions, scripts, links, macros, or embedded objects to
  execute

## Responsibility boundary

The existing Collector Engine remains the proposed admission owner. It may
receive untrusted bytes, validate the submission envelope and detected format,
derive deterministic identities, record provenance, and emit an admitted
source representation for a separately approved transformation consumer.

The Collector does not verify factual truth, grant information-domain
authority, choose knowledge significance, or expose quarantined material to
ordinary retrieval. If ADR 0011 is accepted, the Knowledge Vault may govern
eligible derived representations and lineage; it does not own the original
source facts.

## Information classes

| Information | Category | Authority and use |
| --- | --- | --- |
| Original source in its originating system | Authoritative within its approved domain, when so designated | Remains the fact authority under the source-domain contract |
| Submitted byte stream | Cached evidentiary snapshot or temporary quarantine material, as later approved | Proves what was submitted; does not replace the originating source |
| Submission and admission record | Operational record | Owns processing identity, state transitions, and validation evidence |
| Extracted text and structure | Derived information | Traceable to the submitted content and extractor identity |
| Chunk, summary, entity, relationship, or embedding | Derived information | Eligible only for separately approved uses with complete lineage |
| Search or vector index entry | Rebuildable derived index | Never a source of truth; must point to an eligible derived record |
| Logs and temporary work files | Temporary operational information | Minimized, sanitized, bounded, and removed under an approved policy |

The final authoritative, cached, derived, and temporary classification for an
initial domain requires information-owner approval before live use.

## Submission envelope

Every attempt receives a stable submission identifier before processing. The
envelope records at least:

- Submission identifier
- Approved source-domain and intended-use identifiers
- Producer and submitter references appropriate to the approved privacy model
- Supplied display name, normalized safe name, and claimed media type
- Detected format and detected media type
- Byte size and a versioned cryptographic content digest
- Source-system reference or locator when available and safe to retain
- Source record identifier and source version when available
- Submission time assigned by the receiving system
- Claimed or extracted source-creation and source-modification times, with
  their evidence basis
- Current admission state and append-only transition history
- Validation findings and sanitized reason codes
- Transformation attempts and output identifiers
- Classification, retention, access, and legal-handling references when
  applicable

The display name is metadata, not identity. Two submissions with equal content
digests remain distinct submission occurrences while sharing a content
identity. A changed digest is a new content version even when the display name
is unchanged.

## Time semantics

The contract distinguishes:

- `submitted_at`: when the receiving boundary accepted the attempt
- `source_created_at`: when the source claims the document was created, when
  known
- `source_modified_at`: when the source claims the version changed, when
  known
- `admitted_at`: when admission validation completed successfully
- `processing_started_at`: when a transformation attempt began
- `processed_at`: when that attempt reached a terminal outcome
- `state_changed_at`: when each recorded transition occurred

System-assigned times use UTC and a timezone-aware representation. Source times
retain their supplied timezone and evidence basis when available. Unknown,
ambiguous, or untrusted source time remains labeled as such; the system must not
replace it with submission time.

## Candidate format contracts

Extension and supplied media type are hints only. Acceptance requires format
detection and structural validation.

### TXT and Markdown

- Require a documented text encoding policy and visible rejection of invalid
  byte sequences.
- Enforce byte, character, line, and structural limits before expensive
  transformations.
- Treat links, inline HTML, directives, and model-like instructions as inert
  content.
- Preserve enough location information to cite a line or bounded text span
  when the approved transformation can do so reliably.

### PDF

- Validate the file signature and parseable structure under bounded resource
  limits.
- Treat scripts, actions, forms, attachments, links, fonts, and embedded
  content as untrusted and non-executable.
- Record whether usable text exists and whether extraction is partial.
- Reject or quarantine encrypted, malformed, unsupported, or resource-unsafe
  documents under the approved policy.
- Scanned-image OCR is outside the first scope and cannot be silently implied.

### DOCX

- Validate the Office Open XML package and required document relationships
  under bounded decompression and entry limits.
- Reject or quarantine macro-enabled, encrypted, malformed, path-traversal,
  externally linked, or resource-unsafe content under the approved policy.
- Treat fields, links, alternate chunks, embedded objects, comments, tracked
  changes, and instructions as untrusted data.
- Record material omissions when the approved extractor cannot represent part
  of the source faithfully.

## Admission state model

The minimum state vocabulary is:

| State | Meaning |
| --- | --- |
| `received` | The envelope and stable submission identifier exist |
| `quarantined` | Content is isolated from ordinary consumers pending checks |
| `validating` | Authorization, envelope, format, integrity, limits, and policy checks are running |
| `accepted` | Admission checks passed for the approved intended use; truth is not verified |
| `rejected` | Admission ended with a permanent policy or validation failure |
| `processing` | An approved transformation attempt is running on accepted input |
| `ready` | Required derived outputs completed and passed eligibility checks |
| `failed` | Processing ended without a ready output; the source is not silently rejected or ready |

The ordinary forward path is:

```text
received -> quarantined -> validating -> accepted -> processing -> ready
                                  |                       |
                                  v                       v
                               rejected                 failed
```

Every transition records prior state, next state, time, actor or component,
reason code, and correlation identifier. History is append-only. Reprocessing
creates a new attempt linked to the accepted submission; it does not rewrite a
failed attempt or move a terminal state backward.

`accepted` means admissible for one approved use. It does not mean verified,
accurate, current, safe for every consumer, or eligible for generation.

## Admission validation

Admission must fail closed unless it can establish:

- Source-domain, producer, submitter, consumer, and intended-use authorization
- Allowed classification and retention handling
- Supported detected format and consistent submission envelope
- Size, structure, nesting, decompression, and resource limits
- Content digest and byte integrity
- Required source identity and provenance fields
- Safe filename and path handling
- Malware and active-content disposition required by the approved threat model
- Duplicate and replay disposition
- Sanitized, stable failure classification

Validation results are evidence about admissibility and processing, not proof
that document claims are true.

## Processing and derivation

Each transformation attempt records:

- Input submission and exact content identity
- Transformation name, version, configuration identity, and code or artifact
  identity when reproducibility requires it
- Start, completion, failure, and retry times
- Output identifiers and content identities
- Material omissions, warnings, partial extraction, and limits reached
- Model identity and prompt or policy identity when a model is separately
  authorized
- The eligibility decision for each downstream consumer

Derived outputs cannot overwrite the submitted source record. A changed
extractor, chunker, model, policy, or configuration creates new derived
versions or follows an approved migration. Semantic indexes are rebuilt from
eligible derived records and never used to reconstruct missing authority.

## Duplicate, retry, and partial failure behavior

- Repeated receipt of identical bytes creates a traceable submission
  occurrence and may reuse an eligible content result only under an approved
  policy with matching transformation identity.
- A retry is safe only when the prior attempt outcome is known or a
  reconciliation check resolves an unknown outcome.
- Partial extraction is never reported as complete; its omissions remain
  visible to downstream consumers.
- A processing failure does not erase the admitted source record or expose a
  partial output as ready.
- No automatic retry may bypass authorization, quarantine, rate, cost, or
  resource controls.

## Security and privacy

The receiving boundary treats every byte and metadata field as untrusted.
Before implementation, the threat review must cover malicious document
structure, archive expansion, path traversal, parser vulnerabilities, active
content, prompt injection, external-resource fetching, denial of service,
sensitive-content leakage, logging, temporary files, and parser isolation.

The public repository contains no real organizational document, personal data,
private locator, credential, raw sensitive finding, or exploitable topology.
Tests use synthetic fixtures. Live credentials and source access remain in an
approved secret boundary with least privilege.

## Retention, deletion, and recovery

Implementation cannot begin for live information until an approved policy
defines retention and deletion for submitted bytes, envelopes, validation
records, extracted content, derived records, indexes, logs, and backups. A
request to delete or correct an authoritative source must propagate to cached
and derived material under documented authority and audit rules.

The selected persistence design must prove backup, restore, migration,
reconciliation, and rollback behavior. Quarantine must survive a recoverable
failure without becoming ordinary retrieval content. Rebuilding an index must
not change source or derivation identity.

## Interface boundary

Future interfaces must keep submission, status inspection, admitted-source
reading, transformation, derived-record reading, and ordinary retrieval as
distinct responsibilities. A convenient endpoint or queue must not collapse
these authority boundaries.

Concrete API paths, schemas, queue semantics, and storage contracts require
separate reviewed decisions. The executive interface consumes only eligible
read-model items and never calls a document parser directly.

## Dependencies and authorization gates

Implementation waits for:

1. Acceptance of ADR 0011 or an approved replacement
2. Acceptance of Proposed ADR 0013
3. Approval of one bounded information domain, original authority, producer,
   submitter, consumer, intended use, classification, retention, and deletion
   policy
4. A component contract assigning operational ownership and recovery
5. Parser and processing threat review with explicit resource limits
6. Technology and interface decisions required by the accepted architecture
7. Work Mode architecture review, Chief Architect acceptance, proposal merge,
   and separate sprint authorization

## Acceptance criteria for this specification

The proposal is review-ready when:

- PDF, DOCX, TXT, and Markdown have bounded candidate format contracts.
- Submission identity and content identity cannot be confused.
- Provenance and source, submission, admission, processing, and transition
  times have distinct semantics.
- State transitions are auditable and cannot make partial or failed work ready.
- Admission, fact verification, derivation, indexing, retrieval, and authority
  remain separate.
- Duplicate, retry, active-content, privacy, retention, deletion, and recovery
  requirements are explicit.
- Derived knowledge cannot silently become authoritative or ordinary
  retrieval content.
- No parser, persistence technology, live source, or deployment is authorized.

## Open questions

| Question | Owner or gate |
| --- | --- |
| Which information domain and document set may be the first pilot? | Chief Architect and information-owner approval |
| Must submitted bytes be durably retained, and for how long? | Information owner, legal/privacy review, and persistence decision |
| Which content scanning and parser-isolation controls are required? | Security threat review |
| Which source metadata is authoritative versus submitter-supplied? | Source-domain contract |
| How are corrections, deletion, and legal holds propagated? | Information-owner and retention policy |
| Which transformation outputs are needed by the first consumer? | Accepted consumer and component specifications |

These questions block affected implementation and live use but do not prevent
review of the proposed admission and authority boundaries.

## Related documents

- [Collector 1.0 Specification](COLLECTOR_1_SPECIFICATION.md)
- [Current Architecture](ARCHITECTURE.md)
- [Data Ownership](DATA_OWNERSHIP.md)
- [Organizational Intelligence Interface Specification](ORGANIZATIONAL_INTELLIGENCE_INTERFACE_SPECIFICATION.md)
- [Organizational Intelligence Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md)
- [ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md)
- [Proposed ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
