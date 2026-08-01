# ADR 0004: Embedding Model Identity and Vector Compatibility

**Status:** Accepted

**Decision level:** System

**Date:** 2026-07-31

**Decision owner:** Project maintainer

**Reviewers:** Chief Architect and project maintainer

## Decision summary

The canonical embedding provider is Ollama using
`nomic-embed-text:v1.5`, pinned to the immutable Ollama manifest digest
`sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`.
New vectors contain exactly 768 finite values, receive no application-level
normalization, and persist the full embedding identity. Mutable tags such as
`:latest` are not permitted as configured or persisted compatibility
identities.

## Context

Embedding vectors can be compared safely only when their generating model and
transformation contract are compatible. Equal vector dimensions alone do not
establish that compatibility.

The current service names `nomic-embed-text:latest`, while the root adapter
names `nomic-embed-text`. Neither payload value proves the immutable model
artifact. A mutable tag can resolve to different weights over time while
remaining the same string. Sprint 005 therefore requires model identity to be
an explicit persistence and collection-compatibility contract rather than an
unresolved adapter default.

### Verified facts

- The current FastAPI and service-local embedding path configures Ollama with
  `nomic-embed-text:latest`.
- The root Ollama adapter defaults to `nomic-embed-text`.
- The current FastAPI Qdrant collection and API tests expect 768-dimensional
  vectors.
- The application currently passes provider vectors through without explicit
  normalization.
- The official Ollama model registry identifies
  `nomic-embed-text:v1.5` as the 137-million-parameter F16
  `nomic-embed-text-v1.5` model.
- On 2026-07-31, the official registry manifest for
  `nomic-embed-text:v1.5` hashed to
  `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f`.
- Ollama's model-list API exposes a full model digest that can be checked
  before the service becomes ready.

### Reported facts

- Project materials report a local Ollama service.
- The locally installed model, local manifest digest, Ollama version, and
  operational health have not been verified from repository evidence.

### Working assumptions

- The canonical adapter can query Ollama's local model inventory during
  readiness validation without exposing private endpoint details.
- The pinned model returns 768 values for the existing input behavior.
- Sprint 005 implementation can use deterministic fake providers in tests and
  remain undeployed until the local digest is verified.

### Open questions

- Whether the reported Ollama environment already contains the pinned digest
  is an operations inventory question. If it does not, deployment is blocked;
  the architecture decision remains complete.
- Existing live vectors may not record an immutable identity. Their treatment
  is defined below and does not require assuming compatibility.

## Scope

This decision governs:

- Exact embedding provider and model identity
- Mutable-tag policy
- Vector dimensions and numeric validation
- Application normalization behavior
- Persisted embedding identity
- Collection and query compatibility guarantees
- Failure behavior
- Existing and placeholder vector migration rules

## Non-goals

- Selecting a different embedding model
- Benchmarking retrieval quality
- Re-embedding live memories during Sprint 005
- Supporting multiple model spaces in one collection
- Adding vector quantization, normalization, or dimensionality conversion
- Defining Ollama deployment topology or capacity
- Changing retrieval from semantic-only ranking

## Decision drivers

- Reproducible semantic vector identity
- No silent drift from mutable tags
- Compatibility that is stronger than dimension equality
- Preserve the current 768-dimensional cosine behavior
- Fail before durable writes when model identity is wrong
- Keep live migration outside the consolidation sprint
- Preserve enough metadata for safe future migration

## Considered alternatives

### Continue using `nomic-embed-text:latest`

This preserves the current string but allows the underlying model artifact to
change without a payload or collection identity change. Existing and new
vectors could silently occupy different semantic spaces.

### Use `nomic-embed-text:v1.5` without digest verification

A versioned tag is clearer than `latest`, but registry tags can still be
retargeted. It is not an immutable compatibility identity by itself.

### Pin `nomic-embed-text:v1.5` and verify its manifest digest

This provides a human-readable model reference and a content-addressed
identity. It supports deterministic readiness and payload checks without
inventing a new provider.

### Normalize vectors in the application

Explicit L2 normalization could be valid for a new vector contract, but it
would change the existing transformation behavior and require migration or a
separate collection.

### Generate fallback vectors

Zero, importance, padded, or truncated vectors would fabricate semantic
compatibility and contaminate search results.

### Retain the current design

