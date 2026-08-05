# ADR 0011: Knowledge Vault Authority and Boundary Model

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-04

**Decision owner:** Chief Architect

**Reviewers:** Work Mode architecture review, then Chief Architect final review

**Repository custody:** Project maintainer

**Component maturity:** Named

**Proposed maturity after acceptance:** Specified

**Readiness:** Architecture proposal only; not implementation-ready,
migration-ready, deployment-ready, operational, or authorized for external
information use

## Decision

Project Jebediah will define the Jebediah Knowledge Vault as a **derived
governed knowledge repository**.

The Knowledge Vault will preserve governed, source-linked derived
representations for bounded retrieval and future approved consumers. It will
retain the provenance, transformation identity, freshness, classification,
uncertainty, and lifecycle information needed to interpret those
representations safely.

Reviewed GitHub `main` and its canonical owners remain authoritative for
Project Jebediah's canonical project records, including governance,
architecture, accepted decisions, plans, current status, and reviewed project
evidence. Approved originating sources remain authoritative for the facts
within their defined subjects and scopes.

The Knowledge Vault does not become authoritative merely because information is
reviewed, curated, durable, validated for shape, transformed, indexed,
embedded, summarized, or retrieved. Information authority does not grant action
authority.

The Knowledge Vault remains **Named** while this ADR is Proposed. It may advance
to **Specified** only after this ADR and all affected canonical architecture,
data-ownership, terminology, component, status, sprint, and roadmap records are
accepted and merged. Acceptance does not establish **Implemented** or
**Operational** maturity.

## Context

Project Jebediah already distinguishes authoritative, cached, derived, and
temporary information. It requires explicit provenance, ownership, lifecycle,
recovery, and trust boundaries before dependent implementation.

The term `Jebediah Knowledge Vault` does not yet have an accepted architectural
boundary. Without one, it could be interpreted as:

- A replacement for, or competing authority to, canonical project records
  maintained on reviewed GitHub `main`
- An independent authority for organizational or external facts
- A synonym for the Jebediah Memory Service
- A synonym for Qdrant or another persistence technology
- A vector index, document archive, or model context window
- A future Knowledge Graph
- A collection of VBA demonstration material
- A general-purpose source of truth

Those interpretations assign materially different authority, security,
recovery, lifecycle, and consumer responsibilities. This ADR establishes the
conceptual responsibility before an implementation choice can determine the
boundary implicitly.

### Verified facts

- Reviewed GitHub `main` is authoritative for canonical project records within
  the subject assigned to each canonical owner.
- Project data-ownership policy distinguishes authoritative, cached, derived,
  and temporary information.
- The repository contains Collector and Memory Service implementation
  candidates, but their presence does not establish a Knowledge Vault
  component.
- Qdrant payloads have a narrow operational authority under ADR 0003; Qdrant is
  not authoritative for the truth of represented source claims.
- Open pull request #44 contains proposed VBA demonstration materials on its
  unmerged `feature/interaction-gateway` branch. Those artifacts are not
  canonical project records and do not establish validation, source
  authorization, Knowledge Vault authority, or pilot readiness.
- JCS remains deferred and is not a dependency of this decision.

### Reported facts

- The VBA demonstration content in open pull request #44 is described there as
  public organizational evidence. This ADR does not verify its accuracy,
  currency, rights, classification, validation, or authorization for
  acquisition or use.

### Working assumptions

- `Jebediah Knowledge Vault` is a useful stable label for the proposed
  knowledge-layer responsibility.
- Future approved consumers will need source-linked derived representations
  without transferring source authority into a retrieval repository.
- The boundary can be specified independently from schemas, APIs, storage,
  deployment, and runtime implementation.

### Open questions

- Which concrete information domains may a future Knowledge Vault contain?
- Who will own the component and its future operation?
- Which producers and consumers will be approved?
- Which external information may be acquired or used?
- Which validation, classification, freshness, retention, deletion, and
  recovery requirements apply to each information domain?
- How will the Knowledge Vault relate to the Memory Service, Knowledge Graph,
  and future reasoning components?

These questions do not prevent this decision because the ADR defines an
authority boundary and keeps implementation and external information use
blocked until later approvals resolve them.

## Problem Statement

