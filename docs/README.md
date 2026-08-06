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
- [JCS Specification](JCS_SPECIFICATION.md) is the non-authoritative Milestone
  C1 proposal for JCS evidence, alternatives, decision framing, and review. It
  does not define JCS or prove **Specified** maturity.
- [Collector 1.0 Specification](COLLECTOR_1_SPECIFICATION.md) defines the
  proposed bounded text-record ingestion contract, identity, provenance,
  idempotency, failure, security, and acceptance requirements.
- [Collector 1.0 Implementation Plan](COLLECTOR_1_IMPLEMENTATION_PLAN.md)
  defines implementation gates, adapter boundaries, tests, rollback, and the
  evidence required before live deployment.
- [Memory Architecture](ARCHITECTURE_MEMORY_SYSTEM.md) defines the implemented
  memory-service candidate, governance model, persistence compatibility, and
  retrieval boundary.
- [Sprint 003 Completion](SPRINT_003_COMPLETE.md) records the implemented
  memory-intelligence baseline and its reported runtime validation.
- [Sprint 004 Specification](SPRINT_004_SPECIFICATION.md) defines the merged
  provenance, lifecycle, retrieval-ranking, and compatibility scope.
- [Sprint 005 Implementation Plan](SPRINT_005_IMPLEMENTATION_PLAN.md) defines
  the accepted memory-domain, Qdrant, embedding, migration, and rollback
  architecture and records the completed repository implementation phases.
- [Sprint 005 Validation Requirements](SPRINT_005_VALIDATION_REQUIREMENTS.md)
  defines implementation-review and future deployment evidence gates.
- [Sprint 006 Proposal v1 Abandonment Record](SPRINT_006_PROPOSAL_V1_ABANDONED.md)
  records the unrecoverable proposal's permanent abandonment and the gate for
  a newly authored v2 successor without reconstructing lost architecture.
