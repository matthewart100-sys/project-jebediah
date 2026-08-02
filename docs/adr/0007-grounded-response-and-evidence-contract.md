# ADR 0007: Grounded Response and Evidence Contract

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-01

**Decision owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect

## Decision summary

If accepted, Sprint 006 exposes only `POST /interactions/query` with a minimal
closed request and exactly three result states: `grounded`,
`insufficient_evidence`, and `failed`. Grounding describes validated process
and evidence linkage, not truth, and every public evidence item is a bounded
allowlisted view of a selected memory.

## Context

A public interaction contract must let clients distinguish a grounded answer,
a successful retrieval with no usable evidence, and a failure. Ambiguous
endpoint names or result shapes can cause an empty answer, provider error, or
partial response to be mistaken for success. Returning raw memory payloads can
also expose storage IDs, metadata, paths, or sensitive provenance.

### Verified facts

- The current service exposes `/health`, `/memory/store`, and
  `/memory/context` but no grounded-interaction route.
- `/memory/context` returns raw candidate content and metadata and is not a
  generation or evidence contract.
- Memory provenance and verification state do not establish truth.
- Existing API validation uses FastAPI's default HTTP 422 behavior.

### Reported facts

- No deployed external client contract for a grounded endpoint is verified.
- n8n is reported in the environment but has no approved workflow or special
  integration authority.

### Working assumptions

- An additive endpoint can coexist with current memory routes.
- A closed, versioned contract is preferable to exposing provider or storage
  response objects.
- Selected application memory IDs can remain internal while response-scoped
  opaque aliases expose evidence relationships without revealing identity.

### Open questions

- Authentication and multi-tenant policy remain future service decisions and
  are not weakened by this unauthenticated contract proposal.
- External client retry behavior is not defined here; the service itself does
  not retry generation.

## Scope

This decision governs:

- endpoint and request schema
- public result states and their meaning
- stable error codes and HTTP mappings
- generated answer and citation validation
- public evidence fields and bounds
- compatibility with existing routes

## Non-goals

- Verifying factual truth or source authority
- Ungrounded answers or fallback behavior
- Domain filters, tools, agents, multi-turn conversation, or write options
- Authentication, tenant design, or external retry policy
- Defining internal context, prompt, trust, or model policies governed by ADRs
  0008 through 0010

## Decision drivers

- No false success
- One client-visible contract across all artifacts
- Clear separation of no evidence from dependency failure
- Evidence linkage without raw internal payload exposure
- Framework-independent stable failure semantics
- Additive compatibility with existing memory APIs

## Considered alternatives

### Extend `POST /memory/context`

This would change an existing retrieval contract into a generation contract
and blur memory ownership with interaction response semantics.

### Add multiple routes for answer and evidence modes

Separate routes create unnecessary contract combinations and increase the
chance of divergent grounding and error behavior.

### Return HTTP errors without a stable body

Framework or provider error bodies are easy to implement but force clients to
infer meaning from unstable detail and may expose internals.

### Return an answer when no evidence qualifies

This violates the grounded-only purpose and would require an ungrounded-answer
permission explicitly prohibited by Sprint 006.

### Retain the current design

Clients can retrieve memory candidates but must invent generation, evidence,
failure, and trace behavior independently.

## Decision

### Endpoint and request

The one route is:

```text
POST /interactions/query
```

The request is a UTF-8 JSON object with:

- required `question`: trimmed nonempty string, maximum 2,000 Unicode scalar
  values
- optional `max_evidence`: integer from 1 through 5, default 5

The encoded body is limited to 16,384 bytes before or while parsing. Extra
fields, booleans for `max_evidence`, unsupported options, malformed JSON, and
non-object bodies are invalid. No filter, tool, agent, fallback, or ungrounded
option is accepted.

### Common public result

All results are closed schemas with:

- `status`
- opaque UUID `trace_id`
- `answer`
- `evidence`

Only `grounded` has a non-null answer and nonempty evidence. Unknown fields are
not emitted.

### Grounded result

