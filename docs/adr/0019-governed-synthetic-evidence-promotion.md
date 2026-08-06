# ADR 0019: Governed Synthetic Evidence Promotion

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-06

**Decision owner:** Chief Architect

**Required reviewers:** Independent architecture reviewer under the canonical
coordination policy, then Chief Architect final decision

## Decision summary

For P1 only, promote an exact repository-generated synthetic evidence candidate
after explicit human approval into two linked representations: an immutable
metadata-only record in the existing Knowledge Registry and an immutable,
session-scoped approved-evidence content projection. Rejected, pending,
unknown, stale, mismatched, or otherwise ineligible candidates produce neither
representation and remain unavailable to retrieval.

## Context

[ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md) requires a
governed promotion boundary before derived knowledge becomes available to an
ordinary consumer. [ADR 0014](0014-knowledge-registry-domain-boundary.md)
implements a metadata-only registry, deliberately excluding content,
integration, promotion, retrieval, and runtime consumers. The Phase 3B
reconciliation requires a new promotion ADR before C1.

P1 needs one approved document-derived fact to change one answer. A direct
registry write from dashboard code would collapse presentation, human review,
promotion, and knowledge governance. Writing the source content into the
registry would violate ADR 0014. Writing to Memory Service or Qdrant would
activate C2, which P1 excludes.

### Verified facts

- `collector.knowledge.registry` provides immutable governance models plus
  `register`, `find`, and `contains` through a storage-neutral repository.
- Registry records contain no source or derived content and do not grant
  retrieval, truth, or action authority.
- The current Executive Product Shell imports no registry, Collector, memory,
  model, or runtime module.
- No accepted promotion producer, content store, runtime consumer, or durable
  Knowledge Vault implementation exists.
- Historical pull request #60 contains a `Phase3CBridge` that models approval,
  promotion, citations, and retrieval but keeps candidate, promoted content,
  and audit state in process and bypasses the Knowledge Registry.

### Reported facts

- The P1 product journey requires the answer to remain unchanged until an
  explicit approval makes evidence eligible.

### Working assumptions

- One immutable in-memory content projection is sufficient to demonstrate the
  P1 learning loop without claiming durable Knowledge Vault maturity.
- The exact generated fixture digest can identify a reviewed compiled evidence
  manifest without parsing arbitrary PDF content.
- A compiled synthetic reviewer identity and policy identity are sufficient for
  the demonstration. They do not establish an authentication system.

### Open questions

- Durable content persistence, generalized producers and consumers, policy
  vocabularies, and recovery remain unresolved and blocked after P1.
- Whether the later Knowledge Vault uses the registry, Memory Service, or
  another content store remains unresolved.

These questions do not block an in-process synthetic reference adapter with no
external consumer.

## Scope

- P1 evidence-candidate and review-disposition contracts.
- Exact promotion eligibility and idempotency rules.
- Creation of the metadata-only Knowledge Registry record.
- Creation of the linked session-scoped approved-evidence content projection.
- Provenance, consumer, use, lifecycle, failure, reset, and restart behavior.
- Package and dependency direction for the bounded promotion domain.

## Non-goals

- Accepting this Proposed decision or authorizing implementation.
- General document inspection or content extraction.
- Live sources, real organizational information, or domain policy.
- A durable Knowledge Vault, content database, API, service, or deployment.
- Memory Service, Qdrant, embedding, model, Knowledge Graph, or reasoning
  integration.
- Autonomous review, verification, promotion, lifecycle transition, or action.
- Source truth or action authority.

## Decision drivers

- Make approval a necessary and testable eligibility gate.
- Preserve ADR 0014's metadata-only registry boundary.
- Preserve source, custody, review, promotion, and retrieval identities.
- Keep content and metadata representations linked but semantically distinct.
- Fail closed on missing or contradictory policy and provenance.
- Avoid C2 and durable operational obligations.
- Make reset and rollback complete.

## Considered alternatives

### Store approved content in the Knowledge Registry

This would give one repository both metadata and content, but it contradicts
ADR 0014's fixed metadata-only contract and would require a superseding ADR,
content security, durable storage, migration, and recovery decisions.

**Disposition:** Rejected.

### Promote directly to Memory Service and Qdrant

This could reuse semantic retrieval code but would activate C2, require an ADR
0003 successor, embedding identity, external dependencies, persistence, and
recovery. None is needed for one deterministic P1 question.

