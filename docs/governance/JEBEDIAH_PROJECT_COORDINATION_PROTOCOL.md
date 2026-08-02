# Jebediah Project Coordination Protocol

**Status:** Accepted by the Chief Architect on 2026-08-01; becomes active after
the required exact-head review and merge to `main`

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
Chief Architect. A Work Mode review disposition is required evidence for the
next Chief Architect decision; it is not that decision. A blocking finding
pauses work until it is corrected or receives the explicit Chief Architect
disposition defined below; it does not create an undocumented permanent veto.

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
| Implementation validation | Work Mode | Codex supplies evidence and corrections | The author or implementer may not review the same artifact as Work Mode |
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
Blocking findings stop the workflow until corrected or explicitly disposed by
the Chief Architect under the blocker-disposition rules below.

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
and revalidation or to the Chief Architect for an explicit disposition.

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
Merging the approved closeout pull request completes that closeout; it does not
recursively require a second closeout for the closeout itself.

## Mandatory gates

### No implementation without

Except for the narrowly bounded emergency deferral defined below, no
implementation begins without:

- a defined scope and non-goals
- architecture review by Work Mode
- explicit Chief Architect approval for the exact plan

If any item is absent, Codex stops before implementation and requests the
missing decision or evidence.

### No merge without

- exact implementation evidence
- all required validation passing or a reviewed exception
- Work Mode implementation review with every blocking finding corrected or
  explicitly disposed by the Chief Architect under this protocol
- explicit Chief Architect approval for the exact pull request and head commit

If the head commit changes after approval, the merge gate reopens.

### No documentation closeout before

- the approved merge succeeds
- local `main` is clean and synchronized with the authoritative remote
- the final merged commit is confirmed

A release, deployment, or live-system claim requires its own evidence and is
not implied by a successful repository merge.

## Emergency implementation path

Only the Chief Architect may declare a repository engineering emergency. The
declaration records the active risk, affected scope, exact authorized
containment or correction, evidence available, time boundary, rollback, and
the single gate being deferred.

An emergency exists only when delay would materially worsen an active threat
to security, data integrity, service availability, or repository access. The
Chief Architect may defer the pre-implementation Work Mode architecture review
long enough to perform the smallest reversible correction. Chief Architect
authorization before implementation may not be deferred. If that authority is
unavailable, repository implementation remains blocked.

Emergency work may not introduce or change architecture, ADR decisions,
roadmap priority, sprint scope, interfaces, features, migrations, or broad
refactors. It may not authorize deployment, live-data mutation, or another
external action unless that action has its own explicit authority under the
applicable security and operations rules.

Before an emergency correction may merge:

1. Work Mode performs the deferred architecture review and implementation
   validation on the exact artifacts.
2. Every finding receives the normal correction or Chief Architect
   disposition.
3. Required validation and the Definition of Done pass, or a permitted
   exception is recorded.
4. The Chief Architect approves the exact pull request and head commit.
5. Codex uses the normal controlled merge and post-merge process.

No merge gate is deferred. The pull request records the emergency declaration,
deferred gate, retrospective review, decisions, validation, and follow-up work.
Operational containment that does not change the repository follows separately
authorized security or operations procedures and does not weaken this path.

## Work Mode blocker disposition

Work Mode classifies each finding as a reproducible evidence or validation
failure, an architecture or quality concern, or a non-blocking recommendation.
A blocking finding must identify the affected artifact, evidence, risk, and
condition required to clear it.

The Chief Architect disposes each blocking finding in writing by exactly one
of these actions:

- **Sustain:** require correction and revalidation before the next gate.
- **Resolve:** determine from cited evidence that the condition is corrected,
  inapplicable, or factually unsupported.
- **Reclassify:** accept a non-prohibited residual risk through a documented
  architecture decision or permitted exception that records rationale,
  consequence, owner, and a review or expiration condition.

