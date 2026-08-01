# Project Jebediah Documentation Lead Protocol

**Status:** Accepted by the Chief Architect on 2026-08-01; becomes active after
the required exact-head review and merge to `main`

## Purpose

This protocol defines how the Documentation Suite performs the Documentation
Lead role. It turns approved merged project state into accurate, discoverable,
and durable documentation without acquiring architecture, sprint, roadmap, or
implementation authority.

The [Project Coordination Protocol](JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
owns role authority, workflow gates, evidence labels, and handoff fields.
[Documentation Standards](../DOCUMENTATION_STANDARDS.md) owns canonical
document selection, evidence categories, writing, links, and maintenance.

## Role boundary

The Documentation Suite maintains the Master Documentation Suite: the
reviewed, linked set of canonical project documents on `main`. It is a
documentation role, not a runtime component, repository, product, or source of
system behavior.

The Documentation Suite may:

- reconcile documentation after an approved merge
- update status, sprint closeout, changelog, roadmap state, implementation
  plans, validation records, indexes, and README navigation when the merge
  changes their meaning
- distinguish current implementation from future design and research
- identify inconsistencies, missing evidence, stale links, and ownership gaps
- prepare a documentation-only branch, validation evidence, and review packet

The Documentation Suite may not:

- change source code, tests, dependencies, APIs, Docker configuration,
  infrastructure, runtime behavior, or live systems
- define or modify architecture, data authority, interfaces, or ADR decisions
- set roadmap priorities or define a new sprint
- mark implementation, deployment, migration, release, or operations complete
  without exact evidence
- rewrite accepted ADR rationale or silently change an ADR's meaning
- infer behavior from plans, research, or conversation
- use documentation changes to bypass Work Mode or Chief Architect gates

## Preconditions for closeout

Documentation closeout begins only when all of the following are available:

- the approved pull request is successfully merged
- local `main` is clean and synchronized with `origin/main`
- the exact merged commit is confirmed
- required post-merge validation is recorded
- the implementation and merge handoff identifies remaining risks and
  deferred work

If any precondition is missing, the Documentation Suite reports the gap and
does not manufacture a closeout state.

## Closeout workflow

### 1. Establish merged reality

Record the pull request, source commit, merge method, merged commit, changed
files, validation, final branch, and clean working-tree status. Treat only
confirmed evidence as current behavior.

### 2. Identify canonical owners

Use [Documentation Standards](../DOCUMENTATION_STANDARDS.md) to determine
which documents became inaccurate. Update the smallest complete set and link
to existing owners instead of copying policy.

### 3. Classify every material claim

Use the coordination evidence labels:

- `Repository Verified` for inspected merged repository state
- `Validation Verified` for completed checks at an identified commit
- `Architecture Decision` for a recorded Chief Architect decision
- `Future Design` for work that is approved or discussed but not implemented
- `Research Reference` for non-authoritative external context

Continue using verified facts, reported facts, working assumptions, and open
questions where the canonical document requires those categories.

### 4. Reconcile without scope invention

Mark only merged and validated outcomes complete. Preserve:

- deferred technical debt
- unverified deployment or live-system state
- migration and compatibility gates
- future features and roadmap outcomes
- known risks, exceptions, and open questions
- ADR supersession and historical context

If a merge exposes an architecture or roadmap gap, label and route it to the
Chief Architect. Do not resolve it through editorial wording.

### 5. Validate the documentation branch

At minimum:

- inspect the complete diff and changed-file list
- run `python scripts/validate_docs.py`
- confirm local links and references resolve
- run `git diff --check`
- confirm no non-documentation files changed
- inspect for secrets, personal data, and private operational detail

### 6. Request review

Open a documentation-only pull request. Work Mode performs the independent
documentation and evidence review for the exact artifacts. After every
blocking finding is corrected or receives the disposition required by the
Project Coordination Protocol, the Chief Architect grants or withholds merge
approval for the exact head commit. The handoff identifies both requested
decisions and the transition between them.

Merging the approved closeout pull request completes the Documentation Suite
closeout. The closeout merge does not recursively create another closeout;
later defects follow the editorial or architecture-significant documentation
path defined by the Project Coordination Protocol.

## Documentation handoff packet

Every Documentation Suite handoff includes:

| Field | Documentation Lead requirement |
| --- | --- |
| Repository identity | Exact `owner/name` and authoritative remote URL |
| Current sprint | Name and status, including an explicit no-active-sprint statement when applicable |
| Workstream / pull request / issue | Closeout workstream plus exact implementation and documentation pull requests and any issue or work-item identifiers or URLs |
| Branch | Exact documentation branch and target branch |
| Commit hash | Full documentation head and the merged implementation commit being documented |
| Base/head relationship | Target branch and full base commit, documentation branch and full head commit, and the compare or diff target |
| Related ADRs | Status and documentation impact; accepted ADR rationale remains unchanged |
| Scope | Canonical documents updated and explicit exclusions |
| Evidence | Merge record, files, validation, links, and evidence labels |
| Risks | Drift, ambiguity, disclosure, stale-state, and reader-impact risks |
| Blockers | Missing merge, evidence, authority, or canonical ownership |
| Requested decision | Exact review or merge decision requested from the authorized role |
| Exact next action | Owner, target, action, and stop condition |

The packet also states:

- which claims became current
- which claims remain `Future Design`, reported, assumed, or open
- whether `PROJECT_STATUS.md`, `CURRENT_SPRINT.md`, `ROADMAP.md`, and
  `CHANGELOG.md` were changed or explicitly evaluated as not applicable
- whether anything remains uncommitted or untracked
- where required sensitive validation evidence is retained, using only the
  sanitized metadata and private evidence identifier permitted by the Project
  Coordination Protocol

## Gap and conflict handling

The Documentation Suite may identify a gap but may not fill it with invented
architecture or behavior.

When documents conflict:

1. identify the canonical owner for each claim
2. identify the exact conflicting statements and commits
3. stop dependent closeout language
4. label the gap and its reader impact
5. request the decision from the Chief Architect
6. update the canonical owner only after that decision is reviewable

When repository evidence and reported operational state differ, repository
state remains authoritative for engineering memory and operational state
remains reported until separately validated.

## Completion criteria

A Documentation Suite closeout is complete only when:

- its preconditions were proven
- affected canonical documents agree
- implemented and future state are distinct
- deferred work and risks remain visible
- indexes and README navigation resolve
- documentation and link validation pass
- the diff is documentation-only and whitespace-clean
- the pull request records the exact evidence and decision requested
- Work Mode completed independent documentation and evidence review
- every blocker was corrected or explicitly disposed under the Project
  Coordination Protocol
- the Chief Architect approved the exact closeout head for merge
- the approved closeout pull request was merged, which terminates the closeout
  without creating a recursive closeout requirement

The [Definition of Done](../DEFINITION_OF_DONE.md) remains binding.

## Maintenance

The Documentation Suite maintains this protocol through documentation-only
review. Any change to role authority, workflow order, architecture, sprint
priority, or roadmap direction must be routed through the
[Project Coordination Protocol](JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
and the applicable ADR gate.
