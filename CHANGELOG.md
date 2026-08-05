# Changelog

All notable changes to Project Jebediah will be recorded in this file.

The project uses semantic versioning in the `0.x` range during early
development. Changes not assigned to a published version remain under
`Unreleased`.

## Unreleased

### Added

- Added and accepted Knowledge Manager 1.0 Phase 1 implementation and validation
  plans plus System ADR 0014 for a synthetic, metadata-only Knowledge Registry
  foundation; only the exact bounded implementation is authorized, while
  external information, memory integration, durable storage, runtime, and
  deployment remain unauthorized.
- Added and accepted System ADRs 0012 and 0013 plus organizational-intelligence
  interface, document-admission, and validation specifications without
  authorizing implementation or live information use.
- Added and accepted System ADR 0011 to define the Knowledge Vault as a derived
  governed knowledge repository while preserving canonical project-record,
  originating-source, demonstration, and runtime authority boundaries.
- Added a durable Sprint 006 Proposal v1 abandonment record and a recoverable
  exact-head chain-of-custody requirement for multi-document architecture
  proposals before independent review.
- Added the permanent Project Coordination Protocol, Documentation Lead
  Protocol, and Foundational ADR 0005 for separated architecture,
  implementation, independent review, merge, documentation, and future
  runtime-consumer authority.
- Added the bounded Python Collector and memory-service implementation,
  including deterministic Collector logic, persistence boundaries, Qdrant and
  Ollama adapters, FastAPI routes, consolidation, confidence and retention
  scoring, the intelligence governor, metadata enrichment, and unit tests.
- Added Sprint 004 provenance and lifecycle governance models, backward-
  compatible Qdrant payload serialization, and a semantic-first retrieval
  ranking boundary prepared for future confidence, importance, recency, and
  lifecycle signals.
- Added an explicit embedding persistence identity for Ollama
  `nomic-embed-text:v1.5`, including its pinned manifest digest, 768-value
  geometry, no-normalization contract, readiness validation, and failure-safe
  vector checks.
- Approved the JCS definition implementation plan with repository-backed
  requirements, evidence and maturity separation, documentation ownership,
  decision inventory, implementation order, review gates, dependencies,
  risks, validation, and acceptance criteria without defining JCS; opened
  Milestone C1 for a proposed specification and proposed ADRs only.

### Changed

- Recorded pull request #47's squash merge of reviewed planning source
  `00db845a98f63fc3b8d1bb1135adcafa9d306b97` as
  `f9fc0c6c15a4148f5d538f56ac4ab2ec8e92c93e`, ratified
  `collector.knowledge.registry` as repository packaging only, accepted ADR
  0014, and activated the exact bounded Knowledge Registry Phase 1 scope.
- Recorded pull request #45's squash merge of reviewed source
  `c0a83f8fb4ec6ad82c90c658a4b83b8c596cd250` as
  `72099ac555efbb34b8344c5e34db7fb9aad5f69c` and reconciled the accepted
  Knowledge Vault, executive read-model, and document-admission architecture
  while retaining implementation, deployment, live-information, and action
  gates.
- Consolidated the memory domain, embedding provider, Qdrant durable-record
  and semantic-index adapter, and application orchestration under the root
  package; the FastAPI service now contains composition and HTTP translation
  only, with its duplicate source trees removed.
- Corrected Ollama digest canonicalization for the real bare `/api/tags`
  response, removed permanent model-readiness authorization, and made Qdrant
  semantic results fail closed on post-scan identity or vector
  incompatibility.
- Closed Sprint 005 after 142 tests and the Python 3.12 container build/import
  gate passed; pull request #39 squash-merged reviewed source
  `5a27358e4132a4ba14550b47c64f8538fe29094a` at
  `5f1b58767b54aed797d1ec6a2fafa084a00d6de7`, without authorizing deployment
  or live-data changes.

- Reconciled current sprint, status, architecture, component maturity, data
  ownership, testing, security, operations, release, and navigation documents
  with the merged Sprint 005 implementation while keeping deployment and live
  service operation explicitly unverified and unauthorized.
- Replaced the memory service's private Docker host mapping with Docker's
  portable `host-gateway` mapping.
- Synchronized `uv.lock` with the already declared Qdrant client dependency so
  the tested Python environment is reproducible from a fresh checkout.
- Opened Sprint 003 for Collector 1.0 definition and implementation planning
  after the merged **DEFER JCS** outcome closed C1.
- Added proposed Collector 1.0 contracts for bounded text ingestion,
  deterministic identity, provenance, idempotency, adapter separation,
  testing, rollback, and deployment gates.
- Recorded the C1 outcome **DEFER JCS** because no explicit purpose,
  responsibility, consumer relationship, boundary, or failure consequence
  supports advancing the component; kept JCS **Named**, the specification
  **Proposed**, the no-JCS baseline credible, C2 blocked, and implementation
  unauthorized, with evidence-based reconsideration triggers and no ADR.
- Refined the JCS C1 framing gate to require an explicit proceed, revise,
  defer, or remove outcome; preserved the no-JCS baseline; and kept conceptual
  evidence gaps as architectural questions while draft PR #18 remains
  unmerged and C2 remains blocked.
- Recorded verified `v0.1.0` publication, closed Project Genesis Phase 0, and
  opened Phase 1 JCS specification planning without authorizing
  implementation.
