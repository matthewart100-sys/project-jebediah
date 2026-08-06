# ADR 0020: Executive Pilot Read Model and Deterministic Retrieval

**Status:** Proposed

**Decision level:** System

**Date:** 2026-08-06

**Decision owner:** Chief Architect

**Required reviewers:** Independent architecture reviewer under the canonical
coordination policy, then Chief Architect final decision

## Decision summary

For P1 only, connect the existing Executive Product Shell to a local pilot
coordinator through explicit read and action protocols. The coordinator serves
one evidence-bearing dynamic read model, accepts four fixed synthetic workflow
mutations, and retrieves only active registry/projection pairs approved for one allowlisted
question, consumer, and use. No free-form query, model, vector store, service,
authentication, external network, or deployment is introduced.

## Context

[ADR 0012](0012-executive-organizational-intelligence-interface-boundary.md)
selects an evidence-bearing organizational-intelligence read model and keeps
presentation separate from ingestion, verification, derivation, and action.
[ADR 0015](0015-executive-product-shell-and-local-preview-boundary.md)
implements the Executive Product Shell over immutable compiled fixtures and
explicitly defers any live adapter, request body, mutation, persistence, or
runtime integration.

P1 must demonstrate a causal change in the existing dashboard. A static fixture
cannot prove that submission and approval changed the answer. Directly adding
promotion and retrieval logic to rendering would violate the accepted
presentation boundary. Reusing the historical interaction service, Memory
Service, Qdrant, or model path would exceed P1.

### Verified facts

- The current shell binds to literal `127.0.0.1`, accepts allowlisted GET and
  HEAD routes, rejects query strings and request bodies, escapes dynamic text,
  and uses no JavaScript or external asset.
- `create_app` resolves one immutable briefing at application construction.
- The existing Ask surface has three allowlisted preset question identities,
  including `insufficient-program-outcomes`.
- `AskResponse` distinguishes grounded, insufficient, and failed states and
  requires source references for grounded answers.
- Historical pull request #59 adds bounded POST handling and a workspace
  service, but it also accepts file uploads and connects inspection/review work
  outside P1.
- Historical pull request #60 includes a dynamic governed provider, local
  deterministic retrieval, services, authentication, models, Qdrant, and
  deployment. Its broad implementation is nonconforming and not accepted.

### Reported facts

- The intended user needs to ask the same question before and after approval
  and see why the answer changed.

### Working assumptions

- Reusing the existing `insufficient-program-outcomes` preset avoids a new
  free-form input contract.
- Fixed local actions and a shell-owned one-time synchronizer token can support the
  demonstration without identity or session persistence.
- Exact-policy retrieval by question identity is sufficient for one P1 record
  and is more honest than pretending to provide general semantic search.

### Open questions

- General natural-language querying, generated assistance, multiple users,
  access control, durable read models, and service transport remain unresolved.
- Representative usability and accessibility still require browser validation
  after implementation.

These questions remain outside P1.

## Scope

- P1 coordinator, read-provider, action-handler, and presentation dependency
  direction.
- One allowlisted question and four fixed workflow mutations.
- Approved-only deterministic retrieval and answer assembly.
- Evidence-trace view-model additions.
- Request, rendering, logging, state, failure, reset, and loopback boundaries.
- Compatibility with the existing shell and compiled demonstration provider.

## Non-goals

- Accepting this Proposed decision or authorizing implementation.
- Free-form prompts, arbitrary questions, conversational history, or a model.
- Semantic embeddings, Memory Service, Qdrant, Ollama, or C2.
- File upload, arbitrary PDF input, parser, scanner, OCR, or external source.
- Authentication, authorization, multi-user workspace, session account, or C0.
- Action authority, organizational decision recording, workflow execution, or
  external side effects.
- Network deployment, TLS, container, service, API, public exposure, or O1.
- Replacing the Executive Product Shell.

## Decision drivers

- Keep the existing dashboard as the primary interface.
- Prove the answer changes only after approval.
- Make evidence and lineage visible in the answer itself.
- Keep presentation free from custody, approval, promotion, and retrieval
  decisions.
- Preserve deterministic operation without external dependencies.
- Maintain keyboard, no-JavaScript, loopback, safe-rendering, and visible-state
  properties.
- Fail closed and keep rollback complete.

## Considered alternatives

### Keep static fixtures and swap scenarios manually

A before and after scenario could imitate the result, but it would not prove a
single workflow or causal approval gate. It would remain a scripted
presentation.

