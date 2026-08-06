# Chief Architect P1 Planning Authorization

**Decision ID:** `CA-2026-08-06-P1-PLANNING`

**Status:** Authorized for planning only

**Decision date:** 2026-08-06

**Decision owner:** Chief Architect

**Recorded by:** Implementation Engineer

**Repository:** `matthewart100-sys/project-jebediah`

**Authorized canonical base:**
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

## Decision

Authorize P1 planning for the first complete, runnable Organizational
Intelligence pilot in the existing Executive Product Shell.

The planning owner may inspect canonical repository evidence and historical
pull requests #59 and #60, design the smallest complete end-to-end product
slice, prepare applicable Proposed ADRs, reconcile affected canonical planning
documents, define dependencies and salvage boundaries, specify tests and
acceptance evidence, and publish a review-ready documentation-only planning
pull request.

For this authorization, `runnable` means a future local application execution
that a separately authorized implementation can demonstrate. It does not mean
deployed, publicly exposed, operational, or connected to live organizational
information.

## Required P1 planning outcome

The package must be decision-complete for this user journey:

1. A user asks one allowlisted question in the existing Executive Product
   Shell.
2. The shell reports insufficient approved evidence.
3. One repository-generated synthetic PDF enters a governed custody path.
4. The candidate receives an explicit human approval or rejection disposition.
5. Only approved evidence is projected into a bounded knowledge representation.
6. The same question is asked again.
7. The answer changes only after approval and includes inspectable evidence
   lineage.

The package must define the architecture, exact implementation file manifest,
work breakdown, dependencies, salvage decisions, security boundaries,
validation evidence, branch and pull-request sequence, rollback, stop
conditions, and the exact next authority decision.

## Permitted planning activity

- Read-only inspection of current and historical repository artifacts.
- Documentation-only planning and architecture proposals.
- File- and function-level salvage classification for pull requests #59 and
  #60.
- Proposed reconciliation of the B0-through-D1 sequence for one bounded P1
  planning exception.
- Preparation of implementation-ready branch, pull-request, review, and
  handoff instructions.
- Local documentation validation and ordinary Git publication of the planning
  proposal.

## Explicit non-authorizations

This decision does not authorize:

- application, test, dependency, lock, workflow, service, container, runtime,
  database, infrastructure, deployment, DNS, certificate, or public-exposure
  changes;
- execution or deployment of historical pull-request #59 or #60 code;
- implementation of B1, B2, C1, C2, D1, or any later capability;
- real organizational information, VBA material, arbitrary files, personal
  data, or private operational evidence;
- parser, scanner, OCR, model, embedding, Qdrant, Ollama, authentication,
  multi-user, or production capability;
- acceptance of a Proposed ADR;
- implementation, merge, deployment, or information-use authority; or
- treating planning completeness as evidence that the pilot exists.

P1 may propose a bounded future architecture that crosses existing milestone
labels, but no proposal changes accepted architecture or current authority
until it receives the review, Chief Architect decision, status activation, and
merge required by the canonical coordination policy.

## Relationship to existing authority

Canonical `main` at the authorized base contains the completed B0 normal
revert and no active implementation authority. Pull request #63 remains a
separate proposed governance and B1-activation package. This authorization
does not accept, merge, depend on, or supersede pull request #63.

[ADR 0005](../adr/0005-project-coordination-and-role-authority.md) remains the
controlling coordination decision unless a successor is accepted and merged
before a P1 gate is exercised. The exact canonical coordination policy at each
review head controls reviewer and merge-operator mechanics.

The
[Phase 3B reconciliation decision](CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
remains binding. A proposed cross-milestone exception therefore requires a
Foundational ADR; promotion and read-model relationships require their own
System ADRs. This planning authorization permits those proposals but does not
pre-accept them.

## Completion condition

P1 planning is complete only when one documentation-only pull request contains:

- the complete Proposed ADR set;
- the implementation plan, validation contract, threat model, dependency and
  salvage assessment, and execution handoff;
- an exact proposed implementation manifest;
- consistent planning-only status across current sprint, project status,
  roadmap, ADR index, documentation index, and changelog;
- passing `python scripts/validate_docs.py` and `git diff --check` evidence;
- a complete exact-head handoff for independent architecture review; and
- no application, test, dependency, lock, workflow, runtime, deployment, or
  real-information change.

Completion of this planning package requests architecture review and a later
Chief Architect decision. It does not start implementation.

## Review record

The Chief Architect issued this planning authorization in conversation on
2026-08-06 against canonical base
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`. The planning pull request will
make the authorization durable only after normal review and merge. Exact-head
architecture review, ADR acceptance, implementation authorization, and every
implementation gate remain pending.