**Disposition:** Rejected.

### Keep approved content only in dashboard state

This is small but gives presentation code promotion and knowledge-governance
authority and leaves no reusable domain contract.

**Disposition:** Rejected.

### Register metadata plus a separate session projection

The registry records the governance envelope. A separate immutable in-memory
projection holds only the bounded synthetic statement and evidence trace needed
by the approved consumer. The promotion service creates both only after
eligibility succeeds.

**Disposition:** Selected.

## Decision

### Responsibility boundary

Introduce a standard-library `collector.organizational_intelligence` domain
package for P1. Repository path placement does not assign Collector Engine
component authority. The package owns promotion and retrieval-domain contracts
only; it imports the Knowledge Registry contract but imports no Executive
Product Shell, Memory Service, Qdrant, Ollama, service, or deployment module.

The promotion boundary consumes:

- one immutable `SyntheticEvidenceCandidate` produced by exact fixture-digest
  lookup;
- one append-only `HumanEvidenceDisposition`;
- one exact `PromotionPolicy` naming allowed fixture, domain, classification,
  consumer, use, review policy, and transformation version; and
- one `KnowledgeRegistryRepository` supplied through dependency injection.

### Evidence candidate

The candidate contains no arbitrary metadata and includes:

- candidate, fixture, source-record, submission, custody-object, and admission
  identities;
- exact lowercase SHA-256 PDF digest and byte count;
- compiled evidence-manifest identity and version;
- one bounded synthetic statement and display excerpt;
- classification, domain, intended consumer, and use identifiers;
- source observation and candidate creation times; and
- material limitations stating that the evidence is generated and not
  organizational truth.

Any identity rendered through the existing Executive Product Shell model uses
the compatible `demo-p1-*` safe-ID namespace. The source identity is
`demo-p1-synthetic-program-outcomes-source`, the transformation identity is
`demo-p1-synthetic-fixture-projection` at version `1`, and the only citation
anchor is page `1`.

The statement and excerpt come only from the compiled manifest selected by the
exact PDF digest. No parser or caller-supplied content may populate them.

### Human disposition

The disposition is exactly `approved` or `rejected` and contains:

- disposition and candidate identities;
- compiled reviewer and review-policy identities;
- timezone-aware decision time;
- one allowlisted reason code; and
- an explicit statement that approval grants only the P1 synthetic consumer
  and use.

The dashboard records the user's fixed approve or reject action; it does not
authenticate a real person or establish factual verification. A second
different disposition for the same candidate is a conflict and fails closed.
The approved reason is exactly `approve_exact_p1_synthetic_evidence`; the
rejected reason is exactly `reject_exact_p1_synthetic_evidence`.

The version `1` disposition contains exactly: disposition ID, candidate ID,
candidate digest, `approved` or `rejected`, reviewer ID
`demo-p1-synthetic-reviewer`, review-policy ID
`demo-p1-synthetic-evidence-review-policy`, policy version `1`, the matching
fixed reason code, aware UTC decision time, and the exact consumer/use grant.
No rationale, note, free-form field, self-asserted boolean, or caller identity
is accepted.

### Eligibility

Promotion succeeds only when all of these are true:

1. the candidate digest matches the exact compiled fixture manifest;
2. custody reports the exact object and admission identities as accepted and
   available;
3. the disposition is `approved` under the exact P1 review policy;
4. domain, classification, consumer, use, source, and transformation values
   match the closed P1 policy;
5. every required identifier and timezone-aware time is present;
6. no rejected, deleted, expired, superseded, invalidated, reconciled-as-unsafe,
   or conflicting state exists; and
7. the registry and projection identities are deterministically derivable from
   the admitted digest and policy version.

Unknown or failed evaluation is ineligible. Successful custody, fixture lookup,
or registry registration alone is not approval.

### Atomic application behavior

The in-memory reference composition performs these deterministic steps:

1. validate candidate, disposition, custody evidence, and policy;
2. build an immutable `KnowledgeRegistryRecord` with
   `HumanReviewState.APPROVED`, `KnowledgeLifecycleState.REGISTERED`, synthetic governance scope, freshness, and
   evidence-linked uncertainty;
3. build an immutable `ApprovedEvidenceProjection` containing the statement,
   excerpt, registry identity, full lineage, and allowed consumer/use;
4. register the metadata record; and
5. publish the projection to the in-memory projection repository only after
   registration succeeds or returns the identical idempotent record.

