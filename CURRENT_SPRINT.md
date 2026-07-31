# Current Sprint

## Phase 1 Sprint 2: JCS Definition Framing

**Target window:** 2026-07-31 through 2026-08-13

**Status:** Active; C1 closure review; C2 and implementation blocked

## Sprint goal

Complete Milestone C1 of the approved
[JCS Definition Implementation Plan](docs/JCS_DEFINITION_PLAN.md): preserve the
evidence-backed framing proposal, record the reviewed **DEFER JCS** outcome,
and obtain final exact-artifact closure review without treating JCS as defined,
specified, rejected, or authorized for implementation.

## Context

Project Genesis Phase 0 and the post-release maintenance loop are complete.
Pull request #16 established the JCS definition implementation plan and merged
at `b785bbc71421da84568f2d2be00d877d4e67bdb6`. The required merged-`main`
check passed in GitHub Actions run `30634584406` without annotations.

The plan's C0 gate is therefore complete. The Chief Architect authorized C1 to
create only:

- A **Proposed** JCS specification
- Proposed ADRs when the repository evidence already meets an ADR trigger
- Alternatives analysis, unresolved questions, and repository-backed
  requirements

JCS remains a **Named** future subsystem. Its expansion, purpose,
responsibility, information authority, consumers, interfaces, guarantees,
deployment, and implementation remain unresolved.

Draft pull request #18 supplied the complete first framing proposal. Its
required check passed in run `30635469490`, and the Chief Architect approved
continued C1 work without merge while identifying missing purpose, consumer,
boundary, and failure-consequence evidence. Pull request #19 then made the
four-way C1 outcome gate and no-JCS baseline canonical at merged commit
`2b8e1a318062ce7e5f029cd32521bc655db87712`; run `30636066645` passed without
annotations.

Under the maintainer's standing delegation for this review workflow, the Chief
Architect recommended **DEFER JCS** and authorized preparation of the canonical
outcome record. The final gate is exact-artifact C1 closure review of revised
pull request #18. C2 remains blocked, and no numbered ADR is required because
deferral creates no architecture commitment.

### Prior sprint closeout

Phase 1 Sprint 1 delivered all three committed checkpoints:

- Project Genesis closeout through pull request #13
- Surgical documentation-workflow maintenance and verified closeout through
  pull requests #14 and #15
- Approved JCS definition implementation plan through pull request #16

No work carries over. The sprint demonstrated that exact-head review,
evidence-class separation, and narrow dependency maintenance prevent adjacent
work from expanding architectural scope. The next sprint narrows further to
definition framing only.

## Committed scope

### Checkpoint A: C0 lifecycle closeout

- Mark the approved JCS definition plan **Active**.
- Record the exact approval, merge, required-check, and no-annotation evidence.
- Close Phase 1 Sprint 1 with delivered outcomes and process lessons.
- Open Phase 1 Sprint 2 without creating the specification in the closeout
  change.

### Checkpoint B: C1 requirements and alternatives

- Create `docs/JCS_SPECIFICATION.md` as a complete **Proposed** artifact after
  Checkpoint A merges.
- Preserve verified facts, reported facts, working assumptions, open
  questions, and proposed statements distinctly.
- Gather and promote maintainer intent about the JCS name and problem through
  the approved collaboration path; do not infer it from bootstrap memory.
- Compare credible name, purpose, responsibility, consumer, and no-change
  alternatives, including retain, rename, and defer where applicable.
- Define scope and non-goals as proposals, not current architecture.
- Carry the JCS-01 through JCS-10 decision register into the proposal with
  evidence needs, owners, and gates.
- Create only proposed numbered ADRs for choices that already meet the
  repository's ADR triggers.

### Checkpoint C: C1 framing review

- Validate the full proposed artifact set against repository standards and the
  approved plan.
- Give the Chief Architect the exact changed files, base, head, ADR assessment,
  evidence, and validation results.
- Obtain a formal decision on decision framing, ADR levels, missing evidence,
  and whether Milestone C2 may begin.
- Record every recommendation in a canonical owner before dependent work.
- Record the selected C1 outcome, authority boundary, non-selected paths,
  reconsideration triggers, and exact review identity.
- Submit the revised complete artifact set for final C1 closure review; do not
  merge or begin C2 without that decision.

## Non-goals

- Treating any expansion of `JCS` as already decided
- Accepting the JCS specification or advancing JCS beyond **Named** maturity
- Assigning authoritative information, collector dependency, or an operational
  owner
- Creating schemas, protocols, concrete interfaces, diagrams, catalogs,
  traceability indexes, test trees, runtime folders, workflows, or runbooks
- Selecting a language, framework, database, queue, model, container,
  infrastructure product, host, or deployment topology
- JCS, collector, application, infrastructure, workflow, schema, or test
  implementation
- Treating reported home-lab products as verified requirements

## Acceptance criteria

- The C0 closeout is merged before `docs/JCS_SPECIFICATION.md` is created.
- The specification proposal is substantive rather than a placeholder and
  remains visibly **Proposed** and non-authoritative.
