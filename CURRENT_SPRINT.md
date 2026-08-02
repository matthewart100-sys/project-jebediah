# Current Sprint

## Sprint 005: Memory Architecture Consolidation

**Status:** Complete and merged

**Implementation status:** Merged through pull request #39. The reviewed source
commit was `5a27358e4132a4ba14550b47c64f8538fe29094a`; the squash-merged `main`
commit is `5f1b58767b54aed797d1ec6a2fafa084a00d6de7`.

**Validation status:** Complete. The approved non-container suite passed with
142 tests, and the Python 3.12 container build/import smoke passed on the
Jebediah Ubuntu validation environment.

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

The merged repository now has one memory domain under
`src/collector/memory/`, one embedding implementation under
`src/collector/embeddings/`, and one canonical Qdrant durable-record and
semantic-search adapter. The FastAPI tree contains composition and HTTP
translation only. The container validation proved that Python 3.12 loads the
canonical package from installed `site-packages`, that `/app/collector` is
absent, and that `/app/main.py` imports successfully. Deployment and live
collection compatibility remain unverified and unauthorized.

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

## Completed scope

Sprint 005 completed only the phased canonical-package, service cutover,
Qdrant-adapter, embedding-contract, packaging, test, and documentation work
defined by the accepted plan. It did not deploy or mutate live data. Any
follow-on implementation, deployment, or migration requires a separately
authorized scope.

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

## Closeout acceptance evidence

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
- The exact source artifacts at
  `5a27358e4132a4ba14550b47c64f8538fe29094a` received implementation and
  container review before pull request #39 was squash-merged at
  `5f1b58767b54aed797d1ec6a2fafa084a00d6de7`.

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
| Validation requirements | Complete | 142 tests and all approved non-container gates passed; the Python 3.12 container build/import smoke also passed |
| Implementation | Merged | Pull request #39 squash-merged reviewed source `5a27358e4132a4ba14550b47c64f8538fe29094a` into `main` at `5f1b58767b54aed797d1ec6a2fafa084a00d6de7` |

## Update and close rules

Sprint 005 is closed. This closeout does not define Sprint 006 or authorize
deployment, live-data access, vector migration, or other deferred work. A
future sprint must be selected from the existing roadmap and authorized
through the normal review process.

## Sprint 006 proposal history

[Sprint 006 Proposal v1](docs/SPRINT_006_PROPOSAL_V1_ABANDONED.md) is
permanently **Abandoned** because its source artifacts and exact review head
are unrecoverable. Its successor,
[Sprint 006 Proposal v2](docs/SPRINT_006_SPECIFICATION.md), is newly authored
from the accepted post-Sprint 005 baseline and is not a reconstruction of v1.
It is a Proposed architecture package, not an active or authorized
implementation sprint. Its [validation requirements](docs/SPRINT_006_VALIDATION_REQUIREMENTS.md)
and proposed ADRs 0006 through 0010 require exact-head Work Mode review, Chief
Architect acceptance, and explicit sprint authorization before implementation.

The proposed classification is: **A bounded Phase 2 memory-client validation
that proves governed retrieval, deterministic context assembly, and
evidence-grounded generation. Sprint 006 does not activate or implement the
Phase 6 Reasoning Engine.**
