# Sprint 006 Specification: Grounded Single-Turn Interaction

**Status:** Proposed

**Proposal identity:** Sprint 006 Proposal v2, newly authored from reviewed
`main` at `693a42299d7caff016b78bc9c45ffb5d1a5537e0`

**Date:** 2026-08-01

**Implementation status:** Unauthorized

**Deployment status:** Unauthorized

## Purpose

Sprint 006 proposes the first canonical, single-turn, read-only interaction
path over the existing semantic memory candidate:

```text
Question
-> Request validation
-> Semantic retrieval
-> Deterministic context assembly
-> Ollama generation
-> Evidence packaging
-> Traceable response
```

The governing principle is:

> Every grounded answer must be explainable and traceable. Its configuration,
> policy, evidence selection, and observed model-inventory metadata must be
> recorded sufficiently for investigation and replay attempts; identical
> generated output is not guaranteed.

This specification defines architecture and validation requirements only. It
does not authorize implementation, deployment, live-service access, or data
mutation.

## Sprint classification

Sprint 006 is:

> A bounded Phase 2 memory-client validation that proves governed retrieval,
> deterministic context assembly, and evidence-grounded generation. Sprint
> 006 does not activate or implement the Phase 6 Reasoning Engine.

The interaction path consumes the existing Phase 2 memory retrieval boundary.
It does not introduce agents, tools, planning, autonomous action, durable
conversation memory, or general-purpose reasoning authority.

## Evidence and proposal boundary

### Repository-verified facts

- `src/collector/memory/` is the sole canonical memory domain.
- The memory domain exposes storage-independent `RetrievalCandidate` values
  and currently ranks them by semantic relevance only.
- `services/jebediah-memory/app/main.py` owns FastAPI transport and composes the
  canonical package.
- The current `MemoryApplicationService` exposes both store and context
  behavior, so it is not a structurally read-only dependency for a future
  interaction domain.
- The repository contains no `src/collector/interaction/` package and no
  `POST /interactions/query` endpoint.
- Sprint 004 lifecycle and verification values are representation only.
- Deployment and live Qdrant and Ollama operation remain unverified by the
  repository.

### Architecture input requiring implementation-time revalidation

The Chief Architect supplied a sanitized local Ollama inventory for the
generation proposal. The proposed configured tag and required observed
inventory fields are recorded in
[ADR 0010](adr/0010-generation-model-identity-and-policy-defaults.md). This
input does not prove that a future implementation or deployment still resolves
the same tag, digest, capabilities, or capacity. Preflight and post-generation
inventory observations are mandatory and do not prove which artifact served a
request.

### Proposal v1 separation

This document is newly authored. It does not reconstruct, revise, continue, or
claim equivalence with abandoned Proposal v1. The
[abandonment record](SPRINT_006_PROPOSAL_V1_ABANDONED.md) remains authoritative
for that history. The surviving Work Mode findings are design inputs only.

## Historical design inputs addressed

The seven tracked findings are addressed as first-class v2 requirements:

| Historical design input | Proposal v2 resolution |
| --- | --- |
| Endpoint and public result-contract mismatch | One route, `POST /interactions/query`, one request schema, three result states, and stable HTTP/error mappings are defined below and in ADR 0007. |
| Nondeterministic conflicting duplicate-ID handling | Candidate groups are compared by material fingerprints; identical duplicates collapse and conflicts fail independent of input order under ADR 0008. |
| Missing inclusion, exclusion, and truncation reason contracts | Eight stable context-decision reason codes and separate model-context and public-excerpt rules are defined under ADR 0008. |
| Missing trace-event and state-machine contract | Eight exact trace events, ordering, cardinality, fields, terminals, retention, and cancellation behavior are defined below. |
| Uncalibrated relevance threshold and missing token-capacity validation | `0.50` remains provisional; calibration and full-prompt token fixtures are implementation-acceptance gates. |
| Unresolved roadmap and phase classification | Sprint 006 is explicitly a Phase 2 memory-client validation and not Phase 6 Reasoning Engine work. |
| Overstated atomic model-identity binding and missing identity-drift handling | ADR 0010 defines preflight and post-generation inventory observations, discards uncertain results, and records that matching observations do not prove the serving artifact because a residual race exists before, during, and after tag-based generation. |

