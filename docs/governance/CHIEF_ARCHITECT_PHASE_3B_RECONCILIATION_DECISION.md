# Chief Architect Decision Record — Phase 3B Reconciliation

## 1. Decision metadata

| Field | Value |
| --- | --- |
| Record ID | `CA-2026-08-06-P3B-RECONCILIATION` |
| Decision owner | Chief Architect |
| Recorded by | Implementation Engineer |
| Decision date | 2026-08-06 |
| Repository | `matthewart100-sys/project-jebediah` |
| Reviewed canonical commit | `991929beb6026511e07b6cb7954e1c9e400b9cb5` |
| Architecture baseline | `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` |
| Architecture-baseline tree | `5670add97e9da35e756be8d57e9f78547442c486` |
| Disposition | Strategically aligned, architecturally nonconforming, implementation not accepted |
| Execution authority | None in this original pre-execution decision |
| Record status | Original pre-execution reconciliation decision; retained as controlling reconciliation authority |

This package records the Chief Architect's original pre-execution
reconciliation decision. It did not authorize or execute the selected revert
and granted no coding, merge, deployment, runtime mutation, public exposure, or
real-data authority.

### Later B0 execution status

A later, separate B0 execution directive authorized the normal revert of
`991929beb6026511e07b6cb7954e1c9e400b9cb5` on the pull request #62 recovery
branch. That revert has been executed on the branch. References below to a
"future" or unauthorized revert preserve the boundary at the time of this
original decision; they do not describe the later branch state.

The recovery is not canonical until its corrected exact head passes CI,
receives independent Work Mode approval and a separate Chief Architect
exact-PR and exact-head merge decision, and pull request #62 is merged. The
branch operation changed no runtime, deployment, server, information-use, or
B1 state and grants no such authority.

## 2. Executive decision

- The strategic direction toward governed organizational intelligence is
  accepted.
- The Phase 3B architecture merged through pull request #58 at
  `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` remains accepted.
- [ADR 0016](../adr/0016-local-governed-pdf-intake-and-custody-boundary.md)
  remains Accepted and binding.
- The implementation introduced through pull request #60 is strategically
  aligned but architecturally nonconforming. It is not accepted as conforming
  or operational.
- No code introduced by pull request #60 is retroactively approved.
- No Phase 3B, Phase 3C, Phase 3D, workspace, deployment, domain, real-source,
  model, knowledge-promotion, memory, Qdrant, retrieval, grounded-answer, or
  public-exposure execution authority is active.
- The Phase 3B Completion Directive is superseded as implementation authority.
- The prior Phase 3B Milestone 1 authorization is retained only as a historical
  scope record.
- The Operational Workspace Implementation Sprint and deployment authority
  introduced by the same unreviewed merge are invalidated.
- Pull requests #59 and #60 remain preserved as audit and salvage evidence.
- **HISTORICAL PRE-EXECUTION DISPOSITION:** The selected repository correction
  was a future normal reviewed revert of squash commit
  `991929beb6026511e07b6cb7954e1c9e400b9cb5`. This original package did not
  authorize or perform it; the later B0 directive authorized its execution on
  the pull request #62 recovery branch.

## 3. Capability-level disposition

| Capability or artifact | Disposition | Current authority |
| --- | --- | --- |
| Long-term governed organizational-intelligence direction | Strategically accepted | Architecture and planning only |
| Phase 3B architecture package | Accepted at `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` | Binding architecture; no implementation |
| ADR 0016 | Accepted | Binding within its documented boundary |
| Pull request #59 implementation proposal | Historical salvage and audit evidence | Must not merge or deploy |
| Pull request #60 implementation and operational artifacts | Architecturally nonconforming and not accepted | Repository evidence only; must not run or deploy |
| Phase 3B implementation | Not accepted as conforming or operational | Unauthorized |
| Real-document or VBA use | Not approved | Unauthorized |
| Phase 3C or Phase 3D | Not approved | Unauthorized |
| Knowledge promotion | Not approved | Unauthorized |
| Model use | Not approved | Unauthorized |
| Memory or Qdrant projection | Not approved | Unauthorized |
| Retrieval or grounded answers | Not approved | Unauthorized |
| Operational workspaces | Invalidated as an active sprint or authority | Unauthorized |
| Deployment or public domain exposure | Not approved | Unauthorized |
| Normal revert at the time of this decision | Selected strategy only | Not authorized by this original decision |

