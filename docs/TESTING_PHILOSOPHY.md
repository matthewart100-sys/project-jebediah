# Testing Philosophy

**Status:** Active

## Purpose

Testing provides evidence that Project Jebediah behaves as approved, fails
safely, and remains recoverable as it changes. This philosophy defines
technology-neutral expectations before an implementation language or test
framework is selected.

Tests do not replace architecture, review, security analysis, or operational
validation. They turn important claims from those disciplines into repeatable
evidence.

## Current evidence and scope

### Verified facts

- The repository currently contains documentation and governance, not Project
  Jebediah application or infrastructure implementation.
- No language, framework, test runner, coverage tool, schema validator, or CI
  platform configuration has been selected.
- Documentation checks are currently performed manually and recorded in pull
  requests.

### Reported facts

The bootstrap environment reports products that may later require integration,
workflow, model, persistence, and recovery testing. Their current
configuration and operation are not verified.

### Working assumptions

- Future behavior will include deterministic logic and probabilistic AI
  boundaries.
- Some tests will require controlled substitutes for unavailable or sensitive
  local services.
- Recovery and action safety will matter as much as successful output.

### Open questions

- Which language and test tools best fit the first approved JCS design?
- Which reported services can support safe isolated test environments?
- Which critical user and operator journeys require end-to-end coverage?
- Which performance and reliability targets will future use cases justify?

These are selected with the relevant component architecture, not by this
foundation document.

## Principles

### Test risk, not implementation trivia

Prioritize behavior whose failure would corrupt authority, expose data, perform
an unsafe action, prevent recovery, mislead a person, or break an owned
contract. A large test count is not evidence of good risk coverage.

### Keep evidence deterministic where practical

Control time, randomness, network access, model responses, environment, and
concurrency when the behavior under test does not require them to vary.
Nondeterminism is isolated, bounded, measured, and reported honestly.

### Test observable contracts

Assert owned inputs, outputs, side effects, failure classes, state
transitions, and operational signals. Avoid tests that depend on internal
structure without protecting meaningful behavior.

### Failure paths are first-class

Test invalid input, missing configuration, authorization denial, timeouts,
retries, duplicate requests, partial success, stale state, dependency loss,
restore, rollback, and cleanup where they can affect safety or recovery.

### Fast feedback and realistic boundaries complement each other

Use many focused deterministic tests for local logic and fewer higher-cost
tests for contracts, integrations, critical journeys, and recovery. A test is
valuable because it covers a risk at the right boundary, not because it fits a
pyramid mechanically.

### Test artifacts are maintained engineering assets

Tests, fixtures, fakes, evaluators, and test utilities have owners, clear
purpose, review, and removal paths. Flaky, opaque, or stale tests are defects.

## Evidence layers

### Static and repository validation

Validate artifacts without executing application behavior:

- Markdown structure and links
- Formatting and line endings
- Secrets and prohibited sensitive content
- Configuration and schema syntax once formats exist
- Dependency and license policy
- Generated-artifact consistency
- Architecture, status, sprint, roadmap, and changelog coupling

Milestone 6 will automate agreed repository checks.

### Unit tests

Exercise a small deterministic behavior without live external dependencies.
Use them for transformations, validation, policy, state transitions, conflict
rules, parsing, and failure classification.

Unit tests should be fast enough to run during local development and should
name the behavior they protect.

### Component tests

Exercise a component through its owned public surface with controlled local
dependencies. Verify configuration, state, error mapping, side effects, and
important observability at the component boundary.

### Contract and schema tests

Verify that producers and consumers agree about semantics, required fields,
compatibility, identifiers, time, error behavior, and versioning.

Once machine-readable schemas are approved, validate examples and
compatibility automatically. A schema-valid payload can still violate semantic
or authority rules, so behavioral checks remain necessary.

### Integration tests

Exercise approved adapters or dependencies with realistic behavior:

- Persistence and migration
- Model-serving boundary
- Workflow runtime
- Vector or search index
- External or local source adapters
- Authentication and authorization integration
- Backup and restore tooling

Use isolated test data and reproducible setup. Do not point ordinary tests at
live authoritative data or uncontrolled production-like services.

### End-to-end tests

Cover a small set of critical human or operational journeys across approved
boundaries. Include the result visible to the person or operator, not merely an
internal API response.

End-to-end tests remain few because they are slower and harder to diagnose.
They do not replace focused tests at lower levels.

### Operational and recovery tests

Validate that the system can be operated and recovered:

- Health and degraded-state detection
- Dependency outage and reconnection
- Backup creation and integrity
- Restore to an isolated environment
- Rollback or forward recovery
- Restart and idempotent reconciliation
- Capacity or resource exhaustion behavior
- Runbook accuracy

A backup is not proven until an owned restore test succeeds.

### Security tests

Verify controls proportionate to the threat:

- Authentication and authorization denial
- Least-privilege boundaries
- Untrusted input and injection resistance
- Secret and sensitive-data exclusion
- Dependency and artifact provenance
- Logging and error redaction
- Rate or resource abuse where relevant
- Prompt, tool, template, query, and workflow boundaries

Security testing supports but does not replace threat modeling and review under
[`SECURITY.md`](../SECURITY.md).

## Test selection by change

