# Knowledge Manager 1.0 Phase 2 Document Inspection Plan

**Status:** Accepted architecture and validation baseline

**Milestone:** Knowledge Manager 1.0

**Phase:** 2 - Document Inspection Pipeline

**Date:** 2026-08-05

**Decision owner:** Chief Architect

**Architecture reviewers:** Independent Work Mode exact-head review

**Implementation owner:** Lead Implementation Engineer under the accepted
synthetic-only activation

**Planning base:** `e418479bbb10f48c1a3c7dd207c299cc49226896`

**Authorization state:** Pull request #52 merged the separately reviewed
synthetic implementation activation as
`b099ba156cefd3ba26fa9e5ff89a07d5a9e1f6ca`. Only the exact disconnected
repository candidate is authorized; dependencies, services, deployment, and
real document use remain unauthorized.

## Purpose

This proposal defines a bounded, quarantine-first inspection pipeline for
untrusted document candidates. It refines the accepted document-admission
boundary into a reviewable future implementation plan without selecting a live
information domain, parser product, scanning product, persistence technology,
interface, or deployment.

The proposed phase asks:

> Can Jebediah inspect a synthetic document candidate, preserve exact evidence
> and authority boundaries, and fail closed before any derived output becomes
> eligible for a future consumer?

Passing Phase 2 synthetic validation would not authorize a real VBA document,
establish source truth, register knowledge, promote memory, or permit ordinary
retrieval.

## Proposal custody and decision path

This plan, the
[Phase 2 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_2_VALIDATION_REQUIREMENTS.md),
the [Safe VBA Evidence Preparation Guide](VBA_EVIDENCE_PREPARATION_GUIDE.md),
and required navigation updates form one multi-document architecture proposal.
They must:

1. Exist on one remote short-lived branch with a complete manifest.
2. Receive independent Work Mode review at an exact head.
3. Receive a Chief Architect disposition at that reviewed head.
4. Merge before any accepted direction is treated as canonical.
5. Receive a separate bounded implementation authorization before code begins.
6. Complete synthetic implementation review before any real-document decision.

Authoring or accepting this package does not itself authorize implementation or
live information.

## Architecture basis

### Accepted authority

- [ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md)
  preserves originating-source authority and keeps the Knowledge Vault derived.