Repository presence, a passing documentation check, a merged pull request, or
historical wording does not change any disposition in this table.

## 4. Updated implementation authority

There is no active implementation authority.

The
[Phase 3B Completion Directive](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md)
is Superseded as implementation authority. The
[Phase 3B Implementation Activation](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_IMPLEMENTATION_ACTIVATION.md)
is retained as a historical architecture-activation record and grants no
current execution authority. The
[Phase 3B Milestone 1 Authorization](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_MILESTONE_1_AUTHORIZATION.md)
is Historical and cannot be used to resume, merge, deploy, or expand work.

The original decision authorized only its documentation canonicalization
package. That package later became durable through pull request #61. A separate
B0 directive subsequently authorized the normal revert on the pull request #62
branch. The current recovery gates are, in order:

1. successful CI for the corrected exact pull request #62 head;
2. independent Work Mode review of that exact head;
3. a separate Chief Architect merge decision for the unchanged head; and
4. merge before the recovery becomes canonical.

## 5. Revised milestone structure

The former broad Phase 3B implementation interpretation is replaced by this
gated sequence. The sequence preserves strategic direction; it activates no
implementation milestone.

| Milestone | Purpose | Current state |
| --- | --- | --- |
| B0 - Canonical recovery | Validate the separately authorized pull request #62 recovery, complete independent review, and obtain exact-head merge approval | Recovery branch under review; not canonical before merge |
| B1 - Synthetic custody foundation | Re-establish a bounded synthetic-only custody question after canonical recovery | Future; unauthorized |
| B2 - Isolated PDF inspection and review | Validate isolated synthetic PDF inspection and human review without downstream promotion | Future; unauthorized |
| B3 - Lifecycle and recovery readiness | Prove retention, deletion, hold, backup, restore, and recovery boundaries | Future; unauthorized |
| C0 - Identity and service authorization | Decide principals, authentication, authorization, and service boundaries | Future; unauthorized |
| C1 - Governed knowledge promotion | Define and review promotion from approved evidence into a governed knowledge boundary | Future; unauthorized |
| C2 - Memory and Qdrant projection | Define the separately governed relationship to memory and Qdrant | Future; unauthorized |
| D1 - Evidence read model and grounded assistance | Define a read model, retrieval, citations, and grounded assistance | Future; unauthorized |
| D2 - Authenticated operational workspaces | Define authenticated workspace identity, separation, and lifecycle | Future; unauthorized |
| O1 - Deployment and exposure | Define deployment, operations, recovery, domain, and exposure boundaries | Future; unauthorized |

Each capability milestone after B0 requires its own decision-complete plan,
applicable ADR work, independent review, Chief Architect authorization, bounded
implementation, exact-head validation, merge decision, and closeout.
Completion or evidence from a later milestone cannot authorize an earlier gate
retroactively.

## 6. ADR impacts

- ADR 0016 remains Accepted and binding. This reconciliation does not broaden
  it.
- ADRs 0011 and 0014 continue to require separation among the Knowledge Vault,
  Knowledge Registry, Memory Service, and Qdrant.
- A new promotion ADR is required before C1.
- ADR 0003 requires an amendment or a successor before C2 can assign a governed
  relationship between promoted knowledge, Memory Service records, and Qdrant.
- A new interaction/read-model ADR is required before D1.
- A new identity/workspace ADR is required before D2.
- A new deployment ADR is required before O1.
- ADR 0013 remains conceptual for multi-format support. PDF, DOCX, TXT, and
  Markdown appearing in that ADR does not authorize those formats for use.
- ADR 0005 and the Project Coordination Protocol authority model remain
  unchanged.

The required future ADRs are not drafted, Proposed, or Accepted by this record.

## 7. Repository disposition

