# Project Jebediah Roadmap

## Purpose

This roadmap preserves the required development sequence and the gates between
major capabilities. It describes direction, not delivery dates or guaranteed
features.

A roadmap phase may be refined only through reviewed repository changes.
Material changes to platform intent or subsystem order require architectural
review and may require an ADR.

## Guiding sequence

**Foundation -> Documentation -> JCS definition -> Collectors -> Knowledge
Graph -> Digital Twin -> Automation -> Reasoning Engine -> Production
Platform**

Each phase must leave the repository understandable and recoverable before the
next phase depends on it.

## Phase 0: Project Genesis

**Objective:** Establish the permanent engineering foundation before software
implementation.

**Status:** Complete; `v0.1.0` published from
`978fa7f0ad855986e6bef39b373b6d9e5a9def53`

Required outcomes:

- Mission and manifesto
- Current status and documentation hierarchy
- Repository, engineering, Git, sprint, and documentation standards
- Contribution guide and Definition of Done
- AI collaboration and memory contract
- Architecture principles and current architecture
- Tiered ADR framework
- Data ownership model
- Digital Twin position paper
- Testing, security, operations, and release philosophies
- GitHub review templates and documentation quality enforcement
- Clean-room onboarding audit and `v0.1.0` foundation release

**Exit gate:** A new engineer or AI can understand and contribute using GitHub
alone, and the repository passes its documented quality checks.

## Phase 1: JCS definition

**Objective:** Define JCS before any implementation or collector dependency.

**Status:** Deferred after Milestone C1; reconsideration is evidence-gated

Required outcomes:

- Confirmed name and purpose
- Scope and explicit non-goals
- Responsibility and ownership boundaries
- Authoritative data responsibilities
- Interfaces expressed as requirements, not premature technology
- Failure, recovery, and observability expectations
- Security and privacy constraints
- Alternatives and architectural decision records
- Acceptance criteria for a future implementation

**Exit gate:** The JCS specification is approved and collectors can depend on a
stable conceptual contract.

## Phase 2: Collectors

**Objective:** Establish controlled, observable ingestion from approved
sources.

**Status:** In progress; Sprint 005 completed and merged the bounded memory
architecture consolidation through pull request #39 at
`5f1b58767b54aed797d1ec6a2fafa084a00d6de7`. The cross-phase Knowledge
Registry foundation completed at
`4ed2ac283e4df6aec30b67f7c4aa50338924c435` under accepted ADR 0014. No active
implementation sprint is authorized. Sprint 006 Proposal v2 remains Proposed in
draft pull request #43; it is not active and does not activate Phase 6.
Deployment and external information remain unauthorized.

Required outcomes:

- Source inventory and authorization
- Collector responsibilities and lifecycle
- Provenance and validation requirements
- Retry, idempotency, and failure handling
- Security, rate, and privacy constraints
- Test strategy and operational runbooks

**Entry gate:** Any JCS dependency is either governed by an approved contract
or explicitly absent under the reviewed defer outcome, and applicable data
ownership requirements are documented.

## Accepted cross-phase Knowledge Vault boundary

**Status:** Accepted in ADRs 0011 and 0014; component maturity remains
**Named**; the metadata-only Knowledge Registry library is implemented and
post-merge validated; deployment, external information, runtime consumers, and
operational capability remain unauthorized

The accepted Knowledge Vault boundary does not add, remove, or reorder a
roadmap phase. It governs the authority model for derived knowledge
representations between separately authorized source handling and future
approved consumers while:

- Reviewed GitHub `main` retains canonical project-record authority.
- Original authoritative sources retain authority for their domain facts.
- The Knowledge Vault governs only derived representations and provenance.
- Runtime systems retain only approved execution state and operational outputs.

Acceptance of the boundary does not satisfy Collector, Knowledge Graph, Digital
Twin, Automation, Reasoning Engine, or Production Platform entry or exit gates.
Each information domain, producer, consumer, interface, implementation,
deployment, and external information use remains separately gated.