`grounded` requires successful retrieval, usable whole-record context,
integrity and token checks, generation, model-identity continuity,
provider-contract validation, citation validation, and evidence packaging.

It means none of the following:

- verified fact
- true or authoritative claim
- current or complete answer
- approval to act
- automated verification or lifecycle transition

A grounded result includes a closed `policy` object naming the context-policy
version, prompt-policy version, generation provider, configured model tag,
preflight observed digest, postflight observed digest, and
`identity_continuity_status: observed_consistent`. Those observations do not
prove which artifact served generation. The answer is a nonempty string of at
most 8,000 Unicode scalar values.

The provider contract returns only:

- `answer`
- `cited_evidence_aliases`

Aliases are assigned as `evidence-1` through `evidence-N` in deterministic
selected order and map to raw memory IDs only in a request-lifetime in-process
table. The citation list is nonempty, contains no duplicate, and contains only
aliases selected into context. Every alias resolves exactly once. Unknown,
malformed, duplicate, or missing citations produce
`generation_contract_error`. Public evidence contains only cited selected
records in deterministic context order.

### Insufficient-evidence result

`insufficient_evidence` is a successful terminal result only when retrieval
completed and deterministic policy selected no usable evidence. It contains:

- `status: insufficient_evidence`
- `trace_id`
- `answer: null`
- `evidence: []`

No provider call or generation trace event is permitted.

### Failed result

`failed` contains:

- `status: failed`
- `trace_id`
- stable `error_code`
- safe bounded `message`
- `answer: null`
- `evidence: []`

No partial answer, citation, evidence, provider body, or raw exception is
returned.

### Failure mapping

| Error code | HTTP status | Meaning |
| --- | --- | --- |
| `invalid_request` | 422 | Request body or public schema invalid |
| `retrieval_unavailable` | 503 | Query embedding or semantic retrieval unavailable |
| `generation_unavailable` | 503 | Generation transport or service failed after readiness |
| `generation_provider_not_ready` | 503 | Required generation model identity or capability unavailable |
| `context_integrity_error` | 500 | Conflicting or unsafe retrieval context |
| `generation_contract_error` | 500 | Invalid provider output, citation, response size, or identity continuity |
| `internal_contract_error` | 500 | Internal state or packaging invariant failed |
| `capacity_unavailable` | 503 | Queue, concurrency, token, deadline, or runtime resource capacity unavailable |
| `request_cancelled` | 499 when the connection remains | Request cancelled without successful completion |

These nine values are the exhaustive public `error_code` vocabulary. Internal
reasons map deterministically to one value and never become public codes.
Provider response-body overflow, malformed or unsupported output, unsafe answer
disclosure, and citation or evidence mismatch map to
`generation_contract_error`. Provider timeout after readiness maps to
`generation_unavailable`.

If the client has disconnected, no HTTP response may be possible; cancellation
still terminates the trace as failed and never records success. The service
performs no automatic retry or fallback for any code.

### Safe evidence allowlist

Each evidence object may contain only:

- `evidence_alias`, response-scoped `evidence-N`, never a durable identity
- `disclosure_status`, exactly `disclosed` or `withheld`
- `excerpt`, maximum 600 Unicode scalar values when disclosed, otherwise `null`
- `excerpt_truncated`, explicit boolean when disclosed, otherwise `null`
- finite `semantic_relevance`
- existing `memory_type`
- timezone-qualified `created_at`
- existing `lifecycle_state`
- existing `verification_state`

The public excerpt may be shorter than the whole selected record. That fact is
represented only by `excerpt_truncated`; it never implies model-context
truncation.

Sprint 006 returns no raw provenance or source text field. The
`public-evidence-v1` policy validates bounded excerpt Unicode and fails closed
on internal Windows or Unix paths, localhost or private-network URLs, any
public or private IP address, hostnames, tenant or account identifiers,
credentials, API keys, token-like or secret-like strings, and arbitrary nested
metadata. It does not partially redact uncertain content.