**Disposition:** Rejected.

### Add promotion and retrieval directly to rendering or WSGI routes

This is mechanically small but gives presentation code knowledge and policy
authority, makes testing boundaries unclear, and violates ADR 0012.

**Disposition:** Rejected.

### Restore the historical interaction service and governed provider

This provides broad runtime behavior but introduces authentication, external
services, model paths, memory/Qdrant projection, environment configuration,
deployment artifacts, and operational claims excluded from P1.

**Disposition:** Rejected.

### Add a bounded in-process coordinator behind protocols

The shell delegates fixed actions and reads one validated dynamic briefing.
The coordinator composes custody, disposition, promotion, and retrieval domain
boundaries without giving rendering those responsibilities.

**Disposition:** Selected.

## Decision

### Composition boundary

Add one `P1PilotCoordinator` application-domain composition. It is a
process-local reference composition, not an independently operated service or a
new Operational component.

The coordinator owns sequencing only:

```text
fixed action -> domain boundary -> state transition -> rebuilt read model
```

It does not implement cryptography, custody persistence, registry invariants,
promotion eligibility, retrieval eligibility, or HTML rendering. Those remain
in their owned modules.

The Executive Product Shell depends on two protocols:

- `PilotBriefingProvider.briefing()` returns a newly assembled immutable
  `ExecutiveBriefing` for each request; and
- `PilotActionHandler.perform(action)` applies one allowlisted domain action
  enum and returns a safe fixed redirect result.

The shell does not import a durable repository, registry adapter, promotion
implementation, retrieval implementation, or fixture generator directly.

The existing CLI with required `--port` alone retains the static preview.
Optional `--p1-runtime-directory <absolute-path>` is the only P1 selector. It
accepts an operational runtime root, never a source path. The path must be a
new empty directory or carry the exact P1 marker, have no ancestor containing
`.git`, contain no symlink/reparse traversal, and have no case-insensitive path
component equal to `dropbox`, `google drive`, or `icloud drive`, or starting
with `onedrive`. P1 prompts through `getpass`
and serves only after unlock and startup reconciliation succeed. There is no
host, source, passphrase, key, environment, or configuration option; binding
remains literal `127.0.0.1`.

The marker is `.jebediah-p1-synthetic-runtime-v1` with exact UTF-8/LF content
`{"kind":"jebediah-p1-synthetic-runtime","version":1}\n`. Marker creation is
exclusive and occurs only after path validation.

### Allowlisted question

P1 uses exactly the existing preset:

```text
question_id: insufficient-program-outcomes
question: What are the measured synthetic program outcomes?
consumer_id: demo-p1-executive-product-shell-consumer
intended_use: demo-p1-synthetic-question-answering-use
```

The user cannot modify the question text or identity. The same route and exact
question are used before and after approval.

### Fixed actions

Ask remains the existing pure-read
`GET /ask/insufficient-program-outcomes`. The shell adds exactly four POST
mutations:

| Route | Meaning | Success redirect |
| --- | --- | --- |
| `/pilot/submit/program-outcomes` | Generate and submit the exact P1 PDF fixture to custody | `/workspace` |
| `/pilot/review/program-outcomes/approve` | Record the fixed approval disposition and invoke promotion | `/ask/insufficient-program-outcomes` |
| `/pilot/review/program-outcomes/reject` | Record the fixed rejection disposition without promotion | `/ask/insufficient-program-outcomes` |
| `/pilot/reset` | Remove only generated P1 state and return to the initial insufficient state | `/ask/insufficient-program-outcomes` |

There is no file picker, filename, path, paste field, free-form prompt, note,
review rationale, question, consumer, use, or arbitrary identifier in the
request. Every value other than the shell-owned action token is compiled and
selected by the route.

POST bodies use `application/x-www-form-urlencoded`, are bounded to 4096 bytes,
contain exactly one field named `p1_action_token`, and reject duplicate or
unknown fields. Query strings, non-UTF-8 values, wrong content types, missing,
negative, nonnumeric, or over-limit declared lengths, observable short bodies,
trailing or unknown form data, `Transfer-Encoding`, and unsupported methods
fail without mutation or input echo.

For mutation requests, `Host` is exactly `127.0.0.1:<selected-port>` and
`Origin` is exactly `http://127.0.0.1:<selected-port>`. Missing or different
values fail. P1 uses no cookies and emits no permissive CORS headers. Mutation
responses use `Connection: close`; a surplus octet sequence cannot become a
second request on that development-server connection.

