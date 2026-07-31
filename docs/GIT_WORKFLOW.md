# Git Workflow

## Purpose

Git is the traceability and recovery mechanism for Project Jebediah. This
workflow keeps `main` authoritative while allowing humans and AI contributors
to work in small, reviewable increments.

## Core rules

- `main` is the stable source of truth.
- Feature work never begins directly on `main`.
- Branches are short-lived and represent one coherent outcome.
- Commits are small and explain intent.
- Pull requests contain actual artifacts and validation evidence.
- Documentation changes accompany changes to project reality.
- History is never rewritten on `main`.
- Secrets and private operational data are never committed.

## Starting work

Before creating a branch:

1. Read `PROJECT_STATUS.md`, `CURRENT_SPRINT.md`, and relevant standards.
2. Confirm the work is authorized and has acceptance criteria.
3. Apply the [ADR Process](adr/README.md) and check whether Chief Architect
   review is required.
4. Make sure the working tree is understood and unrelated changes are
   preserved.
5. Synchronize local `main` with `origin/main` using a fast-forward update.

Create a branch using:

- `feature/<topic>`
- `fix/<topic>`
- `docs/<topic>`
- `chore/<topic>`
- `agent/<topic>` for automated engineering agents

Use lowercase, hyphenated topics. Do not create long-lived `develop` or
environment branches.

## Commit discipline

Each commit should:

- Express one logical change.
- Build on a valid repository state.
- Avoid unrelated formatting or cleanup.
- Include relevant documentation and tests when they are inseparable from the
  change.
- Use a concise Conventional Commit-style subject.

Preferred subjects include:

- `docs: define project status categories`
- `feat: add approved collector capability`
- `fix: prevent duplicate entity creation`
- `test: cover workflow retry behavior`
- `refactor: isolate vector store adapter`
- `chore: pin documentation tooling`

Commits on a review branch may be corrected with additional commits. Do not
rewrite a branch after other contributors have based work on it without
coordination.

## Keeping a branch current

Prefer small branches that finish before substantial divergence occurs. Before
merge:

- Fetch the remote.
- Review changes made to `main`.
- Rebase or merge only when necessary and when the chosen operation will not
  destroy collaborator work.
- Rerun affected validation after resolving conflicts.

Conflict resolution must preserve current canonical documentation. Never pick
one side mechanically when both sides encode project decisions.

## Pull-request lifecycle

### Draft

Open a draft when the direction is useful to review but acceptance criteria are
not complete. A draft is not permission to merge incomplete work.

### Ready for review

Mark ready only when:

- The scope is complete.
- The final diff has been inspected.
- Validation results are recorded.
- Documentation and changelog impact are addressed.
- ADR impact is assessed.
- Known facts, assumptions, and open questions are labeled where relevant.

### Architecture review

Milestone, foundational, system, or otherwise architecture-significant changes
use the [Chief Architect Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md).
Provide the actual diff or changed files. A summary alone is insufficient
evidence.

The [ADR Process](adr/README.md) defines Foundational, System, and
Implementation decision levels, their triggers, and when dependent
implementation must wait. The ADR and every affected current architecture or
standards document change together.

The review decision must be one of:

- `APPROVED TO MERGE`
- `REVISIONS REQUIRED`
- `APPROVED TO CONTINUE WITHOUT MERGE`

Record the decision or a durable summary in the pull request.

### Merge

Squash merge is the default. The pull-request title becomes the commit subject
on `main` and must summarize the complete result.

Merge only when:

- Required review is approved.
- Checks pass.
- Review comments are resolved.
- The Definition of Done is satisfied.
- The base branch and changed artifacts are understood.

Delete the remote feature branch after a successful merge. The pull request and
merge commit preserve the durable history.

## Protection policy

GitHub API read-back on 2026-07-30 verified the following effective `main`
protection:

- Pull requests are required.
- `documentation-quality` is required with strict branch currency.
- Review conversations must be resolved.
- Force pushes and branch deletion are blocked.
- Zero approving reviews are required.
- Administrator enforcement is disabled.
- Linear-history enforcement, branch locking, creation blocking, and fork
  syncing are disabled.

The zero-review and administrator settings reflect the verified
single-maintainer state. Requiring an independent approval that the maintainer
cannot provide would deadlock ordinary delivery. Chief Architect review
remains an architectural process gate and is recorded as evidence.

Administrator bypass is a documented residual risk, not permission to skip the
normal pull-request process. Reassess it when a second maintainer joins,
governance authority changes, or production releases begin. Read back GitHub
settings after every protection change and update this section when effective
state changes.

## Emergency changes

An emergency does not eliminate traceability.

1. Create the smallest safe branch.
2. Describe the incident and immediate risk.
3. Implement the narrow correction.
4. Validate the correction and rollback path.
5. Use a pull request unless GitHub itself is unavailable.
6. Document any exceptional direct action immediately afterward.
7. Create follow-up work for root cause, tests, and permanent documentation.

Emergency procedure must not become a shortcut for ordinary work.

## Release tags

Release tags are created from reviewed commits on `main`, never from a feature
branch. Tagging and release notes follow the release process once that document
is approved.

## Repository cleanup

After merge:

- Synchronize local `main`.
- Verify the expected merge commit and files.
- Remove obsolete remote branches.
- Keep local branches only while they provide active recovery or review value.
- Do not use destructive cleanup commands against unverified paths or
  uncommitted work.
