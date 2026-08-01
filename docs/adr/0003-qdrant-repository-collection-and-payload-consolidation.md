# ADR 0003: Qdrant Repository, Collection, and Payload Consolidation

**Status:** Accepted

**Decision level:** System

**Date:** 2026-07-31

**Decision owner:** Project maintainer

**Reviewers:** Chief Architect and project maintainer

## Decision summary

Sprint 005 selects Qdrant architecture option A. Until a separate durable
record store is approved, one Qdrant collection temporarily serves both as the
Memory Service's durable operational record of accepted memories and as its
semantic search index. The canonical root adapter owns both roles; the source
that originated a claim remains authoritative for that claim's truth.

## Context

The repository has no implemented durable `MemoryRepository` other than
Qdrant. The pipeline's in-memory repository is a test/reference
implementation and cannot survive process loss. The service nevertheless
reports accepted memories as stored after writing them to Qdrant.

Three incompatible Qdrant paths currently exist. Consolidation requires an
explicit decision about durable record authority, write success, consistency,
failure, and recovery. Treating Qdrant as a derived index while no other
durable record store exists would leave successful storage without an
authoritative operational record.

### Verified facts

- The root Qdrant repository creates a one-dimensional collection, stores
  importance as the vector, uses the application memory ID as the point ID,
  omits payload `memory_id`, and does not search semantically.
- The service-local Qdrant repository creates a 768-dimensional collection,
  stores a zero vector, uses a random point UUID, stores `memory_id` in the
  payload, and does not search semantically.
- `services/jebediah-memory/app/main.py` writes actual 768-dimensional Ollama
  embeddings with random point UUIDs and application IDs in payloads, then
  calls Qdrant directly for semantic search.
- The current pipeline defaults to an in-memory repository before the API
  performs a separate Qdrant write.
- Qdrant points store a vector and payload together in a single point upsert.
- Sprint 004 payloads contain additive provenance and lifecycle objects.
- Repository tests use isolated clients and do not verify a live collection.

### Reported facts

- Project materials report a local Qdrant service.
- Its collection schema, point count, payload variants, persistence, backup,
  health, and current consumers are unverified.

### Working assumptions

- The FastAPI path is the runtime compatibility target.
- The default collection name remains `jebediah_memory`.
- Sprint 005 can consolidate source code without changing live points or
  deploying the result.
- A single-point Qdrant upsert is the only durable write required for an
  accepted memory during this temporary architecture.

### Open questions

- A sanitized live collection inventory remains required before deployment.
  This is an operational gate, not an unresolved source-architecture choice.
- Backup retention and operator ownership require a later operations
  specification before the service can claim production durability.

## Scope

This decision governs:

- Qdrant's temporary dual role
- The source of truth for accepted Memory Service records
- The canonical repository and search boundary
- Collection geometry and compatibility checks
- Payload schema and point identity
- Write-success and failure semantics
- Consistency and recovery expectations
- Separation of payload compatibility from vector-geometry migration

## Non-goals

- Declaring stored claims true or verified
- Introducing a second database or distributed transaction
- Redesigning memory identity or request idempotency
- Migrating, backfilling, deleting, or re-embedding live points
- Adding lifecycle automation or intelligent reranking
- Establishing production backup retention or service-level objectives

## Decision drivers

- One durable write path and one semantic search path
- Honest `stored` success behavior
- No dual-write inconsistency or distributed transaction
- Preserve current API and application memory IDs
- Preserve Sprint 004 governance payloads and legacy defaults
- Fail safely on incompatible collection geometry
- Make later separation into record store and index possible

## Considered alternatives

### Option A: Qdrant is temporarily both durable record store and semantic index

This matches the only currently implemented durable runtime write. A Qdrant
point contains the accepted memory payload and its derived vector. One
acknowledged point upsert can therefore establish both operational record
durability and search availability without a distributed transaction.

### Option B: A separate canonical record store is authoritative and Qdrant is derived only

This is a valid future target, but no such durable record store is currently
implemented or approved. Adding one would expand Sprint 005 from
consolidation into a persistence feature and introduce dual-write consistency,
recovery, and migration work.

### Keep the three existing Qdrant paths

This leaves incompatible dimensions, placeholder vectors, payload schemas,
identities, and search behavior under different owners.

### Create and migrate to a new collection during Sprint 005

This would require verified live-data inventory, source-content authority,
backup, re-embedding, cutover, and rollback. Those operations are outside the
source-only consolidation scope.

### Retain the current design

The API would continue to report storage through direct Qdrant calls while the
domain pipeline separately writes to volatile memory. Neither repository
adapter would match the actual semantic runtime.

## Decision

### Temporary source of truth

Option A is selected.

For the duration of this architecture, the Qdrant point payload is the
authoritative operational record of what the Memory Service accepted and
durably stored. The point vector is a derived search representation attached
to that record.

This authority is deliberately narrow:

- Qdrant is authoritative for the Memory Service record and its stored
  governance metadata.
- The originating source remains authoritative for the truth or meaning of
  the represented claim.