The Executive Shell application—not the coordinator—generates a 32-byte CSPRNG
token encoded as 43 unpadded base64url ASCII characters, parses the body,
validates the token in constant time, consumes and rotates it before the domain
call regardless of that call's outcome, and passes only an allowlisted action
enum to `perform`. The renderer receives a shell-owned optional form context;
the token never enters the briefing, domain model, lineage, or coordinator.
The application renders it only in fixed local forms. The
Content Security Policy changes from `form-action 'none'` to `form-action
'self'` only in P1 composition. Responses use Post/Redirect/Get to fixed local
locations. The token is temporary, is not a user session or credential, and is
never logged.

HTTP outcomes are fixed: `303` after success; `400` for malformed length,
encoding, fields, or query; `403` for Host, Origin, or token failure; `404` for
an unknown route; `405` plus `Allow` for a wrong method; `409` for an invalid or
conflicting transition; `413` for a declared body above 4096 bytes; `415` for a
wrong content type; `503` for sanitized owned repository or custody
unavailability; and `500` only for unexpected fail-closed rendering. No error
mutates state or echoes input.

Successful reset also rotates the process-local pilot epoch. A
pre-reset form is therefore stale even if its request is delayed until after
cleanup.

### Read-model assembly

The coordinator assembles a fresh immutable briefing for every request from:

- existing compiled synthetic briefing items unaffected by P1;
- sanitized custody, disposition, registry, and projection metadata;
- one current `AskResponse`; and
- append-only synthetic activity entries.

The briefing keeps `scenario_id=synthetic-nonprofit-demo-v1`; all existing
items, the other two Ask presets, coverage inputs, workspace records, and
activities remain value-identical. P1 replaces only the
`insufficient-program-outcomes` response and appends P1 records/events in
deterministic identity order. The briefing ID uses
`demo-p1-briefing-<six-digit-epoch>-<six-digit-snapshot>` and summary counts are
re-derived through the existing model contract.

The exact P1 workspace projection is:

| State | Appended safe records |
| --- | --- |
| Pristine | No P1 document, review, lineage, or knowledge record |
| Submitted/pending | `DOCUMENT/ACCEPTED` plus `REVIEW/REVIEW_PENDING` |
| Rejected | `DOCUMENT/ACCEPTED` plus `REVIEW/REVIEW_REJECTED`; no lineage or knowledge record |
| Approved/eligible | `DOCUMENT/ACCEPTED`, `REVIEW/REVIEW_APPROVED`, `LINEAGE/READY`, and `KNOWLEDGE_OBJECT/ELIGIBLE` |
| Approved/promotion failed | `DOCUMENT/ACCEPTED`, `REVIEW/REVIEW_APPROVED`, `LINEAGE/PROCESSING_FAILED`, and `KNOWLEDGE_OBJECT/UNAVAILABLE` |
| Integrity held | `DOCUMENT/HELD`, `REVIEW/HELD`, and no eligible knowledge record |
| Reset completed | No content-bearing P1 record; one content-free reset activity may identify the sealed epoch as `DELETED` |

Record IDs use `demo-p1-workspace-{document|review|lineage|knowledge}-<epoch>`.
Activities use only these compiled mappings:

| Event | Kind / result | Summary / actor label |
| --- | --- | --- |
| Custody committed | `EVIDENCE_ADDED` / `ACCEPTED` | `Exact generated P1 fixture entered encrypted custody.` / `P1 synthetic fixture authority` |
| Approval | `REVIEW_STATE_CHANGED` / `REVIEW_APPROVED` | `P1 synthetic evidence received the fixed approved disposition.` / `Local synthetic reviewer` |
| Rejection | `REVIEW_STATE_CHANGED` / `REVIEW_REJECTED` | `P1 synthetic evidence received the fixed rejected disposition.` / `Local synthetic reviewer` |
| Lineage ready | `LINEAGE_RECORDED` / `READY` | `P1 synthetic evidence lineage became ready.` / `P1 synthetic pilot` |
| Promotion failed | `LINEAGE_RECORDED` / `PROCESSING_FAILED` | `P1 synthetic evidence promotion failed closed.` / `P1 synthetic pilot` |
| Knowledge eligible | `KNOWLEDGE_STATUS_CHANGED` / `ELIGIBLE` | `Approved P1 synthetic evidence became eligible for the exact preset.` / `P1 synthetic pilot` |
| Reset complete | `KNOWLEDGE_STATUS_CHANGED` / `DELETED` | `P1 synthetic pilot epoch reset completed.` / `P1 synthetic pilot` |

