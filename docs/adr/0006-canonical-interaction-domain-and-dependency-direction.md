# ADR 0006: Canonical Interaction Domain and Dependency Direction

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-01

**Decision owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect

## Decision summary

If accepted, `src/collector/interaction/` becomes the sole canonical
interaction domain. FastAPI remains transport and composition only, while the
interaction domain depends on a narrow read-only capability owned by
`src/collector/memory/` and never receives a store-capable memory service.

## Context

Sprint 005 established one canonical memory domain and removed the service
shadow package. Sprint 006 needs a single-turn interaction boundary that can
retrieve memories, assemble governed context, call a generation provider, and
package evidence without putting reusable behavior back into FastAPI or
granting write authority to a read-only client.

Without an explicit boundary, interaction orchestration could be placed in
`main.py`, copied into a second service tree, added to the memory domain, or
coupled to `MemoryApplicationService`, which exposes both store and context
behavior.

### Verified facts

- `src/collector/memory/` is the sole canonical memory domain under accepted
  ADR 0002.
- The service app currently contains only `main.py` and composes installed
  canonical packages.
- `MemoryApplicationService` owns store and context orchestration and is
  therefore write-capable.
- Semantic retrieval returns storage-independent `RetrievalCandidate` values.
- The repository contains no interaction package or interaction endpoint.
- Existing retrieval remains semantic-only.

### Reported facts

- Project materials report n8n as part of a local environment, but no tracked
  workflow, consumer contract, or operational integration is verified.
- A sanitized Ollama generation inventory was supplied for this proposal and
  remains subject to implementation-time identity checks.

### Working assumptions

- The memory domain can expose a query-only application capability without
  changing semantic ranking, persistence, or public memory APIs.
- The existing service image can install a future interaction package from the
  same reviewed root distribution.
- A single FastAPI process is sufficient for the bounded validation; no new
  independently deployed service is required.

### Open questions

- Final Python module names inside `collector.interaction` are implementation
  choices, provided the ownership and dependency rules remain enforceable.
- Deployment capacity and live provider health remain separate, unauthorized
  operational gates.

## Scope

This decision governs:

- canonical source ownership for interaction behavior
- dependency direction among service, interaction, and memory domains
- responsibilities retained by FastAPI
- the query-only memory capability exposed to interaction
- structural zero-write enforcement
- package installation and import-origin requirements
- n8n's permitted relationship to the interaction API

## Non-goals

- Implementing Sprint 006
- Changing memory storage, ranking, lifecycle, verification, or APIs
- Creating an agent, Reasoning Engine, orchestration system, or n8n workflow
- Deploying a new service or changing Docker or Compose
- Selecting generation identity, response semantics, context policy, or trust
  boundaries governed by ADRs 0007 through 0010

## Decision drivers

- One implementation and owner for reusable interaction behavior
- Preserve ADR 0002 dependency direction and service composition
- Structural prevention of memory writes
- No duplicated retrieval implementation
- Testable separation between HTTP and domain behavior
- Replaceable provider and retrieval ports without speculative services
- Normal root-package installation on Python 3.12

## Considered alternatives

### Put interaction orchestration in FastAPI `main.py`

This is locally convenient but makes transport own prompt, evidence, failure,
trace, and context decisions. Those decisions would be difficult to reuse and
would repeat the service-local ownership failure corrected in Sprint 005.

### Add interaction behavior to `collector.memory`

The memory domain owns records, retrieval, and governance. Generation,
question handling, prompt construction, and response evidence are a consumer
responsibility. Combining them would make memory depend on one use case and
blur the retrieval boundary.

### Inject the existing `MemoryApplicationService`

This reuses current code but gives interaction an object that can store
memories. Tests could promise not to call `store`, but write authority would
remain structurally available.

### Create a separate interaction service and repository package

A new process could isolate runtime resources, but no approved lifecycle or
failure need justifies another deployed service. It would add packaging and
operations cost before the bounded path is validated.

### Retain the current design

There is no canonical grounded interaction path. External clients could call
`/memory/context` and invent prompt, generation, evidence, and failure behavior
outside Project Jebediah governance.

## Decision

### Canonical domain

`src/collector/interaction/` is the only permitted implementation of the
interaction domain.

It owns:

- single-turn orchestration
- deterministic context-decision integration
- prompt construction
- generation-provider interfaces
- result states and failure classification
- provider-response and citation validation
- public evidence packaging
- trace contracts

It must not import FastAPI, the service application module, Docker or Compose
configuration, Qdrant client types, or service-local source paths.

### Dependency direction

The permitted direction is:

```text
services/jebediah-memory
    -> collector.interaction
    -> collector.memory read-only retrieval capability
    -> existing canonical adapter boundaries
```

The memory domain must not import the interaction domain. Neither canonical
domain imports FastAPI or service-local modules.