- Vector similarity, confidence, lifecycle, and verification metadata do not
  acquire truth authority from durable storage.
- GitHub remains authoritative for engineering architecture and configuration
  intent, not runtime memory contents.

A future ADR may select option B and separate the authoritative record store
from the semantic index. Sprint 005 does not anticipate that migration.

### Canonical adapter and contracts

`src/collector/memory/persistence/qdrant_repository.py` becomes the sole
Qdrant implementation. Its current one-dimensional behavior is replaced only
after this ADR is accepted.

The adapter may expose a combined `QdrantMemoryRepository` or implement both
canonical interfaces, but it must provide one implementation and one client
path for:

```text
save or index(memory, vector, embedding_identity) -> memory_id
find(memory_id) -> MemoryItem | None
contains(memory_id) -> bool
search(query_vector, embedding_identity, limit) -> RetrievalCandidate sequence
```

The adapter owns collection inspection, point identity, vector validation,
payload conversion, legacy reading, Qdrant error translation, and candidate
mapping. FastAPI must not construct Qdrant points, filters, collection schemas,
or queries.

### Collection contract

| Property | Required value |
| --- | --- |
| Collection name | Configurable; default `jebediah_memory` |
| Vector kind | One unnamed dense vector |
| Vector dimensions | 768 |
| Distance | Cosine |
| Point ID | Adapter-generated UUID string |
| Application memory ID | Required payload field `memory_id` |

When the collection is absent, the adapter may create it with exactly this
schema. When it exists, the adapter must inspect it and fail readiness on a
dimension or distance mismatch. It must not silently recreate, resize, or
rewrite an existing collection.

### Payload contract

New points contain:

- `memory_id`: required application memory identifier
- `source_identity`: required source identifier
- `content`: required memory content
- `memory_type`: required existing enum value
- `importance`: required number
- `created_at`: required ISO 8601 timestamp
- `metadata`: required object; empty is allowed
- `provenance.source`: required
- `provenance.creator`: optional
- `provenance.creation_context`: optional
- `provenance.confidence_basis`: optional
- `provenance.verification_state`: required and defaulted to `unverified`
- `provenance.supporting_evidence`: required sequence; empty is allowed
- `lifecycle.state`: required and defaulted to `active`
- `lifecycle.reinforcement_count`: required and defaulted to zero
- `lifecycle.superseded_by`: optional application memory ID
- `lifecycle.changed_at`: optional ISO 8601 timestamp
- `embedding_model`: preserved configured model reference for API
  compatibility
- `embedding_identity`: required immutable identity object defined by ADR 0004
- `service`: preserved value `jebediah-memory`

Unknown additive payload fields remain available in retrieval metadata and do
not make a compatible legacy read fail.

### Point identity

New Qdrant point IDs remain adapter-generated UUIDs. Application memory IDs
remain in `payload.memory_id` and are used for application lookup.

This preserves the current FastAPI behavior. Sprint 005 does not introduce
deterministic point IDs or redefine repeat-write idempotency. An outcome-unknown
failure must therefore not trigger a blind automatic retry.

### Write success

An accepted memory is reported as `stored` only when all of the following are
true:

1. Governance and policy accept the memory.
2. ADR 0004 produces a valid compatible embedding.
3. The canonical adapter submits exactly one Qdrant point containing the
   payload and vector.
4. Qdrant acknowledges completed application of that point operation using
   `wait=true` or the client equivalent.

An in-memory repository write, queued operation, embedding result, or partial
payload construction is not durable success.

### Failure behavior

- A rejected memory performs no embedding and no Qdrant write.
- Embedding failure performs no Qdrant write and returns no stored success.
- Collection incompatibility fails readiness or the request before a write.
- Qdrant rejection returns no stored success.
- A timeout or lost acknowledgement is an unknown write outcome, not a
  confirmed failure or success.
- Unknown outcomes are reconciled by searching the payload `memory_id` before
  any operator-authorized retry.
- No automatic retry is added while point IDs are nondeterministic.
- Errors must not expose memory content, private endpoints, or credentials.

### Consistency expectations

The payload and vector are written as one Qdrant point operation. Sprint 005
uses no second durable system and introduces no distributed transaction.

After Qdrant acknowledges completed application:

- `find(memory_id)` is expected to return the stored payload.
- Semantic search is expected to operate on the same collection and vector.
- API `stored=true` is permitted.

Before acknowledgement, no durable success is claimed. If the result is
unknown, the system fails visibly and requires reconciliation.

### Recovery strategy

- Source-only rollback uses Git and the prior reviewed service artifact.
- Sprint 005 does not rewrite live data, so code rollback has no schema undo.
- A live deployment must verify Qdrant persistence and establish sanitized
  snapshot and restore procedures before claiming durable operations.
- After an unknown write outcome, reconcile by application `memory_id`.
- Corrupt or missing Qdrant records cannot be reconstructed from embeddings.
  Recovery requires a verified Qdrant snapshot or an independently authorized
  source replay.
- A future option-B migration requires its own ADR, backup, dual-read or
  cutover strategy, and recovery proof.

### Legacy payload compatibility

