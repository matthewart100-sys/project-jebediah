# ADR 0016: Local Governed PDF Intake and Custody Boundary

**Status:** Accepted

**Decision level:** System

**Date:** 2026-08-05

**Decision owner:** Chief Architect

**Required reviewers:** Independent Work Mode architecture review, then Chief
Architect final decision

**Adopted architecture head:** `bfa18ab35ae1bcd0cf6a91090dba62ab9220076a`

**Chief Architect decision:** Adopted on 2026-08-05 in pull request #58;
status activation only

**Authority boundary:** Implementation, architecture merge, deployment, and real
organizational document use remain unauthorized

## Decision summary

Refine ADR 0013 into one local, loopback-only, single-operator PDF admission and
human-review component for the Virginia B. Andes board-governance roster domain.
Use a signed single-use authorization receipt, browser-pushed bytes, encrypted
local custody, SQLite metadata, isolated offline scanner/native/OCR workers, and
explicit human review.

Phase 3B produces reviewable Source Document Evidence candidates only. It does
not create governed Knowledge Objects, memory, embeddings, Qdrant indexes,
retrieval, grounded answers, action, deployment, or real-source authority.

## ADR trigger and level

ADR 0013 intentionally deferred interface, persistence, encryption, identity,
parser, scanner, OCR, isolation, retention, deletion, legal hold, backup,
recovery, and operational choices. Phase 3B cannot implement durable real-
document capability without selecting them.

This is a System decision because it establishes security and authority
boundaries, a durable data model, a browser input contract, critical
dependencies, worker isolation, lifecycle rules, and recovery strategy.

## Context

### Verified facts

- ADR 0013 accepts quarantine-first admission and a pushed submission envelope;
  supplied names/media types are untrusted metadata.
- The implemented Phase 2 package is disconnected, in-memory, synthetic, and
  non-operational.
- The Executive Product Shell is loopback-only and synthetic, with no input or
  persistence.
- No parser, scanner, OCR engine, durable quarantine, live source, information
  owner, deployment, or operator is accepted.
- The project Python baseline is 3.12 or newer and uses `uv.lock`.

### Reported target

The presentation program needs a future exact authorized non-clinical Virginia
B. Andes board-roster PDF to become human-reviewable evidence before Phase 3C
may derive governed knowledge.

### Working assumptions

- One local operator and one PDF minimize the first risk surface.
- A browser push can preserve the ADR 0013 submission envelope without giving
  the server a filesystem source locator.
- Rootless Linux OCI workers can bound parser/scanner/OCR compromise better than
  host subprocesses.
- The initial board roster can be treated as internal governance information
  with limited personal data unless the information owner supplies a stricter
  classification.

### Open gates, not design gaps

- exact real file, digest, source authority, role holders, and environment;
- passphrase/recovery custody;
- scanner signatures and built image digests;
- private information-owner/legal approval; and
- deployment or any Phase 3C/3D consumer.

These gates block live use, not synthetic implementation.

## Scope

- one organization/domain and one authorized local operator;
- PDF only;
- signed receipt and browser-pushed bytes;
- encrypted durable source and inspection custody;
- SQLite state/audit metadata;
- ClamAV scan, qpdf structural validation, `pypdf` native extraction, and
  Poppler/Tesseract OCR fallback;
- rootless Podman worker isolation;
- explicit retention, deletion, legal-hold, backup, restore, and reconciliation;
- Human Review Workspace integration; and
- generated synthetic implementation fixtures only.

## Non-goals

- DOCX, TXT, Markdown, archives, email, spreadsheet, presentation, audio, video,
  or arbitrary image intake;
- filesystem discovery or path-based acquisition;
- real VBA information under this architecture run;
- Knowledge Registry, Knowledge Object, memory, embedding, Qdrant, retrieval,
  model, grounded response, or action;
- remote/multi-user operation, identity provider, production deployment,
  unattended service, or availability promise;
- factual verification, records management, e-discovery, or public publication;
  and
- altering ADR 0013 state or authority semantics.

## Alternatives

### Path-based CLI acquisition

