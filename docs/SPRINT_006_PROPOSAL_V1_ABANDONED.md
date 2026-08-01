# Sprint 006 Proposal v1 Abandonment Record

**Status:** Abandoned

**Reason:** Unrecoverable proposal artifacts

**Successor:** Sprint 006 Proposal v2

**Recorded:** 2026-08-01

**Last recoverable repository baseline:**
`2e5b3bd1eb2c4ef960ba62dc3798fa975f2c3f66`

## Purpose

This record closes Sprint 006 Proposal v1 without reconstructing it. The
proposal existed outside the authoritative repository, and its exact source
artifacts, package contents, branch, and review head cannot be recovered.
Project Jebediah therefore has no reviewable chain of custody for v1.

## Recovery evidence

Repository checks found:

- no remote branch named
  `agent/sprint-006-grounded-interaction-architecture`
- no tracked Sprint 006 proposal documents or ADRs after ADR 0005
- no matching pull request or reachable proposal commit

Working-session checks found:

- no local proposal branch or matching recoverable reflog entry
- no proposal package in the supplied attachment; only revision instructions
  remained available

These facts prove absence from the inspected repository and working session.
They do not establish the exact content of the lost proposal.

## Consequences

- Proposal v1 is permanently abandoned and must not be recreated, revised,
  continued, approved, or described as a repository artifact.
- No implementation, sprint, architecture, deployment, or live-system
  authority derives from v1 or from a review that cannot resolve its exact
  artifacts.
- Every surviving independent Work Mode blocking finding is a mandatory design
  input for the successor; the findings are not a substitute for v1 and do not
  reconstruct it.
- Proposal v2 must be newly authored from the then-current reviewed `main`
  baseline and must not claim document continuity or byte-level equivalence
  with v1.
- This record does not authorize Proposal v2. Its proposal must follow the
  architecture-proposal chain-of-custody rule and the normal review workflow.

## Successor gate

When Sprint 006 Proposal v2 is authored, its first review packet must identify
the repository, base commit, remote head branch and commit, complete artifact
manifest, and compare target. Chat attachments may be convenience copies
only.

This abandonment record does not define Sprint 006 scope, architecture, ADRs,
implementation, or roadmap priority.
