# JCS Definition Implementation Plan

**Status:** Active

**Last reviewed:** 2026-07-31

**Plan owner:** Lead Engineer

**Approval:** Chief Architect review and final maintainer authority

**Approval evidence:** Pull request #16, merged at
`b785bbc71421da84568f2d2be00d877d4e67bdb6`

## Purpose

This plan defines how Project Jebediah will turn the unresolved name `JCS`
into an approved, implementation-independent subsystem specification. It owns
the execution sequence, evidence requirements, documentation ownership,
decision gates, milestones, risks, and acceptance criteria for Phase 1.

The plan does not define JCS. It does not select what the initials mean, assign
runtime responsibilities, approve information authority, describe an
interface, or choose implementation technology. Those outcomes require the
separate specification and decision reviews described below.

## Authorization and boundary

The Chief Architect approved the exact plan artifacts in pull request #16,
which merged to reviewed `main` with its required check passing. Milestone C1
may create a **Proposed** JCS specification and proposed ADRs under this plan's
gates. That authorization does not approve any JCS answer or design.

Until the complete specification and required ADRs are accepted:

- No JCS schema, interface, runtime architecture, or implementation may begin.
- No collector may depend on an assumed JCS contract.
- No reported product or home-lab element may acquire a JCS responsibility.
- JCS remains at **Named** maturity.

## Intended outcome

Phase 1 must produce one coherent answer, supported by reviewed repository
evidence, to each of these questions:

1. What does `JCS` stand for, and what project problem does it solve?
2. What responsibility does JCS own?
3. What responsibilities does JCS explicitly not own?
4. Which information, if any, is JCS authoritative for?
5. Which components or people depend on JCS, and what may they rely on?
6. Which responsibilities remain with another owner?
7. What implementation-independent guarantees does JCS provide?
8. How does it fail, degrade, recover, and expose meaningful health?
9. Which security, privacy, and human/AI authority boundaries constrain it?
10. What evidence would make a future implementation ready to propose?

The result is complete only when the answers are internally consistent,
accepted through the required ADR and Chief Architect gates, and reflected in
all affected canonical documents.

## Scope

This plan covers:

- Repository-backed discovery and requirements gathering
- JCS name, purpose, scope, and explicit non-goals
- Responsibility, component ownership, and consumer boundaries
- Information authority, provenance, freshness, conflict, and lifecycle
  requirements
- Conceptual interface requirements without syntax or protocol selection
- Failure, degraded-state, recovery, observability, and operational
  expectations
- Security, privacy, trust, and human/AI authority constraints
- Alternatives and ADR trigger assessment
- Specification validation and future implementation acceptance criteria
- Canonical-document integration and review sequence

## Non-goals

This plan does not authorize or select:

- Application, JCS, collector, infrastructure, workflow, or schema
  implementation
- A programming language, framework, API style, protocol, database, queue,
  model, container, process, host, or deployment topology
- A role for n8n, Qdrant, Ollama, Docker, Proxmox, or the reported server
- Concrete collector sources or ingestion behavior
- A Knowledge Graph model, Digital Twin subject, automation boundary, or
  Reasoning Engine design
- Runtime service objectives without an approved use case and consequence
- Creation of catalogs, traceability indexes, runbooks, schemas, or test trees
  before substantive approved content gives them an owner

## Evidence basis

### Verified facts

- Reviewed GitHub `main` is the authoritative engineering memory.
- Project Genesis Phase 0 is complete and published as the documentation-only
  `v0.1.0` foundation release.
- The repository contains no Project Jebediah application, infrastructure
  definition, runtime schema, product workflow, or product test.
- `JCS` is a preserved name for a future foundational subsystem at **Named**
  maturity.
- The JCS expansion, purpose, responsibilities, interfaces, information
  authority, deployment, and implementation are unresolved.
- The roadmap requires an approved JCS specification before collector
  dependency.
- No numbered Project Jebediah ADR has been accepted.

### Reported facts

Bootstrap material reports a Dell PowerEdge R420, Proxmox, an Ubuntu virtual
machine, Docker, n8n, Qdrant, and Ollama. Repository evidence does not verify
their versions, state, configuration, data, security, capacity, or ownership.
They may inform later questions only after a sanitized audit; they are not
JCS requirements or architecture decisions.

