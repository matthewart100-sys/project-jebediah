# P1 Synthetic Organizational Learning Pilot Threat Model

**Status:** Proposed; no implementation authority

**Planning base:**
`37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Decision owner:** Chief Architect

**Security owner for future implementation:** Maintainer accountable for the
repository candidate; no operational owner assigned

## Purpose

This threat model defines the security and privacy evidence required for the
synthetic P1 learning loop. It covers the future local implementation only. It
does not authorize code, a runtime, real information, deployment, or public
exposure.

P1 is deliberately synthetic, but it introduces meaningful security behavior:
encrypted custody, durable local metadata, browser-triggered mutation, human
disposition, knowledge eligibility, and evidence-bearing answers. Synthetic
content reduces consequence; it does not excuse unsafe boundaries that future
work could accidentally reuse.

## Security objectives

- Accept only the exact repository-generated fixture selected by a fixed
  identifier and digest.
- Preserve confidentiality and integrity of generated custody bytes at rest.
- Prevent custody, disposition, registry, projection, and retrieval identities
  from being forged or confused.
- Ensure no unapproved evidence can produce a grounded answer.
- Prevent cross-origin or malformed requests from mutating local state.
- Prevent raw PDF bytes, unapproved or ineligible source content, unbounded
  content, keys, tokens, paths, or raw exceptions from appearing in UI, logs,
  Git, or review evidence. Only the approved compiled projection and answer may
  appear after the registry/projection intersection succeeds.
- Preserve literal loopback and zero external-network behavior.
- Keep historical nonconforming services, models, memory, deployment, and
  authentication code outside P1.
- Fail closed and remain fully resettable and revertible.

## Assets

| Asset | Required protection |
| --- | --- |
| P1 fixture source and manifest | Integrity, version identity, obvious synthetic labeling |
| Generated PDF bytes | Exact identity, encrypted custody, bounded retention |
| Cryptographic master material, DEKs, nonces, salts, and audit keys | Confidentiality, non-reuse, no logging or repository storage |
| Authorization and custody records | Integrity, replay resistance, append-only evidence |
| SQLite metadata and audit chain | Integrity, transition validity, crash reconciliation |
| Human disposition | Candidate binding, immutability, policy scope |
| Registry metadata | Contract integrity, metadata-only boundary |
| Approved-evidence projection | Approved-only confidentiality and integrity |
| Retrieval result and answer | Eligibility, lineage, non-authority labels |
| Synchronizer action token | Unpredictability, process scope, no logging |
| Local runtime directory | Narrow scope, safe path, cleanup, no Git inclusion |
| Review and validation evidence | Exact-head provenance and sanitization |

## Trust boundaries

### Browser to loopback WSGI application

Browser requests are untrusted even on loopback. Method, route, query, content
type, length, encoding, fields, synchronizer token, and transition are
validated before any mutation. Host, origin, filename, question, identity, and
content are not accepted from the caller.

### Fixture generator to custody

Only the repository-owned generator may supply bytes. The custody boundary
recomputes the digest and validates fixed authorization, media type, size, PDF
envelope, and expected identity. Generator success does not bypass custody.

### Process to local durable storage

Filesystem and SQLite outcomes can be partial, reordered, corrupted, replaced,
or interrupted. Object paths are derived from validated opaque identities and
remain inside one verified runtime root. Encryption and metadata reconciliation
must not rely on file presence alone.

The runtime passphrase is entered interactively through `getpass` only. It must
not arrive through command arguments, environment variables, configuration,
HTML, logs, or committed material.

### Custody and manifest to promotion

Custody proves what bytes were accepted, not what they mean. The compiled
manifest maps only the exact digest to bounded synthetic evidence. Human
approval and policy eligibility remain separate required inputs.

### Promotion to registry and projection

The registry owns metadata integrity only. The projection holds content only
after registry success. Every read intersects the projection with its exact
approved, registered registry record. Partial or mismatched state cannot become
retrievable.

### Projection to retrieval and read model

Retrieval receives untrusted question, consumer, use, and time values from its
caller but accepts only the compiled P1 tuple. The dashboard consumes results;
it cannot manufacture grounding or promote evidence.

### Historical Git evidence to new implementation

Pull requests #59 and #60 are untrusted design and salvage input. No file,
dependency, test, or claim is accepted by historical presence. Every selected
idea is rewritten or ported narrowly and reviewed in the current exact diff.

## Threat inventory

| ID | Threat | Prevention and safe failure | Required detection/evidence | Residual risk |
| --- | --- | --- | --- | --- |
| T01 | Arbitrary or real document reaches custody | No upload/path/URL; fixed fixture route; exact digest, size, MIME, and PDF checks | Changed-byte, unknown-fixture, wrong-envelope tests; route inventory | A developer could later broaden the fixture boundary; review must catch it |
| T02 | Path traversal or object overwrite | Application-generated opaque IDs; canonical resolved runtime root; no caller path; exclusive create and conflict checks before replace | Traversal, separator, symlink/reparse, collision, and overwrite tests | Platform filesystem semantics vary |
| T03 | Plaintext custody leakage | AES-256-GCM; plaintext held only during bounded operation; no raw PDF or unapproved/unbounded content in SQLite, logs, or UI; only the eligible compiled projection may render; cleanup buffers/files where practical | Filesystem and database inspection; log and rendered-state capture | Process memory and local OS compromise remain out of scope |
| T04 | Custom, weak, or resource-amplified cryptography | Use exact `demo-p1-crypto-profile` version `1`; reviewed `cryptography` primitives; fixed bounded Argon2id; random DEKs/nonces; HKDF; authenticated AAD; strict decoders | Dependency review, exact-parameter, tamper, wrong-key, malformed-header, and oversized-parameter tests | Library defects and compromised host remain possible |
| T05 | Nonce, key, or salt reuse | Cryptographic RNG; per-object DEK and nonce; explicit uniqueness assertions where observable | Repeated-encryption tests and source review | RNG failure is inherited platform risk |
| T06 | Authorization forgery, self-signing, key collision, or replay | Separate ephemeral `SyntheticFixtureAuthority`; fingerprint-derived signer-key ID; append-only retained public keys; no persisted private key; versioned canonical payload; fixed policy/content/time; custody verification and reserve-first single use | Wrong signature/key/fingerprint/policy/time/content, old-key verification, replay, direct-custody, and crash tests | Synthetic authority is deliberately not a real identity or delegation authority |
| T07 | Crash creates false custody success | Reserve authority first; temporary same-filesystem object; fsync; exclusive publication; transaction ordering; reconciliation tombstones and destroys any published orphan rather than completing it | Failure injection at every durable boundary | Filesystem/SQLite cannot provide one distributed transaction |
| T08 | Corrupt or swapped object is accepted after restart | Verify envelope, AEAD, digest, byte count, object identity, and metadata before reconciliation | Corruption, truncation, swap, missing-object tests | Recovery is local test evidence, not operational readiness |
| T09 | Audit history is rewritten, reordered, or rolled back | Append-only schema controls, serialized write boundary, chained integrity verification | Mutation attempt, concurrent append, chain verification, and coordinated rollback limitation evidence | No external recovery ledger exists; a coordinated rollback of SQLite, objects, wrapped-key, and trust state can be undetectable; no rollback-resistance or non-repudiation claim |
| T10 | PDF content is parsed or active content executed | No parser, scan, OCR, render, subprocess, or embedded-object traversal; exact digest maps to compiled manifest | Import/dependency/source scan and changed-byte tests | PDF envelope validation does not establish general file safety |
| T11 | Manifest and PDF diverge | Generator bytes and manifest version tested together; exact digest key; no caller content | Stable digest and manifest mutation tests | Review error in the compiled synthetic fixture remains possible |
| T12 | Approval is self-asserted or forged | Fixed dashboard action creates append-only disposition bound to candidate and review policy; no boolean promotion API | Direct-promotion, wrong-token, wrong-policy, candidate-swap tests | Compiled reviewer identity does not authenticate a real human |
| T13 | Rejected/pending evidence is promoted | Promotion requires exact approved disposition and every eligibility predicate | Full state matrix and repository-absence assertions | Logic defect remains possible; independent review required |
| T14 | Registry content boundary is violated | Reuse ADR 0014 models; no content fields/arbitrary metadata; package tests | Model serialization inspection and forbidden-field tests | Explanations can still leak content if unconstrained; length/origin checks required |
| T15 | Registry/projection split or mismatch creates false availability | Publish projection only after identical registry success; intersect both repositories on every read; remove partial in-memory publication; return failure | Registry-only, projection-only, mismatch, lifecycle, and injected-failure tests | No durable atomicity is claimed |
| T16 | Projection bypasses approval | Constructor restricted to promotion service; immutable types; repository validates lineage and policy | Direct-construction and wrong-lineage tests | Python cannot enforce absolute encapsulation; package review remains necessary |
| T17 | Retrieval returns stale, deleted, wrong-use, or conflicting evidence | Exact question/consumer/use/time/lifecycle policy; zero-or-one cardinality; fail closed | Eligibility matrix and ambiguity tests | P1 does not prove generalized conflict handling |
| T18 | Dashboard fabricates a grounded answer | Grounded model requires domain result, source reference, and trace; rendering has no synthesis logic | Package dependency and view-model invariant tests | A future UI edit could regress; tests must remain canonical |
| T19 | Cross-site request mutates loopback state | Exact Host and Origin; shell-owned one-time 32-byte token; consume/rotate before domain call; fixed self forms; bounded exact body; Same-Origin CSP; no permissive CORS; reset rotates pilot epoch | Missing/wrong/stale/replayed/pre-reset token and cross-origin form tests | Browser or local malware with process access can still act |
| T20 | Request ambiguity or smuggling changes action | WSGI-owned length bounds; one content type; exact fields; duplicate rejection; no chunked custom server support | Length, encoding, duplicate, method, route, and header tests | `wsgiref` is a development preview, not production server |
| T21 | Token or sensitive input leaks | Never log token/body/content/digest/key/path; sanitized fixed errors; no echo | Log capture, response/header scan, sensitive-value scan | Debugger or compromised process can observe memory |
| T22 | Stored or reflected HTML injection | All dynamic text escaped; compiled safe labels; no raw HTML; CSP denies scripts/external content | Metacharacter and hostile-label rendering tests | Browser bugs remain outside project control |
| T23 | Denial of service or state race through repeated/concurrent actions | Small body cap, one fixture, bounded size/state, one-time token, exclusive runtime lock, one in-process state lock, idempotency, synchronous unthreaded behavior | Second-process, repetition, concurrent-call, duplicate, excessive-body, and state-size tests | Local operator can exhaust its own process; no service objective exists |
| T24 | Restart silently restores approval | Projection and disposition session state start empty; custody reconciliation does not promote | Restart-after-approval test | Users may find reapproval inconvenient; safety is preferred |
| T25 | Reset deletes wrong paths or leaves eligible state | Runtime-root validation; explicit object manifest; tombstone before wrapped-key/ciphertext destruction; retain content-free audit; post-reset verification; rotate token/epoch; no broad recursive target | Exact-path, failure, repeat, stale-form, and post-reset filesystem tests | OS deletion can fail; failure must remain visible |
| T26 | External network or service is contacted | No network clients or service dependencies; injected adapters only; runtime network denial | Import graph, dependency graph, monkeypatched socket denial, browser network inspection | OS/browser background traffic must be distinguished from app traffic |
| T27 | Historical PR code reintroduces excluded capability | No cherry-pick; exact salvage matrix; manifest and forbidden-path/import checks | Complete diff review against both historical heads | Similar-looking code can hide old flaws; review must inspect behavior |
| T28 | Real or sensitive data enters tests/docs/logs | Generated fixtures only; repository scan; sanitized browser evidence; no local path capture | Sensitive-pattern scan and manual diff review | Automated patterns cannot detect every contextual disclosure |
| T29 | Dependency compromise or incompatibility | One direct dependency, locked hashes, provenance/license/version review, frozen sync | Lock diff, clean install, vulnerability method and limitations | No scanner guarantees absence of unknown vulnerabilities |
| T30 | P1 is mistaken for production or truth | Persistent synthetic/local/no-action labels; no deploy artifacts; explicit limitations and component maturity | Rendered text, docs, component registry, route/dependency audit | Demonstration audiences can still overgeneralize; operator guidance required |

## Historical implementation hazards

### Pull request #59

PR #59 uses appropriate primitive families in parts of `crypto.py`, but its
repository and runtime are not accepted for wholesale reuse. Planning review
identified unsafe or incomplete transaction ordering, plaintext-bearing
metadata, unconstrained review transitions, incomplete audit verification and
deletion, runtime-owned signer behavior, synchronous fake inspection, and a
dashboard workflow that was not wired by the actual CLI.

P1 may port narrowly reviewed primitive wrappers and view ideas. It must design
custody transactions, state, promotion, and real application integration anew.

### Pull request #60

PR #60's custom SHA-256-derived XOR stream, HMAC construction, PBKDF2 wrapping,
caller-influenced object paths, raw-PDF excerpt promotion, boolean approval,
registry bypass, giant mixed provider, interaction service, model, memory,
Qdrant, authentication, and deployment surfaces are prohibited.

Useful design references are limited to receipt-policy checks, temporary-file
publication and reconciliation test ideas, insufficient/grounded vocabulary,
citations, and provenance expectations. No PR #60 cryptographic code is
salvageable.

## Required security tests

Security validation includes:

- authorization signature, policy, time, replay, and crash cases;
- cryptographic envelope, AAD, wrong key/passphrase, tamper, header, KDF bound,
  and nonce cases;
- path, collision, symlink/reparse, partial write, SQLite failure, corruption,
  audit, and restart cases;
- disposition forgery, swap, replay, conflict, and direct-promotion cases;
- registry/projection partial failure and constructor-boundary cases;
- retrieval lifecycle, consumer, use, question, ambiguity, and failure cases;
- route, method, length, content type, field, token, cross-origin, redirect,
  logging, escaping, and error cases;
- socket/network denial and forbidden import/dependency cases;
- sensitive-value and real-information repository scans; and
- reset and rollback rehearsal in a verified isolated directory.

The
[P1 Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
own the complete evidence mapping.

## Privacy boundary

P1 processes no real information. Synthetic actor labels, source IDs, and
statements must not resemble real people or organizations. Local runtime paths
and usernames are operationally sensitive and must not enter public evidence.

No analytics, telemetry, external fonts, external assets, crash reporting,
model prompt, export, or third-party API exists. Logs contain no content.

## Residual risk

- A compromised local OS or process can access unlocked plaintext and action
  state.
- `wsgiref` is suitable only for the literal loopback demonstration boundary.
- Compiled reviewer identity proves a workflow action, not real authentication
  or non-repudiation.
- Exact fixture mapping proves code behavior, not general PDF safety or factual
  truth.
- Session-only projection and local custody tests do not prove operational
  recovery.
- The local HMAC chain detects inconsistency and corruption but cannot detect a
  coordinated rollback of every local state artifact because P1 has no external
  recovery ledger.
- The closed synchronized-path component denylist cannot detect every sync or
  backup product; P1 therefore permits only generated synthetic information and
  treats operator path selection as a local-demo limitation, not a privacy
  guarantee.
- Dependency and automated scans cannot establish absence of unknown defects.
- A future contributor could overgeneralize P1 mechanisms unless exclusions
  remain prominent.

These risks are acceptable only for the exact synthetic, local, non-operational
P1 scope. Any real information or deployment requires a new threat model and
authority.

## Stop conditions

Stop if implementation would weaken an exact control, accept caller content,
use custom cryptography, parse a PDF, restore approval on restart, expose a
network, add a service/model/vector path, capture real data, or require a
broader dependency or manifest. Record the affected threat and request a Chief
Architect decision.

## Related documents

- [P1 Pilot Plan](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_PLAN.md)
- [P1 Validation Requirements](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_VALIDATION_REQUIREMENTS.md)
- [P1 Dependency and Salvage Assessment](P1_SYNTHETIC_ORGANIZATIONAL_LEARNING_PILOT_DEPENDENCY_AND_SALVAGE_ASSESSMENT.md)
- [Security Policy](../SECURITY.md)
- [ADR 0016](adr/0016-local-governed-pdf-intake-and-custody-boundary.md)
- [ADR 0019](adr/0019-governed-synthetic-evidence-promotion.md)
- [ADR 0020](adr/0020-executive-pilot-read-model-and-deterministic-retrieval.md)

## Review record

Prepared under `CA-2026-08-06-P1-PLANNING`. Independent security and
architecture review, Chief Architect acceptance, implementation authority, and
implementation evidence remain pending.
