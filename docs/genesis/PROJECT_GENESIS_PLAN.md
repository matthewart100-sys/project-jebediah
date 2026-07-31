# Project Genesis Phase 0 Implementation Plan

**Status:** Approved after minor revisions

**Approved by:** Chief Architect review in the Project Jebediah ChatGPT project

**Execution model:** Sequential, reviewable pull-request checkpoints

## 1. Objective

Project Genesis converts bootstrap intent into durable, reviewable Markdown in
GitHub. Phase 0 establishes project identity, documentation hierarchy,
architecture governance, repository and engineering standards, AI
collaboration rules, contribution processes, lifecycle philosophies, and
quality enforcement.

Phase 0 does not implement JCS, collectors, application services,
infrastructure definitions, automation workflows, schemas, or a Digital Twin.

## 2. Definition of Phase 0 completion

Project Genesis is complete when a new engineer or AI can use the repository
alone to determine:

- The mission, principles, scope, and maturity
- What is verified, reported, assumed, planned, and unresolved
- The intended platform layers and named subsystems
- How architectural decisions are classified, proposed, accepted, and
  superseded
- How to plan, branch, commit, test, review, operate, release, and contribute
- How humans and AI collaborators divide authority and responsibility
- What project information must live in GitHub
- What the current sprint is and what comes next
- What "done" means for any future change

The documentation must pass automated quality checks and a clean-room
onboarding exercise. Empty placeholder documents do not satisfy the plan.

## 3. Approved revisions from the Chief Architect

The Chief Architect required ten minor revisions. They are incorporated as
binding Phase 0 requirements:

1. ADRs carry a decision level: **Foundational**, **System**, or
   **Implementation**.
2. Architecture and design documents separate **Verified Facts**,
   **Reported Facts**, **Working Assumptions**, and **Open Questions**.
3. `docs/AI_MEMORY_CONTRACT.md` defines what belongs in GitHub, what must not
   rely on chat history, how AI-authored documentation is maintained, and how
   future AI sessions establish context.
4. `docs/design/DIGITAL_TWIN_POSITION.md` defines what the Digital Twin
   represents, excludes, and relates to conceptually while deferring
   implementation.
5. `docs/DATA_OWNERSHIP.md` establishes the categories of authoritative,
   cached, derived, and temporary information before JCS or collectors are
   designed.
6. `docs/reference/` holds enduring terminology, naming guidance, and the
   component registry.
7. `CODEX_BOOTSTRAP.md` is limited to operational instructions for Codex;
   `AGENTS.md` is the tool-agnostic AI entry point.
8. `docs/ARCHITECTURE_PRINCIPLES.md` owns enduring architecture principles
   such as local-first, documentation-first, recoverable, modular, observable,
   deterministic where practical, and explicit over implicit.
9. Phase 1 begins by defining and specifying JCS. No collector may depend on
   JCS before that specification is approved.
10. `docs/DEFINITION_OF_DONE.md` defines a consistent finish line covering
    documentation, tests, changelog, links, ADRs, and repository checks.

Incorporation of these revisions constitutes architectural approval to begin
Milestone 0 and execute later milestones through reviewable pull requests.

## 4. Repository organization

The target foundation is:

```text
/
|-- README.md
|-- AGENTS.md
|-- CODEX_BOOTSTRAP.md
|-- PROJECT_STATUS.md
|-- CURRENT_SPRINT.md
|-- ROADMAP.md
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- SECURITY.md
|-- .editorconfig
|-- .gitattributes
|-- .gitignore
|-- .ai/
|   `-- COLLABORATION.md
|-- docs/
|   |-- README.md
|   |-- MISSION_AND_MANIFESTO.md
|   |-- ARCHITECTURE.md
|   |-- ARCHITECTURE_PRINCIPLES.md
|   |-- AI_MEMORY_CONTRACT.md
|   |-- DATA_OWNERSHIP.md
|   |-- DEFINITION_OF_DONE.md
|   |-- REPOSITORY_STANDARDS.md
|   |-- ENGINEERING_STANDARDS.md
|   |-- GIT_WORKFLOW.md
|   |-- SPRINT_PROCESS.md
|   |-- DOCUMENTATION_STANDARDS.md
|   |-- TESTING_PHILOSOPHY.md
|   |-- OPERATIONS_PHILOSOPHY.md
|   |-- RELEASE_PROCESS.md
|   |-- design/
|   |   `-- DIGITAL_TWIN_POSITION.md
|   |-- reference/
|   |   |-- GLOSSARY.md
|   |   `-- COMPONENT_REGISTRY.md
|   |-- genesis/
|   |   `-- PROJECT_GENESIS_PLAN.md
|   |-- reviews/
|   |   `-- ARCHITECT_REVIEW_TEMPLATE.md
|   `-- adr/
|       |-- README.md
|       `-- 0000-template.md
`-- .github/
    |-- PULL_REQUEST_TEMPLATE.md
    |-- ISSUE_TEMPLATE/
    |   |-- bug.yml
    |   |-- feature.yml
    |   `-- architecture.yml
    `-- workflows/
        `-- docs-quality.yml
