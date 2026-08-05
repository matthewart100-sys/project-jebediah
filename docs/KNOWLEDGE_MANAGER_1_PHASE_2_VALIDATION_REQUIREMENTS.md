# Knowledge Manager 1.0 Phase 2 Validation Requirements

**Status:** Proposed

**Phase:** Document Inspection Pipeline

**Date:** 2026-08-05

**Applies to:** A future bounded implementation authorized from the
[Phase 2 Document Inspection Plan](KNOWLEDGE_MANAGER_1_PHASE_2_DOCUMENT_INSPECTION_PLAN.md)

**Authorization state:** Proposal only. These requirements do not authorize
code, dependencies, services, deployment, real document use, or live
information.

## Purpose

These requirements define the evidence needed to review a future
synthetic-only document-inspection implementation. Passing them would prove
only the tested admission, isolation, inspection, failure, and evidence
contracts.

Validation does not prove document claims, source authority, malware absence
beyond the tested evaluator, safe operation outside the tested limits, consumer
eligibility, Knowledge Registry eligibility, memory eligibility, or permission
to use real VBA material.

## Evidence principles

- Use generated synthetic fixtures and non-sensitive identifiers only.
- Test negative and unavailable behavior at every authority and security gate.
- Fail closed on missing policy, ownership, provenance, evaluator, or durable
  outcome.
- Test the exact boundary at, below, and above each configured resource limit.
- Use fakes to prove timeout, crash, malware, indeterminate evaluation, storage
  failure, and unknown-outcome behavior without unsafe payloads.
- Keep raw bytes and extracted text out of logs and failure messages.
- Test package separation mechanically.
- Do not start a network service, Qdrant, Ollama, n8n, Open WebUI, a container,
  or a production persistence dependency.
- Do not read an external folder or use a real organizational document.
- Treat any unplanned runtime integration, dependency, service, content store,
  or live-information path as a stop condition.

## Proposed test organization

The future implementation should use:

