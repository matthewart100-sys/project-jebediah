# P1 Synthetic Organizational Learning Pilot Validation Requirements

**Status:** Proposed; no implementation authority

**Planning base:**
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Decision owner:** Chief Architect

**Validation owner:** Future authorized Implementation Engineer, followed by
an independent exact-head reviewer

## Purpose

These requirements define the evidence needed to accept a future P1
implementation. They prevent a collection of passing unit tests or static
screens from being mistaken for the complete governed learning loop.

The validation target is one exact implementation head and its complete
64-path diff. Evidence from historical pull requests, another commit, a changed
head, a static fixture, or a narrower test is insufficient.

## Validation principles

- Prove the product journey and every authority boundary.
- Use generated synthetic information only.
- Test failure and absence, not just success.
- Keep deterministic and probabilistic behavior distinguishable; P1 has no
  probabilistic behavior.
- Treat dependency, security, recovery, accessibility, and rollback evidence as
  first-class completion requirements.
- Record exact commands, environment class, commit, results, limitations, and
  reviewer.
- Do not infer broad readiness from one green check.

## Primary acceptance journey

At one unchanged exact head, a browser validation must perform these steps in
order:

1. Start the P1 composition on literal `127.0.0.1` with an isolated generated-
   state directory and no external service.
2. Open `/ask/insufficient-program-outcomes`.
3. Observe `insufficient` with no statement, source reference, or evidence
   trace. Ask remains a pure GET read.
4. Open `/workspace` and submit the exact generated P1 PDF fixture.
5. Observe accepted custody metadata, exact digest, and pending disposition.
6. Ask the same question and observe that it remains `insufficient`.
7. Approve the same candidate.
8. Observe one approved registry metadata record and one active session
    projection without source bytes.
9. GET the exact same route and observe `grounded`.
10. Inspect the answer and verify the complete evidence trace.
11. Reset the pilot and observe that the question returns to `insufficient` and
    no generated state remains eligible.

The evidence must show that the route, question identity, and text in steps 2,
3, 6, 9, and 11 are identical: `GET
/ask/insufficient-program-outcomes` and the compiled preset. The success path
admits one occurrence of one generated PDF.

A separate fresh-application browser scenario submits the same generated
fixture, records the fixed reject disposition, and proves that the unchanged
GET remains `insufficient`. Rejection evidence cannot be combined with a second
submission in the primary success path.

## Requirement-to-evidence matrix

| ID | Requirement | Required evidence |
| --- | --- | --- |
| P1-001 | Existing Executive Product Shell is the primary interface | Browser route and package-boundary evidence; no replacement UI |
| P1-002 | Same allowlisted question is used throughout | Contract test plus browser capture of exact question ID/text |
| P1-003 | Initial answer is insufficient | Domain, app, and browser evidence with no statement/reference/trace |
| P1-004 | Only exact generated PDF may enter custody | Fixture-digest, invalid-ID, changed-byte, format, MIME, and size tests |
| P1-005 | Custody encrypts bytes and records deterministic identity | Cryptographic known-behavior, storage inspection, and round-trip tests |
| P1-006 | Interrupted custody is reconciled visibly | Failure-injection and restart tests for every durable boundary |
| P1-007 | Submission alone does not affect retrieval | Integration and browser state test |
| P1-008 | Evidence derives only from exact digest-to-manifest lookup | Source inspection plus changed-digest and no-parser tests |
| P1-009 | Disposition is explicit and append-only | Approved/rejected/conflict transition tests |
| P1-010 | Rejection cannot promote or ground | Domain, integration, and browser tests |
| P1-011 | Approval is exact-policy scoped | Wrong reviewer, policy, domain, classification, consumer, use, and time tests |
| P1-012 | Registry remains metadata-only | Model inspection, no-content tests, and dependency checks |
| P1-013 | Projection publishes only after registry success | Failure injection and repository state assertions |
| P1-014 | Exact retry is idempotent; divergent retry conflicts | Promotion and repository contract tests |
| P1-015 | Retrieval requires an approved active registry/projection intersection | Pending/rejected/expired/deleted/wrong-use/unknown-policy/split-brain tests |
| P1-016 | Retrieval is deterministic and non-model | Repeated-result test and forbidden import/network checks |
| P1-017 | Grounded answer has one complete lineage trace | Domain, view-model, rendered HTML, and browser assertions |
| P1-018 | Grounding grants no truth or action authority | Required limitation text and forbidden control assertions |
| P1-019 | Reset returns to pristine and removes eligibility | Domain, filesystem, registry, projection, app, and browser tests |
| P1-020 | Restart reconstructs at most an ineligible pending candidate and never restores approval implicitly | Intact/ineligible/tampered custody restart tests with empty registry/projection and insufficient answer |
| P1-021 | Existing static preview remains compatible | Full current shell suite and default-composition smoke test |
| P1-022 | POST surface is fixed and fail-closed | Method, route, content type, length, field, duplicate, token, replay, and redirect tests |
| P1-023 | Rendering and logs expose no protected state | Escaping, log-capture, header, error, and sensitive-value tests |
| P1-024 | Keyboard and semantic accessibility remain usable | Static accessibility suite plus browser keyboard workflow |
| P1-025 | Loopback and external-network exclusions hold | Bind inspection and network-call denial tests |
| P1-026 | Only accepted dependency and lock changes exist | Dependency diff, lock verification, license/provenance review, import tests |
| P1-027 | Historical salvage stays bounded | File/function provenance matrix and forbidden historical path checks |
| P1-028 | Exact manifest is respected | Automated comparison of changed paths to the 64-path plan manifest |
| P1-029 | Full repository remains healthy | Complete tests, compilation, docs validation, and diff check |
| P1-030 | Rollback is complete | Isolated revert/reset rehearsal with post-rollback baseline checks |

