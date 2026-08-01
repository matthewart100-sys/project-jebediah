# Current Sprint

## Sprint 005: Memory Architecture Consolidation

**Status:** Implementation complete; validation blocked

**Implementation status:** Completed on
`agent/sprint-005-memory-consolidation`; Quality Control corrections are
applied, uncommitted, and unmerged. The complete 142-test suite and all
available local gates pass. Review handoff remains blocked until the mandatory
container build/import smoke runs in an environment with a container runtime.

**Deployment status:** Not authorized

## Sprint goal

Consolidate the duplicate memory architecture into one canonical domain,
Qdrant path, and embedding contract while preserving the merged Sprint 004
governance and API behavior.

The complete execution contract is the
[Sprint 005 Implementation Plan](docs/SPRINT_005_IMPLEMENTATION_PLAN.md). The
required evidence is defined by the
[Sprint 005 Validation Requirements](docs/SPRINT_005_VALIDATION_REQUIREMENTS.md).

## Current state

Sprint 004 Memory Governance and Intelligence Expansion is merged into
`main`. Its repository baseline has 66 passing tests and includes:

- Provenance representation
- Verification-state representation
- Active, reinforced, superseded, and archived lifecycle states
- Confidence and retention metadata
- Storage-independent retrieval candidates
- Semantic-only ranking

The repository candidate now has one memory domain under
`src/collector/memory/`, one embedding implementation under
`src/collector/embeddings/`, and one canonical Qdrant durable-record and
semantic-search adapter. The FastAPI tree contains composition and HTTP
translation only. Deployment and live collection compatibility remain
unverified and unauthorized.

## Accepted architecture decisions

- [ADR 0002](docs/adr/0002-canonical-memory-domain-and-dependency-direction.md)
  makes `src/collector/memory/` canonical and limits the service to
  composition, HTTP, packaging, and deployment responsibilities.
- [ADR 0003](docs/adr/0003-qdrant-repository-collection-and-payload-consolidation.md)
  selects Qdrant option A: Qdrant temporarily owns the durable operational
  Memory Service record and attached semantic index through one adapter and
  one acknowledged point write.
- [ADR 0004](docs/adr/0004-embedding-model-identity-and-vector-compatibility.md)
  selects Ollama `nomic-embed-text:v1.5`, pins its full manifest digest,
  requires 768 raw finite values with no application normalization, and
  prohibits mutable tags as compatibility identities.

All three ADRs were accepted for implementation after Chief Architect final
review and explicit maintainer authorization on 2026-07-31.

## Current authorized scope

The branch may implement only the phased canonical-package, service cutover,
Qdrant-adapter, embedding-contract, packaging, test, and documentation work
defined by the accepted plan. It may not deploy, mutate live data, commit,
open a pull request, or merge without separate authorization.

## Implementation phases

1. Baseline characterization
2. Contract definition
3. Compatibility layer
4. Service cutover
5. Duplicate removal
6. Final validation and review

Each phase stops at its checkpoint and retains the preceding reviewed state as
its rollback point.

## Governance invariants

- Provenance remains origin metadata, not truth.
- Verification remains explicit representation and defaults to `unverified`.
- Lifecycle remains representation only and defaults to `active`.
- No automatic verification or lifecycle transition is introduced.
- Retrieval remains semantic-only.
- API paths, request schemas, response schemas, and status meanings remain
  compatible.
- Compatible legacy payload defaults do not imply vector compatibility.
- A one-dimensional collection cannot be queried with a 768-dimensional
  vector.
- Placeholder vectors require isolated future migration.

## Non-goals

- Collector 1.0
- Agents or autonomous behavior
- n8n orchestration
- Autonomous verification
- Lifecycle automation
- Intelligent reranking
- Live Qdrant migration or re-embedding
- A separate durable database
- Distributed transactions
- Memory identity or idempotency redesign
- Deployment or home-lab changes

## Implementation-review acceptance criteria

- Root and service use the same installed canonical package.
- API, Sprint 004 governance, lifecycle representation, verification
  boundaries, and semantic-only ranking remain compatible.
- Embedding and Qdrant failures cannot report stored success.
- Qdrant success requires a completed acknowledgement or confirmed read-back;
  unknown outcomes are never retried automatically.
- Model identity, vector geometry, no-normalization behavior, legacy payload
  reading, and incompatible-vector rejection match accepted ADRs.
- Full tests, compilation, packaging, documentation, lock, diff, and sensitive
  data checks pass before review.
- The exact uncommitted artifacts receive implementation review before any
  commit, pull request, or merge.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Architecture review packet | Accepted | Chief Architect final review and maintainer authorization recorded |
| ADR 0002 | Accepted | Canonical domain, dependency direction, packaging, and removal criteria defined |
| ADR 0003 | Accepted | Qdrant option A, authority, write success, failure, consistency, recovery, and legacy separation defined |
| ADR 0004 | Accepted | Exact Ollama model artifact, mutable-tag prohibition, geometry, normalization, and migration defined |
| Baseline characterization | Complete | Pre-change focused and 66-test baselines passed |
| Canonical contracts | Complete | Embedding and Qdrant compatibility suites pass in isolation |
| Service cutover | Complete | API and interaction tests prove one canonical orchestration path |
| Duplicate removal | Complete | Service app contains only `main.py`; import-origin and boundary tests pass |
| Quality Control corrections | Complete | Bare Ollama digest canonicalization, per-operation digest verification, and fail-closed post-scan Qdrant candidate validation pass regression tests |
| Validation requirements | Blocked | 142 tests, compilation, documentation, lock, diff, sensitive-data, and clean wheel/import checks pass; Docker, Podman, and nerdctl are unavailable for the mandatory container run |
| Implementation | Complete | Exact artifacts remain uncommitted and unmerged pending review |

## Update and close rules

Update this file when implementation scope, risk, evidence, or review status
changes. Merge remains blocked until the exact artifacts receive review and
separate authorization.
