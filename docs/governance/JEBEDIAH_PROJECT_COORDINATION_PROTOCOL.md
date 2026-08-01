# Jebediah Project Coordination Protocol

**Status:** Proposed; becomes active only after the required review and merge
to `main`

**Decision level:** Foundational under
[ADR 0005](../adr/0005-project-coordination-and-role-authority.md)

## Purpose

This protocol defines Project Jebediah's permanent multi-role operating model.
It owns cross-role authority, mandatory engineering gates, handoff contents,
and evidence labels. It prevents a tool, chat, reviewer, implementer,
documentation process, or future runtime from silently acquiring authority
assigned to another role.

The [AI Collaboration Standard](../../.ai/COLLABORATION.md) governs day-to-day
human and AI collaboration. The
[Documentation Lead Protocol](JEBEDIAH_DOCUMENTATION_LEAD_PROTOCOL.md) governs
documentation closeout. Neither may redefine the authority or gates in this
protocol.

## Scope and non-goals

This protocol governs planning, architecture review, implementation review,
merge authorization, controlled merge, and post-merge documentation closeout.
It does not:

- define product or runtime architecture
- authorize a sprint, feature, deployment, migration, or live-system action
- define Sprint 006
- replace the [Git Workflow](../GIT_WORKFLOW.md),
  [ADR Process](../adr/README.md), or
  [Definition of Done](../DEFINITION_OF_DONE.md)
- make a conversation, model response, or external research source canonical
- grant the future Jebediah Runtime engineering or governance authority

## Operating roles

### Chief Architect

The Chief Architect is the final decision maker for:

- project strategy
- architecture and architectural boundaries
- scope definition and scope changes
- ADR acceptance, rejection, or revision
- sprint authorization
- merge approval
- roadmap direction and priority

The Chief Architect may approve, reject, block, or require revision. Decisions
must identify the reviewed artifacts, evidence, and exact authorized next
action. The Chief Architect does not perform implementation work by default
and does not make an unreviewed conversation canonical.

Repository administration, credentials, licensing, and legal ownership may
remain with a human maintainer or custodian. Custody of those controls does
not silently transfer the Chief Architect's decision authority. A person
holding more than one role must state which role is acting at each gate.

### Codex — Implementation Engineer

Codex converts approved direction into bounded, reviewable repository work.
Codex:

- inspects repository evidence and creates implementation plans
- executes only approved work
- writes or updates tests when implementation scope requires them
- runs required validation
- prepares architecture, implementation, merge, and closeout handoff packets
- performs a controlled merge only after explicit Chief Architect approval
- verifies the merged state and reports exact results

Codex may identify contradictions, risks, and missing decisions. It must not
redefine architecture, expand scope, accept an ADR, authorize a sprint, or
grant its own merge approval.

### Work Mode — Independent Architecture and Quality Reviewer

Work Mode independently reviews plans and implementation artifacts. Work Mode:

- challenges assumptions and unsupported claims
- checks alignment with current architecture, accepted ADRs, scope, and
  governance guarantees
- requires actual artifacts and reproducible evidence
- identifies blocking defects, risks, and missing validation
- may block implementation or merge until required corrections are complete

Work Mode does not perform final architecture approval and cannot override the
Chief Architect. A Work Mode pass is required evidence for the next Chief
Architect decision; it is not that decision.

### Documentation Suite — Documentation Lead

The Documentation Suite maintains the Master Documentation Suite after
approved merges. It:

- reconciles canonical documentation with confirmed merged reality
- distinguishes implemented behavior from future design
- records exact merge and validation evidence
- preserves deferred work, risks, and unresolved questions
- identifies documentation gaps and routes them to the proper authority

The Documentation Suite changes documentation only within an authorized
documentation task. It may not invent system behavior, change architecture,
reprioritize the roadmap, define a sprint, or silently mark future work
complete. Its detailed operating rules are in the
[Documentation Lead Protocol](JEBEDIAH_DOCUMENTATION_LEAD_PROTOCOL.md).

### Jebediah Runtime — Future Operational Consumer

The Jebediah Runtime is a future consumer of approved project state. It may
use only information that is approved, merged, validated, and documented for
its intended operational purpose.

