# P1 Synthetic Organizational Learning Pilot Execution Handoff

**Status:** Proposed planning handoff; implementation authority none

**Planning base:**
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Planning authority:** `CA-2026-08-06-P1-PLANNING`

**Decision owner:** Chief Architect

## Purpose

This handoff makes the transition from accepted planning to a future P1
implementation mechanical and auditable. It fixes the branch sequence, gates,
review artifacts, implementation order, stop conditions, and exact decision
still required. It does not create a branch, change a dependency, run
historical code, or authorize implementation.

## Frozen proposed outcome

The future implementation proves one synthetic causal loop in the existing
Executive Product Shell:

```text
same GET Ask is insufficient
  -> one exact generated PDF enters encrypted local custody
  -> one explicit fixed human approval becomes eligible
  -> metadata registers and approved content projects separately
  -> the same GET Ask becomes deterministically grounded with full lineage
  -> reset removes eligibility and the same GET Ask is insufficient again
```

A separate fresh-application negative scenario rejects the candidate and keeps
the same Ask result insufficient. No real information, general PDF inspection,
model, Memory Service, vector store, service, deployment, or public exposure is
part of P1.

## Frozen identity and version constants

Implementation must use these separate identity/version fields; it may not
invent replacements:

| Contract | ID | Version |
| --- | --- | --- |
| Fixture | `demo-p1-synthetic-program-outcomes-fixture` | `1` |
| Generator | `demo-p1-pdf-generator` | `1` |
| Evidence manifest | `demo-p1-synthetic-program-outcomes-manifest` | `1` |
| Source | `demo-p1-synthetic-program-outcomes-source` | `1` |
| Transformation | `demo-p1-synthetic-fixture-projection` | `1` |
| Authorization policy | `demo-p1-synthetic-fixture-authorization-policy` | `1` |
| Review policy | `demo-p1-synthetic-evidence-review-policy` | `1` |
| Promotion policy | `demo-p1-synthetic-evidence-promotion-policy` | `1` |
| Retrieval policy | `demo-p1-exact-program-outcomes-retrieval-policy` | `1` |
| Retention policy | `demo-p1-synthetic-program-outcomes-retention-policy` | `1` |
| Cryptographic profile | `demo-p1-crypto-profile` | `1` |
| Synthetic reviewer | `demo-p1-synthetic-reviewer` | `1` |
| Synthetic signer | `demo-p1-fixture-authority` | `1` |
| Consumer | `demo-p1-executive-product-shell-consumer` | `1` |
| Intended use | `demo-p1-synthetic-question-answering-use` | `1` |

The existing question ID remains `insufficient-program-outcomes`. All other
rendered identities match `^demo-[a-z0-9-]+$`. The initial epoch is
`demo-p1-epoch-000001`. Receipt, receipt-verification event, submission,
custody object, admission, candidate, disposition, promotion decision, registry
object, projection, and trace use the exact `demo-p1-*` stems in the plan plus
durable monotonic six-digit epoch/event suffixes. No caller supplies an
identity.

Each ephemeral public key uses
`demo-p1-fixture-authority-key-<64-lowercase-hex-sha256-public-key>`.
Old public keys remain as content-free verification evidence for their
receipt/audit retention; private keys never persist.

The entry point is also frozen. `--port` alone starts the unchanged static
preview. Optional `--p1-runtime-directory <absolute-path>` activates P1 only
for a verified new-empty or exact-marker runtime directory with no `.git`
ancestor or symlink/reparse traversal and no case-insensitive path component
equal to `dropbox`, `google drive`, or `icloud drive`, or starting with
`onedrive`. The marker is
`.jebediah-p1-synthetic-runtime-v1`. The passphrase comes from `getpass` only;
there is no host, source, passphrase, key, environment, or configuration
option. Literal-loopback serving begins only after unlock and reconciliation.
The marker's exact UTF-8/LF content is
`{"kind":"jebediah-p1-synthetic-runtime","version":1}\n` and is created
exclusively only after path validation.

