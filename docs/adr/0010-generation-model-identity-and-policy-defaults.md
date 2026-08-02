# ADR 0010: Generation Model Identity and Policy Defaults

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-01

**Decision owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect

## Decision summary

If accepted, Sprint 006 generation will invoke the configured mutable Ollama
tag `qwen3:8b` under one versioned policy. Immediately before and after every
generation, it will record and compare the required observed inventory fields,
including digest
`sha256:500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`.
Matching observations are inventory-continuity evidence, not cryptographic or
atomic proof of the artifact that served the request. Drift or uncertainty
discards output. There is no fallback model, automatic retry, thinking, or
tool use.

## Context

Model tags can be repointed while a service is running. A startup-only check
would create an authorization window in which later requests could use a
different artifact. Conversely, claiming that separate identity checks and a
generation request are atomic would overstate what the Ollama HTTP API proves.
Sprint 006 therefore needs an explicit configured tag and expected inventory
contract, a fail-closed drift policy, and an honest residual-race statement.

### Required configured and observed inventory values

- provider: Ollama;
- tag: `qwen3:8b`;
- canonical digest:
  `sha256:500a1f067a9f782620b40bee6f7b0c89e17ae61f686b92c24933e4ca4b2b8b41`;
- family: `qwen3`;
- parameter size: `8.2B`;
- quantization: `Q4_K_M`;
- advertised context length: 40,960 tokens;
- authorized operation: completion;
- thinking: disabled;
- tools: unauthorized.

`qwen3:4b` is inventory information only. It is not an authorized fallback or
compatible generation identity.

## Scope

This decision defines the configured tag, required observed inventory fields,
digest normalization, per-operation observations, residual race handling,
request defaults, capacity controls, timeouts, failure behavior, and validation
evidence for Sprint 006.

## Non-goals

- changing the Sprint 005 embedding model or vector compatibility contract;
- model installation, deletion, pull, or live inventory mutation;
- fallback routing, automatic retry, or model selection;
- reasoning-mode or tool-enabled generation;
- claiming transactional identity binding that Ollama does not provide.

## Decision drivers

- The configured tag and expected inventory fields must be explicit.
- A mutable tag must never hide an observed inventory mismatch.
- Observed drift or continuity uncertainty must fail before evidence is
  presented as grounded.
- Request configuration must be fixed and reviewable.
- Capacity limits must protect the local service without becoming hidden policy.

## Decision

### Configured tag and observed inventory contract

The adapter is configured with provider Ollama and mutable tag `qwen3:8b`.
Preflight and postflight observations must each contain the tag, canonical
SHA-256 digest, family, parameter size, quantization, context capacity,
completion capability, thinking mode, and tool policy listed above. The
unversioned alias `:latest` is prohibited. The expected tuple is an inventory
acceptance contract; it is not a content-addressed generation target.

Ollama may report the digest as 64 bare lowercase or uppercase hexadecimal
characters. The adapter must validate exact length and hexadecimal syntax,
lowercase it, prefix `sha256:`, and compare the resulting canonical string for
exact equality. Missing, malformed, incorrectly sized, or wrong digests fail
closed.

### Per-operation observation and continuity classification

For every generation operation:

1. inspect the current `qwen3:8b` inventory entry;
2. canonicalize and record the preflight observed tag, digest, family,
   parameter size, quantization, context capacity, and capability;
3. reject a missing, malformed, ambiguous, or mismatched observation as
   `generation_provider_not_ready` before provider invocation;
4. invoke completion once by the configured tag;
5. inspect and record the same observed fields after generation;
6. classify continuity as `observed_consistent` only when every required
   preflight and postflight observation matches;
7. discard output and return `generation_contract_error` if postflight differs
   or is missing or ambiguous.

Readiness checks are diagnostic only and do not authorize later generation.
Inventory observation must not use a permanent success cache.

### Residual race and operational control

The pre-check, generation call, and post-check are separate HTTP operations.
Matching observations increase confidence that inventory did not visibly
drift. They cannot cryptographically or atomically prove which exact digest
served the request. A residual race remains before, during, and after tag-based
generation, including mutation that is reversed between inspections.

The operational deployment must prevent model inventory mutation while the
interaction service accepts traffic. Pull, delete, copy, and tag-management
operations require a maintenance boundary that drains or stops interaction
traffic. Postflight observation remains mandatory defense in depth. If
controlled mutation cannot be demonstrated in the validation environment,
implementation approval remains blocked.

Public policy and trace metadata report the configured model tag, preflight
observed digest, postflight observed digest, and
`identity_continuity_status: observed_consistent`. This metadata reports
observed inventory continuity only, never proof of the serving artifact.

### Generation policy

The prompt policy ID is `grounded-answer-v1`. Each request uses exactly:

- `think: false`;
- `stream: false`;
- `num_ctx: 8192`;
- `num_predict: 512`;
- `temperature: 0.1`;
- `seed: 42`;
- `top_k: 20`;
- `top_p: 0.9`;
- `repeat_penalty: 1.1`;
- provider timeout: 180 seconds;
- `keep_alive: 10m`.