These resolutions are newly authored architecture. They are not recovered
Proposal v1 content or implementation authority.

## Scope

Sprint 006 proposes:

- the canonical interaction domain at `src/collector/interaction/`
- the fixed `POST /interactions/query` HTTP contract
- a narrow read-only memory retrieval capability
- deterministic retrieval-candidate integrity and context assembly
- whole-record model context with separate bounded public excerpts
- evidence-grounded Ollama generation under a configured tag, fixed policy,
  and recorded preflight and postflight inventory evidence
- a retrieved-content trust boundary and mechanically testable prompt structure
- safe public evidence packaging
- an ephemeral trace-event and state-machine contract
- bounded capacity, cancellation, timeout, and failure behavior
- architecture, API, package, container, calibration, and operationally safe
  validation requirements

## Non-goals

Sprint 006 does not propose or authorize:

- Phase 6 Reasoning Engine activation
- agents, planning loops, tool use, or autonomous action
- n8n orchestration; n8n remains an ordinary external HTTP client
- web access, scheduling, file operations, or external execution
- ungrounded-answer permission
- domain filters, tool controls, agent options, or multi-turn conversation
- memory writes, verification changes, lifecycle transitions, or reranking
- a second retrieval implementation
- persistence of questions, prompts, answers, traces, or interaction records
- Qdrant migration, re-embedding, live-data access, or collection changes
- Ollama inventory mutation, model pull, tag reassignment, or fallback models
- Docker, Compose, deployment, or production configuration changes

## Proposed architecture and dependency direction

The proposed flow is:

```text
external HTTP client
    -> FastAPI composition and HTTP translation
    -> collector.interaction application boundary
    -> collector.memory read-only retrieval capability
    -> existing canonical embedding and Qdrant retrieval path
    -> collector.interaction deterministic context and prompt policy
    -> Ollama generation adapter
    -> collector.interaction response and evidence validation
    -> FastAPI HTTP translation
```

### Canonical interaction domain

Location: `src/collector/interaction/`

The interaction domain owns:

- single-turn orchestration
- request-independent domain input validation
- deterministic context selection and decision records
- prompt construction and structural separation
- generation-provider interfaces and failure classification
- model-inventory observation and continuity classification at the adapter
  boundary
- provider-response validation
- evidence packaging and result states
- trace state-machine rules

It must not import FastAPI, service-local application modules, Docker or
Compose configuration, Qdrant client types, or a store-capable memory service.

### FastAPI boundary

`services/jebediah-memory/` remains the composition and deployment boundary.
It owns only:

- HTTP transport and the route
- request-body limit enforcement
- Pydantic request and response translation
- dependency construction and configuration
- cancellation propagation
- HTTP status mapping

FastAPI must not implement retrieval, duplicate policy, context selection,
prompt construction, evidence selection, citation validation, identity
continuity, or trace-state decisions.

### Memory boundary

`src/collector/memory/` remains the only memory and retrieval domain. It owns
semantic query embedding, Qdrant search, vector-identity validation,
storage-independent candidate construction, and semantic-only ordering.

The interaction domain depends on a protocol with query behavior only. The
proposed semantic shape is:

```text
search(question, candidate_limit) -> sequence of RetrievalCandidate
```

The concrete read-only adapter remains in the memory domain and may compose
the existing embedding and Qdrant search boundaries. The protocol exposed to
interaction has no `store`, `save`, `index`, `upsert`, `delete`, lifecycle,
verification, or repository-client member. The interaction application is
never given `MemoryApplicationService` or another store-capable object.

Zero memory writes are therefore enforced by construction and verified by
success, insufficient-evidence, failure, timeout, and cancellation interaction
counts.

## Canonical HTTP contract

### Endpoint

The only Sprint 006 route is:

```text
POST /interactions/query
```

The existing `/memory/store`, `/memory/context`, and `/health` routes are not
changed by this proposal.

### Request