| Change type | Minimum evidence |
| --- | --- |
| Documentation or governance | Structure, local links, sensitive-content scan, canonical consistency, and `git diff --check` |
| Deterministic logic | Focused unit tests including material failure and boundary cases |
| Interface or schema | Producer/consumer contract tests, compatibility assessment, invalid cases, and migration evidence |
| Persistence or data ownership | Integration tests, conflict and partial-failure cases, migration, backup/restore, and provenance checks |
| External adapter | Contract tests using controlled substitutes plus bounded integration evidence |
| Workflow or automation | Trigger, authorization, idempotency, retry, partial action, rollback, and audit evidence |
| AI or model behavior | Deterministic boundary tests, representative evaluations, safety cases, and controlled model/version evidence |
| Infrastructure or operations | Syntax/plan validation, isolated apply where possible, health, rollback, and restore evidence |
| Security control | Denial and bypass attempts, redaction, least privilege, and regression evidence |
| Defect correction | A regression test that fails before and passes after when practical |

The change may require more evidence based on consequence.

## Deterministic test design

- Give each test one clear behavioral reason to fail.
- Use explicit inputs and expected outputs.
- Control time with an injectable clock or bounded fixture when implementation
  permits.
- Seed or replace randomness.
- Block unapproved network access.
- Bound retries and timeouts.
- Avoid dependence on test order or shared mutable state.
- Compare structured values rather than unstable formatting when formatting is
  not the contract.
- Prefer purpose-built builders over large opaque fixtures.
- Make cleanup safe after success and failure.

## Test data and fixtures

- Use minimal synthetic data by default.
- Never copy credentials, personal data, private prompts, raw logs, database
  contents, or sensitive topology into fixtures.
- Preserve the edge conditions needed by a test without preserving real
  identity.
- Document fixture provenance and regeneration when derived.
- Version fixtures when compatibility matters.
- Keep temporary test state isolated and automatically removable.
- Treat a sanitized dataset as sensitive until the sanitization method is
  reviewed.

## External dependencies and test doubles

A fake, stub, emulator, or recorded response must preserve the contract
behavior the test relies on, including failures. Do not create a permissive
double that makes invalid interactions pass.

Validate critical doubles against the real approved dependency at an owned
cadence. Network recordings must be sanitized, minimal, reviewable, and
invalidated when contracts change.

## AI and probabilistic evaluation

AI behavior needs two complementary kinds of evidence:

### Deterministic boundary tests

Test prompt assembly, context selection, permissions, tool arguments, output
parsing, schema validation, redaction, timeouts, fallback, and refusal without
depending on a live model when practical.

### Behavioral evaluations

Evaluate representative cases against explicit success, safety, and escalation
criteria. Record model identifier and version, prompt or policy version,
parameters, evaluation dataset version, environment, date, and observed
variance.

- Do not assert exact prose unless exact text is the contract.
- Include adversarial, ambiguous, missing-context, and unsafe-action cases.
- Separate quality from safety and latency measures.
- Human review remains necessary when judgment is the product behavior.
- A single successful sample is not evidence of reliable behavior.
- Changed model or prompt versions rerun affected evaluations.

The project does not approve a universal evaluation score during Phase 0.

## Coverage

No numeric line or branch coverage threshold is approved. Coverage can reveal
untested code but cannot prove correct behavior, safe failure, architecture
alignment, or meaningful assertions.

Future components may set justified thresholds for a specific risk. Never add
low-value tests solely to raise a number.

## Flaky and quarantined tests

- A flaky test is a defect with an owner.
- Do not normalize rerunning a failing suite until it passes.
- Diagnose product race, environment instability, shared state, timing, or
  test design.
- Quarantine only to preserve useful signal while an owned fix is active.
- A quarantine records reason, risk, owner, and removal condition.
- Critical safety, security, data-integrity, or release-gate tests cannot be
  silently quarantined.

## Execution stages

### During development

Run the fastest relevant focused checks and inspect the changed behavior.

### Before commit

Run affected deterministic tests, repository checks, and `git diff --check`.

### Pull request

Run the complete affected suite, contract and integration evidence required by
the change, documentation checks, and security checks. Record exact commands,
results, omissions, and environment limitations.

### Main and release

Run stable required checks on reviewed `main`. Release candidates add
end-to-end, migration, rollback, recovery, artifact, and post-deployment
verification appropriate to their contents under the
[Release Process](RELEASE_PROCESS.md).

## Failure triage

When a test fails:

1. Preserve the failing evidence.
2. Determine whether product, test, fixture, environment, or dependency is at
   fault.
3. Reproduce at the smallest useful boundary.
4. Fix the cause rather than weakening the assertion.
5. Add or improve regression evidence.
6. Rerun the affected and neighboring tests.
7. Record any residual uncertainty.

## Test review

Reviewers ask:

- Which risk does this test cover?
- Does it assert behavior rather than implementation trivia?
- Are important failure and boundary cases included?
- Is nondeterminism controlled or measured honestly?
- Are fixtures safe, minimal, and understandable?
- Does the test fail for the intended reason?
- Can a future maintainer diagnose it?
- Does higher-level evidence cover the real owned boundary?

## Exceptions

If required testing is temporarily impossible, the pull request records the
missing evidence, risk, reason, compensating validation, owner, and resolution
gate. An exception requires review and does not become precedent.

The [Definition of Done](DEFINITION_OF_DONE.md) remains the canonical
completion standard.
