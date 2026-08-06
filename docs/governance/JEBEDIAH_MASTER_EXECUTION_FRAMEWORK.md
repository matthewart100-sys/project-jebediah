# Project Jebediah Master Execution Framework

**Status:** Active process framework after merge

## Purpose

This framework defines the repeatable execution path for bounded Project
Jebediah milestones. It is process guidance only. It does not approve an
architecture, activate a milestone, grant information-use authority, or
authorize implementation, merge, deployment, or public exposure.

The [Project Coordination Protocol](JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
remains the authority owner. The [Git Workflow](../GIT_WORKFLOW.md),
[Documentation Standards](../DOCUMENTATION_STANDARDS.md), and
[Definition of Done](../DEFINITION_OF_DONE.md) remain binding.

## Standard milestone workflow

Every milestone follows these gates in order. A later gate cannot cure a
missing earlier decision.

1. **Canonical authority verification.** Identify the controlling decision,
   current sprint, applicable ADRs, authorized role, exact objective, and
   explicit exclusions from reviewed `main`.
2. **Exact-main synchronization.** Fetch and verify local `main`,
   `origin/main`, and the authorized base commit. Stop on divergence.
3. **Fresh isolated branch and worktree.** Create a short-lived branch and a
   clean worktree outside synchronized-cloud storage when isolation is needed.
4. **Documentation-first milestone plan.** Record the intended outcome,
   non-goals, acceptance criteria, dependencies, risks, data boundary,
   recovery expectations, and authority gates before dependent implementation.
5. **Exact expected file manifest.** List every expected added, modified,
   restored, or removed path and define the policy for unexpected paths.
6. **Architecture and ADR traceability.** Map the work to current architecture
   and accepted ADRs; obtain required architecture decisions before code.
7. **Explicit exclusions.** State which capabilities, information, systems,
   environments, and later milestones remain unauthorized.
8. **Implementation.** Make only the approved, bounded changes. Preserve
   unrelated work and do not expand scope silently.
9. **Tests and validation.** Run the full applicable suite plus targeted,
   documentation, dependency, compilation, boundary, and hygiene checks.
10. **Security and boundary audit.** Verify secrets, personal or real data,
    trust boundaries, generated artifacts, prohibited paths, and operational
    exclusions.
11. **Implementation packet.** Record repository identity, exact base and
    head, commit list, file manifest, diff, validation, risks, blockers,
    rollback, and requested decision.
12. **Non-draft pull request.** Publish one reviewable pull request when its
    bounded scope and validation are complete.
13. **Independent exact-head Work Mode review.** A distinct review instance
    that did not author or modify the artifacts reviews the exact head and
    complete evidence package.
14. **Chief Architect exact-PR and exact-head decision.** After Work Mode,
    obtain the formal decision for the unchanged pull request head and resolve
    every blocking finding under the coordination protocol.
15. **Controlled merge.** Merge only with required approval and passing gates;
    do not rewrite `main` history.
16. **Canonical read-back.** Fetch and verify the merge commit, changed files,
    branch state, and canonical documents from updated `main`.
17. **Post-merge validation.** Repeat checks whose evidence depends on merged
    state and record exact results and limitations.
18. **Separate deployment authority.** Treat repository merge and release as
    insufficient for deployment, runtime mutation, or public exposure.
19. **Separate information-use authority.** Treat implementation and
    deployment as insufficient to access, process, retain, or disclose real
    information.
20. **Closeout.** Reconcile canonical documentation from verified merged
    reality and complete the applicable independent review and merge gates.

## Mandatory stop conditions

Stop the affected work, preserve evidence, and request the authorized decision
when any of these conditions occurs:

- authority conflict or missing authority;
- unexpected scope or file-manifest expansion;
- a changed canonical base;
- unexplained worktree mutation or active writer;
- a new or materially changed security boundary;
- a data migration;
- proposed access to or use of real information;
- deployment, runtime mutation, or public exposure;
- a reviewed head changes;
- any required validation failure.

A stop condition is not permission to repair or broaden the milestone. Resume
only from a recorded, reviewable decision and update the canonical owner when
future work depends on it.

## Role boundaries

### Chief Architect

The Chief Architect owns strategy, architecture, scope, ADR acceptance, sprint
authorization, exact-head merge decisions, and roadmap direction. That role
does not replace repository custody, deployment authority, or information-use
authority unless each authority is explicitly and separately exercised.

### Implementation Engineer

The Implementation Engineer inspects, plans, implements authorized scope,
validates, publishes evidence, and prepares handoffs. The engineer may perform
internal self-audits but cannot perform their own independent Work Mode
approval or grant themselves Chief Architect authority.

### Work Mode reviewer

The Work Mode reviewer is a distinct instance that did not author or
materially modify the reviewed artifact. Work Mode may issue blocking findings
and a review disposition but cannot grant final architecture or merge
approval.

### Documentation Lead

The Documentation Lead reconciles confirmed merged reality into the smallest
complete set of canonical documents. The role cannot invent behavior,
architecture, authority, sprint priority, or roadmap direction.

### Operations role

The Operations role acts only under separately recorded deployment or runtime
authority. It verifies environment, change, rollback, recovery, and operational
evidence without treating repository implementation as permission to mutate a
live system.

## Session boundary

Each Codex chat has one bounded milestone objective. A session may prepare an
exact prompt or implementation packet for the next phase, but it must not begin
that phase without its own documented authority and gates.

For B0, this framework records reusable process only. It does not authorize B1
or any later milestone.