No PDF text or answer statement is copied into a workspace record or activity.
Eligibility is true only for the approved `KNOWLEDGE_OBJECT/ELIGIBLE` record and
never causes the shell itself to perform retrieval.

The read model never exposes source bytes, encrypted content, keys, action
tokens, local paths, exception text, or repository internals.

`AskResponse` gains an optional tuple of immutable `EvidenceTrace` records.
Existing fixtures remain compatible through an empty default. A grounded P1
answer requires at least one trace; insufficient and failed answers require no
trace.

Each trace contains safe identities for fixture, source, receipt, signer-key
fingerprint, authorization policy, receipt verification event, submission,
custody, admission, digest, candidate, disposition, reviewer, review policy,
promotion decision, registry object, projection, retrieval policy, and
transformation, plus verification, approval, and assembly times and a bounded
excerpt. It contains no filesystem locator or source bytes.

`EvidenceTrace` version `1` has these exact immutable fields:

```text
trace_id
fixture_id, fixture_version, manifest_id, manifest_version
source_id, source_observed_at, page_reference
content_sha256, content_length, media_type
receipt_id, authority_id, signer_key_id
authorization_policy_id, authorization_policy_version, receipt_verified_at
submission_id, custody_object_id, admission_id
candidate_id, disposition_id, reviewer_id
review_policy_id, review_policy_version, approved_at
promotion_decision_id, promotion_policy_id, promotion_policy_version
registry_object_id, projection_id, projection_version
retrieval_policy_id, retrieval_policy_version, eligibility_evaluated_at
transformation_id, transformation_version, assembled_at
question_id, consumer_id, intended_use_id
excerpt, limitation
```

Every identity/value must equal the corresponding receipt, custody, candidate,
disposition, registry, projection, and policy record. The page is integer `1`;
the digest is 64 lowercase hex; all times are aware UTC; `excerpt` and
`limitation` are the exact compiled strings in the P1 plan. The renderer labels
these fields but never reconstructs lineage from unrelated state.

### Deterministic retrieval

Retrieval accepts only the exact question, consumer, use, and evaluation time.
It asks the approved-evidence projection repository for records eligible under
that tuple, then calls
`KnowledgeRegistryRepository.find(projection.registry_object_id)` for each
candidate. P1 has at most one eligible intersection.

A projection is retrievable only when its registry record exists and the two
records match exactly on deterministic identity, digest, lineage, provenance,
consumer, use, and policy. The registry record must also retain
`HumanReviewState.APPROVED`, `KnowledgeLifecycleState.REGISTERED`, and current temporal
eligibility. Missing or mismatched state, either repository failing, a
Registry-only record, or a projection-only record fails closed with no content
emission.

The result rules are:

- pristine, submitted/pending, rejected, expired, reset, tombstoned, or normally
  ineligible exact evidence: `AskState.INSUFFICIENT`, no statement, references,
  or evidence trace;
- exactly one eligible registry/projection pair: `AskState.GROUNDED`, a
  deterministic template statement, one safe source reference, and one
  complete trace;
- more than one pair, repository failure, registry/projection split or
  mismatch, unknown policy/lifecycle, integrity-held custody, promotion partial
  failure, or wrong question/consumer/use at the domain boundary:
  `AskState.FAILED` and a visible unavailable briefing state with no statement,
  reference, or trace.

Retrieval performs no fuzzy, semantic, vector, probabilistic, or model ranking.
Successful matching does not verify truth. The answer states its synthetic
scope and cannot recommend or execute action.

### Workflow states

Ask does not mutate state. The user-visible domain sequence is:

```text
pristine
  -> submitted_in_custody
  -> approved_and_projected | rejected
  -> reset_to_pristine
```

Invalid transitions fail closed. Approval before custody, approval after
rejection, duplicate divergent disposition, retrieval before projection, and
mutation after reset using an old token cannot create a grounded answer.

### Logging and failure

Logs contain only sanitized method, allowlisted route identity, status,
duration, transition reason code, and opaque correlation identity. They contain
no question text, statement, excerpt, PDF bytes, digest, token, path, key,
reviewer detail, or raw exception.

Domain failure returns a calm fixed error or unavailable state. It never
renders partial state as approved or grounded. A redirect occurs only after the
domain operation reports success.

### Default and rollback behavior

The existing `SyntheticBriefingProvider` remains the default when no P1
coordinator is supplied. Ordinary Phase 3A preview commands therefore preserve
current behavior unless the separately documented P1 entry point selects the
pilot composition.

