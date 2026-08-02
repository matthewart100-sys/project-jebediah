# ADR 0009: Retrieved Content Trust Boundary

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-01

**Decision owner:** Chief Architect

**Reviewers:** Work Mode and Chief Architect

## Decision summary

If accepted, every retrieved memory field will be treated as untrusted data,
never as an instruction. Sprint 006 will place retrieved content in a
structurally isolated prompt region, encode boundary markers, prohibit tools
and side effects, validate provider output against selected evidence IDs, and
return only an allowlisted evidence view.

## Context

Memories can contain quoted instructions, markup, delimiter-like strings, or
malicious prompt-injection text. Provenance and verification metadata describe
governance state; they do not make content safe to execute. Passing retrieved
text directly into a generation prompt can collapse the boundary between
application policy and evidence.

### Verified facts

- Existing memory records may contain arbitrary user- or system-originated
  text.
- Sprint 006 generation is a read-only consumer of selected memory evidence.
- No tool use, write operation, or autonomous verification is authorized.
- The public API must not expose raw internal payloads or private metadata.

## Scope

This decision governs prompt construction, delimiter handling, provider
capabilities, output validation, evidence exposure, logging, and adversarial
validation for Sprint 006.

## Non-goals

- proving that retrieved content is factually true;
- sanitizing or rewriting canonical memory records;
- adding access-control, classification, or redaction architecture;
- enabling tools, agents, browsing, writes, or verification;
- defending an unrestricted autonomous reasoning engine.

## Decision drivers

- Retrieved content must not override system policy.
- Prompt boundary behavior must be mechanically testable.
- Generation must remain incapable of side effects.
- Public output must cite only evidence actually selected for the prompt.
- Sensitive operational data must not enter logs or responses accidentally.

## Decision

### Trust classification

Question text, memory content, and all human-authored memory metadata are
untrusted data. Confidence, verification, creator, origin, and lifecycle fields
do not grant instruction authority. Application-owned policy constants and
validated adapter configuration are the only prompt-control inputs.

### Prompt regions

The `grounded-answer-v1` prompt has three explicit regions:

1. application instructions, authored only by the canonical interaction
   domain;
2. the validated user question, encoded as data;
3. the deterministic evidence context, encoded as zero or more labeled records.

Application instructions state that content inside question or evidence
regions is data, that embedded commands must be ignored, that claims must be
supported by selected evidence, and that the provider must return the required
structured answer contract.

### Boundary encoding

Question and evidence values are serialized with a deterministic length-prefix
encoding. Human-readable section markers are fixed application text, while
every untrusted value carries its exact UTF-8 byte length. Delimiter-like text
inside values cannot terminate or create a region. The validation suite must
round-trip adversarial markers, control characters, Unicode, markup, and
instruction-like content through the exact renderer.

The serialized context remains subject to ADR 0008's 12,000-character total
budget; all length prefixes, labels, escaping, and wrappers count toward that
limit.

### Provider capability restriction

The generation request must set thinking off and must not include tool
definitions. The adapter exposes completion only. It has no memory-write,
network, filesystem, command, orchestration, or verification capability. A
provider response that requests or describes an action is still plain output
and grants no authority.

### Output validation

The provider returns a structured answer containing:

- `answer`;
- `cited_memory_ids`.

The application validates the schema, size limits, and that every cited ID is
present in the selected evidence set. Unknown citations, malformed output,
oversized output, or an empty citation set for a purported grounded answer fail
as `generation_invalid_response`. Provider text cannot add public evidence or
override the interaction result state.

### Public evidence boundary

Only ADR 0007's evidence allowlist may be returned. Raw payloads, embeddings,
internal collection names, point IDs, creation context, confidence basis,
provider prompts, fingerprints, traces containing content, and private
operational metadata are excluded.

### Logging and retention

Question text, retrieved content, rendered prompts, and generated answer text
must not be logged by default. Approved telemetry may contain bounded IDs,
counts, reason codes, policy versions, durations, result state, and error code
for no more than seven days. If an approved retention sink is unavailable,
trace metadata remains process-ephemeral.

## Alternatives considered

### Trust verified or high-confidence memories as instructions

Rejected because governance metadata does not establish safe instruction
authority.

### Escape only known delimiter strings

Rejected because a denylist cannot prove structural isolation for arbitrary
Unicode and novel markers.

### Allow provider tools but instruct the model not to use them

Rejected because capability absence is stronger and within Sprint 006 scope.

### Return the full selected memory payload for transparency

Rejected because it exposes unnecessary internal and potentially sensitive
fields.

## Consequences

### Positive

- Retrieved prompt injection cannot directly gain application authority.
- No provider output can trigger a side effect.
- Evidence linkage is validated after generation.
- Public disclosure is deliberately bounded.

### Negative

- The model may still repeat misleading evidence or adversarial text.
- Strict structured-output validation can turn otherwise readable provider
  output into a visible failure.
- Length-prefix rendering is less human-readable during debugging.

## Data, security, and privacy implications

This boundary reduces prompt injection and accidental disclosure but does not
replace future authorization, data-classification, or redaction controls.
Sensitive validation evidence must use an approved private retention path with
sanitized public metadata; absent such a path, the affected validation gate
remains blocked.

## Operational implications

Operators can diagnose failures with correlation IDs, reason codes, event
names, counts, and durations. Enabling content logging requires a separate
security and privacy decision and is not part of this proposal.

## Compatibility and migration

No existing memory record, API, vector, or service behavior changes. The trust
boundary is introduced only if the proposed interaction endpoint is later
implemented.

## Validation requirements

- delimiter and length-prefix round-trip tests;
- prompt-injection fixtures in questions and every evidence field;
- proof that no tools or side-effect-capable dependency are configured;
- provider-output schema, size, and citation allowlist tests;
- public evidence field allowlist tests;
- log-capture tests proving content is absent;
- cancellation and failure tests proving no partial grounded response;
- sensitive-data scan of proposal and implementation artifacts.

## Related decisions and documents

- [Sprint 006 specification](../SPRINT_006_SPECIFICATION.md)
- [Sprint 006 validation requirements](../SPRINT_006_VALIDATION_REQUIREMENTS.md)
- [Security policy](../../SECURITY.md)
- [ADR 0007](0007-grounded-response-and-evidence-contract.md)
- [ADR 0008](0008-deterministic-retrieval-context-assembly.md)
- [ADR 0010](0010-generation-model-identity-and-policy-defaults.md)

## Review record

This ADR is a proposal on the Sprint 006 Proposal v2 custody branch.
Implementation remains unauthorized until exact-head independent review,
Chief Architect acceptance, and explicit sprint authorization.