The provider response-body limit is 262,144 bytes. Output beyond the structured
contract or body limit maps to `generation_contract_error`.

Fixed parameters and seed improve repeatability under one stable runtime. They
do not make generation deterministic or guarantee identical output across
Ollama versions, model runtimes, hardware, or provider changes.
Reproducibility means configuration, policy, evidence selection, and observed
inventory metadata are recorded sufficiently for investigation and replay
attempts, not that a replay returns identical text.

### Failure behavior

There is one provider attempt. Automatic retries and fallback models are
prohibited. Failures map to the public codes defined by ADR 0007:

- unavailable or connection failure: `generation_unavailable`;
- provider timeout after readiness: `generation_unavailable`;
- malformed or unsupported structured output, response-body overflow, unsafe
  answer disclosure, or citation/evidence mismatch:
  `generation_contract_error`;
- pre-operation identity mismatch: `generation_provider_not_ready`;
- post-operation identity mismatch or uncertainty: `generation_contract_error`.

No failed or drifted output may be returned as grounded.

### Capacity safeguards

The proposed initial service limits are:

- maximum concurrent generation operations: 1;
- maximum queued operations: 2;
- maximum queue wait: 5 seconds;
- retrieval timeout: 10 seconds;
- generation timeout: 180 seconds;
- whole-interaction deadline: 195 seconds;
- request-body limit: 16,384 bytes.

Queue overflow or expiry returns `capacity_unavailable`. The whole-request
deadline bounds retrieval, assembly, generation, inventory observations, and
response validation. Client cancellation maps to `request_cancelled`, stops
downstream work where possible, and prevents persistence or a partial grounded
response.

The 40,960-token advertised model capability does not authorize using that
capacity. Sprint 006 fixes `num_ctx=8192`; validation must prove the worst-case
rendered prompt plus 512-token output allowance fits that configured window.

## Alternatives considered

### Authorize the tag without a digest

Rejected because tags are mutable and do not identify a compatible artifact.

### Verify once at startup

Rejected because later tag drift would remain permanently authorized.

### Use `qwen3:4b` as a fallback

Rejected because it is a different artifact and changes output behavior without
an approved compatibility contract.

### Retry automatically on provider failure

Rejected because it changes latency and duplicate-work behavior and can mask
identity or capacity failures.

### Claim pre/post observations bind the serving artifact

Rejected because the provider does not bind inventory observation and
completion in one transaction. Matching observations do not prove which digest
served generation.

### Use the advertised 40,960-token context

Rejected for this sprint because it would expand capacity and validation scope;
the bounded 8,192-token policy is sufficient for the proposed proof.

## Consequences

### Positive

- Generation uses one explicit configured tag, expected inventory tuple, and
  policy.
- Observed model drift fails visibly rather than degrading silently.
- Request configuration and resource limits are mechanically testable.
- The design makes no unsupported serving-artifact or atomicity claim.

### Negative

- A post-check outage discards otherwise readable output.
- No fallback reduces availability.
- Maintenance must coordinate model inventory mutation with traffic draining.
- A narrow reversed-mutation race remains and is explicitly documented.

## Data, security, and privacy implications

Inventory responses and policy identifiers may be recorded as validation
evidence after secrets and private topology are removed. Prompts, questions,
evidence content, and generated answers are excluded from default logs.

## Operational implications

Readiness must expose identity mismatch without caching authorization. The
service image must include no model-management capability. Operators need a
documented, non-live validation environment for digest and drift tests.

## Compatibility and migration

This generation inventory-observation contract is independent of the accepted
Sprint 005 embedding identity `nomic-embed-text:v1.5`. No vector, memory
payload, or Qdrant migration is required. A future configured model or expected
digest requires a new reviewed decision and policy validation.

## Validation requirements

- exact Ollama inventory-shape observed-digest canonicalization tests;
- wrong, missing, malformed, and incorrectly sized digest failures;
- pre-check failure proving no completion call;
- post-check drift proving output is discarded;
- missing or ambiguous postflight evidence proving output is discarded;
- readiness-cache regression proving every operation rechecks identity;
- metadata assertions for configured tag, both observed digests, and
  `observed_consistent` without serving-artifact claims;
- wording assertions rejecting atomic digest binding, content-addressed
  execution, serving-artifact proof, deterministic generation, and guaranteed
  identical output;
- exact generation option and prompt-policy assertions;
- no retry, fallback, thinking, or tool assertions;
- timeout, response-body limit, cancellation, queue, and deadline tests;
- worst-case 8,192-token capacity proof;
- controlled-inventory container or integration evidence without live mutation.

## Related decisions and documents

- [Sprint 006 specification](../SPRINT_006_SPECIFICATION.md)
- [Sprint 006 validation requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)
- [ADR 0004](0004-embedding-model-identity-and-vector-compatibility.md)
- [ADR 0007](0007-grounded-response-and-evidence-contract.md)
- [ADR 0009](0009-retrieved-content-trust-boundary.md)

## Review record

This ADR is a proposal on the Sprint 006 Proposal v2 custody branch. It does
not authorize implementation, model inventory changes, deployment, or live
validation. Exact-head Work Mode review and Chief Architect acceptance remain
required.
