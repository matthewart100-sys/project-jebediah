# Sprint 005 Validation Requirements

**Status:** Satisfied for Sprint 005 merge review

**Implementation state:** Reviewed source commit
`5a27358e4132a4ba14550b47c64f8538fe29094a` passed the complete validation
gate and was squash-merged through pull request #39 at
`5f1b58767b54aed797d1ec6a2fafa084a00d6de7`; deployment remains unauthorized

## Purpose

This document defines the evidence required to implement and review Sprint 005
memory architecture consolidation. It separates repository implementation
validation from deployment and live-data validation.

It does not authorize source-code changes, deployment, live Qdrant access, or
data migration.

## Closeout evidence

- The complete frozen suite passed with 142 tests.
- Python compilation, documentation, lockfile, diff, sensitive-data, package,
  and clean import-origin checks passed.
- The repository-root service image built successfully on Python 3.12.13.
- The container smoke loaded `collector.memory` from installed
  `site-packages`, proved `/app/collector` absent, and imported `/app/main.py`
  successfully without contacting live Qdrant or Ollama services.
- Sprint 005 performed no deployment, live collection access, data rewrite,
  re-embedding, or migration.

## Governing decisions

Validation must prove conformance with:

- [ADR 0002: Canonical Memory Domain and Dependency Direction](adr/0002-canonical-memory-domain-and-dependency-direction.md)
- [ADR 0003: Qdrant Repository, Collection, and Payload Consolidation](adr/0003-qdrant-repository-collection-and-payload-consolidation.md)
- [ADR 0004: Embedding Model Identity and Vector Compatibility](adr/0004-embedding-model-identity-and-vector-compatibility.md)
- [Sprint 005 Implementation Plan](SPRINT_005_IMPLEMENTATION_PLAN.md)
- [Memory Architecture](ARCHITECTURE_MEMORY_SYSTEM.md)

All three ADRs are accepted. Implementation must conform to them and stop at
the defined checkpoints when required evidence fails.

## Architecture-package validation baseline

Before implementation, the documentation-only package demonstrated:

- Each ADR has a final number, accepted status, decision level, owner,
  reviewers, evidence, alternatives, decision, consequences, recovery,
  compatibility, validation, and review record.
- ADR 0002 selects one canonical domain and one dependency direction.
- ADR 0003 explicitly selects Qdrant option A and defines source of truth,
  success, failure, consistency, and recovery without a distributed
  transaction.
- ADR 0004 defines an exact provider, versioned model, full manifest digest,
  dimensions, normalization, compatibility key, mutable-tag prohibition, and
  migration behavior.
- Legacy payload compatibility is never described as vector-geometry
  compatibility.
- A one-dimensional collection is explicitly incompatible with
  768-dimensional queries.
- Placeholder vectors require isolated future migration.
- The Sprint 005 plan and architecture documents agree with the ADRs.
- Accepted decisions are not described as deployed or merged.
- No runtime source, configuration, lock file, service behavior, or live data
  was changed by the architecture package.

The architecture package ran documentation validation only:

```text
python scripts/validate_docs.py
```

New untracked or newly added Markdown files must also be passed directly
through the repository validator's Markdown and sensitive-value checks until
they are included by the tracked-file scan.

## Implementation baseline (completed)

Before any implementation file is changed, record:

- Exact reviewed base commit
- Complete passing test count
- Root and service `collector.memory` import origins
- Service Python version and build path
- Store, rejection, context, and health API contracts
- Current governor, pipeline, embedding, and Qdrant call counts
- Current point-ID and application-ID behavior
- Current payload variants
- Current embedding length and absence of application normalization
- Current semantic-only ordering
- Proof that lifecycle and verification have no automated authority

Characterization tests must exist before the behavior they characterize is
rewired or deleted.

## Canonical-domain validation

ADR 0002 is satisfied only when tests prove:

- Root tests and the service import the same reviewed
  `src/collector/memory/` package.
- The service uses normal package installation or an immutable reviewed wheel.
- The service runs Python 3.12 or newer.
- No `PYTHONPATH`, execution-directory, source mount, or path-injection trick
  selects the package.
- The canonical domain does not import FastAPI, the service application, or
  deployment configuration.
- `collector.memory` public imports required by existing consumers remain
  valid.
- `services/jebediah-memory/app/collector/` can be removed without changing
  service behavior.
