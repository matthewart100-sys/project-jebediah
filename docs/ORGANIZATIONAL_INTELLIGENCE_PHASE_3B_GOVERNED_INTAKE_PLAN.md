# Organizational Intelligence Phase 3B Governed Intake Plan

**Status:** Proposed; bounded synthetic-only implementation plan

**Program phase:** Organizational Intelligence Product Program Phase 3B -
Synthetic Intake and Custody Foundation

**Prepared:** 2026-08-05

## Purpose

Phase 3B Milestone 1 establishes a loopback-only synthetic intake path for one
browser-pushed PDF plus bounded local custody, review, and lifecycle evidence.
It exists to validate intake contracts and custody mechanics with deterministic
synthetic fixtures only.

## Scope

The bounded implementation may:

1. run the Executive Product Shell on loopback only;
2. accept one browser-selected synthetic PDF byte stream without any server-side
   source path;
3. verify a signed synthetic authorization receipt before accepting bytes;
4. validate PDF signature, MIME type, and size;
5. compute SHA-256 content identity;
6. stage bytes in quarantine and persist opaque metadata plus audit events;
7. record duplicate detection, lifecycle state transitions, expiry, deletion,
   reset, and recovery evidence; and
8. render deterministic review and recovery flows in the local shell.

## Exclusions

The bounded implementation must not add:

- any live or real document handling;
- any non-PDF intake;
- any network service, remote user, or non-loopback bind;
- any filesystem discovery, source-location upload, or server-side file-path
  selection;
- any external execution surface or publication artifact; and
- any later-phase capability outside bounded synthetic intake, custody, review,
  and lifecycle evidence.

## Architecture

The runtime consists of:

- signed synthetic receipt verification;
- in-process PDF admission and inspection;
- durable SQLite metadata;
- staged and quarantined custody objects;
- append-only audit evidence;
- review annotations over sanitized derived output; and
- lifecycle operations for expiry, deletion, reset, and recovery.

The browser pushes bytes directly to the local shell. The server never receives
or resolves a client filesystem path.

## Acceptance criteria

Implementation is complete only when:

- synthetic PDF fixtures are deterministic and repository-safe;
- admission rejects invalid media type, invalid PDF signature, and oversize
  payloads;
- custody records opaque identifiers, SHA-256 identity, lifecycle state, and
  audit evidence;
- duplicate handling is deterministic and preserved in durable metadata;
- deletion, reset, expiry, and recovery behavior are deterministic and
  test-covered;
- the local shell remains synthetic-only and loopback-only; and
- validation, documentation checks, and diff hygiene pass without introducing
  excluded capabilities.

## Exact implementation manifest

The implementation manifest contains 48 files: 20 application/runtime files,
16 tests, and 12 direct documentation files.

### Application and runtime - 20 files

1. `pyproject.toml`
2. `uv.lock`
3. `src/collector/document_admission/__init__.py`
4. `src/collector/document_admission/models.py`
5. `src/collector/document_admission/interfaces.py`
6. `src/collector/document_admission/policies.py`
7. `src/collector/document_admission/orchestration.py`
8. `src/collector/document_admission/authorization.py`
9. `src/collector/document_admission/crypto.py`
10. `src/collector/document_admission/durable_repository.py`
11. `src/collector/document_admission/pdf_pipeline.py`
12. `src/collector/document_admission/review.py`
13. `src/collector/document_admission/lifecycle.py`
14. `src/collector/document_admission/runtime.py`
15. `apps/jebediah_executive/__main__.py`
16. `apps/jebediah_executive/app.py`
17. `apps/jebediah_executive/models.py`
18. `apps/jebediah_executive/rendering.py`
19. `apps/jebediah_executive/routes.py`
20. `apps/jebediah_executive/static/styles.css`

### Tests - 16 files

1. `tests/collector/document_admission/test_models.py`
2. `tests/collector/document_admission/test_policies.py`
3. `tests/collector/document_admission/test_admission_orchestration.py`
4. `tests/collector/document_admission/test_cleanup.py`
5. `tests/collector/document_admission/test_package_boundaries.py`
6. `tests/collector/document_admission/test_authorization.py`
7. `tests/collector/document_admission/test_crypto.py`
8. `tests/collector/document_admission/test_durable_repository.py`
9. `tests/collector/document_admission/test_pdf_pipeline.py`
10. `tests/collector/document_admission/test_review.py`
11. `tests/collector/document_admission/test_lifecycle.py`
12. `tests/apps/jebediah_executive/test_app.py`
13. `tests/apps/jebediah_executive/test_routes.py`
14. `tests/apps/jebediah_executive/test_rendering.py`
15. `tests/apps/jebediah_executive/test_accessibility.py`
16. `tests/apps/jebediah_executive/test_phase3b_workflow.py`

### Direct implementation documentation - 12 files

1. `README.md`
2. `CHANGELOG.md`
3. `CURRENT_SPRINT.md`
4. `PROJECT_STATUS.md`
5. `ROADMAP.md`
6. `docs/ARCHITECTURE.md`
7. `docs/DATA_OWNERSHIP.md`
8. `docs/README.md`
9. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md`
10. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_VALIDATION_REQUIREMENTS.md`
11. `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_LOCAL_OPERATOR_GUIDE.md`
12. `docs/reference/COMPONENT_REGISTRY.md`
