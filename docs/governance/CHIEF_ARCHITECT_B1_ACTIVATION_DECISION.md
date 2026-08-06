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
- PDF signature and structural, MIME, and configurable size validation;
- SHA-256 document identity and opaque metadata;
- encrypted local quarantine and staging custody;
- deterministic custody paths, admission identifiers, lifecycle states, and
  audit events;
- duplicate detection, expiration, deletion, reset, recovery, failure
  isolation, and interruption-safe persistence;
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

Historical pull requests #59 and #60 remain audit and salvage evidence. They
must not be merged, deployed, restored wholesale, or treated as accepted
implementation.

## Routine independent review policy

The routine milestone workflow is:

**Chief Architect authorization -> Codex implementation and validation ->
independent read-only normal-chat review -> Chief Architect exact-head decision
-> merge -> post-merge validation**

Routine exact-head review does not require Work Mode. Work Mode may be used
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
2. A fresh normal-chat reviewer inspects its exact pull-request head read-only.
3. The Chief Architect decides whether that unchanged head may merge.
4. Only after merge may Codex begin B1 implementation from the authorized
   base, updated to the then-current canonical merge commit as required by the
   Git workflow.

A changed reviewed head reopens independent review and Chief Architect
decision. Repository merge does not authorize deployment, real-information
use, B2, or any other excluded capability.

## ADR impact

ADR 0016 remains Accepted and unbroadened. This decision selects only its
smallest generated-synthetic-PDF custody subset and expressly excludes its
inspection, OCR, human-review, real-information, downstream consumer, and
deployment design. No new ADR is accepted by this decision.

## Rollback

Before B1 implementation merges, rollback is an ordinary revert of this exact
documentation package. Reverting the activation removes B1 implementation
authority and restores the prior routine review policy; it does not rewrite
the historical B0, pull request #59, pull request #60, or ADR 0016 records.