- The service-local embedding implementation can be removed after canonical
  provider proof.
- No duplicate governance, intelligence, persistence, or ranking behavior
  remains in the service tree.

## API compatibility validation

Contract tests must preserve:

- `GET /health`
- `POST /memory/store`
- `POST /memory/context`
- Existing required and optional request fields
- Legacy store requests using only the original required fields
- Existing accepted and rejected response fields
- Existing pipeline and intelligence result fields
- Existing context response fields and result limit
- Existing normal and validation status behavior
- Invalid memory-type fallback behavior
- Application memory-ID behavior

Interaction tests must prove:

- One governance evaluation per accepted request
- One embedding call per accepted request
- One acknowledged Qdrant point write per accepted request
- Zero embedding calls and writes for rejected requests
- No stored success after embedding or Qdrant failure
- No fabricated empty context success after query-embedding failure

## Sprint 004 governance validation

Regression tests must preserve:

- Provenance source, creator, creation context, confidence basis, and
  supporting evidence
- `unverified`, `verified`, and `disputed` representation
- `active`, `reinforced`, `superseded`, and `archived` representation
- Legacy `unverified` and `active` defaults
- Governance serialization and deserialization
- Invalid enum failure
- Semantic-only ranking
- Storage-independent `RetrievalCandidate` construction

Tests must prove no component automatically verifies, disputes, reinforces,
supersedes, archives, deletes, or reranks a memory.

## Qdrant contract validation

ADR 0003 requires isolated tests for:

- Default collection name `jebediah_memory`
- One unnamed dense vector
- Exactly 768 dimensions
- Cosine distance
- Compatible existing collection inspection
- Missing collection creation with the exact schema
- Visible failure for dimension or distance mismatch
- Adapter-generated Qdrant UUID
- Application memory ID stored and queried through `payload.memory_id`
- One payload and vector written in one point operation
- Completed acknowledgement using `wait=true` or the client equivalent
- Stored success only after completed acknowledgement
- Qdrant rejection returning no stored success
- Timeout or lost acknowledgement represented as unknown outcome
- Reconciliation by `memory_id` before an operator-authorized retry
- No blind automatic retry while point IDs are nondeterministic
- Record lookup and semantic search through the same canonical adapter
- A fresh current-collection identity and vector scan before every index and
  semantic-search operation
- Exact non-null approved identity and valid non-placeholder vector geometry
  for every returned semantic candidate
- Visible failure when a missing identity, different digest, different
  normalization policy, wrong dimension, or placeholder vector is added after
  an earlier successful scan
- Result-level validation for an incompatible point that appears between the
  current scan and semantic query
- No permanent scan cache unless a later accepted architecture proves
  enforceable exclusive collection ownership
- No direct Qdrant point, collection, filter, or query construction in
  FastAPI after cutover

Recovery review must verify that a future supported deployment has sanitized
Qdrant persistence, snapshot, restore, and unknown-outcome procedures. Source
implementation may be reviewed without live access, but deployment may not be
claimed ready without that evidence.

## Payload compatibility validation

Synthetic fixtures must cover:

- Current payload with `memory_id`
- Root legacy payload without `memory_id`
- Pre-Sprint 004 payload without provenance
- Pre-Sprint 004 payload without lifecycle
- Missing optional governance fields
- Missing `embedding_model`
- Missing `embedding_identity`
- Unknown additive fields
- Invalid required fields
- Invalid enum values

Compatible payload tests may apply documented defaults. They must not rewrite
fixtures or assert vector compatibility from payload readability.

## Embedding compatibility validation

ADR 0004 requires tests for the exact contract:

| Property | Required value |
| --- | --- |
| Provider | `ollama` |
| Model | `nomic-embed-text:v1.5` |
| Manifest digest | `sha256:0a109f422b47e3a30ba2b10eca18548e944e8a23073ee3f3e947efcf3c45e59f` |
| Dimensions | 768 |
| Normalization | `none` |
| Distance | `cosine` |

Tests must prove:

- The exact full manifest digest passes readiness.
- The actual Ollama `/api/tags` bare 64-character hexadecimal digest is
  canonicalized to the exact lowercase `sha256:<hex>` persistence identity.
- A missing or different digest fails readiness and blocks writes.
- A malformed, non-hexadecimal, or incorrectly sized digest fails before
  generation and persistence.
