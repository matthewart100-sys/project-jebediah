# P1 Synthetic Organizational Learning Pilot Dependency and Salvage Assessment

**Status:** Proposed dependency and salvage selection; planning authorized,
implementation authority none

**Program:** Organizational Intelligence Product Program

**Planning date:** 2026-08-06

**Canonical planning base:**
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Planning authority:** `CA-2026-08-06-P1-PLANNING`

**Decision owner:** Chief Architect

**Future dependency and implementation owner:** Implementation Engineer within
separately approved scope; Maintainer accountable for dependency custody and
the repository candidate

## Purpose

This assessment selects the smallest dependency boundary for the proposed P1
synthetic organizational learning pilot and records the file- and
function-level disposition of historical pull requests #59 and #60. It exists
to let a future, separately authorized implementation use bounded engineering
lessons without restoring nonconforming architecture or mistaking historical
code for approved code.

This is a planning selection, not an implementation approval. It does not
authorize a package or lock change, source-code change, test execution against
historical code, runtime, deployment, real organizational information, or
public exposure.

## Authority and inspection boundary

Historical Git objects were inspected statically with read-only `git show`,
`git diff`, and `git grep` operations. Neither historical head, its tests, its
servers, its services, its scripts, its dependency environment, nor its
containers were run.

| Evidence | Exact identity | Disposition |
| --- | --- | --- |
| Canonical P1 planning base | `37dd437617ed731340e9fd3da6cab0b1c49f7b4a` | Sole repository authority for this assessment |
| Shared historical proposal base | `9d4aab6777c01b6d0ffebac620fe4a222a6b0ae8` | Comparison point only |
| Pull request #59 head | `525ed481ce8492a644343e3bf665220936e52ad7` | Open historical salvage and audit evidence; no recorded review; must not merge, deploy, or run |
| Pull request #60 source head | `70db20613e6275d391b2221d04e6ab4314d0a7b5` | Historical salvage and audit evidence; must not merge forward, deploy, or run |
| Pull request #60 squash commit | `991929beb6026511e07b6cb7954e1c9e400b9cb5` | Reconciled historical record, not accepted implementation |

No pull request, commit, file, test, dependency, lock entry, passing check, or
historical documentation claim gains authority through existence. In
particular:

- do not cherry-pick, merge, rebase, restore, or wholesale copy either
  historical branch;
- do not check out and execute either historical head;
- do not run historical tests as evidence for P1;
- do not sync either historical lock, start its applications or services, run
  its operations scripts, or build its images; and
- do not treat the word **reuse** in this assessment as permission to copy a
  file or bypass fresh review.

