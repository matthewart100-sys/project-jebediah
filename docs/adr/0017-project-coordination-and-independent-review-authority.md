# ADR 0017: Project Coordination and Independent Review Authority

**Status:** Proposed

**Decision level:** Foundational

**Date:** 2026-08-06

**Decision owner:** Chief Architect

**Reviewers:** Transitional Work Mode exact-head architecture review under ADR
0005, then Chief Architect final exact-head decision; project maintainer for
repository-custody impact

## Decision summary

Supersede ADR 0005 with a capability-neutral Independent Reviewer role. Routine
review uses a fresh, read-only normal ChatGPT conversation; Work Mode becomes an
optional review mechanism used only when the Chief Architect explicitly
requests unusually high-risk, cross-cutting, or adversarial review.

The decision preserves independent actual-artifact review, same-artifact role
separation, written blocker disposition, and Chief Architect authority for
scope, architecture, ADR acceptance, and exact-head merge decisions. It also
separates merge execution from the artifact's author or implementer through a
non-author Merge Operator.

## Context

ADR 0005 established permanent project coordination and made Work Mode a named,
mandatory reviewer in the plan-to-closeout sequence. The decision also required
any lasting replacement of authority or gate order to use a new ADR that
explicitly supersedes it.

The B1 activation package proposes a tool-neutral independent-review role and a
fresh normal-chat review path. A repository-wide audit found that the proposed
policy conflicted with accepted ADR 0005 and with active process documents. The
Chief Architect therefore authorized this Foundational ADR and the required
canonical reconciliation. Exact-artifact acceptance remains a separate gate.

### Verified facts

- ADR 0005 is Accepted and remains controlling until a successor is accepted
  and merged.
- ADR 0005 requires a new explicitly superseding ADR for a lasting change to
  role authority or gate order.
- The Project Coordination Protocol already separates Chief Architect,
  Implementation Engineer, independent review, Documentation Lead, maintainer,
  and future Runtime responsibilities.
- The B1 activation decision requires an independent reviewer who did not
  author or modify the artifacts, inspects the exact pull-request evidence
  read-only, and cannot grant final approval.
- Tool or product capability does not itself grant project authority.

### Reported facts

None. This governance decision depends on repository evidence and the Chief
Architect's recorded direction, not an unverified operational report.

### Working assumptions

- A fresh normal ChatGPT conversation can occupy the routine independent-review
  role when it remains read-only and receives the complete repository, pull
  request, base, head, diff, and validation evidence. If no qualified
  independent reviewer can inspect the actual artifacts, the applicable gate
  remains blocked.
- The Chief Architect will explicitly request Work Mode when the change's risk
  warrants that review mechanism.

### Open questions

None block this decision. Review depth remains proportional to the artifact and
may be increased by the Chief Architect without changing role authority.

## Scope

- project-wide engineering role authority and separation;
- routine and architecture-significant independent-review mechanisms;
- plan, implementation, exact-head review, merge, and closeout gate order;
- non-author controlled-merge execution and post-merge verification;
- reviewer dispositions and Chief Architect blocker disposition;
- emergency review deferral, context-complete handoff, and evidence rules; and
- migration from the named mandatory Work Mode role in ADR 0005.

## Non-goals

- authorizing B1 implementation before the activation package merges;
- changing B1 scope or any later milestone;
- changing application, runtime, service, schema, dependency, infrastructure,
  deployment, or operations design;
- authorizing real documents, organizational information, model use, memory,
  retrieval, public exposure, or deployment;
- weakening independent review or permitting implementer self-approval or
  self-merge; or
- rewriting historical review and decision records that accurately name Work
  Mode at the time.

## Decision drivers

- Preserve independent challenge without binding authority to one product mode.
- Keep exact-head evidence and same-artifact reviewer independence mandatory.
- Keep the Chief Architect as the final architecture and merge authority.
- Prevent Codex or another implementer from approving or merging its own work.
- Keep routine work reviewable without making one optional interface a permanent
  project role.
- Preserve durable blocker disposition, handoff, emergency, and closeout rules.
- Make the active policy consistent across canonical documents.

## Considered alternatives

### Retain mandatory Work Mode review

Rejected because it binds a permanent project authority to one review mode even
when an equally independent, evidence-complete normal-chat review can satisfy
the routine gate. It also conflicts with the Chief Architect's selected B1
activation workflow.

### Remove independent review from routine work

Rejected because implementer self-audit is not independent evidence and the
Chief Architect should receive an adversarial review disposition before an
exact-head merge decision.

### Use normal-chat review only and prohibit Work Mode

Rejected because unusually high-risk, cross-cutting, or adversarial changes may
benefit from Work Mode when the Chief Architect explicitly requests it.

### Retain Codex merge execution after Chief Architect approval

