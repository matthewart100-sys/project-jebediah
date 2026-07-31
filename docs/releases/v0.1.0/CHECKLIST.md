# v0.1.0 Engineering-Foundation Release Checklist

**Release:** `v0.1.0`

**Type:** Foundation and documentation release

**Status:** Release candidate in review

**Last reviewed:** 2026-07-30

## Purpose and authority

This checklist applies the canonical [Release Process](../../RELEASE_PROCESS.md)
to the first Project Jebediah release. It records release-specific evidence;
it does not replace release policy, the
[Definition of Done](../../DEFINITION_OF_DONE.md), or the
[Security Policy](../../../SECURITY.md).

Candidate requirements must be `Pass` or justifiably `Not applicable` before
the release pull request may merge. Publication requirements depend on the
merged commit, tag, or GitHub release and remain `Pending` until that external
state exists and is read back. The release is not complete while a publication
requirement is `Pending` or `Blocked`.

## Status and gate meanings

| Value | Meaning |
| --- | --- |
| Pass | Exact evidence satisfies the requirement. |
| Pending | Evidence or an authorized decision is still required. |
| Blocked | A known failure prevents the applicable gate. |
| Not applicable | The requirement does not apply to this foundation-only release for the stated reason. |
| Candidate | Evidence must be complete before the release pull request merges. |
| Publication | Evidence can exist only after merge, tag creation, or GitHub release publication. |

## Release identity and boundary

| Requirement | Gate | Status | Evidence or required action |
| --- | --- | --- | --- |
| Version is agreed | Candidate | Pass | The approved Genesis plan and release process define `v0.1.0`. |
| Release type is explicit | Candidate | Pass | Foundation and documentation release; no application or infrastructure artifact. |
| Scope is bounded | Candidate | Pass | Reviewed Project Genesis repository memory and enforcement through Milestone 7. |
| Prior release is identified | Candidate | Pass | Git and GitHub read-back on 2026-07-30 found no prior tag or GitHub release. |
| Release-history baseline is exact | Candidate | Pass | Included history begins at `e42edd0c67e144b556adb77416a1e079eb106b93`; the immutable tag supplies the final inclusive target. |
| Public boundary is prominent | Candidate | Pass | [Release Notes](RELEASE_NOTES.md) lead with the engineering-foundation boundary and enumerate excluded software and infrastructure artifacts. |
| License state is accurate | Candidate | Pass | No license is approved; public visibility is not represented as reuse permission. |
| Release ownership is explicit | Candidate | Pass | Maintainer `matthewart100-sys` owns release and withdrawal decisions; Codex records validation evidence; no deployment owner is required because nothing is deployed. |
| Final source commit is exact | Publication | Pending | After merge, read back synchronized `main`, the successful required check, and the commit selected for the tag. |

## Project Genesis gates

| Requirement | Gate | Status | Evidence or required action |
| --- | --- | --- | --- |
| Milestones 0 through 6 are complete | Candidate | Pass | [Genesis Plan](../../genesis/PROJECT_GENESIS_PLAN.md) records pull requests #1 through #10 and verified GitHub controls. |
| Milestone 7 foundation audit is complete | Candidate | Pass | Pull request #11 was approved at `20b1f559f3a396d9c59e63030337c7fc48f4c63f` and merged at `5c92b5920341c954e51452ff8760ea4aaef3e5bc`. |
| Every required foundation topic has a substantive owner | Candidate | Pass | The [Genesis Foundation Audit](../../genesis/GENESIS_FOUNDATION_AUDIT.md) maps every required topic to a substantive canonical owner. |
| Cross-document status and ownership agree | Candidate | Pass | Findings GA-001 through GA-007 are corrected on `main`; the release candidate advances the audit, sprint, roadmap, status, and changelog together. |
| Clean-room onboarding succeeds | Candidate | Pass | Two repository-only AI reviews cover the system and lifecycle questions plus the complete entry path. |
| Material clean-room findings are resolved | Candidate | Pass | Neither reader found a material blocker; minor friction and test limitations are recorded with dispositions. |
| Chief Architect approves the complete audit | Candidate | Pass | The PR #11 review decision and final addendum approved the exact audit artifacts with no blocker. |
| Chief Architect approves the release candidate | Candidate | Pending | Review the exact release pull-request head, final artifacts, validation, and residual risk. |
| Maintainer authorizes the public tag and release | Publication | Pending | Obtain the delegated final decision only after the merged commit and its required check are verified. |

## Repository and documentation evidence

| Requirement | Gate | Status | Evidence or required action |
| --- | --- | --- | --- |
| Repository validator passes locally | Candidate | Pass | `python scripts/validate_docs.py` checks 36 Markdown files and 45 tracked files. |
| Validator compiles | Candidate | Pass | `python -m py_compile scripts/validate_docs.py`. |
| Workflow and issue configuration remains verified | Candidate | Pass | The release diff does not change the workflow or four issue-template YAML files validated during the approved audit; GitHub Actions run `30597270334` passes on the merged audit commit. |
| Repository object graph is sound | Candidate | Pass | `git fsck --no-dangling`. |
| Release diff is whitespace-clean | Candidate | Pass | `git diff --check main`. |
| Required pull-request check passes | Candidate | Pending | Verify `documentation-quality` on the exact release-candidate head. |
| Required merged-commit check passes | Publication | Pending | Verify `documentation-quality` on the exact merged release commit before tagging. |
| Local links and Markdown structure pass | Candidate | Pass | Supplied by the repository validator. |
| No bootstrap archive or runtime data is tracked | Candidate | Pass | Validator and final tracked-tree review find none. |
| No secrets or private operational data are exposed | Candidate | Pass | Common-pattern and RFC 1918 checks pass; final public-text review finds no credential or private-topology content. |
| No empty policy placeholder is present | Candidate | Pass | Topic mapping and tracked-tree review find no empty policy or speculative directory artifact. |
| Canonical navigation is complete | Candidate | Pass | The full entry-path review reaches all required architecture and lifecycle owners. |
| Status, sprint, roadmap, and changelog agree | Candidate | Pass | All identify the approved audit and the separate `v0.1.0` release gate without claiming publication. |
| Architecture and ADR index agree | Candidate | Pass | Phase 0 selected no implementation technology or product architecture requiring a numbered ADR. |

