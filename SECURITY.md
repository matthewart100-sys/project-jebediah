# Security Policy

**Status:** Active Phase 0 policy

**Last verified:** 2026-07-30

## Purpose

Security is a design, implementation, operations, and recovery responsibility
for Project Jebediah. This policy defines safe vulnerability reporting,
public-repository boundaries, core controls, review expectations, and the
current limitations of a project that has not implemented software yet.

## Current maturity

- The repository is public.
- It contains engineering-foundation documentation and no Project Jebediah
  application or infrastructure implementation.
- No supported software release exists.
- GitHub private vulnerability reporting was verified as disabled through the
  GitHub API on 2026-07-30.
- No canonical public security email or other private reporting address has
  been approved.
- Reported home-lab infrastructure has not received a repository-backed
  security audit.

These limitations are explicit constraints, not permission to disclose
sensitive information.

## Reporting a vulnerability

Do not open a public issue containing vulnerability details, credentials,
private addresses, personal data, exploit steps, logs, or sensitive topology.

Use this order:

1. Contact the maintainer through a private channel already established with
   you.
2. If no private channel exists, open a minimal GitHub issue titled
   `Private security contact requested`.
3. Include only that you need a private security channel and a general affected
   project area. Do not include technical detail or evidence.
4. Wait for the maintainer to establish a private route before sharing the
   report.

Milestone 6 must enable and verify GitHub private vulnerability reporting or
record an approved equivalent, then update this section.

### What to include privately

- Affected artifact, version, branch, or environment
- Impact and realistic attack conditions
- Reproduction steps or proof of concept
- Whether sensitive data or credentials may be exposed
- Known mitigations or workarounds
- Contact preference for coordinated follow-up

Use sanitized evidence and the minimum data necessary.

### What to expect

The maintainer will acknowledge through the private channel, assess scope and
severity, coordinate evidence and remediation, and agree on disclosure.
Project Jebediah does not publish response-time promises before an owned
security-response process and supported release exist.

## Supported versions

No Project Jebediah software version is currently supported because no
application has been released. The current reviewed `main` branch is the
supported source for project documentation.

The release process will add a maintained version table when software or
deployable artifacts exist. Do not infer support from a branch, tag, reported
service, or public repository visibility.

## Security principles

### Default to least privilege

People, agents, components, workflows, models, and integrations receive only
the access required for an approved responsibility and duration.

### Treat boundaries as untrusted

Validate external content, model output, user input, source data, files,
network responses, workflow payloads, templates, commands, queries, and tool
results at their trust and ownership boundaries.

### Minimize data and authority

Collect, retain, replicate, expose, and process only what an approved purpose
requires. Information authority does not grant action authority.

### Fail safely and visibly

Uncertain authorization, invalid input, missing security configuration, and
failed validation default to denial. Failures remain observable without
leaking protected detail.

### Design for compromise and recovery

Assume credentials, dependencies, hosts, data stores, models, or integrations
can fail or be compromised. Bound impact, preserve audit evidence safely,
rotate authority, restore trusted state, and verify recovery.

### Keep security decisions durable

Threats, controls, residual risk, exceptions, and incident follow-up belong in
reviewed repository artifacts or an approved private system with a safe
repository conclusion. Conversation memory is not a security control.

## Public repository boundary

Never commit or paste into public review artifacts:

- Passwords, API keys, tokens, private keys, session values, or recovery codes
- Personal identifiers or private communications
- Private IP addresses, hostnames, firewall rules, or exploit-ready topology
- Raw logs, prompts, model context, database contents, vector-store contents,
  backups, or workflow credentials
- Sensitive vulnerability details before coordinated disclosure
- Real secret examples, even if believed expired

Use unmistakably fake examples. A discovered secret is treated as compromised:
stop exposure, notify the maintainer privately, rotate or revoke it, assess
use, and remove it from current and historical distribution as appropriate.
Deleting only the current line is insufficient.

## Initial threat areas

This is not a complete threat model. Future architecture and components must
refine at least:

- Compromise of local administrative access
- Credential theft or excessive service privileges
- Malicious or malformed source content
- Prompt injection and unsafe model-directed tool use
- Command, query, template, path, and workflow injection
- Unauthorized data collection, retention, inference, or disclosure
- Dependency, container, model, and artifact supply-chain compromise
- Stale, poisoned, duplicated, or conflicting information
- Unsafe automation, replay, retry, and partial action
- Public disclosure of home-lab topology or operational evidence
- Backup theft, untrusted restoration, and recovery failure
- Denial of service or resource exhaustion on constrained local hardware

Threat modeling begins before a component receives data, authority, or an
external interface.

## Identity, authentication, and authorization

- Every security-relevant actor has an identifiable principal.
- Shared administrative credentials are avoided.
- Human, service, automation, and AI-agent identities remain distinguishable.
- Authentication mechanisms and credential lifetimes match consequence.
- Authorization is checked at the action and data boundary, not inferred from
  network location.
- Sensitive and irreversible actions require human approval unless an
  accepted ADR defines a narrower safe automated boundary.
- Permission changes, denials, and privileged actions produce safe audit
  evidence.
- Access removal is part of offboarding, component retirement, and incident
  response.

