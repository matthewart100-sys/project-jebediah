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
`5f1b58767b54aed797d1ec6a2fafa084a00d6de7`. Sprint 006 Proposal v2 is a
Proposed bounded Phase 2 memory-client validation for governed retrieval,
deterministic context assembly, and evidence-grounded generation. It does not
activate or implement Phase 6. Implementation and deployment remain
unauthorized.

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