```json
{
  "question": "What did we decide about Collector 1.0?",
  "max_evidence": 5
}
```

The request contract is:

| Property | Rule |
| --- | --- |
| Content type | UTF-8 JSON object |
| Maximum encoded body | 16,384 bytes, enforced before or while parsing |
| `question` | Required string; 1 through 2,000 Unicode scalar values after leading and trailing whitespace removal |
| `max_evidence` | Optional integer; default `5`; allowed range `1` through `5`; booleans are rejected |
| Extra fields | Rejected |
| Unsupported options | Rejected; no filters, tools, agents, fallback, or ungrounded-answer flag |

Empty, whitespace-only, oversized, malformed, non-object, extra-field, and
out-of-range requests produce `invalid_request` with HTTP 422. FastAPI's
default validation body must be translated to the stable failed-result shape;
framework-specific error arrays are not the public contract.

### Common response fields

Successful and failed responses are closed schemas. They do not return
arbitrary provider, Qdrant, trace, or memory metadata.

| Field | Meaning |
| --- | --- |
| `status` | Exactly `grounded`, `insufficient_evidence`, or `failed` |
| `trace_id` | Opaque UUID assigned to this request |
| `answer` | A nonempty bounded string only for `grounded`; otherwise `null` |
| `evidence` | Validated public evidence for `grounded`; otherwise an empty array |

### `grounded`

`grounded` means only that:

- retrieval succeeded
- at least one usable evidence record was selected
- context integrity and token-capacity checks passed
- generation completed under the required policy
- preflight and post-generation inventory observations matched the required
  fields and were classified `observed_consistent`
- provider response and citations passed the generation contract
- public evidence packaging succeeded

It does not mean the answer is factually verified, true, current,
authoritative, complete, or approved for action.

A grounded response also contains a closed `policy` object with:

- `context_policy_version`
- `prompt_policy_version`
- `generation_provider`
- `configured_model_tag`
- `preflight_observed_digest`
- `postflight_observed_digest`
- `identity_continuity_status: observed_consistent`

These fields report observed inventory continuity, not cryptographic or atomic
proof of the artifact that served generation. The answer is limited to 8,000
Unicode scalar values. Before prompt construction, selected records receive
response-scoped aliases in deterministic selected order: `evidence-1`,
`evidence-2`, and so on. The provider sees those aliases rather than raw memory
IDs and returns a nonempty answer plus a nonempty list of
`cited_evidence_aliases`. Every citation must resolve exactly once to a selected
response alias; unknown, duplicate, malformed, or uncited results fail with
`generation_contract_error`. Public evidence contains only cited aliases in
deterministic selected order.

### `insufficient_evidence`

`insufficient_evidence` requires:

- retrieval completed successfully
- deterministic context assembly selected no usable evidence under policy
- no generation call occurred
- `answer` is `null`
- `evidence` is an empty array
- `response.packaged` is the successful terminal trace event

This state is not a provider failure and must not be converted into an
ungrounded answer.

### `failed`

A failed response contains exactly the common fields plus:

- `status: failed`
- `trace_id`
- stable `error_code`
- safe human-readable `message`
- `answer: null`
- `evidence: []`

It contains no partial answer or evidence that could be mistaken for
successful grounding. Messages never include questions, source content,
prompts, answers, private endpoints, internal paths, provider bodies, or
arbitrary exception text.

### Stable error and HTTP mapping

| Error code | HTTP behavior | Required meaning |
| --- | --- | --- |
| `invalid_request` | 422 | The public request contract was not satisfied. |
| `retrieval_unavailable` | 503 | Embedding or semantic retrieval did not complete safely. |
| `generation_unavailable` | 503 | The generation request failed after readiness was established. |
| `generation_provider_not_ready` | 503 | Required model identity, capability, or readiness preflight failed. |
| `context_integrity_error` | 500 | Candidate conflict or context integrity made evidence unsafe to use. |
| `generation_contract_error` | 500 | Provider output, citations, body shape, or continuity could not be validated. |
| `internal_contract_error` | 500 | An internal state or packaging invariant failed. |
| `capacity_unavailable` | 503 | Queue, concurrency, token, or runtime resource policy blocked safe generation. |
| `request_cancelled` | 499 when a response channel remains; otherwise no response after disconnect | Cancellation terminates work and records failure without false success. |

