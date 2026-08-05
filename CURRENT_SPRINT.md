# Current Sprint

## Active sprint

**Name:** Knowledge Manager 1.0 Phase 1 - Knowledge Registry Foundation

**Status:** Active; bounded implementation candidate validated and awaiting
independent review

**Target window:** 2026-08-04 to 2026-08-18

**Deployment status:** Not authorized

**Information-use status:** Synthetic test metadata only; external and
organizational information use is not authorized

## Sprint goal

Determine whether Project Jebediah can safely represent governed knowledge
objects before learning from, retrieving, exposing, or acting on them.

The sprint will implement only the accepted metadata-only Knowledge Registry
domain, storage-neutral repository abstraction, in-memory reference adapter,
and deterministic validation defined by the
[Phase 1 Implementation Plan](docs/KNOWLEDGE_MANAGER_1_PHASE_1_IMPLEMENTATION_PLAN.md).

## Authority and context

- [ADR 0014](docs/adr/0014-knowledge-registry-domain-boundary.md) is the accepted
  System decision for the registry boundary.
- Independent Work Mode reviewed exact planning head
  `00db845a98f63fc3b8d1bb1135adcafa9d306b97` and returned **APPROVED** with no
  Blocking or High findings.
- The Chief Architect ratified `collector.knowledge.registry` as repository
  packaging only, accepted ADR 0014, authorized the exact bounded Phase 1
  scope, and approved its merge.
- Pull request #47 squash-merged that exact reviewed source into `main` at
  `f9fc0c6c15a4148f5d538f56ac4ab2ec8e92c93e`.
- The canonical activation closeout merged into `main` at
  `e418479bbb10f48c1a3c7dd207c299cc49226896`, which is the implementation
  base.
- During implementation, the required unchanged full-suite command exposed a
  pytest module-name collision between the new and existing `test_models.py`
  files. The Chief Architect authorized
  `tests/collector/knowledge/registry/__init__.py` solely as a test-package
  marker. It adds no runtime behavior, API, dependency, or information scope.
- The package location does not assign Collector Engine authority or ownership
  over registered knowledge.
- The Knowledge Vault remains **Named**. This sprint does not satisfy its full
  component-specification, implementation, deployment, or operations gates.

Sprint 006 Proposal v2 remains a separate proposed workstream. Activating this
sprint does not accept or authorize Sprint 006, the VBA demonstration, live
information use, or an organizational-intelligence implementation.

## Committed scope

The exact implementation targets are:

```text
src/collector/knowledge/
    __init__.py
    registry/
        __init__.py
        models.py
        repository.py
        in_memory_repository.py

tests/collector/knowledge/
    registry/
        __init__.py
        test_models.py
        test_repository.py
        test_package_boundaries.py
```

The sprint includes only:

- Immutable registry metadata domain types accepted in ADR 0014.
- Explicit source, transformation, evidence, ownership, governance, freshness,
  uncertainty, human-review, and lifecycle representation.
- A three-method `KnowledgeRegistryRepository` abstract base class.
- A typed identity-conflict failure.
- An in-memory reference adapter for deterministic tests.
- Model, repository, dependency-boundary, compatibility, and regression tests.
- Directly required documentation and implementation-review evidence.

## Non-goals

The sprint must not implement:

- Document ingestion, quarantine, PDF or DOCX processing, extraction,
  transformation, or admission evaluation.
- VBA, organizational, personal, confidential, or other external information
  loading.
- Source or derived content storage.
- Embeddings, Qdrant writes, semantic search, retrieval, ranking, or model
  context.
- Memory candidate creation, `MemoryItem` conversion, memory persistence,
  consolidation, or runtime integration.
- APIs, CLIs, dashboards, Open WebUI workflows, services, containers,
  deployment, databases, migrations, backup, or recovery.
- Autonomous approval, promotion, lifecycle transitions, actions, or source
  correction.
- New dependencies or dependency-version changes.

Any requested non-goal stops work for plan revision, Work Mode review, and
Chief Architect authorization.

## Acceptance criteria

The sprint is complete only when:

1. Checkpoint 0 reconfirms clean `main`, this active sprint, accepted ADR 0014,
   the accepted plan, and the full pre-change test baseline.
2. Registry records contain fixed governance metadata and no source or derived
   content, arbitrary metadata bag, embedding, score, model response, memory
   object, or action.
