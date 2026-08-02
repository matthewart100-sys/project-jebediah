# Sprint 006 Validation Requirements

**Status:** Proposed

**Proposal identity:** Sprint 006 Proposal v2

**Canonical proposal base:**
`693a42299d7caff016b78bc9c45ffb5d1a5537e0`

**Implementation status:** Unauthorized

**Deployment status:** Unauthorized

## Purpose

This document defines the evidence required to accept the Sprint 006
architecture proposal and, only after separate authorization, to accept a
future implementation. It validates the bounded Phase 2 interaction path in
[the Sprint 006 specification](SPRINT_006_SPECIFICATION.md) without treating
proposal text as implemented behavior.

Validation must prove governed retrieval, deterministic whole-record context
assembly, safe evidence-grounded generation, read-only memory access, exact
model-policy identity, and honest failure. It must not contact or mutate live
Qdrant data, modify the live Ollama inventory, deploy a service, or persist
interaction data.

## Governing proposed decisions

- [ADR 0006: Canonical Interaction Domain and Dependency Direction](adr/0006-canonical-interaction-domain-and-dependency-direction.md)
- [ADR 0007: Grounded Response and Evidence Contract](adr/0007-grounded-response-and-evidence-contract.md)
- [ADR 0008: Deterministic Retrieval and Context Assembly](adr/0008-deterministic-retrieval-context-assembly.md)
- [ADR 0009: Retrieved Content Trust Boundary](adr/0009-retrieved-content-trust-boundary.md)
- [ADR 0010: Generation Model Identity and Policy Defaults](adr/0010-generation-model-identity-and-policy-defaults.md)

All five ADRs must remain `Proposed` throughout proposal review. Future
implementation waits until every ADR is accepted and implementation is
separately authorized.

## Evidence categories

### Proposal evidence

Proposal evidence proves the documentation package is complete, internally
consistent, reviewable at an immutable exact head, and limited to architecture.
It does not prove runtime behavior.

### Deterministic implementation evidence

Future unit, API, package, prompt, state-machine, and interaction-count tests
use synthetic inputs and controlled test doubles. Ordinary validation must
block unapproved network access.

### Calibration and capacity evidence

Versioned synthetic or sanitized fixtures measure retrieval policy and token
capacity under exact model identities. Fixture provenance, identity, method,
and acceptance criteria must be reviewable without exposing live memory data.

### Container evidence

An isolated Python 3.12 image build proves packaging and import boundaries. It
must not connect to live Qdrant or Ollama or deploy the service.

### Operational evidence

Capacity measurements may be produced later on an authorized isolated VM with
synthetic content. Sanitized results may refine provisional concurrency,
queue, deadline, response-size, or keep-alive defaults only through review.
No operational evidence in Sprint 006 authorizes production deployment.

## Proposal-package validation

Before Work Mode review, the proposal branch must prove:

- the two Sprint documents and ADRs 0006 through 0010 exist and are tracked
- every new ADR uses its final number and has `Status: Proposed`
- ADRs 0001 through 0005 are unchanged
- the specification, ADRs, roadmap, current status, current architecture,
  memory architecture, ADR index, and documentation navigation agree
- Sprint 006 is a Phase 2 memory-client validation, not Phase 6 Reasoning
  Engine work
- Proposal v2 is newly authored and never represented as recovered or
  continued Proposal v1
- all seven historical Work Mode findings map to explicit requirements
- implementation, deployment, merge, live Qdrant access, Ollama inventory
  mutation, and Sprint 006 runtime work remain unauthorized
- only documentation files are changed
- no sensitive values, private topology, live payloads, or transient review
  artifacts are included

The proposal-specific assertions must check exact endpoint, result states,
failure codes, reason codes, trace events, context defaults, generation
identity, generation defaults, authority gates, and the historical-input
mapping across the package.

## Baseline characterization before future implementation

A separately authorized implementation must begin with tests that record:

