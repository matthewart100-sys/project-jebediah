ADR 0006 — Canonical Interaction Domain (Proposed)

Status: Proposed
Date: 2026-08-04

Context
-------
Project Jebediah is adopting an Interaction Gateway that mediates requests between upstream clients and downstream model and retrieval services. Without a canonical domain model for interactions, integration variability undermines auditability, interoperability, and governance.

Problem
-------
- Multiple teams and consumers may use different request shapes, metadata conventions, and evidence attachment methods, producing inconsistent provenance and complicating audits.
- Lack of a single canonical interaction domain increases risk when onboarding new model providers or connectors.

Decision (Proposed)
--------------------
Define a Canonical Interaction Domain that prescribes the minimal canonical schema and semantics for requests and responses passing through the interaction layer.

Key elements of the proposed canonical domain:
1. Request envelope
   - request_id: UUID (string)
   - client_id: identifier for upstream client (string)
   - timestamp_utc: ISO8601
   - intent: machine-readable intent token (string) and optional human label
   - parameters: typed map for request parameters (object)
   - context_reference: optional pointer to an externally stored context snapshot (string)
2. Response envelope
   - response_id: UUID
   - request_id: mirrors the originating request
   - timestamp_utc: ISO8601
   - model_identity: canonical model description (see ADR 0009)
   - content: primary generated payload
   - evidence: array of evidence items (see ADR 0007)
   - confidence: optional numeric confidence score (bounded 0.0-1.0)
   - warnings: optional list of policy or operational warnings
3. Evidence item schema (summary)
   - evidence_id: stable identifier
   - source: origin name (retrieval store, connector, or provider)
   - excerpt: small textual summary or highlight
   - location: pointer to the canonical retrieval reference (URN/URL)
   - fetch_timestamp_utc
   - provenance: minimal provenance metadata (who/what/when; normalized)

Rationale
---------
- Standardizing on a minimal, precise envelope reduces per-integration variance and improves auditability.
- Explicit model_identity and evidence arrays enable tracing the origin of generated content.
- The canonical domain is deliberately minimal so it can be applied to diverse upstream clients and downstream providers.

Consequences
------------
- Integrations must map their native request/response shapes to the canonical envelope at the interaction gateway boundary.
- Upstream clients may need small adapters to produce canonical request envelopes if they are not already compatible.
- Some legacy consumers might require backward-compatible wrappers; the interaction gateway should be able to accept both canonical and legacy flavors and normalize them internally.

Alternatives considered
-----------------------
- Do nothing: keep current heterogeneous shapes — rejected for governance and auditability reasons.
- Heavyweight schema (full typed JSON Schema for every parameter): rejected as too prescriptive and likely to block adoption.

Proposed owner and next steps
-----------------------------
- Owner: Interaction Gateway maintainers; reviewed by Architecture and Governance teams.
- Next steps: publish canonical JSON Schemas in docs/schemas/, create normalization adapters, and update validation tests to assert canonical envelope compliance.