- [ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
  owns the quarantine-first admission decision, candidate formats, state
  vocabularies, append-only transition requirements, and derived-content
  boundary.
- [Organizational Document Ingestion Specification](ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
  owns the canonical future submission, admission, processing, provenance,
  security, retention, and retry requirements.
- [Data Ownership](DATA_OWNERSHIP.md) keeps ownership, source authority, and
  permitted use explicit.
- [Security Policy](../SECURITY.md) prohibits public sensitive evidence and
  requires least-privilege secret handling.

### ADR assessment

No new ADR is proposed. The plan does not change ADR 0013's System-level
decision or assign a parser, scanner, store, API, queue, service, or deployment
technology. The proposed package name, internal contracts, and checkpoints are
an application-level refinement of that accepted decision.

A new or revised ADR is required before acceptance if review changes source or
derived authority, the Collector boundary, candidate format families, state
semantics, persistence responsibility, interface ownership, deployment
topology, or recovery authority.

### Existing adapter boundary

The existing `collector.adapters.file.adapt_file_record` reads TXT and Markdown
directly and delegates content into the current Collector pipeline. It has no
quarantine, admission-attempt, malware, active-content, byte-evidence,
retention, or append-only transition contract.

Phase 2 must not extend, wrap, or route untrusted organizational documents
through that adapter. It remains a legacy bounded text adapter until separately
reviewed. The proposed inspection responsibility uses a new package and has no
existing caller integration.

### Evidence classification

**Repository Verified**

- At the planning base, ADR 0013 and the Organizational Document Ingestion
  Specification contain the accepted quarantine-first states and authority
  boundary.
- The existing file adapter directly reads TXT and Markdown and has no accepted
  document-admission contract.
- No document-admission package, quarantine store, binary parser, inspection
  service, or live document path exists in the reviewed baseline.

**Future Design**

- Every package, interface, policy, stage, checkpoint, and validation behavior
  below is proposed and unimplemented.
- The proposal can become an architecture baseline only after exact-head review,
  Chief Architect acceptance, and merge.

**Working Assumptions**

- `collector.document_admission` is the clearest application-level package name
  for ADR 0013's responsibility.
- UTF-8 with an optional UTF-8 byte-order mark is the narrowest useful initial
  text profile.
- Synthetic reference adapters can prove contracts without selecting production
  persistence.

**Open Questions**

| Question | Required owner or gate |
| --- | --- |
| Which scanner, detector, parser, and isolation mechanisms satisfy the threat model? | Security threat review, dependency review, and Chief Architect acceptance |
| What numeric live-data limits are safe for the first domain and environment? | Information owner, security review, operations owner, and Chief Architect acceptance |
| Which digest profile and durable stores retain bytes and evidence? | Security, information-owner, persistence, and ADR review |
| Which component and operational roles own receipt, quarantine, recovery, and deletion? | Chief Architect and named operational owners |
| Which first source and consumer contracts are permitted? | Originating source authority, information owner, consumer owner, and Chief Architect |

These questions block affected implementation or live use. They are not
defaults for an implementation engineer to infer.

## Intended outcome

A future synthetic-only implementation candidate would provide:

- immutable submission, content-identity, admission-attempt, inspection,
  extraction-result, policy-profile, and audit-evidence records;
- a byte-preserving quarantine contract isolated from ordinary consumers;
- file-type detection independent of extension or claimed media type;
- fail-closed malware, macro, active-content, authorization, provenance,
  integrity, and resource-limit evaluation;
- parser execution behind an isolation contract;
- explicit complete, partial, and failed extraction evidence;
- append-only admission and processing histories;
- policy-driven retention, deletion, legal-hold, and correction evidence;
- narrow storage-neutral interfaces and synthetic reference adapters where
  separately authorized; and
- deterministic tests with generated fixtures only.

## Non-goals

Phase 2 preparation and any later bounded synthetic implementation must not:

- inspect, hash, parse, extract, submit, or ingest a real VBA document;
- copy or move a real VBA document into Jebediah, a repository, an
  agent-controlled location, quarantine, or the inspection pipeline;
- process personal, medical, organizational, confidential, licensed, or other
  live information;
- select the first live information domain or infer its source authority;
- add a production persistence store, database, migration, backup, or recovery
  system;
- add an API, queue, service, CLI, user interface, Open WebUI flow, n8n flow,
  container, or deployment;
- write to Qdrant, create embeddings, enable retrieval, or build a semantic
  index;
- create or update a Knowledge Registry record;
- create a `MemoryItem`, call the Memory Service, or grant memory eligibility;
- summarize, classify, infer, rank, recommend, or act with an AI model;
- execute macros, scripts, fields, actions, embedded objects, or fetched
  resources;
- perform OCR;
- silently accept partial extraction;
- give a scanner, parser, store, digest, or model source or truth authority; or
- give a human reviewer power to waive required security, integrity, source,
  use, or provenance checks.

Any requirement for a non-goal stops implementation for architecture and scope
review.

These non-goals constrain repository agents and the proposed system. They do
not authorize local organizational-custody staging. A future human operator may
perform only the separately authorized preparation described in the
[Safe VBA Evidence Preparation Guide](VBA_EVIDENCE_PREPARATION_GUIDE.md), after
all of its preconditions pass and while the material remains outside Jebediah.

## Proposed responsibility and package boundary

The proposed Python responsibility is:

```text
src/collector/document_admission/
    __init__.py
    models.py
    policies.py
    interfaces.py
    orchestration.py
    detection.py
    inspectors/
        __init__.py

tests/collector/document_admission/
    __init__.py
    test_models.py
    test_admission_orchestration.py
    test_byte_integrity.py
    test_format_detection.py
    test_security_dispositions.py
    test_resource_limits.py
    test_inspection_results.py
    test_retention_and_deletion.py
    test_failure_and_retry.py
    test_package_boundaries.py
```

This layout is proposed, not authorized. Concrete scanner, parser, quarantine,
and evidence adapters are omitted until threat, dependency, persistence, and
operations decisions are accepted.

The test `__init__.py` is an empty package marker required to prevent duplicate
test basenames from colliding with existing Collector and registry tests. It
defines no runtime package or behavior.

`collector.document_admission` must not import `collector.memory`,
`collector.knowledge.registry`, current Collector runtime modules, Qdrant
adapters, or network clients. Existing runtime packages must not import it
during the synthetic-only phase.

## Contract model

### Identities

Every receipt has distinct, stable identifiers for:

- submission occurrence;
- exact content identity;
- admission-evaluation attempt;
- transformation or inspection attempt;
- approved consumer and consumer-policy version;
- policy profile and version;
- detector, scanner, and inspector behavior version;
- extracted output, when one exists; and
- correlation across transitions and retries.

A repeated byte stream is a new submission occurrence but shares content
identity under the same versioned digest policy. Changed bytes create a new
content identity. Filename, extension, claimed media type, and derived text are
never identity.

### Byte-preserving source-artifact handling

The receiving boundary must:

1. Assign a submission identity before inspection.
2. Place the exact received bytes in quarantine before format parsing.
3. Record byte count and a versioned cryptographic digest.
4. Preserve the received bytes without normalization, repair, decompression,
   encoding conversion, metadata rewriting, or parser mutation.
5. Give detectors, scanners, and inspectors only a read-only bounded view or
   isolated copy.
6. Store normalized names, claimed types, detected types, and extracted
   representations separately.
7. Recheck byte count and digest when bytes cross a storage or process boundary.
8. Keep quarantine inaccessible to ordinary Collector, registry, memory,
   retrieval, model, and interface consumers.
9. Apply an approved terminal-state retention disposition.

The digest algorithm and version are mandatory policy-profile fields. This
proposal does not select a production digest profile. A digest proves byte
identity only; it does not prove meaning, truth, safety, ownership, or
authority.

### Submission envelope

The future immutable envelope must include every field required by the
canonical ingestion specification, including approved domain and intended use,
producer, submitter, and approved consumer references, consumer-authorization
policy, supplied and safe names, claimed and detected type, byte evidence,
source reference, distinct time semantics, classification and handling policy
references, state, findings, and correlation.

Missing required source, ownership, intended-use, consumer authorization,
classification, retention, deletion, or provenance evidence fails closed. The
implementation must not generate an authoritative value or substitute a
default.

## Initial candidate format profile

Only these detected formats are candidates:

| Candidate | Required detection and initial boundary |
| --- | --- |
| PDF | PDF signature and structurally parseable document; no OCR, executable action, script, attachment execution, external fetch, or encrypted input |
| DOCX | Valid Office Open XML word-processing package; no macro payload, executable object, external fetch, encryption, path traversal, or unsupported package relationship |
| TXT | Valid encoding under the approved text profile; no silent replacement of invalid bytes |
| Markdown | Valid encoding under the approved text profile; links, HTML, directives, and model-like instructions remain inert text |

The approved text policy must be explicit and versioned. This proposal
recommends UTF-8, optionally with a UTF-8 byte-order mark, as the initial
profile. Acceptance of another encoding requires a reviewed plan change rather
than silent auto-detection.

Extension and supplied media type are untrusted hints:

- A conclusively unsupported detected format is `rejected`.
- A conclusive mismatch between the envelope and detected format is `rejected`
  for that attempt and may be resubmitted with corrected evidence.
- An ambiguous format or active-content result is `held`.
- An unavailable or indeterminate required detector is `evaluation_failed`.
- An invalid byte sequence, malformed structure, encryption, traversal entry,
  or exceeded mandatory limit is `rejected`.

Macro-enabled Office formats such as DOCM, XLSM, and PPTM are outside the
initial candidate profile. A macro payload found in a purported DOCX is
`rejected`. No macro is executed, stripped, repaired, or converted.

## Quarantine and inspection stages

The proposed orchestration stages are:

1. **Receive envelope:** validate required metadata and assign submission
   identity.
2. **Quarantine bytes:** isolate exact bytes and record integrity evidence.
3. **Detect format:** inspect bounded signatures and structure without trusting
   the supplied name or media type.
4. **Evaluate security:** apply malware and active-content evaluators.
5. **Evaluate policy and limits:** check domain, producer, submitter, approved
   consumer, use, classification, provenance, duplicate, retention, and
   resource policy.
6. **Record admission disposition:** end the attempt as `accepted`, `rejected`,
   `held`, or `evaluation_failed`.
7. **Inspect accepted content:** run one isolated, versioned inspector.
8. **Record extraction result:** retain complete, partial, failed, omission, and
   resource evidence.
9. **Apply consumer eligibility:** evaluate complete output against the approved
   synthetic validation-consumer policy. `ready` requires a positive result for
   that exact consumer; ordinary and runtime access remain prohibited.
10. **Apply retention disposition:** retain, delete, or hold bytes and derived
    outputs under approved policy without rewriting audit history.

Only an `accepted` submission enters stage 7. No shortcut or human action may
start inspection from `received`, `quarantined`, `held`, `rejected`, or
`evaluation_failed`.

## Admission lifecycle

The implementation must use ADR 0013's states and transitions exactly:

```text
received -> quarantined -> validating -> accepted
                                  |----> rejected
                                  |----> held
                                  `----> evaluation_failed
```

`accepted`, `rejected`, `held`, and `evaluation_failed` are terminal for one
attempt. Every transition records prior state, next state, aware timestamp,
actor or component, stable reason code, policy version, and correlation.

Retry or review creates a linked attempt:

- `held` requires an authorized reviewer or missing policy decision.
- Review evidence may allow a new `validating` attempt; it cannot directly
  create `accepted`.
- `evaluation_failed` waits for the unavailable condition to clear and any
  unknown durable outcome to be reconciled.
- `rejected` is not automatically retried.
- Terminal history is append-only and cannot be overwritten.

Acceptance means admissible for one approved use. It is not factual
verification, approval of document claims, permission for every consumer,
Knowledge Registry registration, memory promotion, or action authority.

## Synthetic validation-consumer boundary

The proposed synthetic-only phase has one bounded consumer contract: the test
and review harness that verifies the document-admission contract. This consumer
is policy evidence, not a deployed component or runtime reader.

Its immutable policy must identify:

- a non-sensitive synthetic consumer identity;
- the intended use `synthetic_contract_validation`;
- the synthetic-only information classification;
- permitted candidate formats and extraction outputs;
- required completeness, integrity, provenance, omission, and limit checks;
- policy identity and version; and
- an explicit prohibition on runtime, API, registry, memory, retrieval, model,
  interface, and real-information access.

Admission must establish authorization for that exact consumer and intended use
before producing `accepted`. Missing, invalid, or mismatched authorization fails
closed. An unavailable policy produces `evaluation_failed`; a decision that
requires authorized judgment produces `held`; a conclusive unauthorized
consumer or use produces `rejected`.

The synthetic consumer's eligibility decision is recorded for each
transformation attempt. `ready` means that required derived outputs completed
and passed the exact synthetic consumer's eligibility checks. It does not make
the output eligible for an ordinary or runtime consumer, expose a content-read
interface, or authorize a future real-information consumer.

Any later pilot, interface, registry producer, memory path, or runtime consumer
requires a separate accepted consumer contract and implementation plan.

## Malware, macro, and active-content dispositions

Required evaluator outcomes are bounded and evidence-linked:

| Evaluator result | Admission disposition |
| --- | --- |
| Clean under the exact evaluator and policy version | Continue validation; never accept on this result alone |
| Confirmed malicious content | `rejected` |
| Confirmed unsupported macro, executable payload, script, external fetch requirement, or path traversal | `rejected` |
| Suspicious or ambiguous content requiring authorized judgment | `held` |
| Evaluator unavailable, timed out without a valid result, or returned an indeterminate result | `evaluation_failed` |

A malware or active-content result must include evaluator identity, version,
policy version, time, sanitized reason code, and evidence reference. Raw
sensitive findings and document content must not enter ordinary logs or the
public repository.

Links, PDF forms, DOCX fields, comments, tracked changes, and other inert but
representational features are recorded as findings. If an approved extractor
cannot represent a feature required for the intended use, the content is held
or its transformation ends as partial; it is never silently complete.

This plan selects no scanning product and authorizes no network lookups.

## Evaluator and parser isolation contract

Every detector, scanner, and binary inspector that handles untrusted bytes must
run behind an isolation boundary appropriate to its threat surface. No
"lightweight" detector receives broader access merely because it runs before
admission. The isolation boundary:

- has no network access or external-resource fetching;
- cannot execute child processes, macros, scripts, actions, or embedded
  payloads;
- exposes only the quarantined read-only input and a bounded private temporary
  workspace;
- applies wall-clock, CPU, memory, input, output, temporary-space, nesting,
  archive-entry, and expansion limits;
- prevents path traversal and writes outside the workspace;
- returns a typed result through a size-bounded channel;
- removes temporary artifacts under the approved cleanup policy;
- survives parser crash, timeout, malformed output, and forced termination
  without exposing bytes or partial output; and
- records sanitized failure and resource evidence.

The process, container, operating-system, or library mechanism is intentionally
unselected. It requires threat review and a separately reviewed technology
decision before implementation.

## Resource-limit policy

No evaluator or inspector may run with an unlimited, absent, zero-by-default,
or silently inferred bound. A versioned policy profile must provide positive
limits appropriate to each candidate format.

| Limit class | Required policy fields |
| --- | --- |
| All inputs | Maximum input bytes, wall-clock time, CPU time, process memory, temporary bytes, result bytes, warnings, and findings |
| TXT and Markdown | Maximum decoded characters, lines, line length, and link or directive count |
| PDF | Maximum pages, objects, object depth, stream bytes, embedded objects, fonts, and extracted characters |
| DOCX | Maximum archive entries, expanded bytes, per-entry bytes, compression ratio, relationship count, XML depth, and extracted characters |

The initial profile fixes executable child processes, network requests,
external fetches, macro execution, embedded payload execution, and OCR to zero.

Numeric live-data values are unresolved because no first information domain,
threat model, operational environment, or information owner is approved. A
future implementation may prove enforcement using deliberately small synthetic
profiles, but it must not contain permissive production defaults or receive
real information until the live profile is reviewed and accepted.

## Inspection and extraction result

Transformation attempts retain ADR 0013's states:

```text
processing -> ready
          `-> processing_failed
```

Each attempt records:

- input submission and content identities;
- inspector, configuration, code or artifact, and policy versions;
- start, completion, and failure times;
- detected format and structural findings;
- output identity, byte count, and digest when an output exists;
- extraction quality: `complete`, `partial`, or `none`;
- location-map capability, counts, warnings, omissions, unsupported features,
  and limits reached;
- sanitized error classification;
- resource-use evidence; and
- the eligibility decision and policy evidence for the approved synthetic
  validation consumer, with ordinary and runtime eligibility fixed to false.

`complete` may become `ready` only when every required output and validation
check succeeds and the exact synthetic validation consumer is eligible.
`partial`, `none`, missing consumer authorization, or failed consumer
eligibility end as `processing_failed`; partial artifacts remain quarantined
evidence and are never ordinary retrieval content. An unexpected parser
exception, timeout, crash, invalid result, or unknown durable outcome cannot
produce `ready`.

Extracted text and metadata are derived. They cannot overwrite, repair, or
impersonate the submitted bytes or originating source.

## Provenance and audit evidence

Append-only evidence must connect:

- source authority and safe source reference;
- producer, submitter, domain, intended use, consumer, and policy references;
- submission occurrence and exact content identity;
- supplied and detected format evidence;
- quarantine placement and integrity checks;
- malware, macro, active-content, authorization, provenance, duplicate, and
  resource findings;
- each admission and transformation transition;
- reviewer identity or approved role, decision, rationale, and time for a held
  follow-up;
- detector, scanner, inspector, configuration, and code versions;
- output identity, omissions, warnings, and eligibility;
- retry and prior-attempt relationships; and
- retention, deletion, correction, legal-hold, and cleanup outcomes.

Audit evidence must not contain raw extracted text, file bytes, credentials,
private locators, personal information, exploitable findings, or unsanitized
parser output. Evidence proves what the pipeline did, not that source claims are
true.

## Retention, deletion, correction, and legal hold

Every submission must have an approved retention and deletion policy before
receipt. The policy records:

- policy identity and version;
- handling for bytes, envelope, findings, extracted output, audit history,
  temporary artifacts, logs, and backups;
- terminal-state retention class and deadline;
- legal-hold and correction authority;
- deletion propagation and verification requirements; and
- accountable owner and custodian roles.

Required behavior:

- `received`, `quarantined`, and `validating` bytes remain isolated only for the
  bounded attempt and recovery window.
- `held` bytes remain isolated until the review deadline, policy-directed
  deletion, or a linked attempt; no indefinite implicit hold is permitted.
- `rejected` and `evaluation_failed` bytes follow their approved evidence and
  troubleshooting window, then verified deletion unless a legal hold applies.
- `accepted` bytes are retained only when the information-owner policy requires
  an evidentiary snapshot; otherwise they are deleted after required evidence
  is sealed.
- Partial or failed derived artifacts are deleted or retained as quarantined
  evidence under explicit policy and never become ordinary content.
- Source correction or authorized deletion propagates to cached and derived
  material without rewriting historical audit evidence.
- Legal hold suspends normal deletion only under recorded authority and policy.
- Deletion records actor or component, time, scope, reason, policy, result, and
  any unresolved backup or recovery obligation.

No duration, backup design, or deletion mechanism is selected here. Missing
policy values block receipt rather than creating indefinite retention.

## Internal interfaces

Future implementation may define narrow, storage-neutral interfaces for:

- immutable quarantine placement, read-only access, integrity verification, and
  policy-directed deletion;
- append-only admission and transformation attempt evidence;
- format detection;
- malware and active-content evaluation;
- isolated document inspection; and
- retention and deletion disposition.

The interfaces must expose no hidden update, ordinary content read, retrieval,
promotion, or approval operation. Not-found, identity conflict, validation
failure, evaluator unavailability, policy failure, resource exhaustion, and
unknown durable outcome remain distinct typed behavior.

No network API or service is proposed. Interface and persistence technology
selection remains a separate gate.

## Implementation checkpoints

The current implementation candidate has completed Checkpoints 0 through 5 on
branch `feature/knowledge-manager-phase2-synthetic-inspection`. Checkpoint 6
remains open pending publication of one exact head, independent Work Mode
review, and Chief Architect merge disposition. Completion here is candidate
evidence only, not canonical merge or operational readiness.

### Checkpoint 0 - canonical activation

Before code:

- Phase 1 implementation and documentation closeout are merged.
- This proposal and its validation requirements are accepted and merged.
- A bounded synthetic-only Phase 2 sprint is authorized.
- Threat-review ownership and the package boundary are accepted.
- The implementation base is clean, synchronized, and recorded.
- Existing tests and documentation validation pass.

### Checkpoint 1 - immutable contracts

Implement only immutable identities, envelope, policy, admission,
transformation, finding, extraction-result, and audit-evidence models. Prove
fail-closed validation with synthetic values.

### Checkpoint 2 - storage-neutral boundaries

Implement narrow quarantine and append-only evidence interfaces plus
non-production synthetic reference adapters. No durable technology or existing
runtime integration is permitted.

### Checkpoint 3 - bounded detection and security behavior

Implement format-detection and evaluator contracts with generated fixtures and
test doubles. Product selection, real scanning, network lookup, and real
document access remain prohibited.

### Checkpoint 4 - isolated synthetic inspectors

Only after threat review and dependency approval, implement bounded TXT,
Markdown, PDF, and DOCX inspectors using generated fixtures. Dependency or
isolation changes reopen review.

### Checkpoint 5 - orchestration and evidence

Connect the synthetic boundaries through the exact state transitions. Verify
retry, conflict, timeout, crash, partial extraction, deletion, and audit
behavior without adding a runtime entry point.

### Checkpoint 6 - independent implementation review

Run the full evidence matrix, publish an exact-head implementation PR, obtain
independent Work Mode review, and stop for Chief Architect merge disposition.
No real-information decision is bundled with implementation approval.

## Validation and demonstration boundary

The normative evidence is in the
[Phase 2 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_2_VALIDATION_REQUIREMENTS.md).
Fixtures must be generated, synthetic, minimal, non-sensitive, and committed
only when their construction and expected behavior are reviewable.

A permitted demonstration shows state transitions, quarantine isolation,
format and security findings, extraction evidence, and fail-closed behavior
using synthetic fixtures. It must not connect to Jebediah runtime, a source
system, Qdrant, a model, or real organizational material.

## Dependencies and blockers

Phase 1 closeout, this architecture baseline, the threat and dependency reviews,
owner assignments, and the exact synthetic-only activation are complete. The
repository candidate is blocked from canonical completion only by:

1. Completion and publication of the exact validation evidence.
2. Independent Work Mode review of one exact remote implementation head.
3. Chief Architect disposition for that exact reviewed head.
4. Canonical merge and post-merge documentation closeout if approved.

Real document use remains additionally blocked by:

1. Approval of one information domain and originating source authority.
2. Producer, submitter, consumer, intended-use, and classification contracts.
3. Privacy, legal, consent, retention, deletion, legal-hold, and correction
   policies.
4. Accepted numeric resource limits and production evaluator policy.
5. Persistence, backup, restore, migration, reconciliation, cleanup, and
   evidence-retention decisions.
6. Synthetic implementation merge and closeout.
7. A separate exact-scope Chief Architect authorization for the named real
   source and document set.

## Risks

- Binary parsers and archive containers create a high-risk untrusted-input
  boundary.
- Incomplete isolation can expose network, filesystem, process, temporary-file,
  or resource-exhaustion paths.
- Overly permissive or missing limits can turn inspection into denial of
  service.
- Retaining bytes or findings without approved policy can create privacy,
  legal, recovery, and deletion liabilities.
- Treating clean scanning, complete extraction, or human review as truth can
  transfer authority incorrectly.
- Partial extraction can hide material omissions if it is represented as ready.
- A convenient integration with the legacy file adapter, registry, memory, or
  retrieval path can bypass admission.

These risks are gates, not implementation details to infer later.

## Rollback

The accepted baseline creates no runtime state to roll back. If the separate
activation proposal is rejected, it may be closed or reverted without changing
this baseline.

A future synthetic implementation must remain removable by reverting its
bounded package and tests. Because it has no production persistence, caller,
service, dependency, external data, or deployment, rollback must require no
data migration. If a proposed implementation cannot preserve that property,
work stops for revised architecture and recovery review.

## Architecture review and merge record

Independent Work Mode approved the substantive proposal at exact head
`d28e1b35d7e495ff1a33d159dbd37f0c2321c8e7`. After Phase 1 closeout created a
mechanical branch conflict, a fresh independent review approved exact updated
head `a6917965236a0897ea2adf8284bb7190a78f488f` with no findings. The Chief
Architect approved that exact head for squash merge.

Pull request #50 squash-merged the five-file documentation package to canonical
`main` as `92e4b8c7353f6d47097e7eaf6c743c78f39c8e10`. Documentation validation
passed for 69 Markdown files and 213 tracked files. Whitespace checks passed.
Acceptance and merge granted no implementation or real-document authority.

## Exact next decision

The separately stated
[Phase 2 Synthetic Implementation Activation](KNOWLEDGE_MANAGER_1_PHASE_2_SYNTHETIC_IMPLEMENTATION_ACTIVATION.md)
must receive independent exact-head Work Mode review, a Chief Architect
exact-head authorization decision, and canonical merge before code begins. It
must not authorize real VBA inspection, production persistence, deployment, or
runtime integration.