Rejected because the B1 activation decision explicitly prohibits Codex from
merging its own work. A non-author Merge Operator preserves the distinction
between exact-head approval, merge execution, and post-merge verification.

### Adopt a capability-neutral Independent Reviewer role

Selected because it preserves role separation and evidence gates while making
the routine mechanism a fresh, read-only normal ChatGPT conversation and
retaining Work Mode as a risk-triggered option.

## Decision

The
[Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
remains the canonical owner of cross-role authority, mandatory gates, handoff
fields, blocker disposition, and coordination evidence labels.

Upon acceptance and merge, this ADR supersedes ADR 0005 in full; no part of ADR
0005 remains independently normative. Until then, ADR 0005 controls this
proposal's transition and review.

The permanent roles are:

- **Chief Architect:** final decision maker for strategy, architecture, scope,
  ADR acceptance, sprint authorization, roadmap direction, blocker disposition,
  and exact-head merge approval;
- **Implementation Engineer:** Codex or an assigned engineer who plans,
  implements, validates, and publishes only authorized scope and may self-audit
  but may not independently approve or merge its own work;
- **Independent Reviewer:** a distinct, read-only reviewer that did not author
  or materially modify the reviewed artifact and may block but cannot grant
  final architecture or merge approval;
- **Merge Operator:** the maintainer or another explicitly assigned operator
  that did not author or implement the artifact and may execute only the Chief
  Architect's exact approved merge without gaining scope or approval authority;
- **Documentation Lead:** the Documentation Suite or assigned documentation
  role that reconciles confirmed merged reality without inventing behavior,
  scope, or priority;
- **Maintainer:** repository custodian for access, licensing, legal control, and
  GitHub settings without silent Chief Architect authority; and
- **Jebediah Runtime:** a future consumer of approved project state without
  engineering decision authority.

Routine independent review uses a fresh normal ChatGPT conversation. The
reviewer receives the authoritative repository identity, pull request or issue,
exact base and head, complete changed-file manifest and diff, relevant decisions,
validation evidence, risks, and requested disposition. It remains read-only and
returns exactly `APPROVED`, `REVISIONS REQUIRED`, or `BLOCKED`.

Work Mode is not a mandatory routine role. It may occupy the Independent
Reviewer role only when the Chief Architect explicitly requests it for an
unusually high-risk, cross-cutting, or adversarial review. Selecting Work Mode
does not transfer final authority to the reviewer.

The normal sequence is:

1. The Implementation Engineer publishes a bounded plan with scope, non-goals,
   acceptance criteria, architecture/ADR impact, risk, validation, and rollback.
2. Architecture- or security-significant work always receives independent
   pre-implementation review. The Chief Architect may require that review for
   other work based on risk.
3. The Chief Architect reviews the exact plan and applicable independent-review
   evidence and returns `APPROVED TO CONTINUE WITHOUT MERGE` or `REVISIONS
   REQUIRED` for that checkpoint.
4. The Implementation Engineer implements only the authorized scope, validates
   it proportionately, and publishes one exact review head.
5. An Independent Reviewer inspects the actual exact-head artifacts and returns
   `APPROVED`, `REVISIONS REQUIRED`, or `BLOCKED`.
6. Every blocking finding is corrected or receives a written Chief Architect
   disposition without making the reviewer the final authority.
7. The Chief Architect returns `APPROVED TO MERGE` or `REVISIONS REQUIRED` for
   the unchanged exact head.
8. A non-author Merge Operator performs the controlled merge. Codex may verify
   canonical state and route any required terminal closeout but may not merge
   its own implementation.

A changed reviewed head invalidates the prior independent-review and Chief
Architect merge decisions. Summary-only approval, conversation memory, an
uncommitted artifact, or an inaccessible branch cannot satisfy an evidence
gate.

An author or implementer cannot satisfy the Independent Reviewer gate by
announcing a role change. If a qualified distinct reviewer is unavailable, work
stops at that gate.

In a repository engineering emergency, only the Chief Architect may defer a
pre-implementation independent architecture review for the smallest reversible
containment. Exact authority, rollback, validation, independent exact-head
review, blocker disposition, all required checks, and Chief Architect merge
approval remain mandatory before merge.

## Consequences

### Positive

- Independent review remains mandatory while no single product mode owns the
  permanent reviewer role.
- Routine milestones have a clear, repeatable normal-chat review mechanism.
- Same-artifact independence, exact-head evidence, and Chief Architect authority
  remain explicit.
- Work Mode remains available for deliberately escalated review.
- The artifact's author or implementer cannot execute its own merge.
- Active governance documents can use one consistent role vocabulary.

### Negative

- Existing active policy documents require coordinated updates.
- Historical records continue to name Work Mode, so readers must distinguish
  historical evidence from current policy.
- A qualified non-author Merge Operator must be available and receive an exact
  handoff, which adds one coordination gate in a single-maintainer project.
- The transition itself remains subject to ADR 0005 until this ADR is accepted
  and merged.

### Neutral

- The decision changes review mechanism, role naming, and merge execution while
  preserving required independence and final Chief Architect authority.
- GitHub branch protection and maintainer custody remain unchanged.
- Review depth may still vary proportionately with risk.

## Data and provenance impact

No runtime-data impact. GitHub remains authoritative for reviewed engineering
memory. Handoffs continue to distinguish verified facts, reported facts,
working assumptions, and open questions and to preserve exact repository and
commit provenance.

## Security and privacy impact

No product/runtime trust boundary, privilege, credential, personal-information,
or live-data authority changes. The governance review boundary changes only in
its routine mechanism: a normal-chat reviewer receives public repository
artifacts and sanitized evidence. Review packets must omit secrets, private
addresses, raw sensitive logs, personal data, and exploitable topology.
Sensitive evidence remains in an approved private location and may be reviewed
only through a separately authorized access path; normal chat receives the
sanitized public result.

## Operations and recovery impact

No runtime, service, deployment, health, capacity, backup, or recovery behavior
changes. The process adds a non-author merge handoff; if no qualified Merge
Operator is available, merge waits. Codex still verifies the resulting
canonical commit and applicable rollback evidence. Before acceptance and merge,
this proposal may be revised or discarded without runtime effect. After
acceptance and merge, restoring mandatory Work Mode or author/implementer merge
execution as a lasting gate requires another Foundational ADR; a Git revert
cannot erase accepted decision history.

## Compatibility and migration

ADR 0005 remains controlling until this ADR is accepted and merged. Therefore
the pull request that introduces this decision uses ADR 0005's incumbent Work
Mode exact-head review gate; a normal-chat review may be additional evidence but
cannot substitute for that transitional gate.

When accepted and merged, this ADR supersedes ADR 0005 in full and re-adopts its
still-valid Chief Architect authority, implementer limits, maintainer-custody
separation, same-artifact independence, actual-artifact evidence, blocker
disposition, emergency, handoff, controlled-merge, Documentation Lead, and
Runtime-consumer guarantees. Controlled merge execution moves to a non-author
Merge Operator so Codex cannot merge its own implementation. Active documents
migrate to the Independent Reviewer vocabulary. Historical records remain
unchanged.

## Validation

Acceptance requires:

- the exact proposed ADR and reconciliation diff to receive incumbent Work Mode
  architecture review under ADR 0005;
- Chief Architect acceptance of the exact proposed head;
- a follow-up status commit that marks this ADR `Accepted`, marks ADR 0005
  `Superseded`, adds reciprocal supersession links, and records exact review
  evidence;
- fresh incumbent Work Mode exact-head review and Chief Architect merge
  approval after that status commit;
- consistent active-policy language across agent, collaboration, sprint, ADR,
  Git workflow, review-template, documentation, glossary, and governance files;
- preservation of historical Work Mode evidence;
- no application, runtime, service, dependency, GitHub Actions workflow-file,
  deployment, or real-information change;
- `python scripts/validate_docs.py`;
- `git diff --check`; and
- successful Documentation Quality CI for every exact review head.

## Follow-up work

- Obtain the transitional review and Chief Architect acceptance described
  above.
- Apply the status, reciprocal-supersession, and review-record commit only after
  that acceptance.
- Revalidate and repeat incumbent Work Mode exact-head review before merge.

## Related documents

- [ADR 0005: Project Coordination and Role Authority](0005-project-coordination-and-role-authority.md)
- [ADR Process](README.md)
- [Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
- [B1 Activation Decision](../governance/CHIEF_ARCHITECT_B1_ACTIVATION_DECISION.md)
- [Git Workflow](../GIT_WORKFLOW.md)
- [Definition of Done](../DEFINITION_OF_DONE.md)
- [Pull request #63](https://github.com/matthewart100-sys/project-jebediah/pull/63)

## Supersession

**Supersedes upon acceptance and merge:** [ADR 0005: Project Coordination and Role Authority](0005-project-coordination-and-role-authority.md)

**Superseded by:** None

## Review record

On 2026-08-06, after a repository-wide consistency audit identified the ADR
0005 conflict, the Chief Architect authorized preparation of a Foundational ADR
that supersedes ADR 0005 and the required canonical reconciliation. That
authorization permits this proposal; it is not acceptance of an unseen exact
artifact.

Transitional Work Mode review, Chief Architect exact-head acceptance, the
status and reciprocal-link commit, fresh incumbent Work Mode exact-head review,
and Chief Architect merge approval remain pending. This proposal authorizes no
B1 implementation, merge, deployment, runtime mutation, or real-information
use.