### Working assumptions

| Assumption | Bounded use | Risk | Confirmation or invalidation |
| --- | --- | --- | --- |
| `JCS` remains a useful working label during discovery. | Names the planning subject without expanding it. | The label may bias the responsibility before its meaning is chosen. | The specification confirms or replaces the name through reviewed alternatives. |
| The approved local-first and six-layer conceptual baseline remains in force. | Constrains proposals without selecting deployment. | A new requirement may reveal a conflict. | Any change is proposed through the appropriate ADR before dependent specification text is accepted. |
| A stable conceptual contract can be specified without verifying deployment technology. | Allows responsibility and information boundaries to precede implementation. | Some requirements may depend on real operational constraints. | Technology-dependent questions are deferred with an owner and gate; no unsupported guarantee is accepted. |
| One maintainer may initially hold several roles. | Makes review responsibilities practical while keeping them explicit. | Component, information, and operational ownership may be conflated. | The specification records each responsibility separately even when one person fills them. |

These assumptions authorize only bounded planning. They do not fill an
unanswered JCS requirement.

### Open questions

The decision register below owns the current JCS questions. A question may be
closed only by repository evidence, an explicit maintainer decision, or an
accepted ADR at the stated gate.

## Requirement traceability

The following sources constrain the future specification. The plan links to
their canonical rules instead of copying policy into the specification.

| Canonical source | Requirement carried into Phase 1 | Planned evidence |
| --- | --- | --- |
| [Mission and Manifesto](MISSION_AND_MANIFESTO.md) | Define and approve JCS before implementation or collector dependency; preserve local-first, explicit, recoverable design. | Specification purpose, scope, non-goals, and dependency gate |
| [Roadmap](../ROADMAP.md) | Confirm name and purpose; boundaries; data responsibilities; conceptual interface requirements; failure, recovery, observability, security, privacy, alternatives, ADRs, and future implementation acceptance. | Complete specification outcome matrix and roadmap exit review |
| [Architecture Principles](ARCHITECTURE_PRINCIPLES.md) | Responsibilities create boundaries; interfaces are minimal; information has authority; deterministic control surrounds probabilistic behavior; recovery and trust boundaries are explicit. | Responsibility model, boundary review, and ADR analysis |
| [Current Architecture](ARCHITECTURE.md) | Preserve JCS as undefined until reviewed; do not assign products, protocols, schemas, deployment, or information authority by implication. | Proposed architecture update only after decisions are accepted |
| [Component Registry](reference/COMPONENT_REGISTRY.md) | Meet every required field before JCS advances from **Named** to **Specified**. | Registry readiness checklist linked to the specification |
| [Data Ownership](DATA_OWNERSHIP.md) | Map concrete information to authoritative, cached, derived, or temporary categories with owners, provenance, time, conflict, retention, deletion, and recovery. | JCS information-responsibility section and any required System ADR |
| [Engineering Standards](ENGINEERING_STANDARDS.md) | Define responsibility, inputs, outputs, side effects, failure, configuration, observability, security, test, and ADR impact before implementation. | Specification quality checklist |
| [Testing Philosophy](TESTING_PHILOSOPHY.md) | Define risk-based evidence for deterministic logic, contracts, integration, security, recovery, and any probabilistic boundary without choosing tools early. | Future implementation acceptance and test-evidence requirements |
| [Security Policy](../SECURITY.md) | Apply least privilege, untrusted-boundary validation, minimal authority, safe failure, recovery, supply-chain discipline, and human approval for sensitive action. | Threat and trust-boundary requirements plus security review |
| [Operations Philosophy](OPERATIONS_PHILOSOPHY.md) | Identify ownership, health, degraded state, configuration, observability, change, recovery, capacity, continuity, and retirement expectations. | Operational responsibility and readiness requirements |
| [AI Memory Contract](AI_MEMORY_CONTRACT.md) | Keep reviewed GitHub memory authoritative; treat conversation and model context as temporary unless safely promoted. | Provenance rules and repository-backed review evidence |
| [AI Collaboration](../.ai/COLLABORATION.md) | Preserve maintainer authority, Chief Architect review, evidence-based handoff, and implementation-agent scope. | Named decision and review owners |
| [ADR Process](adr/README.md) | Record lasting responsibility, data-authority, interface, trust, deployment, and technology decisions at the correct level before dependent implementation. | ADR trigger matrix and accepted decision record links |
| [Definition of Done](DEFINITION_OF_DONE.md) | Complete only with focused scope, validation, current documentation, resolved review, and honest limitations. | Final specification acceptance checklist |