Rejected because it would reverse ADR 0013's pushed submission envelope and
grant the runtime active filesystem acquisition responsibility.

### Standard-library host parsing

Rejected because the standard library cannot safely parse PDF, scan malware,
perform OCR, or isolate untrusted native code.

### One combined worker

Rejected because scanner, native parser, and OCR compromise/resource profiles
are distinct. Separate workers reduce reachable tools and make fallback
explicit.

### Cloud scanning or OCR

Rejected because it exports organizational bytes and introduces accounts,
credentials, network, vendor retention, and legal decisions.

### Full multi-tenant intake service

Rejected as premature. It adds identity, remote transport, tenant isolation,
deployment, and operations before the one-document local boundary is proven.

### Defer durable custody until Phase 3C

Rejected because human review, retry, retention, deletion, and evidence lineage
cannot be reliable over process-local bytes.

## Decision

Adopt the exact design, limits, ownership, lifecycle, file manifest, validation,
and later real-source gate in the Phase 3B package.

The interface is a two-step pushed envelope:

1. verify and reserve a signed single-use authorization receipt; then
2. accept one bounded browser byte stream tied to that reservation.

No server-side source path exists.

Use one random stable content master key wrapped by an operator passphrase-
derived KEK. Wrap per-object random DEKs under the master key and encrypt
objects with AES-256-GCM. Derive a stable audit-integrity HMAC key using HKDF.
Audit HMAC is corruption/offline-tamper evidence, not non-repudiation against the
unlocked operator. Preserve external Ed25519 signatures for authority records.

Store opaque state in SQLite WAL and content-bearing material only in encrypted
objects outside Git. Retain or delete under the fixed Phase 3B pilot profile,
with signed legal-hold suppression and tombstone-aware restore.

Run scanning, native extraction, and OCR in separate rootless offline OCI
workers under enforced cgroups v2 and the exact policy limits. Native extraction
precedes OCR. Persist one encrypted bounded inspection artifact with page-level
method and limitation evidence.

The Human Review Workspace owns only append-only candidate review dispositions.
Nothing leaves Phase 3B until a later accepted Phase 3C contract.

## Consequences

### Positive

- Preserves ADR 0013 rather than replacing it.
- Makes authority, privacy, custody, lifecycle, and recovery explicit.
- Keeps source bytes and extraction off networks.
- Separates scanner, parser, OCR, and host secrets.
- Makes deletion and insufficient-evidence behavior testable.
- Produces a narrow Phase 3C input candidate without granting that consumer.

### Negative

- Adds one host dependency and several pinned worker/system dependencies.
- Requires Linux rootless container support and correct cgroup delegation.
- Requires interactive key custody and operator-triggered lifecycle work.
- Local OS compromise remains a significant residual risk.
- OCR and PDF extraction can be wrong or incomplete.
- Backups delay physical erasure up to thirty days.

### Neutral

- PDF support does not activate the other ADR 0013 candidate formats.
- Approval remains a human-use decision, not truth.
- Loopback operation remains non-deployment.
- Naming Virginia B. Andes does not authorize or reveal a source file.

## Compatibility and migration

Existing Phase 2 public contracts and tests remain compatible. New durable
adapters implement or version the existing interfaces. Review annotations are a
separate model, not a new ADR 0013 admission state.

There is no live dataset to migrate. The first implementation may create and
delete only generated synthetic runtime state. Future schema migrations require
backup, forward migration, reconciliation, validation, and rollback evidence.

## Validation

The Phase 3B Validation Requirements are binding. Implementation requires one
independently reviewed exact head and separate Chief Architect merge approval.
Real information requires the later exact source decision after canonical
implementation closeout.

## Rollback

Before live use, remove synthetic runtime state and revert the exact
implementation. After a pilot, execute authorized reset or honor a hold, verify
deletion and backup obligations, and then revert. Do not downgrade an
incompatible live schema.

## Reconsideration triggers

Reconsider this ADR for another domain/organization/operator, another format,
higher limits, another dependency or isolation runtime, remote or unattended
operation, changed cryptography/lifecycle, or any Phase 3C/3D consumer.