If validation, registration, identity reconciliation, or projection
publication fails, no projection becomes eligible. `publish` is failure-atomic:
it validates the entire immutable record and all conflicts before one
in-memory assignment, and a failure leaves no projection record. P1 does not
claim a distributed transaction or durable atomicity.

Repeating the exact approved promotion is idempotent and returns the same
identities. Reusing an identity with different metadata, content, disposition,
or policy is a visible conflict.

### Exact Knowledge Registry mapping

P1 reuses `KnowledgeRegistryRecord` unchanged and populates every field as
follows; no implementation choice or content field is added:

| Registry field | Exact P1 mapping |
| --- | --- |
| `object_id` | Deterministic `demo-p1-registry-object-<six-digit-epoch-ordinal>` identity from the P1 semantic ID factory |
| `object_kind` | `demo-p1-approved-synthetic-program-outcomes` |
| provenance producer | `demo-p1-synthetic-evidence-promoter` at promotion time |
| provenance source | `demo-p1-synthetic-program-outcomes-source`, manifest revision `1`, observed `2026-01-15T12:00:00Z` |
| transformation | `demo-p1-synthetic-fixture-projection`, version `1` |
| evidence references | Exact candidate, disposition, and promotion-decision identities |
| information owner | `demo-p1-synthetic-fixture-owner` |
| domain/classification | `demo-p1-synthetic-program-outcomes-domain` / `synthetic_non_sensitive` |
| consumer/use | `demo-p1-executive-product-shell-consumer` / `demo-p1-synthetic-question-answering-use` |
| retention policy string | `demo-p1-synthetic-program-outcomes-retention-policy-v1` |
| deletion policy string | `demo-p1-synthetic-reset-deletion-policy-v1` |
| freshness policy string | `demo-p1-fixed-receipt-deadline-freshness-policy-v1` |
| invalidation policy string | `demo-p1-exact-eligibility-invalidation-policy-v1` |
| temporal context | `CURRENT`, evaluated/promoted at promotion time, effective at approval, expires at the fixed custody deadline |
| uncertainty | `BOUNDED`; evidence IDs are candidate/disposition/promotion; explanation `Bounded to one approved generated fixture and the exact P1 use.`; exact synthetic/no-truth limitation |
| human review | policy string `demo-p1-synthetic-evidence-review-policy-v1`, `APPROVED`, fixed reviewer, approval time, rationale `approve_exact_p1_synthetic_evidence` |
| lifecycle | `REGISTERED`, recorded by `demo-p1-synthetic-evidence-promoter` at promotion time, reason `registered_exact_p1_approved_evidence` |

The versioned `*-v1` strings adapt separately modeled P1 policy ID/version
pairs to the existing Registry's single-string policy fields. They do not
change the Registry contract. The record contains no statement, excerpt, PDF
bytes, filename, path, answer, token, key, free-form note, or source locator.

### Projection contract

`ApprovedEvidenceProjection` contains:

- projection and registry object identities;
- exact bounded statement and excerpt;
- source, fixture, receipt, signer key, authorization policy, receipt
  verification event/time, submission, custody, admission, digest, candidate,
  disposition, reviewer, review-policy, promotion-decision, and transformation
  identities;
- source observation, approval, projection, and expiration times;
- qualitative uncertainty and limitations;
- exactly one allowed consumer and use; and
- active session lifecycle.

For implementation readiness, the exact bounded statement is:

> Approved synthetic evidence reports 12 fabricated workshops, 48 fictional
> participants, and 36 fictional follow-up responses.

The source excerpt is exactly:

> The fabricated P1 program recorded 12 synthetic workshops, 48 fictional
> participants, and 36 fictional follow-up responses. These values are
> generated test evidence and must not be used for a real decision.

Its limitation is exactly: `Generated synthetic evidence; not organizational
truth and not authorized for a real decision.`

The projection repository exposes only `publish`, `find`, and
`eligible_for(question_id, consumer_id, intended_use, as_of)`. It provides no
update, arbitrary list, semantic search, source write, action, or external
interface.

### Reset and restart

P1 reset tombstones or invalidates generated synthetic custody, destroys its
wrapped data-encryption key and ciphertext, retains only content-free
audit/tombstone evidence for the isolated epoch, then replaces the entire
process-local registry/projection epoch and clears retrieval and answer
eligibility. It does not add delete or clear methods to either immutable
repository and never affects a real or external resource.