This table is the exhaustive public failure-code vocabulary. Internal provider,
parser, sanitizer, and state-machine reasons must map deterministically to one
of these nine codes and must never enter `error_code`. In particular, response-
body overflow, malformed or unsupported provider output, and citation or
evidence mismatch map to `generation_contract_error`; a provider timeout after
readiness maps to `generation_unavailable`.

No error triggers automatic retry, fallback model selection, context trimming,
or a second generation attempt.

## Deterministic retrieval and context assembly

### Proposed defaults

```text
retrieval_candidate_count = 12
minimum_semantic_relevance = 0.50
maximum_selected_evidence = 5
maximum_context_characters = 12000
maximum_individual_memory_characters = 8000
evidence_excerpt_characters = 600
maximum_question_characters = 2000
context_policy_version = interaction-context-v1
prompt_policy_version = grounded-answer-v1
```

`minimum_semantic_relevance = 0.50` is provisional. It is not a verified
quality threshold and cannot pass implementation acceptance without the
calibration evidence defined below.

### Candidate integrity and duplicate handling

Context assembly operates on a complete bounded candidate list and is
independent of provider input order.

1. Validate finite semantic relevance, memory ID, content, and material
   evidence metadata.
2. Group candidates by application `memory_id` before selection.
3. Build a canonical material fingerprint from content, semantic relevance,
   memory type, creation time, lifecycle state, verification state,
   provenance fields, supporting-evidence references, and every field used in
   public evidence or selection.
4. Collapse candidates with the same ID only when the complete material
   fingerprint is identical. Record `duplicate_identical` for every removed
   copy.
5. If one ID has more than one material fingerprint, record
   `duplicate_conflict` and fail the interaction with
   `context_integrity_error` before generation.

Input order never chooses a conflicting survivor. Conflicting candidates are
never sent to generation.

### Stable context-decision reason codes

Every candidate receives one final ephemeral decision:

| Reason code | Meaning |
| --- | --- |
| `selected` | The whole record was selected into model context. |
| `below_threshold` | Semantic relevance was finite but below `0.50`. |
| `duplicate_identical` | A byte- and metadata-identical duplicate of the canonical candidate was removed. |
| `duplicate_conflict` | The same memory ID carried materially different evidence and caused interaction failure. |
| `record_limit` | The selected-record count was already at the effective request limit. |
| `individual_oversize` | Whole source content exceeded 8,000 characters. |
| `aggregate_budget_exhausted` | The complete deterministic evidence block would exceed 12,000 characters. |
| `malformed_candidate` | Required identity, content, score, or material metadata was invalid. |

Decision records contain only response-scoped aliases or approved nonreversible
trace-local fingerprints, ordinal positions, numeric counts, and reason codes.
Raw memory IDs and rejected raw content are not logged by default. The
alias-to-memory mapping is process-ephemeral for one request and is not a public
response field or durable interaction record.

### Ordering and selection

After duplicate integrity:

1. Exclude malformed and below-threshold candidates.
2. Sort by semantic relevance descending and then by sanitized application
   memory ID ascending. No input-order tie breaker is permitted.
3. Apply the effective record limit, which is the smaller of request
   `max_evidence` and `maximum_selected_evidence`.
4. Render each candidate with deterministic evidence wrappers and metadata.
5. Select only a whole rendered record when its complete block fits both the
   individual and aggregate character budgets.
6. Continue evaluating later candidates deterministically when an earlier
   whole record does not fit; never shorten a record to make it fit.

`maximum_context_characters` counts the complete rendered evidence section,
including labels, separators, and evidence metadata. It is not merely a sum of
source-content lengths.

### Response-scoped evidence aliases

After final selection, assign aliases by deterministic selected order:
`evidence-1` through `evidence-N`. The alias is stable everywhere within that
one prompt, provider response, and public response. It reveals no memory ID,
must not be interpreted as durable identity across requests, and maps to the
selected memory only in an in-process request-lifetime table. The table is
destroyed when the request terminates and is never persisted. Raw application
memory IDs remain internal to retrieval, deduplication, and integrity checks
and are not logged with aliases by default.

