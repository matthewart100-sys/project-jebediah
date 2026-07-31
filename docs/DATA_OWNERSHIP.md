# Data Ownership

**Status:** Active

## Purpose

This document defines how Project Jebediah classifies and governs information
before JCS, collectors, knowledge components, the Digital Twin, automation, or
reasoning are designed. It prevents a cache, model output, vector index,
workflow state, or convenient copy from becoming an accidental source of
truth.

This document owns project-wide information categories and ownership
responsibilities. The [current architecture](ARCHITECTURE.md) owns component
boundaries, and future component specifications will map concrete information
to these categories.

## Scope and non-goals

This policy covers future runtime information and existing engineering memory.
It does not:

- Select a database, schema, serialization, protocol, or storage location
- Define JCS responsibilities
- Verify the reported Qdrant, n8n, Ollama, or home-lab state
- Classify data that has not been inventoried
- Grant a component permission to collect, retain, transform, or act on data
- Replace the future security policy or private threat model

## Evidence and uncertainty

### Verified facts

- Reviewed GitHub `main` is authoritative for Project Jebediah engineering
  memory.
- The repository contains no application schemas, runtime databases,
  collectors, tracked workflow exports, or application data.
- No runtime component currently has approved data authority.

### Reported facts

Bootstrap materials report n8n, Qdrant, and Ollama in a local environment. No
repository evidence verifies their contents, persistence, configuration,
retention, backups, consumers, or current operation.

### Working assumptions

- Future capabilities will use information from sources with different
  authority, freshness, and sensitivity.
- Some information will be copied, transformed, indexed, summarized, or
  inferred.
- Local-first operation will require explicit recovery and reconciliation
  rather than implicit dependence on one machine's current state.

### Open questions

| Question | Why it matters | Resolution gate |
| --- | --- | --- |
| Which source is authoritative for each future information item? | Conflicts and writes cannot be handled safely without one owner. | JCS and component specifications |
| Which data classifications and consent rules apply? | Collection, model access, retention, and public documentation depend on them. | Security policy and source authorization |
| Which runtime information must survive host loss? | Storage, backup, and recovery design depend on durability needs. | Component operations specification |
| Which derived results may influence actions? | Confidence, validation, and human approval depend on consequence. | Automation and Reasoning Engine decisions |
| Which reported stores contain existing data? | Migration and disclosure risks cannot be assessed otherwise. | Sanitized infrastructure and data inventory |

## Core categories

Every durable or decision-relevant information item has exactly one primary
category in a given context. Different representations of the same subject may
have different categories.

### Authoritative information

Authoritative information is the approved source used to resolve conflict for
its defined subject and scope.

It must identify:

- The information owner
- What facts or decisions it is authoritative for
- How writes are authorized and validated
- Version, concurrency, and conflict behavior
- Durability, backup, restore, migration, and deletion expectations
- Consumers that must reconcile when it changes

Authority is specific. A system authoritative for account identity is not
automatically authoritative for device health, semantic relationships, or an
AI summary about that account.

### Cached information

Cached information is a replaceable copy of authoritative information kept to
improve access, availability, or performance.

It must identify:

- The authoritative source
- Cache key and scope
- Freshness, expiration, and invalidation behavior
- Stale-read policy
- Rebuild path
- Behavior when the source is unavailable

A cache must not accept an independent write that bypasses its authoritative
source. Loss of a cache may reduce performance or availability but must not
destroy unique project truth.

### Derived information

Derived information is produced from one or more inputs through a
transformation, aggregation, inference, embedding, classification, or
calculation.

It must identify:

- Source provenance and source versions
- Transformation, model, prompt, or rule version
- Production time and relevant effective time
- Confidence, uncertainty, or quality limits where applicable
- Recompute and invalidation behavior
- Whether human validation changes its status or creates a separate
  authoritative record

Derived information does not become authoritative merely because it is
expensive to reproduce, stored durably, or produced by an advanced model.

### Temporary information

Temporary information exists for bounded processing and is not intended to
become durable authority.

It must identify:

- Purpose and lifetime
- Process or task owner
- Maximum retention or cleanup condition
- Sensitivity and access boundary
- Failure cleanup behavior
- Whether any safe summary or result must be promoted elsewhere