P1 acquires an OS advisory lock on `.jebediah-p1-runtime.lock` before unlock and
refuses a second process or unsupported host lock. One in-process `RLock`
protects actions, epochs, resets, and read snapshots. SQLite uses foreign keys,
`journal_mode=DELETE`, `synchronous=FULL`, `busy_timeout=0`, parameterized SQL,
and `BEGIN IMMEDIATE`; every state transition and audit event share one
transaction. There is no background writer, scheduler, watcher, threaded
server, or second connection.

## Current authority matrix

| Activity | State after this planning pull request opens |
| --- | --- |
| Read canonical repository and historical PRs #59/#60 | Authorized for bounded planning evidence |
| Edit and validate documentation on the planning branch | Authorized |
| Accept ADRs 0018-0020 | Chief Architect decision pending |
| Merge the planning pull request | Separate Chief Architect merge decision pending |
| Create or edit implementation code/tests/dependencies/lock | Prohibited |
| Run or deploy historical PR #59/#60 code | Prohibited |
| Use real organizational information | Prohibited |
| Create the implementation branch | Wait for the exact authorization record and status activation to merge |
| Implement, deploy, expose, or operate P1 | Prohibited |

Planning acceptance or merge does not silently change any prohibited row.

## Architecture decisions that must become canonical

The implementation base must contain all three accepted decisions:

1. [ADR 0018](adr/0018-p1-synthetic-organizational-learning-pilot-sequencing.md)
   grants only the bounded vertical-slice sequencing exception.
2. [ADR 0019](adr/0019-governed-synthetic-evidence-promotion.md) defines exact
   fixture evidence, disposition, metadata registration, and the separate
   process-local projection.
3. [ADR 0020](adr/0020-executive-pilot-read-model-and-deterministic-retrieval.md)
   defines read-time registry/projection intersection, the unchanged GET Ask,
   four fixed mutations, and the additive P1 shell composition.

ADR 0017 is reserved by open pull request #63 and is not canonical at this
planning base. P1 neither assumes its acceptance nor depends on its B1
activation proposal. Until a later canonical change, ADR 0005 and the current
Project Coordination Protocol govern review. If pull request #63 merges first,
the then-canonical review policy applies without weakening actual-artifact,
independence, blocker, changed-head, or Chief Architect gates.

## Pull-request and branch sequence

### 1. Planning and architecture pull request

- Branch: `docs/p1-synthetic-learning-pilot-planning`
- Base: `37dd437617ed731340e9fd3da6cab0b1c49f7b4a`
- Allowed content: Markdown planning and canonical reconciliation only
- Requested disposition: independent Work Mode architecture review of the exact
  head under current canonical ADR 0005
- Required packet: authorization, three ADRs, plan, validation contract, threat
  model, dependency/salvage assessment, this handoff, canonical reconciliation,
  actual diff, validation output, limitations, and a completed
  [Architecture Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md)
- Result if merged: canonical implementation-ready plan; implementation
  authority remains none

If review changes any decision or status record, the changed exact head receives
a fresh review before the Chief Architect merge decision.

### 2. Explicit implementation authorization

After the planning merge, the Chief Architect must issue a durable directive
that names:

- the exact canonical planning merge commit;
- accepted ADRs 0018-0020;
- the exact 64-path manifest in the P1 plan;
- the Implementation Engineer and independent-review gate;
- generated synthetic information and local test execution as the only data
  and runtime scope;
- the exclusions and stop conditions;
- changed-head invalidation; and
- the requirement to stop before merge.