The Runtime is not currently an engineering authority. It may not approve
architecture, change scope, accept ADRs, authorize work, merge changes, or
rewrite project memory. Any future operational or automated authority requires
an explicitly approved sprint and the appropriate ADR, security, data,
operations, and recovery review.

## Authority matrix

| Decision or action | Accountable role | Required contributors | Prohibited substitution |
| --- | --- | --- | --- |
| Strategy and roadmap direction | Chief Architect | Work Mode may challenge; Codex may provide feasibility evidence | No tool or runtime may reprioritize work |
| Architecture and ADR acceptance | Chief Architect | Work Mode reviews; Codex supplies artifacts | Work Mode may block but may not give final approval |
| Sprint and scope authorization | Chief Architect | Codex plans; Work Mode reviews architecture | Codex may not self-authorize or expand scope |
| Implementation | Codex | Chief Architect supplies approved scope | Review or documentation roles do not implement by default |
| Implementation validation | Work Mode | Codex supplies evidence and corrections | A self-review alone cannot satisfy independent review |
| Merge approval | Chief Architect | Work Mode supplies implementation disposition | Codex may not grant its own merge authority |
| Controlled merge and merge verification | Codex | Chief Architect identifies the exact approved artifacts | Approval does not itself perform or prove the merge |
| Documentation closeout | Documentation Suite | Codex supplies merged commit and validation evidence | Documentation may not precede or manufacture merged reality |
| Operational consumption | Jebediah Runtime | Approved future interfaces and policy | Runtime output is not engineering authority |

## Mandatory workflow

Every implementation-bearing change follows this order:

**PLAN → Work Mode architecture review → Chief Architect approval → Codex
implementation → Work Mode implementation validation → Chief Architect merge
approval → Codex controlled merge → Documentation Suite closeout**

### 1. Plan

Codex or another authorized planner defines the problem, outcome, scope,
non-goals, acceptance criteria, affected architecture and ADRs, dependencies,
risks, validation, rollback, and requested decision.

### 2. Work Mode architecture review

Work Mode reviews the actual plan and relevant repository evidence. It returns
blocking corrections, non-blocking risks, and an explicit review disposition.
Unresolved blocking findings stop the workflow.

### 3. Chief Architect approval

The Chief Architect reviews the plan and Work Mode evidence. Approval must
identify the exact scope and next action. Approval to implement is not merge,
deployment, or live-system authority.

### 4. Codex implementation

Codex implements only the approved scope on a reviewable branch, preserves
unrelated work, validates incrementally, and records any condition that
invalidates the approved plan.

### 5. Work Mode implementation validation

Work Mode reviews the exact implementation, tests, validation output, diff,
and remaining risk. Blocking findings return to Codex for bounded correction
and revalidation.

### 6. Chief Architect merge approval

The Chief Architect reviews the final implementation packet and Work Mode
disposition. Merge approval names the exact pull request and head commit. A
changed head invalidates the approval unless the Chief Architect explicitly
approves the new artifacts.

### 7. Codex controlled merge

Codex confirms branch, commit, files, checks, and approval; applies the
repository's established merge method; updates local `main`; reruns required
post-merge validation; and reports the final commit and clean status. It does
not deploy or mutate live systems unless separately authorized.

### 8. Documentation Suite closeout

After the merge is proven, the Documentation Suite reconciles status,
changelog, roadmap, plans, validation records, indexes, and other affected
canonical documentation without adding unapproved behavior or future scope.

## Mandatory gates

### No implementation without

- a defined scope and non-goals
- architecture review by Work Mode
- explicit Chief Architect approval for the exact plan

If any item is absent, Codex stops before implementation and requests the
missing decision or evidence.

### No merge without

- exact implementation evidence
- all required validation passing or a reviewed exception
- Work Mode implementation review with no unresolved blocker
- explicit Chief Architect approval for the exact pull request and head commit

If the head commit changes after approval, the merge gate reopens.

### No documentation closeout before

- the approved merge succeeds
- local `main` is clean and synchronized with the authoritative remote
- the final merged commit is confirmed