The root and service defaults would continue naming the model differently,
and `:latest` payloads would not prove which model produced a vector.

## Decision

### Exact provider

The provider identity is `ollama`. The canonical adapter lives under
`src/collector/embeddings/` and uses Ollama's embedding API. The memory domain
depends on the `EmbeddingProvider` interface and does not construct an Ollama
client.

No OpenAI-compatible proxy, cloud provider, alternative local model server,
or fallback provider is part of Sprint 005.

### Exact model identity

The only approved Sprint 005 embedding model is:

| Identity element | Required value |
| --- | --- |
| Provider | `ollama` |
| Model reference | `nomic-embed-text:v1.5` |
| Manifest digest | `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Vector dimensions | 768 |
| Application normalization | `none` |
| Qdrant distance | `cosine` |

The service must check the locally resolved full manifest digest before
declaring embedding readiness or accepting a write. A missing or different
digest is an incompatibility failure.

### Mutable tags

Mutable tags, including `nomic-embed-text:latest`, are not permitted:

- As the configured production or supported-deployment model reference
- As the persisted compatibility identity
- As the collection compatibility key
- As evidence that a legacy vector is compatible

The implementation may recognize `:latest` only while reading legacy payload
metadata. It must represent that metadata as legacy/unverified identity, not
silently rewrite it to the pinned digest.

### Persistence contract

Every new Qdrant payload contains this additive object:

```text
embedding_identity:
  provider: ollama
  model: nomic-embed-text:v1.5
  manifest_digest: sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f
  dimensions: 768
  normalization: none
