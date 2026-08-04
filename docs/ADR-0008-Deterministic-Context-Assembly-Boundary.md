ADR 0008 — Deterministic Context Assembly Boundary (Proposed)

Status: Proposed
Date: 2026-08-04

Context
-------
The interaction gateway assembles context for generation requests by fetching retrieval candidates, applying filters, and constructing the context payload delivered to models. Non-deterministic or loosely-specified context assembly increases variance between runs and undermines reproducibility, debugging, and governance.

Problem
-------
- Without a clearly-defined deterministic boundary, two identical requests may produce different context payloads, making audits and blame assignment difficult.
- Some retrieval or ranking systems include non-deterministic behavior (e.g., time-based recency, approximate nearest neighbors with random seeds), complicating reproducibility.

Decision (Proposed)
--------------------
Define a deterministic context assembly boundary and ruleset: the interaction gateway will implement a determinism-first context assembly pipeline where the final context snapshot attached to a model request is reproducible given the same inputs and configuration. Where non-determinism is unavoidable, it will be explicitly recorded and bounded.

Key rules (proposed)
1. Determinism seed and configuration
   - Each context assembly run must include an explicit assembly_config object containing the deterministic seed (if used), the retriever version, retrieval parameters, ranking parameters, and timestamps.
2. Immutable context snapshot
   - The gateway must persist the exact context snapshot that was submitted to the model (context_snapshot blob or pointer), together with assembly_config and evidence references.
3. Bounded non-determinism
   - If a retrieval or ranking component is inherently non-deterministic, the component must accept a seed or be wrapped to produce deterministic outputs for governance-mode runs. If this is not possible, the interaction should still record version, random seed, and a "non_deterministic=true" flag in assembly_config.
4. Re-execution and replay
   - Given request_id and assembly_config, the system must be able to re-run the same retrieval and assembly steps and arrive at an equivalent context_snapshot, or provide a reproducibility record explaining any variance.
5. Time and recency handling
   - Time-bounded retrievals must explicitly declare the time window in assembly_config (e.g., now-30d) so that replay uses the same time window even if "now" has advanced.

Rationale
---------
- Deterministic context assembly is essential for auditable generation, reproducible tests, and post-hoc investigations.
- Persisting context snapshots enables debugging and forensic review without relying on reconstructing from sources that may change.

Consequences
------------
- Storage requirements increase due to persisted context snapshots and assembly metadata.
- Some retrieval providers may need adaptation to support deterministic results or seed input.
- Replay capability imposes engineering cost but yields high governance value.

Alternatives considered
-----------------------
- Best-effort reproducibility without persisted snapshots: cheaper but brittle for audits.
- Full snapshotting of all raw retrieval inputs (network-level): heavy-handed and may include protected data unnecessarily.

Proposed owner and next steps
-----------------------------
- Owner: Interaction Gateway maintainers with Retrieval and Platform teams.
- Next steps: define assembly_config schema, implement snapshot persistence and replay tooling, and add replay-based tests to the validation checklist.

