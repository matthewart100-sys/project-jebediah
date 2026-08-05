# Knowledge Manager 1.0 Phase 1 Implementation Plan

**Status:** Proposed

**Milestone:** Knowledge Manager 1.0

**Phase:** 1 - Knowledge Registry Foundation

**Date:** 2026-08-04

**Decision owner:** Chief Architect

**Implementation owner:** Implementation Engineer after exact-scope
authorization

**Reviewers:** Work Mode architecture review before implementation; Work Mode
implementation review before merge

**Planning base:** `c5693f5995738ddd62acfef7782728dcf815b146`

**Authorization state:** Planning only; implementation is not authorized by this
proposal

## Purpose

This plan defines the smallest implementation that can answer:

> Can Project Jebediah safely represent governed knowledge objects before it
> learns from them?

The answer is tested through a synthetic, metadata-only registry domain. The
phase does not ingest, store, learn from, retrieve, expose, or act on
organizational information.

`Knowledge Manager 1.0` is a milestone label, not a component, service, source
of authority, or runtime owner. The future Knowledge Vault remains the affected
named component.

## Intended outcome

Produce a reversible Python domain library that:

- Represents immutable registry metadata for a derived knowledge object.
- Keeps source, transformation, evidence, governance, human-review, and
  lifecycle context explicit.
- Provides a storage-neutral repository interface and in-memory reference
  adapter.
- Fails explicitly on invalid metadata and identity conflicts.
- Has no dependency on or integration with the Memory Service, Qdrant,
  embeddings, Collector pipelines, runtime services, or external information.
- Is covered by deterministic synthetic tests.

## Non-goals

Phase 1 must not implement:

- Document ingestion, quarantine, PDF or DOCX processing, text extraction,
  transformation, or admission evaluation.
- VBA, organizational, personal, confidential, or other external information
  loading.
- Embeddings, Qdrant writes, semantic search, retrieval, ranking, or model
  context construction.
- Open WebUI workflows, APIs, CLIs, pages, dashboards, or user workflows.
- Memory candidate creation, `MemoryItem` conversion, memory persistence,
  memory policy, consolidation, or runtime integration.
- A Knowledge Manager or Knowledge Vault service, deployment, container,
  database, migration, backup, or recovery process.
- Autonomous approval, promotion, lifecycle transitions, actions, or source
  correction.
- A new dependency or a change to existing dependency versions.
- Knowledge Vault advancement to **Specified**, **Implemented**, or
  **Operational** maturity.

If implementation requires any non-goal, work stops for scope and architecture
review.

## Architecture basis

### Accepted decisions

- [ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md)
  establishes the Knowledge Vault as a derived governed knowledge repository
  without source, memory, storage, model, or action authority.
- [ADR 0012](adr/0012-executive-organizational-intelligence-interface-boundary.md)
  defines a future read-only executive read model. It is not a Phase 1
  consumer.