Legacy payload migration is a schema-reading concern. The canonical reader
supports:

- Payloads containing `memory_id`
- Root legacy points whose point ID is the application memory ID and whose
  payload omits `memory_id`
- Missing provenance, defaulting source from `source_identity` and
  verification to `unverified`
- Missing lifecycle, defaulting to `active`
- Missing optional governance fields
- Missing `embedding_identity`, represented as legacy and unverified for
  vector compatibility
- Unknown additive fields

These defaults allow compatible payloads to be read. They do not alter vector
geometry or establish embedding compatibility.

### Incompatible vector geometry

Vector geometry migration is explicitly separate from payload compatibility:

- A one-dimensional placeholder collection cannot be queried with a
  768-dimensional query vector.
- A 768-dimensional zero vector is not a valid semantic embedding.
- Payload defaults cannot make a one-dimensional or placeholder vector
  compatible.
- Qdrant collection dimensions are fixed collection geometry, not per-point
  metadata that a reader can default.
- If a live collection is one-dimensional, zero-filled, or otherwise
  incompatible, service cutover stops.
- Those vectors require a future isolated migration that re-embeds approved
  source content into a separate compatible collection with its own backup,
  validation, cutover, and rollback plan.

Sprint 005 performs no such migration.

## Consequences

### Positive

- Durable record success and semantic-index success share one acknowledged
  point operation.
- No distributed transaction or dual-write inconsistency is introduced.
- One adapter owns collection, payload, identity, and search behavior.
- Failure semantics become honest and testable.
- Legacy payload handling is separated from unsafe vector migration.

### Negative

- Qdrant temporarily carries both durable-record and index responsibilities.
- Loss of Qdrant can lose accepted Memory Service records until backups are
  operationally proven.
- Random storage point IDs make blind retry unsafe after unknown outcomes.
- The combined role must later be reconsidered if stronger record-store
  semantics are required.

### Neutral

- Qdrant's durable custody does not make source claims true.
- Application and storage identities remain separate.
- No existing point is rewritten by this decision.

## Data and provenance impact

This ADR explicitly assigns Qdrant payloads temporary authority for the
Memory Service's accepted-record state. It does not promote embeddings,
similarity, confidence, or source claims to authoritative facts.

Provenance and lifecycle remain stored governance metadata. Verification
defaults to `unverified`, lifecycle defaults to `active`, and neither is
automated.

## Security and privacy impact

Qdrant payloads may contain memory content and provenance. Deployment must
apply access control, data classification, retention, backup protection, and
least-privilege requirements before real information is stored. Public tests
use synthetic payloads only.

Errors, logs, inventories, and review artifacts must not disclose memory
content, credentials, private addresses, or sensitive topology.

## Operations and recovery impact

Deployment readiness now depends on:

- Collection schema inspection
- Qdrant persistence verification
- Snapshot and restore validation
- Failure and unknown-outcome observability
- Model and vector inventory without publishing payload contents

Repository implementation and deployment remain separate decisions.

## Compatibility and migration

The canonical adapter first proves isolated contract behavior. The service is
cut over only after API and governance compatibility passes. Direct Qdrant
logic and duplicate repositories are removed afterward.

No live collection is recreated, rewritten, or backfilled in Sprint 005.
Legacy payload compatibility is implemented as read behavior. Incompatible
vector geometry is blocked and deferred to an isolated future migration.

## Validation

Acceptance requires tests for:

- Exact 768-dimensional cosine collection creation
- Existing compatible collection inspection
- Dimension and distance mismatch failure
- One acknowledged point write per accepted memory
- No write on policy or embedding failure
- Unknown write-outcome handling without blind retry
- Application-ID and point-ID separation
- Payload and Sprint 004 governance round trips
- Compatible legacy payload defaults
- Root legacy point-ID fallback
- Placeholder and geometry incompatibility classification
- Semantic search and storage-independent candidate mapping
- No direct Qdrant operations in FastAPI after cutover
- The full requirements in
  [Sprint 005 Validation Requirements](../SPRINT_005_VALIDATION_REQUIREMENTS.md)

Reconsider option A if Qdrant cannot provide the required acknowledged
single-point durability or if an approved durable record store becomes
available before implementation.

## Follow-up work

- Perform a sanitized live Qdrant inventory before deployment.
- Define and validate operational snapshot and restore procedures.
- Decide memory request idempotency in a separate future scope.
- Use a new ADR if option B later separates record storage from semantic
  indexing.
- Create a separately approved migration if incompatible vectors exist.

## Related documents

- [Sprint 005 Implementation Plan](../SPRINT_005_IMPLEMENTATION_PLAN.md)
- [Memory Architecture](../ARCHITECTURE_MEMORY_SYSTEM.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [ADR 0002](0002-canonical-memory-domain-and-dependency-direction.md)
- [ADR 0004](0004-embedding-model-identity-and-vector-compatibility.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Accepted for implementation on 2026-07-31 after Chief Architect final review
and explicit maintainer authorization. Implementation is limited to Sprint
005; deployment, commit, pull-request, and merge authority were not granted.