## Domain and contract tests

### Generated fixture

Tests must prove:

- deterministic bytes and stable digest for one exact generator version;
- literal `%PDF-` header, terminal EOF marker, bounded byte count, exact
  `application/pdf` media type, and no tracked binary fixture;
- the exact reviewed PDF evidence, grounded statement, limitation, page `1`,
  and `demo-p1-*` visible identities frozen by the P1 plan;
- obvious synthetic labeling inside the reviewed generator source;
- exact fixture identity, media type, domain, classification, consumer, use,
  and source identity;
- changed byte, changed manifest, unknown fixture, excessive size, wrong PDF
  signature, wrong MIME, and malformed envelope fail before custody success;
- manifest selection uses exact digest equality and cannot parse, search, or
  decode caller-supplied PDF text; and
- no real organization, person, account, private address, path, or credential
  occurs in fixtures.

### Custody and cryptography

Tests must cover:

- canonical versioned receipt validation for correct signer, signature,
  purpose, classification, operation, environment, content, not-before,
  expiry, lifetime, and single use;
- receipt reservation before payload durability, including crash behavior;
- SHA-256 identity and byte count;
- unique submission occurrence and deterministic linked duplicate behavior;
- AES-256-GCM authenticated encryption with per-object DEK, unique nonce,
  authenticated associated data, and tamper rejection;
- Argon2id master-key envelope and HKDF-derived audit-key boundaries without
  logging key material;
- wrong passphrase, header, tag, associated data, digest, and length failure;
- SQLite state transitions, audit integrity, object write ordering, and
  transaction failure;
- path-safe opaque IDs, no overwrite on identity collision, restrictive
  storage permissions, and no plaintext in object, SQLite, or log output;
- missing, truncated, swapped, corrupted, or unauthenticated object behavior;
- published orphan after reserved receipt but before metadata/audit commit is
  tombstoned and destroyed, never completed; its receipt stays consumed;
- failure before object write, after object write, before metadata commit, and
  after metadata commit;
- deterministic restart reconciliation of each partial state;
- file flush/`fsync` and atomic same-volume publication on every host;
  directory `fsync` and restrictive-permission verification where supported;
  explicit unsupported-host limitations otherwise;
- expiration and reset of generated state; and
- no backup, restore, legal hold, or live retention claim.

Concurrency tests prove the exclusive runtime lock rejects a second process,
an unsupported lock primitive refuses startup, one in-process `RLock` protects
state and snapshots, and the exact SQLite foreign-key/journal/synchronous/busy-
timeout/`BEGIN IMMEDIATE` profile is active. State and audit either commit
together or neither commits.

Boundary tests cover the exact 900-second receipt lifetime, 65,536-byte
admission cap, 30-day eligible-content deadline, 7-day rejected/failure
ciphertext deadline with immediate access denial, 365-day safe-audit/tombstone
retention, and the rule that retry/review/restart never extends a deadline.

