# Current Sprint

## Sprint 003: Collector 1.0 Definition and Implementation Planning

**Target window:** 2026-07-31 through 2026-08-13

**Status:** Active; specification and implementation planning only

## Sprint goal

Define the first bounded Collector contract and produce an implementation plan
for a controlled local-first ingestion path using the currently reported n8n,
Ollama, and Qdrant environment.

This sprint must make Collector 1.0 implementable without inventing a universal
ingestion platform, depending on JCS, or changing the live server.

## Context

Project Genesis is complete and published as `v0.1.0`.

Milestone C1 closed through pull request #18 at merged commit
`5895e8f5896cf0687a43c978ec2f17da53d6b78c` with the outcome **DEFER JCS**.
JCS remains **Named**, its specification remains **Proposed**, and no JCS
implementation or Collector dependency on JCS is authorized.

The repository currently contains governance, architecture documentation, and
validation tooling, but no Project Jebediah application implementation. The
home-lab stack is reported to include n8n, Ollama, and Qdrant, but those runtime
claims remain subject to sanitized infrastructure verification.

Collector 1.0 is the first proposed product subsystem with a concrete outcome:
accept one bounded text record, preserve its source and provenance, apply
deterministic identity and validation, prevent accidental duplicate creation,
and prepare an approved storage request.

## Committed scope

### Checkpoint A: Collector contract

Create `docs/COLLECTOR_1_SPECIFICATION.md` defining:

- One text-record input contract
- Required provenance and source metadata
- Deterministic record identity
- Validation and rejection behavior
- Duplicate and update semantics
- Embedding and Qdrant payload boundaries
- Success, failure, and health reporting
- Privacy and security restrictions
- Acceptance criteria

### Checkpoint B: Implementation plan

Create `docs/COLLECTOR_1_IMPLEMENTATION_PLAN.md` defining:

- Implementation order and gates
- Proposed repository structure
- Separation between pure contract logic and runtime adapters
- n8n, Ollama, and Qdrant adapter responsibilities
- Unit, contract, integration, and failure testing
- Rollback and live-server protection
- Exact evidence required before deployment

### Checkpoint C: Architecture review

- Validate the complete proposed artifact set.
- Confirm that the specification does not depend on JCS.
- Confirm that current infrastructure remains reported rather than verified.
- Confirm that no runtime deployment is authorized by planning approval.
- Record exact review identity and recommendation dispositions.
- Authorize, revise, defer, or reject Collector implementation planning.

## Non-goals

- Modifying the Dell R420, Proxmox, Ubuntu VM, Docker, n8n, Ollama, or Qdrant
- Importing or changing an n8n workflow
- Creating production credentials, endpoints, secrets, or network topology
- Defining JCS
- Building a universal plugin framework
- Supporting arbitrary binary files, images, audio, email, or web crawling
- Building a knowledge graph, Digital Twin, reasoning engine, or automation
  control plane
- Autonomous collection
- Selecting a permanent embedding model
- Treating Qdrant as the authoritative source record
- Implementing code before the specification and plan pass review

## Acceptance criteria

- Collector 1.0 has one coherent responsibility.
- The input and output contracts are implementation-independent.
- Raw source identity and provenance remain distinguishable from embeddings.
- Stable identity is deterministic for the same logical source record.
- Duplicate handling is explicit and testable.
- Updates do not silently create unrelated records.
- Invalid records fail closed and return structured errors.
- Sensitive values and secrets are prohibited from logs and public fixtures.
- n8n, Ollama, and Qdrant remain replaceable adapters.
- The specification creates no JCS dependency.
- Infrastructure claims remain reported until separately verified.
- The implementation plan includes rollback and prohibits direct production
  deployment before approval.
- Repository validation and `git diff --check` pass.
- The Chief Architect reviews the exact complete artifact set.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| JCS Milestone C1 | Complete | Pull request #18 merged at `5895e8f5896cf0687a43c978ec2f17da53d6b78c`; outcome **DEFER JCS** |
| Checkpoint A: Collector contract | In progress | `docs/COLLECTOR_1_SPECIFICATION.md` proposed in this branch |
| Checkpoint B: Implementation plan | In progress | `docs/COLLECTOR_1_IMPLEMENTATION_PLAN.md` proposed in this branch |
| Checkpoint C: Architecture review | Blocked | Begins only after Checkpoints A and B validate as one exact artifact set |

## Dependencies

- Reviewed GitHub `main` remains authoritative.
- The [Collector 1.0 Specification](docs/COLLECTOR_1_SPECIFICATION.md) owns the
  proposed component contract.
- The [Collector 1.0 Implementation Plan](docs/COLLECTOR_1_IMPLEMENTATION_PLAN.md)
  owns implementation order and gates.
- The [Data Ownership](docs/DATA_OWNERSHIP.md), security, testing, operations,
  ADR, and Definition of Done policies remain binding.
- JCS remains deferred and is not a Collector dependency.
- Live-server work requires a separately approved execution checkpoint.

## Risks

| Risk | Response |
| --- | --- |
| Collector becomes a generic ingestion platform. | Limit 1.0 to one bounded text-record contract. |
| n8n implementation details become the architecture. | Keep the contract independent and treat n8n as an adapter. |
| Qdrant becomes mistaken for authoritative source storage. | Store provenance and references explicitly; do not make vectors the source of truth. |
| Duplicate detection relies on semantic similarity. | Use deterministic identity for idempotency; similarity is not identity. |
| Retried requests create extra records. | Require idempotent writes for the same record identity and revision. |
| Sensitive content enters public tests or logs. | Use synthetic fixtures and prohibit credentials and personal data. |
| Planning is mistaken for deployment approval. | Repeat that no server or workflow changes are authorized. |
| Reported infrastructure is treated as verified. | Keep runtime claims reported until a sanitized inventory is reviewed. |

## Update and close rules

Update this file whenever scope, gates, evidence, dependencies, or risks change.

At sprint close:

1. Record exact merged artifacts and validation evidence.
2. Record every review recommendation and disposition.
3. Carry incomplete work only with an owner, reason, risk, and new gate.
4. Update project status, roadmap, registry, documentation index, and changelog
   when their owned reality changes.
5. Do not deploy Collector 1.0 without a separately approved execution sprint.