The [Chief Architect Phase 3B reconciliation decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
owns the historical disposition.

## Salvage classification

The matrix uses these exact meanings:

- **Reuse requirement or test intent:** preserve an invariant, vocabulary, or
  test scenario in the new design. It does not authorize copying source.
- **Adapt:** independently implement a narrowly identified pattern after
  comparing it with accepted architecture. The resulting diff must be reviewed
  as new code and satisfy every current validation requirement.
- **Reject:** do not copy, import, execute, configure, or depend on the asset.
  A rejected asset may be cited only to explain a hazard.

There is no whole-file or whole-commit reuse selection.

## Selected P1 dependency boundary

### New direct dependency selected for future implementation

P1 selects exactly one new direct runtime dependency:

```text
cryptography>=50,<51
```

The 50.x compatible line is inherited from the accepted
[Phase 3B Dependency Assessment](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_DEPENDENCY_ASSESSMENT.md).
This constraint is an implementation input, not permission to modify
`pyproject.toml` or `uv.lock` during planning.

A future authorized implementation must resolve one exact compatible patch
release through the repository's approved `uv` workflow and commit the exact
distribution artifacts, hashes, and transitive graph in `uv.lock`. Floating on
the range at runtime is prohibited. The exact patch is not guessed in this
planning document; it must be selected using then-current provenance,
compatibility, license, and vulnerability evidence.

P1 may use the library only for the accepted host cryptographic boundary:

- Ed25519 receipt signing and verification;
- AES-256-GCM authenticated encryption;
- Argon2id passphrase-based key derivation;
- HKDF key separation; and
- maintained serialization helpers required by those primitives.

P1 must not implement a cryptographic primitive, stream construction, key-wrap
algorithm, or authentication construction itself.

### Exact P1 cryptographic profile

Implementation uses `demo-p1-crypto-profile` version `1`:

| Item | Exact P1 value |
| --- | --- |
| Passphrase input | `getpass`; initialize with matching confirmation; 16-128 printable ASCII characters; never argv/env/config/HTML/log |
| Argon2id | 16 random salt bytes, 32 output bytes, 3 iterations, 4 lanes, 65,536 KiB memory |
| Stable content master key | 32 CSPRNG bytes, wrapped only by the Argon2id-derived KEK using AES-256-GCM |
| Object DEK | Fresh 32 CSPRNG bytes for the sole object, wrapped by the master key using AES-256-GCM |
| AEAD nonces | Fresh 12 CSPRNG bytes per master-key wrap, DEK wrap, and object encryption; never reused with a key |
| Object encryption | One-shot AES-256-GCM; no custom stream or chunk construction is needed below the 65,536-byte P1 cap |
| AEAD associated data | Canonical profile/header version, kind, opaque ID, digest, byte count, policy IDs/versions, receipt/submission IDs, and fixed retention deadline |
| Audit key | HKDF-SHA256, 32 bytes, `salt=None`, info `jebediah-p1-audit-hmac-v1` |
| Audit chain | HMAC-SHA256 over canonical event JSON plus the prior event MAC; content-free events only |
| Ed25519 | Raw 32-byte public key, 64-byte signature, full lowercase SHA-256 public-key fingerprint in signer-key ID |
| Binary serialization | Strict unpadded base64url; digests and fingerprints are exactly 64 lowercase hex characters |
| Canonical records | UTF-8 JSON, sorted keys, separators `,` and `:`, no NaN, exact schema version `1` |

Envelope and record readers reject any other version, KDF value, length,
encoding, unknown field, duplicate key, malformed time, or associated-data
mismatch before allocating from caller-controlled parameters or decrypting.
The exact Argon2id resource profile is reviewed and exercised on the authorized
implementation host; inability to support it is a stop condition, not permission
to weaken it silently.

### Standard-library and existing test facilities

| Need | Selected facility | Constraint |
| --- | --- | --- |
| Durable custody metadata | Python `sqlite3` / runtime SQLite | Record the runtime SQLite identity; use no new database package |
| Digest, token, and constant-time operations | `hashlib`, `hmac`, and `secrets` | Use only for their documented purposes; do not construct encryption |
| Data and policy models | `dataclasses`, `enum`, `datetime`, `json`, and typing facilities | Keep domain models immutable where selected by ADR 0019/0020 |
| Loopback request and response boundary | Existing WSGI and Python standard-library parsing/escaping | No new web framework, client, template engine, or JavaScript chain |
| Deterministic fixture generation | Python standard library and reviewed constants | No PDF parser; generated bytes must match the compiled manifest digest |
| Tests | Existing `pytest` development dependency | No new test dependency selected by P1 |

### Existing repository dependencies are not P1 dependencies

Canonical base already declares dependencies used by other components,
including `ollama`, `pydantic`, `qdrant-client`, `fastapi`, and `uvicorn` and
their transitives. Their presence in the repository environment does not
authorize P1 to import, invoke, wrap, or reach them.

P1 packages must have no dependency edge to a model, embedding, vector,
Memory Service, API-service, general HTTP-client, or service-server package.
Static import analysis and runtime network denial must establish this boundary;
a statement that P1 does not intend to use an installed package is
insufficient.

### Phase 3B selections not inherited by P1

The Phase 3B assessment also selects future B2 worker capabilities: rootless
Podman, qpdf, `pypdf`, ClamAV, Poppler, Tesseract, language data, worker images,
and scanner-signature artifacts. P1 inherits none of them. P1 accepts only the
exact repository-generated fixture by identity and digest and performs no
general PDF parsing, scanning, rendering, OCR, embedded-object traversal,
container execution, or subprocess inspection.

Using any later Phase 3B worker dependency would expand the P1 architecture and
requires a new Chief Architect decision before dependent work continues.

## Forbidden dependency and transitive capabilities

The future dependency and lock diff must add only `cryptography` and transitives
strictly necessary for that selected distribution. It must not add or activate
any of these capability classes for P1:

| Forbidden capability | Examples or boundary evidence | Reason |
| --- | --- | --- |
| General document input | File picker, multipart upload, source path, URL, paste, drag-and-drop, arbitrary bytes | P1 accepts one generated fixture selected internally by exact identity and digest |
| PDF parsing or repair | `pypdf`, qpdf, pikepdf, PyMuPDF, OCRmyPDF, generic MIME parsers | P1 is not B2 and does not inspect arbitrary PDFs |
| Malware scanning, rasterization, or OCR | ClamAV, Poppler, Tesseract, language packs | Later isolated-worker scope only |
| Container or subprocess execution | Podman, Docker, worker images, shell helpers | No worker, infrastructure, or deployment boundary exists in P1 |
| Model or embedding execution | `ollama`, model SDKs, tokenizer or embedding packages | P1 answers are fixed and deterministic |
| Memory or vector retrieval | Memory Service clients, `qdrant-client`, vector or semantic-ranking packages | ADR 0019 selects a session projection and ADR 0020 selects deterministic exact retrieval |
| New HTTP client or API service | `requests`, `httpx`, FastAPI use, Uvicorn use, OpenAI-compatible endpoints | P1 adds no network client or service boundary |
| Authentication or tenancy | Account, user database, reset, session-identity, organization, workspace, or RBAC packages | D2 and multi-tenant scope are excluded; the fixed process action token is not identity |
| Browser or frontend framework | JavaScript packages, bundlers, browser automation runtime, template engines | Existing server-rendered shell and progressive HTML are sufficient |
| Deployment or operations | Docker, Caddy, TLS, DNS, infrastructure, workflow, backup, restore, or public-server packages | O1, deployment, and public exposure are excluded |
| Cloud or external processing | OCR, malware, storage, telemetry, analytics, model, or retrieval API clients | P1 is literal loopback with zero external-network behavior |

This prohibition applies to imports and runtime reachability as well as newly
declared packages. A capability does not become acceptable because it arrives
transitively, already exists in the repository lock, is dynamically imported,
or is hidden behind a fallback.

## Pull request #59 salvage matrix

Pull request #59 changed 39 paths. Its useful material is limited to selected
primitive families, bounded model/view ideas, and test intent.

| Historical file or symbol | Decision | Selected lesson | Rejected behavior and future verification |
| --- | --- | --- | --- |
| `src/collector/document_admission/crypto.py::{hash_content_identity,_derive_kek,create_master_key_envelope,unlock_master_key,encrypt_object,decrypt_object,derive_audit_hmac_key,audit_hmac_hex}` | Adapt | Argon2id, AES-GCM, random master key/DEK/nonces, wrapped-key AAD, HKDF separation, and SHA-256 content identity align with accepted primitive families | Do not copy the old dependency range or wrappers unchanged. Validate versioned envelopes before KDF/decrypt, bound KDF parameters, validate base64 and lengths, map failures explicitly, use safe AAD, and test wrong passphrase, tamper, malformed headers, digest mismatch, and nonce behavior |
| `src/collector/document_admission/authorization.py::{canonical_receipt_payload,sign_receipt,SyntheticReceiptVerifier}` | Adapt | Canonical receipt serialization and Ed25519 verification are useful patterns | The verifier omits several policy predicates and does not normalize invalid-signature failures. Add version, signer, purpose, classification, operation, environment, not-before, expiry, lifetime, content binding where selected, and single-use checks |
| `src/collector/document_admission/authorization.py::synthetic_signing_key` | Reject | A generated per-test key may support verifier cases; the fresh P1 plan separately defines an ephemeral `SyntheticFixtureAuthority` adapter | The runtime must never contain the fixed historical private key. Custody and the coordinator must never sign; the separate adapter may issue only the exact short-lived P1 receipt and never persists its private key |
| `src/collector/document_admission/durable_repository.py::Phase3BDurableRepository` | Reject implementation; adapt schema separation only | Separate receipt, source-object, artifact, review, state, and audit concepts help identify responsibilities | File-before-reservation ordering can orphan bytes; inspection content and notes enter SQLite plaintext; `INSERT OR REPLACE` mutates evidence; review lacks preconditions; audit MACs are unchained and unverified; caller state is trusted; deletion and recovery are incomplete. Design transactions, append-only evidence, lifecycle, reconciliation, and safe internal IDs anew |
| Phase 3B additions in `src/collector/document_admission/models.py` | Adapt shapes | Frozen records, timestamps, digests, page references, submission summaries, and detail views are useful model ideas | Combined states such as `REVIEW_APPROVED` conflict with the separate admission/transformation state and append-only disposition boundaries. Use the exact ADR 0019 disposition and lineage vocabulary and enforce cross-record invariants |
| Changes to `interfaces.py`, `orchestration.py`, `policies.py`, and `__init__.py` | Adapt narrowly | Protocol injection, PDF-only limits, and explicit policy bundles are useful | Do not carry overlapping Phase 2/3 policy authority or expose inert policy fields. Enforce every selected predicate at its owner boundary and keep packages acyclic |
| `runtime.py::SyntheticPhase3BDocumentAdmissionRuntime` | Reject | None beyond identifying composition hazards | It constructs its signer, issues receipts, owns persistence, and inspects synchronously in the host, collapsing authority and component boundaries |
| `pdf_pipeline.py::Phase3BPDFPipeline.inspect_payload` | Reject as runtime; adapt only the idea of an injected fake in tests | An explicitly named fake inspector can drive deterministic unit tests | Literal marker parsing, string checks for malware/JavaScript, fabricated native captures, and success after scanner warnings are not inspection. P1 must not ship or claim an inspector |
| `review.py` and `lifecycle.py` | Reject | None | Thin repository pass-through wrappers establish no invariant; lifecycle and disposition behavior must be owned by explicit application/domain boundaries |
| `apps/jebediah_executive/{app,models,rendering,routes,__main__}.py` and `static/styles.css` | Adapt presentation and request-test intent | Sanitized workspace/detail views, progressive forms, method handling, and bounded-body ideas can inform the existing shell | The launched CLI never injects the workspace service, so the historical workflow is not integrated. Do not copy multipart upload. Future fixed actions require strict route, method, length, content-type, origin, action-token, escaping, redirect, and log tests under ADR 0020 |
| `tests/collector/document_admission/*` additions and modifications | Reuse requirement and test intent | Receipt, crypto round-trip, repository, lifecycle, model, cleanup, and boundary scenarios identify test categories | They do not prove malformed crypto, crash ordering, tamper, plaintext absence, audit verification, exact transition rules, or actual P1 integration. Replace with the P1 validation suite |
| `tests/apps/jebediah_executive/*` additions and modifications | Reuse requirement and test intent | Preserve accessibility, safe rendering, method allowlist, sanitized logs, and no-source-echo expectations | Fake-service GET tests do not prove the dashboard-domain learning loop. Test the real coordinator and application composition with the same question before and after approval |
| `pyproject.toml` and `uv.lock` | Reject | None | Historical `cryptography` 45.x selection is superseded. Future P1 uses `cryptography>=50,<51` with a fresh exact lock and supply-chain review |
| `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md` changes and `docs/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_LOCAL_OPERATOR_GUIDE.md` | Reject as current guidance | Retain only synthetic-only, no-remote-fetch, no-source-path, and no-real-information constraints | The guide claims a workflow the CLI does not compose and uses review states inconsistent with current architecture. Historical text grants no authority |

## Pull request #60 salvage matrix

Pull request #60 changed 79 paths and combined custody, promotion, retrieval,
models, memory, identity, services, deployment, and operations. Its broad
composition is the failure mode P1 must avoid.

| Historical file, symbol, or path group | Decision | Selected lesson | Rejected behavior and future verification |
| --- | --- | --- | --- |
| `src/collector/document_admission/authorization.py::{canonical_receipt_payload,Ed25519ReceiptVerifier.verify}` | Adapt; preferred receipt-policy reference | It checks signer, purpose, classification, operation, single-use policy, lifetime, not-before, expiry, and signature | Add explicit payload version, selected content/environment binding, structured signature failures, immutable policy inputs, and full negative/replay/crash tests. Historical signing helpers are not reused; the fresh P1 authority adapter owns its narrowly specified signing behavior |
| `src/collector/document_admission/crypto.py` | Reject completely | None | Custom SHA-256-derived XOR streaming, HMAC construction, PBKDF2 wrapping, and hard-coded policy conflict with ADR 0016. No PR #60 cryptographic code is salvageable |
| `src/collector/document_admission/durable_repository.py::SqliteDurableRepository` | Adapt mechanics only | Same-filesystem temporary publication, `flush`/`fsync`/replace, append-only SQLite triggers, reservation ordering, and reconciliation outcomes are useful patterns | Caller-controlled object paths permit traversal; conflicts can overwrite objects before database failure; permissions are not hardened; audit-chain concurrency and verification are incomplete; tombstone ordering is unsafe; expiry is optional; digest reconciliation is incomplete. Implement safe internal IDs, transaction ownership, fail-before-decrypt, and verified recovery anew |
| `runtime.py::{validate_pdf_admission,DocumentCustodyRuntime.admit}` | Adapt only envelope-validation and reservation concepts | Minimal magic, EOF, size, and receipt-reservation-before-bytes behavior are appropriate B1 ideas | Remove DOCX/TXT/Markdown activation. P1 must additionally bind the exact generated fixture identity and digest and must not represent envelope checks as PDF safety inspection |
| `lifecycle.py::{is_expired,deny_if_expired}` | Adapt | Fail-before-decrypt and whole-scope hold behavior are useful requirements | Eligibility cannot be an optional caller step. Redesign deletion, key destruction, tombstones, reset, backup implications, and restart behavior to current P1 policy |
| `models.py`, `interfaces.py`, `policies.py`, and `failures.py` | Adapt | Authorization/custody records, verification results, reconciliation findings, and explicit failure categories provide useful type ideas | Keep PDF-only, use internally safe opaque IDs, forbid unguarded plaintext reads, and align all states with ADR 0016/0019/0020 |
| `src/collector/organizational_intelligence/bridge.py::Phase3CBridge` and its models | Reuse behavior vocabulary; reject implementation | `INSUFFICIENT_EVIDENCE`, `GROUNDED`, citations, provenance, deterministic ordering, and unauthorized-use denial are valuable acceptance vocabulary | It bypasses the Knowledge Registry, accepts `approved: bool`, promotes raw PDF bytes, discards reviewer evidence, keeps ungoverned process state, uses substring matching, and lacks claim-level lineage. Implement ADR 0019/0020 fresh |
| `tests/collector/organizational_intelligence/test_phase3c_bridge.py` | Reuse test intent | Preserve approval gating, consumer/use denial, citations, provenance, and audit scenarios | Require the exact same question and continuing system state before and after approval. Submission, rejection, expired/deleted/superseded evidence, wrong policy, or partial publication must never ground an answer |
| `apps/jebediah_executive/governed_provider.py` | Reject completely | Retain only the architectural need for one small provider/coordinator boundary | The file mixes custody, promotion, registry-bypassing bridge state, Memory, Qdrant, Ollama, embeddings, organization/workspace state, and presentation. It silently falls back, mislabels homemade embeddings, creates new keys, self-signs receipts, fabricates confidence/type metadata, and can produce contradictory answers |
| `apps/jebediah_executive/auth.py` | Reject | None for P1 | Accounts, password reset, user persistence, sessions, organizations, workspaces, and identity are D2 scope and do not provide adequate action-level authorization here |
| `apps/jebediah_executive/{app,models,rendering,routes}.py` and `static/styles.css` | Adapt only bounded view concepts | Insufficient/grounded, trace, review, and status rendering can inform ADR 0020 view models | Unbounded body reads, authentication-off mutation, incomplete CSRF behavior, missing role authorization, synthetic fallback, uploads, promotion routes, organization/workspace switching, and broad POST behavior are rejected |
| `services/jebediah-interaction/**` | Reject completely | None beyond documenting why a separate service is unnecessary | The service parses PDFs in-process, stores weakly governed candidates, sends content to a model, assumes Memory APIs, exposes unauthenticated general chat/OpenAI-style endpoints, accepts unbounded base64, and substitutes bearer possession for human disposition |
| `services/jebediah-memory/app/main.py` and `src/collector/memory/**` | Reject for P1 | A producer-owned structured eligibility predicate is a useful future principle | Caller-authored `governance_state=approved` is not approval. Qdrant UUID changes can overwrite immutable points. P1 must not import Memory Service, Qdrant, arbitrary metadata filtering, vector search, or semantic retrieval |
| `docker/production/**`, `scripts/operations/**`, and `tests/docker/**` | Reject categorically | None | Docker, Caddy, public/server configuration, backup, restore, upgrade, deployment, and infrastructure are O1 or later and expressly outside P1 |
| `docs/{ADMINISTRATOR_QUICK_START,BACKUP_GUIDE,DEMONSTRATION_GUIDE,DEPLOYMENT_GUIDE,DISASTER_RECOVERY_GUIDE,OPERATIONS_GUIDE,PRODUCTION_CONFIGURATION_GUIDE,WORKSPACE_GUIDE}.md` | Reject as guidance | They remain historical audit evidence only | Do not restore or execute their commands; they cannot supply operational readiness or authority |
| Changes to `README.md`, `CHANGELOG.md`, `CURRENT_SPRINT.md`, `PROJECT_STATUS.md`, architecture, standards, component registry, and governance files | Reject as canonical input | Their later reconciliation identifies claim and boundary hazards | Current canonical documents, accepted ADRs, and a fresh implementation diff own all claims |
| PR #60 application, domain, service, memory, and Docker tests | Reuse limited negative/test vocabulary only | Insufficient/grounded, citation, route, dependency-boundary, and operational-artifact scenarios identify areas requiring evidence | Historical tests validate their own nonconforming implementation, not P1. They must not be run as P1 evidence or copied wholesale |
| `pyproject.toml`, service requirements, Docker build dependencies, and `uv.lock` | Reject | None | Historical `cryptography` 43.x, `pypdf` 5.x, service/model/vector, and deployment graphs are not P1 dependencies. Generate a fresh exact lock from canonical base only after implementation authority |

## Selected salvage extraction order

If implementation is later authorized, work must proceed as new code in this
order:

1. Start from the exact authorized canonical base and record its dependency and
   lock state.
2. Add only `cryptography>=50,<51`; resolve and review the exact lock delta.
3. Implement receipt-policy behavior using PR #60 only as a static comparison
   and cryptographic primitive wrappers using PR #59 only as a static
   comparison.
4. Design custody transactions, encrypted object publication, append-only
   audit, lifecycle, safe IDs, and recovery anew; use selected PR #60 atomic
   publication and reconciliation ideas only after failure-injection design.
5. Implement ADR 0019 promotion, registry metadata, and session projection
   fresh. Do not port `Phase3CBridge`.
6. Implement ADR 0020 deterministic retrieval and the existing-shell
   coordinator fresh. Adapt only safe rendering and test vocabulary.
7. Prove the complete same-question learning loop and every forbidden
   capability at one unchanged exact head.

No step may use a historical cherry-pick as a shortcut. Similar code still
requires line-by-line behavioral review against the current threat model and
validation requirements.

## Required future implementation verification

### Dependency and supply-chain evidence

At the exact future implementation head, record and review:

- the pre-change `pyproject.toml` and `uv.lock` state;
- a dependency diff showing `cryptography>=50,<51` as the only new direct
  dependency selected by P1;
- the exact resolved cryptography patch, source, wheel/sdist artifact hashes,
  Python 3.12 compatibility, license, and all changed transitives;
- the vulnerability-review method, results, date, and limitations without
  claiming that any tool proves absence of unknown vulnerabilities;
- `uv lock --check` and a clean `uv sync --frozen` result;
- proof that no parser, scanner, OCR, web, model, vector, frontend, container,
  deployment, or operations dependency entered because of P1; and
- rollback to the prior reviewed lock plus cryptographic compatibility and
  authorized-reset evidence.

Any unexplained lock change, mutable source, missing artifact hash,
incompatible license, or broader direct dependency is blocking.

### Static boundary and provenance evidence

The exact diff must establish:

- the changed-file inventory equals the separately accepted P1 manifest;
- no historical file or commit was cherry-picked or copied wholesale;
- every adapted function has its historical provenance and current rationale
  recorded in review evidence;
- P1 import graphs do not reach Ollama, Qdrant, Memory Service, FastAPI,
  Uvicorn, general HTTP clients, PDF parsers, scanners, OCR, authentication,
  workspace, deployment, or operations code;
- no dynamic import, plugin lookup, subprocess, environment switch, or fallback
  can activate a forbidden capability;
- the route inventory contains only the fixed ADR 0020 read and action routes;
- no file picker, upload, source path, URL, paste, free-form question, general
  API, or public listener exists; and
- repository scans find no real organizational information, credentials,
  private paths, fixture plaintext in custody artifacts, or generated runtime
  data.

Text search alone is insufficient. Use import/AST inspection, full diff review,
route inventory, dependency graph inspection, runtime socket denial, and
filesystem evidence.

### Cryptography, authorization, and custody evidence

Tests must cover:

- canonical and versioned receipt payloads;
- valid and invalid Ed25519 signatures, wrong signer, wrong purpose,
  classification, operation, environment, content binding, not-before, expiry,
  lifetime, replay, and crash-after-reservation cases;
- Argon2id parameter validation and upper bounds;
- AES-GCM round trip, wrong passphrase/key, header/version/base64/length
  corruption, ciphertext/tag/AAD tamper, nonce uniqueness, and digest mismatch;
- HKDF separation and audit-integrity verification;
- internal opaque IDs, traversal, absolute-path, separator, collision,
  symlink/reparse, and unsafe-runtime-directory cases;
- transaction interruption before and after reservation, temporary write,
  `fsync`, publication, SQLite commit, audit append, reset, and deletion;
- no plaintext source or approved projection in SQLite, logs, UI, audit,
  exceptions, or review artifacts; and
- restart reconciliation, corruption, expiry, reset, and unknown-outcome
  behavior that fails closed.

### Promotion, retrieval, and product evidence

Tests must prove:

- custody, candidate creation, registry registration, or projection construction
  alone is never approval;
- approval requires the exact immutable fixture digest, candidate, disposition,
  reviewer/process identity, policy, consumer, intended use, transformation,
  and lifecycle predicates from ADR 0019;
- rejection, a conflicting second disposition, partial publication, wrong
  lineage, expiry, deletion, supersession, unknown policy, or restart cannot
  produce eligible evidence;
- the Knowledge Registry remains metadata-only;
- registry and projection publication either complete consistently or fail
  closed with no grounded answer;
- the exact same allowlisted question and identity return `insufficient` before
  approval, remain `insufficient` after submission and rejection, and become
  `grounded` only after successful approval, registration, projection, and
  eligibility;
- the grounded answer is the fixed deterministic statement, not model output;
- exactly one safe source reference and a complete trace reach the fixture,
  digest, submission, custody object, attempt, candidate, disposition, policy,
  registry record, projection, retrieval rule, transformation, and assembly
  time; and
- restart begins with no implicit disposition, registry record, projection, or
  grounded answer even when custody reconciliation succeeds.

### Shell, security, accessibility, and recovery evidence

The real WSGI application composed with the real P1 coordinator must prove:

- literal loopback binding and runtime denial of external sockets;
- fixed route and method handling, request length and content-type bounds,
  duplicate/unknown field rejection, origin/host checks, constant-time action
  token verification, safe redirects, escaping, and sanitized failures;
- presentation contains no custody, promotion, retrieval, or answer-synthesis
  logic;
- no source bytes, secrets, tokens, paths, raw exceptions, or ineligible
  content appear in HTML or logs;
- keyboard-only, focus, landmark, heading, label, error, status, contrast,
  reflow, and no-JavaScript behavior;
- reset is scoped to a verified generated P1 runtime directory, clears every
  eligible representation, rotates process tokens/epoch, and proves no object
  remains; and
- rollback removes P1 routes/composition, restores the prior exact lock, and
  returns the existing shell to its prior deterministic fixture behavior.

The canonical command set and exact evidence format are owned by the
[P1 Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md).
At minimum, the future exact head must record:

```text
uv lock --check
uv sync --frozen
uv run --frozen pytest tests/collector/document_admission
uv run --frozen pytest tests/collector/organizational_intelligence
uv run --frozen pytest tests/apps/jebediah_executive
uv run --frozen pytest tests/integration/test_p1_dashboard_learning_loop.py
uv run --frozen pytest
uv run --frozen python -m compileall -q apps src services tests
python scripts/validate_docs.py
git diff --check <authorized-base>...HEAD
```

Historical test results cannot substitute for any of this evidence.

## Stop conditions

Stop dependent implementation and return to the Chief Architect if work would:

- change the `cryptography` major release line or selected primitives;
- add another direct dependency or an unexplained transitive capability;
- require a parser, scanner, OCR worker, container, subprocess, model, vector,
  Memory Service, API service, authentication, workspace, deployment, or
  network boundary;
- accept arbitrary or real information;
- restore or execute historical PR #59/#60 code;
- store content in the Knowledge Registry or make approved projection durable;
- restore approval implicitly after restart;
- weaken exact fixture, consumer, use, policy, trace, or deterministic-answer
  invariants; or
- diverge from the accepted ADRs or exact authorized implementation manifest.

## Related current planning and architecture

- [P1 Synthetic Organizational Learning Pilot Plan](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Synthetic Organizational Learning Pilot Threat Model](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_THREAT_MODEL.md)
- [P1 Synthetic Organizational Learning Pilot Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
- [P1 Synthetic Organizational Learning Pilot Execution Handoff](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_EXECUTION_HANDOFF.md)
- [ADR 0016: Local Governed PDF Intake and Custody Boundary](adr/0016-local-governed-pdf-intake-and-custody-boundary.md)
- [ADR 0019: Governed Synthetic Evidence Promotion](adr/0019-governed-synthetic-evidence-promotion.md)
- [ADR 0020: Executive Pilot Read Model and Deterministic Retrieval](adr/0020-executive-pilot-read-model-and-deterministic-retrieval.md)

ADR 0016 is the accepted custody boundary. ADR 0019 and ADR 0020 are proposed
P1 decisions until they receive their required reviews, Chief Architect
acceptance, activation, and merge. Their presence does not authorize dependent
implementation.

## Related historical audit and salvage evidence

- [Chief Architect Phase 3B Reconciliation Decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
- [Phase 3B Dependency Assessment](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_DEPENDENCY_ASSESSMENT.md)
- [Phase 3B Governed Intake Plan](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md)
- [Phase 3B Threat Model](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_THREAT_MODEL.md)
- [Phase 3B Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_VALIDATION_REQUIREMENTS.md)
- [Phase 3B Lifecycle and Recovery](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_LIFECYCLE_AND_RECOVERY.md)
- [Historical Phase 3B Milestone 1 Authorization](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_MILESTONE_1_AUTHORIZATION.md)
- [Historical Phase 3B Implementation Activation](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_IMPLEMENTATION_ACTIVATION.md)
- [Historical Phase 3B Completion Directive](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md)
- [Pull request #59](https://github.com/matthewart100-sys/project-jebediah/pull/59)
- [Pull request #60](https://github.com/matthewart100-sys/project-jebediah/pull/60)

Historical documents remain evidence of prior intent, hazards, and salvage
possibilities. The reconciliation decision and current canonical planning
package control whenever wording conflicts.

## Review record

This assessment records a planning-stage static inspection and dependency
selection only. Required architecture review, Chief Architect acceptance,
implementation activation, exact-head implementation review, merge approval,
and merge remain pending.
