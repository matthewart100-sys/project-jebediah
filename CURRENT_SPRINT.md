# Current Sprint

## Genesis Sprint 1: Working Methodology

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Establish the permanent planning, contribution, and engineering methodology
that all remaining Project Genesis work must follow.

## Context

The first Genesis checkpoint established the project mission, current status,
documentation hierarchy, and approved implementation plan. This sprint makes
that foundation operational by defining how work is selected, reviewed,
completed, and tracked.

The two-week window is a planning default, not permission to sacrifice quality.
The sprint closes when its accepted outcomes are complete or when remaining
work is explicitly carried forward.

## Committed scope

### Checkpoint A: Planning and contribution workflow

- Contribution guide
- Git workflow and branching strategy
- Sprint methodology
- Current sprint
- Roadmap
- Universal Definition of Done
- Chief Architect review template
- Canonical navigation, status, plan, and changelog updates

### Checkpoint B: Engineering documentation standards

- Repository standards
- Engineering standards
- Documentation standards
- Cross-document ownership and maintenance rules

Each checkpoint is delivered as a separate, reviewable pull request.

## Non-goals

- Application or infrastructure implementation
- JCS design or implementation
- Collector design
- API, schema, protocol, language, or framework selection
- Deployment changes to the reported home-lab environment
- GitHub Actions enforcement, which belongs to a later Genesis milestone
- License selection, which requires a maintainer decision

## Acceptance criteria

- A contributor can determine how to select, branch, commit, validate, review,
  merge, and close work.
- `CURRENT_SPRINT.md` identifies one active goal and bounded scope.
- `ROADMAP.md` distinguishes strategic sequence from schedules or promises.
- The Definition of Done applies across documentation, code, architecture,
  infrastructure, and security changes.
- Chief Architect reviews are based on actual artifacts and produce an
  explicit recorded decision.
- Checkpoint A and Checkpoint B each pass documentation validation and receive
  the required review.
- Status, navigation, plan, and changelog remain consistent.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Genesis source-of-truth checkpoint | Complete | Pull request #1 merged into `main` |
| Checkpoint A: planning and contribution workflow | Complete | Pull request #2 approved by the Chief Architect and merged |
| Checkpoint B: engineering documentation standards | In progress | Active bounded feature branch |
| Milestone 3: AI onboarding and memory | Pending | Starts after Sprint 1 methodology is accepted |

## Dependencies

- Authoritative `main` remains synchronized with reviewed pull requests.
- Chief Architect review receives the exact changed files or diff.
- The maintainer retains final repository authority.
- Unknown architecture remains explicitly deferred.

## Risks

| Risk | Response |
| --- | --- |
| Process documentation becomes bureaucracy | Require each rule to protect traceability, safety, quality, or maintainability. |
| Sprint scope expands into architecture | Enforce the non-goals and require an ADR trigger assessment. |
| Documentation duplicates the Genesis plan | Give each operational document one clear responsibility and link instead of copying. |
| Calendar pressure lowers quality | Carry work forward explicitly rather than declaring incomplete work done. |
| Reviews rely on summaries | Require actual artifacts in the Chief Architect evidence package. |

## Update rule

Update this file when sprint scope, status, dependencies, or risk changes. At
sprint close:

1. Record completed outcomes in the changelog and project status.
2. Move unfinished work deliberately; do not erase it.
3. Capture process improvements.
4. Define the next sprint before beginning unscheduled implementation.
