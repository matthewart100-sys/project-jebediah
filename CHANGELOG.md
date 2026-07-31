# Changelog

All notable changes to Project Jebediah will be recorded in this file.

The project will use semantic versioning in the `0.x` range during early
development. Until the release process is approved, changes remain under
`Unreleased`.

## Unreleased

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

### Security

- Established that bootstrap infrastructure details remain reported and must
  be sanitized before public documentation.