- [ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
  defines quarantine-first document admission within the Collector boundary.
  Phase 1 does not implement that flow or reuse its attempt states as registry
  lifecycle states.
- [ADR 0002](adr/0002-canonical-memory-domain-and-dependency-direction.md)
  assigns the canonical memory domain and dependency direction.
- [ADR 0003](adr/0003-qdrant-repository-collection-and-payload-consolidation.md)
  limits Qdrant's current role to Memory Service payload and semantic-index
  responsibilities.

### Required proposed decision

[ADR 0014](adr/0014-knowledge-registry-domain-boundary.md) is a System-level
prerequisite because the work introduces a lasting domain responsibility,
authority boundary, metadata contract, package boundary, and repository
interface.

Implementation may begin only after:

1. Work Mode approves the exact plan and ADR proposal head.
2. The Chief Architect accepts ADR 0014 and authorizes the exact Phase 1 scope.
3. The accepted planning artifacts are present on reviewed `main`.
4. `CURRENT_SPRINT.md` records an active sprint or other bounded execution
   authority consistent with the accepted plan.

### Verified repository baseline

- The root Python package is `collector`; the project requires Python 3.12 or
  newer.
- `collector.memory.models.MemoryItem` is a frozen dataclass with identity,
  source identity, content, memory type, importance, metadata, memory
  provenance, and memory lifecycle.
- `MemoryItem` has real callers across memory policy, consolidation,
  integration, persistence, pipeline, runtime, and tests.
- `collector.memory.governance.MemoryProvenance` and
  `MemoryLifecycleState` have memory-specific semantics.
- `collector.memory.persistence.MemoryRepository` and
  `SemanticMemoryRepository` serve memory persistence and semantic retrieval.
- `InMemoryMemoryRepository` is the existing memory reference adapter.
- No Knowledge Registry package, contract, producer, consumer, store, service,
  or data exists.
- The clean planning baseline passes 142 tests in Python 3.14.5.
- Workspace problem inspection reports no current source or test problems.

## Relationship to the memory domain

Phase 1 adds a distinct registry contract because the accepted Knowledge Vault
boundary is not the Memory Service.

The implementation must not:

- Modify `MemoryItem`, `MemoryProvenance`, `MemoryLifecycle`,
  `MemoryLifecycleState`, `MemoryRepository`, or semantic repository APIs.
- Add registry fields to Qdrant payloads.
- Import `collector.memory` from the registry.
- Import the registry from existing memory, Collector, service, or runtime code.
- Convert a registry record to or from a `MemoryItem`.
- Treat a memory identity as a registry identity without a future approved
  producer contract.

This is semantic separation, not model duplication. Registry records omit
content, memory type, importance, memory metadata, reinforcement, retrieval,
and semantic persistence. The small registry-specific lifecycle vocabulary is
required because memory lifecycle and document-admission attempt states mean
different things.

## Proposed package boundary

The exact implementation target is:

```text
src/collector/knowledge/
    __init__.py
    registry/
        __init__.py
        models.py
        repository.py
        in_memory_repository.py

tests/collector/knowledge/
    registry/
        test_models.py
        test_repository.py
        test_package_boundaries.py
```

`collector.knowledge.registry` exports the reviewed enums, immutable metadata
types, `KnowledgeRegistryRepository`, and `KnowledgeRegistryConflict`.
`InMemoryKnowledgeRegistryRepository` remains available from its named adapter
module for contract tests and explicit local construction; it is not added to
an existing root or memory export. `collector.knowledge` does not re-export the
registry API. No existing export changes in Phase 1.

The package uses only the Python standard library. `pyproject.toml` and
`uv.lock` must remain unchanged unless implementation proves the package is not
included by the current build configuration. Such a proof stops work for plan
revision rather than authorizing an unreviewed packaging change.

## Domain contract

### Fixed metadata types

Implementation will create frozen dataclasses and enums for:

- `SourceReference`
  - `source_id`
  - `authority_scope`
  - `source_revision` or `observed_at`
- `TransformationReference`
  - `transformation_id`
  - `transformation_version`
- `EvidenceReference`
  - `evidence_id`
- `KnowledgeProvenance`
  - `producer_id`
  - `created_at`
  - one or more source references
  - one transformation reference
  - one or more evidence references
- `GovernanceScope`
  - `information_owner_id`
  - `information_domain`
  - `classification`
  - one or more `permitted_consumer_ids`
  - one or more `permitted_uses`
  - `retention_policy_id`
  - `deletion_policy_id`
  - `freshness_policy_id`
  - `invalidation_policy_id`
- `FreshnessState`
  - `current`
  - `aging`
  - `stale`
  - `unknown`
  - `not_applicable`
- `TemporalContext`
  - optional effective time
  - freshness state
  - freshness evaluation time
  - optional expiration time
- `UncertaintyState`
  - `bounded`
  - `incomplete`
  - `conflicting`
  - `unknown`
  - `not_applicable`
- `UncertaintyAssessment`
  - state
  - plain-language explanation
  - supporting evidence identifiers
  - material limitations or missing-evidence requirements
- `HumanReviewState`
  - `pending`
  - `approved`
  - `rejected`
- `HumanReview`
  - `review_policy_id`
  - state
  - reviewer identity, decision time, and rationale when decided
- `KnowledgeLifecycleState`
  - `registered`
  - `superseded`
  - `archived`
  - `invalidated`
- `KnowledgeLifecycle`
  - state
  - recording actor identity
  - recording time
  - reason
  - successor object identity when superseded
- `KnowledgeRegistryRecord`
  - `object_id`
  - `object_kind`
  - provenance
  - governance scope
  - temporal context
  - uncertainty assessment
  - human review
  - lifecycle state

No type contains source or derived content, an arbitrary metadata dictionary,
an embedding, a score, a model response, a memory object, or an action.

### Validation invariants

Constructors must reject:

- Empty or whitespace-only identifiers and policy labels.
- Naive datetimes.
- A source reference with neither revision nor observation context.
- Empty source, evidence, permitted-consumer, or permitted-use collections.
- Duplicate identifiers inside a source, evidence, permitted-consumer, or
  permitted-use collection.
- An uncertainty assessment without the evidence or limitations required by
  its qualitative state.
- `bounded` uncertainty without supporting evidence.
- `incomplete` uncertainty without a missing-evidence limitation.
- `conflicting` uncertainty with fewer than two evidence references.
- `unknown` uncertainty without a limitation explaining why no other state can
  be established.
- An uncertainty evidence identity that is absent from the record's provenance.
- A decided human review without reviewer identity, aware decision time, or
  rationale.
- A pending review that claims reviewer identity, decision time, or rationale.
- Lifecycle metadata without recording actor, aware time, or reason.
- A superseded lifecycle without a different successor object identity.
- A non-superseded lifecycle that claims a successor.
- Non-enum review or lifecycle states.

Constructors must normalize input collections to immutable tuples. They must
not silently invent identifiers, timestamps, freshness, uncertainty, policy
labels, review evidence, or lifecycle values. Missing freshness evidence is
represented as `unknown`, never inferred as `current`.

Phase 1 validates timezone awareness but does not interpret policy-specific
ordering among effective, freshness-evaluation, and expiration times. Adding a
temporal ordering rule is a plan change, not implementation discretion.

### Authority semantics

- `registered` means that the repository acknowledged the registry metadata,
  not that the represented claim is true or available.
- `approved` means only that an identified human approved the registry metadata
  for the stated governance scope.
- `approved` does not imply truth probability, verification, freshness,
  admission for another use, retrieval eligibility, action authority, or
  permission to update a source.
- Uncertainty is qualitative and evidence-linked. It is not a numeric
  confidence score or probability that a claim is true.
- Registration, retrieval rank, model self-confidence, repetition, and fluent
  wording cannot improve freshness or uncertainty.
- `superseded`, `archived`, and `invalidated` are explicit non-current states.
- Every lifecycle state retains actor, time, and reason; supersession also
  retains the successor identity.
- Phase 1 has no transition or promotion function. Callers construct an
  explicit immutable record.

## Repository contract

`KnowledgeRegistryRepository` will be a storage-neutral abstract base class
using the existing `abc.ABC` and `abstractmethod` repository convention. It
exposes only:

```python
register(record: KnowledgeRegistryRecord) -> None
find(object_id: str) -> KnowledgeRegistryRecord | None
contains(object_id: str) -> bool
```

The contract requires:

- Equal repeated registration under the same identity is idempotent.
- Different metadata under an existing identity raises a typed
  `KnowledgeRegistryConflict`.
- Invalid lookup identities raise `ValueError`.
- A miss returns `None` from `find` and `False` from `contains`.
- Returned records preserve immutability.

The interface deliberately excludes update, delete, list, query, search,
review, promote, transition, retrieval, and action methods.

`InMemoryKnowledgeRegistryRepository` is a reference adapter for tests. It is
not durable, thread-safety is not claimed, and no runtime composition may
instantiate it in Phase 1.

## Work sequence

### Checkpoint 0: Confirm authorization and baseline

- Confirm the exact accepted plan and ADR are on `main`.
- Confirm the current sprint or equivalent bounded authority names Phase 1.
- Confirm a clean short-lived implementation branch.
- Run the full existing test suite and record the count.
- Confirm no existing Knowledge Registry implementation appeared after the
  plan review.

**Stop condition:** Any head, scope, architecture, or baseline mismatch.

### Checkpoint 1: Implement domain types

- Add the proposed package and immutable metadata types.
- Implement explicit invariant validation.
- Export only the reviewed public types.
- Add focused positive and negative model tests.

**Review evidence:** Domain diff, invariant matrix, targeted tests, and package
imports.

### Checkpoint 2: Implement repository abstraction

- Add the storage-neutral interface and typed conflict.
- Add the in-memory reference adapter.
- Add repository contract tests for save, find, contains, idempotency,
  conflict, missing identity, and immutability.

**Review evidence:** Repository diff and targeted contract tests.

### Checkpoint 3: Prove separation and compatibility

- Add AST-based package-boundary tests that reject memory, adapter, service,
  Qdrant, Ollama, and runtime imports.
- Verify no existing source module imports the registry.
- Run the full suite.
- Run packaging/import validation using the existing environment and project
  configuration.
- Inspect the final diff for dependency, runtime, data, and documentation
  expansion.

**Stop condition:** Any existing memory contract, payload, behavior, dependency,
  or runtime composition changes.

### Checkpoint 4: Prepare implementation review

- Update the plan and validation evidence with actual results only.
- Update canonical status, sprint, component maturity, and changelog only to
  the extent supported by the implementation.
- Keep the Knowledge Vault below **Implemented** unless the full component
  criteria are separately satisfied; this phase alone does not satisfy them.
- Push one exact implementation head for independent Work Mode review.

Implementation does not merge until Work Mode validates the exact head and the
Chief Architect grants exact-head merge approval.

## Tests required

The
[Phase 1 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_1_VALIDATION_REQUIREMENTS.md)
are normative for implementation review. At minimum:

- Model construction and immutability.
- Every invalid metadata and review combination.
- Source revision or observation-context requirement.
- Review-state evidence requirements.
- Registry lifecycle state, actor, time, reason, and supersession evidence.
- Freshness, uncertainty, conflict, limitation, and invalidation-policy
  representation.
- Repository registration, lookup, presence, idempotency, and conflicts.
- Package dependency direction and lack of existing callers.
- Full regression suite.
- Documentation and whitespace validation.

Only fabricated, test-only identifiers and labels may appear in fixtures. The
plan authorizes those synthetic fixtures solely for deterministic tests; they
must not be copied from an external or organizational source.

## Acceptance criteria

Phase 1 implementation is acceptable only when:

1. ADR 0014 and the exact implementation plan were accepted before code began.
2. The final diff contains only the reviewed domain, repository, tests, and
   directly required documentation.
3. Registry records contain governance metadata but no source or derived
   content.
4. Source identity, authority scope, revision or observation context,
   transformation identity, evidence, information owner, classification,
   permitted consumers and uses, retention, deletion, freshness, uncertainty,
   invalidation policy, human review, and lifecycle are explicit.
5. Human approval cannot be inferred, omitted for a decided state, or produced
   by repository registration.
6. The repository is storage-neutral and its only adapter is an in-memory test
   reference.
7. Existing memory models, repositories, payloads, pipelines, and callers are
   unchanged.
8. No Qdrant, embedding, ingestion, API, UI, service, runtime, or external-data
   work exists.
9. Targeted and full tests, package validation, documentation validation, and
   diff checks pass.
10. Independent Work Mode review has no unresolved blocking findings.
11. The Chief Architect approves the exact implementation head for merge.

## Dependencies

Phase 1 depends on:

- Accepted ADRs 0002, 0003, 0011, 0012, and 0013 remaining unchanged.
- Work Mode approval and Chief Architect acceptance of proposed ADR 0014.
- Exact-scope implementation authorization in canonical project state.
- The existing Python package and test environment.

It does not depend on JCS, Qdrant availability, Ollama availability, Docker,
organizational information, the VBA demonstration, or runtime services.

## Risks and responses

| Risk | Required response |
| --- | --- |
| Registry becomes a second Memory Service | Separate package, no memory imports, no content or retrieval fields, boundary tests |
| Registry approval is interpreted as truth | Explicit review semantics, no confidence score, negative tests and documentation |
| Registration becomes implicit promotion | No promotion or transition API; `registered` means record presence only |
| Package path implies Collector component authority | ADR 0014 explicitly separates repository namespace from component authority |
| Opaque policy labels appear enforced | Describe them as references only; no runtime or external information |
| Arbitrary metadata leaks content or sensitive data | No arbitrary metadata bag; fixed typed fields and synthetic fixtures |
| Repository interface expands into search or storage design | Keep three-method contract; stop on requested expansion |
| Existing memory compatibility regresses | No memory edits; package-boundary tests and full regression suite |
| Implementation silently selects durability | In-memory reference only; no dependency or configuration changes |
| Scope expands after review | Stop, revise artifacts, obtain re-review and exact-scope authorization |

## Rollback

Before any consumer or durable store exists, rollback is:

1. Revert the Phase 1 implementation commit or pull request.
2. Remove the new package exports and tests through normal review.
3. Re-run the pre-implementation full suite and documentation checks.
4. Update canonical status and changelog to record the reverted reality.

No data migration, service shutdown, source correction, or consumer
coordination is required because Phase 1 creates no durable or external state.

## Remaining limitations after Phase 1

Even a successful Phase 1 will not provide:

- An implemented Knowledge Vault component.
- A source, admission flow, transformation, or content store.
- A durable registry.
- A registry producer or consumer.
- Identifier generation or cross-system versioning.
- Policy interpretation or enforcement.
- Review workflow or lifecycle mutation.
- Retrieval, learning, memory, reasoning, interface, or action capability.
- Deployment, operations, backup, restore, migration, or recovery readiness.

## Phase 2 prerequisites

Before any next phase, the Chief Architect must approve a bounded objective and
resolve at least:

- Knowledge Vault component owner and operational owner.
- The first producer and consumer contracts.
- The approved information domain, originating source authority, purpose,
  classification, permitted uses, retention, deletion, and legal or consent
  constraints.
- Identifier generation and versioning.
- Whether the next phase implements admission, transformation, registry
  mutation, or a durable adapter; these are separate responsibilities and must
  not be bundled by default.
- Security, access, audit, observability, failure, retry, backup, restore,
  migration, and recovery requirements appropriate to the selected scope.
- The relationship, if any, to the Memory Service.
- A storage ADR before choosing Qdrant or another durable technology.

No Phase 2 work begins from this plan alone.

## Review and authorization request

Work Mode is asked to determine whether the proposed ADR, domain contract,
package boundary, test plan, rollback, and stop conditions preserve accepted
architecture and are sufficiently bounded for an implementation-authorization
decision.

If Work Mode approves, the Chief Architect is asked to:

1. Accept or reject ADR 0014 at the exact reviewed head.
2. Authorize or withhold only the bounded Phase 1 implementation described
   here.

Approval must identify the exact reviewed commit. Until that decision is
recorded and reconciled into canonical `main`, implementation remains
unauthorized.
