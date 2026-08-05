# Phase 3B Governed Intake Validation Requirements

**Status:** Proposed; applies to the exact bounded implementation only

## Evidence principles

- Generated synthetic PDF fixtures only.
- No existing VBA or organizational file may be discovered, opened, copied,
  hashed, scanned, parsed, OCR-processed, stored, displayed, or logged.
- Tests prove behavior, not truth, operational readiness, or malware absence.
- Every negative authority and capability boundary is executable.
- Linux rootless Podman evidence must prove controls are enforced, not merely
  present in a command.

## Exact test inventory

### Contract and authority tests

- Existing Phase 2 immutable models and state transitions remain compatible.
- Receipt schema, canonical serialization, signature, signer role, expiry,
  environment, purpose, classification, operation, and retention policy.
- Exact source-authority and information-owner principals or role holders,
  source issue/version date, independently verifiable authority evidence, and
  signer trust binding to role, organization, domain, document scope, and
  effective period.
- Unknown/revoked signer, altered receipt, wrong environment, expired receipt,
  missing expected digest, digest mismatch, and replay denial.
- Receipt is reserved before body read and cannot be reused after interruption.
- Browser upload contract has no server path or directory field.
- Legal-hold declaration/lift signature, role, scope, expiry, and operator
  self-authorization denial.

### Cryptography and custody tests

- Secure master key and DEK generation.
- Argon2id parameter/version validation and wrong-passphrase denial.
- AES-GCM round trip, associated-data mismatch, tag failure, truncated object,
  nonce uniqueness, chunk ordering, and length/digest verification.
- Passphrase rotation preserves object and historical audit verification.
- No plaintext source, receipt, or evidence exists in the runtime directory,
  SQLite, WAL, logs, backups, or host temporary paths.
- Atomic object creation and failures at every flush/replace/commit boundary,
  including proof that state and its audit event commit or roll back together.
- Orphan, missing, corrupt, duplicate, and tombstoned-object reconciliation.
- Database constraints prevent updates and individual deletion of append-only
  evidence; only the authenticated whole-epoch pruning transaction is allowed.
- Audit hash/HMAC chain, epoch closure, retained closure anchor, hold-blocked
  pruning, whole-epoch expiry, interrupted pruning, and restore propagation.

### Admission and worker tests

- PDF signature and extension/media-type disagreement.
- Native-text, image-only, mixed, encrypted, malformed, truncated, unsupported,
  JavaScript, launch, XFA, AcroForm, attachment, portfolio, rich-media, URI,
  EICAR, and signature-stale fixtures.
- Page, object, nesting, decoded stream, character, finding, output, memory,
  CPU, PID, tmpfs, and wall-clock limits.
- Scanner unavailable/error/timeout and clean/positive outcomes.
- qpdf recovery disabled and malformed input rejected rather than repaired.
- `pypdf` strict native extraction with page references, warnings, omissions,
  and bounded output.
- OCR invoked only for eligible insufficient-native-text pages; engine,
  language, page, quality, and limitations recorded.
- OCR unavailable, timeout, low quality, page limit, and rendering failure.
- Worker stdout oversize, malformed JSON, unknown fields/vocabulary, invalid
  UTF-8, injection strings, and non-zero/signal exits.
- Worker cannot access network, host runtime paths, secrets, SQLite, object
  directory, or another worker.

### Lifecycle and review tests

- Exact ADR 0013 transitions and terminal immutability.
- Retry creates a linked attempt and does not rewrite failure.
- Exact duplicate creates a new occurrence; changed bytes create a new content
  identity.
- Explicit supersession, conflict hold, and no automatic reactivation.
- Review workspace displays identity, page, method, quality, warnings, omissions,
  limitations, classification, purpose, and retention.
- Approval, rejection, correction, and supersession are append-only annotations.
- Approval cannot create a Knowledge Object, registry record, memory record,
  embedding, Qdrant point, retrieval result, or supported Ask answer.
- Seven-, thirty-, and 365-day retention boundaries, including denial before
  decrypt/display and synchronous cleanup when expiry occurs without restart.
- Expired content with an active hold remains encrypted and retained but cannot
  be decrypted, displayed, reviewed, or consumed.
- Reset by submission, lineage, and domain.
- Active hold blocks reset/deletion without partial effects.
- Cleanup failure remains visible and is never reported as completion.
- Backup registration and opaque inventories, mandatory purge of every
  applicable pre-deletion backup, missing-backup `cleanup_failed`, and tombstone
  propagation.

### Backup, restore, and rotation tests

- Consistent SQLite snapshot with concurrent mutations blocked.
- Backup interruption at every reservation, ledger, snapshot, copy, manifest,
  verification, completion, abort, and local-registration boundary; verified
  abort closes a pending registration without blocking deletion.