## Evidence and maturity separation

Every Phase 1 artifact must identify its evidence category, canonical owner,
maturity state, and acceptance gate.

| Evidence class | Meaning in Phase 1 | Current state | Promotion gate |
| --- | --- | --- | --- |
| Foundation evidence | Approved principles, policies, architecture baseline, terminology, and process that constrain the work | Present on reviewed `main` | Changes require their normal review and any triggered ADR |
| Specification evidence | Accepted statements about JCS purpose, responsibilities, boundaries, guarantees, and constraints | Absent | Complete specification, accepted ADRs, Chief Architect approval, maintainer authority, and merge to `main` |
| Implementation evidence | Source, configuration, schemas, tests, builds, and measured behavior showing an approved design exists | Absent and unauthorized | Separate implementation plan and sprint authorization after specification acceptance |
| Operational evidence | Sanitized proof of deployment, health, capacity, security controls, backup, restore, and supportability | Absent and unauthorized | Approved implementation plus operational-readiness validation |

A successful foundation check is not specification evidence. An accepted
specification is not implementation evidence. Local success is not operational
evidence.

## Documentation hierarchy and ownership

### Current plan owner

This file is the canonical owner for Phase 1 JCS definition execution. It owns
order, gates, planned artifacts, and completion evidence. It must not become a
second owner for architecture, data, security, operations, testing, or ADR
policy.

### Proposed specification owner

After this plan is approved, create `docs/JCS_SPECIFICATION.md` as the proposed
canonical owner for JCS purpose, scope, responsibilities, non-goals,
implementation-independent guarantees, conceptual consumers and interfaces,
failure behavior, and readiness criteria.

That artifact must start as **Proposed** and remain non-authoritative until its
required ADRs and full contents are approved and merged. Its creation must add
the ownership entry to [Documentation Standards](DOCUMENTATION_STANDARDS.md).

### Existing canonical owners that must change with accepted decisions

| Concept | Canonical owner | Phase 1 update condition |
| --- | --- | --- |
| Shared expansion and concise meaning of JCS | [Glossary](reference/GLOSSARY.md) | Update when the name and meaning are accepted |
| Current JCS relationships and conceptual boundaries | [Architecture](ARCHITECTURE.md) | Update with accepted responsibility or system-boundary decisions |
| JCS identity, maturity, responsibility, and component owner | [Component Registry](reference/COMPONENT_REGISTRY.md) | Advance to **Specified** only after the complete specification is accepted |
| Information categories and concrete JCS mappings | [Data Ownership](DATA_OWNERSHIP.md) and the JCS specification | Update only when approved mappings are substantive; do not create a separate catalog prematurely |
| Lasting decision rationale | [`docs/adr/`](adr/README.md) | Add numbered ADRs when the trigger matrix requires them |
| Current reality and planning | [Project Status](../PROJECT_STATUS.md), [Current Sprint](../CURRENT_SPRINT.md), and [Roadmap](../ROADMAP.md) | Update at each accepted lifecycle transition without claiming later maturity |
| Notable delivered outcome | [Changelog](../CHANGELOG.md) | Record approved plan and later specification separately |

### Artifacts deliberately not created by this plan

- `docs/reference/ARCHITECTURE_TRACEABILITY.md` waits for real ADR and
  specification relationships.
- `docs/reference/DATA_CATALOG.md` waits for approved concrete information
  domains and ownership mappings.
- `schemas/`, `tests/`, `workflows/`, `docker/`, and runbook paths wait for
  approved implementation or operational content.

## Decision register

The register frames decisions; it does not select answers.

