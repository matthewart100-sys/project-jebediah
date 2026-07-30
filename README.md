# Project Jebediah

Project Jebediah is a local-first AI platform initiative focused on
transparency, recoverability, modularity, deterministic behavior where
practical, and long-term maintainability.

The project is currently in **Project Genesis (Phase 0)**. This phase creates
the documentation, standards, decision framework, and contribution process
that must exist before application or infrastructure implementation begins.
There is no Project Jebediah application code in this repository yet.

## Source of truth

The default branch of this GitHub repository is the authoritative project
record. Prior chats, the onboarding ZIP, and the Genesis PDFs were bootstrap
inputs only. Their durable requirements are being incorporated into reviewed,
version-controlled Markdown.

When repository documents disagree, contributors must stop dependent work and
resolve the inconsistency in GitHub. Conversation history must not be used to
fill gaps silently.

## Start here

AI contributors begin with [AGENTS.md](AGENTS.md). Codex also follows the
tool-specific operating checklist in
[CODEX_BOOTSTRAP.md](CODEX_BOOTSTRAP.md).

1. Read the [mission and manifesto](docs/MISSION_AND_MANIFESTO.md).
2. Review the [current project status](PROJECT_STATUS.md).
3. Read the [current sprint](CURRENT_SPRINT.md) and [roadmap](ROADMAP.md).
4. Use the [documentation index](docs/README.md) to find canonical guidance.
5. Read the [contribution guide](CONTRIBUTING.md) before changing the
   repository.
6. Read the approved [Project Genesis implementation plan](docs/genesis/PROJECT_GENESIS_PLAN.md).
7. Review the [changelog](CHANGELOG.md) for repository history.

Additional architecture, security, operations, and release documents will be
delivered through the reviewable milestones defined in the Genesis plan. A
document is added only when it contains substantive guidance; empty
placeholders are not accepted.

## Preserved design intent

The bootstrap requirements establish a reported deployment context consisting
of a Dell PowerEdge R420, Proxmox, an Ubuntu virtual machine, Docker, n8n,
Qdrant, and Ollama. These details are **reported facts**, not independently
verified infrastructure inventory.

The intended platform layers are:

1. Infrastructure
2. Services
3. Automation
4. Knowledge
5. Reasoning
6. User experience

Named future subsystems include JCS, a Collector Engine, a Knowledge Graph, a
Digital Twin, automation, and a Reasoning Engine. Their names preserve design
intent; they do not imply that interfaces, protocols, schemas, or
implementation technologies have been approved.

The required roadmap order is:

**Foundation -> Documentation -> JCS definition -> Collectors -> Knowledge
Graph -> Digital Twin -> Automation -> Reasoning Engine -> Production
Platform**

## Current contribution gate

Project Genesis is documentation and governance work only. All changes must be
made on short-lived feature branches, reviewed through pull requests, and
delivered in small, understandable commits. No application implementation may
begin until the relevant architecture and decision records have been approved.

The [Git workflow](docs/GIT_WORKFLOW.md) defines the branch and review
lifecycle. The [Definition of Done](docs/DEFINITION_OF_DONE.md) applies to
every change.
