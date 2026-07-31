# Engineering Standards

## Purpose

These standards define the quality expected of Project Jebediah engineering
work regardless of implementation language or subsystem. They protect
readability, correctness, recoverability, security, and long-term ownership
without selecting technology prematurely.

No application implementation begins until its relevant architecture and
interfaces are approved.

The [current architecture](ARCHITECTURE.md) owns approved conceptual
boundaries, and the [Architecture Principles](ARCHITECTURE_PRINCIPLES.md)
constrain future decisions.

## Engineering principles

### Architecture before implementation

Implementation follows documented responsibilities and boundaries. If the
design is missing, contradictory, or materially changed by the proposed work,
resolve the architecture or ADR first.

### Readability is an operational requirement

Code will be read during incidents, upgrades, reviews, and recovery. Prefer
clear names, direct control flow, explicit state, and small cohesive units over
clever compression.

### Deterministic where practical

Stable inputs should produce predictable outputs when the problem permits it.
Time, randomness, network state, model behavior, and environment dependencies
must be controlled or made explicit in tests and interfaces.

### Explicit over implicit

Ownership, configuration, failure behavior, side effects, data provenance, and
assumptions must be visible. Hidden conventions and magic global state create
unrecoverable knowledge.

### Modular by responsibility

Modules and services exist to own coherent responsibilities, not to satisfy an
arbitrary directory pattern. Do not create a new abstraction or service
without a demonstrated boundary and consumer.

### Safe and recoverable

Changes must consider failure, rollback, retry, restore, and partial state.
Happy-path behavior alone is not production quality.

### Observable without leaking

Systems must make health, significant actions, failures, and recovery visible
while protecting secrets, personal data, prompts, and sensitive operational
details.

## Before implementation

Define:

- Problem and intended outcome
- Scope and non-goals
- Acceptance criteria
- Verified facts, reported facts, assumptions, and open questions
- Responsible component and owner
- Inputs, outputs, side effects, and failure modes
- Data ownership and provenance impact
- Security, privacy, operations, and recovery impact
- Test approach
- ADR requirement

Do not begin dependent work when a blocking question has no safe bounded
assumption.

## Interfaces and contracts

Future interfaces refine the boundaries in the
[current architecture](ARCHITECTURE.md); they do not establish competing
component responsibilities.

- Interfaces are small, explicit, and owned.
- Inputs and outputs have documented meaning, validation, and failure behavior.
- Optional and missing values are distinguished.
- Units, time zones, encodings, identifiers, and ordering guarantees are
  explicit.
- Network and process boundaries use versioned contracts when compatibility
  matters.
- Consumers do not depend on undocumented internal behavior.
- Breaking changes require migration and rollback planning.
- Schemas are machine validated once a schema format is approved.

Do not expose an internal structure as a public contract merely because it is
convenient.

## State and data

- Every mutable state item has an authoritative owner.
- Cached, derived, and temporary data are distinguishable from authoritative
  data.
- Provenance is retained where later decisions depend on origin.
- Writes validate preconditions and report partial failure.
- Repeated operations are idempotent where practical.
- Concurrent updates have an explicit conflict policy.
- Retention and deletion behavior follow data classification and ownership.
- Time-dependent state records timestamps and clock assumptions.

The [Data Ownership](DATA_OWNERSHIP.md) document defines project-wide
categories and responsibilities. Subsystem specifications must map concrete
information before implementation.

## Errors and failure behavior

- Validate at trust and ownership boundaries.
- Fail with actionable context, not raw ambiguity.
- Preserve the original cause when wrapping errors.
- Distinguish retryable, permanent, validation, authorization, and dependency
  failures where behavior differs.
- Timeouts and retry limits are explicit.
- Retries use backoff and avoid multiplying side effects.
- Partial success is represented honestly.
- Safe failure is preferred to silent corruption.
- User-facing errors do not expose secrets or private internals.

Do not catch and discard errors merely to keep a workflow moving.

## Configuration

- Configuration is external to business logic and has a documented owner.
- Defaults are safe, visible, and testable.
- Required configuration fails early with a useful message.
- Environment-specific values do not leak into shared source.
- Secret configuration uses an approved secret mechanism.
- Configuration precedence is documented.
- Runtime configuration can be inspected safely without revealing secret
  values.

