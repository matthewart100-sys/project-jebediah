# Current Sprint

## Genesis Sprint 5: GitHub Enforcement

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Convert approved repository, documentation, security, and Git standards into
proportionate GitHub enforcement that a sole maintainer can use without
bypassing the documented review lifecycle.

## Context

Pull requests #7 and #8 completed the testing, security, operations, release,
and repository-hygiene foundation. The repository now defines what evidence a
change needs, but GitHub does not yet enforce a documentation-quality check,
structured contribution intake, private vulnerability reporting, or
protection of `main`.

GitHub API evidence collected on 2026-07-30 confirms that private
vulnerability reporting is disabled and `main` is unprotected. Sprint 5
closes those verified gaps in two reviewable checkpoints.

## Committed scope

### Checkpoint A: Repository-owned quality gate

- A maintained, standard-library documentation and repository validator
- A least-privilege GitHub Actions workflow using immutable action revisions
- A pull-request template aligned with the Definition of Done and evidence
  categories
- Structured bug, feature, and architecture issue forms
- A safe issue chooser route to the canonical security policy
- Canonical documentation integration

### Checkpoint B: Verified GitHub control plane

- Successful execution of the documentation-quality workflow on `main`
- Enabled and verified GitHub private vulnerability reporting
- Proportionate protection for `main` requiring pull requests and the
  documentation-quality check without requiring an impossible independent
  approval
- Blocked force pushes and branch deletion
- Required conversation resolution where supported
- Canonical records of the effective settings and verification evidence

Each checkpoint uses a separate pull request and Chief Architect review.
Control-plane changes occur only after Checkpoint A is merged and its check
name is verified.

## Non-goals

- Application, service, schema, Digital Twin, or infrastructure implementation
- Home-lab changes or disclosure of private operational details
- Selecting a product language, build system, dependency manager, or general
  test framework
- Dependency, container, infrastructure, or model scanning before those
  artifact classes exist
- Requiring approval from a second maintainer who does not exist
- Creating the `v0.1.0` release before the Milestone 7 audit

## Acceptance criteria

- Contributors can invoke one documented local command for the automated
  repository checks.
- The workflow runs for pull requests and pushes to `main`, uses read-only
  repository permission, and pins third-party actions to immutable revisions.
- The validator checks canonical files, Markdown structure and local links,
  common sensitive values, bootstrap or runtime artifacts, and repository
  hygiene without adding a runtime dependency.
- Pull-request and issue templates request useful evidence without treating
  templates as substitutes for review.
- Private vulnerability reporting is enabled and the security policy points
  to an actually verified private route.
- `main` requires pull requests, conversation resolution, and the successful
  documentation-quality check while blocking force pushes and deletion.
- The effective GitHub settings are read back after configuration and recorded
  without secrets.
- Exact artifacts and proposed control settings receive explicit Chief
  Architect decisions.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Milestone 5A: testing and security | Complete | Pull request #7 approved by the Chief Architect and merged |
| Milestone 5B: operations, release, and repository hygiene | Complete | Pull request #8 approved by the Chief Architect and merged |
| Checkpoint A: repository-owned quality gate | In progress | Bounded Sprint 5 feature branch |
| Checkpoint B: verified GitHub control plane | Pending | Begins after Checkpoint A passes on `main` |
| Milestone 7: Genesis audit and release | Pending | Begins after GitHub enforcement is verified |

## Dependencies

- The [Git Workflow](docs/GIT_WORKFLOW.md) owns the intended branch policy.
- The [Security Policy](SECURITY.md) owns the vulnerability-reporting route.
- The [Repository Standards](docs/REPOSITORY_STANDARDS.md) and
  [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md) own automated
  repository rules.
- The `documentation-quality` check must exist successfully on `main` before
  it becomes required protection.
- The authenticated repository owner must retain GitHub administration
  permission for control-plane configuration.
- Chief Architect review receives the exact artifacts, proposed settings, and
  sanitized verification evidence.

## Risks

| Risk | Response |
| --- | --- |
| A quality script becomes an accidental application stack | Use Python standard library only and limit it to repository policy. |
| A pattern scan claims to prove the repository has no secrets | Describe it as a common-pattern guard and retain human review. |
| Protection locks out the sole maintainer | Require pull requests and checks with zero required approving reviews. |
| A required check name is guessed incorrectly | Merge the workflow, observe its successful check name, then configure protection. |
| Security reports are directed to a route that does not exist | Enable, read back, and test the GitHub private-reporting capability before updating the policy. |
| Templates create bureaucratic noise | Require only information needed for reproduction, decisions, risk, and evidence. |
| Mutable action tags introduce supply-chain drift | Resolve supported tags to full commit revisions and retain version comments. |

## Update rule

Update this file when sprint scope, status, dependencies, or risk changes. At
sprint close:

1. Record completed outcomes in the changelog and project status.
2. Move unfinished work deliberately; do not erase it.
3. Capture process improvements and accepted recommendations.
4. Define the next sprint before beginning unscheduled implementation.
