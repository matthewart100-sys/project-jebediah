# Operations Philosophy

**Status:** Active

## Purpose

Operations keeps Project Jebediah understandable, available, safe, and
recoverable after implementation leaves a developer's workstation. This
philosophy defines technology-neutral expectations for ownership,
configuration, observability, change, backup, restore, incidents, and
continuity.

It does not claim the reported home-lab environment is verified or
production-ready.

## Current evidence and scope

### Verified facts

- A Collector package and Dockerized memory-service candidate exist in the
  repository, but no deployment evidence, operational runbook, backup job,
  monitoring rule, or supported capability release is verified.
- The repository is authoritative for approved engineering memory.
- Operations must follow current architecture, data ownership, testing, and
  security policy.

### Reported facts

Bootstrap materials report a Dell PowerEdge R420, Proxmox, an Ubuntu virtual
machine, Docker, n8n, Qdrant, and Ollama. Versions, health, capacity,
configuration, persistence, backups, network exposure, and ownership remain
unverified.

### Working assumptions

- The first deployment will be local-first and resource constrained.
- Components will fail independently and sometimes lose dependencies.
- Some future information will require durable recovery while caches and
  derivatives may be rebuilt.
- One maintainer may initially perform several operational roles.

### Open questions

| Question | Operational impact | Resolution gate |
| --- | --- | --- |
| What infrastructure is actually present and supportable? | Capacity, patching, backup, and recovery plans cannot be confirmed. | Sanitized infrastructure audit |
| Which component owns each runtime responsibility? | Alerts, changes, recovery, and escalation need accountable owners. | Component specifications |
| What availability and data-loss targets do approved use cases require? | Redundancy and recovery design depend on measured consequence. | Component service objectives |
| Which private system stores sensitive operational evidence? | Public GitHub cannot hold raw sensitive logs or topology. | Security and operations implementation decision |

## Principles

### Operate from reviewed desired state

Configuration intent, procedures, and safe automation belong in version
control. Live state is evidence, not an undocumented alternative source of
truth. Emergency changes are reconciled into GitHub after containment.

### Ownership precedes alerts

Every component, dependency, signal, backup, and runbook has an owner who can
interpret it and act. A notification without an action, threshold rationale,
or escalation path is noise.

### Degraded state is explicit

A system must distinguish healthy, degraded, unavailable, stale, and unsafe.
It must not report success while a required dependency, authoritative source,
or recovery guarantee is missing.

### Recovery is proven

Backups, replicas, retries, and rollback claims become trusted only through
repeatable validation. A successful backup command is not a successful
restore.

### Changes are bounded and reversible

Operational changes identify scope, preconditions, validation, failure
behavior, rollback or forward recovery, and affected authority. Automation is
idempotent where practical and guarded where repetition is unsafe.

### Observability protects privacy

Signals answer operational questions without exposing credentials, personal
data, prompts, private content, or exploitable topology.

### Local-first still requires dependency discipline

Local execution does not eliminate hardware, network, power, software,
capacity, or human dependencies. Each dependency has an explicit impact and
recovery expectation.

## Operational ownership

A future operational component identifies:

- Component and information owner
- Operator or custodian
- Supported environment and dependencies
- Configuration and secret owner
- Health and service objectives
- Logs, metrics, events, and alerts
- Capacity constraints
- Backup, restore, rebuild, and rollback
- Maintenance and patch responsibility
- Incident escalation and communication
- Retirement and data-removal path

One person may hold several roles, but the responsibilities remain separate.

## Environments and configuration

No fixed development, staging, or production topology is approved. Each
approved environment must nevertheless:

- Have a named purpose and owner
- Identify which data categories it may contain
- Separate secrets and access from other environments
- Use reviewed configuration intent
- Expose its version and relevant configuration safely
- Define promotion, reset, and retirement behavior
- Prevent tests from modifying live authoritative data

Configuration precedence, defaults, required values, and environment-specific
overrides are documented. Missing security-critical configuration fails
closed.

## Health model

Components define signals appropriate to their responsibility:

- **Process health:** the process or workflow can execute.
- **Readiness:** it can accept intended work safely.
- **Dependency health:** required owned boundaries are usable.
- **Data health:** authority, freshness, conflict, and processing lag meet the
  consumer's stated needs.
- **Functional health:** a bounded representative operation succeeds.
- **Recovery health:** required backups and rebuild inputs remain valid.

A single “up” signal must not hide degraded dependencies or stale data.

## Service objectives

Do not invent universal availability, latency, recovery-time, or recovery-point
numbers. A future component sets measurable objectives from user and
operational consequence, including:

- Availability or completion expectation
- Latency or processing window
- Freshness and tolerated staleness
- Error and partial-success tolerance
- Recovery time objective
- Recovery point objective
- Capacity and saturation boundary

Objectives identify the measurement, window, owner, and response when breached.

## Observability

### Logs

Record important lifecycle transitions, failures, retries, authorization
decisions, external dependency outcomes, and recovery actions. Use structured
fields when the implementation supports them. Preserve original causes and
correlation identifiers across boundaries.

### Metrics

Measure behavior tied to an owned question, such as throughput, failures,
latency, queue depth, freshness, saturation, retry rate, or restore age. A
metric without a consumer or decision is not automatically valuable.

### Traces and events

Use traces or durable events when work crosses components and diagnosis
requires causal sequence. Do not introduce observability infrastructure before
the diagnostic need exists.

### Alerts

An alert identifies:

- Condition and user or operational impact
- Measurement and threshold rationale
- Owner and delivery route
- Immediate triage and safe action
- Escalation and suppression behavior
- Link to a maintained runbook