Reset tests prove the locked order: deny retrieval/mark resetting; commit
tombstone plus audit; destroy and verify wrapped-key/ciphertext removal; discard
the process-local disposition/registry/projection epoch; rotate token and epoch.
Injected cleanup failure remains `cleanup_failed`, never grounded or
pristine-success, and succeeds only after an explicit retry completes.

Cryptographic tests validate application usage and failure behavior. They do
not claim independent validation of the underlying library primitives.
They assert every `demo-p1-crypto-profile` version `1` parameter in the
dependency assessment, strict canonical decoding, resource bounds, nonce/key
uniqueness, same-key/same-payload Ed25519 determinism, fingerprint identity,
full associated-data binding, and rejection of every version/parameter/field
deviation.

### Promotion and registry

Tests must cover every eligibility predicate in ADR 0019, including:

- pending and rejected dispositions;
- approval before custody;
- wrong candidate, digest, fixture, source, admission, or custody identity;
- wrong policy, reviewer, domain, classification, consumer, use, or
  transformation;
- naive timestamps, expired evidence, deleted custody, or unknown lifecycle;
- exact approved promotion;
- identical retry and divergent conflict;
- registry conflict or injected failure;
- projection publication failure and cleanup;
- metadata-only registry invariants; and
- complete linked identity and time lineage.

Registry contract tests assert every exact ADR 0019 field mapping, including
versioned single-string policy adapters, and prove that no statement, excerpt,
PDF byte, filename, path, answer, token, key, note, or locator enters the
record.

Clock tests freeze the single injected UTC clock, assert exact microsecond `Z`
serialization, and reject naive, non-UTC, retrograde, filesystem-mtime-derived,
or deadline-inconsistent values.

The approved reason code is exactly
`approve_exact_p1_synthetic_evidence`; the rejected reason code is exactly
`reject_exact_p1_synthetic_evidence`. Reviewer and policy identities are
compiled. Approval before eligible custody, after expiry, or after reset fails
closed.

### Retrieval

Tests must prove:

- exact question/consumer/use match;
- no projection, pending, rejected, expired, deleted, superseded, invalidated,
  wrong-consumer, wrong-use, wrong-question, and conflict behavior;
- one eligible projection plus its exact approved, registered registry record
  yields one stable result;
- read-time `KnowledgeRegistryRepository.find` failure, missing record,
  Registry-only state, projection-only state, identity/digest/provenance
  mismatch, non-approved review, non-registered lifecycle, or temporal
  ineligibility emits no statement, citation, or trace;
- result ordering and content are identical across repeated calls;
- grounded statement is deterministic and derived only from the projection;
- the grounded trace reaches the receipt, signer-key fingerprint,
  authorization-policy version, receipt-verification event/time, candidate,
  promotion decision, registry record, and projection;
- no model, embedding, network, memory, or Qdrant code path executes; and
- successful retrieval does not alter custody, disposition, registry, or
  projection state.

State assertions use the exact ADR 0020 partition: ordinary absence,
pending/rejected/expired/reset/tombstoned evidence is `INSUFFICIENT`; wrong
domain tuple, integrity hold, ambiguity, repository failure, split/mismatch, or
unknown policy/lifecycle is `FAILED`; only the exact eligible pair is
`GROUNDED`.

## Application and presentation tests

### Entry point and runtime root

Tests must prove `--port` alone preserves the static preview and optional
`--p1-runtime-directory` is the only P1 selector. Reject relative, root,
repository/worktree, `.git`-ancestor, symlink/reparse, recognized synchronized-
storage, wrong-marker, nonempty-unmarked, and unknown-artifact paths. Prove
exclusive creation and exact content of the P1 marker, passphrase input through
`getpass` only, nonzero failure before serving, and literal-loopback serving
only after unlock and reconciliation. No host, source, passphrase, key,
environment, or configuration option may exist.

### Request boundary

For every fixed POST route, test:

- accepted exact method and path;
- an inventory of exactly submit, approve, reject, and reset mutation routes;
- GET/HEAD/POST method matrix and `Allow` header;
- unknown, trailing-slash, encoded, nested, and query-string route rejection;
- exact loopback Host and same-origin Origin validation, with no permissive
  CORS or cookie dependency;
