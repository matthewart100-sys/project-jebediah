# Release Process

**Status:** Active

## Purpose

This process defines how Project Jebediah turns reviewed `main` into an
identifiable, reproducible, supportable release. A release is a durable project
statement about scope, evidence, compatibility, and recovery—not merely a Git
tag.

## Current state

- `v0.1.0` is the published Project Genesis engineering-foundation release.
- Project Jebediah software and Docker deployment candidates exist in the
  repository, but no reviewed capability release or supported deployment has
  been published.
- `CHANGELOG.md` contains the `0.1.0` history and a new `Unreleased` section.
- Release automation, signing, artifact storage, software bill of materials,
  and deployment tooling are not selected.

Project visibility and the foundation release do not imply supported software.

## Versioning

Project Jebediah uses Semantic Versioning with a `v`-prefixed Git tag:
`vMAJOR.MINOR.PATCH`.

Before `1.0.0`:

- `MINOR` may introduce or change developing contracts and capabilities.
- `PATCH` contains compatible corrections, documentation fixes, and low-risk
  maintenance within the current minor line.
- Breaking changes are permitted only with explicit changelog, migration,
  compatibility, and rollback treatment.

`1.0.0` will require an explicit decision that public contracts and support
expectations are mature. Do not use build metadata or prerelease identifiers
without a current release need.

## Release ownership

Every release identifies:

- Release owner
- Scope and target version
- Included pull requests or commit range
- Validation owner and evidence
- Security review status
- Artifact owner and provenance
- Deployment owner when deployment is included
- Rollback or withdrawal authority
- Supported-version impact

One maintainer may hold several roles, but each responsibility remains visible.

## Release types

### Foundation or documentation release

Publishes reviewed governance, architecture, or specifications without
claiming application behavior. `v0.1.0` is the published Project Genesis
foundation release.

### Capability release

Introduces an approved user, developer, or operational capability and its
contracts, tests, security, and operations support.

### Maintenance release

Corrects compatible defects, documentation, dependencies, or operational
behavior inside an existing supported line.

### Security release

Addresses a vulnerability through coordinated private handling and sanitized
public notes. Disclosure detail follows `SECURITY.md`.

Release type does not weaken readiness gates.

## Release readiness

A release candidate must:

- Originate from reviewed `main`.
- Have an agreed version and bounded scope.
- Satisfy the [Definition of Done](DEFINITION_OF_DONE.md).
- Pass required repository, test, security, integration, recovery, and
  documentation checks.
- Have no unresolved blocking review or known critical defect.
- Include required ADRs and current architecture updates.
- Finalize the relevant `CHANGELOG.md` entries.
- Identify supported-version and compatibility impact.
- Identify artifacts, configuration, migration, deployment, and rollback.
- Confirm secrets and private operational data are absent.
- Receive required maintainer and Chief Architect decisions.

An exception records impact, owner, compensating control, and resolution. A
deadline alone does not justify an unsafe release.

### Reader-centered release validation

A foundation release, major documentation release, or significant lifecycle
transition must include proportionate clean-room validation. Give a fresh
reader the canonical entry point without relying on the author's explanation,
conversation history, or unpromoted bootstrap material. Test whether the
reader can reconstruct the release's purpose, current reality, authority,
boundaries, operating process, and next gate.

Record the exact material supplied, questions, wrong inferences, navigation
failures, corrections, and material test limitations. Repeated friction is
evidence for improving canonical documentation. A routine correction or
low-risk patch does not require a full clean-room exercise unless its scope or
reader impact makes one necessary.

## Version selection

1. Identify the last release and full reviewed commit range.
2. Classify externally meaningful changes and compatibility.
3. Select the smallest version increment that describes the most significant
   included change.
4. Confirm version references in changelog, documentation, artifacts, and
   supported-version policy.
5. Record the decision in the release pull request.

The absence of application code does not prevent a foundation version, but the
release notes must state its documentation-only scope clearly.

## Changelog finalization

Before tagging:

1. Move included `Unreleased` entries under
   `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD`.
2. Keep categories that contain real changes, such as `Added`, `Changed`,
   `Deprecated`, `Removed`, `Fixed`, and `Security`.
3. Describe user, developer, architecture, security, or operational impact.
4. Link the version to the relevant Git comparison after a prior tag exists.
5. Leave a new empty `Unreleased` section only when its maintained structure is
   useful; do not add empty category headings.

Security notes disclose only coordinated safe detail.

## Release pull request

The release pull request contains:

- Proposed version and release type
- Included commit range and notable pull requests
- Final changelog and release-note draft
- Compatibility and migration impact
- Validation commands, environments, and results
- Security review and known vulnerabilities
- Artifact inventory and provenance
- Deployment and post-deployment plan when applicable
- Rollback, forward-recovery, or withdrawal plan
- Known limitations and residual risk
- Required approval decisions

The pull request changes versioned files and release documentation only. Do not
hide unrelated features in a release-preparation change.

## Artifacts and provenance

When release artifacts exist:

