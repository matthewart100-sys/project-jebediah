# Current Sprint

## Genesis Sprint 3: Architecture and Information Boundaries

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Preserve Project Jebediah's conceptual design intent, establish a formal
decision process, and define information boundaries without inventing
implementation architecture.

## Context

Pull request #4 completed AI onboarding and durable memory. The repository can
now orient future contributors and promote decisions safely. This sprint uses
that foundation to describe the current conceptual architecture and the gates
that must precede JCS, collectors, data use, and the Digital Twin.

The two-week window is a planning default. Evidence quality and architectural
review determine completion.

## Committed scope

### Checkpoint A: Architecture and decision governance

- Architecture principles
- Current conceptual architecture
- Shared glossary
- Component registry with component ownership distinct from repository
  ownership
- Foundational, System, and Implementation ADR process and template
- Accepted interface, Git, memory, and terminology cross-references

### Checkpoint B: Information and Digital Twin boundaries

- Authoritative, cached, derived, and temporary information categories
- Ownership, provenance, freshness, retention, and conflict expectations
- Digital Twin purpose, exclusions, conceptual relationships, and deferrals
- Architecture, glossary, registry, status, and navigation updates

Each checkpoint is a separate pull request and Chief Architect review.

## Non-goals

- Application or infrastructure implementation
- Verification or reconfiguration of the reported home lab
- Definition or implementation of JCS
- Collector, Knowledge Graph, Automation, or Reasoning Engine design
- API, schema, protocol, language, framework, database, model, or deployment
  selection
- Assigning reported products to permanent component responsibilities

## Acceptance criteria

- Architecture documents use verified facts, reported facts, working
  assumptions, and open questions correctly.
- Principles constrain decisions without selecting technology.
- Current architecture explains context, layers, boundaries, named future
  subsystems, and deliberate unknowns.
- The glossary owns shared terms without creating architecture.
- The component registry distinguishes component ownership from
  repository-path ownership and does not claim reported products are verified.
- ADR triggers, levels, lifecycle, evidence, supersession, and documentation
  coupling are actionable.
- Checkpoint B establishes information and Digital Twin boundaries before
  Phase 1 design.
- Exact artifacts receive explicit Chief Architect decisions.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Milestone 3: AI onboarding and memory | Complete | Pull request #4 approved by the Chief Architect and merged |
| Checkpoint A: architecture and decision governance | Complete | Pull request #5 approved by the Chief Architect and merged |
| Checkpoint B: information and Digital Twin boundaries | In progress | Bounded Sprint 3 feature branch |
| Milestone 5: lifecycle philosophies | Pending | Starts after Sprint 3 closes |

## Dependencies

- The approved mission, roadmap, standards, and AI memory contract remain
  authoritative.
- Chief Architect review receives exact artifacts and validation.
- Data ownership and Digital Twin work builds on accepted Checkpoint A terms.
- JCS remains undefined until Phase 1.

## Risks

| Risk | Response |
| --- | --- |
| Reported infrastructure is presented as verified | Label every reported product and require a sanitized audit. |
| Named subsystems acquire invented contracts | Record only preserved intent, current gate, and unresolved responsibility. |
| Principles become slogans | Give each principle an architectural consequence and application rule. |
| ADRs become bureaucracy | Trigger them only for lasting decisions with material consequences. |
| Registry ownership conflicts with repository ownership | Define component lifecycle ownership separately and link to repository standards. |
| Data or Digital Twin detail leaks into Checkpoint A | Defer their categorical definitions to Checkpoint B. |

## Update rule

Update this file when sprint scope, status, dependencies, or risk changes. At
sprint close:

1. Record completed outcomes in the changelog and project status.
2. Move unfinished work deliberately; do not erase it.
3. Capture process improvements and accepted recommendations.
4. Define the next sprint before beginning unscheduled implementation.