Rollback removes the P1 composition and routes, clears generated runtime state,
and restores the exact current shell behavior without a data migration.

## Consequences

### Positive

- The existing dashboard proves the complete loop without replacement.
- The same question and route visibly change only because eligibility changes.
- Presentation remains a consumer of domain-owned decisions.
- Fixed actions avoid arbitrary file and prompt attack surfaces.
- Exact retrieval is deterministic, transparent, and easy to falsify in tests.
- Existing static preview behavior remains available.

### Negative

- The WSGI application gains bounded mutation and request-body handling.
- Dynamic briefing assembly changes a previously immutable app lifecycle.
- A shell-owned one-time action token and form rendering path add security-sensitive
  code.
- The fixed question and fixture do not demonstrate general query usefulness.

### Neutral

- No JavaScript, frontend framework, API service, or external dependency is
  selected for the shell.
- The pilot remains local and synthetic, not Operational.
- Human action remains limited to an in-process synthetic disposition.

## Data and provenance impact

The dynamic briefing, activity records, retrieval result, and answer are
temporary derived presentation data. The approved-evidence projection and
registry record retain their categories from ADR 0019. The action token is
temporary security state. No user preference, session account, prompt history,
or analytics record is created.

## Security and privacy impact

P1 preserves literal loopback, no external assets, escaping, restrictive
headers, safe errors, and sanitized logs. It adds fixed POST forms protected by
a synchronizer token, body and field bounds, fixed redirects, and no
caller-controlled content. The unauthenticated preview must not bind to a
non-loopback address or contain real information.

The threat model owns CSRF, request smuggling/body ambiguity, replay,
transition abuse, stale briefing, evidence leakage, forged grounding, denial of
service, and historical-code boundary risks.

## Operations and recovery impact

No deployment or service operation is approved. The process may expose a local
health-independent preview only. Reset and clean restart are the only P1
recovery mechanisms. No availability, backup, restore, multi-process
consistency, or operational support claim is made.

## Compatibility and migration

Existing GET/HEAD routes, models, compiled fixtures, and default provider remain
compatible. `EvidenceTrace` is additive with an empty default. P1-specific POST
routes are new and fixed. No public API or live consumer exists.

The application factory must retrieve the active briefing per request in P1
composition while preserving current fail-closed rendering and static-provider
tests.

## Validation

Implementation evidence must prove:

- the exact same question is insufficient initially and after submission;
- rejection keeps it insufficient;
- approval creates one grounded answer with complete trace;
- resetting restores the initial state;
- no grounded answer can be produced by invalid transition, direct route call,
  missing token, stale token, wrong consumer/use, or repository failure;
- GET/HEAD and existing synthetic fixture behavior remain compatible;
- POST method, content type, length, field, token, route, redirect, and logging
  boundaries fail closed;
- every dynamic string remains escaped and keyboard workflow remains usable;
- no file input, free-form question, network call, model, memory, Qdrant,
  authentication, deployment, or external information path exists; and
- a local browser can complete the entire loop through the dashboard.

Reconsider if P1 needs arbitrary questions, more than one fixture or consumer,
JavaScript, authentication, an external service, durable answer state, a model,
semantic retrieval, or deployment.

## Follow-up work

- Accept ADRs 0018 and 0019 with this decision before implementation.
- Implement only under the exact accepted P1 plan and later implementation
  authorization.
- Use post-P1 evidence to decide whether a generalized D1 architecture is
  justified.

## Related documents

- [ADR 0012](0012-executive-organizational-intelligence-interface-boundary.md)
- [ADR 0015](0015-executive-product-shell-and-local-preview-boundary.md)
- [ADR 0018](0018-p1-synthetic-organizational-learning-pilot-sequencing.md)
- [ADR 0019](0019-governed-synthetic-evidence-promotion.md)
- [P1 Pilot Implementation Plan](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Validation Requirements](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
- [P1 Threat Model](../P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_THREAT_MODEL.md)

## Supersession

**Supersedes:** None

**Superseded by:** None

This decision refines ADRs 0012 and 0015 for the exact P1 composition. It does
not replace their general presentation and authority boundaries.

## Review record

The Chief Architect authorized preparation through
`CA-2026-08-06-P1-PLANNING`. Independent architecture review, Chief Architect
acceptance, status activation, merge approval, and merge remain pending. This
Proposed decision grants no implementation, deployment, or real-information
authority.