- Build from the reviewed release commit in a controlled environment.
- Record source commit, toolchain, dependency lock state, and build procedure.
- Produce immutable uniquely versioned artifacts.
- Generate checksums and signatures when an approved mechanism exists.
- Produce a software bill of materials when dependencies exist and tooling is
  approved.
- Scan artifacts and dependencies proportionate to risk.
- Store artifacts in an approved location with retention and access ownership.
- Verify that artifacts contain no secrets, private data, debug state, or
  unintended files.

Do not rebuild a published version under the same identifier. Correct it with a
new version.

## Tagging and GitHub release

After the release pull request is merged:

1. Synchronize and verify local `main`.
2. Confirm the exact release commit and clean working tree.
3. Rerun required release checks that depend on the merged state.
4. Create an annotated `vMAJOR.MINOR.PATCH` tag at that exact commit.
5. Push the tag without rewriting it.
6. Create the GitHub release from the tag with approved release notes.
7. Attach or link only verified artifacts.
8. Verify the tag, notes, links, and artifacts from the public reader's view.

Release tags are immutable. If a tag targets the wrong commit or contains
unsafe material, stop distribution, document the incident, and use an
explicitly reviewed correction; never move a published tag silently.

## Deployment

Release and deployment are separate decisions. A release may exist without
deployment, and a deployment identifies the exact release it uses.

Before deployment:

- Verify environment, access, capacity, dependencies, configuration, and
  secrets.
- Confirm data migration, compatibility, backup, rollback, and recovery.
- Define success, abort, and post-deployment verification.
- Communicate impact and owner.

Follow the [Operations Philosophy](OPERATIONS_PHILOSOPHY.md). Record the
deployed version and outcome in an approved operational system without
publishing sensitive topology.

## Post-release verification

Verify:

- Release tag and source commit
- Artifact provenance and retrieval
- Documentation and changelog links
- Critical behavior and contracts
- Health and degraded-state signals
- Data integrity and migration
- Security controls and secret handling
- Backup, rollback, or recovery readiness
- Supported-version documentation

Record unexpected results and stop further promotion when authority, integrity,
or recovery is uncertain.

## Rollback, forward recovery, and withdrawal

- **Rollback** returns behavior to a prior compatible release.
- **Forward recovery** corrects the current state with a new change when
  rollback is unsafe or incompatible.
- **Withdrawal** stops recommending or distributing a release.

The plan must consider schemas, authoritative data, workflow side effects,
credentials, configuration, and consumers. A Git checkout alone is not a
complete rollback.

A withdrawn or faulty release remains in history with a clear warning; do not
erase evidence silently.

## Security releases

Use the private vulnerability process in `SECURITY.md`:

- Limit sensitive discussion and access.
- Prepare the correction and regression evidence privately where necessary.
- Coordinate affected versions, release timing, and disclosure.
- Rotate exposed credentials or authority.
- Publish sanitized impact, upgrade, and mitigation guidance.
- Verify remediation after release.

Security urgency may compress scheduling but not provenance, testing, rollback,
or traceability.

## Hotfixes

Follow the emergency Git workflow:

1. Branch from the affected supported release or current `main` as appropriate.
2. Make the smallest safe correction.
3. Add regression and security evidence.
4. Review compatibility, deployment, and rollback.
5. Merge through a pull request.
6. Release a new patch version.
7. Reconcile any parallel development and record follow-up work.

Never replace an existing release artifact or move its tag.

## Deprecation and support

A deprecation identifies:

- Affected contract, component, version, and consumers
- Reason and replacement
- Migration procedure and verification
- Warning and removal timeline based on real consumer needs
- Data, security, and operational impact
- Owner

`SECURITY.md` records supported versions once releases exist. End of support
removes maintenance promises, credentials, dependencies, artifacts, and data
according to approved policy.

## Phase 0 `v0.1.0` gate

The Project Genesis release may proceed only after:

- Milestones 0 through 7 are complete.
- Every required foundation topic maps to substantive documentation.
- Automated documentation and repository checks pass.
- A clean-room human or AI can orient from GitHub alone.
- Status, sprint, roadmap, changelog, architecture, and ADR index agree.
- Security reporting and known Phase 0 gaps are accurate.
- The Chief Architect approves the full foundation audit.
- The maintainer authorizes the tag and GitHub release.

The release notes must state that `v0.1.0` is an engineering-foundation release
and does not contain a Project Jebediah application.

## Release record

For each release, preserve:

- Version, date, and release type
- Tag and commit
- Release owner and approvals
- Changelog and notes
- Validation evidence
- Artifact inventory and provenance
- Compatibility, migration, and deployment status
- Known limitations and supported-version impact
- Rollback, withdrawal, incident, or follow-up links

The GitHub release and repository documents are durable memory; conversational
coordination is not.

## Maintenance

Update this process when release tooling, artifact policy, support commitments,
or deployment reality changes. Material changes to versioning, artifact trust,
or support policy assess the [ADR Process](adr/README.md).
