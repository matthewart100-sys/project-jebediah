# Organizational Intelligence Phase 3B Implementation Activation

**Status:** Prepared; not adopted; implementation remains unauthorized

**Program phase:** Phase 3B - Governed Real-Document Intake and Inspection

**Prepared:** 2026-08-05

**Decision owner:** Chief Architect

**Required prior evidence:** Independent Work Mode exact-head architecture
review

## Recommended disposition

**ADOPT ADR 0016 AND AUTHORIZE THE SYNTHETIC-ONLY PHASE 3B IMPLEMENTATION**

Authorize only the exact 59-file implementation in the Phase 3B Governed Intake
Plan after:

1. the complete Proposed architecture package is independently approved at one
   exact head;
2. the Chief Architect adopts this decision for that head;
3. a bounded activation edit changes Proposed/Prepared statuses and records the
   decision;
4. the same sole reviewer freshly approves the changed activation head;
5. the Chief Architect separately approves that unchanged head for merge; and
6. the package merges to canonical `main`.

This decision would authorize generated synthetic PDF fixtures only. It would
not authorize a real VBA document.

## Recommended option

Implement one local, single-operator, PDF-only intake and review slice using:

- signed single-use authorization receipts;
- browser-pushed bytes on literal loopback;
- encrypted local object custody and SQLite metadata;
- rootless offline scanner, native PDF, and OCR workers;
- explicit review, retention, deletion, hold, backup, restore, and reset; and
- no Phase 3C or Phase 3D capability.

## Alternatives rejected

- Path-based CLI acquisition reverses the accepted pushed-envelope boundary.
- A multi-user or network service adds deployment and identity decisions.
- Host parsing lacks sufficient isolation.
- Cloud scanning/OCR exports data.
- DOCX expands dependency and attack surface without the first demonstration
  requiring it.
- Implementing Phase 3C concurrently would bypass the approved phase gate and
  obscure whether Phase 3B deletion and authority work independently.

## Operational consequence

The implementation will add durable encrypted local state, interactive key
custody, SQLite migrations, rootless OCI workers, dependency/image maintenance,
manual backups, and explicit cleanup. It remains a repository candidate with no
availability or deployment claim. All testing uses generated synthetic PDFs.

## Exact authorization text

> For repository `matthewart100-sys/project-jebediah`, I adopt System ADR 0016
> and the Phase 3B architecture package at exact reviewed head
> `<ARCHITECTURE_HEAD>`, whose independent Work Mode disposition is
> **APPROVED** with `<FINDING_SUMMARY>`. I authorize the Implementation Engineer
> to implement only the exact 59-file manifest and generated-synthetic-PDF
> behavior defined by that head. This authorization permits no real Virginia B.
> Andes or other organizational information, no source discovery, no deployment,
> no non-loopback access, no DOCX, no Knowledge Registry or Knowledge Object
> write, no memory, embedding, Qdrant, retrieval, model inference, grounded
> answer, action, or files outside the manifest. The activation status edit,
> architecture merge, implementation review, implementation merge, real-source
> use, and deployment each remain separately gated as documented.

## Exact implementation scope

The Phase 3B Governed Intake Plan's Appendix A is the sole file manifest.
Implementation may add the specified host dependency, lock exact worker
dependencies and images, extend the current admission contracts compatibly,
create durable adapters/workers, extend the Executive Product Shell workspace,
add the exact tests/workflow/operator guide, and update direct documentation.

## Explicitly unauthorized

- discovering or processing any existing document;
- accessing filenames, folders, or source locations;
- real VBA, organizational, personal, clinical, patient, credential, banking,
  donor, or personnel information;
- a real authorization receipt or operational key;
- non-loopback or multi-user service;
- deployment, background scheduling, remote backup, or availability claim;
- any format except generated synthetic PDF;
- Knowledge Registry, Knowledge Objects, memory, embeddings, Qdrant, retrieval,
  models, grounded answers, Phase 3C, Phase 3D, or action;
- changing the exact limits, retention, deletion, hold, authority, privacy,
  encryption, worker, or file-scope decisions; and
- implementation or architecture merge without their later exact-head decisions.

## Implementation gates

Before code:

- the architecture package and ADR 0016 are canonical Accepted records;
- this activation is canonical Adopted;
- `main` is clean and synchronized at the architecture merge;
- documentation validation, whitespace, sensitive-value, lock, and existing
  Python tests pass;
- worker build prerequisites are available without credentials; and
- the implementation owner confirms no prohibited input is required.

## Implementation review and merge gates

The implementation must match all 59 files, pass the complete Phase 3B
validation inventory, publish one exact head, receive one independent Work Mode
review, and stop for a separate Chief Architect implementation merge decision.
A changed implementation head requires fresh review.

## Later real-source decision

After implementation merge, canonical read-back, and terminal closeout, stop
before inspecting any real file. The later decision must use the exact
authorization fields in section 22 of the plan and must identify one explicit
non-clinical board-roster PDF. It cannot authorize a folder or arbitrary VBA
documents.
