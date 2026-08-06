# Organizational Intelligence Phase 3B Implementation Activation

**Status:** Architecture activation complete; Milestone 1 remains the historical
bounded authorization baseline, and branch-level completion work now references
the [Phase 3B Completion Directive](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md)

**Program phase:** Phase 3B - Governed Real-Document Intake and Inspection

**Prepared:** 2026-08-05

**Decision owner:** Chief Architect

**Required prior evidence:** Independent Work Mode exact-head architecture
review

**Adopted architecture head:** `bfa18ab35ae1bcd0cf6a91090dba62ab9220076a`

**Chief Architect architecture decision:** Pull request #58, 2026-08-05 - adopt
ADR 0016 and merge the Phase 3B architecture package

**Chief Architect implementation decision:** Authorize only Phase 3B
Implementation Milestone 1, Synthetic Intake and Custody Foundation, against
canonical baseline `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8`

**Still unauthorized:** The complete Phase 3B implementation, deployment, real
Virginia B. Andes or other organizational document use, knowledge promotion,
memory integration, and every Phase 3C or Phase 3D capability

## Current bounded authorization

For this branch, the active implementation authority is the
[Phase 3B Completion Directive](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md).
Milestone 1 remains the accepted historical bounded authorization that
established the custody foundation and prohibitions.

The
[Phase 3B Implementation Milestone 1 authorization](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_MILESTONE_1_AUTHORIZATION.md)
is the canonical implementation authority now in force. It permits only the
synthetic intake and custody foundation needed to answer whether Project
Jebediah can receive, classify, hold, reject, expire, and delete a generated
synthetic document without promoting it into knowledge or memory.

Milestone 1 does not activate the complete 59-file implementation manifest in
the Phase 3B Governed Intake Plan. That manifest remains unchanged as a future
full-package boundary and requires a separate exact authorization.

## Historical full-package disposition

**ADOPT ADR 0016 AND AUTHORIZE THE SYNTHETIC-ONLY PHASE 3B IMPLEMENTATION**

This prepared disposition did not authorize the complete 59-file implementation.
That full package remains gated by:

1. the complete Proposed architecture package is independently approved at one
   exact head;
2. the Chief Architect adopts this decision for that head;
3. a bounded activation edit changes Proposed/Prepared statuses and records the
   decision;
4. the same sole reviewer freshly approves the changed activation head;
5. the Chief Architect separately approves that unchanged head for merge; and
6. the package merges to canonical `main`.

Any later full-package decision may authorize only generated synthetic PDF
fixtures unless another separately reviewed decision changes the information-use
boundary. It cannot authorize a real VBA document implicitly.

## Prepared full-package option

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

## Historical full-package authorization template

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

## Full-package implementation scope

The Phase 3B Governed Intake Plan's Appendix A remains the sole file manifest for
a future complete Phase 3B implementation. Milestone 1 does not activate that
manifest as a whole. No file in Appendix A is added to Milestone 1 merely because
it appears in the future full-package manifest.

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
- full Phase 3B implementation or implementation merge without its later
  exact-head decisions.

## Implementation gates

Before Milestone 1 code:

- the architecture package and ADR 0016 are canonical Accepted records;
- the Milestone 1 authorization is canonical;
- `main` is clean and synchronized at the architecture merge;
- the exact bounded Milestone 1 implementation manifest is published before
  coding;
- required baseline validation passes; and
- the implementation owner confirms no prohibited input is required.

## Implementation review and merge gates

Milestone 1 must remain inside its separately published exact changed-file
manifest, use generated synthetic fixtures only, pass its complete required
validation, publish one non-draft pull request at one exact head, receive one
independent read-only Work Mode review, and stop for a separate Chief Architect
exact-head merge decision. A changed implementation head requires fresh review.

## Later real-source decision

After implementation merge, canonical read-back, and terminal closeout, stop
before inspecting any real file. The later decision must use the exact
authorization fields in section 22 of the plan and must identify one explicit
non-clinical board-roster PDF. It cannot authorize a folder or arbitrary VBA
documents.