### Whole-record and excerpt separation

- Model context uses whole selected source records only.
- Silent source-content or model-context truncation is prohibited.
- A source record over the individual limit is excluded.
- A complete context over the aggregate or token budget fails or excludes
  according to the reason contract before generation; it is never trimmed.
- Public evidence returns at most 600 Unicode scalar values of the selected
  source record as `excerpt`.
- Every evidence item contains `excerpt_truncated`, which is `true` exactly
  when the excerpt is shorter than the selected source record.
- Public excerpt truncation does not alter or describe model context.

## Safe public evidence

Each evidence object is a closed allowlist:

| Field | Limit and meaning |
| --- | --- |
| `evidence_alias` | Response-scoped `evidence-N` value assigned in selected order; not a durable identifier |
| `disclosure_status` | Exactly `disclosed` or `withheld` |
| `excerpt` | For `disclosed`, safe UTF-8 text of at most 600 Unicode scalar values; for `withheld`, `null` |
| `excerpt_truncated` | For `disclosed`, explicit boolean; for `withheld`, `null` |
| `semantic_relevance` | Finite number in the provider's documented cosine range; selected records meet the provisional threshold |
| `memory_type` | One existing `MemoryType` value |
| `created_at` | Valid ISO 8601 timestamp with timezone |
| `lifecycle_state` | `active`, `reinforced`, `superseded`, or `archived` |
| `verification_state` | `unverified`, `verified`, or `disputed` |

Sprint 006 returns no public raw provenance or source text field. Public
excerpt disclosure uses the fixed `public-evidence-v1` policy. It first takes
the bounded 600-character view without changing the whole record supplied to
model context, then validates exact Unicode encoding and rejects uncertain or
matched filesystem paths, localhost or private-network URLs, any public or
private IP address, hostnames, tenant or account identifiers, credentials,
API keys, token-like or secret-like strings, and arbitrary nested metadata.
It does not partially redact an uncertain excerpt.

When the excerpt passes, `disclosure_status` is `disclosed`. When it does not,
the response still returns the safe alias and non-text allowlisted fields with
`disclosure_status: withheld`, `excerpt: null`, and
`excerpt_truncated: null`. This is the only excerpt-failure behavior. A failure
to construct even that closed safe record is evidence-packaging failure and
maps to `internal_contract_error` with no grounded response.

Withholding an excerpt does not remove the whole selected record from model
context or invalidate its internal citation. A grounded response may therefore
contain a cited `withheld` evidence alias when the answer and remaining public
fields pass disclosure validation.

The validated generated answer is subject to the same prohibited-value and
Unicode disclosure checks. Unsafe or uncertain answer text maps to
`generation_contract_error`; no answer or evidence is returned. Evidence must
never expose raw memory IDs, Qdrant point IDs, internal paths, URLs, network
addresses, hostnames, tenant identifiers, arbitrary metadata, secrets, raw
prompts, provider payloads, or full trace events.

## Retrieved-content trust boundary

The following are all untrusted data:

- user question
- memory content
- provenance text
- metadata
- provider response

Prompt construction creates four structural regions:

1. immutable system policy
2. a delimited user-question data region
3. individually delimited untrusted-evidence records
4. a provider-output schema and response-validation boundary

Evidence delimiters and record labels are generated by the application, not
copied from content. Source content is encoded so it cannot terminate or
create a trusted region. Instructions inside questions or evidence are data
and cannot override system policy.

No tools are registered or sent. The generation request grants no web,
scheduling, filesystem, shell, network-action, or external-execution
capability. Tests inspect the prompt structure and provider request
mechanically rather than treating compliant model behavior as the boundary.

## Generation identity and policy

### Required model inventory identity

```text
provider = Ollama
model_tag = qwen3:8b
digest = sha256:500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41
family = qwen3
parameter_size = 8.2B
quantization = Q4_K_M
advertised_context = 40960
required_capability = completion
thinking_capability = present but disabled
tool_capability = present but unauthorized
```