A release, deployment, or live-system claim requires its own evidence and is
not implied by a successful repository merge.

## Handoff packet contract

Every role-to-role handoff contains all of these fields. Use `Not applicable`
with a reason rather than silently omitting a field.

| Field | Required content |
| --- | --- |
| Current sprint | Sprint name and status, or an explicit statement that no active sprint is authorized |
| Branch | Exact local and remote branch relevant to the handoff |
| Commit hash | Full reviewed or merged commit hash |
| Related ADRs | Accepted, proposed, superseded, or not-applicable ADRs and their effect |
| Scope | Included outcome and explicit non-goals |
| Evidence | Actual files, diff, tests, validation, reviews, and source labels |
| Risks | Known residual, compatibility, security, operations, recovery, and documentation risks |
| Blockers | Unresolved conditions that stop the requested action, or `None` |
| Requested decision | One decision the receiving role is authorized to make |
| Exact next action | One bounded action, owner, target, and stop condition |

Role-specific handoffs add:

- **Chief Architect:** decision, reviewed artifacts, authority granted or
  withheld, and the next permitted gate.
- **Codex:** exact changed files, commands and results, working-tree status,
  implementation limitations, and rollback point.
- **Work Mode:** review method, blocking findings, recommendations, evidence
  gaps, and review disposition.
- **Documentation Suite:** merged commit, documents reconciled, claims left
  deferred, link and documentation validation, and unresolved documentation
  gaps.
- **Jebediah Runtime:** once authorized, consumed version, policy and interface
  identity, operational evidence, rejected or stale inputs, and escalation
  request. Runtime output never constitutes an approval.

## Evidence labels

These labels classify evidence in handoff and review packets. They supplement,
but do not replace, the evidence categories in
[Documentation Standards](../DOCUMENTATION_STANDARDS.md).

### Repository Verified

A claim directly supported by inspected repository state, preferably reviewed
`main`, an exact commit, or a pull-request diff. The packet identifies the
path and commit.

### Validation Verified

A claim supported by a completed test, validator, build, smoke test, or
controlled system check. The packet identifies the command or method, target
commit, environment, and result. Validation does not prove facts outside the
tested boundary.

### Architecture Decision

A decision made by the Chief Architect and recorded in the appropriate
canonical artifact, accepted ADR, or reviewed pull request. A proposed or
conversation-only decision is not labeled `Architecture Decision`.

### Future Design

An approved direction, proposal, or open design that is not implemented and
must not be described as current behavior. The label identifies its approval
state and implementation gate.

### Research Reference

External or exploratory material used for context. It may inform analysis but
does not establish repository state, architecture, product authority, or
validation success.

## Authority and conflict rules

- No role may silently assume another role's authority.
- Work Mode may block implementation or merge but may not give final
  architecture approval.
- Codex may implement approved work but may not redefine architecture or
  scope independently.
- The Documentation Suite may document confirmed state but may not invent
  system behavior or roadmap priority.
- The Chief Architect is the final decision maker within the authority listed
  in this protocol.
- The future Jebediah Runtime consumes approved state only and has no current
  engineering authority.
- A person or tool performing multiple roles must announce each role
  transition and satisfy the evidence gate between them.
- Repository state, validation evidence, and architecture decisions remain
  distinct. One label must not be used as a substitute for another.

When instructions or canonical documents conflict, stop dependent work,
identify the conflicting owners, preserve the current state, and request a
Chief Architect decision. Update the canonical owner through review before
resuming.

## Record and maintenance

Plans, findings, approvals, merges, and closeouts become durable only through
reviewed GitHub artifacts. Chat transcripts are not copied as authority.
Sensitive evidence remains in an approved private channel while the public
record contains only a sanitized conclusion and verification method.

Changes to role authority, mandatory gate order, or final decision ownership
are Foundational decisions and require a new or superseding ADR plus Chief
Architect review. Editorial corrections may use the normal documentation
workflow when they do not change meaning.

Historical plans, changelog entries, and review records may retain earlier
role names or authority wording as evidence of the process in effect at that
time. Any new or resumed work follows this protocol after it becomes active.