Knowledge Manager 1.0 Phase 1 is a completed bounded cross-phase foundation,
not a new roadmap phase or component. It added only the accepted
`collector.knowledge.registry` metadata contract, storage-neutral repository
interface, in-memory reference adapter, and synthetic validation. The package
path is repository organization only and does not give the Collector Engine
authority over registered knowledge. The completed sprint did not implement the
Knowledge Vault component, ingestion, content storage, durable persistence,
retrieval, memory integration, or a runtime consumer.

The VBA demonstration artifacts in pull request #44 do not advance this roadmap.
Their evidence validation is pending, and no live organizational pilot is
authorized.

## Accepted organizational-intelligence foundation

**Status:** Accepted in ADRs 0012 and 0013; no sprint position, implementation,
live information use, deployment, or action authorized

The accepted architecture combines two boundaries without changing the roadmap
order:

- A quarantine-first extension of the Collector boundary for candidate PDF,
  DOCX, TXT, and Markdown submissions
- A read-only executive interface over eligible evidence-bearing read-model
  items answering what is happening, what needs attention, what Jebediah knows,
  and what should happen next

The document-admission boundary may refine Phase 2 only after source,
information-owner, security, retention, component, ADR, and sprint gates are
satisfied. The executive interface is a future human-experience consumer; it
does not bypass Knowledge Graph, Digital Twin, Automation, or Reasoning Engine
entry gates and does not activate those phases.

The Chief Architect must separately position and authorize any implementation
milestone after its exact plan receives Work Mode review. Architecture
acceptance alone does not authorize organizational information, deployment, or
a pilot.

## Phase 3: Knowledge Graph

**Objective:** Represent approved entities and relationships with traceable
provenance.

Required outcomes:

- Entity and relationship model
- Identity and deduplication rules
- Provenance and confidence semantics
- Query and update boundaries
- Recovery and migration strategy
- Relationship to Qdrant and other knowledge stores

**Entry gate:** Collector outputs and authoritative data boundaries are stable.

## Phase 4: Digital Twin

**Objective:** Build an approved representation of relevant system and project
state.

Required outcomes:

- Approved Digital Twin position and scope
- State ownership and freshness rules
- Relationship to infrastructure, services, and knowledge
- Explicit exclusions
- Failure and stale-state behavior
- Security and operational boundaries

**Entry gate:** The position paper, data ownership model, and relevant
knowledge contracts are approved.

## Phase 5: Automation

**Objective:** Perform controlled actions from trusted state and explicit
policy.

Required outcomes:

- Automation authority and approval boundaries
- Deterministic workflows where practical
- Human-in-the-loop requirements
- Idempotency, rollback, and auditability
- n8n workflow ownership and versioning
- Safety tests and operational controls

**Entry gate:** Source data, state representation, and action authority are
understood.

## Phase 6: Reasoning Engine

**Objective:** Add bounded reasoning over trusted project knowledge and state.

Required outcomes:

- Reasoning responsibilities and exclusions
- Model and tool boundaries
- Evidence and provenance requirements
- Evaluation and failure criteria
- Human escalation behavior
- Privacy, security, and cost controls

**Entry gate:** Knowledge, state, and automation boundaries are stable and
observable.

## Phase 7: Production Platform

**Objective:** Harden the complete platform for reliable long-term operation.

Required outcomes:

- Reproducible deployment
- Security review and threat-model closure
- Backup and tested restoration
- Monitoring, alerting, and incident response
- Performance and capacity validation
- Upgrade, migration, and rollback procedures
- Release governance and support expectations

**Entry gate:** All earlier subsystems meet their documented Definitions of
Done and integration acceptance criteria.

## Roadmap governance

- `CURRENT_SPRINT.md` selects near-term work from this roadmap.
- `PROJECT_STATUS.md` records what actually exists.
- ADRs record decisions that change architecture.
- The changelog records delivered outcomes.
- An item appearing here does not mean it is implemented or approved in detail.
- Unknown dates remain unknown; false precision is not project memory.