Project Jebediah needs a governed boundary from which approved consumers may
retrieve source-linked knowledge without:

- Creating a competing source of canonical project records
- Promoting a derived representation into source truth
- Treating model output, curation, or vector similarity as verification
- Conflating retrieval persistence with information ownership
- Allowing VBA demonstration materials to define permanent architecture
- Allowing implementation convenience to assign authority
- Exposing unapproved external information to transformation, retrieval, or
  publication
- Reopening or assigning a responsibility to deferred JCS

The architecture must define what future consumers may rely on while preserving
the authority, provenance, uncertainty, and lifecycle of underlying
information.

## Scope

This decision governs:

- The conceptual responsibility of the Jebediah Knowledge Vault
- Its authority relationship with canonical project records and originating
  sources
- The meaning of a derived representation
- Ownership boundaries among the repository, sources, Vault, demonstration
  materials, and future runtime systems
- The conceptual quarantine, evaluation, transformation, and retrieval flow
- Required provenance and lifecycle responsibilities
- Failure behavior and future decision gates

## Definitions

### Derived representation

A **derived representation** is an information artifact produced from one or
more source records by a documented transformation for a bounded knowledge use.
Transformations may include selection, normalization, segmentation,
annotation, aggregation, summarization, embedding, classification, indexing,
or correlation.

A derived representation retains sufficient provenance to identify its source
inputs and transformation context. It is not authoritative for the underlying
source facts merely because it is reviewed, curated, durable, validated for
shape, indexed, embedded, or retrieved.

An unchanged source mirror is cached information under Project Jebediah's data
ownership model, not a derived representation. Model output is derived or
temporary information unless a separately approved process creates a different
governed record.

### Canonical project records

**Canonical project records** are the reviewed repository artifacts assigned to
own Project Jebediah governance, architecture, accepted decisions, plans,
current status, standards, and other maintained project evidence within their
defined subjects.

This authority is scoped. Canonical project records do not become authoritative
for external organizational facts, source content, or live runtime state merely
because those subjects are described in the repository.

### Quarantined candidate information

**Quarantined candidate information** is untrusted, non-authoritative, and
non-consumable input awaiting an admissibility evaluation. It is temporary
information unless a separate accepted contract assigns another category.

## Decision Drivers

- Preserve one explicit authority for each information subject and scope.
- Keep canonical project records separate from runtime and external facts.
- Preserve originating-source authority.
- Make provenance, freshness, uncertainty, and conflict visible.
- Prevent curation, retrieval, or model behavior from establishing truth.
- Keep information authority separate from action authority.
- Permit future implementation choices without allowing them to redefine the
  conceptual boundary.
- Fail closed when authorization, classification, provenance, or admissibility
  cannot be established.
- Preserve local-first recoverability and future replaceability.

## Alternatives Considered

### Alternative 1: Derived governed knowledge repository

The Knowledge Vault contains governed derived representations linked to
authoritative sources. Its transformations, summaries, embeddings, indexes,
classifications, and retrieval signals remain derived.

This alternative:

- Preserves existing information-authority principles.
- Avoids creating a competing source of truth.
- Supports invalidation, rebuilding, and technology replacement.
- Keeps source corrections and deletion authoritative.
- Limits the consequence of incorrect transformation or model output.
- Requires consumers to interpret provenance, freshness, conflict, and
  uncertainty.

### Alternative 2: Independent knowledge authority

The Knowledge Vault becomes authoritative for selected information after
ingestion, validation, or curation.

This alternative could give consumers one normalized authority, but it would:

- Create competing authority with originating sources.
- Require domain-specific write and correction authority.
- Require stronger conflict, retention, deletion, migration, backup, and
  restoration guarantees.
- Increase the consequence of incorrect ingestion, curation, or
  transformation.
- Require reconciliation or controlled write-back to originating systems.
- Expand security, privacy, audit, and operational obligations.
- Risk treating model-generated or semantically retrieved content as truth.

No concrete information domain, authority transfer, or operational evidence
justifies those consequences.

### Alternative 3: No distinct Knowledge Vault boundary

Project Jebediah could continue using only existing Memory Service and retrieval
terminology.

This alternative avoids another named component, but it leaves the Knowledge
Vault undefined, gives future consumers no governed knowledge boundary, and
allows the Memory Service or its persistence technology to acquire authority by
implementation convenience.

