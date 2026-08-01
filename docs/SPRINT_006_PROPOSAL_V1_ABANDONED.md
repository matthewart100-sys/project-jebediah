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

## Recovery evidence boundary

Recovery established the absence of a verifiable immutable review target:

- no committed Sprint 006 proposal head was found
- no recoverable Git object or immutable proposal commit was found
- no pull request or repository-backed exact review target was found
- no cryptographically verifiable artifact identity was available

Recovery did not establish the absence of every possible transient or local
proposal-shaped copy. A transient local file, working-session copy, chat
attachment, or download cannot be proven identical to the artifact reviewed by
Work Mode without an immutable artifact identity and exact review target.
Transient files therefore cannot restore chain of custody and must not be
presented as recovered Proposal v1.

The distinction is material: absence of a recoverable immutable review target
is proven within the inspected repository and working session; absence of
every possible transient copy is not claimed. Proposal v1 remains permanently
abandoned because no transient copy can satisfy exact-artifact review.

## Consequences

- Proposal v1 is permanently abandoned and must not be recreated, revised,
  continued, approved, or described as a repository artifact.
- No implementation, sprint, architecture, deployment, or live-system
  authority derives from v1 or from a review that cannot resolve its exact
  artifacts.
- The seven surviving independent Work Mode findings are preserved as
  [historical design inputs for Sprint 006 Proposal v2](reviews/SPRINT_006_PROPOSAL_V1_WORK_MODE_FINDINGS.md).
  They are mandatory successor inputs, not a substitute for v1, and do not
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