Temporary information includes local scratch data, intermediate files,
short-lived queues, and conversational context when no reviewed process
promotes it.

## Category is contextual

The category applies to an information representation in a named scope, not to
a product.

Examples:

- A source document may be authoritative for its own authored content.
- Extracted text is derived from that document.
- A search index entry is derived, even when stored in a database.
- A fetched copy is cached when it is intended to mirror the source.
- A reviewed correction may become authoritative only when written through
  the approved owner.

Qdrant, a relational database, GitHub, a file, or a model can hold different
categories. Storage technology does not determine authority.

## Ownership roles

### Information owner

Accountable for meaning, authority, permitted use, quality expectations,
conflict policy, retention, and deletion. This owner approves category changes.

### Component owner

Accountable for the component that stores, processes, or serves the
information, including its interfaces, failure behavior, security, operations,
and recovery. Component ownership is tracked in the
[Component Registry](reference/COMPONENT_REGISTRY.md).

### Custodian or operator

Maintains an approved runtime environment and executes backup, restore,
monitoring, access, and incident procedures. Custody does not grant authority
to reinterpret data.

### Producer

Creates or supplies information under an approved contract. The producer
records provenance and does not overstate quality or authority.

### Consumer

Uses information under documented freshness, classification, and failure
expectations. A consumer does not treat a convenient copy as authoritative.

One role may perform several responsibilities in a small project, but the
responsibilities remain explicit so they can separate safely later.

## Required ownership record

Before a component persists or makes decisions from an information item, its
specification records:

| Field | Required meaning |
| --- | --- |
| Name and subject | What the information represents |
| Primary category | Authoritative, cached, derived, or temporary |
| Information owner | Who resolves meaning, authority, and conflict |
| Component and custodian | Who stores, serves, operates, and recovers it |
| Producers and consumers | Approved origins and uses |
| Provenance | Source identity and transformation history |
| Time semantics | Observed, effective, processed, updated, and expiration times as applicable |
| Freshness | How staleness is measured, exposed, and handled |
| Classification | Sensitivity, access, consent, and disclosure constraints |
| Validation | Required shape, identity, integrity, and quality checks |
| Conflict policy | How competing observations or writes are reconciled |
| Retention and deletion | Duration, legal or project reason, and propagation |
| Recovery | Backup, restore, rebuild, reconciliation, and data-loss tolerance |
| Change policy | Compatibility, migration, and category-transition approval |

The record may live in a component or data specification and link here rather
than duplicate this policy.

## Provenance and identity

- Preserve stable source identity when later decisions depend on origin.
- Record transformations from input to derived output.
- Do not merge records solely because names look similar.
- Distinguish a source's identifier from Project Jebediah's future internal
  identity.
- Identify manual corrections, their reviewer, and their relationship to the
  original observation without exposing personal data publicly.
- Keep confidence and uncertainty separate from identity.
- A citation or link is not sufficient provenance when content can change
  without a version or observation time.

Entity identity and deduplication rules remain future subsystem decisions.

## Time, freshness, and stale state

Time-dependent information distinguishes when practical:

- **Observed time:** when a source reported or a collector observed a value
- **Effective time:** when the represented fact applies in its domain
- **Processed time:** when Project Jebediah handled it
- **Updated time:** when the current representation changed
- **Expiration time:** when it must no longer be treated as fresh

Consumers must know whether stale data is usable, degraded, or unsafe. Missing
freshness metadata is not equivalent to fresh. Clock source and timezone
assumptions become explicit in component contracts.

## Conflict and reconciliation

- One authoritative owner resolves each defined conflict domain.
- Last-write-wins is prohibited as an unstated default.
- Competing observations remain distinguishable until an approved rule
  reconciles them.
- Automated reconciliation records the rule and inputs.
- Manual reconciliation records the decision safely and preserves audit
  history.
- Cached and derived stores reconcile from their sources; they do not silently
  overwrite authority.
- Partial reconciliation and unresolved conflict remain visible to consumers.

## Ingestion and transformation

Before accepting source information:

- Confirm authorization and intended use.
- Validate identity, format, size, integrity, classification, and required
  fields.
- Record provenance and time semantics.
- Define duplicate, replay, retry, and partial-failure behavior.
- Quarantine or reject unsafe input without contaminating authoritative state.

