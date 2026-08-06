# Chief Architect B1 Activation Decision

**Decision ID:** `CA-2026-08-06-B1-ACTIVATION`

**Status:** Approved for canonicalization; effective only after this activation
package is independently reviewed, approved for the exact head, and merged

**Decision owner:** Chief Architect

**Authorized base:** `37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

## Decision

Activate **B1 - Synthetic Custody Foundation** as the next bounded milestone
after canonical B0 recovery. Replace mandatory Work Mode review for routine
milestones with independent read-only review in a fresh normal ChatGPT
conversation. Preserve Codex as implementer, the independent reviewer as a
read-only reviewer, and the Chief Architect as the sole exact-head decision
authority. Codex may not approve or merge its own work.

This decision authorizes only this documentation activation package until it
merges. B1 implementation authority becomes effective after that merge.

## Authorized B1 scope

- generated synthetic PDF fixtures only;
- local or loopback-only programmatic custody;
- fail-closed PDF signature, bounded structural, MIME, and configurable size
  validation without text extraction, OCR, active-content inspection, native
  parser workers, scanner workers, or containerized inspection;
- SHA-256 document identity and opaque metadata;
- encrypted local quarantine and staging custody;
- deterministic custody paths, admission identifiers, lifecycle states, and
  audit events;
- duplicate detection, expiration, deletion, reset, failure isolation,
  interruption-safe persistence, and deterministic restart reconciliation of
  generated-synthetic custody state;
- deterministic automated tests and package/import boundaries; and
- file-level reuse or adaptation of appropriate custody engineering from pull
  requests #59 and #60 after inspection.

## Explicit exclusions

B1 does not authorize real documents, VBA information, arbitrary production
ingestion, text extraction, OCR, summarization, evidence or knowledge
promotion, Knowledge Objects, Knowledge Registry integration, memory writes,
embeddings, Qdrant, retrieval, models, grounded answers, question answering,
executive-dashboard integration, production workspaces, deployment, Docker
production work, Caddy, Cloudflare, DNS, domain work, public exposure, GPU
routing, or B2 and later milestones.

B2 retains scanner/native-parser workers, active-content inspection, text
extraction, OCR, container isolation, and human review. B3 retains legal hold,
backup creation, backup restore, recovery-authority ledgers and attestations,
key or trust rotation, operational recovery readiness, and any real-data
retention profile. B1 restart reconciliation does not activate those B2 or B3
capabilities.

Historical pull requests #59 and #60 remain audit and salvage evidence. They
must not be merged, deployed, restored wholesale, or treated as accepted
implementation.

## Proposed routine independent review policy

After ADR 0017 is accepted and merged, the routine milestone workflow is:

**Chief Architect authorization -> Codex implementation and validation ->
independent read-only normal-chat review -> Chief Architect exact-head decision
-> merge -> post-merge validation**

Under the successor policy, routine exact-head review does not require Work
Mode. Work Mode may be used
only when explicitly requested for unusually high-risk, cross-cutting, or
adversarial review. Major architecture or security-boundary changes still
require full independent review, but the reviewer need not use Work Mode.

The independent normal-chat review must:

- occur in a fresh conversation that did not author or modify the artifacts;
- inspect the actual supplied pull request, exact base and head, complete diff,
  commits, validation, and relevant authority records;
- remain read-only and identify evidence limitations honestly;
- return exactly `APPROVED`, `REVISIONS REQUIRED`, or `BLOCKED`;
- not modify GitHub, merge, act as Chief Architect, or begin the next
  milestone.

## Activation and merge gates

1. Codex prepares this documentation-only activation package.
2. Because ADR 0005 controls the transition, Work Mode independently reviews
   the exact ADR 0017 proposal and reconciliation head. A fresh read-only
   normal-chat review may provide additional evidence but cannot replace this
   incumbent gate.
3. The Chief Architect decides whether to accept ADR 0017 for that exact head.
4. After acceptance, Codex publishes the status, reciprocal-supersession, and
   review-record update as a new exact head.
5. Work Mode independently reviews that changed exact head, and the Chief
   Architect separately decides whether it may merge.
6. A non-author Merge Operator executes the unchanged exact approved merge;
   Codex may verify but may not merge its own work.
7. Only after merge may Codex begin B1 implementation from the authorized
   base, updated to the then-current canonical merge commit as required by the
   Git workflow.

A changed reviewed head reopens independent review and Chief Architect
decision. Repository merge does not authorize deployment, real-information
use, B2, or any other excluded capability.

## ADR impact

ADR 0016 remains Accepted and unbroadened. This decision selects only its
smallest generated-synthetic-PDF custody subset and expressly excludes its
inspection, OCR, human-review, real-information, downstream consumer, and
deployment design.

[ADR 0017](../adr/0017-project-coordination-and-independent-review-authority.md)
is the proposed Foundational successor to ADR 0005 for project coordination and
independent-review authority. On 2026-08-06, the Chief Architect authorized its
preparation and the required canonical reconciliation. ADR 0005 remains
controlling until ADR 0017 receives its incumbent transitional review,
exact-head Chief Architect acceptance, status and reciprocal-supersession
update, fresh incumbent Work Mode exact-head review, final merge approval, and
merge.

## Rollback

Before B1 implementation merges, rollback of B1 activation is an ordinary
revert of its exact canonical documentation package. Reverting B1 activation
removes B1 implementation authority but does not restore a superseded review
policy. After ADR 0017 is accepted and merged, a lasting return to mandatory
Work Mode requires another Foundational ADR. Rollback does not rewrite the
historical B0, pull request #59, pull request #60, ADR 0005, or ADR 0016
records.