| ID | Decision question | Required evidence and alternatives | Decision level assessment | Owner and gate |
| --- | --- | --- | --- | --- |
| JCS-01 | What does `JCS` stand for, and what problem does it solve? | Maintainer intent, mission alignment, downstream need, retain/rename alternatives, ambiguity cost | System unless the answer changes project-wide principles or roadmap direction, then Foundational | Maintainer decision with Chief Architect review before the definition is accepted |
| JCS-02 | What coherent responsibility does JCS own, and what is excluded? | Consumer needs, existing conceptual boundaries, alternative responsibility groupings, retain-undefined option | System | Accepted System ADR before dependent boundary text becomes authoritative |
| JCS-03 | Which information, if any, is JCS authoritative for? | Concrete domains, owners, producers, consumers, provenance, conflict, freshness, retention, recovery, and no-authority alternative | System; Foundational if project-wide authority changes | Accepted ADR and data-ownership review before collector dependency |
| JCS-04 | Who consumes JCS guarantees, and what remains owned elsewhere? | Collector and future-component needs, human/AI roles, coupling risks, no-dependency alternatives | System when a cross-component contract is established | Chief Architect review and maintainer decision in the specification gate |
| JCS-05 | Which conceptual interactions are required? | Meaning, validation, authorization, side effects, failure, compatibility, and alternatives including no direct interface | System for public or cross-component interfaces | Accepted ADR before interface requirements become binding |
| JCS-06 | What are JCS failure, stale-state, conflict, retry, and recovery guarantees? | Consequence analysis, partial failure, degraded modes, durability category, rebuild/restore expectations | System when it fixes subsystem guarantees; otherwise part of approved specification | Specification lifecycle review before acceptance |
| JCS-07 | Which trust, privacy, and human/AI authority boundaries apply? | Data classification, least privilege, unsafe-action cases, prompt/model exposure, no-action default | System; Foundational if human authority or project-wide security posture changes | Security and Chief Architect review before acceptance |
| JCS-08 | What must operators observe and own? | Health questions, degraded states, dependency failure, configuration, recovery, capacity, and retirement | System if it changes deployment or independently operated boundaries | Operations review before specification acceptance; mechanism deferred |
| JCS-09 | What evidence will prove a future implementation conforms? | Contract, failure, security, recovery, and acceptance scenarios; alternatives for untestable claims | Specification requirement; later tools may require Implementation ADRs | Test acceptance review before specification acceptance |
| JCS-10 | Which technology and deployment choices must remain deferred? | Identify whether each choice is necessary to the conceptual contract; compare deferral with premature selection | Later System or Implementation ADR as consequence requires | Explicit deferred-decision list; no selection in the definition specification unless indispensable and separately approved |

If one answer would decide several independent concerns, split the ADRs rather
than hiding multiple choices in a broad record. A Foundational classification
must be justified by project-wide consequence, not by the importance of the
JCS name.

## Implementation order and milestones

Specification work uses one short-lived branch from synchronized `main` and a
draft pull request. Commits remain small and coherent, but an incomplete
specification does not merge merely to create progress. Each milestone below
must satisfy its gate before dependent work begins.

### Milestone C0: approve this implementation plan

**Artifacts:**

- This complete plan
- Navigation and canonical ownership updates for the plan
- Sprint, status, and changelog integration

**Acceptance:**

- Every roadmap outcome maps to an artifact and gate.
- Evidence classes, owners, milestones, dependencies, risks, assumptions, and
  acceptance criteria are explicit.
- The plan selects no JCS answer or implementation technology.
- The Chief Architect reviews the actual changed artifacts and records an
  explicit decision.
- Final maintainer authority is recorded through the approved collaboration
  workflow.

**Gate:** No JCS specification file is created before C0 approval.

### Milestone C1: frame the definition and decisions

**Artifacts after C0 approval:**

- A complete first proposal of `docs/JCS_SPECIFICATION.md` covering evidence,
  name and purpose alternatives, scope, non-goals, responsibility alternatives,
  consumers, and the decision register
- Proposed numbered ADRs for decisions already known to meet a trigger

**Acceptance:**

- Every statement is labeled as verified, reported, assumed, open, or
  proposed where ambiguity matters.
- The proposal compares credible alternatives, including retaining the
  undefined state when it is a real option.