## Decision Rationale

Alternative 1 is selected because it is the smallest architecture consistent
with current Project Jebediah principles:

- Authority remains assigned to an explicit owner.
- Derived representations remain distinguishable from their sources.
- Provenance and uncertainty remain visible.
- Retrieval does not establish truth.
- Components receive bounded responsibilities.
- Durable knowledge remains recoverable without depending on conversation
  history.
- Information authority and action authority remain separate.

Alternative 2 is rejected because the project has no approved information
domain, write authority, conflict policy, correction process, or operational
evidence that would justify transferring source authority to the Vault.

Alternative 3 is rejected because leaving the term undefined would allow future
implementation choices to establish authority and responsibility without an
accepted architecture decision.

## Authority Model

| Information | Authority |
| --- | --- |
| Canonical project records, including governance, architecture, accepted decisions, plans, current status, and reviewed project evidence | Reviewed GitHub `main` and the canonical owner for each subject |
| Source-domain facts | The approved originating source for its defined subject and scope |
| Quarantined candidate information | Non-authoritative and non-consumable pending evaluation; retained only under an approved temporary-information policy |
| Unchanged source mirrors | Cached information governed by the originating source's authority and freshness |
| Vault records produced by transformation | Derived representations governed by the Vault contract |
| Embeddings, indexes, summaries, classifications, confidence signals, and retrieval scores | Derived information |
| VBA demonstration scripts, prompts, and fixtures | Demonstration material only |
| Runtime health and execution evidence | The owning runtime component within its approved operational scope |
| Model output | Derived or temporary information unless a separately approved process creates another governed record |

Evaluation determines admissibility and policy conformance. It does not verify
the truth of a source claim or transfer source authority to the Knowledge Vault.

A Vault representation may authoritatively record only that its governed
process accepted and transformed specified input. That operational fact does
not make the represented source claim true.

The authority hierarchy is:

1. Reviewed GitHub `main` for canonical project records within each canonical
   owner's subject.
2. Approved original authoritative sources for facts within their defined
   domains.
3. The Knowledge Vault for governed derived representations and their
   provenance, not the represented source facts.
4. Runtime systems for execution state and operational outputs within their
   approved scopes.

This ordering does not broaden any authority scope. A lower layer cannot
override a higher layer, and canonical project-record authority does not make
GitHub authoritative for external source facts or live runtime state.

## Ownership Boundaries

### Project Jebediah repository

The repository owns canonical project records within the subject assigned to
each canonical document or accepted decision record, including:

- Project governance and standards
- Current architecture
- Accepted decisions and their rationale
- Planning and current project status
- Reviewed source and configuration intent
- Review and acceptance evidence

Canonical project-record authority is scoped. It does not make the repository
authoritative for external organizational facts, live runtime state, or source
content merely because those subjects are described in documentation.

### Originating sources

Approved originating sources retain responsibility for:

- Facts and records within their defined authority
- Corrections to those facts
- Source revision and publication state
- Source-specific access and authorization

### Jebediah Knowledge Vault

The Knowledge Vault owns:

- Governance of accepted derived representations
- Preservation of source linkage and transformation context
- Exposure of provenance, freshness, uncertainty, conflict, and limitations
- Invalidation, reconciliation, deletion propagation, rebuild, and retirement
  requirements
- Consumer guarantees established by a future accepted specification

The Knowledge Vault does not own:

- Canonical project-record authority
- Source-domain truth
- Source authorization
- Autonomous verification
- Action authorization
- Source correction
- General runtime orchestration
- Reasoning conclusions
- Knowledge Graph identity or relationship semantics unless separately
  approved

### VBA demonstration materials

VBA demonstration materials may own presentation flow, prompts, bounded
fixtures, expected demonstration outcomes, and operator guidance. They do not
define Knowledge Vault authority, project architecture, source truth, or
production readiness. Their evidence validation remains pending, and no live
organizational pilot is authorized.

### Future runtime systems

Future runtime systems own only their approved execution, health,
configuration, failure, and recovery responsibilities. They may consume Vault
representations only according to documented provenance, freshness,
classification, uncertainty, and failure guarantees.