The exact requested authorization text is in the
[P1 Pilot Plan](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md#exact-implementation-authorization-requested-after-planning-merge).

### 3. Implementation-authorization pull request

- Branch: `docs/p1-synthetic-learning-pilot-activation`
- Base: the exact canonical planning merge named by the directive
- Exact paths:
  `docs/governance/CHIEF_ARCHITECT_P1_IMPLEMENTATION_AUTHORIZATION.md`,
  `CURRENT_SPRINT.md`, `PROJECT_STATUS.md`, and `CHANGELOG.md`
- Content: record the directive and activate only the already accepted exact
  P1 implementation scope
- Review: required independent exact-head authority/policy review and separate
  Chief Architect merge decision
- Result: canonical implementation authority; still no application,
  dependency, test, runtime, or deployment change

Implementation cannot begin from the conversational directive or the open
activation branch. The four-path activation record must merge to canonical
`main` first.

### 4. Implementation pull request

- Branch: `feat/p1-synthetic-organizational-learning-pilot`
- Base: the exact canonical implementation-activation merge
- Scope: exactly the plan's 64-path manifest
- Publication: one non-draft pull request; no partial subsystem merge
- Result: a repository implementation candidate only; no deployment or real
  use

The branch is created only after the authority/base/worktree/baseline gate
passes. An unexpected path or capability stops the work before publication.

### 5. Controlled merge and closeout

The implementation exact head requires independent actual-artifact review,
blocking-finding resolution, fresh review after material changes, and a
separate Chief Architect merge decision. After controlled merge and post-merge
verification, use a small documentation-only branch:
`docs/p1-synthetic-learning-pilot-closeout`.

Closeout records merged evidence and terminal P1 status only. It does not
activate B2 general inspection or any later milestone.

## Implementation checkpoint order

One implementation pull request uses these non-skippable checkpoints:

| Checkpoint | Deliverable | Gate before continuing |
| --- | --- | --- |
| 0 | Exact authority, base, clean isolated worktree, frozen baseline | Every value matches the authorization |
| 1 | Receipt verification, cryptography 50.x, encrypted custody, audit, restart/reset | Custody tests and dependency review pass; no inspection or UI code |
| 2 | Exact digest manifest, candidate, disposition, registry metadata, projection | Eligibility, idempotency, split-state, and package-boundary tests pass |
| 3 | Exact-policy retrieval and read-model assembly | Registry/projection intersection and all denial paths pass |
| 4 | Additive P1 shell composition and four fixed mutations | Default shell compatibility and HTTP/security tests pass |
| 5 | Causal WSGI/browser journeys, restart, rollback, accessibility, negative capabilities | Every P1-001 through P1-030 row has exact-head evidence |
| 6 | Complete diff and review publication | Manifest is exact; full validation is recorded |

The commits may follow the plan's logical commit strategy, but commit boundaries
do not grant authority to merge an incomplete subsystem.

## Baseline and implementation commands

Checkpoint 0 records at minimum:

```text
git rev-parse HEAD
git status --short --branch
uv lock --check
uv sync --frozen
uv run --frozen pytest
uv run --frozen python -m compileall -q apps src services tests
python scripts/validate_docs.py
git diff --check <authorized-base>...HEAD
```

The full targeted and final commands are binding in the
[P1 Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md).
Command, environment, exact commit, result, and limitation are recorded. A
summary-only green status is not evidence.

HTTP outcomes are fixed for implementation and tests: `303` after success;
`400` for malformed length, encoding, fields, or query; `403` for Host, Origin,
or token failure; `404` for an unknown route; `405` plus `Allow` for a wrong
method; `409` for an invalid or conflicting transition; `413` for a declared
body above 4096 bytes; `415` for a wrong content type; `503` for sanitized owned
repository/custody unavailability; and `500` only for unexpected fail-closed
rendering. No error mutates state or echoes input.

The only POST field is `p1_action_token`, exactly 43 unpadded base64url ASCII
characters encoding 32 CSPRNG bytes. The shell owns it. Under the action lock,
a boundary-valid request consumes and rotates it before the domain call even if
the domain result fails; invalid boundary requests do not mutate domain state.
Neither coordinator nor briefing receives token bytes.

The implementation also has no retention choice left open: use
`demo-p1-synthetic-program-outcomes-retention-policy` at version `1`, a 900-second maximum receipt
lifetime, exact PDF admission capped at 65,536 bytes, 30 days from receipt for
pending/processing/accepted/ready/approved ciphertext, 7 days for
rejected/failure ciphertext with immediate access denial, and 365 days for
safe audit/tombstones. Deadlines never extend; P1 has no legal hold, backup, or
restore. Integrity failures still enter a held, ineligible state.

Reconciliation never completes a published orphan. If receipt reservation and
encrypted-object publication exist without the committed metadata-and-audit
transaction, record unknown outcome, tombstone and destroy the orphan, keep the
receipt consumed, and require a new submission. Reset runs under one
coordinator lock in this order: deny retrieval/mark resetting; commit custody
tombstone plus audit; destroy and verify wrapped-key/ciphertext removal; discard
the process-local disposition/registry/projection epoch; rotate token and pilot
epoch. Cleanup failure is visible `cleanup_failed`, never pristine success, and
may be retried.

## Historical salvage controls

Pull requests #59 and #60 are read-only historical inputs. Do not cherry-pick,
merge, run, deploy, or copy either branch wholesale. The
[Dependency and Salvage Assessment](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_DEPENDENCY_AND_SALVAGE_ASSESSMENT.md)
is the allowlist and rejection record for every selected concept.

Implementation must record each salvaged concept by historical path/symbol,
new path/symbol, adaptation, tests, and reviewer. Similar code without that
provenance is newly implemented code, not implicitly accepted salvage.

## Review strategy

### Planning review packet

The independent architecture reviewer must inspect:

- the actual complete documentation diff;
- the exact contradiction and bounded sequencing exception in ADR 0018;
- reconciliation against ADRs 0011-0016 and the Phase 3B decision;
- the one-fixture/no-parser boundary;
- registry metadata versus content projection ownership;
- read-time registry/projection intersection;
- four POST mutation routes and pure GET Ask behavior;
- the exact implementation manifest, dependency line, tests, risks, rollback,
  and stop conditions; and
- whether canonical files accurately say planning only and implementation none.

The reviewer returns the completed
[Architecture Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md) against the
exact planning head through the reviewer mechanism required by the canonical
coordination policy. On this planning base that mechanism is Work Mode. If a
reviewed ADR 0005 successor becomes canonical first, its normal-chat reviewer
mechanism applies to the then-current exact head instead.

### Implementation review packet

The independent implementation reviewer receives the actual exact-head diff,
all commits, the 64-path inventory, full command output, requirement evidence,
browser transcript/screenshots, dependency and lock diff, salvage mapping,
sensitive-value/network/forbidden-capability results, restart and rollback
evidence, residual risks, and requested disposition.

Any changed implementation head invalidates the review and any merge decision
based on it.

## Stop conditions

Stop and request a Chief Architect decision if implementation would require:

- a changed canonical base or a path outside the exact manifest;
- a second, real, external, or caller-controlled document;
- parsing, extracting, scanning, OCR, native execution, or a worker container;
- durable promoted content or approval restoration after restart;
- free-form questions, a model, Memory Service, Qdrant, embeddings, or semantic
  retrieval;
- authentication, multi-user state, a service/API, non-loopback access,
  deployment, or public exposure;
- an additional dependency or changed component/information/authority boundary;
- a weakened security or validation requirement; or
- a review-policy conflict that cannot be resolved from canonical repository
  state.

Report the exact affected requirement and the smallest required decision. Do
not silently reinterpret P1.

## Rollback handoff

Before merge, rollback means abandon the implementation branch and remove only
verified isolated generated state. After an approved implementation merge but
before any separately authorized deployment, use a reviewed normal Git revert,
run the scoped P1 reset, verify no eligible/content-bearing state remains, and
prove the default static Executive Product Shell still works from the reverted
frozen lock.

P1 has no external recovery ledger. Its content-free HMAC audit evidence can
detect local inconsistency but not a coordinated rollback of every local state
artifact. That residual is accepted only for the synthetic local pilot.

## Related documents

- [P1 Planning Authorization](governance/CHIEF_ARCHITECT_P1_PLANNING_AUTHORIZATION.md)
- [P1 Pilot Plan](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
- [P1 Threat Model](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_THREAT_MODEL.md)
- [P1 Dependency and Salvage Assessment](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_DEPENDENCY_AND_SALVAGE_ASSESSMENT.md)
- [Phase 3B Reconciliation Decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
- [Architecture Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md)

## Review record

Prepared under `CA-2026-08-06-P1-PLANNING`. Independent architecture review,
Chief Architect acceptance, planning merge approval, merge, and a separate P1
implementation authorization remain pending. This handoff performs none of
those decisions.