- exact reviewed base commit and accepted proposal commit
- current 142-test baseline or the then-current full count
- current `/health`, `/memory/store`, and `/memory/context` behavior
- absence of `/interactions/query`
- absence of `src/collector/interaction/`
- `collector.memory` canonical import origin
- service composition and Python 3.12 packaging behavior
- semantic-only retrieval ordering
- `RetrievalCandidate` fields and Qdrant compatibility checks
- one current store-capable `MemoryApplicationService`, demonstrating why it
  is prohibited as the interaction dependency
- zero existing persistence of questions, prompts, answers, interaction
  traces, or interaction records
- no lifecycle, verification, or ranking automation

Characterization is evidence, not permission to change these contracts.

## Unit-test requirements

Focused deterministic tests must cover:

- question and request-size validation boundaries
- Unicode scalar counting and whitespace-only rejection
- optional `max_evidence` default and integer range
- boolean, extra-field, and unsupported-option rejection
- result construction for exactly three states
- stable error-code classification and safe messages
- public evidence allowlist, encoding, and every length limit
- public excerpt creation and exact `excerpt_truncated` behavior
- provider response schema and citation validation
- answer length, missing citation, unknown citation, duplicate citation, and
  extra provider-field rejection
- policy and model identity packaging
- monotonic duration calculation and trace-sequence validation

Tests must never assert a provider answer is true merely because its contract
is valid.

## API contract tests

Contract tests must freeze:

- `POST /interactions/query`
- no alternate Sprint 006 route
- JSON request with only `question` and optional `max_evidence`
- maximum 16,384-byte request body before or during parsing
- maximum 2,000-character question
- optional `max_evidence` default `5` and allowed range `1` through `5`
- closed request and response schemas
- exactly `grounded`, `insufficient_evidence`, and `failed`
- grounded, insufficient, and failed field requirements
- stable error codes and HTTP mappings
- normalization of FastAPI validation errors into `failed` plus
  `invalid_request`
- request cancellation using HTTP 499 when a response remains possible and no
  response after a disconnected client
- compatibility of existing `/health`, `/memory/store`, and `/memory/context`

API tests must prove no partial answer or evidence appears in failed results.

## Architecture-boundary tests

Static import and interaction tests must prove:

- `src/collector/interaction/` is the sole interaction-domain implementation
- the interaction domain imports no FastAPI or service-local application
  module
- the interaction domain imports no Qdrant client type or direct embedding
  provider implementation
- FastAPI owns transport, configuration, dependency construction, and HTTP
  translation only
- `src/collector/memory/` remains the only semantic retrieval domain
- the memory domain implements the narrow read-only retrieval protocol
- the protocol exposed to interaction has search/query behavior only
- no store-capable `MemoryApplicationService`, Qdrant repository, or memory
  writer is injected into interaction
- no second retrieval or semantic-ranking implementation exists
- n8n receives no privileged package, workflow, or internal interface; it is
  only a possible external HTTP client
- service and container imports resolve canonical installed packages

Forbidden-member and protocol-surface tests must fail if `store`, `save`,
`index`, `upsert`, `delete`, verification-transition, or lifecycle-transition
behavior enters the interaction dependency.

## Prompt-structure tests

Tests inspect the exact structured generation request and prove:

- system policy is a distinct trusted region
- user question is encoded inside a delimited untrusted data region
- every evidence record has an application-generated label and delimiter
- source content cannot close or create a trusted region
- evidence instructions remain data and cannot modify generation settings
- provider output-schema instructions are separate from evidence
- `think` is false
- no tool definitions, tool choice, web access, file access, scheduling, or
  external action are sent
- raw prompt, question, evidence, answer, or thinking output does not enter
  logs or traces

Adversarial fixtures include delimiter-looking content, prompt injection,
JSON fragments, Markdown instructions, role-like labels, control characters,
and very long untrusted strings. Tests must not rely only on a model choosing
to ignore them.

## Duplicate-integrity tests

Tests must cover:

- one unique candidate
- multiple unique candidates
- two fully identical candidates with the same memory ID
- identical duplicates in every input permutation
- the same ID with different content
- the same ID with different semantic relevance
- the same ID with different memory type, creation time, lifecycle,
  verification, provenance, supporting evidence, or public-evidence metadata