3. Required identifiers are non-empty, collections are immutable and
   duplicate-free, and all retained times are timezone-aware.
4. Freshness and uncertainty remain qualitative, explicit, evidence-linked,
   and separate from truth probability.
5. Approved or rejected review states require identified human decision
   evidence; repository registration cannot manufacture approval.
6. Lifecycle retains state, actor, time, reason, and required supersession
   evidence without implementing transitions.
7. The repository interface exposes only `register`, `find`, and `contains`;
   equal repeated registration is idempotent and conflicting identity reuse
   fails explicitly without overwrite.
8. The registry imports no memory, Collector pipeline, Qdrant, Ollama,
   embedding, service, runtime, or third-party module.
9. Existing code does not import the registry during Phase 1, and existing
   memory models, payloads, repositories, pipelines, dependencies, and runtime
   composition remain unchanged.
10. Targeted tests, the full regression suite, package/import checks,
    documentation validation, and diff checks pass.
11. Independent Work Mode implementation review has no unresolved Blocking
    findings.
12. The Chief Architect approves the exact implementation head for merge.

The normative evidence matrix is the
[Phase 1 Validation Requirements](docs/KNOWLEDGE_MANAGER_1_PHASE_1_VALIDATION_REQUIREMENTS.md).

## Work status

| Work item | State | Evidence or next gate |
| --- | --- | --- |
| Architecture and plan | Accepted | Work Mode approval and Chief Architect decisions recorded on PR #47 at exact source head `00db845a98f63fc3b8d1bb1135adcafa9d306b97` |
| Planning merge | Complete | PR #47 squash merge `f9fc0c6c15a4148f5d538f56ac4ab2ec8e92c93e` |
| Sprint activation | Active | This closeout reconciles canonical status, sprint, roadmap, architecture, ownership, and decision records; it becomes authoritative when merged |
| Checkpoint 0 | Complete | Clean synchronized `main` at implementation base `e418479bbb10f48c1a3c7dd207c299cc49226896`; package absent; documentation validation passed; 142 baseline tests passed |
| Domain types | Candidate complete | Immutable metadata contract and invariant tests implemented on `feature/knowledge-registry-foundation` |
| Repository abstraction and reference adapter | Candidate complete | Three-method ABC, typed conflict, and in-memory reference adapter implemented without runtime composition |
| Validation and compatibility proof | Candidate complete | 93 targeted tests and 235 full-suite tests pass; import smoke, documentation validation, package-boundary tests, and diff checks pass |
| Work Mode implementation review | Pending | Review the exact committed implementation head, complete diff, and evidence packet |
| Chief Architect implementation merge decision | Pending | Requires exact reviewed implementation head |

## Dependencies

- Accepted ADRs 0002, 0003, 0011, 0012, 0013, and 0014 remain unchanged.
- The implementation branch starts from clean synchronized `main` after this
  closeout.
- The existing Python package, Python 3.12-or-newer requirement, and pytest
  configuration remain available.
- The 142-test planning baseline is rerun before implementation.

The sprint does not depend on JCS, Qdrant availability, Ollama availability,
Docker, a service, organizational information, or the VBA demonstration.

## Risks

| Risk | Required response |
| --- | --- |
| Registry becomes a second Memory Service | Keep separate package and semantics; reject memory imports, content, and retrieval fields |
| Package path implies Collector authority | Preserve the Chief Architect's repository-packaging-only decision |
| Approval or uncertainty is treated as truth | Enforce explicit evidence contracts and negative tests; add no numeric truth score |
| Registration becomes promotion | Provide no promotion or transition API |
| Metadata leaks source content | Use fixed typed fields and fabricated synthetic fixtures only |
| Persistence scope expands | Keep the three-method interface and in-memory reference adapter only |
| Existing behavior regresses | Leave existing code unchanged and run the full suite |
| Scope changes after review | Stop and obtain revised architecture, review, and exact authorization |

## Update and close rules

- Update work status only from repository and validation evidence.
- Do not mark implementation complete because types compile or targeted tests
  pass.
- Any architecture, dependency, runtime, information-use, or file-scope change
  requires Chief Architect authorization before implementation continues.
- Work Mode reviews the exact final implementation before the Chief Architect
  merge decision.
- After a verified implementation merge, the Documentation Suite performs the
  normal documentation closeout.
- Deployment, external information, and Knowledge Manager Phase 2 remain
  separately gated after this sprint closes.