Pull request #60's squash commit remains present on canonical `main`. A later,
separately authorized normal revert has been executed on the pull request #62
B0 recovery branch, but that recovery is not canonical before exact-head CI,
independent Work Mode approval, a separate Chief Architect merge decision, and
merge. Pull request #60 and its commits remain repository, audit, and salvage
evidence. Their historical presence establishes no approved architecture,
implementation maturity, operational readiness, deployment authority, or
permission to run them.

The B0 recovery removed all eight operator and deployment guides added by pull
request #60 from the proposed pull request #62 tree:

- `docs/ADMINISTRATOR_QUICK_START.md`
- `docs/BACKUP_GUIDE.md`
- `docs/DEMONSTRATION_GUIDE.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/DISASTER_RECOVERY_GUIDE.md`
- `docs/OPERATIONS_GUIDE.md`
- `docs/PRODUCTION_CONFIGURATION_GUIDE.md`
- `docs/WORKSPACE_GUIDE.md`

No current-tree or quarantine-notice copy remains. Their historical evidence
survives only through pull request #60, source head
`70db20613e6275d391b2221d04e6ab4314d0a7b5`, squash commit
`991929beb6026511e07b6cb7954e1c9e400b9cb5`, and normal Git history. That
preservation supplies audit and salvage evidence only; it does not make the
guides current repository guidance, provide operator availability, grant
deployment authority, or permit anyone to execute their instructions.

## 8. Preservation requirements for pull requests #59 and #60

