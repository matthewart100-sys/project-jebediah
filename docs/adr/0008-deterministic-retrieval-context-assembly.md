# ADR 0008: Deterministic Retrieval and Context Assembly

**Status:** Proposed

**Decision level:** Implementation

**Date:** 2026-08-01

**Decision owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect

## Decision summary

If accepted, Sprint 006 will transform semantic retrieval candidates into a
generation context through one deterministic, inspectable policy. Candidates
will be filtered, grouped, selected, and rendered using stable reason codes,
ordering rules, and character budgets. Retrieval remains semantic-only; context
assembly does not introduce hidden reranking.

## Context

The canonical memory domain currently returns semantic candidates. An
interaction client needs a bounded subset, but naive truncation can make the
same input produce different evidence, silently select conflicting duplicate
records, or omit the reason a candidate did not reach the prompt. Sprint 006
must prove a reproducible client-side assembly boundary without changing the
memory repository or ranking algorithm.

### Verified facts

- `collector.memory` is the canonical memory domain.
- Current retrieval ranks candidates by semantic relevance only.
- Sprint 004 governance fields and lifecycle representations already exist.
- Sprint 005 preserved Qdrant as the authoritative memory record and semantic
  index under its accepted repository contract.

## Scope

This decision defines the proposed retrieval request, duplicate handling,
candidate reasons, ordering, whole-record selection, separate public
excerpting, character accounting, calibration, and prompt-capacity checks for
Sprint 006.

## Non-goals

- confidence-, importance-, recency-, or lifecycle-weighted reranking;
- mutation, verification, consolidation, lifecycle automation, or migration;
- vector schema or embedding identity changes;
- truth adjudication;
- a Phase 6 Reasoning Engine.

## Decision drivers

- Identical validated inputs and candidate records must assemble identically.
- Every candidate must have an auditable disposition.
- Conflicting duplicate identifiers must not be resolved by arrival order.
- Prompt limits must be enforced before provider invocation.
- Existing semantic-only ranking must remain visible and unchanged.

## Decision

### Retrieval request

The interaction application requests at most 12 semantic candidates from the
read-only memory query port. The provisional minimum semantic relevance is
`0.50`. The threshold is a policy default to be calibrated before
implementation approval, not a claim of universal relevance.

### Material fingerprint and duplicate groups

Candidates are grouped by canonical memory ID. A material fingerprint is
computed from the fields that can affect public evidence or prompt meaning:

- memory ID;
- content;
- semantic relevance;
- source type;
- origin;
- creator;
- creation context;
- confidence and confidence basis;
- verification state;
- lifecycle state;
- importance;
- created and updated timestamps;
- supporting-evidence references;
- embedding compatibility identity.

The fingerprint uses a specified canonical JSON serialization and SHA-256
digest. Exact material duplicates collapse to one candidate. Because their
complete material fingerprints are identical, input order cannot change the
surviving evidence value. Every removed copy receives
`duplicate_identical`.

If one memory ID has multiple material fingerprints, the entire group is
marked `duplicate_conflict` and the interaction fails with
`context_integrity_error`. No candidate in a conflicting group may be used as
evidence or passed to generation. The conflict is visible in trace counts and
candidate dispositions but does not expose raw conflicting content publicly.

### Candidate reason contract

Every bounded candidate receives exactly one terminal reason:

- `selected`;
- `below_threshold`;
- `duplicate_identical`;
- `duplicate_conflict`;
- `record_limit`;
- `individual_oversize`;
- `aggregate_budget_exhausted`;
- `malformed_candidate`.

These strings are stable internal decision semantics for Sprint 006. Traces
may expose only aggregate reason counts, not candidate content. A later change
requires an explicit contract review.

### Ordering and selection

After validation, duplicate handling, and threshold filtering, candidates are
sorted by:

1. semantic relevance descending;
2. canonical memory ID ascending.

No other score or hidden weighting is permitted. Selection walks that order
until both the requested evidence limit and the configured character budget are
reached. The default and maximum selected evidence count is 5.

### Context and record budgets

Context assembly uses the `interaction-context-v1` policy with:

- total rendered context budget: 12,000 Unicode scalar values;
- individual source-record budget: 8,000 Unicode scalar values;
- separate public evidence excerpt: 600 Unicode scalar values;
- maximum validated question: 2,000 Unicode scalar values.

