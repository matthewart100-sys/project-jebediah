# v0.1.0 Engineering-Foundation Release Checklist

**Release:** `v0.1.0`

**Type:** Foundation and documentation release

**Status:** Candidate audit in progress

**Last reviewed:** 2026-07-30

## Purpose and authority

This checklist applies the canonical [Release Process](../../RELEASE_PROCESS.md)
to the first Project Jebediah release. It records release-specific evidence;
it does not replace release policy, the
[Definition of Done](../../DEFINITION_OF_DONE.md), or the
[Security Policy](../../../SECURITY.md).

The release is blocked while any required row is `Pending` or `Blocked`.
`Not applicable` requires a release-specific rationale.

## Status meanings

| Status | Meaning |
| --- | --- |
| Pass | Exact evidence satisfies the requirement for this candidate. |
| Pending | Evidence or an authorized decision is still required. |
| Blocked | A known failure prevents release. |
| Not applicable | The requirement does not apply to this foundation-only release for the stated reason. |

## Release identity and boundary

| Requirement | Status | Evidence or required action |
| --- | --- | --- |
| Version is agreed | Pass | The approved Genesis plan and release process define `v0.1.0`. |
| Release type is explicit | Pass | Foundation and documentation release; no application or infrastructure artifact. |
| Scope is bounded | Pass | Reviewed Project Genesis repository memory and enforcement through Milestone 7. |
| Prior release is identified | Pass | This is the initial release; no prior tag or GitHub release exists. |
| Included commit range is exact | Pending | Final release PR must record baseline `e42edd0c67e144b556adb77416a1e079eb106b93` through the approved release commit. |
| Public boundary is prominent | Pending | Final notes must retain the foundation-only warning from [Release Notes](RELEASE_NOTES.md). |
| License state is accurate | Pass | No license is approved; public visibility is not represented as reuse permission. |

## Project Genesis gates

| Requirement | Status | Evidence or required action |
| --- | --- | --- |
| Milestones 0 through 6 are complete | Pass | [Genesis Plan](../../genesis/PROJECT_GENESIS_PLAN.md) records PRs #1 through #10 and verified GitHub controls. |
| Milestone 7 foundation audit is complete | Pending | Complete and approve the [Genesis Foundation Audit](../../genesis/GENESIS_FOUNDATION_AUDIT.md). |
| Every required foundation topic has a substantive owner | Pass | The Genesis Foundation Audit maps every required topic to a substantive canonical owner. |
| Cross-document status and ownership agree | Pass | Findings GA-001 through GA-007 are corrected in the audit candidate. |
| Clean-room onboarding succeeds | Pass | Two repository-only AI reviews cover the system/lifecycle questions and the complete entry path. |
| Material clean-room findings are resolved | Pass | Neither reader found a material blocker; minor friction and test limitations are recorded with dispositions. |
| Chief Architect approves the complete foundation | Pending | Record the exact reviewed commit and decision in the release PR. |
| Maintainer authorizes the public tag and release | Pending | Obtain final authorization after all other gates pass. |

## Repository and documentation evidence

| Requirement | Status | Evidence or required action |
| --- | --- | --- |
| Required repository check passes locally | Pending | Run `python scripts/validate_docs.py` on the final candidate and record exact counts. |
| `git diff --check` passes | Pending | Run against the final release change. |
| Required GitHub check passes | Pending | Verify `documentation-quality` on the final release PR and merged release commit. |
| Local links and Markdown structure pass | Pending | Supplied by the final validator run. |
| No bootstrap archive or runtime data is tracked | Pending | Confirm through validator output and final tree review. |
| No secrets or private operational data are exposed | Pending | Run automated common-pattern checks and perform human review. |
| No empty policy placeholder is present | Pass | Topic mapping and tracked-tree review found no empty policy or speculative directory artifact. |
| Canonical navigation is complete | Pass | The full entry-path review reached all required architecture and lifecycle owners. |
| Status, sprint, roadmap, and changelog agree | Pending | Review their final release-state changes together in the release PR. |
| Architecture and ADR index agree | Pass | Phase 0 selected no implementation technology or product architecture requiring a numbered ADR. |

## Security and lifecycle evidence

| Requirement | Status | Evidence or required action |
| --- | --- | --- |
| Private vulnerability reporting is usable | Pass | GitHub API read-back on 2026-07-30 returned `enabled: true`; `SECURITY.md` owns the route. |
| `main` protection matches policy | Pass | GitHub API read-back verifies strict `documentation-quality`, pull-request and conversation requirements, blocked force pushes/deletion, zero approvals, and administrator bypass. |
| Known security gaps are accurate | Pending | Recheck GitHub and repository state immediately before release. |
| Supported-version impact is explicit | Pass | No Project Jebediah application version is supported by this foundation release. |
| Compatibility impact is explicit | Pass | Initial documentation release; no runtime interface, schema, data, or deployment compatibility exists. |
| Migration is defined | Not applicable | There is no prior release, persisted application state, or runtime schema to migrate. |
| Deployment is defined | Not applicable | The release publishes Git history, an annotated tag, and GitHub notes; it deploys no service or infrastructure. |
| Rollback or withdrawal is understood | Pass | Do not rewrite the tag; correct with a reviewed later version or mark the GitHub release withdrawn with rationale. |
| Recovery impact is understood | Pass | The release contains Git-backed engineering memory and no unique runtime state. |

## Changelog and release artifacts

| Requirement | Status | Evidence or required action |
| --- | --- | --- |
| `Unreleased` entries are finalized under `0.1.0` | Pending | Move the full Genesis history under `## [0.1.0] - YYYY-MM-DD` in the release PR. |
| A fresh `Unreleased` section is deliberate | Pending | Add only the heading needed for later maintained entries; do not add empty categories. |
| Release notes describe notable outcomes | Pending | Finalize [Release Notes](RELEASE_NOTES.md) after audit corrections settle. |
| Release notes state limitations | Pass | The draft identifies no application, deployment, verified home-lab inventory, supported software, or approved license. |
| Release artifact provenance is explicit | Pending | Record the final commit, annotated tag, tagger, date, and GitHub release URL. |
| Release notes disclose no sensitive details | Pending | Review the final public text against `SECURITY.md`. |

## Publication sequence

Perform these steps in order. Stop if any read-back differs from intended
state.

1. Merge the approved audit checkpoint.
2. Create a release branch from synchronized `main`.
3. Finalize changelog, status, sprint, roadmap, release notes, and this
   checklist.
4. Run all required local checks.
5. Open the release pull request and wait for the required GitHub check.
6. Give the Chief Architect the exact release artifacts and candidate commit.
7. Obtain explicit maintainer authorization for the tag and GitHub release.
8. Squash-merge the approved release pull request.
9. Synchronize local `main`; verify a clean tree and the exact merge commit.
10. Confirm `documentation-quality` succeeds on that merged commit.
11. Create annotated tag `v0.1.0` at that exact commit.
12. Push the tag without rewriting it.
13. Create the GitHub release using the reviewed release notes.
14. Verify the public tag, commit, notes, links, and foundation-only boundary.
15. Record final tag, release URL, and verification outcome in this checklist
    through the next appropriate reviewed change if they are not already
    durable in GitHub.

## Final authorization

The release remains unauthorized until every required row is `Pass` or
justifiably `Not applicable`, the Chief Architect approves the exact
foundation, and the maintainer authorizes the public tag and GitHub release.
