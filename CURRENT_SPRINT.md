# Current Sprint

## Active sprint

**Name:** B1 - Synthetic Custody Foundation

**Status:** Authorized for implementation after the B1 activation package is
independently reviewed, approved, and merged

**Canonical base:** `37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Implementation authority:** B1 only, effective after merge of
[CA-2026-08-06-B1-ACTIVATION](docs/governance/CHIEF_ARCHITECT_B1_ACTIVATION_DECISION.md)

**Deployment status:** Unauthorized

**Information-use status:** Generated synthetic PDFs are authorized only for
the bounded B1 local custody implementation. Real documents, VBA information,
text extraction, OCR, model use, knowledge promotion, memory/Qdrant projection,
retrieval, grounded answers, and public exposure remain unauthorized.

## Active milestone question

Can Project Jebediah prove a generated synthetic PDF can be validated,
identified, encrypted, stored, audited, deduplicated, expired, deleted, reset,
and recovered within a deterministic local custody boundary without activating
downstream intelligence capabilities?

## Authorized milestone boundary

Chief Architect decision `CA-2026-08-06-B1-ACTIVATION` authorizes, after this
activation package merges:

- generated synthetic PDF fixtures only;
- local or loopback custody with PDF, MIME, structure, and size validation;
- SHA-256 identity, encrypted custody, and opaque metadata;
- quarantine, staging, audit, duplicate, expiration, deletion, reset, and
  recovery behavior;
- deterministic tests and appropriate file-level reuse of custody engineering
  from pull requests #59 and #60; and
- one bounded implementation pull request under the independent review policy.

This sprint does **not** authorize:

- B2 or any later milestone;
- a reset, rebase, force update, self-approval, self-merge, deployment, or
  runtime mutation;
- real documents or VBA access;
- text extraction, OCR, Knowledge Objects, workspace, identity, model,
  promotion, memory, Qdrant, retrieval, grounded-answer, executive-dashboard,
  domain, GPU-routing, or public-exposure work; or
- any runtime, server, container, DNS, certificate, database, or external-state
  mutation.

## Success criteria

1. The B1 implementation remains inside the exact synthetic custody boundary.
2. ADR 0016 remains Accepted and unbroadened.
3. Synthetic-only enforcement is technical and fail-closed.
4. Custody is encrypted, opaque, auditable, recoverable, and deletable.
5. No downstream intelligence, runtime, deployment, or real-information path
   is added.
6. Required tests and repository validation pass.
7. One non-draft pull request receives independent read-only normal-chat review
   and a later Chief Architect exact-head merge decision.

## Next authority gate

This activation package must first receive independent read-only normal-chat
review, a Chief Architect exact-head merge decision, and merge. Only then may
Codex begin B1 implementation. B2 remains unauthorized.