The 12,000-character limit includes record wrappers, delimiters, labels,
evidence metadata, and escaping. It is measured on the exact rendered evidence
section sent to the generation adapter.

A source record over 8,000 characters is excluded as
`individual_oversize`. A record whose complete rendered representation fits
the remaining 12,000-character aggregate budget is selected as `selected`.
If the whole representation does not fit, it is excluded as
`aggregate_budget_exhausted`; later candidates continue to be evaluated in
stable order. Candidates after the effective selected-record limit receive
`record_limit`.

Model context uses whole source records only. Silent truncation,
provider-generated compression, and excerpt substitution in model context are
prohibited. Public evidence separately uses a deterministic prefix of at most
600 Unicode scalar values and an explicit `excerpt_truncated` boolean; that
public view never changes the model context.

### Insufficient evidence

If zero candidates are selected after all rules, the interaction returns
`insufficient_evidence` and must not invoke generation.

### Calibration and token-capacity proof

Before implementation approval, a versioned fixture of at least 20 clearly
relevant, 20 clearly irrelevant, and 20 borderline question-memory judgments
must evaluate the provisional `0.50` threshold under the exact accepted
embedding identity and geometry. The acceptance target is no more than 5%
false inclusion and no more than 10% false exclusion. If the target is missed,
architecture review must approve a new documented default; runtime code must
not tune it silently.

The validation suite must render worst-case policy inputs, apply the selected
model tokenizer or a conservative documented bound, and prove that system
instructions, question, evidence, output allowance, and provider overhead fit
within `num_ctx=8192`. Exceeding capacity blocks provider invocation.

## Alternatives considered

### Preserve provider or database return order

Rejected because arrival order is not a stable conflict or selection policy.

### Select the highest-scored duplicate

Rejected because equal IDs with different material payloads represent an
integrity conflict, not competing evidence to resolve silently.

### Add governance-weighted reranking

Rejected because Sprint 006 must preserve semantic-only retrieval and is not
authorized to introduce intelligent ranking.

### Summarize oversized records with the generation model

Rejected because it creates an extra ungrounded generation step and makes
context assembly nondeterministic.

## Consequences

### Positive

- Context construction is reproducible and mechanically testable.
- Duplicate conflicts fail closed for the affected memory ID.
- Every candidate has an inclusion, exclusion, or truncation reason.
- Existing memory ranking remains unchanged.

### Negative

- Conservative character budgets can exclude potentially useful evidence.
- Public prefix excerpts may omit later relevant text even though the whole
  source record was supplied to model context.
- Calibration fixtures and tokenizer-capacity checks become release gates.

## Data, security, and privacy implications

Fingerprints may be retained in approved trace metadata, but candidate content
must not be logged. Public evidence is governed separately by ADR 0007's
allowlist. Invalid or conflicting payload details remain internal and
ephemeral.

## Operational implications

Policy identifiers and all defaults must be emitted in the interaction trace.
Any change to ordering, reasons, budgets, or threshold requires a new policy
version and compatibility review.

## Compatibility and migration

This proposal consumes the existing `RetrievalCandidate` abstraction through a
read-only port. It does not alter memory payloads, Qdrant collections, vectors,
or API routes. No data migration is required.

## Validation requirements

- randomized-input-order determinism tests;
- exact and conflicting duplicate-ID tests;
- complete candidate-reason coverage;
- Unicode-scalar and wrapper-accounting tests;
- whole-record-only model-context and separate public-excerpt tests;
- evidence-count and context-budget boundary tests;
- zero-generation proof for empty selection;
- threshold calibration fixture acceptance;
- 8,192-token worst-case capacity proof;
- regression proof that ranking is semantic-only.

## Related decisions and documents

- [Sprint 006 specification](../SPRINT_006_SPECIFICATION.md)
- [Sprint 006 validation requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)
- [ADR 0007](0007-grounded-response-and-evidence-contract.md)
- [ADR 0009](0009-retrieved-content-trust-boundary.md)

## Review record

This ADR is a proposal on the Sprint 006 Proposal v2 custody branch.
Implementation remains unauthorized until Work Mode reviews the exact proposal
head and the Chief Architect accepts the architecture and authorizes the
sprint.
