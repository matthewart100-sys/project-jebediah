# Project Jebediah Documentation

This directory contains the durable technical, process, and governance memory
for Project Jebediah. GitHub Markdown is preferred because it is reviewable,
searchable, linkable, and version controlled.

## Current canonical documents

- [Mission and Manifesto](MISSION_AND_MANIFESTO.md) defines why the project
  exists and the principles that must survive implementation choices.
- [Project Genesis Plan](genesis/PROJECT_GENESIS_PLAN.md) defines the approved
  Phase 0 organization, delivery order, risks, and acceptance criteria.
- [JCS Definition Implementation Plan](JCS_DEFINITION_PLAN.md) defines the
  approved Phase 1 execution order, evidence, ownership, decisions, review
  gates, risks, and acceptance criteria without defining JCS.
- [Project Genesis Foundation Audit](genesis/GENESIS_FOUNDATION_AUDIT.md)
  maps required topics, records consistency evidence and corrections, and
  owns the clean-room onboarding result.
- [Project Status](../PROJECT_STATUS.md) distinguishes current truth from
  reported facts, assumptions, and unresolved questions.
- [Current Sprint](../CURRENT_SPRINT.md) defines the active goal, bounded
  scope, and acceptance criteria.
- [Roadmap](../ROADMAP.md) preserves the strategic sequence and phase gates.
- [Contribution Guide](../CONTRIBUTING.md) defines how contributors prepare,
  validate, review, and merge work.
- [Git Workflow](GIT_WORKFLOW.md) defines branches, commits, pull requests, and
  merge policy.
- [Sprint Process](SPRINT_PROCESS.md) defines planning, execution, review,
  carryover, and closure.
- [Definition of Done](DEFINITION_OF_DONE.md) defines the universal finish
  line.
- [Repository Standards](REPOSITORY_STANDARDS.md) defines paths, artifact
  policy, generated content, dependencies, and repository hygiene.
- [Engineering Standards](ENGINEERING_STANDARDS.md) defines
  language-independent engineering quality.
- [Documentation Standards](DOCUMENTATION_STANDARDS.md) defines canonical
  ownership, evidence labels, writing, navigation, review, and maintenance.
- [Architecture Principles](ARCHITECTURE_PRINCIPLES.md) defines enduring
  constraints for architectural decisions.
- [Current Architecture](ARCHITECTURE.md) defines the approved conceptual
  layers, context, boundaries, and unresolved decisions.
- [ADR Process](adr/README.md) defines decision triggers, levels, lifecycle,
  numbering, and review.
- [Glossary](reference/GLOSSARY.md) owns shared project terminology.
- [Component Registry](reference/COMPONENT_REGISTRY.md) tracks component
  identity, maturity, responsibility, and component ownership.
- [Data Ownership](DATA_OWNERSHIP.md) defines authoritative, cached, derived,
  and temporary information plus lifecycle responsibility.
- [Digital Twin Position](design/DIGITAL_TWIN_POSITION.md) defines the
  concept's purpose, exclusions, relationships, and implementation gates.
- [Testing Philosophy](TESTING_PHILOSOPHY.md) defines risk-based evidence
  layers, deterministic testing, AI evaluation, recovery testing, and review.
- [Security Policy](../SECURITY.md) defines safe vulnerability reporting,
  public-repository boundaries, controls, and current security gaps.
- [Operations Philosophy](OPERATIONS_PHILOSOPHY.md) defines ownership, health,
  observability, change, recovery, runbooks, incidents, and readiness.
- [Release Process](RELEASE_PROCESS.md) defines versioning, release gates,
  artifacts, tagging, deployment separation, verification, and withdrawal.
- [v0.1.0 Release Checklist](releases/v0.1.0/CHECKLIST.md) applies those gates
  and preserves the verified initial engineering-foundation release record.
- [v0.1.0 Release Notes](releases/v0.1.0/RELEASE_NOTES.md) define the public
  scope, limitations, onboarding path, and release boundary.
- [AI Entry Point](../AGENTS.md) defines the mandatory orientation and
  invariants shared by every AI contributor.
- [Codex Bootstrap](../CODEX_BOOTSTRAP.md) defines Codex-specific Lead
  Engineer operations.
- [AI Collaboration Standard](../.ai/COLLABORATION.md) defines human and AI
  roles, authority, review, and handoff behavior.
- [AI Memory Contract](AI_MEMORY_CONTRACT.md) defines durable memory layers,
  promotion rules, session recovery, and prohibited content.
- [Chief Architect Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md)
  defines the evidence and formal decision required at significant
  checkpoints.
- [Changelog](../CHANGELOG.md) records notable repository changes and releases.
- [Repository README](../README.md) is the primary entry point.
- [`scripts/validate_docs.py`](../scripts/validate_docs.py) implements the
  repository-owned documentation and hygiene checks run locally and by GitHub
  Actions.

Only documents that exist and contain substantive guidance are linked here.
This index grows only when approved work creates another substantive canonical
owner.

## Documentation authority

Repository documents serve different purposes:

1. `PROJECT_STATUS.md` records current verified reality.
2. Architecture and standards documents define current technical and process
   expectations.
3. Accepted, non-superseded Architecture Decision Records explain decisions
   and their consequences.
4. Sprint and roadmap documents describe intended work.
5. Issues and pull requests record proposals, reviews, and work history.
6. External bootstrap artifacts and conversations are historical context only.

The documents must agree. An accepted decision that changes architecture also
requires the current architecture documentation to change in the same pull
request. Contributors may not choose whichever conflicting statement is most
convenient.

## Evidence categories

Architecture, design, data, and operations documents must distinguish:

- **Verified facts:** supported by repository or validated system evidence.
- **Reported facts:** provided by a trusted source but not independently
  validated.
- **Working assumptions:** temporary premises used to make bounded progress.
- **Open questions:** unresolved matters with an owner or resolution gate.

Unsupported statements must not be presented as established truth.

## Future permanent documentation

The approved Genesis plan and roadmap identify reference, specification,
runbook, workflow, schema, test, and source artifacts that later work may
require. They are created only when approved content provides a real owner,
consumer, and maintenance path. Empty policy placeholders are not created.

## Bootstrap-material policy

The onboarding ZIP, Word document, and Genesis PDFs are not copied into this
directory as canonical sources. Binary and conversational sources are
difficult to review and can drift from the repository. Their requirements must
instead be promoted into maintained Markdown through normal pull requests.
