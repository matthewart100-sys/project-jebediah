# ADR 0014: Knowledge Registry Domain Boundary

**Status:** Accepted

**Accepted:** 2026-08-04

**Decision level:** System

**Date:** 2026-08-04

**Decision owner:** Chief Architect

**Reviewers:** Work Mode architecture review, then Chief Architect final review

**Repository custody:** Project maintainer

**Affected component:** Knowledge Vault

**Component maturity impact:** None; acceptance or bounded implementation of
this registry alone does not advance the Knowledge Vault beyond **Named**

**Implementation status:** The bounded metadata-only library was implemented
through pull request #49 and squash-merged at
`4ed2ac283e4df6aec30b67f7c4aa50338924c435`. This status note records
implementation evidence only and does not change this decision or advance the
Knowledge Vault component beyond **Named**.

## Decision summary

Introduce a metadata-only Knowledge Registry domain library as a bounded
foundation for future Knowledge Vault work. The registry records immutable
governance metadata for derived knowledge objects without storing their
content, becoming a source of truth, integrating with memory, or authorizing
runtime use.

## Context

[ADR 0011](0011-knowledge-vault-authority-and-boundary-model.md) defines the
Knowledge Vault as a derived governed knowledge repository, but deliberately
does not select its schema, interface, storage, service, or relationship to the
implemented Memory Service. The Knowledge Vault remains **Named** in the
[component registry](../reference/COMPONENT_REGISTRY.md).

Knowledge Manager 1.0 Phase 1 asks whether Project Jebediah can represent
governed knowledge objects before it learns from, retrieves, or acts on them.
Answering that question requires a small domain contract, but implementing the
contract inside the existing memory domain would silently identify the
Knowledge Vault with the Memory Service. Selecting a durable store or service
would introduce operations and recovery obligations that Phase 1 does not
authorize.

The term `Knowledge Manager 1.0` is a milestone label. This decision does not
create a component, service, operator, information authority, or source-use
authorization with that name.

### Verified facts

- Reviewed GitHub `main` is authoritative for Project Jebediah's canonical
  project records.
- Originating sources retain authority for facts in their approved subjects and
  scopes.
- ADR 0011 makes Knowledge Vault representations derived and requires source
  identity, provenance, transformation identity, classification, permitted use,
  review state, uncertainty, freshness, and lifecycle context.
- ADR 0011 prohibits treating the Memory Service, Qdrant, retrieval success, or
  model output as knowledge authority.
- ADR 0013 defines document-admission attempt states within the Collector
  boundary. Those states do not define the lifecycle of a derived knowledge
  representation.
- The canonical `collector.memory` domain already owns `MemoryItem`,
  `MemoryProvenance`, `MemoryLifecycle`, `MemoryLifecycleState`, and
  `MemoryRepository`.
- `MemoryItem` includes content, memory type, importance, memory provenance, and
  memory lifecycle. It has callers across policy, consolidation, integration,
  persistence, pipeline, runtime, and tests.
- `MemoryLifecycleState` values describe memory representations:
  `active`, `reinforced`, `superseded`, and `archived`.
- `MemoryRepository` and `SemanticMemoryRepository` serve memory persistence and
  semantic retrieval. Qdrant is one implemented adapter under that boundary.
- The full repository baseline passes 142 tests in the selected Python 3.14.5
  development environment.
- At planning base `c5693f5995738ddd62acfef7782728dcf815b146`, no active
  implementation sprint, external information source, Knowledge Vault storage
  system, service, deployment, or operator was authorized.
- The Chief Architect ratified `collector.knowledge.registry` as repository
  packaging only; it does not assign Collector Engine authority or ownership
  over registered knowledge.

### Reported facts

- None. This decision relies on repository and validation evidence.

### Working assumptions

- A metadata-only library can test the governance contract without source
  content, external information, retrieval, or persistent infrastructure.
  Implementation review must reject the assumption if the proposed code needs
  any of those capabilities.

### Open questions

- The future Knowledge Vault component owner, operational owner, producers,
  consumers, service boundary, durable store, recovery contract, and approved
  information domains remain unresolved. Those questions block later
  component maturity and runtime work, but they do not block a synthetic,
  metadata-only domain contract with no runtime consumer.
- Stable object identifiers are caller-supplied opaque strings in Phase 1.
  Identifier generation and cross-system namespace allocation require a future
  producer contract.
- Concrete classification vocabularies, permitted-use vocabularies, retention
  policies, and review-role identities require approved information-domain and
  security contracts. Phase 1 represents their identifiers but does not define
  them.

## Scope

This decision governs:

- The responsibility and authority of a metadata-only Knowledge Registry.
- Its separation from source content, the Memory Service, admission,
  transformation, retrieval, and action.