```

The existing `embedding_model` payload field remains for schema compatibility
but new writes set it to `nomic-embed-text:v1.5`. Compatibility decisions use
the full `embedding_identity`, not `embedding_model` alone.

An embedding compatibility key is the exact tuple:

```text
(provider, model, manifest_digest, dimensions, normalization)
```

Two vectors are guaranteed compatible by this architecture only when every
element matches and they are stored under the same distance contract. Equal
dimensions, related tags, shared model family, or similar names are
insufficient.

### Vector validation and normalization

The canonical adapter accepts exactly 768 finite numeric values. It rejects an
empty vector, non-numeric value, non-finite value, or wrong length before any
Qdrant write.

The application stores the provider vector unchanged. It does not perform:

- L2 normalization
- Rounding
- Quantization
- Clipping
- Truncation
- Padding
- Dimension conversion

Shape and finiteness validation are not normalization. Qdrant cosine distance
remains the approved similarity metric.

### Failure handling

If Ollama is unavailable, the pinned model is absent, the resolved digest
differs, or the returned vector is invalid:

- No Qdrant write occurs.
- The request is not reported as stored.
- Context search does not return a fabricated empty success.
- No zero, importance, or other fallback vector is generated.
- The failure is visible without logging sensitive content or private
  endpoint details.
- No automatic retry is introduced during Sprint 005.

Service readiness must fail when the configured local model does not match the
approved identity.

### Compatibility guarantees

New store and query embeddings produced under this ADR may share a collection
only with vectors whose full compatibility key is known to match.

The adapter must not claim compatibility for:

- `nomic-embed-text:latest` payloads without a recorded digest
- 768-dimensional vectors with missing model identity
- Vectors produced by a different digest
- Vectors normalized differently
- Vectors with a different dimension

Unknown identity remains unknown. It is not upgraded by inference.

### Existing vector migration

Sprint 005 performs no automatic vector migration.

Existing vectors are classified as follows:

1. **Payload-compatible with proven embedding identity:** A 768-dimensional
   vector whose exact compatibility key is independently proven may remain in
   the compatible collection without rewriting.
2. **Payload-compatible with unknown embedding identity:** The record payload
   may be readable, but the vector is not guaranteed compatible with new
   queries. New writes must not be mixed into that collection until a
   sanitized inventory proves the identity.
3. **Incompatible vector geometry or placeholder:** A one-dimensional vector,
   zero vector, wrong-length vector, or differently normalized/modelled vector
   requires isolated future migration.

Payload defaults do not change vector geometry or identity. A readable legacy
payload is not evidence of a query-compatible vector.

If migration is later approved, it must:

- Use authorized source content, not reverse engineering from vectors
- Write to a separate versioned or isolated collection
- Generate embeddings with the exact approved compatibility key
- Validate retrieval and record counts side by side
- Preserve the source collection and a verified backup through cutover
- Provide rollback before changing consumers

## Consequences

### Positive

- Every new vector has a reproducible, content-addressed model identity.
- `:latest` cannot silently mix vector spaces.
- Readiness fails before incompatible writes.
- Future migration can distinguish payload compatibility from vector
  compatibility.
- Current dimensions and lack of application normalization remain explicit.

### Negative

- The service cannot become ready until the pinned model digest is installed
  and verified.
- Existing `:latest` vectors are not automatically trusted as compatible.
- A model update requires an ADR or accepted replacement decision and an
  isolated migration plan.
- The existing `embedding_model` value changes for new writes from `:latest`
  to `:v1.5` after implementation.

### Neutral

- This decision does not assess retrieval quality.
- The model remains local through Ollama.
- No vector or payload is changed merely by proposing or accepting this ADR.

## Data and provenance impact

Embeddings remain derived information. The new identity object records the
provider, exact model artifact, geometry, and transformation behavior required
to interpret that derivation.

Model identity does not confer truth, verification, or source authority on a
memory. Existing vectors with unknown identity remain explicitly uncertain.

## Security and privacy impact

Model inventory and readiness checks must not disclose private endpoints,
host details, memory content, or credentials. Model digests are public
artifact identifiers and are safe to record.

The adapter must not send memory content to any provider other than the
approved local Ollama boundary.

## Operations and recovery impact

- Operators must install and preserve the exact approved model artifact.
- Readiness must verify the local full digest and dimensions.
- Model upgrades are controlled migrations, not tag changes.
- Recovery of a compatible service requires the pinned model artifact as well
  as the Qdrant collection.
- Source-only rollback returns to the previous reviewed code; no vector is
  rewritten during Sprint 005.

## Compatibility and migration

The service-local and root embedding defaults are reconciled to the exact
identity only after this ADR is accepted. The API retains its existing fields;
the payload gains an additive `embedding_identity` object and the existing
`embedding_model` field uses the versioned reference for new writes.

Legacy payloads remain readable. Legacy vectors are query-compatible only
when their full identity can be proven. Incompatible or unknown collections
block deployment or require a separately approved isolated migration.

## Validation

Acceptance requires tests for:

- Exact provider and versioned model reference
- Exact manifest-digest readiness validation
- Rejection of `:latest` as a configured or persisted compatibility identity
- Required `embedding_identity` payload fields
- Exactly 768 finite numeric values
- No application-level normalization
- Empty, non-numeric, non-finite, short, and long vector rejection
- No Qdrant write after provider, digest, or vector failure
- No fabricated context result after query-embedding failure
- Exact compatibility-key equality
- Unknown legacy identity remaining unknown
- Separation of legacy payload reading from vector-geometry compatibility
- Placeholder vectors being blocked from normal migration
- The full requirements in
  [Sprint 005 Validation Requirements](../SPRINT_005_VALIDATION_REQUIREMENTS.md)

Reconsider this decision only through a new ADR if the pinned artifact becomes
unavailable, does not produce the verified geometry, or a different model is
approved.

## Follow-up work

- Verify the reported local Ollama inventory before deployment.
- Preserve the pinned model artifact in the future operations and recovery
  procedure.
- Create a separate migration proposal if existing vectors cannot prove the
  approved compatibility key.
- Benchmark a replacement model only in a separately approved future scope.

## Related documents

- [Official Ollama `nomic-embed-text:v1.5` entry](https://ollama.com/library/nomic-embed-text:v1.5)
- [Official Ollama model-list API](https://docs.ollama.com/api/tags)
- [Sprint 005 Implementation Plan](../SPRINT_005_IMPLEMENTATION_PLAN.md)
- [Memory Architecture](../ARCHITECTURE_MEMORY_SYSTEM.md)
- [Data Ownership](../DATA_OWNERSHIP.md)
- [ADR 0002](0002-canonical-memory-domain-and-dependency-direction.md)
- [ADR 0003](0003-qdrant-repository-collection-and-payload-consolidation.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Accepted for implementation on 2026-07-31 after Chief Architect final review
and explicit maintainer authorization. Implementation is limited to Sprint
005; deployment, commit, pull-request, and merge authority were not granted.
