# Contributing to Project Jebediah

Project Jebediah uses documentation-first, reviewable engineering. A
contribution is complete only when the repository accurately explains the
change, its rationale, its validation, and any remaining uncertainty.

The repository is public but does not yet have an approved software license.
Prospective external contributors should coordinate with the maintainer before
investing in substantive work.

## Before starting

Read these documents in order:

1. [README](README.md)
2. [Mission and Manifesto](docs/MISSION_AND_MANIFESTO.md)
3. [Project Status](PROJECT_STATUS.md)
4. [Current Sprint](CURRENT_SPRINT.md)
5. [Roadmap](ROADMAP.md)
6. [Repository Standards](docs/REPOSITORY_STANDARDS.md)
7. [Engineering Standards](docs/ENGINEERING_STANDARDS.md)
8. [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)
9. [Git Workflow](docs/GIT_WORKFLOW.md)
10. [Definition of Done](docs/DEFINITION_OF_DONE.md)
11. Any architecture or ADR documents relevant to the proposed
   change

If a required document does not yet exist, treat that absence as a project
constraint. Do not invent the missing policy inside implementation code.

## Choose and describe the work

A contribution should have one coherent outcome. Before implementation:

- Confirm that the work belongs in the current sprint or has explicit
  maintainer authorization.
- Describe the problem, intended outcome, non-goals, and acceptance criteria.
- Identify affected canonical documents.
- Determine whether the work changes architecture or requires an ADR.
- Record material assumptions and unresolved questions.

Use a GitHub issue when the work needs discussion, coordination, design
clarification, or tracking beyond a single obvious pull request. Security
vulnerabilities and private infrastructure details must not be disclosed in a
public issue.

## Branches

Never perform feature work directly on `main`. Use a short-lived branch from an
up-to-date `main` representing one reviewable outcome.

The [Git Workflow](docs/GIT_WORKFLOW.md) is the canonical owner for branch
prefixes, naming, synchronization, and lifecycle. This guide deliberately does
not duplicate those rules.

## Commits

Commits must be small, logical, and understandable without conversation
history. Use a concise Conventional Commit-style subject:

- `docs: define the sprint process`
- `fix: handle collector timeout`
- `test: cover configuration fallback`
- `refactor: isolate graph client`
- `chore: update repository tooling`

Use `feat:` only when the commit adds approved product behavior. Do not hide
unrelated cleanup inside another change.

Every commit must avoid secrets, private addresses, credentials, personal data,
generated noise, and unexplained binary artifacts.

## Pull requests

Open a draft pull request when early visibility is useful. The description
must state:

- What changed
- Why it changed
- User, developer, operational, or documentation impact
- What is deliberately out of scope
- Validation performed
- Documentation and changelog impact
- ADR impact
- Known facts, assumptions, and open questions when relevant
- Whether AI materially contributed and which evidence the reviewer should
  inspect

Significant architecture, milestone, or canonical-documentation changes use
the [Chief Architect Review Template](docs/reviews/ARCHITECT_REVIEW_TEMPLATE.md).
The reviewer must receive the actual diff or changed files, not only a summary.

## Validation

Run checks proportionate to the change and report their exact results. At a
minimum:

- Inspect the final diff.
- Run `git diff --check`.
- Verify affected links and references.
- Confirm the repository contains no secrets or private operational data.
- Run applicable tests or explain why none apply.
- Evaluate whether `PROJECT_STATUS.md`, `CURRENT_SPRINT.md`, `ROADMAP.md`, and
  `CHANGELOG.md` need updates.

Passing checks do not replace review of behavior, architecture, or meaning.

## Review and merge

A pull request may merge only when:

- Its acceptance criteria are met.
- Review comments are resolved or explicitly deferred with rationale.
- Required architectural review has an explicit decision.
- The [Definition of Done](docs/DEFINITION_OF_DONE.md) is satisfied.
- The branch is current enough to merge safely.

Pull requests are squash-merged by default. The pull-request title becomes the
durable summary on `main`, so it must accurately describe the full change.

## AI-assisted contributions

AI contributors follow the same quality bar as humans. They must:

- Establish context from the repository before acting.
- Distinguish repository evidence from conversational claims.
- State assumptions rather than silently resolving uncertainty.
- Respect approval and architecture gates.
- Provide the reviewer with actual artifacts and validation evidence.
- Leave repository documentation more accurate than before.

Chat output is not a substitute for documentation, a diff, tests, or review.

## Getting help

If the repository does not contain enough information to make a safe decision,
stop dependent work and raise the missing question. Document the answer in the
appropriate canonical file before relying on it.
