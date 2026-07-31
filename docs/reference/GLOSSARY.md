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

The project role responsible for protecting design intent and providing the
required formal review of architecture-significant plans and artifacts. The
role does not replace the maintainer's final authority or reviewed GitHub
evidence.

### Lead Engineer

The project role responsible for evidence-based implementation, validation,
repository quality, and review handoff within approved scope.

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
conflict. The detailed categories will be defined in `docs/DATA_OWNERSHIP.md`.

### Cached information

A replaceable copy of authoritative information kept for access or
performance. Its owner and freshness rules remain explicit.

### Derived information

Information produced from other information by a recorded transformation.
Its provenance and recomputation behavior remain explicit.

### Temporary information

Information created for bounded processing and not intended to become durable
authority. Its retention and cleanup behavior remain explicit.

## Named future capabilities

### JCS

A preserved name for the foundational subsystem that Phase 1 must define and
specify before implementation or collector dependency. Its expansion,
responsibilities, interfaces, and data authority are unresolved.

### Collector Engine

A named future capability for controlled ingestion from approved sources.
Sources, contracts, lifecycle, and implementation remain unapproved.

### Knowledge Graph

A named future capability for representing traceable entities and
relationships. Its model, storage, identity rules, and relationship to Qdrant
remain unapproved.

### Digital Twin

A named future concept for a bounded representation of relevant system or
project state. The planned position paper will define its subject, exclusions,
and relationship to other capabilities before implementation.

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

A vector database reported in the bootstrap environment. It is not yet
assigned as the authoritative implementation of a knowledge component.

### Ollama

A local model-serving product reported in the bootstrap environment. Its
current operation, supported models, and future Reasoning Engine role are not
verified.

## Maintenance

Add a term when multiple documents or contributors need one stable meaning.
Do not use the glossary to introduce a decision. A changed term that alters
architecture must update the relevant architecture and ADR in the same pull
request.