On restart, durable custody may be reconciled, but registry and content
projections start empty. The answer therefore returns insufficient evidence
until a new explicit synthetic disposition and promotion occur. Intact,
active, eligible exact-fixture custody may deterministically reconstruct only
an ineligible `pending` candidate from its digest and compiled manifest.
Expired, held, missing, or tampered custody cannot reconstruct a candidate. P1
must not infer approval from custody history or silently reconstruct
retrievable content.

### Ownership and authority

The maintainer remains accountable for the repository candidate. No Knowledge
Vault component or operational owner is assigned. The registry has authority
only over acknowledged metadata integrity; the projection has authority only
over the exact derived record produced by the P1 process. Neither is
authoritative for represented facts.

## Consequences

### Positive

- Approval is a hard boundary rather than a UI label.
- ADR 0014 remains intact because content stays outside the registry.
- Full evidence lineage is available to retrieval and presentation.
- No memory, vector, model, service, or durable-content dependency is added.
- Deterministic identities make retries and tests precise.
- Restart fails closed instead of reviving approval implicitly.

### Negative

- P1 introduces a second process-local repository beside the registry.
- Approved content is intentionally lost on restart.
- The exact-fixture mechanism cannot generalize to arbitrary documents.
- Later durable promotion may replace rather than extend the P1 adapter.

### Neutral

- Knowledge Registry component maturity and Knowledge Vault maturity do not
  advance.
- Human approval remains a bounded use decision, not factual verification.
- The source PDF remains under custody policy and is not stored in the
  projection.

## Data and provenance impact

The registry record and content projection are derived information. The
disposition and promotion audit are synthetic operational records. The PDF and
fixture manifest remain reviewed demonstration sources, not organizational
truth. Every projection retains the full identity chain required to trace back
to the exact bytes and approval.

No personal data, real organization, arbitrary source, model output, embedding,
or external identifier is permitted.

## Security and privacy impact

The fixed schema has no arbitrary metadata bag. Statement and excerpt length,
characters, and origin are validated. Unknown policy, content, digest,
consumer, use, reviewer, or transition values fail closed. Error and audit
surfaces use identities and reason codes without copying content.

The session projection is accessible only through the injected domain
interface and the loopback shell composition selected by ADR 0020. It has no
file, network, database, export, or model interface.

## Operations and recovery impact

No operational or durable knowledge store is introduced. The in-memory
repositories lose state at process exit by design. A future durable promotion
system requires component ownership, schema, migration, backup, restore,
deletion propagation, observability, and recovery decisions.

## Compatibility and migration

Existing registry types and methods remain unchanged. The new package consumes
them through dependency injection. Existing memory and dashboard packages do
not import the new domain directly except through the separately accepted P1
adapter boundary.

No data migration is required. Rollback clears process state and removes the
new package, tests, and composition.

## Validation

Tests must prove:

- pending, rejected, deleted, expired, digest-mismatched, policy-mismatched,
  unknown, and conflicting candidates cannot produce a registry record or
  projection;
- an exact approved candidate produces linked immutable representations;
- exact retry is idempotent and divergent retry conflicts;
- registry failure leaves no eligible projection;
- projection lookup enforces question, consumer, use, time, and lifecycle;
- restart restores no projection or approval;
- lineage contains every required identifier and time; and
- package boundaries exclude dashboard, memory, Qdrant, model, service, and
  deployment imports.

Reconsider if P1 needs durable promoted content, more than one fixture or
consumer policy, autonomous review, real information, Memory Service, Qdrant,
or an external API.

## Follow-up work

- Accept ADR 0018 and ADR 0020 before dependent implementation.
- Implement only after the complete P1 plan is accepted and activated.
- Define a new durable Knowledge Vault and generalized promotion decision for
  any post-P1 consumer.

## Related documents

- [ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md)
- [ADR 0014](0014-knowledge-registry-domain-boundary.md)
- [ADR 0018](0018-p1-synthetic-organizational-learning-pilot-sequencing.md)
- [ADR 0020](0020-executive-pilot-read-model-and-deterministic-retrieval.md)
- [P1 Pilot Implementation Plan](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Validation Requirements](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

The Chief Architect authorized preparation through
`CA-2026-08-06-P1-PLANNING`. Independent architecture review, Chief Architect
acceptance, status activation, merge approval, and merge remain pending. This
Proposed decision grants no implementation or information-use authority.
