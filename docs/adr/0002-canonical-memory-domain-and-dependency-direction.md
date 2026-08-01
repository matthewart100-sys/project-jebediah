# ADR 0002: Canonical Memory Domain and Dependency Direction

**Status:** Accepted

**Decision level:** System

**Date:** 2026-07-31

**Decision owner:** Project maintainer

**Reviewers:** Chief Architect and project maintainer

## Decision summary

`src/collector/memory/` is the sole canonical implementation of the
`collector.memory` domain. `services/jebediah-memory/` is a composition, HTTP,
process, packaging, and deployment boundary that consumes the installed
canonical package and does not retain copied memory-domain or embedding logic.

## Context

Project Jebediah currently contains two source trees that provide the same
Python import namespace:

- `src/collector/memory/`
- `services/jebediah-memory/app/collector/memory/`

Which implementation is loaded depends on the execution directory. This
allows tests and the service runtime to exercise different files while using
identical imports. A lasting ownership and dependency-direction decision is
required before either tree can be removed safely.

### Verified facts

- The root project packages `src/collector` through `pyproject.toml`.
- The root test suite imports `collector.memory` from the packaged `src/`
  tree.
- The service image currently copies only
  `services/jebediah-memory/app/`, including a second `collector` package.
- Running the service from its application directory resolves
  `collector.memory` to the service-local tree.
- The two memory trees contain 29 corresponding Python files. Twenty-five are
  byte-identical, three differ only in formatting, export order, or
  documentation, and the two Qdrant repository files differ materially.
- `services/jebediah-memory/app/main.py` also contains direct Qdrant write and
  search behavior outside both repository implementations.
- The root project requires Python 3.12 or newer, while the service Dockerfile
  currently uses Python 3.11.
- The merged Sprint 004 baseline has 66 passing tests.

### Reported facts

- Project materials report a local Docker, Qdrant, and Ollama environment.
- Repository evidence does not verify the deployed service image, its import
  origin, or the current runtime environment.

### Working assumptions

- The tracked FastAPI endpoints are the compatibility target for the service
  cutover.
- The canonical package can be installed into the service image from the
  reviewed repository commit or an immutable wheel produced from that commit.
- Consolidation can be implemented and reviewed without deployment or live
  data changes.

### Open questions

- The final container build mechanism is an implementation choice within this
  decision, provided it installs the reviewed canonical package without a path
  hack and uses a supported Python version.
- Live deployment remains a separate operations gate. It does not prevent the
  source-ownership decision because Sprint 005 performs no deployment.

## Scope

This decision governs:

- Canonical ownership of the memory Python domain
- Allowed dependency direction
- Service and domain responsibility boundaries
- Package installation and import-origin requirements
- Compatibility and removal criteria for the duplicate service tree
- Ownership of the embedding provider boundary used by memory

## Non-goals

- Redesigning memory models, governance, lifecycle, or verification
- Changing endpoint paths, HTTP schemas, or response meanings
- Adding Collector 1.0, agents, n8n orchestration, or new memory features
- Selecting Qdrant data authority or vector compatibility rules, which are
  governed by ADR 0003 and ADR 0004
- Deploying or changing live infrastructure

## Decision drivers

- One source of memory-domain behavior
- Preserve the existing `collector.memory` import namespace
- Make tests exercise the same package used by the service
- Keep reusable domain behavior independent from FastAPI and deployment
- Avoid path injection and manually synchronized copies
- Preserve Sprint 004 governance and semantic-only retrieval behavior
- Make removal incremental and reversible

## Considered alternatives

### Make the service-local memory tree canonical

This would match the current executable service path, but it would leave
reusable domain behavior inside a deployment directory and conflict with the
existing root packaging and test layout. Other consumers would need to depend
on service internals.

### Create a new top-level memory package

A package such as `src/jebediah_memory/` could provide a clean name, but it
would require a broad import migration without resolving an additional
current requirement. The existing `collector.memory` namespace is already
used consistently by callers.

### Keep both source trees synchronized

This retains the drift mechanism Sprint 005 exists to remove. Byte-identical
files still have separate ownership, packaging, and review paths.

### Retain the current design

Tests and runtime would continue resolving identical imports to different
files. Qdrant, embedding, governance, and pipeline changes would continue to
require manual duplication and could diverge silently.

## Decision

### Canonical domain

`src/collector/memory/` is the only source location for the
`collector.memory` implementation.

It owns:

- Memory models and memory types
- Provenance, verification-state, and lifecycle representation
- Confidence, retention, importance, and duplicate evaluation
- Consolidation and policy
- Pipeline and runtime result contracts
- Record-repository and semantic-index boundaries
- Qdrant payload conversion and retrieval-candidate construction
- Semantic-only ranking

`src/collector/embeddings/` owns the canonical `EmbeddingProvider` boundary,
the Ollama adapter, and embedding-response validation. The memory domain may
depend on that provider interface but must not construct an Ollama client.