Every transformation identifies its input set and versioned behavior when
reproduction matters. A changed transformation invalidates or migrates
dependent derived information deliberately.

## AI, embeddings, and vector indexes

- Model output is derived or temporary unless a reviewed human or system
  process creates a separate authoritative record.
- Prompts and model context may contain sensitive information and follow the
  same classification and retention rules as their sources.
- Embeddings are derived representations. They retain links to source identity,
  source version, embedding model/version, and creation time.
- Vector indexes are search aids, not implicit authoritative stores.
- Chunking, summarization, classification, and entity extraction record their
  transformation versions and quality limits.
- A model's confidence statement is not evidence of correctness.
- Deleted or reclassified source data must have an owned propagation path to
  prompts, caches, embeddings, indexes, and other derivatives.

## Automation and action

Information authority and action authority are separate.

- An authoritative fact does not automatically authorize an action.
- Derived or stale information that influences an action requires a documented
  risk boundary and validation.
- Sensitive or irreversible actions require human approval unless an accepted
  ADR defines a narrower safe automated boundary.
- Actions record the policy, input versions, approval, result, and partial
  failure needed for audit and recovery.
- A future Digital Twin may inform action but is not an autonomous control
  plane by default.

## Retention, deletion, and category changes

- Retain information only for an approved purpose and duration.
- Deletion propagates to caches and derivatives according to owned procedures.
- Backups document deletion limitations and restoration safeguards.
- A category change requires information-owner review, affected-consumer
  analysis, migration, and documentation.
- Temporary information promoted to durable storage receives a category,
  owner, provenance, classification, and retention rule before promotion.
- Derived information becomes authoritative only through an explicit decision
  that identifies its validation and conflict behavior.

## Security and privacy

- Minimize collection, access, retention, replication, and model exposure.
- Apply least privilege to producers, consumers, components, operators, and
  automation.
- Keep secrets and credentials separate from ordinary information stores.
- Treat source content and model output as untrusted.
- Public documentation records sanitized policy and conclusions, not personal
  data, raw private logs, prompts, addresses, or exploitable topology.
- Unknown classification defaults to no collection or use until resolved.

The future `SECURITY.md` may strengthen these requirements.

## Durability and recovery

Durability follows category and consequence:

- Authoritative information requires owned backup, restore, integrity, and
  recovery-point expectations.
- Cached information requires a tested rebuild or refetch path.
- Derived information requires either reproducible inputs and transformations
  or an explicit reason it must be backed up.
- Temporary information requires safe cleanup and no unique durable value.

Restoration must not silently revive deleted, expired, superseded, or
unauthorized information. Reconciliation after restore is part of recovery.

## Current baseline mapping

| Information | Category and authority | Current owner | Limitation |
| --- | --- | --- | --- |
| Reviewed project documentation on GitHub `main` | Authoritative engineering memory within each canonical document's subject | Maintainer | Does not own future runtime facts merely because they are documented |
| Accepted ADRs | Authoritative decision history for their scoped choice | Decision owner and maintainer | No numbered ADR exists yet |
| Sprint and roadmap | Authoritative plan for their planning scope | Maintainer | Plans do not prove implementation |
| Pull requests and Git history | Durable review and change history | Maintainer | Superseded content is history, not current architecture |
| Bootstrap environment claims | Reported information | No runtime information owner verified | Requires sanitized audit |
| Chats and model context | Temporary working context unless promoted | Active participant for safe handling | Not authoritative project memory |
| Future runtime records, caches, indexes, embeddings, and inferences | Unassigned | Unassigned pending specification | Collection or persistence is not approved |

## Decision and review requirements

A Foundational or System ADR is required to:

- Assign authority for a major information domain
- Move authority between components
- Make a derived representation authoritative
- Approve a cross-system conflict or consistency model
- Establish material retention, deletion, identity, or provenance behavior
- Grant automated action based on information whose uncertainty matters

Routine mappings inside an already approved component contract may use normal
review unless their consequence triggers the
[ADR Process](adr/README.md).

## Maintenance

Update this document when project-wide categories or responsibilities change.
Update component specifications and the registry when concrete ownership is
assigned. An implementation must not silently establish data authority before
the corresponding documentation and review.
