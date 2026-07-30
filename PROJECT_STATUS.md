# Project Status

**Phase:** Project Genesis (Phase 0)

**Status:** Engineering foundation in progress

**Last reviewed:** 2026-07-30

## Summary

Project Jebediah is establishing its permanent engineering memory in GitHub
before implementing software. The repository currently contains foundational
documentation only. There are no application services, infrastructure
definitions, schemas, workflows, or tests yet.

The initial GitHub baseline was commit
`e42edd0c67e144b556adb77416a1e079eb106b93`, which contained only a one-line
`README.md`. Project Genesis work begins from that baseline on feature branches
and is reviewed through pull requests.

## Verified facts

- The authoritative repository is
  `matthewart100-sys/project-jebediah`.
- The default branch is `main`.
- The repository is public.
- Project Genesis is the active phase.
- No Project Jebediah application code has been implemented in this
  repository.
- The first Genesis source-of-truth checkpoint was approved by the Chief
  Architect and merged through pull request #1.
- The onboarding ZIP, PDFs, and prior conversations are not authoritative
  project memory.

## Reported facts

The bootstrap materials report the following operating environment:

- Dell PowerEdge R420
- Proxmox host
- Ubuntu virtual machine
- Docker
- n8n
- Qdrant
- Ollama

These claims require an infrastructure audit before they can be promoted to
verified facts. Public documentation must not expose credentials, private
addresses, sensitive topology, or personal data during that audit.

## Working assumptions

- GitHub will remain the canonical project record.
- The repository will remain public unless the maintainer records a different
  decision.
- The project currently has one maintainer.
- Canonical documentation will use English UTF-8 Markdown.
- Diagrams will be stored as text, using Mermaid where practical.
- Phase 0 will not select an application language, framework, API protocol,
  data schema, or deployment mechanism.
- Development releases will use the `0.x` semantic-versioning range once the
  release process is approved.

## Open questions

| Question | Why it matters | Resolution gate |
| --- | --- | --- |
| What does JCS stand for, own, and guarantee? | Collectors and later knowledge components must not depend on an undefined contract. | Resolve through a Phase 1 specification before implementation. |
| Which reported infrastructure components are currently running and how are they configured? | Architecture and operations documents must distinguish desired state from actual state. | Perform a sanitized infrastructure inventory. |
| What information is authoritative, cached, derived, or temporary? | JCS, collectors, and the Digital Twin need explicit data ownership. | Approve the planned data ownership document before system design. |
| What data classifications and privacy constraints apply? | A public repository and local AI platform create disclosure and retention risks. | Complete data classification and threat-model work before ingesting data. |
| Which software license should govern the public repository? | Public visibility does not grant reuse rights. | Maintainer selects a license before inviting external reuse. |
| What does the Digital Twin represent and explicitly exclude? | The term must not accumulate incompatible meanings. | Approve the planned Digital Twin position paper before implementation. |

## Current work

Genesis Sprint 1 is establishing the working methodology in two bounded
checkpoints:

- Planning and contribution workflow: contribution guide, Git workflow, sprint
  process, current sprint, roadmap, Definition of Done, and Chief Architect
  review template
- Engineering documentation standards: repository, engineering, and
  documentation standards

Later milestones will add AI collaboration and memory contracts, architecture
and ADR guidance, data ownership, the Digital Twin position paper, lifecycle
philosophies, GitHub quality enforcement, and the Phase 0 release audit.

## Phase 0 exit criteria

Phase 0 is complete only when a new engineer or AI can use this repository
alone to explain:

- The mission, principles, current state, and roadmap
- Verified facts, reported facts, assumptions, and open questions
- The intended platform layers and named subsystems
- The architectural decision process
- Contribution, Git, sprint, testing, security, operations, and release rules
- The AI collaboration and memory contract
- The universal Definition of Done

The repository must pass its documentation quality checks and a clean-room
onboarding review before the foundation is tagged for release.

## Maintenance rule

Every pull request that changes project reality must update this file when its
statements would otherwise become inaccurate. Status claims must be supported
by repository evidence or labeled as reported or assumed.
