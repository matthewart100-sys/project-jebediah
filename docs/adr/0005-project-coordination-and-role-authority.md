# ADR 0005: Project Coordination and Role Authority

**Status:** Proposed

**Date:** 2026-08-01

**Decision level:** Foundational

**Owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect; project maintainer for repository
custody impact

## Context

Project Jebediah already defines a maintainer, Chief Architect, and Lead
Engineer across its collaboration, sprint, glossary, and Codex guidance. It
does not define Work Mode, the Documentation Suite, or the future Jebediah
Runtime as distinct roles, and it does not assign one canonical owner to the
full plan-to-closeout workflow.

This creates several risks:

- a reviewer can be mistaken for the final architecture authority
- an implementer can infer permission from a plan or review pass
- documentation can precede or overstate a merge
- a future runtime can be treated as an authority rather than a consumer
- handoffs can omit the exact commit, evidence, blocker, or requested decision
- overlapping role text can drift across governance documents
- maintainer custody can be mistaken for Chief Architect scope authority
- an undefined emergency path can bypass mandatory review gates
- a Work Mode blocker can become either an unintended permanent veto or an
  undocumented override
- an implementer can relabel itself as the independent reviewer of its own
  artifact
- a context-isolated handoff can identify a branch or commit without the
  repository, workstream, pull request, or base/head relationship needed to
  resolve it safely

A permanent operating model changes project-wide authority and gates. That is
a Foundational decision under the
[ADR Process](README.md).

## Decision

