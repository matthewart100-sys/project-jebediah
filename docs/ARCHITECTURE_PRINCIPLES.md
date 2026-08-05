# Architecture Principles

**Status:** Active

## Purpose

These principles govern architectural decisions for Project Jebediah. They
translate the [Mission and Manifesto](MISSION_AND_MANIFESTO.md) into durable
technical constraints without choosing an application language, framework,
protocol, schema, or deployment design.

The [current architecture](ARCHITECTURE.md) describes the approved conceptual
system. Architecture Decision Records (ADRs) explain lasting choices made
within these principles.

## Evidence basis

### Verified facts

- GitHub `main` is the authoritative project record.
- The repository contains engineering-foundation documentation, a Python
  Collector package, and a semantic memory-service implementation candidate.
- Repository implementation does not prove deployment or operational state.
- ADR 0011 is a Proposed System decision for a Knowledge Vault authority
  boundary. Proposal presence does not prove acceptance, implementation,
  deployment, or external information authorization.

### Reported facts

Bootstrap materials report a local environment involving a Dell PowerEdge
R420, Proxmox, an Ubuntu virtual machine, Docker, n8n, Qdrant, and Ollama.
These reports inform questions but do not prove current deployment state or
make any product mandatory.

### Working assumptions

- Project Jebediah will remain local-first.
- The six approved conceptual layers remain useful until evidence supports a
  reviewed change.
- Named future subsystems will receive narrower responsibilities during their
  roadmap phases.

### Open questions

- Which reported infrastructure is running and supportable?
- Which information will be authoritative, cached, derived, or temporary?
- What responsibilities and guarantees will JCS own?
- Which information domains, producers, consumers, and component relationships
  could a future Knowledge Vault receive after ADR 0011 review?
- Which trust boundaries and data classifications will future use cases
  require?

These questions block dependent design where their answers would change a
boundary or risk decision.

## Principles

### 1. Local-first means controlled authority

Core project memory, configuration, data authority, and recovery paths must
remain under deliberate project control. External tools may be used when their
role, failure behavior, data exposure, and replacement path are understood.
An external conversation or hosted service must not be the only place required
to understand or recover the platform.

### 2. Documentation and decisions precede implementation

A component needs a documented purpose, boundary, owner, inputs, outputs,
failure expectations, and data responsibilities before dependent
implementation begins. An ADR is required when the decision meets the
triggers in the [ADR process](adr/README.md).

Unknowns are documented as unknowns. Plausible implementation detail is not a
substitute for evidence.

### 3. Responsibilities create boundaries

Modules, services, and processes exist to own coherent responsibilities.
Deployment convenience, directory symmetry, or a preferred tool is not enough
to justify a boundary. A boundary must identify its consumers, state,
lifecycle, failure isolation, and operational owner.

Do not split a responsibility across services without a demonstrated reason,
and do not combine responsibilities whose authority, security, or lifecycle
must differ.

### 4. Interfaces are explicit and minimal

Cross-boundary interactions must define meaning, ownership, validation,
failure behavior, compatibility, and observability before implementation.
Expose only what consumers require. Internal storage or library structures do
not become stable contracts accidentally.

The [Engineering Standards](ENGINEERING_STANDARDS.md) own detailed interface
quality requirements.

### 5. Information has authority and provenance

Every important state item must have one authoritative owner. Cached, derived,
and temporary representations remain distinguishable from authoritative
information. Provenance, freshness, and uncertainty must remain visible when
later decisions depend on them.

The detailed categories and responsibilities belong to
[Data Ownership](DATA_OWNERSHIP.md); component design must map concrete
information without weakening that policy.

Proposed
[ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md) applies
this principle to the Knowledge Vault: canonical project records and original
sources retain their scoped authority, while Vault content remains derived.
That proposal does not become binding or implementation-ready until accepted
and merged.

### 6. Deterministic control surrounds probabilistic behavior

Use deterministic processing, validation, policy, and state transitions where
the problem permits it. Probabilistic model behavior must operate inside
explicit input, output, permission, evaluation, timeout, and failure
boundaries. Model output is evidence to validate, not automatic authority.

### 7. Recoverability is designed, not inferred

Every durable capability must eventually identify how its configuration,
state, and dependencies can be reconstructed, backed up, restored, migrated,
and rolled back. A component that works only while its current machine or
operator memory survives is incomplete.

### 8. Observability answers owned questions

Health, important transitions, dependency failures, degraded behavior, and
recovery must be visible to an owner who can act. Logs, metrics, and traces
must have a purpose and retention boundary. Observability must not expose
secrets, personal data, prompts, or sensitive topology.

### 9. Trust boundaries are explicit

External input, model output, user actions, administrative control, secrets,
and cross-process communication are untrusted until validated for their
context. Least privilege, data minimization, and safe failure apply at every
trust and ownership boundary.

### 10. Simplicity precedes distribution and optimization

Prefer the smallest architecture that satisfies approved responsibilities and
failure requirements. New services, queues, caches, concurrency, and
distributed coordination require evidence that their benefits outweigh new
operational and consistency costs.

### 11. Replaceability follows owned contracts

A component is replaceable when consumers depend on an owned interface and
documented behavior rather than its internals. Replaceability does not require
premature abstraction. Introduce an adapter or portability layer only when a
real boundary, risk, or second implementation justifies it.

### 12. Architecture evolves through evidence

Measurements, incidents, validated constraints, and approved product needs may
change the architecture. Update current architecture and add or supersede the
appropriate ADR in the same reviewed change. Historic decisions remain
traceable; current documentation must never stay knowingly stale.

## Applying the principles

Architecture proposals must state:

- The responsibility or risk being addressed
- Evidence and assumptions
- Affected boundaries, owners, and consumers
- Alternatives, including retaining the current design
- Data, security, recovery, operations, and test consequences
- The applicable ADR decision level
- How the proposal preserves or intentionally changes these principles

Principles can conflict in a specific case. The proposal must name the
tradeoff rather than claiming every principle is maximized.

## Non-goals

These principles do not:

- Confirm the reported infrastructure
- Assign responsibilities to JCS or another future subsystem
- Accept ADR 0011 or authorize a Knowledge Vault implementation, external
  information use, VBA demonstration readiness, or a live organizational pilot
- Approve a language, framework, protocol, schema, database, model, or service
- Require microservices, containers, cloud services, or a particular topology
- Replace data ownership, security, testing, operations, or release policy

## Maintenance

A change to these principles is a Foundational decision and requires a new
accepted ADR plus Chief Architect review. Editorial clarification that does
not change meaning may use the normal documentation workflow.