Avoid alerts for conditions that require no action.

## Sensitive operational evidence

Public GitHub stores sanitized conclusions, policies, and procedures. Raw logs,
private hostnames, addresses, credentials, personal data, prompts, database
contents, backups, and exploit-ready topology use an approved private system.

Operational evidence records its owner, retention, integrity expectations, and
safe retrieval method without publishing the sensitive content.

## Change management

Before an operational change:

1. Define intended outcome and affected components, data, users, and
   dependencies.
2. Confirm authority and maintenance window when required.
3. Capture safe pre-change state and recovery prerequisites.
4. Validate configuration or plan output.
5. Define success, abort, rollback, and forward-recovery criteria.
6. Communicate expected impact.
7. Apply the smallest controlled change.
8. Observe health and important behavior.
9. Reconcile desired state, documentation, and changelog.

Direct live changes use the same evidence and are not allowed to become
permanent undocumented state.

## Deployment and rollback

Deployment is a controlled operational action, distinct from creating a
release.

- Deploy an identified release or reviewed commit.
- Verify artifact provenance and configuration compatibility.
- Protect secrets and authoritative data.
- Validate dependencies and migrations before irreversible steps.
- Preserve a rollback or forward-recovery path.
- Stop when health, data integrity, or authorization is uncertain.
- Perform post-deployment functional and operational verification.
- Record the deployed version and outcome safely.

Rollback must consider data and schema compatibility; returning binaries alone
may not restore a valid state.

## Backup, restore, and rebuild

Apply [Data Ownership](DATA_OWNERSHIP.md):

- Authoritative information requires owned backup and restore expectations.
- Cached information requires a verified refetch or rebuild path.
- Derived information requires reproducible inputs and transformations or an
  explicit backup reason.
- Temporary information must not contain unique durable value.

A backup plan identifies scope, frequency, retention, encryption, access,
integrity, storage-failure independence, recovery objectives, and deletion
behavior.

Restore tests:

- Run in an isolated destination
- Verify integrity and application-level meaning
- Confirm secrets and access are handled safely
- Reconcile deleted, expired, or superseded state
- Measure actual recovery time and data loss
- Record evidence, limitations, and owner

## Maintenance and upgrades

- Inventory supported components and versions.
- Review security, compatibility, migration, capacity, and rollback.
- Test against representative sanitized state.
- Back up required authority before change.
- Upgrade in bounded steps.
- Verify health, contracts, data, and critical journeys.
- Remove obsolete versions, credentials, and configuration after the
  transition is proven.

Unmaintained dependencies and unsupported platforms become explicit risks with
owners and resolution gates.

## Runbooks

A runbook is written for a real owned operational task or failure. It includes:

- Purpose, scope, prerequisites, and authority
- Safe commands or actions with expected effects
- Required evidence and sensitive-data handling
- Decision points and stop conditions
- Validation, rollback, and escalation
- Related architecture, component, and incident links
- Last exercised date and owner when maintenance depends on recency

Do not use screenshots as the only record of commands or configuration.

## Incident lifecycle

1. **Detect and validate:** confirm the signal and immediate impact.
2. **Coordinate:** name an incident lead and safe communication route.
3. **Contain:** limit harm while preserving evidence.
4. **Diagnose:** build a timestamped factual timeline and test hypotheses.
5. **Recover:** restore trusted service and data through an approved path.
6. **Verify:** confirm health, authority, security, and user-visible behavior.
7. **Communicate:** provide accurate status without exposing sensitive detail.
8. **Learn:** identify root cause, contributing conditions, and missed
   detection.
9. **Improve:** assign tested corrective actions and update canonical
   documents.

Severity and communication cadence will be defined from real service impact.
Do not create false response-time promises during Phase 0.

## Capacity and resource management

Future components measure their limiting resources, which may include CPU,
memory, storage, model memory, network, file descriptors, concurrency, queue
depth, or operator attention.

- Establish a baseline before optimization.
- Define saturation and safe shedding behavior.
- Bound untrusted or expensive workloads.
- Preserve capacity for health, recovery, and administrative action.
- Test relevant exhaustion behavior.
- Do not expose private inventory details in public evidence.

The reported R420 does not establish verified capacity.

## Continuity and disaster recovery

Identify credible loss scenarios such as host loss, storage corruption,
credential compromise, unavailable dependency, bad deployment, operator
error, or repository unavailability.

For each material scenario, define:

- Authority and data at risk
- Detection
- Recovery source and procedure
- Required access independent of the failed system
- Recovery objectives
- Validation and safe return to service
- Residual risk

GitHub-hosted engineering memory also requires a future export or recovery
strategy; platform recovery must not depend on inaccessible chat history.

## Operational readiness gate

Before a component is called operational, reviewers can answer:

- Who owns it and its dependencies?
- What version and configuration are running?
- What is healthy, degraded, stale, or unsafe?
- Which objectives are measured?
- Where are safe logs and operational evidence?
- What can fail, retry, duplicate, or partially succeed?
- How is authority protected and recovered?
- Has backup restore or rebuild been tested?
- Can deployment be stopped or reversed safely?
- Are runbooks current and exercised?
- Are access, secrets, patches, and capacity owned?
- What is the retirement path?

## Maintenance

Component specifications and runbooks refine this philosophy with real
evidence. Changes to operational boundaries, recovery strategy, or material
risk assess the [ADR Process](adr/README.md), [Security Policy](../SECURITY.md),
[Testing Philosophy](TESTING_PHILOSOPHY.md), and
[Release Process](RELEASE_PROCESS.md).