## Data Flow Boundaries

The approved conceptual flow is:

```text
Approved originating source
    -> separately authorized acquisition, collection, or submission
    -> quarantine boundary
    -> admissibility evaluation
       - source authorization
       - purpose and approved consumer
       - provenance sufficiency
       - classification and permitted use
       - integrity and bounded format
       - retention and deletion requirements
    -> accept, reject, or hold for explicit review
    -> documented transformation
    -> governed derived Vault representation
    -> bounded retrieval
    -> approved consumer
```

This flow defines responsibilities, not an API, schema, service, storage
technology, or deployment topology.

The following boundaries apply:

- Source information may enter only after separate source and use
  authorization.
- Quarantined information is untrusted, non-authoritative, and unavailable to
  ordinary Vault retrieval consumers.
- Evaluation establishes whether information may enter a specific governed
  processing path. It does not determine that the information is true.
- Rejected information must not produce a Vault representation.
- Information held for review remains temporary and requires an owner, access
  boundary, retention limit, and cleanup condition.
- Only accepted inputs may cross into a documented transformation boundary.
- Successful evaluation does not transfer authority from the originating
  source.
- Transformations produce derived representations and retain their relationship
  to their inputs.
- Retrieval returns governed evidence and context, not authoritative
  conclusions.
- Consumers must not infer freshness, verification, or authority from
  successful retrieval.
- Consumer output does not write to a source or the Vault without separate
  authority.
- Runtime observations must not become canonical project records without
  promotion through the normal repository review and evidence-classification
  process.

## Provenance Requirements

Every decision-relevant derived representation must identify, as applicable:

- Originating source
- Stable source identity
- Source revision, version, or observation context
- Observation and processing times
- Submitting producer
- Quarantine receipt identity
- Evaluation disposition
- Evaluation policy or criteria version
- Admission decision and accountable owner or process
- Transformation identity and version
- Relationship to supporting evidence
- Information classification
- Verification or review state
- Freshness and expiration information
- Known uncertainty or conflict
- Derived representation identity
- Conditions requiring invalidation or recomputation

Provenance begins at quarantine receipt and remains connected through
evaluation, transformation, Vault representation, and retrieval.

Missing provenance must remain visible and must not be replaced with inferred
certainty. Evaluation evidence records admissibility; it must not be presented
as verification of source truth.

A citation alone is insufficient when cited content can change without a
retained version or observation context.

## Lifecycle Responsibilities

The Knowledge Vault boundary requires owned lifecycle rules for:

- Quarantine
- Evaluation
- Rejection
- Quarantine cleanup
- Admission
- Transformation
- Review
- Availability to consumers
- Freshness evaluation
- Invalidation
- Reconciliation
- Supersession
- Deletion propagation
- Reclassification
- Rebuilding
- Migration
- Recovery
- Retirement

Quarantined candidate information is temporary unless a separate accepted
contract assigns another category. Its lifecycle must define access, maximum
retention, review ownership, rejection evidence, and cleanup after success,
rejection, timeout, or failure.

A future specification must distinguish:

- Removing a derived representation
- Correcting an authoritative source
- Recording an annotation or dispute
- Recomputing a derived representation
- Rebuilding an index
- Retiring a transformation or consumer contract

Restoration must not silently revive deleted, expired, superseded,
unauthorized, rejected, or invalidated information.

## Failure Modes

The architecture must account for:

- External source use was not separately authorized.
- Source identity is missing or ambiguous.
- Source content changed.
- Quarantine was bypassed.
- Quarantined information became retrievable.
- Evaluation was incomplete, unavailable, or used an unknown policy version.
- Evaluation success was misrepresented as factual verification.
- Authorization, classification, provenance, or permitted use is unresolved.
- Rejected or expired quarantined content was retained or transformed.
- Transformation failed or used an unknown identity.
- Source observations conflict.
- A derived representation is stale or expired.
- Correction or deletion did not propagate.
- A consumer cannot interpret uncertainty or conflict.
- Retrieval is unavailable or returns irrelevant evidence.
- Model output contradicts retrieved evidence.
- Derived content is presented as authoritative.
- Demonstration data is mistaken for approved production knowledge.
- Vault state conflicts with canonical project records.
- Recovery restores invalid, rejected, expired, or unauthorized content.