### Dependency direction

The only permitted direction is:

```text
services/jebediah-memory
    -> src/collector/memory
    -> canonical boundary interfaces and domain behavior
```

The service may import and construct canonical components. The canonical
domain must not import:

- FastAPI
- Service request or response models
- The service application module
- Docker or Compose configuration
- Service-local source paths

External adapters implement canonical interfaces and are constructed by the
service composition root.

### Service boundary

`services/jebediah-memory/` retains only:

- FastAPI application and route definitions
- Pydantic HTTP request models
- HTTP response and status mapping
- Environment configuration
- Dependency construction and injection
- Health and process-startup composition
- Docker, Compose, and runtime packaging

After cutover it must not contain:

- `app/collector/`
- A second embedding implementation
- Copied governance, policy, intelligence, persistence, or ranking modules
- Qdrant collection, point, payload, filter, or query logic in `main.py`
- A second intelligence evaluation path
- Hidden persistence through a default in-memory repository

HTTP-to-domain translation is permitted. Reimplementing domain decisions in
that translation is not.

### Packaging and removal

- The service must install the root project or an immutable wheel built from
  the exact reviewed commit.
- The service runtime must use Python 3.12 or newer.
- No `PYTHONPATH` injection, source bind mount, or execution-directory trick
  may select the canonical implementation.
- An import-origin smoke test must prove the service loads the reviewed root
  package.
- The service-local tree is removed only after characterization, API,
  governance, packaging, and adapter tests pass against the canonical package.
- Temporary import aliases may preserve existing internal imports during the
  transition, but no duplicate implementation may remain after cutover.

## Consequences

### Positive

- Memory behavior has one implementation, owner, test path, and review path.
- Tests and service runtime exercise the same package.
- The FastAPI service remains independently deployable without owning a
  second domain.
- Existing `collector.memory` imports can remain stable.
- Future domain changes cannot silently drift between root and service trees.

### Negative

- The service build and dependency installation must change.
- Python 3.11 must be replaced with a root-compatible runtime.
- The cutover requires import-origin and container tests.
- Duplicate removal must wait until compatibility is demonstrated.

### Neutral

- This decision does not change API behavior, governance behavior, storage
  data, or retrieval ranking.
- Directory movement alone does not establish deployment readiness.

## Data and provenance impact

No runtime data is migrated by this decision. Memory provenance, lifecycle,
verification, payload fields, and source authority remain unchanged.

Canonical source-code ownership is distinct from information authority. The
root package owns memory behavior; it does not become authoritative for the
truth of stored claims.

## Security and privacy impact

Removing copied code reduces unreviewed drift in validation and failure paths.
The packaging change must not copy secrets, local model data, private
configuration, or runtime databases into the image or repository.

## Operations and recovery impact

The service image must identify the reviewed package artifact and supported
Python version. Before duplicate removal, the previous service composition is
the rollback point. After a source-only merge, a Git revert restores the prior
layout because this decision performs no live-data operation.

Deployment remains separately gated by service health, dependency,
configuration, backup, and recovery validation.

## Compatibility and migration

Migration proceeds in this order:

1. Characterize current imports and behavior.
2. Define canonical contracts.
3. Install the root package into the service without deleting the shadow
   tree.
4. Cut service composition over to canonical dependencies.
5. Prove API and governance compatibility.
6. Remove the service-local memory and embedding trees.

Public endpoint paths, request fields, response fields, enum values, default
governance behavior, and semantic-only ranking remain compatible.

## Validation

Acceptance requires:

- Root and service import-origin tests
- Service/container build using Python 3.12 or newer
- API characterization and compatibility tests
- Governance regression tests
- One-evaluation and one-write interaction tests
- Proof that rejected requests do not embed or write
- Proof that no service-local domain or embedding implementation remains
- Full future Sprint 005 validation defined in
  [Sprint 005 Validation Requirements](../SPRINT_005_VALIDATION_REQUIREMENTS.md)

Reconsider this decision if normal package installation cannot support the
service without changing the public namespace or API contract.

## Follow-up work

- Implement the phased source and packaging migration only after this ADR is
  accepted.
- Reconcile shared dependency ownership during the implementation phase.
- Record deployment evidence separately from repository implementation.

## Related documents

- [Sprint 005 Implementation Plan](../SPRINT_005_IMPLEMENTATION_PLAN.md)
- [Memory Architecture](../ARCHITECTURE_MEMORY_SYSTEM.md)
- [Repository Standards](../REPOSITORY_STANDARDS.md)
- [Engineering Standards](../ENGINEERING_STANDARDS.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [ADR 0003](0003-qdrant-repository-collection-and-payload-consolidation.md)
- [ADR 0004](0004-embedding-model-identity-and-vector-compatibility.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Accepted for implementation on 2026-07-31 after Chief Architect final review
and explicit maintainer authorization. Implementation is limited to Sprint
005; deployment, commit, pull-request, and merge authority were not granted.