- The minimum metadata required to represent one governed derived knowledge
  object.
- Human review and registry lifecycle representation.
- A storage-neutral repository interface and an in-memory test adapter.
- Package dependency direction and Phase 1 compatibility.

## Non-goals

This decision does not:

- Implement or authorize document ingestion, quarantine, parsing, extraction,
  transformation, or admission evaluation.
- Acquire, retain, or use organizational or other external information.
- Store source content or derived content.
- Define a source adapter, producer, consumer, service, API, command, user
  interface, workflow, or deployment.
- Generate embeddings, write to Qdrant, search, rank, retrieve, or construct
  model context.
- Integrate with `MemoryItem`, memory pipelines, consolidation, runtime
  intelligence, or memory persistence.
- Select a durable store or define backup, restore, migration, or operations.
- Implement autonomous review, promotion, lifecycle transitions, or action.
- Advance the Knowledge Vault to **Specified**, **Implemented**, or
  **Operational** maturity.

## Decision drivers

- Preserve repository and originating-source authority.
- Keep Knowledge Vault records explicitly derived and evidence-linked.
- Avoid duplicating or silently extending canonical memory models.
- Represent human review without granting automated approval authority.
- Keep admission, registry lifecycle, memory lifecycle, and runtime
  availability semantically distinct.
- Make persistence replaceable and avoid premature operational commitments.
- Produce a small contract that can be validated with synthetic information.
- Keep rollback complete because no durable state or consumer exists.

## Considered alternatives

### Alternative A: Extend `MemoryItem` and `MemoryRepository`

Adding registry fields to `MemoryItem` would reuse an existing object and
repository. It would also couple the new contract to content, importance,
memory types, memory policy, semantic retrieval, Qdrant serialization, and many
existing callers. It would make the Knowledge Vault appear to be the Memory
Service, contradict ADR 0011, and would exceed the authorized no-memory-
integration boundary.

This alternative is rejected.

### Alternative B: Add a metadata-only adjacent domain library

An adjacent domain can represent only the governance envelope needed by future
Knowledge Vault work. It can avoid content and runtime dependencies, use a
storage-neutral repository contract, and remain fully reversible. The cost is
an additional domain vocabulary whose semantic separation from memory must be
explicit and tested.

This alternative is selected.

### Alternative C: Create a Knowledge Manager service and durable database

A service and store could provide real persistence and APIs immediately. They
would require component ownership, authentication, classification enforcement,
health, operations, backup, restore, migration, and recovery decisions that
are unresolved and unauthorized.

This alternative is rejected for Phase 1.

### Retain the current design

The project could keep the Knowledge Vault conceptual and implement nothing.
That remains the safe outcome if this ADR or its implementation plan is not
accepted. It does not test whether a bounded registry contract can represent
the required governance metadata.

## Decision

### Responsibility

The Knowledge Registry is a metadata-only domain library. It records that a
specific immutable registry record, with stated provenance, governance scope,
human-review state, and lifecycle state, was registered. Its authority extends
only to the integrity of that registry record.

A registry record does not establish that:

- Its source claims are true, current, complete, or authorized outside their
  stated scope.
- Its derived representation has been retrieved, validated as factual, or made
  available to a consumer.
- Its review decision grants source authority, action authority, or general
  permission to use information.
- The Knowledge Vault, Memory Service, Qdrant, or a model is authoritative.

### Domain contract

Phase 1 will define immutable, standard-library domain types equivalent to the
following semantic contract:

| Type | Required meaning |
| --- | --- |
| `SourceReference` | Stable source identity, authority scope, and a source revision or observation context |
| `TransformationReference` | Identity and version of the transformation that produced the derived representation |
| `EvidenceReference` | Stable reference to supporting evidence without embedding evidence content |
| `KnowledgeProvenance` | Producer identity, creation time, one or more source references, transformation reference, and evidence references |
| `GovernanceScope` | Information owner, domain, classification, permitted consumer and use, retention, deletion, freshness, and invalidation policy identifiers |
| `FreshnessState` | `current`, `aging`, `stale`, `unknown`, or `not_applicable` under the referenced policy |
| `TemporalContext` | Effective, freshness-evaluation, and expiration times plus freshness state |
| `UncertaintyState` | `bounded`, `incomplete`, `conflicting`, `unknown`, or `not_applicable` |
| `UncertaintyAssessment` | Qualitative state, explanation, supporting evidence references, and material limitations |
| `HumanReview` | Review-policy identity, `pending`, `approved`, or `rejected` state, and required decision evidence |
| `KnowledgeLifecycleState` | `registered`, `superseded`, `archived`, or `invalidated` registry-record state |
| `KnowledgeLifecycle` | Lifecycle state, recording actor, time, reason, and successor identity when superseded |
| `KnowledgeRegistryRecord` | Stable object identity, object-kind identifier, provenance, governance scope, temporal context, uncertainty, review, and lifecycle |