- The framing review records exactly one C1 outcome: **DEFER JCS**.
- The no-JCS baseline remains visible until an accepted decision establishes a
  component responsibility.
- Missing purpose, consumer, boundary, and failure-consequence evidence remains
  first-class architectural questions rather than backlog items.
- JCS-01 through JCS-10 remain questions until their required evidence and
  decisions exist.
- Alternatives include retaining the current undefined state when it is a
  credible option.
- Maintainer intent used by the proposal is promoted into the repository as a
  proposed statement with its decision gate.
- Proposed ADRs contain no accepted decision and use proportionate System or
  Foundational assessments.
- Only the proposed specification and required proposed ADRs are created.
- Repository validation and `git diff --check` pass.
- The Chief Architect reviews the exact complete artifact set and returns an
  explicit framing decision.
- No specification acceptance or implementation authorization is implied.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Milestone C0: JCS definition implementation plan | Complete | Pull request #16 approved at `53504ba7865e02235b3ddcf5228b40ca972b7d68`, merged at `b785bbc71421da84568f2d2be00d877d4e67bdb6`, and passed merged-main run `30634584406` without annotations |
| Checkpoint A: C0 lifecycle closeout | Complete | Pull request #17 merged at `13756d97081e45684564accb666703845017800d`; merged-main run `30635006984` passed without annotations |
| Checkpoint B: C1 requirements and alternatives | Complete | Draft PR #18 at `5dea1aea6e8b264b74c05b063157f72e863fff54` contains the complete first proposal; run `30635469490` passed; the Chief Architect found no framing defect and identified the blocking evidence gaps |
| Checkpoint C: C1 framing review | In review | The Chief Architect recommended **DEFER JCS**, confirmed delegated acknowledgment for canonical outcome preparation, kept C2 blocked, and authorized revised pull request #18 for final exact-artifact closure review |

## Dependencies

- Reviewed GitHub `main` remains authoritative.
- The active [JCS Definition Implementation Plan](docs/JCS_DEFINITION_PLAN.md)
  owns order, gates, artifacts, and completion evidence.
- The [ADR Process](docs/adr/README.md) governs decision triggers, levels, and
  acceptance.
- The [Component Registry](docs/reference/COMPONENT_REGISTRY.md) keeps JCS at
  **Named** maturity until the complete specification is accepted.
- Explicit maintainer intent remains required before JCS-01 can accept a
  purpose or any question of project or human authority can be decided.
- Responsibility framing precedes information authority, consumer contracts,
  and interface requirements.
- Milestone C2 remains blocked. Reconsideration requires an explicit problem
  or purpose, named consumer and need, candidate responsibility and boundary,
  failure consequence, and Chief Architect authorization for reopened C1;
  C2 would still require a reviewed candidate direction and separate explicit
  authorization.
- The [Definition of Done](docs/DEFINITION_OF_DONE.md) applies to each
  checkpoint.

## Risks

| Risk | Response |
| --- | --- |
| The acronym is expanded from assumption or conversation momentum. | Compare retain, expand, rename, and defer alternatives; keep JCS-01 open until reviewed maintainer intent exists. |
| A broad "core" proposal absorbs unrelated responsibilities. | Require one coherent problem, explicit exclusions, named consumers, and a proportionate System ADR. |
| A proposed specification is mistaken for current architecture. | Mark it **Proposed**, keep JCS **Named**, repeat the acceptance gate, and do not update current architecture as if decided. |
| C1 creates placeholder artifacts around the proposal. | Permit only the proposed specification and triggered proposed ADRs; keep all other artifact gates closed. |
| Bootstrap products bias the conceptual contract. | Treat them as reported facts only and defer all product and deployment selection. |
| An ADR bundles several independent decisions. | Split choices by responsibility, authority, interface, or trust consequence when reviewers cannot assess them coherently. |
| Maintainer intent remains only in chat. | Promote it into the proposed specification with evidence category and gate before depending on it. |
| The existence of a specification file makes JCS feel inevitable. | Preserve proceed, revise, defer, remove, and no-JCS outcomes until an accepted decision closes them. |
| Evidence gaps are converted into low-visibility backlog work. | Keep each gap in the decision register with its consequence, owner, and gate. |
| Review of a stale or partial artifact authorizes dependent work. | Require exact head, complete files, passing checks, and explicit recommendation dispositions. |
| Deferral is mistaken for rejection or completion. | Keep JCS **Named**, keep the specification **Proposed**, state the reconsideration triggers, and repeat that C2 and implementation remain blocked. |

## Update and close rules

Update this file when checkpoint scope, evidence, assumptions, dependencies, or
risks change. At sprint close:

1. Record the exact artifacts and review decision for every completed
   checkpoint.
2. Carry incomplete work only with its reason, risk, owner, and revised gate.
3. Record new risks and process lessons.
4. Update status, roadmap, plan, registry, ADR index, and changelog where their
   owned reality changes.
5. Define the next sprint before beginning work outside approved scope.
