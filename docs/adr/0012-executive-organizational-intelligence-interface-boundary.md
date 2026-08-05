# ADR 0012: Executive Organizational Intelligence Interface Boundary

**Status:** Accepted

**Accepted:** 2026-08-04

**Decision level:** System

**Date:** 2026-08-04

**Decision owner:** Chief Architect

**Reviewers:** Work Mode architecture review, then Chief Architect final review

## Decision summary

Define the first executive organizational-intelligence interface as a
read-only presentation consumer of an evidence-bearing read model organized
around “What is happening?”, “What needs attention?”, “What does Jebediah
know?”, and “What should happen next?”. The interface may present facts and
derived material but owns no source truth, verification, ingestion, knowledge
derivation, or action authority.

## Context

Project Jebediah has Collector and Memory Service implementation candidates and
an accepted Knowledge Vault authority boundary. Before this decision, it had no
approved executive interface, organizational read model, live information
domain, or action contract. An interface implemented directly against parsers,
vector results, or model output would silently decide data authority, failure
semantics, and human-action boundaries.

### Verified facts

- Reviewed `main` has no dashboard or executive-interface implementation.
- No active sprint is authorized.
- ADR 0011 is Accepted, and the Knowledge Vault remains **Named**.
- Collector and Memory Service candidates are implemented in the repository,
  but deployment and live information use are unauthorized.
- Data Ownership requires authority, provenance, freshness, conflict,
  classification, and lifecycle semantics before information use.

### Reported facts

- The attached implementation directive reports a nonprofit executive need to
  understand organizational state through four plain-language questions.
- That need requires validation with representative users before a live
  interface can be called useful.

### Working assumptions

- A read-only briefing can provide a bounded first value without action
  execution. This must be confirmed during sprint selection and user testing.
- The four questions are stable enough to organize a read model without
  choosing presentation technology.

### Open questions

- The first authorized information domain, user population, access model,
  freshness policies, read-model owner, and operational owner are unresolved.
- Generated assistance may depend on disposition of the separate Sprint 006
  interaction proposal.

These questions block affected implementation and live use. The system
responsibility boundary can be reviewed without resolving technology or pilot
details.

## Scope

- Executive-interface responsibility and exclusions
- Read-model evidence, time, freshness, lifecycle, and uncertainty semantics
- The four executive sections and user-visible failure states
- Boundary between presentation, generated assistance, and external action

## Non-goals

- UI framework, transport, database, model, hosting, or deployment selection
- Authentication or authorization design
- Live organizational information use
- Ingestion, source verification, knowledge derivation, or indexing design
- Workflow execution, approvals, record mutation, or automation
- Phase 6 Reasoning Engine activation

## Decision drivers

- A nonprofit executive must receive useful plain-language orientation.
- Every material claim must remain traceable to eligible evidence.
- The interface must fail visibly when evidence is stale, incomplete,
  conflicting, unavailable, or unauthorized.
- Presentation must not acquire source, verification, or action authority.
- The first foundation must remain reversible and technology-neutral.

## Considered alternatives

### Direct dashboard over source systems

The interface could query approved sources directly. This reduces intermediate
structure but distributes authority, freshness, conflict, and failure behavior
across presentation code. It also makes consistent evidence and access control
harder to review.

### Model-first conversational interface

A model could answer natural-language questions from retrieved documents. This
may feel flexible, but it makes incomplete evidence, citation, prompt
injection, determinism, cost, and degraded behavior the foundation rather than
an optional consumer concern.

### Evidence-bearing read model with optional assistance

A structured read model can separate eligible evidence and deterministic
briefing assembly from visual presentation and optional generation. It adds a
component contract but makes authority, testing, and degraded behavior
reviewable.

### Retain the current design

The project could continue without an executive interface. This avoids new
risk but does not satisfy the stated usability goal and encourages later ad hoc
clients to invent incompatible boundaries.

## Decision

Select an evidence-bearing organizational-intelligence read model as the only
ordinary input to the first executive interface.

The interface organizes items into `happening`, `attention`, `know`, and
`next`, corresponding to the four named executive questions. The knowledge
section states coverage and limitations so that the interface cannot imply
complete organizational knowledge. The next section treats “should” as a
supported proposal for human decision, not action authority. Each item
identifies its evidence classification, safe source references, source time
when known, assembly time, freshness, evidence sufficiency basis, bounded
qualitative uncertainty state and explanation, lifecycle, transformation
identity when derived, material limitations, and permitted human next step.
Uncertainty is one of `bounded`, `incomplete`, `conflicting`, `unknown`, or
`not_applicable`; it is evidence-linked and cannot be interpreted as a numeric
truth probability.