Adopt the
[Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
as the canonical owner of cross-role authority, mandatory workflow gates,
handoff packet fields, and coordination evidence labels.

The protocol establishes:

- the Chief Architect as final decision maker for strategy, architecture,
  scope, ADR acceptance, sprint authorization, merge approval, and roadmap
  direction
- Codex as Implementation Engineer within approved scope
- Work Mode as independent architecture and quality reviewer with blocking but
  not final approval authority
- the Documentation Suite as Documentation Lead after approved merges
- the future Jebediah Runtime as a consumer without current engineering
  authority
- same-artifact independence: an author or implementer cannot satisfy Work
  Mode review for the artifact it created or materially modified
- written Chief Architect disposition of every Work Mode blocker, preventing
  both silent override and unintended permanent veto
- a narrowly bounded emergency path in which only pre-implementation Work Mode
  architecture review may be deferred, while Chief Architect authorization and
  every merge gate remain mandatory
- context-complete handoffs that identify repository, workstream, pull request
  or issue, and exact base/head relationship
- proportional review paths for editorial documentation,
  architecture-significant documentation, and post-merge closeout

The mandatory sequence is:

**PLAN → Work Mode architecture review → Chief Architect approval → Codex
implementation → Work Mode implementation validation → Chief Architect merge
approval → Codex controlled merge → Documentation Suite closeout**

The
[Documentation Lead Protocol](../governance/JEBEDIAH_DOCUMENTATION_LEAD_PROTOCOL.md)
defines the subordinate documentation-only closeout procedure.

Merging an approved Documentation Suite closeout pull request completes that
closeout and does not recursively create another closeout requirement.

## Alternatives considered

### Retain informal role coordination in conversations

Rejected because conversation history is not durable project memory and does
not protect authority boundaries for future contributors.

### Keep the existing three-role model without Work Mode or Documentation Suite

Rejected because independent validation and post-merge documentation closeout
would remain implicit and inconsistently handed off.

### Allow each tool or workflow to define its own authority

Rejected because tool capability is not project authority and parallel role
definitions would drift.

### Give Work Mode final architecture approval

Rejected because independent challenge and final strategic accountability
must remain separate.

### Grant the future Runtime authority over engineering state

Rejected because runtime output is derived operational evidence and cannot
authorize its own design, scope, or repository changes.

## Consequences

### Positive

- Every engineering stage has one accountable role and explicit entry gate.
- Independent review is required before implementation and merge decisions.
- Merge approval is separated from merge execution and verification.
- Documentation closeout is based on confirmed merged state.
- Handoffs carry consistent commits, evidence, risks, blockers, and next
  actions.
- Emergency corrections retain pre-implementation authority, retrospective
  independent review, and all merge controls.
- Blocking findings have a traceable final disposition without transferring
  final architecture authority to Work Mode.
- Context-isolated reviewers can resolve the exact repository, workstream,
  pull request, and base/head comparison from the packet alone.
- Future Runtime behavior cannot silently become project authority.

### Negative

- Even small implementation-bearing work has more explicit handoffs.
- A role holder may transition between roles for unrelated artifacts, but the
  author or implementer cannot act as Work Mode for the same artifact.
- Work can pause when an assigned review role is unavailable.
- Written blocker dispositions and sensitive-evidence retention add governance
  overhead.

### Neutral

- GitHub `main` remains the authoritative project memory.
- Existing Git, documentation, testing, security, operations, release, and
  Definition of Done requirements remain binding.
- Accepted ADRs 0001 through 0004 are not changed or superseded.
- The decision changes governance only; it does not change runtime behavior,
  APIs, infrastructure, deployment, or live data.

## Compatibility and migration

Existing role references are reconciled by linking to the coordination
protocol and removing conflicting authority language. Historical pull
requests and decisions remain valid under the authority recorded at their
time.

Repository custody remains with the maintainer, while sprint, scope,
architecture, ADR, roadmap, and merge decisions remain with the Chief
Architect. Documentation changes are classified before work so editorial
corrections do not inherit architecture review gates and
architecture-significant changes cannot hide behind an editorial label.

This decision does not authorize Sprint 006 or any implementation. Work in
progress at the time of acceptance must identify its current gate and produce
the required next handoff rather than replaying already completed, reviewed
stages without cause.

## Failure and recovery

Before merge, reject or revise this proposal without runtime effect. After
acceptance, a documentation-only Git revert can restore the prior governance
text, but any lasting replacement of authority or gate order requires a new
ADR that explicitly supersedes this record.

When a required role is unavailable, work stops at that role's gate. No other
role silently substitutes its approval. The Chief Architect may explicitly
assign a qualified role holder without collapsing the defined authorities or
allowing an author or implementer to independently review the same artifact.

In an engineering emergency, the Chief Architect may defer only the
pre-implementation Work Mode architecture review for the smallest reversible
correction. Chief Architect authorization remains required before work, and
the deferred review, independent implementation validation, all required
checks, blocker disposition, exact-head approval, and controlled merge remain
required before merge.

## Security and privacy

Handoff evidence must contain no credentials, private addresses, personal
data, raw sensitive logs, or exploitable topology. Sensitive evidence remains
in an approved access-controlled location with an owner, retention period, and
integrity information sufficient for authorized re-verification. The public
packet records only a sanitized result, commit, method, environment class,
date, custodian, and an opaque private evidence identifier when safe. A
required validation claim remains blocked if no approved evidence-retention
path exists.

## Validation

Acceptance requires:

- Work Mode architecture review of the actual protocol and integration diff
- Chief Architect approval of this ADR and the exact protocol artifacts
- proof that maintainer custody does not grant sprint or scope authority
- proof that emergency work can defer only pre-implementation Work Mode
  architecture review and cannot bypass Chief Architect authorization or any
  merge gate
- proof that every Work Mode blocker has a written Chief Architect disposition
  path without silent override or permanent veto
- proof that the author or implementer cannot satisfy same-artifact Work Mode
  review through a role transition
- a handoff packet containing repository identity, workstream, pull request or
  issue, and exact base/head relationship
- explicit review paths for editorial documentation,
  architecture-significant documentation, and terminal post-merge closeout
- defined sanitized and private retention metadata for sensitive validation
  evidence
- consistent authority language in agent, collaboration, sprint, glossary,
  documentation, and contributor guidance
- valid documentation links and indexes
- `python scripts/validate_docs.py`
- `git diff --check`
- proof that the diff contains documentation only

## Related documents

- [Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
- [Documentation Lead Protocol](../governance/JEBEDIAH_DOCUMENTATION_LEAD_PROTOCOL.md)
- [AI Collaboration Standard](../../.ai/COLLABORATION.md)
- [Documentation Standards](../DOCUMENTATION_STANDARDS.md)
- [Sprint Process](../SPRINT_PROCESS.md)
- [Git Workflow](../GIT_WORKFLOW.md)
- [Definition of Done](../DEFINITION_OF_DONE.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Work Mode reviewed pull request 41 at head
`c114dd6282ba09138e5c9412e10cf62a36c754fa` and returned `CHANGES REQUIRED
BEFORE ACCEPTANCE`. This revision addresses maintainer-versus-Chief-Architect
scope authority, emergency gate behavior, blocker disposition, same-artifact
reviewer independence, context-complete handoffs, proportional documentation
paths, terminal closeout, and sensitive-evidence retention.

The ADR remains `Proposed` pending independent Work Mode review of the revised
head and Chief Architect acceptance. After that acceptance, the status change
to `Accepted` creates a new head that must itself receive the required Work
Mode review and Chief Architect exact-head merge approval before merge. No
implementation, sprint, merge, deployment, or live-system authority is granted
by this proposed ADR.
