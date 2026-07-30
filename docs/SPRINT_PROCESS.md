# Sprint Process

## Purpose

Sprints turn the roadmap into bounded, reviewable outcomes without converting
uncertain architecture into artificial deadlines.

The default sprint length is two weeks. Outcome quality and explicit carryover
matter more than claiming that every planned item finished on schedule.

## Canonical artifacts

- `ROADMAP.md` describes strategic sequence and gates.
- `CURRENT_SPRINT.md` describes one active sprint.
- GitHub issues and pull requests hold task discussion and evidence.
- `PROJECT_STATUS.md` records current reality.
- `CHANGELOG.md` records delivered outcomes.
- ADRs record material architectural decisions.

These artifacts must not contradict one another.

## Roles

### Maintainer

- Sets final priorities and authority.
- Accepts sprint scope.
- Resolves business or ownership questions.
- Controls repository merges and releases.

### Chief Architect

- Reviews architecture-significant scope and artifacts.
- Protects design intent and decision quality.
- Returns explicit checkpoint decisions.
- Does not approve artifacts it cannot inspect.

### Lead Engineer or implementing contributor

- Converts accepted scope into reviewable work.
- Identifies dependencies and uncertainty.
- Provides actual diffs, validation, and handoffs.
- Keeps canonical documentation accurate.

## Sprint lifecycle

### 1. Prepare

Review project status, roadmap gates, unfinished work, risks, and capacity.
Candidate work must have a clear outcome and known reason for being selected.

### 2. Plan

Write the sprint goal first. Then define:

- Target window
- Committed scope
- Non-goals
- Acceptance criteria
- Work items and review checkpoints
- Dependencies
- Risks and responses

Do not commit work merely because it is interesting or technically adjacent.

### 3. Execute

- Use short-lived branches and pull requests.
- Keep work items small enough to review.
- Update status when reality changes.
- Surface blockers and assumptions early.
- Maintain the Definition of Done.
- Route architecture-significant checkpoints to the Chief Architect with
  actual artifacts.

### 4. Review

At each logical checkpoint:

- Compare the diff to acceptance criteria.
- Run proportional validation.
- Review documentation and changelog impact.
- Assess ADR impact.
- Obtain the required explicit decision.

Rejected or revision-required work remains open; it is not declared complete.

### 5. Close

At sprint end:

- Mark delivered outcomes complete with evidence.
- Update project status and changelog.
- Carry unfinished work forward deliberately or return it to the roadmap.
- Record process lessons.
- Identify newly resolved or newly discovered risks.
- Define the next sprint before beginning unrelated work.

## Scope changes

New information may change sprint scope. When it does:

1. Explain the trigger.
2. State what enters or leaves scope.
3. Evaluate dependencies and risk.
4. Update `CURRENT_SPRINT.md`.
5. Obtain the appropriate authority.

Silent scope expansion is not acceptable.

## Carryover

Incomplete work is not failure when uncertainty was handled honestly. Carryover
must state:

- What remains
- Why it remains
- Whether assumptions changed
- Whether the work still belongs next
- What evidence or decision will unblock it

Do not repeatedly carry an item without reconsidering its size or priority.

## Measures

Useful sprint measures are evidence of flow and quality, not targets to game:

- Accepted outcomes
- Review turnaround
- Rework caused by missing context
- Escaped documentation inconsistencies
- Failed checks or incidents
- Age of blockers and open questions

Velocity is not used as a proxy for engineering quality.

## Sprint document requirements

Every `CURRENT_SPRINT.md` must contain:

- Name and target window
- Status
- Goal
- Context
- Committed scope
- Non-goals
- Acceptance criteria
- Work status with evidence
- Dependencies
- Risks
- Update and close rules

There is exactly one active current-sprint document.
