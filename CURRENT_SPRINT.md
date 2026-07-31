# Current Sprint

## Genesis Sprint 4: Lifecycle Philosophies

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Define how Project Jebediah will validate, secure, operate, recover, and release
future capabilities before implementation begins.

## Context

Pull requests #5 and #6 completed architecture and information boundaries.
Future subsystem work now needs lifecycle expectations that translate those
boundaries into evidence, protection, operation, recovery, and release gates.

The two-week window is a planning default. Each checkpoint requires
substantive guidance and evidence-based review.

## Committed scope

### Checkpoint A: Testing and security

- Risk-based, technology-neutral testing philosophy
- Deterministic, component, contract, integration, end-to-end, recovery,
  security, and documentation evidence
- AI and probabilistic evaluation
- Safe vulnerability reporting for the currently verified GitHub state
- Public-repository, trust, secret, data, AI, supply-chain, incident, and
  review boundaries

### Checkpoint B: Operations, release, and repository hygiene

- Operations, health, observability, backup, restore, rollback, runbook, and
  incident philosophy
- Pre-1.0 versioning, release readiness, tagging, notes, artifacts, deployment,
  verification, rollback, and deprecation
- `.editorconfig`, `.gitattributes`, and `.gitignore`
- Canonical integration and Sprint 4 closure

Each checkpoint is a separate pull request and Chief Architect review.

## Non-goals

- Application or infrastructure implementation
- Home-lab reconfiguration, audit, penetration test, or incident simulation
- Selection of language, test framework, scanner, secret manager, monitoring
  stack, deployment tool, or artifact registry
- GitHub Actions and branch-protection enforcement, which belong to Milestone 6
- Enabling GitHub private vulnerability reporting before the security policy
  and Milestone 6 configuration are reviewed
- Creating a release before all Phase 0 exit criteria pass

## Acceptance criteria

- Test selection follows risk and owned boundaries rather than a universal
  coverage number.
- Deterministic and probabilistic behavior have appropriate distinct evidence.
- Failure, recovery, security, data, workflow, AI, and documentation testing
  are covered.
- Vulnerability reporting is safe and accurate for the verified current
  GitHub configuration.
- Security guidance covers the full lifecycle without exposing or inventing
  private infrastructure.
- Operations and release guidance defines readiness, recovery, and ownership
  without selecting tools.
- Repository hygiene configuration is minimal, explained, and consistent.
- Exact artifacts receive explicit Chief Architect decisions.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Milestone 4A: architecture and decision governance | Complete | Pull request #5 approved by the Chief Architect and merged |
| Milestone 4B: information and Digital Twin boundaries | Complete | Pull request #6 approved by the Chief Architect and merged |
| Checkpoint A: testing and security | Complete | Pull request #7 approved by the Chief Architect and merged |
| Checkpoint B: operations, release, and repository hygiene | In progress | Bounded Sprint 4 feature branch |
| Milestone 6: GitHub enforcement | Pending | Starts after Sprint 4 closes |

## Dependencies

- Current architecture, data ownership, and ADR governance remain
  authoritative.
- The security policy reports actual repository capability rather than desired
  settings.
- Operations and release work builds on accepted testing and security gates.
- Chief Architect review receives exact artifacts and validation.

## Risks

| Risk | Response |
| --- | --- |
| Testing policy selects tools prematurely | Define evidence types and risk, leaving framework choice to component architecture. |
| Security reporting invents a private channel | Record verified GitHub capability and a no-detail interim contact request. |
| Security policy claims controls that do not exist | Separate current maturity and known gaps from future requirements. |
| Testing becomes a coverage-number exercise | Prohibit a universal threshold and require risk-based assertions. |
| Operations promises unverified recovery | Require restore evidence before calling a backup usable. |
| Release process permits an incomplete foundation release | Keep `v0.1.0` behind all Genesis exit and review gates. |

## Update rule

Update this file when sprint scope, status, dependencies, or risk changes. At
sprint close:

1. Record completed outcomes in the changelog and project status.
2. Move unfinished work deliberately; do not erase it.
3. Capture process improvements and accepted recommendations.
4. Define the next sprint before beginning unscheduled implementation.
