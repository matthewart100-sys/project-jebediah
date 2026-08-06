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

Proposed ADR 0017's Independent Reviewer policy becomes effective only after
acceptance and merge. ADR 0005 controls the successor pull request's transition
and requires incumbent Work Mode exact-head review until then.

Before creating a branch:

1. Read `PROJECT_STATUS.md`, `CURRENT_SPRINT.md`, and relevant standards.
2. Confirm the work is authorized and has acceptance criteria.
3. Identify the current gate and authorized role under the
   [Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md).
4. Apply the [ADR Process](adr/README.md) and check which independent-review and
   Chief Architect decisions are required.
5. Make sure the working tree is understood and unrelated changes are
   preserved.
6. Synchronize local `main` with `origin/main` using a fast-forward update.

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

Before independent review, a proposal spanning multiple documents
must be committed and pushed to one short-lived branch in the authoritative
repository. Its review packet identifies the full base and head commits,
complete file manifest, and repository-backed compare or pull-request diff.
All artifacts needed to interpret the proposal must be tracked at that head;
chat attachments and uncommitted files cannot satisfy the review target. The
[Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
owns abandonment and successor handling when an exact proposal target is lost.

The distinct Independent Reviewer performs the required architecture or
implementation review first. Routine review uses a fresh, read-only normal
ChatGPT conversation; Work Mode is optional only when the Chief Architect
explicitly requests unusually high-risk, cross-cutting, or adversarial review.
The Chief Architect then grants or withholds final approval for the exact
artifacts. The Project Coordination Protocol owns this sequence, the required
same-artifact reviewer separation, and the written disposition of blocking
findings.

The [ADR Process](adr/README.md) defines Foundational, System, and
Implementation decision levels, their triggers, and when dependent
implementation must wait. The ADR and every affected current architecture or
standards document change together.

The review decision must be one of:

- `APPROVED TO MERGE`
- `REVISIONS REQUIRED`
- `APPROVED TO CONTINUE WITHOUT MERGE`

Record the decision or a durable summary in the pull request.

### Proportional documentation review

Classify documentation-only changes using the
[Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md):

- Editorial corrections use documentation, link, and whitespace validation
  plus Chief Architect exact-head merge approval. They do not require
  architecture or implementation review unless meaning changes or the
  classification is disputed.
- Architecture-significant documentation follows the full Independent Reviewer
  and Chief Architect sequence.
- Documentation Suite closeout receives independent documentation and evidence
  review in a fresh, read-only normal ChatGPT conversation, followed by Chief
  Architect exact-head merge approval.
  Merging that closeout pull request completes the closeout and does not create
  a recursive closeout requirement.

### Merge

Squash merge is the default. The pull-request title becomes the commit subject
on `main` and must summarize the complete result.

The maintainer or another explicitly assigned non-author Merge Operator executes
the exact Chief Architect-approved merge. An author or implementer may not merge
its own artifact, and merge execution does not grant decision authority.

Merge only when:

- Required review is approved.
- Every independent-review blocking finding is corrected or has the explicit
  Chief Architect disposition required by the Project Coordination Protocol.
- The Chief Architect approved the exact pull request and head commit.
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

An emergency does not eliminate traceability or a merge gate. Only the Chief
Architect may declare a repository engineering emergency under the
[Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md).

1. Record the active material risk, time boundary, exact scope, rollback, and
   the pre-implementation independent architecture-review gate being deferred.
2. Obtain Chief Architect authorization before repository implementation.
3. Create the smallest safe branch and implement only the reversible
   containment or correction that was authorized.
4. Validate the correction and rollback path.
5. Before merge, obtain the deferred independent architecture review and the
   normal independent implementation validation.
6. Correct or obtain an explicit Chief Architect disposition for every
   finding, then obtain Chief Architect approval for the exact pull request and
   head commit.
7. Use the normal pull request, checks, controlled merge, and post-merge
   process. If GitHub is unavailable, repository merge waits until the review
   record and controls are available.
8. Record follow-up work for root cause, tests, and permanent documentation.

Emergency work may not change architecture, ADR decisions, roadmap priority,
sprint scope, interfaces, features, migrations, or broad design. It does not
authorize deployment or live-data mutation. Emergency procedure must not
become a shortcut for ordinary work.

## Release tags

Release tags are created from reviewed commits on `main`, never from a feature
branch. Tagging and release notes follow the approved
[Release Process](RELEASE_PROCESS.md).

## Repository cleanup

After merge:

- Synchronize local `main`.
- Verify the expected merge commit and files.
- Remove obsolete remote branches.
- Keep local branches only while they provide active recovery or review value.
- Do not use destructive cleanup commands against unverified paths or
  uncommitted work.