The contract contains no source or derived content, embedding, retrieval score,
memory type, importance, model output, arbitrary metadata bag, or action
instruction.

All identifiers are non-empty opaque strings. All times are timezone-aware.
At least one source reference, evidence reference, permitted consumer, and
permitted use are required. Duplicate identifiers inside one collection are
invalid. Every source reference includes a revision or observation context. A
transformation identity and version are required because the registered object
is derived.

Freshness is an explicit qualitative state evaluated under the referenced
freshness policy. Missing freshness evidence is `unknown`, never `current`.
Expiration, when present, is visible and cannot be converted into current state
by registration.

Uncertainty uses the qualitative contract accepted for the organizational-
intelligence interface. Every assessment has a plain-language explanation and
evidence references or material limitations appropriate to the state.
`bounded` requires supporting evidence; `incomplete` identifies missing
evidence; `conflicting` identifies at least two materially conflicting evidence
references; and `unknown` identifies why the evidence cannot establish another
state. Every referenced evidence identity must exist in the same record's
provenance. `not_applicable` is reserved for a deterministic registry condition
for which claim uncertainty does not apply.

Uncertainty is not a numeric confidence score or probability that a claim is
true. Retrieval rank, model self-confidence, repetition, fluent wording, and
successful registration cannot set or improve it.

Every human-review record identifies the review policy. `HumanReview.pending`
contains no reviewer decision. `approved` and `rejected` require an identified
human reviewer, decision time, and rationale. Approval means only that the
registry metadata passed the explicitly identified review for its stated
scope. It is not a truth probability, factual verification, consumer
authorization, or action authorization.

`registered` means only that the record exists in the registry. `superseded`,
`archived`, and `invalidated` make that record ineligible for future ordinary
use. Each lifecycle value identifies who or what recorded it, when, and why;
`superseded` also identifies its successor. Phase 1 represents these states but
implements no transition engine, automatic promotion, retrieval eligibility,
or state mutation.

### Repository contract

Phase 1 will define `KnowledgeRegistryRepository` with only:

- `register(record)` to persist an immutable registry record.
- `find(object_id)` to return the exact record or no result.
- `contains(object_id)` to report registration presence.

Registering an identical record with the same object identity is idempotent.
Registering different metadata under an existing identity raises an explicit
conflict. The interface has no update, delete, list, search, retrieval,
promotion, review-decision, or lifecycle-transition method.

An in-memory adapter may implement this contract only as a reference adapter
and deterministic test fixture. It is not a durable store or runtime
composition decision.

### Package and dependency boundary

The proposed library path is `collector.knowledge.registry`. This is repository
packaging, not an assignment of Knowledge Vault authority to the Collector
Engine component.

The registry library may import only the Python standard library and modules
inside its own boundary. It must not import:

- `collector.memory`
- Collector pipelines, adapters, or runtime composition
- Qdrant or Ollama libraries
- service or API modules

No existing module may import the registry during Phase 1. Integration requires
separate authorization and review.

### Ownership

The project maintainer owns repository custody and the implemented bounded
library. This ADR does not assign Knowledge Vault component or operational
ownership. The component remains unassigned pending specification.

## Consequences

### Positive

- The project can validate governance metadata before processing real
  information.
- Existing memory models, payload contracts, and callers remain unchanged.
- Human review is explicit and cannot be inferred from successful storage.
- Content, retrieval, model, and action authority remain outside the registry.
- The persistence contract is testable without selecting a durable technology.
- Phase 1 can be rolled back without data migration or consumer coordination.

### Negative

- The project gains a second lifecycle vocabulary that reviewers must keep
  distinct from memory and admission states.
- The registry is not useful to a runtime consumer until later architecture and
  authorization exist.
- Opaque policy identifiers can be validated structurally but not interpreted
  until information-domain contracts are approved.
- Package placement under `collector` can be misread as component ownership
  unless dependency and documentation boundaries remain explicit.

### Neutral

- The design neither selects nor rejects Qdrant or another future durable store.
- The design neither integrates nor forbids a future adapter to the Memory
  Service; that relationship remains a separate decision.
- The registry is not a document catalog, vector index, knowledge graph, or
  source repository.

## Data and provenance impact

The registry record is derived governance metadata. Its repository has
operational authority over the record it acknowledged, not over source facts or
the derived representation referenced by the record.

