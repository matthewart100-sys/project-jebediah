ADR 0007 — Grounded Response and Evidence Contract (Proposed)

Status: Proposed
Date: 2026-08-04

Context
-------
Generative responses can be persuasive but occasionally ungrounded. For Project Jebediah to rely on generated outputs operationally, responses must be accompanied by verifiable evidence and provenance. This ADR proposes a contract that defines the minimum evidence and grounding metadata that the interaction gateway must attach to any non-trivial generated response.

Problem
-------
- Generated content without attached evidence is risky for downstream decision-making.
- Auditors and reviewers require reproducible links between assertions in generated content and the sources used to produce them.

Decision (Proposed)
--------------------
Adopt a Grounded Response and Evidence Contract mandating that all generated responses include a structured evidence array plus minimal provenance metadata, except where explicitly declared (e.g., purely conversational or transient messages flagged as "no-evidence-required").

Minimum contract elements (for responses where evidence is required):
- evidence[]: ordered array of evidence items (any evidence item that materially supports assertions in content must appear)
  - evidence_id: stable identifier
  - role: {context, citation, supporting_fact, contradictory_evidence}
  - source: canonical source identifier (URN/URL) or retrieval-store key
  - excerpt: textual excerpt or summary from source showing the supporting text
  - relevance_score: numeric score representing retrieval relevance (optional)
  - fetch_timestamp_utc: when the evidence was retrieved
  - provenance: who fetched it and by what retrieval method (retriever id/version)
- content_highlights: optional mapping from content spans to evidence_id(s)
- model_identity: which model produced the content (see ADR 0009)
- evidence_confidence: optional aggregated score or qualitative label
- evidence_policy_flags: any flags indicating policy concerns (PII, untrusted source, stale, paywalled)

Operational rules (proposed)
- Evidence must be collected during deterministic context assembly and retrieval, and recorded in an immutable audit trail.
- Evidence excerpts must not contain secrets or full protected documents; excerpts must be bounded (configurable max length) and redacted as required by policy.
- When the gateway cannot attach evidence because none was found, the response must include an explicit "no_evidence_found" marker and a provenance trace describing which retrievals were attempted.

Rationale
---------
- Associating evidence with generated assertions increases trust and makes results auditable.
- A minimal contract balances governance needs with performance and privacy constraints.

Consequences
------------
- Retrieval systems and connectors must expose identifiers and excerpts suitable for inclusion in the evidence array.
- Additional storage and audit-log capacity will be needed to retain retrieval traces and evidence references.
- Some responses (e.g., short conversational replies) may be marked as exempt; the exemption must be explicit and logged.

Alternatives considered
-----------------------
- Per-team evidence policies (not centralized): rejected because inconsistent policies impede governance.
- Require full-source replication for every claim: rejected for privacy and performance reasons.

Proposed owner and next steps
-----------------------------
- Owner: Interaction Gateway maintainers in collaboration with Retrieval and Security teams.
- Next steps: publish evidence JSON Schema, update retrieval connectors to supply the required evidence metadata, and add validation tests that assert evidence presence for production-critical workflows.

