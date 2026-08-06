# ADR 0018: P1 Synthetic Organizational Learning Pilot Sequencing

**Status:** Proposed

**Decision level:** Foundational

**Date:** 2026-08-06

**Decision owner:** Chief Architect

**Required reviewers:** Independent architecture reviewer under the canonical
coordination policy, then Chief Architect final decision

## Decision summary

Create one bounded P1 implementation milestone for a complete synthetic
Organizational Intelligence learning loop instead of implementing B1, B2, C1,
and D1 as disconnected product increments. P1 is a narrow sequencing exception,
not a broad phase activation: it uses one generated fixture, one allowlisted
question, one local human disposition, deterministic approved-only retrieval,
and the existing Executive Product Shell, while leaving real information,
general document inspection, C2, deployment, and every external capability
unauthorized.

## Context

The
[Phase 3B reconciliation decision](../governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
replaced an over-broad implementation with a strict B0, B1, B2, B3, C0, C1,
C2, D1, D2, and O1 sequence. It requires each capability milestone to complete
its own plan, ADR, implementation, merge, and closeout before a later milestone
begins. That sequence successfully restored authority discipline, but it makes
the smallest user-visible learning loop span several separately stopped
increments.

The Chief Architect has now authorized P1 planning for a complete product
slice. The planning directive does not authorize implementation or change the
reconciliation decision. A Foundational decision is required because a lasting
exception changes roadmap ordering and gate application across several system
boundaries.

### Verified facts

- Canonical `main` at the planning base is
  `37dd437617ed731340e9fd3da6cab0b1c49f7b4a`.
- That commit includes the B0 normal revert and contains no active pilot
  implementation authority.
- The Executive Product Shell is implemented as a compiled-synthetic,
  presentation-only, GET/HEAD loopback preview under ADR 0015.
- The metadata-only Knowledge Registry is implemented under ADR 0014 and has
  no runtime producer or consumer.
- Synthetic document-admission contracts are implemented, but durable custody,
  general PDF inspection, human review, promotion, retrieval, and dashboard
  integration are not accepted implementations.
- ADRs 0011 through 0016 preserve the source, custody, derived-knowledge,
  registry, read-model, presentation, and human-authority separations required
  by P1.
- Pull request #59 contains a synthetic custody proposal. Pull request #60
  contains a promotion and retrieval prototype. Neither is accepted as a
  conforming implementation or as authority.
- Pull request #63 is open and Proposed. It does not change canonical authority.

### Reported facts

- The product objective is to demonstrate that the same executive question
  changes from insufficient to evidence-grounded only after a governed
  document approval.
- No representative user result or operational environment is verified.

### Working assumptions

- One repository-generated PDF whose exact digest maps to one compiled
  synthetic evidence manifest can prove the workflow without a general parser,
  scanner, OCR worker, or arbitrary-file surface.
- One allowlisted preset question is sufficient to prove a changed answer and
  evidence lineage.
- A single local operator with compiled synthetic role identifiers can provide
  an explicit human disposition without activating C0 identity or D2 workspace
  architecture.
- Session-scoped promoted content is sufficient for P1; restart may require a
  fresh synthetic approval and must never restore ordinary retrieval silently.

These assumptions are implementation constraints. If any fails, P1 stops for
reconsideration rather than expanding to the deferred milestone.

### Open questions

- The exact implementation head, dependency resolution, and test evidence do
  not exist. They are produced only after later implementation authorization.
- Representative executive usefulness remains untested. P1 proves the
  workflow, not organizational value.
- The canonical reviewer mechanism may change if a successor to ADR 0005 is
  accepted before P1 review. The role separation and exact-head evidence gates
  remain mandatory either way.

None of these questions prevents review of the proposed sequencing boundary.

## Scope

This decision governs:

- one product-first P1 milestone and its relationship to the revised B0-O1
  sequence;
- the exact capabilities that may coexist in one future implementation pull
  request;
- the deferred milestones that P1 does not satisfy;
- required ADR, plan, review, implementation, merge, and closeout gates; and
- the conditions under which the exception terminates.

## Non-goals

- Accepting or implementing P1 through this Proposed record.
- Reopening the broad Phase 3B interpretation or restoring pull request #60.
- General PDF parsing, scanning, active-content inspection, OCR, or B2
  completion.
- B3 lifecycle and recovery readiness.
- C0 identity or service authorization.
- C2 Memory Service, embedding, or Qdrant projection.
- D2 authenticated workspaces or O1 deployment and exposure.
- Real information, external sources, free-form questions, models, actions, or
  operational claims.
- Changing the accepted authority boundaries in ADRs 0011 through 0016.

## Decision drivers

- Deliver a complete user-visible learning loop rather than isolated plumbing.
- Preserve admission, approval, promotion, retrieval, presentation, and human
  authority as distinct responsibilities.
- Keep tests deterministic and independent from external services.
- Reuse bounded historical engineering without inheriting nonconforming
  architecture.
- Make the smallest exception that removes repeated product-disconnecting
  governance pauses.
- Keep rollback complete and prevent any real-information or deployment path.

## Considered alternatives

### Retain strict serial milestones

Implement B1, close it, then separately plan and implement B2, C1, C2, and D1.
This maximizes gate isolation but creates several increments that cannot satisfy
the first product outcome independently. It also forces repeated handoffs
before a user can observe the learning loop.

**Disposition:** Retained as the default for all work except the exact P1
exception.

### Restore or cherry-pick historical pull request #60

The historical branch already combines dashboard, promotion, retrieval,
memory, model, workspace, and deployment work. Reusing it wholesale would
restore the architecture and authority failures that B0 corrected, introduce
excluded capabilities, and make review evidence ambiguous.

**Disposition:** Rejected. File- or concept-level salvage is allowed only after
fresh implementation and tests inside accepted P1 boundaries.

### Implement only B1 before returning to product planning

This follows the current next milestone but leaves the Executive Product Shell
unchanged and proves no user-visible learning behavior.

**Disposition:** Rejected for P1 because it does not meet the authorized
planning objective. B1 remains available as a separate fallback if P1 is not
accepted.

### One bounded vertical-slice milestone

Combine only the minimal custody, exact-fixture evidence disposition,
metadata/content promotion, deterministic retrieval, read-model assembly, and
presentation changes needed for one synthetic question.

**Disposition:** Selected.

## Decision

If accepted and activated, P1 becomes one implementation milestone with this
complete journey:

```text
allowlisted question
    -> insufficient approved evidence
    -> exact generated synthetic PDF submission
    -> encrypted local custody
    -> digest-to-compiled-manifest evidence candidate
    -> explicit local human approval or rejection
    -> approved-only registry metadata and session projection
    -> deterministic retrieval
    -> evidence-bearing read model
    -> same question returns a changed grounded answer
```

P1 may implement these capability slices together:

| Existing milestone label | P1 slice | What remains unsatisfied |
| --- | --- | --- |
| B1 | Generated-PDF validation, identity, encrypted custody, audit, reset, and restart reconciliation | B1 is not generalized beyond the exact P1 fixture and policy |
| B2 | No general inspection; only exact-digest lookup of a compiled synthetic evidence manifest plus explicit human disposition | Scanner, native parser, active-content inspection, OCR, isolated workers, and general Human Review Workspace |
| B3 | Deterministic local reset and custody reconciliation only | Legal hold, backup, restore, recovery authority, rotation, and operational readiness |
| C0 | Compiled synthetic actor, consumer, and use identifiers only | Principals, authentication, authorization service, and multi-user boundaries |
| C1 | Approved-evidence promotion into registry metadata and a session-scoped content projection | Durable Knowledge Vault component, general producers/consumers, and real-domain policy |
| C2 | None | Memory Service and Qdrant relationship remains entirely deferred |
| D1 | One deterministic exact-policy retriever, citations, lineage, and read-model adapter | Model assistance, general query interface, service transport, and live consumers |
| D2/O1 | None | Authentication, workspaces, deployment, operation, and exposure remain deferred |

The exception applies only when all three conditions hold:

1. every byte and fact is generated synthetic information owned by reviewed
   repository fixtures;
2. no external service, model, vector store, deployment, authentication, or
   real-information path exists; and
3. the implementation remains inside the exact manifest and acceptance
   contract in the P1 plan.

P1 does not mark B2, B3, C0, C2, D2, or O1 complete. It does not generally mark
B1, C1, or D1 complete outside the exact synthetic pilot contract. The roadmap
continues to govern later generalized or operational work.

P1 also adopts one named, P1-only interface exception to ADR 0016's general
browser-pushed byte-stream contract. The fixed submit action invokes the
reviewed local fixture generator; the coordinator then calls the custody
boundary with those exact generated bytes under a signed synthetic receipt. No
caller byte, upload, path, URL, or content field exists. This exception does not
implement or supersede ADR 0016's general browser-push contract, and general B1
remains unsatisfied. A separate process-local `SyntheticFixtureAuthority`
adapter owns an ephemeral Ed25519 key for one pilot epoch, registers only its
public key after startup reconciliation under a fingerprint-derived signer-key
identity in the integrity-protected synthetic trust record, and issues one
short-lived receipt bound to the exact digest and policy. Old public keys remain
with safe audit/tombstone evidence; private keys are never persisted. Custody independently verifies and reserves the receipt;
neither custody nor the coordinator can issue its own authorization. This is a
synthetic authority simulation, not a real principal, delegation, revocation,
or operational trust/key-rotation claim.

P1 also narrows the local durability claim for supported host semantics. It
requires file flush and `fsync`, atomic same-volume exclusive publication to a
reserved absent final path without replacement, directory
`fsync` and restrictive permissions where the host exposes and verifies them,
and startup reconciliation on every host. Python on Windows cannot reliably
prove directory `fsync` or POSIX mode/ACL restriction, so P1 makes no
sudden-power-loss durability or OS-ACL guarantee on an unsupported host. This
is a P1-local exception to the stronger general Phase 3B lifecycle target, not
evidence that general B1/B3 durability is complete.

The closed retention profile is
`demo-p1-synthetic-program-outcomes-retention-policy` at version `1`. Its receipt is valid for at most
900 seconds; admission is exactly `application/pdf` and at most 65,536 bytes;
pending, processing, accepted, ready, or approved ciphertext expires no later
than 30 days from receipt; rejected or failed ciphertext expires no later than
7 days and is inaccessible immediately; safe audit/tombstones retain for 365
days. Receipt acceptance fixes the deadline, and no retry, review, approval,
restart, duplicate, or reconstruction extends it. P1 supports no legal hold,
backup, or restore; an integrity-failure held state remains mandatory and
ineligible.

[ADR 0019](0019-governed-synthetic-evidence-promotion.md) must be accepted in
the same architecture package before promotion implementation.
[ADR 0020](0020-executive-pilot-read-model-and-deterministic-retrieval.md) must
be accepted in the same package before retrieval or shell integration.

## Consequences

### Positive

- One implementation and review head can prove the complete product outcome.
- The dashboard remains the primary interface.
- Approval becomes an observable causal gate: no approval, no retrievable
  evidence, no changed answer.
- General parser, model, memory, identity, and deployment complexity remains
  outside P1.
- Historical code can be salvaged selectively without reviving its authority.
- The exception is testable, reversible, and bounded by exact fixtures and
  routes.

### Negative

- One implementation pull request crosses several responsibility boundaries
  and therefore requires stronger architecture and security review.
- P1 uses special synthetic mechanisms that are deliberately unsuitable for
  live documents or general queries.
- Session-scoped promoted content does not prove durable Knowledge Vault
  recovery.
- Later generalized milestones cannot claim completion from P1 and may replace
  its adapters.

### Neutral

- Existing accepted ADRs remain binding.
- The strict milestone sequence remains the default outside P1.
- P1 remains a local repository candidate and does not advance any component
  to Operational.

## Data and provenance impact

P1 uses generated synthetic information only. The generated fixture and its
manifest are reviewed demonstration source artifacts. Custody records and audit
events are synthetic operational records. The evidence candidate, registry
record, content projection, deterministic retrieval eligibility/result, read
model, and answer are derived.

The exact lineage must preserve fixture identity and version, PDF digest,
submission and custody identities, disposition identity and actor, registry and
projection identities, retrieval policy version, question identity, and answer
assembly time. Approval establishes eligibility for the exact synthetic use; it
does not establish factual truth or action authority.

## Security and privacy impact

P1 intentionally accepts no real or arbitrary source. A fixed fixture
identifier selects repository-generated bytes; the implementation exposes no
path, URL, paste, drag-and-drop, or free-form file surface. Unknown fixture,
question, action, digest, consumer, use, or state fails closed.

The future implementation adds local mutation and encrypted custody, so the
planning package requires request-body bounds, same-origin action protection,
safe redirects, output escaping, opaque identifiers, sanitized logging,
cryptographic dependency review, interruption tests, and negative-capability
tests. The local preview remains unauthenticated and must bind only to literal
`127.0.0.1`.

## Operations and recovery impact

No deployment or operational service is approved. P1 may prove local process
start, deterministic reset, encrypted custody restart reconciliation, and
fail-closed loss of session projections. It does not claim availability,
backup, restore, legal hold, key rotation, service objectives, or disaster
recovery.

## Compatibility and migration

The existing compiled-fixture provider and GET/HEAD routes remain available.
P1 adds a separately composed provider and allowlisted POST actions. No existing
runtime consumer or durable live data exists, so no data migration is required.

Rollback removes the P1 composition and its generated synthetic runtime state,
then restores the existing synthetic shell. A rollback must not relabel
remaining custody records as approved or retrievable.

## Validation

Acceptance requires review of the complete P1 plan, both dependent System
ADRs, threat model, dependency and salvage assessment, validation contract,
exact implementation manifest, and canonical planning reconciliation.

Implementation evidence must later prove the same question is insufficient
before approval, remains insufficient after submission and rejection, becomes
grounded only after approval, and returns complete lineage without exposing
prohibited content or capabilities.

Reconsider this decision if P1 requires arbitrary documents, general parsing,
an external dependency beyond the accepted cryptographic library, durable
promoted content, a model, vector storage, authentication, another user or
organization, real information, deployment, or files outside the approved
manifest.

## Follow-up work

- Complete independent architecture review of the exact planning head.
- Obtain Chief Architect acceptance or revision of all three Proposed ADRs.
- Activate statuses and implementation authority only through a separately
  reviewed exact-head decision.
- Implement only from the later canonical planning merge commit.
- Close out the implementation before any generalized milestone resumes.

## Related documents

- [P1 Pilot Implementation Plan](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Validation Requirements](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
- [P1 Threat Model](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_THREAT_MODEL.md)
- [P1 Dependency and Salvage Assessment](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_DEPENDENCY_AND_SALVAGE_ASSESSMENT.md)
- [P1 Execution Handoff](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_EXECUTION_HANDOFF.md)
- [P1 Planning Authorization](../governance/CHIEF_ARCHITECT_P1_PLANNING_AUTHORIZATION.md)
- [ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md)
- [ADR 0012](0012-executive-organizational-intelligence-interface-boundary.md)
- [ADR 0014](0014-knowledge-registry-domain-boundary.md)
- [ADR 0015](0015-executive-product-shell-and-local-preview-boundary.md)
- [ADR 0016](0016-local-governed-pdf-intake-and-custody-boundary.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

This decision creates one scoped exception to the reconciliation milestone
sequence. It does not erase or supersede the reconciliation record.

## Review record

The Chief Architect authorized preparation of this Proposed record through
`CA-2026-08-06-P1-PLANNING`. Independent architecture review, Chief Architect
acceptance, status activation, exact-head merge approval, and merge remain
pending. This record grants no implementation, deployment, or information-use
authority while Proposed.
