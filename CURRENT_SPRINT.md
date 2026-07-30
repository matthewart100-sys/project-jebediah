# Current Sprint

## Genesis Sprint 2: AI Onboarding and Memory

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Make GitHub sufficient for a new AI contributor to orient, collaborate, act
within authority, and preserve durable project memory without bootstrap files
or prior chat history.

## Context

Genesis Sprint 1 established the working methodology through pull requests #2
and #3. This sprint applies that methodology to the human-and-AI engineering
model described by the bootstrap requirements.

The two-week window is a planning default, not permission to sacrifice quality.
The sprint closes when its accepted outcomes are complete or when remaining
work is explicitly carried forward.

## Committed scope

- Tool-agnostic AI onboarding in `AGENTS.md`
- Codex Lead Engineer operations in `CODEX_BOOTSTRAP.md`
- Role, authority, review, and handoff rules in `.ai/COLLABORATION.md`
- Durable memory layers and promotion rules in
  `docs/AI_MEMORY_CONTRACT.md`
- Canonical navigation, ownership, status, plan, and changelog updates
- Durable ownership for accepted Chief Architect follow-up recommendations

## Non-goals

- Application or infrastructure implementation
- Architecture, ADR, JCS, collector, or Digital Twin design
- Data ownership decisions
- API, schema, protocol, language, or framework selection
- Deployment changes to the reported home-lab environment
- GitHub Actions enforcement, which belongs to a later Genesis milestone
- License selection, which requires a maintainer decision

## Acceptance criteria

- A new AI can reconstruct project context from the repository alone.
- Tool-agnostic rules and Codex-specific operations have distinct owners.
- Human maintainer, Chief Architect, Lead Engineer, and future-agent
  responsibilities are explicit.
- Durable information has a defined promotion path into reviewed GitHub
  artifacts.
- AI guidance links to existing standards and the Definition of Done instead
  of creating weaker copies.
- The Chief Architect receives the exact artifacts and records an explicit
  decision.
- Status, navigation, ownership, plan, and changelog remain consistent.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Genesis source-of-truth checkpoint | Complete | Pull request #1 merged into `main` |
| Checkpoint A: planning and contribution workflow | Complete | Pull request #2 approved by the Chief Architect and merged |
| Checkpoint B: engineering documentation standards | Complete | Pull request #3 approved by the Chief Architect and merged |
| Genesis Sprint 1 | Complete | Both working-methodology checkpoints accepted |
| Milestone 3: AI onboarding and memory | In progress | Bounded Sprint 2 feature branch |
| Milestone 4: architecture and information boundaries | Pending | Starts after Sprint 2 is accepted |

## Dependencies

- Authoritative `main` remains synchronized with reviewed pull requests.
- Chief Architect review receives the exact changed files or diff.
- The maintainer retains final repository authority.
- Unknown architecture remains explicitly deferred.

## Risks

| Risk | Response |
| --- | --- |
| Tool-specific behavior leaks into universal guidance | Keep Codex operations in `CODEX_BOOTSTRAP.md` and shared invariants in `AGENTS.md`. |
| AI guidance duplicates existing policy | Assign one owner per concept and link to standards and the Definition of Done. |
| Chat decisions remain ephemeral | Promote decisions and recommendations through the AI memory contract. |
| Role language implies AI authority | Keep final maintainer authority and formal architecture review boundaries explicit. |
| Reviews rely on summaries | Require actual artifacts in the Chief Architect evidence package. |

## Update rule

Update this file when sprint scope, status, dependencies, or risk changes. At
sprint close:

1. Record completed outcomes in the changelog and project status.
2. Move unfinished work deliberately; do not erase it.
3. Capture process improvements.
4. Define the next sprint before beginning unscheduled implementation.
