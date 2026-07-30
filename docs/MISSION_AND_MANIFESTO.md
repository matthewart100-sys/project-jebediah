# Mission and Manifesto

## Mission

Project Jebediah exists to build a local-first, production-quality AI platform
that can be understood, recovered, changed, and operated over the long term.

The platform is intended to combine knowledge, automation, reasoning, and
AI-assisted operations without surrendering control of project memory or
system behavior to opaque conversations, unreviewed configuration, or
unrecoverable services.

## The problem we are solving

Useful local AI systems can become fragile when their architecture exists only
in a maintainer's memory, workflows are modified without traceability, data
ownership is unclear, or AI conversations quietly become the only record of
why a decision was made.

Project Jebediah addresses that failure mode by treating documentation,
recoverability, and reviewability as engineering work rather than
administrative overhead.

## Manifesto

### GitHub is the enduring project memory

The repository is the authoritative record for current state, standards,
architecture, decisions, and planned work. Chats can help create or review that
record, but they cannot replace it.

### Documentation precedes implementation

Components must have a documented purpose, boundary, ownership model, and
decision history before dependent implementation begins. Documentation and
code evolve together after implementation starts.

### Architecture guides code

Code is evidence of an approved design, not a substitute for one. Material
changes to platform boundaries, data ownership, topology, security posture, or
core technology require a reviewed Architecture Decision Record.

### Local-first means durable control

Project Jebediah should remain useful and understandable without depending on
an external conversation or an unavailable hosted service for its core memory.
Local-first does not mean isolated from every external tool; it means the
project deliberately controls its authoritative data, configuration, and
recovery path.

### Recoverability is a feature

A system that cannot be restored, reconstructed, or explained is not
production quality. Configuration, backups, restore procedures, and rollback
expectations must become versioned and testable as the platform grows.

### Determinism is preferred where practical

Stable inputs should produce predictable outcomes when the problem permits it.
When probabilistic AI behavior is necessary, its boundaries, inputs, outputs,
and failure handling must be explicit and observable.

### Explicit beats implicit

Assumptions, ownership, interfaces, data classifications, failure modes, and
operational expectations should be written down. Unknowns are acceptable;
hidden unknowns are not.

### Modularity protects the future

Subsystems should have coherent responsibilities and replaceable boundaries.
Modularity is not permission to create speculative services: separation must
follow demonstrated responsibilities and approved architecture.

### Every change is reviewable and traceable

Work occurs on short-lived branches, in small logical commits, through pull
requests. Meaningful changes update documentation, tests where applicable, and
the changelog.

### Humans and AI follow the same quality bar

AI assistance does not weaken review, testing, security, attribution, or
documentation requirements. An AI contributor must establish context from the
repository, state assumptions, respect approval gates, and leave a durable
handoff.

## Phase 0 boundaries

Project Genesis will not choose an application language, framework, protocol,
schema, or new service. It will preserve the reported platform and named
subsystems while creating the process needed to evaluate those choices later.

JCS begins with definition and specification, not implementation. Collectors
must not depend on JCS until that specification is reviewed and approved.

## Commitment to future contributors

A new engineer or AI should be able to clone this repository, follow its
onboarding path, distinguish fact from assumption, understand the approved
architecture, and contribute safely without access to previous chat history.
Meeting that standard is the central deliverable of Project Genesis.