- Maintainer input is promoted as a proposed repository statement rather than
  left in conversation.
- The Chief Architect confirms the ADR levels and identifies blocking missing
  evidence before boundary choices are accepted.

**Gate:** Do not make information authority or interfaces binding until the
responsibility decision is accepted.

#### Permitted C1 outcome states

C1 discovery does not assume that JCS should advance. The framing review must
record exactly one proposed next-state recommendation:

| Outcome | Meaning | Required evidence and next gate |
| --- | --- | --- |
| Proceed toward specification | A candidate problem and responsibility are supported well enough to evaluate information and consumer boundaries. | Maintainer-reviewed purpose, named consumer/problem relationship, candidate responsibility, boundary evidence, and Chief Architect authorization for a bounded C2 scope; no JCS decision is accepted by this outcome. |
| Revise problem framing | The alternatives or evidence model are incomplete or biased. | Exact framing defect, owner, and revision criteria; remain in C1. |
| Defer JCS | No current evidence justifies investing in a component decision, but the preserved concept may be reconsidered after named evidence appears. | Deferral reason, triggering evidence, roadmap and sprint impact, and continued **Named** maturity; no dependent work. |
| Remove JCS | Evidence shows the named subsystem is unnecessary or harmful to the approved architecture. | Maintainer decision, Chief Architect review, ADR assessment, and consistent updates to roadmap, architecture, glossary, registry, status, sprint, and changelog. |

The no-JCS baseline remains credible through every later milestone until an
accepted decision establishes otherwise. An unresolved evidence gap remains
an architectural question with an owner and gate; it must not be relabeled as
ordinary backlog work merely to advance the milestone.

### Milestone C2: define information and consumer boundaries

**Artifacts:**

- JCS information-responsibility mappings in the proposed specification
- Consumer and dependency requirements
- Conceptual interaction requirements without protocol or schema
- Required System ADR updates or additions

**Acceptance:**

- Each concrete information domain has one proposed owner or remains an
  explicit blocking question.
- Authoritative, cached, derived, and temporary representations are not
  conflated.
- Provenance, time, freshness, conflict, retention, deletion, and recovery are
  addressed for any owned information.
- Collector dependency is described only against accepted conceptual
  guarantees.
- No reported product is treated as a data owner or interface by convenience.

**Gate:** Blocking authority or consumer ambiguity prevents acceptance of the
affected contract.

### Milestone C3: define lifecycle and assurance requirements

**Artifacts:**

- Failure, degraded-state, timeout, retry, partial-success, stale-state, and
  recovery requirements
- Security, privacy, trust, and human/AI authority requirements
- Configuration, health, observability, capacity, continuity, retirement, and
  support expectations
- Risk-based validation and future implementation acceptance scenarios

**Acceptance:**

- Reviewers can explain how JCS fails safely and what a consumer observes.
- Recovery expectations follow the information category and do not claim an
  untested mechanism.
- Least privilege, untrusted inputs, sensitive data, and action authority are
  explicit.
- Health signals answer owned operational questions without exposing private
  details.
- Acceptance scenarios cover success, invalid input, dependency loss,
  conflicts, stale state, partial failure, authorization denial, and recovery
  as applicable.

**Gate:** A guarantee that cannot be validated or owned must be narrowed,
deferred, or rejected before specification acceptance.

### Milestone C4: integrate canonical project memory

**Artifacts:**

- Final proposed JCS specification and accepted ADRs
- Consistent updates to the glossary, architecture, component registry, data
  ownership, documentation ownership, status, sprint, roadmap, and changelog
- Optional traceability or data-catalog artifacts only if approved content now
  satisfies their creation gates

**Acceptance:**

- One canonical owner exists for each shared concept.
- JCS relationships and maturity agree across every entry point.
- All local links resolve and repository validation passes.
- No document claims implementation or operational evidence.
- The actual complete artifact set receives Chief Architect review.

**Gate:** JCS remains **Named** until the complete specification and required
ADRs are approved.

### Milestone C5: accept the specification and close Phase 1

**Artifacts:**

- Recorded Chief Architect decision and recommendation dispositions
- Final maintainer acceptance
- Merged GitHub pull request with passing required checks
- Post-merge read-back of `main` and the required workflow