Avoid adding a configuration option when one supported behavior is sufficient.

## Logging and observability

Record:

- Service or workflow health
- Important lifecycle transitions
- External dependency failures
- Retries, timeouts, and degraded behavior
- Security-relevant decisions without secret values
- Correlation or trace identifiers when a request crosses boundaries

Logs should be structured once implementation technology supports it. Log
levels have consistent meaning. High-volume debug data is disabled or bounded
in normal operation.

Metrics and alerts must correspond to an operational question or action.
Collecting data without an owner or response path is not observability.

## Security and privacy

- Apply least privilege.
- Validate untrusted input.
- Treat external content and model output as untrusted data.
- Use allowlists for sensitive actions where practical.
- Never log or commit secrets.
- Minimize collected and retained personal data.
- Protect command, template, query, and workflow boundaries from injection.
- Review dependency and artifact provenance.
- Default to denial when authorization is uncertain.
- Document residual risk.

Security requirements may be strengthened by the future `SECURITY.md`; code
must not use its absence as permission for unsafe behavior.

## Dependencies

Add a dependency only when it provides durable value that is not reasonably
implemented within the project.

Before adding one:

- Identify the exact capability required.
- Review maintenance health, security history, license, and transitive impact.
- Pin or constrain versions according to ecosystem practice.
- Define upgrade and removal ownership.
- Add tests around project-critical behavior at the dependency boundary.

Avoid overlapping libraries that solve the same problem without a documented
reason.

## Functions, modules, and services

- Each unit has one coherent responsibility.
- Names express domain meaning.
- Public surfaces are smaller than internal surfaces.
- Side effects occur at explicit boundaries.
- Pure transformation is separated from I/O where practical.
- Circular dependencies are prohibited.
- Shared utility modules do not become unowned dumping grounds.
- A service boundary requires independent responsibility, lifecycle, or
  operational need.

Refactor when repetition represents one concept, not merely similar text.

## Testing

- Tests validate behavior and important failure modes.
- Unit tests cover deterministic logic.
- Integration tests cover owned boundaries and external adapters.
- End-to-end tests cover a small number of critical user or operational flows.
- Tests control time, randomness, network access, and model responses where
  practical.
- Fixtures are minimal, understandable, sanitized, and owned.
- A regression fix includes a test that would have detected the defect when
  applicable.
- Flaky tests are defects; do not normalize rerunning until green.

No numeric coverage target is approved yet. Test selection is governed by risk
and the future testing philosophy, not by the absence of a percentage.

## AI and probabilistic behavior

- Model inputs, tool permissions, output expectations, and failure handling are
  explicit.
- Deterministic preprocessing and validation surround probabilistic behavior.
- Model output is not authoritative without the required validation.
- Prompts that affect behavior are versioned when implementation begins.
- Evaluations use representative cases and defined success criteria.
- Human approval is required for sensitive or irreversible actions unless an
  accepted decision establishes a safe automated boundary.

AI conversation history is not runtime configuration or project memory.

## Performance

Correctness and clarity precede optimization. Performance work requires:

- A stated user or operational problem
- A reproducible measurement
- A target or constraint
- Consideration of resource and complexity tradeoffs
- Evidence that the change improves the relevant measure

Do not add caches, concurrency, batching, or distributed boundaries without a
measured need and an invalidation or failure strategy.

## Refactoring

Refactoring preserves approved behavior unless the change explicitly includes
behavior modification.

- Establish tests or other behavioral evidence first.
- Keep refactors separate from unrelated features when practical.
- Update architecture or documentation when responsibilities move.
- Remove obsolete paths rather than leaving duplicate implementations.
- Verify operational and configuration compatibility.

## Review requirements

Reviewers evaluate:

- Alignment with architecture and scope
- Correctness and failure behavior
- Interface and data ownership
- Security and privacy
- Tests and validation
- Observability and operations
- Readability and maintainability
- Dependency necessity
- Documentation and changelog impact
- The [Definition of Done](DEFINITION_OF_DONE.md)

Architecture-significant work follows the
[Chief Architect Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md).

## Exceptions

When a standard cannot be met, document:

- The conflicting constraint
- Alternatives considered
- Risk introduced
- Compensating control
- Owner and resolution condition

An exception requires review and does not become precedent automatically.
