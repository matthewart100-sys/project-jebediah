# Collector 1.0 Implementation Plan

**Status:** Proposed

**Execution state:** Planning only; implementation and deployment blocked

**Last reviewed:** 2026-07-31

## Objective

Produce a small, testable Collector 1.0 implementation that conforms to the
Collector specification while keeping n8n, Ollama, and Qdrant behind replaceable
adapters.

## Delivery strategy

Implementation proceeds through four gates. No gate authorizes live-server
deployment unless that authorization is stated explicitly.

## Gate I1: Contract fixtures and schemas

Create repository-owned synthetic fixtures for:

- Valid creation
- Exact retry
- Revision update
- Revision conflict
- Invalid timestamps
- Unsupported source type
- Empty content
- Embedding failure
- Storage failure

Define versioned request, result, error, provenance, and storage-request shapes.

**Exit evidence:**

- Fixtures contain no real personal or operational data.
- Schema tests pass.
- Identity test vectors are deterministic.
- Chief Architect confirms the implementation contract matches the
  specification.

## Gate I2: Pure Collector core

Implement pure logic for:

- Validation
- Normalization
- Content digest
- Logical and revision identity
- Duplicate decision
- Provenance construction
- Structured results and errors

The core must not call n8n, Ollama, Qdrant, Docker, the network, or the live
server.

**Exit evidence:**

- Unit tests cover every acceptance rule that does not require an adapter.
- Repeated test runs produce identical IDs.
- Conflict and retry behavior are demonstrated.
- Coverage is proportionate to risk rather than a vanity target.

## Gate I3: Adapter contracts and local test doubles

Define narrow interfaces for:

- Submitting adapter
- Embedding adapter
- Storage adapter
- Clock and correlation provider where required

Create deterministic local test doubles before real adapters.

**Exit evidence:**

- Core tests run with no external service.
- Adapter failures map to stable error categories.
- Timeouts and retries are bounded.
- Model changes do not alter logical identity.
- Storage retries cannot create duplicate logical revisions.

## Gate I4: Reported-stack integration candidate

Only after sanitized infrastructure verification, create proposed adapters for:

- n8n as orchestration or submitting adapter
- Ollama as the local embedding adapter
- Qdrant as the vector-search storage adapter

Real product adapters must not redefine the Collector contract.

**Exit evidence:**

- Exact product versions and sanitized configuration are recorded.
- Integration tests run against disposable or isolated test resources.
- No production collection or live data is used.
- Rollback is documented and tested.
- A separate review explicitly authorizes any live-server deployment.

## Proposed repository structure

```text
src/
  collector/
    core/
    contracts/
    adapters/
tests/
  collector/
    fixtures/
    unit/
    contract/
    integration/
docs/
  COLLECTOR_1_SPECIFICATION.md
  COLLECTOR_1_IMPLEMENTATION_PLAN.md
```

The language and exact module layout remain deferred until implementation
planning selects them through repository evidence.

## n8n boundary

n8n may:

- Receive an explicitly triggered request
- Extract source-specific fields
- Call the Collector implementation
- Display or route a structured result
- Coordinate bounded retry behavior

n8n must not become the only owner of identity, validation, provenance,
idempotency, or contract semantics.

An exported workflow is an adapter artifact, not the complete Collector.

## Ollama boundary

Ollama may provide local embeddings after validation.

The adapter must:

- Record model identity
- Enforce timeouts
- Map failures predictably
- Avoid changing record identity
- Support deterministic test substitution

Collector correctness must remain testable while Ollama is offline.

## Qdrant boundary

Qdrant may store vectors and approved payload fields for retrieval.

The adapter must:

- Use deterministic point or payload identity
- Support idempotent upsert behavior
- Detect revision conflicts before destructive overwrite
- Preserve required provenance
- Expose health without leaking content or topology
- Use a disposable test collection for integration tests

Qdrant similarity results must not determine source identity.

## Testing strategy

### Unit tests

Cover pure validation, normalization, identity, conflicts, provenance, and
result mapping.

### Contract tests

Run every real and test adapter against the same expected behaviors.

### Integration tests

Use isolated local services or disposable resources. Do not depend on existing
production data.

### Failure tests

Demonstrate:

- Embedding timeout
- Embedding unavailable
- Storage timeout
- Storage unavailable
- Partial orchestration failure
- Exact retry after ambiguous timeout
- Conflict under repeated submission

### Security tests

Verify:

- Secrets are rejected from prohibited metadata
- Logs redact or omit content
- Error payloads exclude stack traces and private endpoints
- Public fixtures are synthetic

## Configuration

Configuration must be explicit, validated, and separated from code.

Secrets must use an approved secret mechanism and must never be committed.

Configuration should include:

- Allowed source types
- Maximum content and metadata sizes
- Retry and timeout limits
- Embedding adapter selection
- Storage adapter selection
- Contract and schema versions
- Logging policy

## Migration and rollback

The first deployment must target an isolated test path.

Before live use:

1. Export and back up the current n8n workflow involved.
2. Snapshot or back up relevant Qdrant data.
3. Record current service health.
4. Use a separate test workflow or disabled copy.
5. Use a disposable Qdrant collection where practical.
6. Verify rollback restores the prior state.
7. Obtain explicit execution authorization.

Rollback must not require deleting unrelated collections or workflows.

## Required implementation decisions

Before Gate I2 begins, a reviewed implementation change must decide:

- Language and supported runtime
- Package and dependency management
- Schema representation
- Hash algorithm and canonical serialization
- Test runner
- Logging interface

Before Gate I4 begins, a reviewed integration change must decide:

- Exact n8n integration shape
- Exact Ollama embedding endpoint and model
- Exact Qdrant collection and payload schema
- Authentication and secret handling
- Test-resource lifecycle
- Deployment and rollback commands

## Definition of implementation complete

Collector 1.0 implementation is complete only when:

- All specification acceptance tests pass.
- The core works without external services.
- Real adapters pass shared contract tests.
- Integration tests use isolated resources.
- Retry and conflict behavior is demonstrated.
- Security controls are verified.
- Operator documentation and rollback are complete.
- Exact implementation artifacts receive Chief Architect review.
- A separate decision authorizes deployment.

Planning approval alone does not satisfy this definition.