Phase 1 uses synthetic records only. It retains no source content, derived
content, personal data, external information, embeddings, or model output.
Source identity, source revision or observation context, transformation
identity and version, evidence references, review evidence, classification,
permitted-use identifiers, and lifecycle remain visible.

No migration applied because Phase 1 began without a Knowledge Registry
implementation or data and the merged library creates no durable state.

## Security and privacy impact

The fixed metadata contract minimizes accidental content retention and has no
arbitrary metadata field. Uncertainty explanations and limitations are
governance metadata, not a place to copy source or derived content. Tests use
synthetic identifiers and labels.

The registry does not validate source authorization, classification policy,
legal basis, or permitted use; it only requires the corresponding identifiers.
No external information may enter Phase 1. A future producer must enforce
source and use authorization before registry registration.

The package exposes no network, file, database, model, or action surface.
Missing required governance metadata fails explicitly rather than producing a
success-shaped record.

## Operations and recovery impact

No runtime, durable state, deployment, health check, telemetry, backup, restore,
or recovery responsibility is introduced. The in-memory adapter loses all
records when its process ends and must not be described as durable.

Operational design remains blocked on component ownership, an approved durable
store, consumer contracts, security, observability, migration, backup, restore,
and recovery evidence.

## Compatibility and migration

The new package has no existing consumer. Existing `collector.memory` APIs,
Qdrant payloads, tests, and runtime composition remain unchanged.

Rollback removes the new package and its tests. No external or durable state
requires migration. A future breaking change to the registry contract requires
consumer inventory and a versioning decision before integration.

## Validation

Acceptance requires the evidence in the
[Phase 1 validation requirements](../KNOWLEDGE_MANAGER_1_PHASE_1_VALIDATION_REQUIREMENTS.md),
including:

- Domain invariant and failure tests.
- Human-review evidence tests.
- Repository idempotency and conflict tests.
- Package dependency tests.
- Proof that existing memory callers and contracts remain unchanged.
- The full repository test suite.
- Documentation and diff validation.

Reconsider this decision if the implementation needs content storage, a memory
import, a runtime consumer, a durable store, lifecycle mutation, external
information, or a broader repository API.

## Follow-up work

- Preserve the merged Phase 1 implementation and closeout evidence without
  expanding its bounded authority.
- Assign Knowledge Vault component and operational ownership before component
  specification.
- Approve producers, consumers, interfaces, information domains, policy
  vocabularies, security, operations, and recovery before runtime integration.
- Define identifier generation and versioning with the first approved producer.
- Select a durable store only through a separately reviewed persistence and
  recovery decision.
- Define any relationship to the Memory Service before either package imports
  the other.

## Related documents

- [Knowledge Manager 1.0 Phase 1 Implementation Plan](../KNOWLEDGE_MANAGER_1_PHASE_1_IMPLEMENTATION_PLAN.md)
- [Knowledge Manager 1.0 Phase 1 Validation Requirements](../KNOWLEDGE_MANAGER_1_PHASE_1_VALIDATION_REQUIREMENTS.md)
- [ADR 0011: Knowledge Vault Authority and Boundary Model](0011-knowledge-vault-authority-and-boundary-model.md)
- [ADR 0013: Governed Organizational Document Admission Boundary](0013-governed-organizational-document-admission-boundary.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [Component Registry](../reference/COMPONENT_REGISTRY.md)
- [Memory Architecture](../ARCHITECTURE_MEMORY_SYSTEM.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Independent Work Mode reviewed exact proposal head
`00db845a98f63fc3b8d1bb1135adcafa9d306b97` against base
`c5693f5995738ddd62acfef7782728dcf815b146` and returned **APPROVED** with no
Blocking or High findings.

The Chief Architect then:

- Ratified `collector.knowledge.registry` as repository packaging only.
- Accepted ADR 0014 at that exact reviewed head.
- Authorized only the bounded Phase 1 implementation defined by the associated
  plan, subject to its canonical Checkpoint 0.
- Approved squash merge of pull request #47 at that exact head.

Pull request #47 squash-merged the reviewed proposal into `main` as
`f9fc0c6c15a4148f5d538f56ac4ab2ec8e92c93e`.

Independent Work Mode later approved exact Phase 1 implementation head
`7b06b1df831ad2a7a4726fa5e92746538cec34b4` with no findings. The Chief
Architect approved that exact head for merge and closeout, and pull request #49
squash-merged it into `main` as
`4ed2ac283e4df6aec30b67f7c4aa50338924c435`. Post-merge validation is recorded
in the
[Phase 1 closeout](../KNOWLEDGE_MANAGER_1_PHASE_1_CLOSEOUT.md).

Acceptance does not authorize any excluded ingestion, external information,
memory integration, durable storage, runtime, deployment, or autonomous
capability.