- exact `application/x-www-form-urlencoded` content type;
- required numeric Content-Length, no Transfer-Encoding, and rejection of
  missing, negative, non-numeric, excessive, observable short-body, and parsed
  trailing/unknown form data;
- invalid UTF-8, duplicate fields, unknown fields, empty token, wrong token,
  and stale token;
- exact `p1_action_token` name, 43-character unpadded base64url encoding,
  consume-before-domain behavior, and rotation after every boundary-valid
  mutation attempt whether the domain result succeeds or fails;
- constant-time token comparison through owned helper coverage;
- no mutation on any failure;
- fixed 303 redirect after success only; and
- no request value echoed into response, location, header, or log.

Mutation responses close the development-server connection. A raw-socket test
must prove surplus octets cannot become a second request; P1 does not require a
WSGI application to detect unread octets beyond a declared length by blocking
past the bounded input stream.

Successful reset rotates both the synchronizer token and pilot epoch. A form
rendered before reset cannot mutate the new epoch.

Redirect tests assert submit targets `/workspace`; approve, reject, and reset
target `/ask/insufficient-program-outcomes`; and no request value can influence
`Location`.

### Read model and rendering

Tests must prove:

- the briefing is assembled per request in P1 composition;
- the default static provider remains immutable and current tests pass;
- every P1 state is represented honestly;
- ineligible content appears only as sanitized metadata/state;
- grounded answers require a source reference and `EvidenceTrace`;
- the rendered trace includes every authorization-through-promotion identity
  and time required by ADRs 0019 and 0020;
- insufficient and failed answers contain no statement or trace;
- all dynamic strings are escaped;
- evidence identity labels are readable and safe;
- limitations, synthetic status, no-action authority, and local-preview status
  are visible; and
- headers preserve CSP, referrer, nosniff, no-store, UTF-8, and frame denial,
  with `form-action 'self'` only for P1 composition.

### Accessibility

Automated and browser checks must cover:

- unique page title and level-one heading;
- skip link and landmarks;
- associated form labels and descriptive button text;
- logical focus order and visible focus;
- full keyboard completion of the primary journey;
- status changes announced or discoverable without color alone;
- evidence trace rendered as semantic description/list content;
- text enlargement, narrow viewport, print behavior, and reduced motion; and
- no JavaScript dependency.

## Integration tests

One in-process integration test must instantiate real P1 adapters against an
isolated temporary directory and prove the complete primary journey. Mocks may
inject time and failure, but the primary success path must use real generated
bytes, encryption, SQLite metadata, registry adapter, projection adapter,
retriever, coordinator, WSGI app, routes, and rendering.

An HTTP-level integration test must drive the WSGI application through fixed
requests and verify state after each redirect.

Neither test may connect to Qdrant, Ollama, Memory Service, an external network,
or a real browser dependency.

## Browser validation

The future local preview guide defines the exact command. Browser validation
uses an isolated temporary P1 runtime directory outside the repository, literal
loopback, and no external services.

Record:

- source commit and clean status;
- Python and browser versions;
- local start command with sanitized path placeholders;
- every primary-journey step and observed state;
- keyboard completion;
- response security headers through developer tools or an owned HTTP probe;
- absence of external requests;
- reset result and clean shutdown; and
- limitations, including the absence of a third-party accessibility engine if
  one remains unapproved.

Screenshots may supplement but not replace textual observations and automated
assertions. Do not capture local paths, usernames, tokens, or private topology.

## Failure injection and recovery

Inject and verify failure at each owned boundary:

1. generator lookup;
2. authorization validation;
3. encryption;
4. object write;
5. SQLite write and commit;
6. restart reconciliation;
7. disposition append;
8. registry registration;
9. projection publication;
10. retrieval;
11. briefing assembly;
12. rendering; and
13. reset cleanup.

Each failure must have one documented visible state, no false success, no
grounded answer, no sensitive log content, and a deterministic retry or reset
rule.

## Security and negative-capability evidence

The exact head must prove the absence of:

- real or arbitrary document input;
- file picker, multipart upload, source path, URL, paste, or drag and drop;
- general PDF parser, scanner, OCR, native worker, container, or subprocess;
- free-form prompt or question;
- model, embedding, Ollama, Memory Service, Qdrant, vector, or semantic ranker;
- authentication, account, user database, session identity, or multi-tenant
  workspace;
