# Organizational Intelligence Validation Requirements

**Status:** Proposed

**Implementation state:** No implementation, live source, deployment, or
operational validation is authorized

## Purpose

This document defines the evidence required to review the organizational
intelligence interface and governed document-ingestion proposal. It also
defines future implementation gates without claiming that the prerequisites
have been accepted.

## Governing proposals

- [Organizational Intelligence Interface Specification](ORGANIZATIONAL_INTELLIGENCE_INTERFACE_SPECIFICATION.md)
- [Organizational Document Ingestion Specification](ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
- [ADR 0011: Knowledge Vault Authority and Boundary Model](adr/0011-knowledge-vault-authority-and-boundary-model.md)
- [Proposed ADR 0012](adr/0012-executive-organizational-intelligence-interface-boundary.md)
- [Proposed ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
- [Data Ownership](DATA_OWNERSHIP.md)
- [Security Policy](../SECURITY.md)

Proposed documents are not authoritative implementation contracts until the
required review and acceptance are recorded.

## Documentation-only proposal gate

Before architecture review, the actual proposal diff must prove:

- The interface answers the four executive questions with evidence, freshness,
  uncertainty, and degraded behavior.
- The interface is read-only and cannot ingest sources, mutate authoritative
  information, or execute external actions.
- Direct facts, reported facts, assumptions, open questions, derived
  summaries, and action candidates remain distinguishable.
- PDF, DOCX, TXT, and Markdown submission contracts are bounded and treat
  content as untrusted.
- Source identity, content identity, provenance, time semantics, validation,
  processing state, and transformation lineage are explicit.
- Admission never implies factual verification or downstream authorization.
- Quarantined, rejected, failed, stale, unauthorized, and partial states cannot
  become ordinary success.
- Original sources retain domain authority and derived representations remain
  non-authoritative.
- Technology selection, live information use, implementation, deployment, and
  external action remain unauthorized.
- Open questions have an owner or resolution gate and block affected work.

The proposal branch runs:

```text
python scripts/validate_docs.py
git diff --check
```

New Markdown files must also be included in the validator's direct file and
sensitive-value checks until tracked by Git.

## Required review sequence

1. Work Mode reviews the actual exact-head architecture package and may block
   on findings.
2. The Chief Architect accepts, rejects, or requires revision of the exact
   proposal head.
3. The accepted proposal is merged through the controlled workflow.
4. The Chief Architect separately authorizes a bounded implementation sprint.
5. Codex implements only that scope with synthetic information unless live use
   is separately approved.
6. Work Mode reviews the exact implementation artifacts.
7. The Chief Architect decides whether the implementation may merge.

Architecture acceptance does not authorize live source use, deployment, or an
organizational pilot.

## Future implementation baseline

Before implementation changes, record:

- Exact accepted base commit and approved sprint scope
- Accepted ADRs, component ownership, and interface responsibilities
- Approved information domains, producers, consumers, intended uses,
  classification, retention, deletion, and freshness rules
- Existing Collector, memory, Qdrant, embedding, and service contracts that
  must remain compatible
- Complete passing test count and relevant build/import evidence
- Synthetic fixture inventory and assurance that no live organizational
  content entered the repository
- Approved threat model, parser limits, failure taxonomy, and recovery design

Missing baseline evidence stops dependent implementation.

## Document admission contract tests

Synthetic tests must cover each candidate format and prove:

- Extension and supplied media type cannot override detected format.
- Unsupported, malformed, encrypted, active, oversized, deeply nested, or
  resource-unsafe input follows the approved quarantine or rejection policy.
- TXT and Markdown encoding errors and configured resource limits fail
  visibly.
- PDF parsing never executes scripts, actions, links, attachments, or embedded
  content; scanned-image files do not imply successful text extraction.
- DOCX parsing enforces package, decompression, entry, relationship, and path
  safety and never executes or fetches embedded or external content.
- Every attempt receives a stable submission identifier.
- Content identity is deterministic under the accepted digest contract.
- Identical bytes submitted twice preserve two occurrences without duplicating
  authority.
- A changed byte changes content identity even when the name is unchanged.
- Display names and source locators are sanitized and never used as filesystem
  authority.

## Provenance and time tests

Tests must prove:

- Source, submission, content, processing-attempt, and derived-output
  identifiers remain distinct and traceable.
- `submitted_at`, source times, `admitted_at`, processing times, and transition
  times preserve their documented meanings.
- Unknown or ambiguous source time remains unknown or ambiguous.
- System times are timezone-aware and use the accepted UTC representation.
- Every derived output identifies its exact input content and transformation
  identity.
- Model-derived output, if later authorized, records model and policy identity
  and remains derived.
- Provenance is not interpreted as verification or truth.

## State, retry, and failure tests

Tests must prove:

- Only documented admission-state transitions are accepted.
- Transition history is append-only and includes actor, time, reason, and
  correlation evidence.
- Rejected, failed, partial, or quarantined work cannot appear as `ready`.
- A retry creates a new linked attempt and does not rewrite prior evidence.
- Unknown durable outcomes are reconciled before retry.
- Partial extraction retains warnings and omissions.
- A failed transformation does not delete the admitted source record or expose
  partial output to ordinary retrieval.
- Rate, cost, resource, and authorization controls are not bypassed by retry.

## Knowledge and retrieval tests

Tests must prove:

- Source snapshots, extracted text, derived knowledge records, embeddings, and
  indexes retain separate identities and categories.
- Only outputs with an approved domain, intended use, lifecycle, validation,
  and classification become eligible for ordinary retrieval.
- Quarantined, rejected, failed, superseded, archived, deleted, and
  unauthorized material is excluded.
- Index entries point to eligible records and can be rebuilt without becoming
  authoritative.
- A transformation change creates a new version or follows an approved
  migration.
- Deletion or correction propagates according to the approved ownership and
  retention policy.

No live Qdrant, source, migration, or deletion test is authorized until a
separate approved test environment and information policy exist.

## Executive read-model contract tests

Synthetic contract tests must prove:

- Every item belongs to exactly one of the four executive sections.
- Every claim exposes its evidence classification, safe source references,
  time, freshness, confidence basis, lifecycle, transformation identity when
  derived, and limitations.
- Missing evidence remains missing and cannot be replaced with fabricated
  defaults.
- Conflicting facts remain visible under an approved reconciliation policy.
- Empty results state their coverage and do not claim nothing is happening.
- Partial, stale, insufficient-evidence, unauthorized, and unavailable states
  are distinguishable.
- Attention ranking exposes its rule and cannot grant action authority.
- Next-step items identify whether they navigate, request review, draft, or
  require a separately governed action.
- A failed refresh cannot overwrite a usable last-known view with false empty
  success.

## Generated-assistance tests

If generated assistance is later included, evaluation must prove:

- Only eligible context is provided to the model.
- Retrieved instructions, active content, and prompt-injection attempts remain
  inert data.
- Supported claims cite the correct read-model evidence.
- Insufficient evidence produces an explicit bounded response.
- The model cannot change verification, lifecycle, priority, or action
  authority.
- Model unavailability leaves deterministic briefing evidence usable.
- Generated output is labeled and stored, if stored at all, as derived under
  an approved retention policy.
- Privacy, security, quality, latency, and cost thresholds are defined before
  acceptance.

The test set must include ordinary, conflicting, stale, incomplete, malicious,
and no-evidence cases. Passing examples alone are insufficient.

## Accessibility and usability validation

The first interface implementation must demonstrate:

- Complete keyboard use and visible focus
- Programmatic structure and meaningful accessible names
- Sufficient contrast, text resizing, and non-color status cues
- Clear form, authorization, stale-data, and service error identification
- Plain-language summaries with evidence through progressive disclosure
- Unambiguous dates, times, timezones, and freshness states
- Usability review with representative nonprofit-executive tasks using only
  synthetic or explicitly authorized information

The evaluation measures whether users can answer the four questions and locate
the supporting evidence, not visual preference alone.

## Security and privacy validation

Before live use, evidence must cover:

- Authentication, authorization, least privilege, and access revocation
- Information classification through submission, derivation, retrieval,
  presentation, logs, analytics, exports, backups, and deletion
- Parser and renderer isolation, dependency review, and resource limits
- Malicious documents, path traversal, decompression abuse, active content,
  external fetching, injection, and denial-of-service cases
- Sanitized errors, logs, metrics, citations, and source references
- Secret storage and rotation outside the repository and document content
- Retention, correction, deletion, backup, restore, and legal-handling evidence

Sensitive test evidence may remain in an approved private channel, but the
repository records sanitized conclusions and owners.

## Operations and recovery validation

An implementation cannot be called deployable until it proves:

- Named component and operational owners
- Health, metrics, sanitized logs, alert thresholds, and support procedures
- Bounded capacity, timeout, retry, and backpressure behavior
- Backup, restore, reconciliation, migration, and rollback
- Recovery that preserves quarantine and ordinary-retrieval separation
- Last-known-view and stale-state behavior during dependency failure
- Rebuild of derived indexes from eligible records
- No deployment dependence on private addresses or manual unrecorded state

## Future implementation validation commands

The accepted sprint must define exact commands. At minimum, the implementation
branch is expected to run:

```text
uv --system-certs run --frozen pytest -q
uv --system-certs run --frozen python -m compileall -q src services tests
python scripts/validate_docs.py
uv --system-certs lock --check
git diff --check
```

Additional frontend, accessibility, dependency, package, container, security,
and integration checks depend on the later accepted technology and deployment
decisions.

## Stop conditions

Stop dependent work when:

- Any required ADR is Proposed, rejected, superseded, or missing.
- No implementation sprint is explicitly authorized.
- Information ownership, intended use, classification, retention, deletion,
  or consumer authorization is unresolved for the proposed live scope.
- A source, parser, transformation, or model boundary would be invented to fill
  a documentation gap.
- Quarantined or failed content can reach ordinary retrieval.
- Provenance, timestamps, lifecycle, or transformation identity can be lost.
- A derived result can overwrite or impersonate an authoritative source.
- Partial, stale, conflicting, or unavailable information can appear as
  complete current success.
- The executive interface can perform an external action without a separate
  authority decision.
- Secrets, personal data, private locators, or real organizational content
  would enter public repository or review artifacts.

## Evidence report

Every handoff records:

- Exact branch and commit
- Reviewed base and actual diff
- Commands, exit results, test counts, and skipped evidence
- Synthetic or approved data boundary
- ADR and sprint authorization state
- Security, privacy, accessibility, operations, and recovery conclusions
- Known limitations, open questions, and the next authorized decision
- Whether implementation, deployment, live information use, and external
  action remain unauthorized