```

The planned `docker/`, `scripts/`, `workflows/`, `schemas/`, and `tests/`
directories are documented as future ownership boundaries but are not created
until they contain real artifacts. The structure does not preselect a language
or runtime.

## 5. Documentation hierarchy

1. The default branch of the GitHub repository is the project source of truth.
2. `README.md` is the primary entry point.
3. `PROJECT_STATUS.md` records current verified reality and clearly labeled
   reported facts and assumptions.
4. Architecture and standards documents define the current technical and
   procedural contract.
5. Accepted, non-superseded ADRs explain decisions and consequences.
6. `CURRENT_SPRINT.md` and `ROADMAP.md` describe intended work, not current
   implementation.
7. Issues and pull requests record proposals, reviews, and execution history.
8. Bootstrap files and conversations are historical inputs only.

An ADR and the current architecture must be updated together when a decision
changes the system. Contributors stop dependent work when canonical documents
conflict.

## 6. Documentation content

### Project identity and state

- `MISSION_AND_MANIFESTO.md` defines local-first purpose and the transparency,
  recoverability, modularity, maintainability, determinism, traceability, and
  documentation-first commitments.
- `PROJECT_STATUS.md` separates verified facts, reported facts, assumptions,
  open questions, implemented capabilities, and planned work.
- `CURRENT_SPRINT.md` records one active sprint with its goal, scope,
  non-goals, acceptance criteria, risks, and progress.
- `ROADMAP.md` preserves the required order: Foundation, Documentation, JCS
  definition, Collectors, Knowledge Graph, Digital Twin, Automation, Reasoning
  Engine, Production Platform.
- `CHANGELOG.md` keeps an `Unreleased` section and versioned release history.

### Architecture and decisions

- `ARCHITECTURE_PRINCIPLES.md` contains durable constraints rather than
  implementation instructions.
- `ARCHITECTURE.md` documents goals, the reported R420/Proxmox/Ubuntu/Docker
  context, six-layer model, system context, trust boundaries, component
  relationships, and unresolved decisions. It does not invent APIs, ports,
  schemas, or service ownership.
- The component registry moves to `docs/reference/COMPONENT_REGISTRY.md` so
  architecture remains focused.
- ADRs use a single numbered log with a required decision-level field:
  Foundational for platform-wide choices, System for subsystem choices, and
  Implementation for lower-level choices with lasting consequences.
- The ADR template includes status, level, context, decision, alternatives,
  consequences, evidence, date, and supersession links.

### Data and Digital Twin

- `DATA_OWNERSHIP.md` defines authoritative, cached, derived, and temporary
  information categories; ownership responsibilities; provenance; retention;
  and unresolved system mappings.
- `DIGITAL_TWIN_POSITION.md` defines the Digital Twin as a conceptual
  representation of relevant project/system state, explicitly excludes an
  undefined replica of everything, explains its relationship to
  infrastructure, services, and knowledge, and defers implementation.

### Standards and lifecycle

- Repository standards define directory ownership, naming, dependencies,
  generated files, secret handling, binary artifacts, and canonical-document
  ownership.
- Engineering standards define readability, modularity, deterministic
  behavior, error handling, logging, configuration, dependency review, and
  documentation coupling.
- Git workflow defines a protected `main`, short-lived branches, pull requests,
  small commits, merge policy, and emergency changes.
- Sprint process uses a two-week default cadence while remaining
  outcome-focused.
- Documentation standards define Markdown, relative links, Mermaid, evidence
  categories, review rules, and maintenance responsibilities.
- Testing philosophy defines deterministic unit tests, integration tests at
  boundaries, critical-path end-to-end tests, infrastructure validation, and
  documentation checks without inventing a coverage threshold.
- Security policy addresses public-repository constraints, vulnerability
  reporting, least privilege, secrets, dependency safety, data minimization,
  threat modeling, and private infrastructure.
- Operations philosophy covers reproducibility, health checks, logs, metrics,
  backup, restore testing, rollback, runbooks, incidents, and configuration
  traceability.
- Release process uses pre-1.0 semantic versioning, tags from `main`, release
  notes, changelog finalization, rollback expectations, and post-release
  verification.
- Definition of Done applies to every change and requires current
  documentation, applicable tests, changelog evaluation, valid links, an ADR
  when triggered, passing checks, and an understandable handoff.

### Human and AI contribution

- `CONTRIBUTING.md` defines onboarding, issue, branch, commit, pull-request,
  testing, documentation, ADR, and AI-disclosure rules.
- `AGENTS.md` gives every AI contributor the same mandatory read order and
  project invariants.
- `CODEX_BOOTSTRAP.md` contains Codex operational instructions only.
- `.ai/COLLABORATION.md` defines authority, roles, approval boundaries,
  assumptions, security, and handoff behavior.
- `AI_MEMORY_CONTRACT.md` makes GitHub the durable memory layer and prevents
  unreviewed chat content from becoming implicit project truth.

## 7. Git and delivery strategy

The [Git Workflow](../GIT_WORKFLOW.md) is the canonical owner for branches,
commits, pull requests, protection, merge policy, and cleanup. The
[Contribution Guide](../../CONTRIBUTING.md) owns contributor onboarding, and
the [Definition of Done](../DEFINITION_OF_DONE.md) owns completion criteria.

Project Genesis adds one milestone-specific constraint: execute the plan
through bounded, short-lived pull-request checkpoints, provide actual artifacts
to the Chief Architect, and merge only after the required formal decision.

## 8. Implementation milestones

### Milestone 0: Approval and workspace alignment

- Incorporate the ten Chief Architect revisions.
- Connect the local checkout to the GitHub remote.
- Track `origin/main` from the verified initial commit.
- Create a dedicated feature branch.

**Acceptance:** local history matches GitHub, the working tree is understood,
and no work occurs directly on `main`.

### Milestone 1: Source-of-truth entry points

- Commit this approved plan.
- Replace the one-line README.
- Add the mission, documentation index, project status, and changelog.
- Mark bootstrap artifacts as historical inputs.

**Acceptance:** GitHub explains what Project Jebediah is, what currently
exists, and where canonical information belongs.

### Milestone 2: Working methodology

- Add repository, engineering, Git, sprint, and documentation standards.
- Add `CONTRIBUTING.md`, `CURRENT_SPRINT.md`, `ROADMAP.md`, and the Definition
  of Done.
- Add an evidence-based Chief Architect review template and use it at
  significant checkpoints.

**Acceptance:** all later Phase 0 work can follow documented rules.

### Milestone 3: AI onboarding and memory

- Add `AGENTS.md`, `CODEX_BOOTSTRAP.md`, `.ai/COLLABORATION.md`, and
  `AI_MEMORY_CONTRACT.md`.
- Verify tool-agnostic versus Codex-specific responsibilities.

**Acceptance:** a new AI can orient without the ZIP, PDFs, or chat history.

### Milestone 4: Architecture and information boundaries

- Add architecture principles, current architecture, reference terminology,
  component registry, ADR process, data ownership, and Digital Twin position.
- Apply the four evidence categories to each architecture/design document.
- Do not select protocols, schemas, languages, or new services.

**Acceptance:** design intent is preserved, information ownership is framed,
and architectural change has a tiered formal gate.

### Milestone 5: Lifecycle philosophies

- Add testing, security, operations, and release documentation.
- Add repository hygiene configuration.
- Define the Phase 0 release as `v0.1.0` after all criteria pass.

**Acceptance:** future implementation has explicit quality, safety,
operational, and release expectations.

### Milestone 6: GitHub enforcement

- Checkpoint A adds pull-request and issue templates, a maintained
  standard-library validator, and a least-privilege documentation-quality
  workflow with immutable action revisions.
- Checkpoint A validates required canonical files, Markdown structure and
  relative links, common sensitive values, prohibited runtime or bootstrap
  artifacts, and repository hygiene.
- Checkpoint B enables and verifies private vulnerability reporting.
- Checkpoint B configures `main` protection only after the workflow succeeds
  on `main`, then reads back and records the effective settings.
- Protection requires pull requests, conversation resolution, and the
  documentation-quality check; blocks force pushes and deletion; and does not
  require an independent approval unavailable to the sole maintainer.

**Acceptance:** practical standards have automated enforcement, security
reports have a verified private route, and actual GitHub settings match
canonical policy.

### Milestone 7: Genesis audit and release

- Perform a cross-document consistency and broken-link audit.
- Run a clean-room onboarding exercise.
- Map every required foundation topic to substantive documentation.
- Update status, sprint, roadmap, and changelog.
- Merge and tag the approved foundation as `v0.1.0`.

**Acceptance:** a fresh reader can accurately explain the project using GitHub
alone.

## 9. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Bootstrap claims do not match the server | Label them reported until a sanitized infrastructure audit verifies them. |
| JCS remains undefined | Block implementation and collector dependencies until the Phase 1 specification is approved. |
| "Digital Twin" accumulates incompatible meanings | Approve a position paper before implementation. |
| Data ownership is implicit | Define information categories and provenance expectations before system design. |
| Premature architecture constrains the project | Document principles and boundaries; use tiered ADRs for choices. |
| Public documentation exposes private infrastructure | Exclude secrets, addresses, personal data, and exploitable topology. |
| Documentation drifts | Couple documentation to changes and add automated quality checks. |
| Documentation becomes fragmented | Assign one canonical document per subject and maintain an index. |
| Reviews become too large | Use separate milestone pull requests and small commits. |
| Branch protection blocks a single maintainer | Require pull requests and checks without impossible self-approval. |
| The public repository has no license | Require an explicit maintainer decision before inviting reuse. |
| Binary bootstrap files become competing truth | Promote requirements into diffable Markdown rather than committing binaries as canonical sources. |

## 10. Dependencies and explicit assumptions

- The GitHub repository remains public and currently has one maintainer.
- English UTF-8 Markdown is canonical.
- Mermaid is preferred for source-controlled diagrams.
- Sprints default to two weeks but are evaluated by outcomes.
- Semantic versioning starts in the `0.x` range.
- The reported infrastructure is not yet independently verified.
- The maintainer must decide the software license.
- Phase 1 defines and specifies JCS before implementation.
- No application language, framework, API, schema, network layout, or
  deployment mechanism is selected during Genesis.

## 11. Review checkpoints

Each milestone is delivered in a small pull request or a deliberately bounded
sequence of pull requests. Work pauses after logical checkpoints for maintainer
and Chief Architect review. A later milestone may not silently revise an
earlier architectural constraint; it must update the plan or record an ADR as
appropriate.

Every Chief Architect checkpoint includes an accessible diff, patch, or exact
changed files. The formal decision and accepted recommendations are promoted
into the pull request or canonical project documents instead of remaining only
in conversation history.

## 12. Execution status

| Milestone | Status | Evidence |
| --- | --- | --- |
| Milestone 0: approval and workspace alignment | Complete | Local checkout aligned to GitHub and feature-branch workflow established |
| Milestone 1: source-of-truth entry points | Complete | Pull request #1 approved by the Chief Architect and squash-merged |
| Milestone 2A: planning and contribution workflow | Complete | Pull request #2 approved by the Chief Architect and squash-merged |
| Milestone 2B: engineering documentation standards | Complete | Pull request #3 approved by the Chief Architect and squash-merged |
| Milestone 3: AI onboarding and memory | Complete | Pull request #4 approved by the Chief Architect and squash-merged |
| Milestone 4A: architecture and decision governance | Complete | Pull request #5 approved by the Chief Architect and squash-merged |
| Milestone 4B: data ownership and Digital Twin position | Complete | Pull request #6 approved by the Chief Architect and squash-merged |
| Milestone 5A: testing and security | Complete | Pull request #7 approved by the Chief Architect and squash-merged |
| Milestone 5B: operations, release, and repository hygiene | Complete | Pull request #8 approved by the Chief Architect and squash-merged |
| Milestone 6A: repository-owned quality gate | In progress | Genesis Sprint 5 bounded feature branch |
| Milestone 6B: verified GitHub control plane | Pending | Begins after the quality workflow succeeds on `main` |
| Milestone 7: Genesis audit and release | Pending | Sequenced after verified GitHub enforcement |

## 13. Accepted follow-up recommendations

Chief Architect recommendations that are non-blocking for one checkpoint still
become durable work. The following items are accepted and assigned to the
milestone that owns their subject:

| Recommendation | Canonical owner and resolution |
| --- | --- |
| Cross-reference the Git workflow to ADR requirements. | Milestone 4 updates `docs/GIT_WORKFLOW.md` when the ADR framework exists. |
| Link AI collaboration guidance to the Definition of Done instead of duplicating it. | Milestone 3 links `.ai/COLLABORATION.md` and `CODEX_BOOTSTRAP.md` to `docs/DEFINITION_OF_DONE.md`. |
| Distinguish repository ownership from component ownership. | Milestone 4 defines component ownership in `docs/reference/COMPONENT_REGISTRY.md` without changing repository-path ownership. |
| Link interface guidance to the approved current architecture. | Milestone 4 updates `docs/ENGINEERING_STANDARDS.md` when `docs/ARCHITECTURE.md` exists. |
| Define canonical ownership for shared terminology. | Milestone 4 assigns terminology to `docs/reference/GLOSSARY.md` and cross-references architecture and ADR governance. |
| Connect durable memory promotion to architecture decision governance. | Milestone 4 adds reciprocal links between `docs/AI_MEMORY_CONTRACT.md` and the ADR framework. |
| Illustrate how ephemeral context becomes durable project memory. | Milestone 7 uses the clean-room onboarding audit to add a concise lifecycle example to `docs/AI_MEMORY_CONTRACT.md` if it improves correct application. |
| Route project-specific terms to the glossary from AI onboarding. | Milestone 4 links `AGENTS.md` to `docs/reference/GLOSSARY.md` after the glossary exists. |
| Add lightweight traceability across principles, ADRs, current architecture, and component specifications as those artifacts grow. | The Phase 1 JCS specification checkpoint evaluates a substantive `docs/reference/ARCHITECTURE_TRACEABILITY.md`; it is created only when real ADR and specification relationships exist to index. |
| Make ADR supersession, affected components, and affected architecture sections easy to navigate. | `docs/adr/README.md` adds a cross-reference index when the repository contains multiple numbered ADRs. |
| Explain how conceptual architecture becomes implementation architecture without weakening governance. | The Phase 1 JCS specification checkpoint adds architecture-evolution guidance before concrete component implementation design begins. |
| Add worked information-lifecycle examples once concrete components exist. | The Phase 1 JCS specification checkpoint adds one or two evidence-based examples to `docs/DATA_OWNERSHIP.md` after real authoritative, cached, derived, and temporary mappings exist. |
| Catalog concrete information domains, authority, derivatives, consumers, and retention ownership. | The Phase 1 JCS specification checkpoint creates `docs/reference/DATA_CATALOG.md` only when approved mappings provide substantive entries. |
| Reuse the Digital Twin acceptance questions for consistent proposal review. | The first Digital Twin specification extracts the questions from `docs/design/DIGITAL_TWIN_POSITION.md` into its review checklist without duplicating the canonical position. |
| Trace security principles to implemented controls, evidence, owners, and ADRs. | The first implementation checkpoint evaluates `docs/reference/SECURITY_CONTROL_MATRIX.md`; it is created only after concrete controls and evidence exist. |
| Map architectural risks to test evidence and responsible components. | The first checkpoint involving multiple specified subsystems evaluates a concise testing-evidence matrix based on real risks and regression obligations. |
| Reuse security review gates consistently in implementation decisions. | The first implementation-facing security ADR derives a review checklist from `SECURITY.md` and links to the policy instead of duplicating it. |
| Make real runbooks discoverable by component, owner, and recovery procedure. | The first approved operational runbook creates a lightweight `docs/runbooks/README.md` index and links to `docs/OPERATIONS_PHILOSOPHY.md` instead of duplicating policy. |
| Apply release gates consistently without rewriting them in every release pull request. | Milestone 7 derives a substantive release checklist from `docs/RELEASE_PROCESS.md` for the `v0.1.0` foundation release. |
| Standardize operational status language after real evidence exists. | The first operational implementation checkpoint defines evidence-based status terms in `docs/reference/GLOSSARY.md` and applies them to runbooks and status surfaces. |
| Keep future required status-check names deterministic. | The checkpoint that introduces a second required GitHub check establishes a concise naming convention in `docs/GIT_WORKFLOW.md` before changing protection. |
| Make required workflow ownership discoverable once multiple workflows exist. | After at least two required workflows exist, the owning checkpoint evaluates a concise `docs/reference/GITHUB_CHECKS.md` mapping each check to its owner and canonical purpose; it is not created before substantive entries exist. |
| Keep documentation validation lightweight as implementation begins. | The first Phase 1 implementation checkpoint reviews `scripts/validate_docs.py` scope and adds implementation-specific evidence through separate purpose-built workflows rather than turning `documentation-quality` into a catch-all pipeline. |
| Revisit administrator protection bypass when repository governance matures. | The first applicable checkpoint reassesses `enforce_admins` when a second maintainer joins, governance authority changes, or production releases begin, and records the verified decision in Git workflow and status documentation. |