- three or more candidates containing identical and conflicting copies
- conflict discovered before record-limit or character-budget selection

Identical duplicates collapse to one deterministic candidate and record
`duplicate_identical`. Any material conflict produces
`context_integrity_error`, records `duplicate_conflict`, causes zero generation
calls, and exposes no conflicting raw content.

## Context-decision reason-code tests

Every stable reason must have focused and combination coverage:

- `selected`
- `below_threshold`
- `duplicate_identical`
- `duplicate_conflict`
- `record_limit`
- `individual_oversize`
- `aggregate_budget_exhausted`
- `malformed_candidate`

Tests prove every bounded input candidate has exactly one final decision,
reason precedence is deterministic, input order does not change selected IDs
or reasons, and rejected content is absent from logs and traces.

## Whole-record and public-excerpt tests

Tests must prove:

- only whole records enter model context
- content at 8,000 characters may be selected when the complete rendered
  context fits
- content over 8,000 characters is excluded as `individual_oversize`
- the 12,000-character budget counts wrappers, delimiters, and metadata
- no source or rendered evidence block is trimmed to fit
- a later smaller candidate is considered deterministically after an earlier
  candidate does not fit
- public excerpts stop at 600 Unicode scalar values
- `excerpt_truncated` is false for exact or shorter content and true only for
  longer selected content
- public excerpt truncation never changes the model-context record

## Trace state-machine tests

State-machine tests must validate exact events:

- `interaction.received`
- `retrieval.started`
- `retrieval.completed`
- `context.assembled`
- `generation.started`
- `generation.completed`
- `response.packaged`
- `interaction.failed`

Required cases include grounded success, insufficient evidence, invalid
request, retrieval failure, context conflict, capacity failure, preflight
identity failure, generation failure, provider-contract failure, timeout, and
cancellation during queueing, retrieval, generation, and packaging.

Tests prove:

- event ordering and at-most-once cardinality
- exactly one terminal event
- completion never precedes its start event
- insufficient evidence has no generation events
- failure terminates with `interaction.failed`
- `response.packaged` never follows or implies success after failure
- `interaction.failed.error_code` matches the public failure code when a
  response is possible
- durations are nonnegative monotonic-clock values
- only event-specific allowlisted fields are present
- traces exclude full or partial question, content, provenance, prompt,
  answer, provider body, thinking output, exception body, paths, and endpoints
- telemetry is process-ephemeral or retained no longer than seven days in an
  approved sink

## Retrieval calibration fixture

Implementation acceptance requires a versioned synthetic or sanitized fixture
with at least:

- 20 clearly relevant judgments
- 20 clearly irrelevant judgments
- 20 borderline judgments
- exact query and candidate labels
- expected class and rationale
- fixture version, authoring method, and safe provenance
- exact embedding provider, model, manifest digest, dimensions,
  normalization, and distance

The calibration run records raw score distributions and computes false
inclusion and false exclusion at the provisional `0.50` threshold.

Acceptance criteria are:

- false-inclusion rate no higher than 5% for clearly irrelevant pairs
- false-exclusion rate no higher than 10% for clearly relevant pairs
- every score is finite and produced under the exact ADR 0004 identity
- borderline outcomes are reported without relabeling
- the fixture and calculation are reproducible from tracked inputs

Failure blocks implementation acceptance. It does not authorize silent
threshold adjustment.

## Token-capacity fixtures

Fixtures must evaluate the complete serialized provider request, including
system policy, question wrapper, evidence wrappers, provider-output schema,
prompt overhead, and 512-token answer reservation.

Required cases include:

- representative English questions and evidence
- maximum-length English question
- maximum selected record count
- maximum individual record
- near-maximum aggregate rendered context
- worst-case or adversarial Unicode/token-density strings
- delimiter-heavy and structured-data evidence
- prompt and evidence-wrapper overhead changes

For every request sent to the provider, measured tokens plus the answer
reservation must be no greater than `8192`. A fixture that cannot fit must
produce `capacity_unavailable` before generation, with no silent evidence or
prompt trimming. The tokenizer or provider-counting method, version, and
measurement uncertainty are recorded.