- Readiness is reverified before every embedding operation.
- A digest change after a successful startup check causes the next embedding
  operation to fail before generation or Qdrant persistence.
- `:latest` is rejected as configuration for supported writes and as a
  persisted compatibility identity.
- Every new point contains the complete `embedding_identity` object.
- The provider vector is unchanged after validation.
- Exactly 768 finite numeric values are accepted.
- Empty, non-numeric, non-finite, short, and long vectors are rejected.
- No zero, importance, padded, truncated, or fallback vector is produced.
- Store and query vectors use the same full compatibility key.
- Unknown legacy identity remains unknown.
- Equal dimensions without matching model identity are not declared
  compatible.

## Vector-geometry migration validation

Geometry tests are separate from payload tests and must prove:

- A one-dimensional collection cannot accept or search a 768-dimensional
  vector.
- A 768-dimensional zero vector is classified as a placeholder, not a valid
  embedding.
- Wrong-dimension, differently normalized, different-digest, and unknown
  vectors cannot enter the approved collection through normal migration.
- Placeholder vectors are not repaired automatically.
- Any future migration target is isolated from the source collection.
- Future migration requires authorized source content, backup, side-by-side
  validation, explicit cutover, and rollback.

Sprint 005 must contain no live re-embedding or collection rewrite.

## Phase checkpoints

| Phase | Required evidence before proceeding |
| --- | --- |
| Baseline characterization | Current behavior and imports are fully asserted |
| Contract definition | ADRs accepted; interfaces and ownership agree |
| Compatibility layer | Canonical adapters pass isolated contract, payload, embedding, and geometry tests while inactive |
| Service cutover | API, interaction-count, acknowledgement, failure, and governance tests pass |
| Duplicate removal | One canonical domain, provider, and Qdrant implementation remain; import origin is proven |
| Final validation | Full suite, packaging, documentation, diff, security, and review evidence pass |

Failure at a checkpoint stops the next phase. The previous reviewed phase is
the rollback point.

## Final implementation validation commands

The final implementation branch must run:

```text
uv run --frozen pytest -q
python compilation validation
service/container build and import smoke validation
python scripts/validate_docs.py
uv lock --check
git diff --check
```

It must also receive exact diff inspection, secret and private-data review,
and the formal architecture review required by the Definition of Done.

When a Docker runtime is available, run this gate from the repository root:

```text
docker build --pull --tag jebediah-memory:sprint-005-review --file services/jebediah-memory/Dockerfile .
docker run --rm --entrypoint python jebediah-memory:sprint-005-review -c "import pathlib, sys, collector.memory, main; origin=pathlib.Path(collector.memory.__file__).resolve().as_posix(); assert sys.version_info[:2] == (3, 12); assert '/site-packages/collector/memory/' in origin; assert '/services/jebediah-memory/app/collector/' not in origin; assert not pathlib.Path('/app/collector').exists(); print(sys.version.split()[0]); print(origin); print(pathlib.Path(main.__file__).resolve().as_posix())"
```

The build must complete the frozen dependency installation in the Dockerfile.
The smoke command must report Python 3.12, load `collector.memory` from the
installed canonical package, prove no service-local shadow tree exists, and
import `main.py` without contacting live Qdrant or Ollama services.

These commands were validation gates only. Subsequent formal review authorized
pull request #39 and the recorded merge. The validation did not authorize
deployment, live collection access, data migration, or other deferred work.

## Stop conditions

Stop implementation or deployment when:

- A required ADR is not accepted.
- A characterization or checkpoint test fails.
- API or Sprint 004 governance behavior changes unexpectedly.
- The service imports a noncanonical package.
- The pinned Ollama digest is absent or different.
- Collection dimensions or distance are incompatible.
- Vector identity cannot be proven compatible.
- Placeholder vectors are found in the target collection.
- A request can produce duplicate durable writes.
- An unknown Qdrant outcome can be retried blindly.
- Lifecycle, verification, or reranking automation appears.
- Live data, secrets, or private operational details would be required for
  source consolidation.

## Evidence report

Every validation handoff records:

- Exact commit and branch
- Commands run
- Exit results and test counts
- Skipped or unavailable evidence
- Import origin and container result when applicable
- Qdrant and embedding compatibility conclusions without sensitive contents
- Remaining warnings or blockers
- Whether implementation, deployment, or migration remains unauthorized