- [Sprint 006 Proposal v1 Work Mode Findings](reviews/SPRINT_006_PROPOSAL_V1_WORK_MODE_FINDINGS.md)
  preserves seven historical design inputs for v2 without treating them as
  recovered or accepted architecture.
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
- [Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
  defines permanent role authority, mandatory engineering gates, handoff
  packets, and coordination evidence labels.
- [Chief Architect Phase 3B Reconciliation Decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
  records `CA-2026-08-06-P3B-RECONCILIATION`, the inactive implementation
  authority, revised milestone sequence, pull-request preservation, ADR impact,
  and documented-but-unexecuted future revert plan.
- [Documentation Lead Protocol](governance/JEBEDIAH_DOCUMENTATION_LEAD_PROTOCOL.md)
  defines the Documentation Suite's post-merge closeout responsibilities and
  limits.
- [Architecture Principles](ARCHITECTURE_PRINCIPLES.md) defines enduring
  constraints for architectural decisions.
- [Current Architecture](ARCHITECTURE.md) defines the approved conceptual
  layers, context, boundaries, and unresolved decisions.
- [ADR Process](adr/README.md) defines decision triggers, levels, lifecycle,
  numbering, and review.
- [ADR 0011: Knowledge Vault Authority and Boundary Model](adr/0011-knowledge-vault-authority-and-boundary-model.md)
  is an Accepted System decision for a derived governed knowledge repository;
  it does not authorize implementation, external information use, or a live
  organizational pilot.
- [Organizational Intelligence Interface Specification](ORGANIZATIONAL_INTELLIGENCE_INTERFACE_SPECIFICATION.md)
  defines an accepted evidence-bearing, read-only executive interface organized around
  four plain-language questions without selecting implementation technology.
- [Organizational Document Ingestion Specification](ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
  defines accepted quarantine-first PDF, DOCX, TXT, and Markdown admission with source
  identity, provenance, time, state, and derivation boundaries.
- [Organizational Intelligence Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md)
  defines architecture and future implementation evidence without authorizing
  implementation, live information use, deployment, or action.
- [ADR 0012: Executive Organizational Intelligence Interface Boundary](adr/0012-executive-organizational-intelligence-interface-boundary.md)
  is an Accepted System decision for the read-only executive read-model
  boundary.
- [ADR 0013: Governed Organizational Document Admission Boundary](adr/0013-governed-organizational-document-admission-boundary.md)
  is an Accepted System decision for quarantine-first document admission and
  non-authoritative derivation.
- [Organizational Intelligence Phase 3A Executive Product Shell Plan](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_PRODUCT_SHELL_PLAN.md)
  is the accepted complete product, component, route, view-model, synthetic-data,
  state, accessibility, test, rollback, and exact-file plan; it grants no
  implementation merge, live-information, or deployment authority.
- [Organizational Intelligence Phase 3A Local Preview Operator Guide](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_LOCAL_PREVIEW.md)
  explains how to run and inspect the implemented synthetic, loopback-only local
  preview; it describes no deployment and claims no Operational maturity.
- [Organizational Intelligence Product Program Phase 3A Closeout](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_CLOSEOUT.md)
  records the exact implementation review, pull request #56 squash merge,
  post-merge automated and browser validation, synthetic-only boundary,
  exclusions, rollback, and remaining authorization gates.
- [Organizational Intelligence Phase 3A Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_VALIDATION_REQUIREMENTS.md)
  define accepted model, fixture, rendering, route, workflow, accessibility,
  security, isolation, browser, repository, and review evidence.
- [Organizational Intelligence Phase 3A Threat Model](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_THREAT_MODEL.md)
  defines accepted assets, trust boundaries, threats, controls, residual risks,
  and stop conditions for a synthetic loopback preview.
- [Organizational Intelligence Phase 3A Dependency Assessment](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_DEPENDENCY_ASSESSMENT.md)
  selects the existing Python standard library and test tooling without a
  dependency, lock, browser framework, or build-chain addition.
- [ADR 0015: Executive Product Shell and Local Preview Boundary](adr/0015-executive-product-shell-and-local-preview-boundary.md)
  is an Accepted System decision for one presentation-only component over
  compiled fabricated fixtures.
- [Phase 3A Implementation Authorization](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_IMPLEMENTATION_AUTHORIZATION.md)
  is the adopted bounded Chief Architect decision record under which the exact
  merged synthetic implementation was completed; it grants no live-information,
  deployment, action, or later-phase authority.
- [Phase 3B Governed Intake Plan](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_GOVERNED_INTAKE_PLAN.md)
  is the accepted PDF-only, one-operator architecture. Its former broad-package
  manifest is historical design and salvage evidence, not active implementation
  authority.
- [Phase 3B Lifecycle and Recovery Specification](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_LIFECYCLE_AND_RECOVERY.md)
  defines accepted future architecture constraints for encryption, retention,
  deletion, hold, reconciliation, backup, restore, and rotation without
  authorizing implementation or custody.
- [Phase 3B Threat Model](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_THREAT_MODEL.md),
  [Dependency Assessment](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_DEPENDENCY_ASSESSMENT.md),
  and [Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_VALIDATION_REQUIREMENTS.md)
  define accepted future security, supply-chain, isolation, test, browser, and
  negative-capability constraints. No dependency, implementation, runtime, or
  live-use authority is active.
- [ADR 0016: Local Governed PDF Intake and Custody Boundary](adr/0016-local-governed-pdf-intake-and-custody-boundary.md)
  is the Accepted System decision for the local governed PDF intake and custody
  boundary; it grants no real-source or deployment authority.
- [Phase 3B Implementation Activation](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_IMPLEMENTATION_ACTIVATION.md)
  is a historical architecture-activation record with no active implementation
  authority.
- [Phase 3B Implementation Milestone 1 Authorization](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_MILESTONE_1_AUTHORIZATION.md)
  is a Historical scope record that grants no current implementation authority.
- [Phase 3B Completion Directive](governance/ORGANIZATIONAL_INTELLIGENCE_PHASE_3B_COMPLETION_DIRECTIVE.md)
  is Superseded as implementation authority and retained for audit context.
- [Knowledge Manager 1.0 Phase 1 Implementation Plan](KNOWLEDGE_MANAGER_1_PHASE_1_IMPLEMENTATION_PLAN.md)
  defines the accepted and authorized metadata-only Knowledge Registry
  foundation while preserving its Checkpoint 0 and excluded capabilities.
- [Knowledge Manager 1.0 Phase 1 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_1_VALIDATION_REQUIREMENTS.md)
  defines the accepted synthetic domain, repository, dependency, compatibility, and stop
  evidence for the authorized registry foundation.
- [Knowledge Manager 1.0 Phase 1 Closeout](KNOWLEDGE_MANAGER_1_PHASE_1_CLOSEOUT.md)
  records the exact implementation merge, post-merge validation, implemented
  maturity, exclusions, rollback, and remaining gates.
- [ADR 0014: Knowledge Registry Domain Boundary](adr/0014-knowledge-registry-domain-boundary.md)
  is an Accepted System decision for a storage-neutral registry domain separate
  from memory, ingestion, retrieval, runtime, and source authority.
- [Knowledge Manager 1.0 Phase 2 Document Inspection Plan](KNOWLEDGE_MANAGER_1_PHASE_2_DOCUMENT_INSPECTION_PLAN.md)
  defines the accepted synthetic-only, quarantine-first planning baseline under
  ADR 0013 without authorizing code, live documents, storage, services, or
  deployment.
- [Knowledge Manager 1.0 Phase 2 Validation Requirements](KNOWLEDGE_MANAGER_1_PHASE_2_VALIDATION_REQUIREMENTS.md)
  define the accepted fail-closed fixture, isolation, state, resource, provenance,
  retention, authority, and review evidence for the bounded candidate.
- [Knowledge Manager 1.0 Phase 2 Synthetic Implementation Activation](KNOWLEDGE_MANAGER_1_PHASE_2_SYNTHETIC_IMPLEMENTATION_ACTIVATION.md)
  defines the accepted exact models, states, interfaces, reference adapters,
  tests, owners, rollback, files, and implementation gates merged through pull
  request #52.
- [Knowledge Manager 1.0 Phase 2 Closeout](KNOWLEDGE_MANAGER_1_PHASE_2_CLOSEOUT.md)
  records the exact reviewed implementation head, pull request #53 squash merge,
  post-merge validation, synthetic-only boundary, exclusions, rollback, and
  remaining authorization gates.
- [Knowledge Manager 1.0 Phase 2 Threat Model](KNOWLEDGE_MANAGER_1_PHASE_2_THREAT_MODEL.md)
  assigns prevention, detection, safe failure, audit evidence, tests, and
  canonical owners for the complete synthetic threat inventory.
- [Knowledge Manager 1.0 Phase 2 Dependency Assessment](KNOWLEDGE_MANAGER_1_PHASE_2_DEPENDENCY_ASSESSMENT.md)
  selects a standard-library-only candidate with no dependency or lock change
  and defers parser, scanner, isolation, and persistence technologies.
- [Phase 2 Implementation Authorization](governance/KNOWLEDGE_MANAGER_1_PHASE_2_IMPLEMENTATION_AUTHORIZATION.md)
  records the adopted bounded Chief Architect decision and its completed
  implementation execution while preserving separate deployment and
  real-information gates.
- [Safe VBA Evidence Preparation Guide](VBA_EVIDENCE_PREPARATION_GUIDE.md)
  provides local-only blank preparation structures and checklists while keeping
  real VBA material outside Jebediah.
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
- [Codex Bootstrap](../CODEX_BOOTSTRAP.md) defines Codex-specific
  Implementation Engineer operations.
- [AI Collaboration Standard](../.ai/COLLABORATION.md) defines human and AI
  collaboration behavior within the canonical coordination authority model.
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

## Historical pull request #60 audit and salvage artifacts

The following Markdown files were introduced by pull request #60. Their
substantive instructions are preserved as audit and salvage evidence, with a
later quarantine notice added so a direct reader cannot mistake them for
current guidance. They are not canonical operator guidance, confer no
authority, and must not be executed, followed, deployed, or used to configure a
runtime, domain, certificate, workspace, backup, restore, or public endpoint:

- `docs/ADMINISTRATOR_QUICK_START.md`
- `docs/BACKUP_GUIDE.md`
- `docs/DEMONSTRATION_GUIDE.md`
- `docs/DEPLOYMENT_GUIDE.md`
- `docs/DISASTER_RECOVERY_GUIDE.md`
- `docs/OPERATIONS_GUIDE.md`
- `docs/PRODUCTION_CONFIGURATION_GUIDE.md`
- `docs/WORKSPACE_GUIDE.md`

The
[Chief Architect Phase 3B reconciliation decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md)
owns their disposition. Pull request #60's Git history is the evidence source;
these files are intentionally excluded from the current canonical-document
list. Direct access to an artifact does not override this quarantine.

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