- Manifest identity/HMAC and corrupt/missing/extra object denial.
- Backup contains no passphrase/plaintext.
- Restore into staging only; no partial activation.
- Wrong wrapper, wrong trust registry, incompatible schema, corrupt event chain,
  expired retention, and unresolved tombstone denial.
- Recovery-authority signature, role, monotonic generation and chain; missing,
  stale, rolled-back, malformed, unavailable, or backup-local-only ledger denial.
- A pre-deletion backup blocks deletion completion until physically purged;
  unregistered backups and backups with unresolved purge obligations cannot
  restore; a copied valid pre-deletion set remains revoked after current-runtime
  loss; deleted content does not return after restore.
- Passphrase and trust-key rotation preserve historical verification and deny
  revoked new authority.

### Application and browser tests

- Literal `127.0.0.1` bind and configurable non-loopback rejection.
- Bootstrap token exchange, redirect removal, strict cookie, CSRF, Host/Origin,
  session expiry, cache, CSP, frame, MIME, and referrer headers.
- Upload streaming, progress/status, interruption, retry, and safe errors.
- Keyboard-only authorization, file selection, submit, review, approve, reject,
  correction, supersede, reset, and confirmation workflows.
- Focus moves to errors/status; all controls have names/instructions; no
  color-only state.
- Loading, empty, insufficient, held, failed, disconnected, expired,
  unauthorized, cleanup-failed, and success states.
- 320px and 1280px layouts, 200% zoom, reduced motion, and print.
- Browser storage remains empty; responses are `no-store`.
- Request capture shows only loopback traffic and zero external requests.
- Before upload Ask is insufficient; after Phase 3B review Ask remains
  insufficient because Phase 3C is absent.

### Package and capability tests

- Document-admission runtime cannot import Knowledge Registry, memory, Ollama,
  model, embedding, Qdrant, retrieval, n8n, Open WebUI, or external HTTP clients.
- Executive Product Shell cannot bypass the Phase 3B service boundary or read
  custody files directly.
- Worker modules cannot import host application or custody packages.
- No DOCX support or hidden format fallback.
- No export, remote bind, telemetry, analytics, model, action, or deployment
  path.
- Only the exact 59-file manifest changes.

## Generated fixtures

Fixtures are created in tests and never copied from existing documents:

- minimal native-text PDF;
- image-only PDF with known synthetic text;
- mixed native/image PDF;
- malformed and truncated PDFs;
- encrypted PDF;
- PDF with each prohibited active-content feature;
- EICAR-bearing synthetic PDF;
- page/object/stream/resource boundary PDFs;
- duplicate and changed-content versions;
- interrupted upload/custody streams; and
- generated Ed25519 receipt, legal-hold, and trust-registry keys conspicuously
  labeled `SYNTHETIC TEST ONLY`.

Fixture keys and trust roots must fail the real-authorized environment guard.

## Container proof

CI on Linux must build immutable worker images and demonstrate:

- rootless execution;
- no network;
- non-root UID/GID;
- read-only root;
- no capabilities;
- no-new-privileges;
- pinned seccomp;
- no host mounts;
- cgroups v2 memory, CPU, and PID controller delegation;
- actual OOM/PID/time-limit termination;
- tmpfs and stdout caps;
- image and tool identities; and
- SBOM and vulnerability/license reports.

If GitHub-hosted CI cannot prove a rootless controller, the package cannot claim
that validation and implementation review remains blocked until an approved
runner supplies the evidence.

## Required commands

During implementation, targeted selectors may be used. Before publication:

```text
uv sync --frozen
uv run pytest tests/collector/document_admission tests/apps/jebediah_executive
uv run pytest
uv run python -m compileall -q apps src tests workers
uv lock --check
uv run python scripts/validate_docs.py
git diff --check <implementation-base>...HEAD
```

The Phase 3B workflow must additionally build and test all worker images, run
container-isolation assertions, produce SBOM/SCA/license evidence, and execute
the synthetic browser workflow. Browser tooling may be an approved CI/operator
prerequisite but must not become a shipped runtime dependency without review.

## Documentation-package validation

Before this architecture package is published:

```text
uv run python scripts/validate_docs.py
git diff --check
```

Also verify:

- all links;
- ADR numbering and status;
- exact architecture and implementation manifests;
- no secret/private value;
- no unsupported operational or live-information claim;
- no Pylance MCP dependency;
- one branch, one PR, and one reviewer; and
- clean synchronized worktree.

## Implementation acceptance

Implementation is eligible for independent review only when every required test
passes, exact file scope matches, the operator guide reproduces the synthetic
workflow, no real information was accessed, and all residual limitations remain
visible.