`qwen3:4b` is inventory-only and is never a fallback. The generation adapter
is configured with the mutable `qwen3:8b` tag. It inspects Ollama inventory and
requires the observed digest, family, parameter size, quantization, completion
capability, thinking policy, tool policy, and minimum context capacity of 8,192
tokens to match the values above before generation.

### Identity continuity

Ollama generation is invoked by mutable model tag. It is not atomic or
content-addressed execution and does not prove the exact digest that served a
request.

For every generation operation:

1. Preflight the current tag and record its observed digest, family, parameter
   size, quantization, context capacity, and completion capability.
2. Reject missing, malformed, ambiguous, changed, or insufficient observations
   before generation.
3. Issue one generation call by the approved tag with no fallback or retry.
4. Read and validate the complete bounded response.
5. Postflight the tag and record the same observed inventory fields after
   generation.
6. Classify continuity as `observed_consistent` only when every required
   preflight and postflight observation matches.
7. Discard the answer and return `generation_contract_error` if any observation
   differs or postflight evidence is missing or ambiguous.

Matching observations increase confidence that inventory did not visibly
drift; they do not cryptographically or atomically bind generation to an exact
digest. A residual race exists before, during, and after tag-based execution,
including a mutation that is reversed between observations. Controlled
operations must prevent model pulls, removals, and tag mutation during active
requests. No result survives an observed mismatch, missing or ambiguous
postflight evidence, or another continuity uncertainty.

Public policy metadata and trace metadata record the configured model tag,
preflight observed digest, postflight observed digest, and
`identity_continuity_status: observed_consistent`. This is observed inventory
continuity evidence, not proof of the serving artifact.

### Generation defaults

```text
think = false
stream = false
num_ctx = 8192
num_predict = 512
temperature = 0.1
seed = 42
top_k = 20
top_p = 0.9
repeat_penalty = 1.1
generation_timeout_seconds = 180
keep_alive = 10m
```

The 180-second value is one total wall-clock deadline from
`generation.started` through response-body read, provider-contract validation,
and the post-generation inventory observation. Timeout or cancellation
discards all partial output. Thinking output is never requested, stored,
logged, or returned. Tools are never registered or sent. `keep_alive = 10m`
retains model capacity after a request and must be included in memory and
concurrency planning.

Fixed parameters and seed improve repeatability under one stable runtime; they
do not make generated output deterministic or guarantee identical output
across Ollama versions, model runtimes, hardware, or provider changes.

## Token-capacity validation

The 12,000-character context budget is not a token guarantee. Before every
generation call, the implementation must calculate or provider-tokenize the
complete serialized request, including:

- system policy
- user-question wrapper
- evidence wrappers and whole records
- provider output-schema instructions
- prompt overhead
- answer reservation of 512 tokens

Generation proceeds only when the complete request plus answer reservation is
within `num_ctx = 8192`. Overflow returns `capacity_unavailable` before
generation. Evidence and prompt sections are not silently trimmed.

Implementation validation includes representative English and adversarial
Unicode/token-density fixtures. Maximum-bound representative input must fit;
any adversarial case that cannot fit must deterministically fail before the
provider call. Every request actually sent to Ollama must be proven within
8,192 tokens.

## Relevance calibration

The implementation branch must add a versioned, labeled, synthetic or
sanitized calibration fixture with at least 20 clearly relevant, 20 clearly
irrelevant, and 20 borderline query-memory judgments. It records:

- exact `nomic-embed-text:v1.5` model and approved manifest digest
- 768-dimensional, no-normalization, cosine geometry
- fixture version and provenance
- false-inclusion rate for clearly irrelevant pairs
- false-exclusion rate for clearly relevant pairs
- borderline score distribution
- threshold evaluation method

At `0.50`, implementation acceptance requires a false-inclusion rate no higher
than 5% and a false-exclusion rate no higher than 10% on the approved fixture.
Borderline outcomes are reported for review and are not relabeled to make the
threshold pass. Failure stops implementation acceptance and requires a
reviewed policy revision; it does not permit silent threshold tuning.