The Chief Architect may not relabel a failed required check, exposed sensitive
data, missing legal or repository authority, or another non-waivable boundary
as passing. Exceptions are valid only where the owning standard and the
[Definition of Done](../DEFINITION_OF_DONE.md) permit them.

Once every blocker has a recorded disposition, Work Mode cannot create an
unintended permanent veto. Changed artifacts still require the applicable
independent re-review, and the Chief Architect must approve the exact final
head before merge. Silent override, omission, or unexplained reclassification
is prohibited.

## Proportional documentation paths

Documentation work is classified by its effect before editing:

### Editorial documentation correction

An editorial correction changes spelling, formatting, or a broken reference
without changing meaning, authority, status, scope, roadmap priority, ADR
content, or a claim about runtime behavior. It requires a documentation-only
diff, documentation and link validation, whitespace validation, and Chief
Architect merge approval for the exact head. The Work Mode architecture and
implementation-review gates are not required unless the classification is
disputed or the diff changes meaning.

### Architecture-significant documentation

Documentation that changes authority, architecture, ADR meaning or status,
scope, roadmap priority, interfaces, or lasting technical direction follows
the full mandatory workflow, including independent Work Mode review before
implementation and before Chief Architect merge approval.

### Documentation Suite closeout

A post-merge closeout begins from the confirmed merge handoff rather than a new
feature plan. The Documentation Suite prepares only the authorized canonical
reconciliation. Work Mode performs an independent documentation and evidence
review, and the Chief Architect grants or withholds merge approval for the
exact closeout head. The merge of that approved pull request is the terminal
closeout event and does not trigger another mandatory closeout.

If a documentation change does not clearly fit a path, work pauses for Chief
Architect classification. A documentation label may not be used to bypass an
architecture or implementation gate.

## Handoff packet contract

Every role-to-role handoff contains all of these fields. Use `Not applicable`
with a reason rather than silently omitting a field.

| Field | Required content |
| --- | --- |
| Repository identity | Exact `owner/name` and authoritative remote URL |
| Current sprint | Sprint name and status, or an explicit statement that no active sprint is authorized |
| Workstream / pull request / issue | Workstream name plus exact pull request and issue or work-item identifiers or URLs; use `Not applicable` with a reason |
| Branch | Exact local and remote branch relevant to the handoff |
| Commit hash | Full reviewed or merged commit hash |
| Base/head relationship | Base branch and full commit, head branch and full commit, and the compare or diff target |
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

When raw validation evidence is sensitive, the public packet records a
sanitized result, commit, command or method, environment class, date, evidence
custodian, and an opaque private evidence identifier when safe. The raw record
must remain in an approved access-controlled location with an owner, retention
period, and enough integrity information for authorized re-verification. If no
approved retention path exists for evidence required by a gate, the claim is
not `Validation Verified` and the gate remains blocked.

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
- The person, tool, chat, session, or process that authored or materially
  modified an artifact may not satisfy Work Mode's independent review for that
  same artifact merely by announcing a role transition.
- Work Mode review for an artifact must be performed by a distinct review
  instance that did not author or modify it. If none is available, the review
  gate remains blocked.
- Repository state, validation evidence, and architecture decisions remain
  distinct. One label must not be used as a substitute for another.

When instructions or canonical documents conflict, stop dependent work,
identify the conflicting owners, preserve the current state, and request a
Chief Architect decision. Update the canonical owner through review before
resuming.

## Architecture proposal chain of custody

A multi-document architecture proposal is a review target whose substantive
design spans more than a single ADR, including a combination of proposed
specifications, plans, ADRs, or architecture documents. Required index updates
belong in its artifact manifest but do not by themselves turn one ADR into a
multi-document proposal. Authoring these planning artifacts is not
implementation and does not grant implementation, merge, deployment, or
live-system authority.

Before Work Mode begins independent architecture review of a multi-document
proposal:

- every proposal artifact and required index update must exist on one
  short-lived remote branch in the authoritative repository
- the proposal must be committed, and the handoff must identify the full base
  and head commit hashes
- the handoff must include the complete artifact manifest and an accessible
  pull-request diff, compare link, or equivalent repository-backed diff
- the proposal worktree must contain no uncommitted or untracked artifact that
  is necessary to interpret the review target
- Work Mode must verify that the repository head and manifest resolve before
  treating the review as evidence

The worktree requirement is scoped to the proposal review target. It does not
require unrelated local work to be absent. Unrelated work must remain
preserved and outside the artifact manifest, and no uncommitted or untracked
file may be necessary to interpret the proposal.

Chat messages, attachments, local archives, generated downloads, and model
memory may duplicate the proposal for convenience but are not the canonical
review target. A head change after review reopens the applicable exact-head
review gate.

If the remote branch, exact commit, or complete artifact set cannot be
recovered, the proposal must be recorded as `Abandoned` with its reason and
successor. Findings from an earlier review may inform a newly authored
successor, but they must not be used to reconstruct, continue, or approve the
lost proposal. The successor starts from the current reviewed `main` baseline
and receives its own identity, commit history, and review.

A single-ADR proposal remains subject to exact-artifact review and the ADR
workflow. It does not require a separate package manifest beyond the ADR and
normal handoff unless another document is part of the same proposed decision.

### Chief Architect acceptance record

On 2026-08-01, the Chief Architect accepted the architecture-proposal
chain-of-custody proposal in pull request 42 at exact head
`8471b56bfd139097f9988aeff8c7924f5e74a526`.

Acceptance is limited to the pull request's documentation-only ten-file
manifest: the Proposal v1 abandonment evidence boundary, the historical Work
Mode findings, repository-backed exact-head custody requirements, the recovery
matrix, proposal-scoped worktree and review-checklist clarifications, and the
related status and navigation updates. It does not authorize Sprint 006
Proposal v2, implementation, deployment, live-system action, or a change to
role authority or ADRs 0001 through 0005.

The chain-of-custody rule added by pull request 42 remains inactive until that
pull request merges to `main`. Recording this acceptance creates a new branch
head and therefore requires final exact-head review before merge; it does not
broaden the accepted scope or itself grant merge authority.

### Proposal recovery matrix

| Recovery condition | Required action | Custody result |
| --- | --- | --- |
| Exact commit remains reachable but its branch or tag ref was deleted | Restore a ref to the exact commit, verify its complete artifact manifest and base relationship, and reverify the review evidence | Custody may resume only after the restored immutable target matches the recorded review target |
| Head commit or artifact manifest changed | Publish the new exact head and manifest, then repeat the applicable Work Mode exact-head review | Earlier review does not authorize the changed target |
| Exact commit is lost or required artifacts are incomplete | Record the proposal as `Abandoned` with its reason and successor | Findings may inform a new proposal but cannot reconstruct or continue the lost target |
| Required evidence is sensitive | Retain raw evidence in an approved private location and publish only the sanitized metadata required by the `Validation Verified` contract | Review may proceed when authorized reviewers can reverify the retained evidence safely |
| No acceptable evidence-retention path exists | Stop and report the missing retention authority or location | The review gate remains blocked |

## Record and maintenance

Plans, findings, approvals, merges, and closeouts become durable only through
reviewed GitHub artifacts. Chat transcripts are not copied as authority.
Sensitive evidence follows the retention contract under `Validation Verified`;
raw sensitive material is never copied into the public repository or packet.

Changes to role authority, mandatory gate order, or final decision ownership
are Foundational decisions and require a new or superseding ADR plus Chief
Architect review. Editorial corrections may use the normal documentation
workflow when they do not change meaning.

Historical plans, changelog entries, and review records may retain earlier
role names or authority wording as evidence of the process in effect at that
time. Any new or resumed work follows this protocol after it becomes active.
