# Project Jebediah Glossary

**Status:** Active

## Purpose

This glossary owns the current shared meaning of Project Jebediah terms.
Architecture documents own component relationships, standards own normative
policy, and ADRs own decision rationale. A glossary definition does not prove
that a capability exists or approve an implementation.

## Evidence terms

### Verified fact

A claim supported by repository state, inspected configuration, tests, or
validated system evidence.

### Reported fact

A claim provided by a trusted source but not independently verified. It
requires a resolution path before it supports implementation-sensitive
decisions.

### Working assumption

A temporary premise used for bounded progress, with an impact and a condition
that confirms or invalidates it.

### Open question

An unresolved matter whose significance and resolution gate are explicit.

### Proposal

A change under discussion or review. A proposal is not current architecture
until accepted through the required process.

### Accepted decision

A reviewed decision recorded in an accepted ADR or another canonical artifact
with appropriate authority. It remains subject to explicit supersession.

## Project and governance terms

### Project Jebediah

The local-first AI platform initiative governed by this repository. The name
refers to the whole project, not a currently implemented service.

### Project Genesis

Phase 0 of Project Jebediah. It establishes the permanent engineering
foundation before application or infrastructure implementation.

### Canonical document

The single repository artifact assigned to own a shared concept's current
meaning or policy.

### Canonical project record

A reviewed repository artifact on GitHub `main` assigned to own Project
Jebediah governance, architecture, accepted decisions, plans, current status,
standards, or maintained project evidence within a defined subject. This scoped
authority does not make the repository authoritative for external
organizational facts or live runtime state.

### Architecture Decision Record (ADR)

An immutable record of a lasting architectural choice, including its context,
alternatives, consequences, evidence, decision level, and supersession
relationships.

### Decision level

The scope of an ADR: Foundational, System, or Implementation. The
[ADR process](../adr/README.md) defines the levels and their review gates.

### Repository ownership

Responsibility for the purpose, placement, and maintenance rules of a tracked
path or artifact. It is defined by
[Repository Standards](../REPOSITORY_STANDARDS.md).

### Component ownership

Accountability for a runtime or conceptual component's purpose, interfaces,
state, lifecycle, operations, recovery, and deprecation. It is tracked in the
[Component Registry](COMPONENT_REGISTRY.md) and is distinct from repository
ownership.

### Chief Architect