**Acceptance:**

- Every Phase 1 roadmap outcome is `Pass` or has a reviewed exception that
  does not make the contract unsafe or ambiguous.
- The component registry may advance JCS from **Named** to **Specified**.
- Collectors may plan against the approved conceptual contract.
- A later JCS or collector implementation still requires a separately approved
  plan, sprint scope, and any remaining ADRs.

**Gate:** Specification acceptance does not automatically authorize code,
schemas, infrastructure, or deployment.

## Review sequence

1. **Lead Engineer self-review:** Check scope, evidence labels, source
   traceability, canonical ownership, ADR triggers, and repository validation.
2. **Maintainer intent review:** Resolve questions that depend on project
   purpose or human authority. Promote the result into the proposed artifact.
3. **Chief Architect framing review:** Review C1 alternatives, responsibility
   boundaries, and ADR levels before dependent specification sections become
   binding.
4. **Domain reviews:** Apply data ownership, security, operations, recovery,
   testing, and AI collaboration policy to the actual proposed contract.
5. **Chief Architect final review:** Use the
   [review template](reviews/ARCHITECT_REVIEW_TEMPLATE.md) with the complete
   changed files or diff, validation, ADRs, and unresolved risks.
6. **Maintainer decision:** Exercise final project authority only after
   blocking revisions are resolved.
7. **Merge and read-back:** Merge the exact approved head, validate merged
   `main`, and record the next authorized work in canonical status.

A summary-only review, a review of stale files, or an approval without the
exact head is insufficient.

## Branch and commit strategy

After C0 approval:

1. Synchronize `main` and create a short-lived JCS specification branch.
2. Commit the evidence and decision framing separately from later accepted
   boundary edits.
3. Commit information and consumer boundaries as one coherent review unit.
4. Commit lifecycle, security, operations, and validation requirements as one
   coherent review unit.
5. Commit canonical navigation and lifecycle integration after the complete
   specification is internally consistent.
6. Rebase or update only through non-destructive project workflow; never hide
   unrelated work in the specification pull request.

The full branch remains a proposal until reviewed and merged. Commit order is
for reviewer clarity, not incremental authorization.

## Dependencies

| Dependency | Why it matters | Required before |
| --- | --- | --- |
| Approved C0 plan | Prevents specification work from inventing its own process or scope | Creating the JCS specification |
| Maintainer intent on name and problem | The repository cannot infer the meaning of `JCS` from bootstrap memory | Accepting JCS-01 |
| Accepted responsibility boundary | Data authority, consumers, and interfaces depend on coherent ownership | Accepting JCS-03 through JCS-05 |
| Concrete information-domain evidence | Authority and lifecycle cannot be assigned to vague "project data" | Accepting each affected information mapping |
| Security and privacy classification evidence | Access, retention, model exposure, and public documentation depend on consequence | Accepting sensitive data or action responsibilities |
| Required ADR decisions | Lasting boundaries cannot be established only in prose or review comments | Final specification acceptance |
| Passing repository checks and exact-artifact review | Prevents broken or stale project memory from becoming canonical | Every merge |

A sanitized infrastructure audit is not a prerequisite for deciding the
conceptual JCS purpose unless a proposed guarantee genuinely depends on a
verified operational constraint. Deployment-specific claims remain deferred
until that audit exists.

## Risks and responses