## Trace event and state-machine contract

### Exact event names

- `interaction.received`
- `retrieval.started`
- `retrieval.completed`
- `context.assembled`
- `generation.started`
- `generation.completed`
- `response.packaged`
- `interaction.failed`

### Common event fields

Every event contains only:

- `event_name`
- `trace_id`
- monotonically increasing `sequence`
- UTC `occurred_at`
- event-specific allowlisted numeric, enum, boolean, policy-version, and model
  identity fields

Duration fields are nonnegative integer milliseconds measured from a monotonic
clock. Wall-clock timestamps are informational and do not calculate duration.

### Event-specific fields

| Event | Allowed additional fields |
| --- | --- |
| `interaction.received` | `request_body_bytes`, `question_characters`, `requested_max_evidence` |
| `retrieval.started` | `candidate_limit`, embedding compatibility-key hash or approved public identity |
| `retrieval.completed` | `candidate_count`, `duration_ms` |
| `context.assembled` | `selected_count`, reason-code counts, `context_characters`, `duration_ms`, `context_policy_version` |
| `generation.started` | provider, configured model tag, preflight observed digest, family, parameter size, quantization, context capacity, capability, `num_ctx`, `num_predict`, `prompt_policy_version` |
| `generation.completed` | `duration_ms`, `response_body_bytes`, postflight observed tag, digest, family, parameter size, quantization, context capacity, capability, `identity_continuity_status` |
| `response.packaged` | result status, evidence count, `total_duration_ms` |
| `interaction.failed` | error code, failed stage, cancellation flag, `total_duration_ms` |

No trace contains the full or partial question, source content, provenance
text, prompt, answer, provider thinking output, arbitrary metadata, private
endpoint, or exception body by default.

### Ordering and cardinality

- `interaction.received` occurs exactly once and is first.
- Each started, completed, assembled, or packaged event occurs at most once.
- `retrieval.completed` requires an earlier `retrieval.started`.
- `context.assembled` requires `retrieval.completed`.
- `generation.completed` requires `generation.started`.
- `response.packaged` requires `context.assembled` and is terminal for
  `grounded` or `insufficient_evidence`.
- `interaction.failed` may follow any nonterminal state and is the only
  terminal event for failure.
- Exactly one terminal event exists.
- No event follows a terminal event.

For `insufficient_evidence`, no generation event occurs. For failure,
`response.packaged` is absent; it must never imply success after
`interaction.failed`.

Cancellation propagates to retrieval or generation, prevents later provider
or packaging work, records `interaction.failed` with `request_cancelled` when
the trace exists, and never reports success.

### Trace retention

Telemetry is not a durable interaction store. Trace events may be retained for
at most seven days in an approved access-controlled operational telemetry
sink, then deleted. If no such sink is approved, events are process-ephemeral
only. The repository, Qdrant, and interaction domain do not persist traces.

## Capacity and operational safeguards

The following controlled-use defaults are proposed and remain provisional
until sanitized Python 3.12 VM performance evidence is reviewed:

```text
maximum_request_body_bytes = 16384
maximum_provider_response_bytes = 262144
maximum_concurrent_generation_requests = 1
maximum_queued_generation_requests = 2
maximum_queue_wait_seconds = 5
retrieval_timeout_seconds = 10
generation_timeout_seconds = 180
maximum_interaction_seconds = 195
```

- Request bytes are bounded before or while JSON is parsed.
- Provider bodies are streamed only into a bounded accumulator despite
  `stream = false`; exceeding the bound fails and discards the body.
- One process admits at most one active generation and two bounded waiters.
- A full queue or queue-wait expiry returns `capacity_unavailable` without a
  provider call.
- Cancellation removes queued work or interrupts the active request and
  discards partial output.
- The overall deadline includes queueing, retrieval, assembly, generation,
  validation, and packaging. The 180-second generation subdeadline remains a
  total wall-clock limit.
- Load shedding does not retry, fall back, or persist the request.
- Ten-minute keep-alive resource residency is measured before concurrency is
  raised.

No capacity default authorizes production deployment.

