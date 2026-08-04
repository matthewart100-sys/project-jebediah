ADR 0009 — Generation Model Identity Policy (Proposed)

Status: Proposed
Date: 2026-08-04

Context
-------
Multiple generative models and providers may be invoked by the interaction gateway. For accountability and auditability, each model invocation must be accompanied by a canonical model identity that is recorded in request/response metadata, logs, and evidence traces.

Problem
-------
- Absent a consistent model identity policy, logs and artifacts can contain ambiguous or incomplete model descriptions (e.g., "openai", "gpt-4", or provider internal codes), making audits and incident analysis difficult.

Decision (Proposed)
--------------------
Adopt a Generation Model Identity Policy that requires an explicit, versioned, and discoverable model identity for every model invoked through the interaction gateway. The policy defines the minimal identity fields and where they must appear.

Minimal model_identity fields (proposed)
- model_id: stable canonical identifier string (e.g., provider:model-name:version or urn scheme)
- provider: provider short name (e.g., openai, local, acme-ai)
- model_name: provider model name
- model_version: explicit version or semantic version tag if available
- invocation_config: normalized map of invocation parameters (temperature, max_tokens, sampling, top_k, etc.) used for that call
- model_signature_hash: optional content-derived signature of the model binary or container image (when available for on-prem models)
- trust_level: categorical label (trusted | untrusted | external) assigned by governance

Where model_identity must appear
- In the response envelope model_identity field (see canonical interaction domain ADR 0006)
- In audit logs and traces that record generation events
- In persisted context snapshots and replay records

Operational rules (proposed)
- The interaction gateway will maintain a model registry (or reference to a platform registry) mapping model_id to human-readable metadata and compliance notes.
- When invoking third-party cloud models that do not supply a trustworthy model_version, the gateway will capture the provider-declared model identifier string and mark model_version as "provider_declared" while recording the provider response to a discovery call.
- The invocation_config must be recorded verbatim in logs and in persisted request artifacts to enable replay and audit.

Rationale
---------
- Explicit model identity improves traceability and accountability.
- Inclusion of invocation_config enables deterministic replay when paired with deterministic context snapshot.

Consequences
------------
- Implementers must populate and persist model_identity for every model invocation.
- Interaction gateway will need to integrate or reference a model registry and ensure the registry is maintained.
- Extra logging and storage are required to capture invocation_config and identity metadata.

Alternatives considered
-----------------------
- Lightweight identity (provider only): insufficient for audits.
- No registry: short-term simplicity, long-term governance debt.

Proposed owner and next steps
-----------------------------
- Owner: Platform and Interaction Gateway maintainers.
- Next steps: define the model_id URN scheme, implement a minimal model registry or integrate with an existing platform registry, and update the gateway to record model_identity for every invocation.

