# Phase 3B Implementation Milestone 1 - Synthetic Intake and Custody Foundation

**Decision authority:** Chief Architect

**Canonical authorization baseline:** `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8`

**Architecture baseline:** Phase 3B accepted and merged

**Relevant accepted decision:** ADR 0016

**Decision status:** `IMPLEMENTATION AUTHORIZED - BOUNDED MILESTONE ONLY (HISTORICAL BASELINE)`

**Real-document use:** `NOT AUTHORIZED`

**Deployment:** `NOT AUTHORIZED`

**Phase 3C:** `NOT AUTHORIZED`

**Phase 3D:** `NOT AUTHORIZED`

## Purpose

> Branch note: ongoing completion implementation now references
> [Phase 3B Completion Directive](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md).
> This document remains the historical Milestone 1 scope and stop-condition
> baseline.

This milestone exists only to answer:

> Can Project Jebediah safely receive, classify, hold, reject, expire, and
> delete a synthetic document without promoting it into knowledge or memory?

This authorization is narrower than full Phase 3B implementation authority. It
does not activate the complete 59-file implementation manifest in the
[Phase 3B Governed Intake Plan](../ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md).
That future manifest remains unchanged and separately gated.

## Authorized scope

- generated synthetic PDF fixtures only;
- loopback-only local operator access;
- bounded synthetic intake;
- authorization and admission enforcement;
- PDF signature, type, size, and count validation;
- opaque identifiers;
- content hashing;
- quarantine and staging custody;
- architecture-compliant local custody;
- opaque metadata;
- lifecycle persistence;
- audit evidence;
- duplicate detection;
- failure isolation;
- expiry;
- deletion and reset;
- required recovery behavior;
- deterministic synthetic tests; and
- directly required operator and validation documentation.

Implementation must use the smallest exact changed-file manifest that answers the
milestone question. Appearance in the full Phase 3B 59-file manifest does not by
itself authorize a file or behavior for Milestone 1.

## Prohibited scope

- real VBA or organizational documents;
- local-folder document discovery;
- organizational text extraction;
- OCR for organizational use;
- Source Document Evidence promotion;
- Knowledge Objects;
- Knowledge Registry writes;
- memory records;
- embeddings;
- Qdrant;
- semantic retrieval;
- model or Ollama use;
- Open WebUI attachment ingestion;
- n8n or email ingestion;
- external integration;
- multi-user or non-loopback operation;
- deployment;
- Phase 3C; and
- Phase 3D.

No milestone result may be described as factual verification, knowledge,
memory, production readiness, operational readiness, or authorization to begin
VBA onboarding.

## Required workflow

1. Preserve a dedicated implementation branch and isolated worktree created from
   the canonical authorization baseline.
2. Publish the exact bounded Milestone 1 implementation manifest before coding.
3. Use only generated synthetic fixtures.
4. Run the full validation required by the bounded implementation and applicable
   repository standards.
5. Publish one non-draft pull request.
6. Obtain one independent read-only Work Mode review of the exact immutable
   implementation head.
7. If the head changes, obtain a fresh exact-head review.
8. Do not merge without a separate Chief Architect decision naming the exact
   pull request and head commit.

## Stop conditions

Stop implementation and return to the Chief Architect if the milestone requires:

- any real or existing document;
- a filesystem discovery or source-location path;
- any prohibited downstream knowledge, memory, model, retrieval, or integration
  capability;
- non-loopback, multi-user, deployed, or externally connected operation;
- a change to ADR 0016, the Phase 3B threat model, lifecycle/recovery
  architecture, validation architecture, dependency architecture, or accepted
  59-file future manifest; or
- behavior beyond the bounded milestone question.

## Remaining gates

Implementation authorization is not merge, deployment, real-source, Phase 3C,
or Phase 3D authority. The implementation pull request must stop after
independent Work Mode review for a separate Chief Architect exact-head merge
decision.