```text
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

The existing pytest configuration remains authoritative. Adding a dependency,
test runner, container, service, or external fixture source requires separate
review.

The empty test-package marker is part of the proposed test layout because
existing Collector and registry suites already use overlapping test basenames.
It must contain no test or runtime behavior.

## Fixture requirements

All committed fixtures must be:

- generated specifically for testing;
- minimal and deterministic;
- free of names, personal information, organizational records, credentials,
  private addresses, sensitive topology, and copyrighted source material;
- reviewable from a generator or exact byte construction;
- labeled synthetic in code and documentation; and
- limited to the behavior under test.

The future fixture matrix must include:

| Family | Synthetic cases |
| --- | --- |
| TXT | Valid UTF-8, optional UTF-8 BOM, invalid byte sequence, line limit, character limit, oversized input |
| Markdown | Valid bounded text, inert link, inert HTML or directive, model-like instruction treated as data, structural limit |
| PDF | Minimal valid text document, signature mismatch, malformed structure, encryption marker, active action, embedded attachment, page or object limit, parser timeout |
| DOCX | Minimal valid Office Open XML document, malformed package, traversal entry, external relationship, macro payload marker, encryption marker, archive-entry limit, expansion limit, compression-ratio limit |

No fixture may contain functional malware, an executable macro, an exploit, or
private source material. Security dispositions use inert markers and evaluator
test doubles.

## Immutable contract validation

Tests must prove:

- all submission, content, attempt, transition, finding, policy, extraction,
  and audit records are immutable values;
- identifiers are required, stable, and never derived from filename alone;
- empty and whitespace-only identifiers or policy references are rejected;
- datetimes are timezone-aware and preserve their stated semantics;
- supplied and detected names and types remain distinct;
- content identity requires a versioned digest and byte count;
- collection inputs normalize to immutable collections and reject duplicates;
- required source, domain, intended-use, producer, submitter, approved consumer,
  consumer-policy, classification, retention, deletion, and provenance
  references cannot be omitted;
- invalid enum or state values are rejected;
- equality is deterministic; and
- construction performs no current-time, random-identity, source-authority,
  admission, or approval inference.

## Byte integrity and quarantine validation

Tests must prove:

- a submission identity exists before any detector or inspector runs;
- received bytes move to quarantine before format parsing;
- the quarantined byte sequence is exactly equal to the received sequence;
- byte count and versioned digest are stable and rechecked at each simulated
  boundary;
- no detector, scanner, or inspector can mutate the quarantined bytes;
- normalized names and derived outputs are stored separately;
- failed placement, partial write, digest mismatch, missing bytes, or unknown
  write outcome cannot advance to `validating`;
- quarantined bytes have no ordinary read, registry, memory, retrieval, model,
  or interface consumer;
- cleanup follows policy and records evidence; and
- a quarantine failure does not leak bytes into exceptions or logs.

Property-based tooling is not required. Deterministic fixed byte sequences and
existing test facilities are sufficient.

## Admission transition matrix

The future orchestration tests must permit only:

| Prior state | Next state |
| --- | --- |
| `received` | `quarantined` |
| `quarantined` | `validating` |
| `validating` | `accepted` |
| `validating` | `rejected` |
| `validating` | `held` |
| `validating` | `evaluation_failed` |

Tests must reject:

- every skipped, reversed, self, or terminal-state transition;
- inspection from any state other than `accepted`;
- a human review that directly writes `accepted`;
- acceptance with one required check missing, false, indeterminate, or
  unavailable;
- acceptance without authorization for the exact synthetic consumer and
  intended use;
- overwrite of prior transition or terminal evidence; and
- transition history without prior state, next state, aware time, actor or
  component, reason code, policy version, and correlation.

Each terminal disposition must retain its exact evidence. `accepted` must
remain explicitly scoped to one intended use and must not expose an authority,
truth, approval, registry, memory, retrieval, or action flag.

## Admission failure matrix

| Condition | Required disposition |
| --- | --- |
| All required checks pass under exact policies | `accepted` |
| Permanent authorization, policy, format, integrity, provenance, encryption, structural, or limit failure | `rejected` |
| Authorized human decision or missing policy judgment is required | `held` |
| Required evaluator, policy version, or durable result is unavailable or indeterminate | `evaluation_failed` |
| Confirmed malicious content | `rejected` |
| Confirmed macro, executable payload, script, external fetch requirement, or path traversal | `rejected` |
| Suspicious or ambiguous active content | `held` |
| Scanner timeout or unavailable result | `evaluation_failed` |

Tests must prove that a clean malware result does not accept content by itself
and that uncertainty or evaluator failure never defaults to clean.

## Synthetic consumer-authorization validation

Tests must prove:

- the consumer contract has immutable non-sensitive consumer, policy-version,
  intended-use, classification, permitted-format, required-output, and
  eligibility evidence;
- the only Phase 2 consumer is the synthetic test and review harness under the
  intended use `synthetic_contract_validation`;
- admission verifies the exact consumer identity, policy version, intended use,
  and synthetic-only classification;
- missing, invalid, mismatched, expired, or unauthorized consumer evidence never
  produces `accepted`;
- an unavailable consumer policy produces `evaluation_failed`;
- a consumer decision requiring authorized judgment produces `held`;
- a conclusive unauthorized consumer or use produces `rejected`;
- one consumer's eligibility is not copied to another consumer or use;
- the synthetic consumer contract grants no API, runtime reader, ordinary
  retrieval, registry, memory, model, interface, or real-information access;
  and
- authorization and eligibility evidence contain no document content or
  sensitive value.

## Format detection validation

Tests must prove:

- extension and claimed media type are not trusted as format identity;
- detection runs against bounded bytes in quarantine;
- a supported extension with unsupported bytes is rejected;
- a mismatched claimed and detected format is rejected for that attempt;
- ambiguous detection is held;
- detector unavailability is evaluation-failed;
- invalid text bytes are visibly rejected rather than replaced;
- only the accepted text encoding profile succeeds;
- PDF signature and structure checks are distinct;
- DOCX requires a valid bounded Office Open XML word-processing package;
- macro-enabled Office formats and a macro payload inside purported DOCX are
  rejected;
- encrypted, malformed, traversal, and resource-unsafe inputs are rejected;
- links, directives, HTML, and model-like instructions remain inert; and
- OCR and external fetch are never invoked.

## Resource-limit validation

Every required numeric policy field must reject absent, unlimited, negative,
zero, non-integral, or overflow-unsafe values.

For each implemented limit, tests must cover:

- one value below the limit;
- exactly the limit;
- one value above the limit;
- combined limits where one permitted dimension cannot bypass another;
- sanitized evidence naming the exceeded policy field; and
- no output becoming accepted or ready after exceedance.

The matrix includes:

- input, output, temporary-space, wall-clock, CPU, memory, warning, and finding
  bounds;
- decoded character, line, line-length, link, and directive bounds;
- PDF page, object, depth, stream, embedded-object, font, and extracted-text
  bounds; and
- DOCX entry, expanded-byte, per-entry-byte, compression-ratio, relationship,
  XML-depth, and extracted-text bounds.

Timeout, CPU, memory, and storage exhaustion may be simulated through
deterministic fakes. Tests must not intentionally exhaust the development
machine.

## Evaluator and parser isolation validation

The accepted detector, scanner, and parser isolation mechanisms must prove:

- network access and external fetching are unavailable;
- child process, macro, script, action, and embedded-payload execution are
  unavailable;
- only the bounded read-only input and private temporary workspace are visible;
- writes outside the workspace are denied;
- path traversal is denied;
- output crosses a typed, size-bounded channel;
- parser crash, timeout, forced termination, malformed output, and oversized
  output are isolated and recorded;
- temporary artifacts are removed or retained only under explicit policy;
- bytes and partial output do not enter logs;
- one failed attempt does not corrupt or alter another; and
- no isolated result can directly write a registry, memory, retrieval, or
  consumer store.

These checks must target the selected mechanism. Interface mocks alone are not
sufficient evidence once an isolation implementation is proposed.

## Transformation and extraction validation

The only permitted transformation transitions are:

```text
processing -> ready
processing -> processing_failed
```

Tests must prove:

- only accepted input can create `processing`;
- one accepted submission may have separately identified versioned attempts;
- complete extraction records exact inspector and configuration identity;
- complete output becomes `ready` only after every required output check and a
  positive eligibility decision for the exact approved synthetic consumer;
- partial and no-output results become `processing_failed`;
- missing consumer authorization, consumer mismatch, or failed eligibility
  becomes `processing_failed`, never `ready`;
- partial output retains explicit omissions, warnings, limits, and locations;
- partial or failed output remains quarantined and consumer-ineligible;
- parser crash, exception, timeout, invalid result, and unknown durable outcome
  become `processing_failed` with sanitized evidence;
- a failed attempt does not change the accepted admission record;
- reprocessing creates a linked attempt rather than rewriting history;
- extracted bytes or text cannot overwrite the submission; and
- per-consumer eligibility and policy evidence are recorded;
- ordinary and runtime eligibility remain false in the synthetic-only phase;
  and
- the test harness receives no runtime content-read interface.

## Duplicate, retry, and conflict validation

Tests must prove:

- equal bytes create distinct submission occurrences with shared content
  identity under one digest profile;
- changed bytes create a different content identity;
- equal filename with changed bytes is not treated as a duplicate;
- a held follow-up creates a new linked `validating` attempt after authorized
  evidence;
- an evaluation-failed retry waits for the unavailable condition to clear;
- an unknown durable outcome is reconciled before retry;
- rejection is not retried automatically;
- automatic retry cannot bypass quarantine, authorization, policy, rate, cost,
  or resource controls;
- identity conflict is distinct from idempotent equal evidence;
- conflict never overwrites original evidence; and
- failures remain isolated between submission and transformation attempts.

## Provenance and audit validation

Tests must prove that evidence links:

- source authority and safe source reference;
- producer, submitter, domain, use, consumer, and policy references;
- submission, content, admission-attempt, transformation-attempt, and
  correlation identities;
- detector, scanner, inspector, policy, configuration, and code versions;
- every state transition and disposition;
- reviewer role, decision, rationale, and time when applicable;
- output identity, quality, omissions, warnings, and eligibility;
- prior attempt, retry, correction, and deletion relationships; and
- retention, cleanup, legal-hold, and unresolved recovery outcomes.

Audit tests must also prove that evidence excludes raw file bytes, extracted
text, credentials, private locators, personal information, exploitable
findings, and unsanitized exceptions.

## Retention and deletion validation

Using synthetic policies and reference adapters, tests must prove:

- receipt fails when retention or deletion policy is missing;
- each admission state maps to an explicit byte and evidence disposition;
- held material has a deadline and cannot default to indefinite retention;
- accepted bytes are retained only under affirmative policy;
- rejected, evaluation-failed, partial, and failed artifacts remain excluded
  and follow their policy deadline;
- legal hold requires recorded authority and suspends only the covered deletion;
- deletion propagates to cached and derived material;
- historical audit evidence is retained without retaining prohibited content;
- deletion records scope, actor or component, time, reason, policy, result, and
  unresolved backup obligation;
- failed or partial deletion is visible and retryable without claiming success;
- correction creates linked evidence and cannot rewrite source history; and
- a deleted or ineligible artifact cannot be reconstructed from an index,
  cache, log, or ordinary consumer path.

A production retention duration, backup, restore, or deletion mechanism cannot
be validated until separately selected and reviewed.

## Authority-negative validation

Mechanical model, export, dependency, and behavior checks must prove there is
no field, method, transition, or relationship that grants:

- factual truth or truth probability;
- source authority;
- general approval;
- Knowledge Registry registration;
- memory eligibility or promotion;
- retrieval or indexing eligibility;
- consumer access;
- decision or action authority; or
- permission to use a real document.

Tests must prove that scanner-clean, format-valid, accepted, extraction-complete,
human-reviewed, and `ready` each remain bounded evidence rather than an
authority shortcut.

## Package and dependency validation

Tests and diff inspection must prove:

- `collector.document_admission` does not import `collector.memory`,
  `collector.knowledge.registry`, runtime modules, Qdrant, model clients, API
  frameworks, queue clients, or network clients;
- current Collector, memory, service, and runtime modules do not import the new
  package during the synthetic-only phase;
- the legacy file adapter is unchanged and is not called;
- no API, CLI, service, scheduled job, watcher, or deployment entry point is
  added;
- no production persistence, migration, container, or infrastructure file is
  added;
- no dependency manifest or lock file changes without separate approval; and
- only standard-library, approved local, and separately reviewed parser or
  isolation dependencies are present.

## Failure-message and logging validation

Tests must capture representative failures and prove that messages and logs:

- use stable sanitized reason codes;
- identify attempt and correlation only through approved safe identifiers;
- omit bytes, extracted text, supplied sensitive metadata, credentials, private
  locators, stack-local content, and raw scanner or parser output;
- distinguish validation, conflict, not-found, evaluator-unavailable,
  resource-exhausted, parser-failed, persistence-failed, deletion-failed, and
  unknown-outcome behavior; and
- do not return a success-shaped fallback after failure.

Unexpected internal errors must surface through the reviewed error boundary and
leave the attempt failed or indeterminate. They must not be broadly swallowed.

## Synthetic demonstration

The review demonstration must show, without a network or live source:

1. A generated candidate receives a stable submission identity.
2. Exact bytes enter quarantine and retain byte evidence.
3. Format, security, provenance, consumer-authorization, policy, and limit
   evidence is recorded.
4. One fully valid synthetic candidate is authorized for the synthetic
   validation consumer, reaches `accepted`, passes that consumer's output
   eligibility checks, and then reaches `ready`.
5. Unsupported, suspicious, unavailable, oversized, malformed, partial, crash,
   and deletion-failure cases reach their exact non-success outcomes.
6. Held review and evaluation-failed retry create linked attempts.
7. Quarantined and failed artifacts remain inaccessible to ordinary consumers.
8. Audit evidence contains no document content or sensitive value.

The demonstration must not inspect a local document folder, call a runtime
service, write Qdrant, create a registry or memory record, or claim live
readiness.

## Required validation commands

The future implementation review records exact environment and results for:

```text
python -m pytest -q tests/collector/document_admission
python -m pytest -q
python -m compileall -q src services tests
python scripts/validate_docs.py
uv --system-certs lock --check
git diff --check
```

It must also record:

- editor or language-server diagnostics for changed Python files;
- import-boundary and dependency checks;
- changed-file and protected-path manifest;
- sensitive-value scan of the complete diff;
- confirmation that no real or external document was read;
- confirmation that no service or network dependency ran;
- complete base and head commit hashes; and
- independent exact-head Work Mode disposition.

If the selected parser or isolation mechanism requires an additional existing
project check, the accepted implementation plan must name it before coding.

## Documentation-only proposal validation

Before architecture review of this proposal:

- run the documentation validator and link checks;
- run `git diff --check`;
- inspect the full base-to-head diff and complete artifact manifest;
- scan for sensitive values, private paths, document content, and operational
  topology;
- confirm every changed artifact is documentation;
- confirm the branch contains no untracked artifact needed for review; and
- publish an accessible exact-head pull-request diff.

## Acceptance criteria

A future synthetic implementation is review-ready only when:

- every required matrix has passing deterministic evidence;
- the complete existing test suite passes unchanged except for reviewed count
  additions;
- package, authority, content, network, and runtime boundaries are mechanically
  verified;
- documentation describes the actual candidate without claiming operation;
- rollback requires no data migration;
- no blocking security, retention, dependency, recovery, or ownership gap is
  hidden; and
- Work Mode receives the actual diff at one exact remote head.

Even then, real VBA inspection remains unauthorized until a separate
information-domain, policy, operations, and exact-scope decision is reviewed
and recorded.