## Generation identity tests

The proposed required identity is:

```text
provider = Ollama
model_tag = qwen3:8b
digest = sha256:500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41
family = qwen3
parameter_size = 8.2B
quantization = Q4_K_M
advertised_context = 40960
required_capability = completion
```

Controlled doubles using the real Ollama inventory response shape must prove:

- exact preflight identity passes
- wrong, missing, malformed, or incorrectly sized digest fails
- wrong tag, family, parameter size, quantization, capability, or insufficient
  context fails
- thinking present is accepted only with `think = false`
- tool capability present grants no tool authority
- `qwen3:4b` remains inventory-only and never receives a call
- identity is rechecked before every generation
- post-generation exact identity passes
- tag or digest drift after preflight discards the result
- missing or failed postflight inspection discards the result
- no automatic retry or fallback occurs after any failure
- no result is reported as grounded when continuity is uncertain

Tests record the residual inspection-to-execution race rather than asserting
atomic content-addressed generation.

## Generation-policy and provider-contract tests

Configuration consistency tests require exactly:

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

Tests prove all values are sent once and cannot be overridden by a request or
evidence record. The bounded provider response accepts only the approved
answer-and-citation schema, rejects extra or malformed fields, never requests
or accepts thinking output, and never sends tools.

## Cancellation, timeout, and response-size tests

Tests cover:

- cancellation before retrieval
- cancellation during retrieval
- cancellation while queued
- cancellation during provider connection, body read, validation, and
  postflight identity check
- retrieval timeout
- 180-second total wall-clock generation timeout
- 195-second total interaction timeout
- provider body exactly at and one byte above 262,144 bytes
- partial provider body before timeout, cancellation, disconnect, or overflow

Every case discards partial output, emits the correct terminal trace, performs
no retry or fallback, and returns no successful result. A disconnected client
may receive no response, but internal state must never record success.

## Concurrency, backpressure, and capacity tests

Deterministic concurrency tests prove the provisional controlled-use defaults:

- one active generation request
- at most two queued generation requests
- five-second maximum queue wait
- immediate load shedding after the bounded queue is full
- cancellation removes a waiter without leaking capacity
- permits are released after success and every failure path
- no request exceeds its total deadline while waiting
- `capacity_unavailable` maps to HTTP 503
- keep-alive effects are measured before concurrency is raised

Tests use controlled clocks and provider doubles; they do not load a live
model during ordinary validation.

## Zero-write interaction counts

Success and every failure-path test must record interactions with memory and
provider doubles. They must prove:

- one read-only retrieval call for valid requests that reach retrieval
- zero memory writes for grounded responses
- zero memory writes for insufficient evidence
- zero memory writes for invalid request, retrieval failure, context failure,
  capacity failure, provider failure, contract failure, timeout, and
  cancellation
- zero Qdrant write, lifecycle transition, verification transition, memory
  store, interaction store, file write, and trace-store call
- zero generation calls for invalid request, retrieval failure, context
  failure, insufficient evidence, token overflow, and failed preflight
- one generation call at most for a valid grounded attempt

Questions, prompts, answers, traces, provider bodies, and interaction records
must not persist after any case.

## Failure and insufficient-evidence tests

### Retrieval failure

Embedding or Qdrant search failure produces `retrieval_unavailable`, HTTP 503,
no generation, no evidence, and no partial answer.

### Insufficient evidence

Zero usable selected records produces `insufficient_evidence`, `answer: null`,
`evidence: []`, no generation events or call, and successful terminal
`response.packaged`.

### Generation readiness failure

Preflight identity or capability failure produces
`generation_provider_not_ready`, HTTP 503, and no provider generation request.

### Generation failure

Provider transport or service failure after readiness produces
`generation_unavailable`, HTTP 503, with no retry or partial output.

### Context and provider-contract failure

Candidate conflict produces `context_integrity_error`. Invalid provider body,
citation mismatch, response overflow, or failed postflight continuity produces
`generation_contract_error`. Both return HTTP 500 and no successful payload.

## Python 3.12 container validation