## Security and lifecycle evidence

| Requirement | Gate | Status | Evidence or required action |
| --- | --- | --- | --- |
| Private vulnerability reporting is usable | Candidate | Pass | GitHub API read-back on 2026-07-30 returned `enabled: true`; `SECURITY.md` owns the route. |
| `main` protection matches policy | Candidate | Pass | API read-back verifies strict `documentation-quality`, pull-request and conversation requirements, blocked force pushes and deletion, zero approvals, and administrator bypass. |
| Known security gaps are accurate | Candidate | Pass | GitHub API read-back on 2026-07-30 reports secret scanning, push protection, validity checks, non-provider patterns, and Dependabot security updates disabled; policy records the available common-pattern guard and absence of artifact-specific scanning. |
| Open-work state is clear | Candidate | Pass | GitHub read-back on 2026-07-30 found no open issue, tag, or release. |
| Supported-version impact is explicit | Candidate | Pass | No Project Jebediah application version is supported by this foundation release. |
| Compatibility impact is explicit | Candidate | Pass | Initial documentation release; no runtime interface, schema, data, or deployment compatibility exists. |
| Migration is defined | Candidate | Not applicable | There is no prior release, persisted application state, or runtime schema to migrate. |
| Deployment is defined | Candidate | Not applicable | The release publishes Git history, an annotated tag, and GitHub notes; it deploys no service or infrastructure. |
| Rollback or withdrawal is understood | Candidate | Pass | Do not rewrite the tag; correct with a reviewed later version or mark the GitHub release withdrawn with rationale. |
| Recovery impact is understood | Candidate | Pass | The release contains Git-backed engineering memory and no unique runtime state. |

## Changelog and release artifacts

| Requirement | Gate | Status | Evidence or required action |
| --- | --- | --- | --- |
| `Unreleased` entries are finalized under `0.1.0` | Candidate | Pass | The complete Genesis history is under `## [0.1.0] - 2026-07-30`. |
| A fresh `Unreleased` section is deliberate | Candidate | Pass | A heading is retained for later entries without empty category headings. |
| Release notes describe notable outcomes | Candidate | Pass | [Release Notes](RELEASE_NOTES.md) describe the foundation, verification, limitations, recovery, and next gate. |
| Release notes state limitations | Candidate | Pass | Notes identify no application, deployment, verified home-lab inventory, supported software, or approved license. |
| Artifact inventory is explicit | Candidate | Pass | The only artifacts are the reviewed Git commit, annotated tag, and GitHub release record; there are no binaries, containers, models, schemas, migrations, or deployments. |
| Release notes disclose no sensitive details | Candidate | Pass | Final public-text review against `SECURITY.md` found no secret, personal, or private-topology detail. |
| Annotated tag is verified | Publication | Pending | Create `v0.1.0` only at the authorized merged commit and read it back without rewriting. |
| GitHub release is verified | Publication | Pending | Publish the approved notes from the tag and verify the release URL, tag, commit, links, and foundation-only boundary. |
| Durable closeout is recorded | Publication | Pending | A reviewed closeout change records the tag, release URL, verification, Phase 0 completion, and Phase 1 planning gate. |

## Publication sequence

Perform these steps in order. Stop if any read-back differs from intended
state.

1. Merge the approved audit checkpoint.
2. Create a release branch from synchronized `main`.
3. Finalize changelog, status, sprint, roadmap, release notes, and this
   checklist.
4. Run all required local checks.
5. Open the release pull request and wait for its required GitHub check.
6. Give the Chief Architect the exact release artifacts and candidate commit.
7. Resolve review findings and obtain approval to merge the release candidate.
8. Squash-merge the approved release pull request.
9. Synchronize local `main`; verify a clean tree and the exact merge commit.
10. Confirm `documentation-quality` succeeds on that merged commit.
11. Give the Chief Architect the exact merged commit and final read-back;
    obtain explicit delegated authorization for the tag and GitHub release.
12. Create annotated tag `v0.1.0` at that exact commit.
13. Push the tag without rewriting it.
14. Create the GitHub release using the reviewed release notes.
15. Verify the public tag, commit, notes, links, and foundation-only boundary.
16. Record final publication evidence and close Phase 0 through a reviewed
    repository change.

## Final authorization

The release-candidate pull request may merge only after every `Candidate`
requirement is `Pass` or justifiably `Not applicable` and the Chief Architect
approves its exact head. Tag creation remains unauthorized until the merged
commit and required check are read back and the maintainer's delegated final
decision explicitly authorizes publication. The release is complete only
after every `Publication` requirement is also `Pass` or justifiably
`Not applicable`.