Every `next` item is classified as exactly one of `decision_required`,
`organizational_gate`, `action_candidate`, or `informational_attention`. It
identifies the decision or gate owner when known and the separate authority
required before any decision or action takes effect.

The interface owns presentation and navigation only. It cannot ingest source
content, verify claims, transform or index knowledge, mutate authoritative
records, approve work, or execute external actions. Attention and next-step
items are human-review aids, not permissions.

The core briefing must have deterministic evidence assembly. Generated
assistance is optional and requires separately accepted interaction
architecture. When present, generated output remains derived,
non-authoritative, evidence-bounded, and unable to change verification,
lifecycle, priority, next-item classification, uncertainty state, or action
authority.

The user-visible contract distinguishes ready, partial, stale, insufficient-
evidence, unauthorized, and unavailable states. A last-known view is labeled
with its capture time and staleness. Empty eligibility cannot be presented as
proof that nothing is happening.

This decision does not name the component that assembles the read model or
select its interface. Those require an accepted component specification before
implementation.

## Consequences

### Positive

- The executive experience is organized around decisions rather than system
  internals.
- Evidence, time, uncertainty, and degraded behavior become testable contracts.
- Presentation cannot silently become a source or action system.
- Generated assistance can be added or removed without losing deterministic
  evidence access.
- Framework and deployment choices remain open.

### Negative

- A separately owned read-model assembly responsibility is required.
- Information domains need explicit mappings and freshness policies before
  they can appear.
- The interface may show incomplete or unavailable states instead of a
  visually complete briefing.
- Optional generation requires additional security, evaluation, cost, and
  operations work.

### Neutral

- The four-question organization is a user-facing contract, not a persistence
  schema.
- A future component may serve several interfaces if it preserves the accepted
  read-model semantics.

## Data and provenance impact

The interface reads eligible authoritative references and derived records but
does not own them. Presented items are cached or derived view data with source
and transformation lineage. Preferences or saved views, if later added,
require their own category, retention, and ownership decisions.

Generated summaries remain derived. Citations do not promote the interface or
Knowledge Vault to authority for source facts.

## Security and privacy impact

The interface creates a human-facing disclosure boundary. Live deployment
requires authentication, authorization, classification, least privilege,
safe citations, sanitized logs and errors, rendering protections, injection
defenses, and explicit export and analytics policies.

Ordinary client code receives only information approved for the current user
and use. The interface cannot expose storage topology or function as an
administrative path.

## Operations and recovery impact

The later component contract must define read-model health, freshness,
dependency failure, metrics, alerts, capacity, timeout, and support ownership.
The interface shows partial and last-known state without converting failure to
false success.

No authoritative backup or recovery responsibility is assigned to the
presentation layer. Saved state requires a separate decision.

## Compatibility and migration

No approved executive-interface consumer exists, so runtime migration is not
required. The later concrete read-model interface must be versioned and must
preserve the semantic fields and degraded states in this decision.

The existing memory API remains unchanged. The separate Sprint 006 interaction
proposal is neither accepted nor superseded by this decision.

## Validation

The decision is validated by the
[Organizational Intelligence Validation Requirements](../ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md).
Future tests must prove evidence completeness, state distinctions, action
non-authority, accessibility, privacy, injection resistance, and deterministic
briefing availability without a model.

Reconsider this decision if representative user testing shows that the four
questions cannot support the bounded executive task, or if the read-model
boundary prevents required evidence fidelity.

## Follow-up work

- Approve the first information domain, owner, user, consumer, and use.
- Specify and assign the read-model assembly component.
- Decide authentication, authorization, classification, freshness, retention,
  and operations.
- Decide whether generated assistance belongs in the first implementation.
- Select technology only after the architecture and sprint gates are complete.

## Related documents

- [Organizational Intelligence Interface Specification](../ORGANIZATIONAL_INTELLIGENCE_INTERFACE_SPECIFICATION.md)
- [Organizational Intelligence Validation Requirements](../ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md)
- [Current Architecture](../ARCHITECTURE.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md)
- [Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Work Mode approved exact proposal head
`c0a83f8fb4ec6ad82c90c658a4b83b8c596cd250` with no remaining findings. The
Chief Architect approved that exact head for merge in pull request #45. The
proposal was squash-merged to `main` as
`72099ac555efbb34b8344c5e34db7fb9aad5f69c`. Acceptance grants no
implementation, deployment, live-information-use, or action authority.