Authorization failure, unknown classification, missing provenance, or failed
evaluation must stop admission. Failure must remain visible to affected
consumers. The Knowledge Vault must not produce success-shaped output when
required authority, provenance, classification, or validity cannot be
established.

## Consequences

### Positive

- The Knowledge Vault receives one coherent architectural responsibility.
- Canonical project records and source authority remain protected.
- Retrieval and future reasoning gain a governed evidence boundary.
- Storage, indexing, and model technologies remain replaceable.
- VBA demonstration material remains bounded.
- Provenance, freshness, uncertainty, quarantine, evaluation, and lifecycle
  become required architectural concerns.
- Incorrect or stale derived representations can be invalidated without
  rewriting source authority.

### Negative

- Consumers must handle missing, stale, conflicting, rejected, or uncertain
  information.
- Candidate information requires quarantine and evaluation before admission.
- Derived representations require more governance metadata than an unqualified
  document store.
- Correction and deletion require propagation across derivatives.
- Some information cannot be admitted when its authorization, source,
  classification, or provenance is inadequate.
- Rebuild and recovery planning become mandatory before operational acceptance.

### Neutral

- This decision does not select a storage system or retrieval technology.
- The existing Memory Service may later participate in a Knowledge Vault
  implementation, but this ADR does not make them identical.
- Qdrant may remain an implementation candidate without becoming a knowledge
  authority.
- The Knowledge Vault may later interact with a Knowledge Graph or Reasoning
  Engine, but their responsibilities remain separate.
- JCS remains deferred and is not a dependency of this decision.

## Non-Goals

This ADR does not:

- Define schemas
- Define APIs or protocols
- Select storage or indexing technology
- Select a model or embedding technology
- Define deployment topology
- Authorize runtime implementation
- Authorize live-data migration
- Assign responsibilities to JCS
- Define Knowledge Graph identity or relationship semantics
- Define automated verification
- Define reasoning behavior
- Grant action authority
- Approve VBA demonstration readiness
- Authorize a live organizational pilot
- Make the Knowledge Vault authoritative for source-domain facts

This ADR does not authorize the acquisition, collection, ingestion, retention,
transformation, model exposure, publication, retrieval, or other use of any
external information. Each external source and information domain requires
separate approval of purpose, authority, permitted use, classification,
producers, consumers, provenance, retention, deletion, security, and applicable
legal or consent constraints before its information may enter the quarantine
boundary.

## Implementation Constraints

Any future Knowledge Vault proposal must:

- Follow this derived-authority boundary.
- Identify approved producers and consumers.
- Map concrete information through Project Jebediah's data-ownership model.
- Preserve source identity and provenance.
- Represent freshness, uncertainty, conflict, and invalidation.
- Separate original source content, cached mirrors, and derived
  representations.
- Define quarantine, admissibility evaluation, rejection, and cleanup
  responsibilities.
- Define correction and deletion propagation.
- Define rebuild, migration, recovery, and retirement expectations.
- Treat external content and model output as untrusted.
- Prevent retrieval success from being interpreted as verification.
- Prevent information authority from granting action authority.
- Use synthetic or separately approved information for public tests and
  demonstrations.
- Receive separate architecture approval before implementation begins.

No implementation may accept external information solely because this ADR is
accepted. Every future source adapter or submission path must prove separate
source and use authorization before reaching quarantine. The quarantine and
evaluation boundary must be defined and testable before ordinary Vault
admission or retrieval is implemented.

A future implementation must not silently identify the Knowledge Vault with the
Memory Service, Qdrant, a Knowledge Graph, a document directory, or a model
context window.

## Security and Privacy Impact

This decision introduces a conceptual trust boundary around candidate
information:

- External and submitted information remains untrusted.
- Unknown classification defaults to no admission or use.
- Quarantined information must not be available to ordinary consumers.
- Evaluation must address authorization, purpose, classification, permitted
  use, provenance, retention, and deletion before admission.
- Sensitive evidence must not enter public canonical project records.
- Model exposure requires separate approval based on source classification and
  permitted use.

This ADR defines obligations but does not approve an information source, access
model, security mechanism, or privacy treatment.

## Operations and Recovery Impact

No operational component or deployment is approved.