[Pull request #59](https://github.com/matthewart100-sys/project-jebediah/pull/59)
remains open at inspected head
`525ed481ce8492a644343e3bf665220936e52ad7`, based on
`9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8`. It is preserved as a bounded
synthetic-intake salvage candidate and audit record. Its passing
`documentation-quality` check is validation of that check only. It has no
recorded GitHub review and must not be merged, deployed, rebased into authority,
or treated as accepted implementation.

[Pull request #60](https://github.com/matthewart100-sys/project-jebediah/pull/60)
merged source head `70db20613e6275d391b2221d04e6ab4314d0a7b5` as squash commit
`991929beb6026511e07b6cb7954e1c9e400b9cb5`. Both commits have tree
`0caa432e362f63e7217043a854c072fadff0579e`. The pull request changed 79
files, had no recorded GitHub review, retained an uncompleted pull-request
template, and passed only the repository `documentation-quality` check. It is
preserved as merged audit and salvage evidence, not as an accepted
implementation, deployment, or operations record.

Do not delete, rewrite, force-update, or conceal either pull request or its
commits. Future work may salvage an idea only through the revised milestone
sequence and a fresh reviewed implementation. Pull request #59 must not be
merged or deployed. Pull request #60 is already merged; its content must not be
merged forward, run, deployed, or treated as accepted.

## 9. Historical pre-execution corrective plan

This section preserves the corrective plan as it stood when the original
reconciliation decision was recorded. A later, separate B0 execution directive
authorized the normal revert on the pull request #62 recovery branch, where it
has been executed but is not yet canonical. The original decision itself did
not authorize or perform the operation.

### Originally selected future action

The selected correction was a normal Git revert of pull request #60's squash
commit. At the time of this original decision it was a future repository
action, not an implementation approval and not an action authorized by this
package.

| Item | Required value |
| --- | --- |
| Originally planned corrective branch | `fix/revert-pr60-nonconforming-implementation` |
| Target squash commit | `991929beb6026511e07b6cb7954e1c9e400b9cb5` |
| Target parent / content baseline | `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` |
| Target parent tree | `5670add97e9da35e756be8d57e9f78547442c486` |
| Required Git operation | Apply the normal revert inverse without an automatic commit, validate it, then create an ordinary revert commit; no reset, rebase, force update, or history rewrite |

The later B0 directive superseded the planned branch name with
`fix/b0-canonical-repository-recovery` and separately supplied execution
authority.

### Historical future pre-flight

Before running a revert command, the Implementation Engineer must:

1. obtain a separate Chief Architect authorization naming the target commit,
   branch, scope, and exact next action;
2. fetch `origin` and verify local `main` and `origin/main` equal the exact
   canonical base named by that future authorization;
3. verify a clean working tree and list all worktrees;
4. create a fresh isolated worktree outside synchronized-cloud storage;
5. verify the future branch does not already exist locally or remotely;
6. verify `991929beb6026511e07b6cb7954e1c9e400b9cb5` has sole parent
   `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` and that the parent tree is
   `5670add97e9da35e756be8d57e9f78547442c486`;
7. capture pull requests #59 and #60, their refs, commit identities, changed-file
   manifests, and checks as preservation evidence; and
8. verify no deployment, runtime, container, server, DNS, certificate, database,
   model, document, or external system will be mutated.

If any check fails, stop without running the revert.

### Exact planned revert command

```text
git revert --no-commit 991929beb6026511e07b6cb7954e1c9e400b9cb5
```

This controlled command applies the inverse without automatically creating a
commit, allowing conflict inspection and validation first. It was not run or
authorized by the original documentation package. The later B0 directive
authorized its execution on the pull request #62 recovery branch, followed by
an ordinary revert commit, validation, push, and exact-head review.

### Expected baseline and conflict policy

Reverting the target directly on its own commit would restore exact parent tree
`5670add97e9da35e756be8d57e9f78547442c486`. After this reconciliation package
is merged, the final repository tree cannot equal that historical tree because
this decision record and the reviewed canonicalization changes must remain.
Therefore, `5670add...` is the exact pre-pull-request-#60 content reference, not
a promise that the post-reconciliation root tree hash will equal it.

If the normal revert reports a conflict:

- stop and record every conflicted path;
- do not accept `ours` or `theirs` mechanically;
- preserve this reconciliation record and the canonical authority/status
  corrections that make it durable;
- restore the inverse of pull request #60 for code, tests, dependencies,
  workflows, Docker, Caddy, runtime, service, and operator artifacts;
- resolve any delete/modify conflict on the eight then-quarantined operator guides
  by removing those pull-request-#60 additions, while retaining their history
  in pull request #60 and its commits;
- resolve only paths inside the separately authorized corrective manifest;
- abort the revert if the intended inverse cannot be established from the
  target, its parent, and the canonical reconciliation record; and
- obtain independent exact-head review of every resolution.

No conflict resolution may salvage implementation into the corrective branch
without a separately accepted milestone and implementation authorization.

### Historical planned validation

The planned corrective branch was required to:

- show `git status --short`, `git diff --stat`, `git diff --name-only`, and the
  complete diff from its authorized base;
- verify every pull-request-#60 path matches the target parent's content or
  absence except the exact surviving reconciliation items 1-23 in section 10;
- verify the eight then-quarantined pull-request-#60 guides in items 24-31 are absent
  from the corrective result and remain preserved through pull request #60 and
  its commits;
- verify no pull-request-#59 content was merged or substituted;
- run `uv sync --frozen`, the complete applicable test suite, compilation,
  `python scripts/validate_docs.py`, and `git diff --check`;
- inspect dependencies, locks, workflows, containers, scripts, services,
  documentation, and secrets against the exact inverse manifest;
- confirm no runtime, deployment, domain, database, model, document, or public
  exposure state changed; and
- publish one non-draft pull request for independent exact-head Work Mode
  review.

At the time of the original decision, separate Chief Architect authorization
was required before the revert command could run. The later B0 execution
directive supplied that branch authority. The resulting pull request #62 head
still requires independent exact-head review and a separate Chief Architect
decision before merge. No history rewriting, force-resetting `main`, deployment
mutation, or automatic merge is permitted.

## 10. Historical original canonicalization manifest

The original reconciliation canonicalization package changed exactly these 31
Markdown files:

1. `README.md`
2. `CHANGELOG.md`
3. `CURRENT_SPRINT.md`
4. `PROJECT_STATUS.md`
5. `ROADMAP.md`
6. `SECURITY.md`
7. `docs/ARCHITECTURE.md`
8. `docs/DATA_OWNERSHIP.md`
9. `docs/README.md`
10. `docs/REPOSITORY_STANDARDS.md`
11. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md`
12. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_THREAT_MODEL.md`
13. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_DEPENDENCY_ASSESSMENT.md`
14. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_LIFECYCLE_AND_RECOVERY.md`
15. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_VALIDATION_REQUIREMENTS.md`
16. `docs/adr/README.md`
17. `docs/adr/0016-local-governed-pdf-intake-and-custody-boundary.md`
18. `docs/governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md`
19. `docs/governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_IMPLEMENTATION_ACTIVATION.md`
20. `docs/governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_MILESTONE_1_AUTHORIZATION.md`
21. `docs/governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md`
22. `docs/reference/COMPONENT_REGISTRY.md`
23. `docs/reference/GLOSSARY.md`
24. `docs/ADMINISTRATOR_QUICK_START.md`
25. `docs/BACKUP_GUIDE.md`
26. `docs/DEMONSTRATION_GUIDE.md`
27. `docs/DEPLOYMENT_GUIDE.md`
28. `docs/DISASTER_RECOVERY_GUIDE.md`
29. `docs/OPERATIONS_GUIDE.md`
30. `docs/PRODUCTION_CONFIGURATION_GUIDE.md`
31. `docs/WORKSPACE_GUIDE.md`

No code, test, dependency, lock, workflow, Docker, Caddy, script, runtime, or
other executable or non-Markdown deployment artifact belongs to this package.
In that original package, items 24-31 received quarantine notices only. The
later B0 recovery removes all eight files from the proposed pull request #62
tree; their evidence remains only in pull request #60 and normal Git history.

## 11. Future implementation gates

After B0 canonical recovery is terminally complete, any future milestone must:

1. start from the then-current reviewed `main`;
2. identify one bounded outcome, non-goals, exact manifest, data boundary,
   security and recovery impact, and validation contract;
3. complete every required ADR before dependent implementation;
4. receive independent Work Mode architecture review;
5. receive a separate Chief Architect implementation authorization for the
   exact plan;
6. use synthetic information unless a later exact real-source decision is
   independently reviewed and approved;
7. receive independent exact-head implementation review and a separate Chief
   Architect merge decision; and
8. merge and close out before a later milestone can become active.

No artifact from pull request #59 or #60 satisfies a future gate by existence,
test result, similarity, or reuse.

## 12. Explicit non-authorizations

This record and package authorize none of the following:

- production code or test changes;
- dependency or lock changes;
- workflow, Docker, Caddy, server, container, or runtime changes;
- a revert, cherry-pick, reset, rebase, force update, merge, or deployment;
- real-document discovery, access, opening, hashing, scanning, parsing, OCR,
  ingestion, storage, review, or use;
- VBA onboarding, document access, ingestion, or use;
- Phase 3B, Phase 3C, or Phase 3D implementation;
- workspace, identity, domain, model, knowledge-promotion, memory, Qdrant,
  retrieval, grounded-answer, or public-exposure implementation;
- Cloudflare, DNS, certificate, or public-domain changes; or
- treating pull request #59 or #60 as mergeable, deployable, conforming, or
  operational.

## 13. Chain-of-custody status

The Chief Architect accepted decision
`CA-2026-08-06-P3B-RECONCILIATION` in conversation against reviewed canonical
commit `991929beb6026511e07b6cb7954e1c9e400b9cb5`. Conversation acceptance
authorized preparation of the original documentation package only.

The original chain-of-custody requirements were:

1. every artifact in the exact 31-file manifest is committed and pushed on one
   short-lived branch;
2. an independent Work Mode reviewer inspects the exact head and complete diff;
3. every blocking finding is corrected or receives the disposition required by
   the Project Coordination Protocol;
4. the Chief Architect separately approves that unchanged head for merge; and
5. the reviewed pull request merges to `main`.

Those requirements were satisfied when pull request #61 merged the decision as
canonical commit `b1d8dea531ad0b82171cb0f3f3979323b712a5de`. That merge did
not authorize the revert or any implementation. A later, separate B0 directive
authorized the normal revert only on the pull request #62 recovery branch.
That recovery remains noncanonical until exact-head CI, independent Work Mode
approval, a separate Chief Architect exact-head merge decision, and merge.