- Updated the documentation workflow's immutable `actions/checkout` pin from
  `v4` to official `v7.0.1` to use the maintained Node 24 action runtime
  without changing permissions, triggers, validation, or the required check
  name; pull-request and merged-`main` checks passed without annotations and
  branch protection remained unchanged.

### Fixed

- Updated the memory service's Qdrant lookup to use the current typed filter
  contract, restoring isolated save-and-find round trips with
  `qdrant-client`.

## [0.1.0] - 2026-07-30

### Added

- Project Genesis implementation plan, including the Chief Architect's ten
  required revisions.
- Permanent mission and manifesto.
- Source-of-truth documentation hierarchy and project entry point.
- Current-status model separating verified facts, reported facts, working
  assumptions, and open questions.
- Contribution guide and short-lived branch workflow.
- Current sprint and strategic roadmap.
- Sprint methodology and universal Definition of Done.
- Evidence-based Chief Architect review template.
- Repository standards defining path ownership, artifact policy, generated
  content, dependencies, configuration, and hygiene.
- Language-independent engineering standards for interfaces, state, failure
  behavior, security, testing, observability, and maintainability.
- Documentation standards defining canonical ownership, evidence categories,
  style, navigation, review, and drift prevention.
- Tool-agnostic AI onboarding and project invariants.
- Codex-specific Lead Engineer operating guidance.
- Human and AI collaboration roles, authority, review, and handoff rules.
- AI memory contract defining durable memory, ephemeral context, promotion,
  recovery, and sensitive-content boundaries.
- Architecture principles defining enduring technical constraints.
- Current conceptual architecture documenting evidence, layers, system
  context, boundaries, named future subsystems, and open questions.
- Tiered ADR process and decision template.
- Shared project glossary and component registry.
- Data ownership model defining information categories, roles, provenance,
  freshness, conflict, AI derivatives, retention, action, and recovery.
- Digital Twin position defining a bounded derived representation, explicit
  exclusions, conceptual relationships, state semantics, and implementation
  gates.
- Risk-based testing philosophy covering evidence layers, deterministic
  tests, AI evaluations, recovery, security, fixtures, flakiness, and review.
- Public security policy defining safe vulnerability reporting, trust and
  repository boundaries, core controls, secure lifecycle, and Phase 0 gaps.
- Operations philosophy covering ownership, health, observability, change,
  deployment, backup, restore, incidents, capacity, continuity, and readiness.
- Release process covering pre-1.0 versioning, readiness, changelog, artifacts,
  tags, deployment separation, verification, rollback, and `v0.1.0`.
- Minimal editor, Git text/binary, and ignore configuration implementing
  repository hygiene policy.
- Standard-library documentation and repository validator with one local
  invocation.
- Least-privilege GitHub Actions documentation-quality workflow using
  immutable action revisions.
- Pull-request template aligned with evidence categories, lifecycle review,
  and the Definition of Done.
- Structured bug, feature, and architecture issue forms plus a safe security
  reporting route.
- Project Genesis foundation audit mapping every required topic, recording
  consistency findings, and preserving independent clean-room evidence.
- Release-specific `v0.1.0` readiness checklist and foundation-only release
  notes.

### Changed

- Replaced the initial one-line README with a substantive Project Jebediah
  overview and onboarding path.
- Updated canonical navigation and status for the working-methodology
  checkpoint.
- Centralized branch policy in the Git workflow and documentation ownership in
  the documentation standards to prevent duplicated rules.
- Closed Genesis Sprint 1 after both working-methodology checkpoints were
  approved and opened Genesis Sprint 2 for AI onboarding and memory.
- Added canonical navigation and ownership for AI contributors and durable
  memory.
- Closed Genesis Sprint 2 after the AI onboarding and memory checkpoint was
  approved and opened Genesis Sprint 3 for architecture and information
  boundaries.
- Connected interface, Git, AI memory, repository, and onboarding guidance to
  the current architecture, ADR process, and glossary.
- Integrated data ownership and the Digital Twin position with architecture,
  terminology, component maturity, contributor onboarding, and navigation.
- Closed Genesis Sprint 3 after both architecture and information-boundary
  checkpoints were approved and opened Genesis Sprint 4 for lifecycle
  philosophies.
- Integrated operations and release requirements with engineering, security,
  testing, completion criteria, onboarding, and canonical navigation.
- Closed Genesis Sprint 4 after both lifecycle checkpoints were approved and
  opened Genesis Sprint 5 for GitHub enforcement.
- Closed Genesis Sprint 5 after repository and GitHub control-plane
  enforcement were verified and opened Genesis Sprint 6 for the Genesis audit
  and foundation release.
- Corrected stale enforcement, release-process, repository-tree, navigation,
  and component-registry statements found by the combined foundation audit.

### Security

- Established that bootstrap infrastructure details remain reported and must
  be sanitized before public documentation.
- Enabled GitHub private vulnerability reporting and made GitHub Security
  Advisories the canonical private reporting route.
- Protected `main` with pull-request, strict documentation-quality, and
  conversation-resolution requirements while blocking force pushes and
  deletion.
- Recorded the sole-maintainer administrator bypass as residual risk with
  explicit reassessment triggers.