- external network call or asset;
- API service, Docker, Caddy, workflow, infrastructure, deployment, TLS, DNS,
  or public exposure;
- export, analytics, action execution, or authoritative record mutation;
- source bytes, plaintext custody, keys, tokens, content, paths, or raw
  exceptions in logs; and
- executable code or guidance copied wholesale from historical pull requests.

Use source inspection, import graphs or AST checks, route inventory, dependency
diff, filesystem scan, runtime network denial, and complete diff review. A text
search alone is not sufficient where aliases or dynamic imports could bypass a
boundary.

## Dependency and supply-chain validation

The implementation must:

1. record the pre-change dependency and lock state;
2. add only the accepted direct `cryptography` constraint;
3. refresh the lock using the repository's approved `uv` workflow;
4. inspect every changed lock package, version, source, artifact hash, license,
   Python compatibility, and transitive dependency;
5. run `uv lock --check` and `uv sync --frozen` in a clean environment;
6. prove no parser, scanner, OCR, web, model, vector, frontend, or deployment
   dependency entered the graph; and
7. record vulnerability-scan method and limitations without fabricating a clean
   result if no approved scanner is available.

## Required commands

Run from the repository root at the exact implementation head. Adjust only when
the accepted toolchain changes and record the reason.

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

Also record:

```text
git status --short --branch
git diff --name-status <authorized-base>...HEAD
git diff --stat <authorized-base>...HEAD
git diff <authorized-base>...HEAD
```

The changed-file inventory must equal the exact accepted manifest.

## Rollback validation

In an isolated clone or worktree:

1. complete the primary journey;
2. run P1 reset and verify no eligible state or plaintext object remains;
3. apply a normal revert of the exact implementation commit or merge result;
4. reinstall from the reverted frozen lock;
5. run the full pre-P1 test and documentation baseline;
6. start the default synthetic Executive Product Shell; and
7. verify no P1 route, provider, dependency, runtime state, or grounded dynamic
   answer remains.

No destructive command may target the repository root, user profile, home
directory, or an unresolved variable. Verify the isolated runtime path before
cleanup.

## Exact-head review evidence

The implementation handoff must contain:

- repository, pull request, branch, exact base and head;
- commit list and complete 64-path manifest;
- dependency and lock diff;
- salvage provenance and rejected historical capabilities;
- requirement-to-evidence table with result for P1-001 through P1-030;
- exact commands, outputs, environment, dates, and limitations;
- browser and rollback evidence;
- security, sensitive-value, network, and prohibited-capability results;
- residual risks and unresolved findings;
- rollback instructions; and
- requested disposition.

The independent reviewer inspects the actual artifacts and returns the
disposition required by the canonical coordination policy. A changed head
invalidates the review evidence and Chief Architect merge decision.

## Acceptance rule

P1 implementation is acceptable only when every P1-001 through P1-030 row is
proved at the same exact head, every required command passes, browser and
rollback validation pass, no unexpected path or capability exists, and no
unresolved blocking finding remains.

Known limitations may remain only when they are explicit consequences of the
accepted synthetic P1 boundary and do not contradict a requirement.

## Stop and reconsideration triggers

Stop if validation requires real information, an external service, another
dependency, arbitrary input, a general parser, a model, durable promoted
content, authentication, deployment, a broader manifest, or a weakened
authority boundary. Record the exact failed requirement and request a Chief
Architect decision rather than changing the acceptance criterion.

## Related documents

- [P1 Pilot Plan](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Threat Model](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_THREAT_MODEL.md)
- [P1 Dependency and Salvage Assessment](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_DEPENDENCY_AND_SALVAGE_ASSESSMENT.md)
- [P1 Execution Handoff](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_EXECUTION_HANDOFF.md)
- [ADR 0018](adr/0018-p1-synthetic-organizational-learning-pilot-sequencing.md)
- [ADR 0019](adr/0019-governed-synthetic-evidence-promotion.md)
- [ADR 0020](adr/0020-executive-pilot-read-model-and-deterministic-retrieval.md)

## Review record

Prepared under `CA-2026-08-06-P1-PLANNING`. This validation contract remains
Proposed. It authorizes no test execution against historical code, no
implementation, no deployment, and no information use.