## Information ownership, retention, and side effects

- The user question is temporary untrusted request data.
- Retrieved memory records retain the ownership and governance defined by the
  memory architecture.
- Context decisions, prompts, provider responses, answers, and traces are
  temporary derived information.
- Public evidence is a bounded derived view of selected memory records.
- A grounded result does not change verification, lifecycle, confidence,
  importance, or source authority.
- Questions, prompts, answers, traces, and interaction records are not written
  to Qdrant, files, databases, logs, or another durable store.
- The only intended external side effect is one bounded Ollama completion
  request after retrieval and all preflight checks pass.

## Proposed architecture decisions

- [ADR 0006: Canonical Interaction Domain and Dependency Direction](adr/0006-canonical-interaction-domain-and-dependency-direction.md)
- [ADR 0007: Grounded Response and Evidence Contract](adr/0007-grounded-response-and-evidence-contract.md)
- [ADR 0008: Deterministic Retrieval and Context Assembly](adr/0008-deterministic-retrieval-context-assembly.md)
- [ADR 0009: Retrieved Content Trust Boundary](adr/0009-retrieved-content-trust-boundary.md)
- [ADR 0010: Generation Model Identity and Policy Defaults](adr/0010-generation-model-identity-and-policy-defaults.md)

All five ADRs remain `Proposed`. Nothing in this specification is current
runtime behavior until the required decisions are accepted, implementation is
separately authorized, reviewed code merges, and documentation closeout
records the result.

## Definition of Done and authority gates

Sprint 006 implementation cannot begin until:

- ADRs 0006 through 0010 are `Accepted`
- Work Mode approves the exact proposal head
- the Chief Architect approves the exact proposal head
- the proposal pull request merges
- implementation authorization is issued separately

Sprint 006 implementation cannot merge until:

- every requirement in
  [Sprint 006 Validation Requirements](SPRINT_006_VALIDATION_REQUIREMENTS.md)
  passes
- Work Mode independently reviews the exact implementation head
- the Chief Architect gives exact-head merge approval
- Codex performs the controlled merge and verifies the merged state
- Documentation Suite closeout follows

Proposal approval is not implementation, merge, deployment, or live-system
authority.

## Stop conditions

Stop proposal or future implementation work when:

- any proposed ADR or canonical document conflicts
- the interaction domain can access a write-capable memory object
- endpoint, request, result, reason, trace, or failure contracts diverge
- candidate conflicts can be resolved by input order
- source content can be silently truncated for model context
- a prompt or sent request can exceed 8,192 tokens
- a generation result can survive uncertain model continuity
- tools, thinking output, retry, or fallback appear
- a question, prompt, answer, trace, or interaction record can persist
- validation requires live Qdrant mutation, Ollama inventory mutation, secrets,
  private topology, or deployment

## Chief Architect acceptance record

On 2026-08-01, the Chief Architect accepted the Sprint 006 Proposal v2
architecture in pull request 43 at exact head
`288b248fd660785bed25d9afbee1800f13f2bc99`.

Acceptance is limited to the existing documentation-only 16-file proposal
manifest at that exact head: the bounded Phase 2 interaction scope, ADRs 0006
through 0010, validation requirements, and the related canonical status,
architecture, navigation, roadmap, and changelog updates. It does not broaden
the proposal or change its implementation requirements.

ADRs 0006 through 0010 remain `Proposed` until the proposal merges to `main`.
This acceptance does not authorize Sprint 006 implementation, deployment,
live-system work, or any runtime change. Merge authorization has not been
granted.

Recording this acceptance creates a new branch head and therefore requires
final exact-head review before any later merge authorization. It does not
itself authorize merge or implementation.

## Review and chain of custody

This proposal receives independent review only after all proposal artifacts
and index updates are committed and pushed to one remote branch at one exact
head. The review packet must include the repository, base and head commits,
branch, pull request, complete manifest, repository-backed compare target,
validation, requested decision, exact next action, and confirmation that no
uncommitted or untracked artifact is required to interpret the proposal.

The [Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
remains authoritative for review independence, blocker disposition, approval,
merge, and closeout.