### Read-only memory protocol

The memory domain owns a protocol semantically equivalent to:

```text
search(question, candidate_limit) -> sequence of RetrievalCandidate
```

The implementation may compose the approved embedding provider and Qdrant
semantic search internally. The interface visible to interaction contains no
store, save, index, upsert, delete, record mutation, verification transition,
or lifecycle transition.

The service composition root constructs the concrete memory reader and injects
only that restricted view into the interaction application. It must not inject
`MemoryApplicationService`, `QdrantMemoryRepository`, an embedding adapter, or
another store-capable or storage-specific object.

### Service boundary

FastAPI owns:

- `POST /interactions/query`
- HTTP request-size enforcement and schema translation
- dependency and configuration composition
- cancellation propagation
- response schema and HTTP status translation

FastAPI does not decide retrieval, duplicate handling, evidence selection,
prompt construction, generation validation, trace transitions, or result
state.

### External clients

n8n and every other external consumer use only the public HTTP contract. No
external client receives package imports, Qdrant access, write authority,
provider credentials, tools, or service-internal interfaces.

### Packaging

The interaction package is installed from the reviewed root project in the
same non-editable Python 3.12 service environment as `collector.memory`.
`PYTHONPATH`, source mounts, duplicate packages, and execution-directory
selection are prohibited. A container smoke must prove canonical
`site-packages` import origins.

## Consequences

### Positive

- Interaction behavior has one source, owner, and test boundary.
- FastAPI remains a thin composition and HTTP layer.
- Memory retrieval stays under the canonical memory domain.
- Write authority is absent from the interaction dependency rather than
  discouraged by convention.
- The package can be tested without HTTP, Qdrant types, or a live provider.

### Negative

- The memory domain needs a query-only application facade or adapter in
  addition to its current store-capable service.
- Static package-boundary and interaction-count tests become mandatory.
- A future need for a separately scaled interaction service would require a
  later deployment decision.

### Neutral

- Existing memory routes and ranking remain unchanged.
- This decision creates no runtime package until implementation is separately
  authorized.
- n8n remains possible as a caller but receives no special architecture role.

## Data and provenance impact

The interaction domain consumes derived retrieval candidates and produces
temporary context, prompt, provider-response, answer, evidence-view, and trace
data. It owns no authoritative memory and performs no write. Source authority,
provenance, lifecycle, verification, and Qdrant custody remain governed by the
memory architecture and ADR 0003.

Questions, prompts, answers, traces, and interaction records are not persisted.

## Security and privacy impact

The narrow port reduces accidental write and storage authority. FastAPI and
interaction must treat questions, candidates, metadata, and provider output as
untrusted. The package boundary does not authorize access to Qdrant internals,
tools, files, web services, private topology, or secrets.

## Operations and recovery impact

Sprint 006 remains a single-process repository candidate. The source-only
rollback is a Git revert because no live data, schema, or deployment is
changed. Future operations must measure model capacity, health, cancellation,
and keep-alive before deployment.

## Compatibility and migration

The proposal adds one endpoint and one package without changing current memory
contracts. There is no interaction-domain state to migrate. Existing clients
remain compatible. A future consumer moves from ad hoc `/memory/context`
composition to the governed interaction endpoint only through an explicit
client change.

## Validation

Acceptance and implementation require:

- static proof of one interaction package and no service shadow package
- no FastAPI, service, Qdrant-client, or concrete provider imports in the
  interaction domain
- a query-only protocol with no write-capable members
- no store-capable object injected into interaction
- one memory retrieval implementation and semantic-only ordering
- zero memory writes on success and every failure path
- existing API regression tests
- Python 3.12 installed-package and container import-origin smoke
- the complete
  [Sprint 006 Validation Requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)

Reconsider this decision only if a reviewed operational boundary requires a
separate service or the memory domain cannot expose read-only retrieval without
breaking its approved responsibilities.

## Follow-up work

- Implement the package and protocol only after all Sprint 006 ADRs are
  accepted and implementation is separately authorized.
- Evaluate deployment topology only after isolated capacity evidence exists.
- Document a future n8n client separately if an authorized workflow is later
  proposed.

## Related documents

- [Sprint 006 Specification](../SPRINT_006_SPECIFICATION.md)
- [Sprint 006 Validation Requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)
- [Memory Architecture](../ARCHITECTURE_MEMORY_SYSTEM.md)
- [Current Architecture](../ARCHITECTURE.md)
- [ADR 0002](0002-canonical-memory-domain-and-dependency-direction.md)
- [ADR 0007](0007-grounded-response-and-evidence-contract.md)
- [ADR 0008](0008-deterministic-retrieval-context-assembly.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Proposed for independent Work Mode review and Chief Architect decision at the
future exact head of the Sprint 006 Proposal v2 pull request. No decision or
implementation authority exists before that review is recorded.