| Risk | Consequence | Response and owner |
| --- | --- | --- |
| The acronym biases the design before its purpose is known. | The project rationalizes a name instead of solving a real problem. | Compare retain, expand, rename, and defer alternatives under JCS-01; maintainer and Chief Architect own the decision. |
| JCS becomes a catch-all "core." | Responsibility, failure, security, and ownership become unbounded. | Require one coherent responsibility, explicit non-goals, named consumers, and a System ADR. |
| JCS silently becomes authoritative for all project data. | Conflicts, retention, recovery, and downstream actions become unsafe. | Require concrete domain-by-domain mappings and preserve the no-authority alternative. |
| Reported infrastructure drives architecture. | Unverified products and constraints become permanent coupling. | Keep reports separate; defer technology and deployment; require a sanitized audit for operational claims. |
| Conceptual interface requirements become a disguised API design. | Protocol, schema, and compatibility choices are made without evidence. | Specify meaning and failure only; route syntax and technology through later ADRs. |
| The plan produces many empty artifacts. | Navigation and ownership degrade while apparent progress increases. | Create only the specification and triggered ADRs; apply explicit gates to catalogs, indexes, schemas, tests, and runbooks. |
| Approval language is mistaken for implementation authorization. | Code or collector work starts before architecture is stable. | Repeat the maturity boundary in the plan, sprint, status, PR, and final review record. |
| Specification claims cannot be tested. | Future implementation cannot demonstrate conformance. | Require acceptance scenarios and narrow or defer unverifiable guarantees. |
| Human, AI, information, and action authority are conflated. | A fact, model output, or component grants itself unsafe control. | Review authority types separately under JCS-03 and JCS-07; preserve human approval defaults. |
| Review occurs against a summary or stale head. | Canonical decisions differ from approved evidence. | Require exact files or diff, exact head, passing checks, and recorded recommendation dispositions. |

## Validation strategy

### Plan validation

- Run `python scripts/validate_docs.py`.
- Run `python -m py_compile scripts/validate_docs.py`.
- Run `git diff --check`.
- Run `git fsck --no-dangling`.
- Inspect every changed file and canonical link.
- Confirm no secret, personal, or private operational information is present.
- Confirm the plan contains no JCS expansion, responsibility selection,
  information assignment, interface, schema, or technology choice.

### Future specification validation

The specification review must demonstrate:

- Traceability from every roadmap outcome to specification text and evidence
- Closure or explicit blocking disposition for every decision-register item
- Accepted ADRs for every triggered lasting choice
- Complete registry fields required for **Specified** maturity
- Consistency across glossary, architecture, data ownership, security,
  operations, testing, status, sprint, roadmap, and changelog
- Representative acceptance scenarios for behavior, failure, security,
  recovery, and consumer dependence
- Passing local and required GitHub repository checks
- Chief Architect approval of the exact complete artifact set

No runtime test, benchmark, or operational claim may be fabricated to satisfy
a documentation gate.

## Completion criteria for this plan

This plan is complete when:

- Its scope, non-goals, evidence, assumptions, and open questions are explicit.
- Every required Phase 1 outcome has an owner, artifact, milestone, and review
  gate.
- The evidence and maturity classes prevent specification, implementation, and
  operational claims from being conflated.
- ADR candidates are identified without selecting their answers.
- Risks, dependencies, validation, and recommendation dispositions are
  actionable.
- Documentation ownership and navigation identify this plan as the current
  execution source.
- The Chief Architect approves the exact artifacts and final head.
- The approved plan is merged to reviewed `main` with its required check
  passing.

After those conditions are met, Milestone C1 may begin. The next deliverable is
a proposed JCS specification and any required proposed ADRs, not code.

### Completion evidence

- Chief Architect decision: **APPROVED TO MERGE** for exact head
  `53504ba7865e02235b3ddcf5228b40ca972b7d68`, recorded on pull request #16
- Merge: pull request #16 at
  `b785bbc71421da84568f2d2be00d877d4e67bdb6`
- Required merged-`main` check: `documentation-quality` passed in GitHub
  Actions run `30634584406`, job `91168847689`, with no annotations
- Authorized next work: Milestone C1 proposed specification and proposed ADRs
  only; no accepted JCS answer, schema, interface, collector dependency,
  runtime architecture, infrastructure selection, or implementation

## Change control and handoff

Update this plan when approved scope, sequence, ownership, decision gates,
dependencies, risks, or acceptance evidence changes. A change that alters the
project-wide roadmap, architecture principles, or decision authority requires
the corresponding canonical update and ADR assessment.

At every handoff, report:

- Exact branch, head, base, and changed artifacts
- Current milestone and authorized next action
- Verified facts, assumptions, open questions, and blockers
- Validation commands and exact results
- ADR status and pending decisions
- Review decision and every recommendation disposition

Do not leave an accepted JCS conclusion only in conversation or a pull-request
summary. Promote it to the correct canonical owner before dependent work.
