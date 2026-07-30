# Definition of Done

## Purpose

The Definition of Done provides one consistent finish line for Project
Jebediah. "Code written," "document drafted," or "works on my machine" is not
enough.

A requirement may be marked not applicable only with a clear reason in the
pull request.

## Universal requirements

A change is done when:

- Its stated acceptance criteria are met.
- The final diff contains only intended work.
- Canonical documentation reflects the resulting reality.
- Tests and validation appropriate to the change pass.
- `CHANGELOG.md` is updated or explicitly evaluated as not applicable.
- Local links and references are valid.
- No secrets, credentials, personal data, or private infrastructure details
  are exposed.
- Known facts, reported facts, assumptions, and open questions are labeled
  when relevant.
- ADR impact has been assessed and a required ADR is accepted.
- Required human and Chief Architect reviews have explicit decisions.
- Review comments are resolved or deliberately deferred with ownership.
- The branch is safe to merge and the repository remains understandable.
- The pull request explains impact, validation, and remaining risk.

## Documentation changes

Documentation work is done when:

- The document has a single, clear responsibility.
- Content is substantive and actionable rather than a placeholder.
- Statements are consistent with higher-authority documents.
- Duplicate policy text is replaced with links to the canonical owner.
- Headings and navigation make the content discoverable.
- Examples do not expose sensitive information.
- Dates, status, and evidence labels are accurate.
- Markdown structure, formatting, and links pass available checks.

## Architecture and design changes

Architecture work is done when:

- Context and problem boundaries are explicit.
- Verified facts, reported facts, assumptions, and open questions are
  separated.
- Design intent and non-goals are preserved.
- Alternatives and consequences are documented.
- The ADR decision level is correct when an ADR is required.
- Data ownership, security, operations, recovery, and observability impacts are
  considered.
- The current architecture is updated with the decision.
- The Chief Architect reviews the actual artifacts and records a formal
  decision.
- No implementation detail is presented as approved without evidence.

## Code changes

Code work is done when:

- The implementation follows approved architecture and standards.
- Behavior is readable, modular, and deterministic where practical.
- Error and failure behavior is explicit.
- Configuration is not hidden in code.
- Unit and integration tests cover the approved behavior and important
  failures.
- Existing relevant tests continue to pass.
- Logging and observability are proportionate and do not leak sensitive data.
- Dependencies are necessary, reviewed, and pinned according to repository
  policy.
- Documentation and examples reflect the code.

No numeric coverage threshold applies until the testing strategy approves one.
The absence of a threshold does not excuse missing tests.

## Infrastructure, workflow, and operations changes

Operational work is done when:

- Desired state is version controlled.
- Secrets are supplied outside the repository.
- Validation or dry-run behavior is documented.
- Deployment, rollback, and recovery paths are understood.
- Health, logs, metrics, and failure visibility are addressed.
- Backup and restore impact is considered.
- Changes are safe to repeat or explicitly guarded when not idempotent.
- Runbooks and project status are updated.

## Security-sensitive changes

Security-sensitive work is done when:

- Assets, trust boundaries, threats, and mitigations are documented.
- Least privilege and data minimization are applied.
- Sensitive values are not present in commits, logs, fixtures, or examples.
- Dependency and supply-chain impact is reviewed.
- Failure defaults are safe.
- Residual risk and follow-up ownership are recorded.
- Private vulnerability details use an appropriate non-public reporting path.

## Merge decision

The pull-request reviewer confirms the applicable requirements. If a necessary
requirement cannot be met:

1. Keep the pull request open, or
2. Record an explicit, owned exception with impact and resolution date.

An exception must not silently redefine "done."