After separately authorized implementation, an environment with Docker must
build the repository-root service image from the exact implementation head:

```text
docker build --pull --no-cache --tag jebediah-memory:sprint-006-review --file services/jebediah-memory/Dockerfile .
```

An import smoke must prove:

- Python 3.12
- `collector.memory` and `collector.interaction` resolve from installed
  `site-packages`
- no `/app/collector` service-local shadow tree exists
- `main.py` imports from `/app/main.py`
- the smoke contacts no live Qdrant or Ollama service

The exact smoke command is finalized with implementation so it can construct
only inert test doubles and avoid application lifespan network access.

## Full validation commands

The proposal branch runs at minimum:

```text
uv run --frozen pytest -q
uv run --frozen python -m compileall -q src services tests
python scripts/validate_docs.py
uv lock --check
git diff origin/main...HEAD --check
```

It also runs explicit local-link validation, proposal-contract assertions,
configuration-consistency assertions, scope inspection, ADR 0001-0005
preservation, and sensitive-value review. The base-to-head command runs after
the proposal is committed so it evaluates the immutable review target.

A future implementation reruns the complete frozen suite, focused interaction
tests, compilation, documentation, links, lockfile, package/import, container,
diff, scope, ADR, and sensitive-data checks.

## Phase checkpoints and rollback

| Checkpoint | Required evidence | Rollback point |
| --- | --- | --- |
| Proposal package | Complete exact-head documents, proposed ADRs, validation, and independent review | Reviewed `main` at the proposal base |
| Characterization | Existing APIs, package boundaries, test count, and zero interaction persistence recorded | Accepted proposal merge |
| Domain contracts | Interaction models, read-only retrieval port, reason codes, trace state machine, and tests pass without service cutover | Characterization commit |
| Adapter and prompt boundary | Generation identity, prompt structure, response validation, calibration, and token fixtures pass through controlled doubles | Domain-contract commit |
| Service cutover | One route composes canonical packages; API, zero-write, timeout, cancellation, and capacity tests pass | Adapter commit |
| Container and final review | Full suite and Python 3.12 canonical import origin pass at exact implementation head | Pre-service-cutover commit or Git revert; no live data was changed |

Failure at a checkpoint stops the next phase. No checkpoint authorizes
deployment or live-data mutation.

## Stop conditions

Stop proposal review or implementation acceptance when:

- an ADR is accepted prematurely or ADRs 0001 through 0005 change
- implementation begins without separate authorization
- a runtime, test, dependency, Docker, Compose, or live-system change enters
  the proposal branch
- the public endpoint or result states diverge
- candidate order changes a conflict or selection outcome
- a reason code, trace event, identity, or policy default is missing or
  inconsistent
- model context truncation, automatic retry, fallback, thinking output, or
  tool registration appears
- a request can reach generation over token capacity
- model continuity uncertainty can return a result
- any interaction path can write memory or persist interaction data
- a required fixture uses unsanitized live content
- sensitive values or private topology enter review artifacts
- the exact remote proposal head or complete manifest cannot be recovered

## Review and authority gates

Sprint 006 implementation cannot begin until:

- ADRs 0006 through 0010 are accepted
- Work Mode approves the exact proposal head
- the Chief Architect approves the exact proposal head
- the proposal pull request merges
- implementation authorization is issued separately

Sprint 006 implementation cannot merge until:

- every applicable requirement in this document passes
- Work Mode independently reviews the exact implementation head
- the Chief Architect grants exact-head merge approval
- Codex performs and verifies the controlled merge
- Documentation Suite closeout follows

The proposal branch, its validation, and any proposal approval do not authorize
implementation, deployment, live access, or merge.

## Evidence handoff

Every review packet records:

- repository and authoritative remote
- current sprint status and workstream
- base branch and full commit
- head branch and full commit
- pull request and compare target
- complete artifact manifest
- related ADR statuses
- exact commands, results, counts, and environment
- scope, non-goals, risks, blockers, and sensitive-evidence handling
- requested decision and exact next action
- clean status and confirmation that no uncommitted or untracked artifact is
  required to interpret the proposal