The final decision-making role for strategy, architecture, scope, ADR
acceptance, sprint authorization, merge approval, and roadmap direction. The
role requires actual evidence and does not perform implementation work by
default. The
[Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
owns its authority.

### Implementation Engineer

The Codex role responsible for planning, evidence-based implementation,
validation, repository quality, controlled merge, and review handoff within
approved scope. Earlier historical documents may call this role Lead Engineer;
the Project Coordination Protocol uses Implementation Engineer.

### Work Mode

The independent architecture and quality review role. It challenges
assumptions, requires evidence, and may block implementation or merge, but it
cannot issue final architecture approval or override the Chief Architect.

### Documentation Suite

The Documentation Lead role responsible for reconciling canonical project
documentation after approved merges. It may identify gaps but cannot invent
system behavior, architecture, sprint scope, or roadmap priority.

### Jebediah Runtime

A future operational consumer of approved, merged, validated, and documented
project state. It has no current engineering authority and is not an approved
runtime component merely because the role is named.

### Revised organizational-intelligence milestone sequence

The gated recovery and capability sequence established by
[CA-2026-08-06-P3B-RECONCILIATION](../governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md):
B0 canonical recovery; B1 synthetic custody foundation; B2 isolated PDF
inspection and review; B3 lifecycle and recovery readiness; C0 identity and
service authorization; C1 governed knowledge promotion; C2 memory and Qdrant
projection; D1 evidence read model and grounded assistance; D2 authenticated
operational workspaces; and O1 deployment and exposure. The labels describe
gates, not active or pre-authorized implementation.

## Architecture terms

### Local-first

An architectural property in which the project deliberately controls its
authoritative memory, configuration, data boundaries, and recovery path.
Local-first permits reviewed external dependencies; it does not mean every
operation must be offline.

### Component

A conceptual or implemented unit with one coherent responsibility and an
owned lifecycle. A component is not necessarily a service, process, container,
package, repository, or host.

### Service

A runtime capability with an independently meaningful interface or lifecycle.
A product running in a container is not automatically an approved Project
Jebediah service.

### Interface

An owned boundary through which a consumer observes behavior, exchanges
information, or requests an action. An interface includes semantics, failure
behavior, compatibility, authority, and validation—not only syntax.

### Trust boundary

A point where information, identity, permissions, or control crosses between
contexts with different assurance or authority.

### Provenance

Information describing the origin and relevant transformation history of data
or a claim.

### Authoritative information

Information for which one approved owner is the source used to resolve
conflict. [Data Ownership](../DATA_OWNERSHIP.md) defines the category and
required responsibilities.

### Cached information

A replaceable copy of authoritative information kept for access or
performance. Its owner and freshness rules remain explicit.

### Derived information

Information produced from other information by a recorded transformation.
Its provenance and recomputation behavior remain explicit.

### Temporary information

Information created for bounded processing and not intended to become durable
authority. Its retention and cleanup behavior remain explicit.

### Derived representation

As defined by accepted
[ADR 0011](../adr/0011-knowledge-vault-authority-and-boundary-model.md), an
information artifact produced from one or more source records by a documented
transformation for a bounded knowledge use. It retains sufficient source and
transformation provenance and does not become authoritative for the underlying
source facts through review, curation, durability, validation for shape,
embedding, indexing, summarization, or retrieval.

### Quarantined candidate information

As defined by ADR 0011, untrusted, non-authoritative, non-consumable candidate
input awaiting admissibility evaluation. It remains temporary unless a separate
accepted contract assigns another category. Evaluation may establish policy
admissibility but does not verify source truth.

### Source Document Evidence candidate

A Phase 3B encrypted derived representation of one exact submitted document,
including content identity, source/provenance references, extraction method,
page locations, warnings, omissions, quality, limitations, and review state. It
is not source truth, a Knowledge Object, memory, an embedding, an index entry,
or a supported answer. Accepted ADR 0016 defines the architecture boundary but
does not authorize implementation or a real source.

### Human Review Workspace

The accepted but unimplemented Phase 3B Executive Product Shell surface design
that would present admission and Source Document Evidence candidates to one
authorized operator for append-only approval, rejection, correction,
supersession, deletion, and reset. Its approval would mean only
`approved_for_phase3c_candidate`; it would not verify facts or invoke a Phase
3C consumer. No implementation or real-document use is active.

### VBA demonstration materials

Proposed scripts, prompts, fixtures, operator guidance, and related artifacts
for a bounded demonstration. Open pull request #44 contains such artifacts, but
they are not canonical project records, validated production knowledge,
Knowledge Vault content, or evidence of pilot readiness. Evidence validation is
pending, and no live organizational pilot is authorized.

## Named future capabilities

### Knowledge Registry

An accepted metadata-only domain library foundation under
[ADR 0014](../adr/0014-knowledge-registry-domain-boundary.md). It may represent
immutable governance metadata for a derived knowledge object without storing
source or derived content, integrating with memory, selecting durable storage,
or granting source, truth, retrieval, action, or runtime authority.
`collector.knowledge.registry` is repository packaging only and does not assign
Collector Engine component authority. The bounded Phase 1 implementation is
complete on reviewed `main` and has **Implemented** repository maturity. It
provides immutable domain models, lifecycle representation, a storage-neutral
repository abstraction, and an in-memory reference implementation. The
Knowledge Vault remains **Named**. The separate Phase 2 synthetic document
inspection package is implemented and terminally closed, but it does not write
the registry. No real document ingestion, production document parsing,
organizational-information authorization, durable storage, Qdrant integration,
retrieval integration, runtime service, or deployment exists.

### Knowledge Vault

A **Named** future component boundary whose authority model is defined by
accepted
[ADR 0011](../adr/0011-knowledge-vault-authority-and-boundary-model.md) as a
derived governed knowledge repository. It is not GitHub `main`, an original
authoritative source, the Memory Service, Qdrant, a vector index, a model
context store, a Knowledge Graph, or a production deployment. The separate
metadata-only Knowledge Registry foundation is authorized, but no Knowledge
Vault component implementation or external information use is authorized.

### JCS

A preserved name for the foundational subsystem that Phase 1 must define and
specify before implementation or collector dependency. Its expansion,
responsibilities, interfaces, and data authority are unresolved.

### Collector Engine

An **Implemented** repository component for bounded text-record ingestion,
provenance, deterministic identity, and storage coordination. Accepted ADR 0013
and the terminally closed Knowledge Manager Phase 2 package add a disconnected
synthetic document-admission and inspection boundary. Real sources, production
parsers and scanners, durable quarantine, runtime integration, deployment, and
operational ownership remain unapproved. Accepted ADR 0016 defines a bounded
PDF-only architecture candidate, but current maturity and authority do not
change without a separately reviewed and authorized future milestone,
implementation, review, and merge.

### Executive Product Shell

An **Implemented** human-experience component under Accepted
[ADR 0015](../adr/0015-executive-product-shell-and-local-preview-boundary.md).
It owns presentation and navigation over immutable compiled fabricated briefing
fixtures in a loopback-only local preview. It has no source-truth, verification,
derivation, approval, action, organizational-information, service, deployment,
or operational authority. The synthetic implementation is present on canonical
`main`; it is not Operational.

### Knowledge Graph

A named future capability for representing traceable entities and
relationships. Its model, storage, identity rules, and relationship to Qdrant
remain unapproved.

### Digital Twin

A named future concept for a bounded representation of relevant system or
project state. The [Digital Twin Position](../design/DIGITAL_TWIN_POSITION.md)
defines its time-aware, provenance-rich intent, exclusions, derived-information
default, and implementation gates.

### Automation

A future capability for controlled actions and orchestration from trusted
state and explicit policy. The word does not by itself approve a workflow,
trigger, tool, or autonomous authority.

### Reasoning Engine

A named future capability for bounded reasoning over trusted knowledge and
state. Models, prompts, interfaces, tools, and deployment remain unapproved.

## Reported product names

### Proxmox

A virtualization platform reported in the bootstrap environment. Its current
installation and future architectural role are not verified.

### Docker

A container runtime reported in the bootstrap environment. Its current
installation and future use are not verified or mandated.

### n8n

A workflow automation product reported in the bootstrap environment. It is not
yet an approved implementation of Project Jebediah's Automation capability.

### Qdrant

A vector database with an implemented Memory Service adapter. Under ADR 0003,
an acknowledged point payload temporarily owns the operational record of what
the service stored while its vector remains derived. Live operation and any
future knowledge-component role remain unverified.

### Ollama

A local model-serving product with an implemented embedding adapter pinned by
ADR 0004 to `nomic-embed-text:v1.5` and its immutable manifest digest. Current
operation, installed model inventory, and any future Reasoning Engine role are
not verified.

## Maintenance

Add a term when multiple documents or contributors need one stable meaning.
Do not use the glossary to introduce a decision. A changed term that alters
architecture must update the relevant architecture and ADR in the same pull
request.