No authentication technology is approved during Phase 0.

## Secrets and configuration

- Secrets use an approved external secret mechanism once implementation
  begins.
- Secret values never use source control, ordinary logs, issue text, test
  fixtures, model prompts, or workflow exports as storage.
- Configuration fails closed when a required secret or security control is
  missing.
- Runtime inspection may show that a secret is configured but never reveal its
  value.
- Rotation, revocation, recovery, and owner are documented.
- Local development secrets are separate from operational credentials.
- Examples and defaults are non-sensitive and safe.

## Data and privacy

Apply [Data Ownership](docs/DATA_OWNERSHIP.md):

- Identify information owner, component owner, producers, consumers, and
  custodian.
- Record provenance, classification, freshness, retention, deletion, and
  recovery.
- Minimize personal and sensitive information.
- Propagate deletion and access restrictions to caches, derivatives,
  embeddings, indexes, prompts, exports, logs, and backups.
- Unknown classification defaults to no collection or use.
- Do not make a derived representation authoritative without an approved
  decision.

A future classification model and privacy requirements must be based on real
use cases and applicable obligations.

## AI and automation security

- Model output and retrieved content are untrusted data.
- Deterministic validation and policy surround probabilistic behavior.
- Tool names, arguments, targets, permissions, and side effects are explicit.
- Prompt content follows source classification and retention.
- External content cannot grant project authority or change instructions.
- Sensitive tool use requires allowlisted scope and approval where practical.
- Automation is idempotent where possible and records partial success.
- A Digital Twin, model, or authoritative fact does not automatically
  authorize action.
- Evals include unsafe requests, injection, ambiguous authority, missing
  context, and escalation.

## Dependencies and supply chain

Before adding a dependency, container image, action, model, plugin, or external
service:

- Identify the exact capability and consumer.
- Review publisher and artifact provenance.
- Review maintenance, security history, license, and transitive impact.
- Pin or constrain versions according to ecosystem and repository policy.
- Verify integrity or signatures when supported.
- Minimize execution permissions and network access.
- Define update, vulnerability, rollback, and removal ownership.
- Isolate project-critical behavior behind tested boundaries.

GitHub Actions must use full immutable commit pins when introduced.

## Secure engineering lifecycle

### Plan

Identify assets, actors, trust boundaries, abuse cases, data categories,
privileges, safe failure, recovery, tests, and ADR impact.

### Design

Apply least privilege, minimal interfaces, explicit validation, defense in
depth, secure defaults, and owned residual risk. Architecture-significant
security choices use the [ADR Process](docs/adr/README.md).

### Implement

Avoid unsafe parsing, command construction, secret exposure, insecure defaults,
unbounded resource use, and ambiguous authorization. Review code and
configuration at the actual boundary.

### Validate

Use the [Testing Philosophy](docs/TESTING_PHILOSOPHY.md), including denial,
bypass, injection, redaction, abuse, dependency, and recovery evidence
appropriate to risk.

### Operate

Patch owned dependencies, monitor actionable security signals, control
administrative access, protect backups, rotate secrets, and rehearse recovery.

### Retire

Remove access, credentials, data, routes, dependencies, artifacts, and
documentation deliberately. Preserve only safe required history.

## Vulnerability handling

1. Establish a private channel and protect evidence.
2. Triage affected assets, versions, data, privileges, and exploitation
   conditions.
3. Contain immediate risk without destroying evidence.
4. Rotate or revoke potentially compromised authority.
5. Develop the smallest safe correction and rollback.
6. Add regression and security validation.
7. Review through the normal pull-request process using sanitized content.
8. Release or deploy the correction through the approved process.
9. Verify remediation and monitor recurrence.
10. Coordinate disclosure and record owned follow-up work.

An emergency does not eliminate traceability. Sensitive details may remain in
an approved private record while GitHub stores the safe decision and outcome.

## Incident response expectations

A future operations policy will define the full incident lifecycle. Security
incidents at minimum require:

- Named coordinator and private communication path
- Timeline using exact timestamps
- Scope, affected authority, and data assessment
- Containment and evidence-preservation decisions
- Recovery from a trusted state
- Credential and access review
- User or stakeholder notification decision
- Root cause and contributing conditions
- Tested corrective actions with owners
- Sanitized repository updates when architecture or policy changes

## Security review gates

Chief Architect and security-focused review are required for lasting changes
to:

- Trust boundaries
- Identity or authorization model
- Major data authority or classification
- External exposure or deployment topology
- Automated sensitive action
- Secret-management strategy
- Core dependency or model execution boundary
- Material residual risk or standards exception

Use the appropriate Foundational, System, or Implementation ADR level.

## Known Phase 0 gaps

- Private vulnerability reporting is disabled.
- No private reporting address is canonical.
- No concrete data-classification inventory exists.
- No application threat model exists.
- No dependency, container, model, or infrastructure inventory is verified.
- No security automation or branch protection is configured.
- No supported software release exists.

These gaps are scheduled through later Genesis and implementation milestones.
They must not be misrepresented as completed controls.

## Maintenance

Update this file when the reporting route, supported versions, threats,
controls, or project maturity changes. Security changes also evaluate
architecture, data ownership, operations, testing, release, status, and
changelog impact.