When safe, an excerpt is `disclosed`. When unsafe or uncertain, the evidence
record remains as a safe alias with `disclosure_status: withheld`,
`excerpt: null`, and `excerpt_truncated: null`. Failure to construct that closed
record maps to `internal_contract_error` and prevents a grounded response. The
whole selected record remains in model context, so a safe grounded answer may
cite a `withheld` alias. The generated answer passes the same disclosure
checks; unsafe answer output maps to `generation_contract_error` with no answer
or evidence returned.

The response must not expose raw application memory IDs, Qdrant point IDs,
internal paths, URLs, network addresses, hostnames, tenant IDs, arbitrary
metadata, secrets, provider request or response objects, raw prompts, or trace
payloads. The alias-to-memory mapping is process-ephemeral, not logged with raw
IDs by default, and destroyed at request termination.

### Existing-route compatibility

`/health`, `/memory/store`, and `/memory/context` retain their current paths,
requests, responses, status behavior, and semantic-only ranking. No existing
client is silently redirected to generation.

## Consequences

### Positive

- Clients can distinguish answer, no-evidence, and failure reliably.
- Framework and provider details do not become public contracts.
- Evidence is bounded, traceable, and separated from truth authority.
- Insufficient evidence cannot trigger an ungrounded response.
- Existing memory clients remain compatible.

### Negative

- FastAPI validation errors require explicit translation.
- Provider output must satisfy a strict answer-and-citation schema.
- Some useful metadata is deliberately unavailable publicly.
- HTTP 499 is nonstandard and applies only while a response channel remains.

### Neutral

- Grounded responses remain probabilistic generated text.
- The contract is additive and has no current consumers to migrate.
- Authentication remains a separate unresolved service concern.

## Data and provenance impact

Answers and public evidence are temporary derived information. Evidence
preserves only a response-scoped alias and allowlisted governance state without
exposing application memory identity or raw provenance and without granting
truth authority. No result is persisted by Sprint 006.

## Security and privacy impact

Closed schemas and bounded fields reduce metadata and exception leakage.
Questions, evidence, and provider responses remain untrusted. Public output
sanitization does not replace future authentication or data-classification
policy.

## Operations and recovery impact

Stable errors support safe health and failure diagnosis without exposing
content. The endpoint remains undeployed. Source rollback removes an additive
route and package; no persisted interaction state requires migration or
recovery.

## Compatibility and migration

No existing route changes. A future version that changes result states,
evidence fields, grounding meaning, or HTTP mappings requires compatibility
review and may require versioning. There is no current interaction data to
migrate.

## Validation

Acceptance and implementation require:

- one route across source, docs, tests, and OpenAPI
- request-body, question, optional range, extra-field, and unsupported-option
  tests
- exact result-state and error-mapping tests
- no generation for insufficient evidence
- no partial success on any failure
- answer-and-citation schema validation
- public evidence allowlist and bound tests
- response-scoped alias stability and raw memory-ID non-disclosure tests
- fail-closed excerpt and generated-answer disclosure tests for paths, URLs,
  IP addresses, hostnames, tenant or account identifiers, secrets, malformed
  Unicode, oversize, and nested metadata
- excerpt versus model-context separation tests
- existing memory API regressions
- the complete
  [Sprint 006 Validation Requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)

Reconsider the contract if an approved client requires a versioned extension
that cannot fit the closed request or evidence schemas.

## Follow-up work

- Implement only after all proposed Sprint 006 ADRs are accepted and separate
  authorization is issued.
- Define authentication before any deployment that handles classified data.
- Version the endpoint through a later decision if a real compatible evolution
  need appears.

## Related documents

- [Sprint 006 Specification](../SPRINT_006_SPECIFICATION.md)
- [Sprint 006 Validation Requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)
- [ADR 0006](0006-canonical-interaction-domain-and-dependency-direction.md)
- [ADR 0008](0008-deterministic-retrieval-context-assembly.md)
- [ADR 0009](0009-retrieved-content-trust-boundary.md)
- [ADR 0010](0010-generation-model-identity-and-policy-defaults.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

Proposed for independent Work Mode review and Chief Architect decision at the
future exact head of the Sprint 006 Proposal v2 pull request. No endpoint or
result contract is accepted before that review is recorded.
