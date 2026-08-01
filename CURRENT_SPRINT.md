# Current Sprint

## Sprint 004: Memory Governance and Intelligence Expansion

**Status:** Active implementation and review

**Deployment status:** Blocked; this sprint changes repository artifacts only

## Sprint goal

Extend the implemented memory service with provenance, lifecycle awareness,
and a replaceable retrieval-ranking boundary while preserving current storage
and API behavior.

The complete implementation contract is the
[Sprint 004 Specification](docs/SPRINT_004_SPECIFICATION.md).

## Context

Sprint 003 added the repository implementation of the memory API, Ollama
embedding adapter, Qdrant persistence, memory pipeline, consolidation engine,
intelligence governor, confidence scoring, retention scoring, and metadata
enrichment. The unit baseline before Sprint 004 is 53 passing tests.

Repository evidence verifies that source and tests exist. Deployment, live
service health, live Qdrant contents, and the reported home-lab environment
remain unverified and are not changed by this sprint.

The previous sprint, status, architecture, and foundation documents still
contained planning-only statements after the implementation was added. Sprint
004 includes the smallest documentation reconciliation needed to make current
repository reality explicit.

## Committed scope

### Phase 1: Provenance foundation

- Add typed source, creator, creation-context, confidence-basis, verification,
  and supporting-evidence metadata.
- Preserve `source_identity` and `created_at` semantics.
- Attach safe defaults for legacy callers.
- Persist and retrieve provenance without presenting unverified data as
  verified.

### Phase 2: Lifecycle foundation

- Add `active`, `reinforced`, `superseded`, and `archived` states.
- Preserve minimal reinforcement and supersession metadata.
- Default new and legacy memories to `active`.
- Do not automate state transitions or deletion.

### Phase 3: Retrieval preparation

- Add an internal retrieval candidate and ranker boundary.
- Expose semantic relevance, confidence, importance, creation time, and
  lifecycle state to that boundary.
- Retain semantic-only ranking as the current behavior.
- Preserve the context API response contract.

### Documentation reconciliation

- Complete the previously truncated Sprint 004 specification.
- Update current status, sprint, architecture, component maturity, roadmap,
  navigation, and changelog statements that would otherwise remain stale.
- Repair existing documentation-validation findings that affect this change.

## Non-goals

- Live deployment or modification of Docker, Qdrant, Ollama, n8n, or home-lab
  state
- Backfilling or rewriting a live Qdrant collection
- Automatic claim verification
- Automatic lifecycle transitions, filtering, or deletion
- A multi-factor ranking formula or learned ranking model
- Knowledge-graph relationships
- Autonomous collection or action
- Replacing or consolidating the duplicate package and service source trees
- Changing deterministic Collector identity

## Acceptance criteria

- Existing callers can still construct and store a memory without new fields.
- New persistence carries provenance and lifecycle payloads.
- Legacy Qdrant payloads remain readable with safe defaults.
- All four lifecycle states are represented and documented.
- Retrieval remains ordered by semantic similarity while carrying the future
  signals internally.
- Existing store and context response fields are preserved.
- Existing tests and new focused tests pass.
- `python scripts/validate_docs.py` and `git diff --check` pass.
- The final diff contains no private operational data or real memory content.
- The uncommitted exact diff receives review before any commit.

## Dependencies

- The existing memory architecture and service boundaries remain in force.
- Qdrant and embeddings remain derived information under
  [Data Ownership](docs/DATA_OWNERSHIP.md).
- The [Security Policy](SECURITY.md),
  [Testing Philosophy](docs/TESTING_PHILOSOPHY.md), and
  [Definition of Done](docs/DEFINITION_OF_DONE.md) remain binding.
- JCS remains deferred and is not a memory-service dependency.

## Risks and responses

| Risk | Response |
| --- | --- |
| New metadata breaks existing callers. | Add only defaulted domain fields and optional API inputs. |
| Legacy Qdrant payloads fail to load. | Derive unverified provenance and active lifecycle when fields are absent. |
| Lifecycle labels imply automated policy. | Add state representation only; explicitly defer transitions and filtering. |
| Retrieval behavior changes unexpectedly. | Use a semantic-only default ranker and test stable ordering and response keys. |
| Provenance is mistaken for truth. | Keep verification explicit and default it to `unverified`. |
| Duplicate source trees drift further. | Apply equivalent domain changes to both active trees and validate their shared governance modules. |
| Documentation overstates operations. | Separate repository implementation evidence from unverified deployment claims. |

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Orientation and baseline | Complete | Current `origin/main` inspected; 53 tests passed before changes |
| Canonical Sprint 004 contract | Complete | Specification, status, architecture, and affected standards reconciled in this branch |
| Provenance implementation | Complete | Domain, persistence, pipeline, API, legacy-default, and round-trip tests pass |
| Lifecycle implementation | Complete | Four states, persistence metadata, safe defaults, and serialization tests pass |
| Retrieval foundation | Complete | Candidate/ranker boundary is integrated with semantic-only API ordering |
| Validation and review handoff | Awaiting maintainer review | 66 tests, compilation, documentation validation, lock check, `git diff --check`, exact local diff inspection, and sensitive-data scans pass; commit withheld |

## Update and close rules

Update this file when scope, acceptance criteria, risk, or evidence changes.
At close, record exact validation, review disposition, merge evidence, any
deployment limitation, and the next authorized lifecycle or retrieval decision.