A future operational proposal must identify:

- Ownership of quarantine, evaluation, transformation, retrieval, and recovery
- Health and degraded-state semantics
- Cleanup of rejected and expired candidate information
- Rebuild inputs and transformation identities
- Invalidation and deletion propagation
- Backup, restoration, migration, and retirement expectations appropriate to
  each information category

Operational evidence is required before the Knowledge Vault can advance to
**Operational** maturity.

## Compatibility and Migration

No existing service, database, collection, demo fixture, backup, or runtime
record is declared a Knowledge Vault artifact by this ADR.

Existing Memory Service or Qdrant content must not be relabeled, migrated, or
treated as conformant without a separate inventory, authority mapping,
provenance assessment, compatibility decision, and migration plan. Payload
readability or vector compatibility does not establish compliance with this
authority model.

Because no accepted Knowledge Vault implementation or consumer contract exists,
this ADR creates no runtime compatibility obligation.

## Validation

This decision is ready for acceptance when review confirms:

- `canonical project records` is used consistently and remains scoped to each
  canonical owner.
- `derived representation` has one clear meaning.
- Unchanged source mirrors remain cached rather than being mislabeled as
  derived.
- Status remains Proposed and maturity remains Named until acceptance.
- The proposed Specified transition cannot be read as implementation,
  migration, deployment, operational, or external-use readiness.
- The conceptual flow includes source authorization, quarantine, evaluation,
  accept/reject/hold disposition, transformation, retrieval, and an approved
  consumer.
- Quarantined information is unavailable to ordinary retrieval consumers.
- Evaluation establishes admissibility, not factual verification.
- Unknown authorization, classification, provenance, or evaluation fails
  closed before admission.
- No wording authorizes acquisition, ingestion, retention, transformation,
  model exposure, retrieval, or publication of external information.
- Canonical project records, sources, the Knowledge Vault, demonstration
  materials, and runtime systems retain distinct authority scopes.
- VBA demonstration evidence remains pending, and no live organizational pilot
  is authorized.
- Information authority remains separate from action authority.
- JCS remains deferred.
- No schema, API, storage, model, deployment, migration, or runtime
  implementation is selected.
- The complete exact artifact receives independent Work Mode review and the
  Chief Architect's final decision under the Project Coordination Protocol.

Reconsideration is required if a later proposal would:

- Transfer source authority into the Knowledge Vault
- Make the Knowledge Vault authoritative for canonical project records
- Grant action authority based on Vault content
- Bypass quarantine or admissibility evaluation
- Make a technology product define the Vault boundary
- Establish guarantees that cannot be tested or owned

## Future ADR Dependencies

Separate ADRs may be required for:

- Source authorization and external-information use
- Quarantine and evaluation policy when it establishes a lasting
  cross-component boundary
- Verification authority beyond admissibility evaluation
- Public or cross-component Knowledge Vault interfaces
- Concrete information domains and authority mappings
- Permanent storage and indexing architecture
- Knowledge Graph relationship
- Memory Service relationship
- Identity and deduplication rules
- Conflict and reconciliation strategy
- Retention and deletion policy
- Security classification and access control
- Model and transformation identity
- Deployment and operational ownership
- Backup, restoration, migration, and disaster recovery
- Automated action based on Vault information
- Any transfer of authority from an originating source to the Knowledge Vault

Dependent implementation must wait for the relevant decisions and
specifications to be accepted.

## Related Documents

- [Project Jebediah Architecture](../ARCHITECTURE.md)
- [Architecture Principles](../ARCHITECTURE_PRINCIPLES.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [AI Memory Contract](../AI_MEMORY_CONTRACT.md)
- [Component Registry](../reference/COMPONENT_REGISTRY.md)
- [Glossary](../reference/GLOSSARY.md)
- [Security Policy](../../SECURITY.md)
- [Operations Philosophy](../OPERATIONS_PHILOSOPHY.md)
- [Testing Philosophy](../TESTING_PHILOSOPHY.md)
- [ADR Process](README.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review Record

The Chief Architect implementation directive authorized preparation of this
Proposed artifact. Independent Work Mode review, formal Chief Architect
exact-head decision, any required project-maintainer repository action, merge,
and post-merge read-back remain pending.
