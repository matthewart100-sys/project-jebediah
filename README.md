# Project Jebediah

Project Jebediah is a local-first AI platform initiative focused on
transparency, recoverability, modularity, deterministic behavior where
practical, and long-term maintainability.

The **Project Genesis (Phase 0)** engineering foundation is complete and
published as [`v0.1.0`](https://github.com/matthewart100-sys/project-jebediah/releases/tag/v0.1.0).
JCS definition was deferred after Milestone C1. The repository now contains a
bounded Collector and semantic memory implementation; its deployment and live
home-lab operation remain unverified.

## Source of truth

The default branch of this GitHub repository is the authoritative project
record. Prior chats, the onboarding ZIP, and the Genesis PDFs were bootstrap
inputs only. Their durable Phase 0 requirements were incorporated into
reviewed, version-controlled Markdown.

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
4. Understand the [architecture principles](docs/ARCHITECTURE_PRINCIPLES.md)
   and [current conceptual architecture](docs/ARCHITECTURE.md).
5. Apply [data ownership](docs/DATA_OWNERSHIP.md) to information-bearing work.
6. Use the [documentation index](docs/README.md) to find canonical guidance.
7. Follow the
   [Project Coordination Protocol](docs/governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
   for role authority, review gates, handoffs, and evidence labels.
8. Read the [contribution guide](CONTRIBUTING.md) before changing the
   repository.
9. Read the approved [Project Genesis implementation plan](docs/genesis/PROJECT_GENESIS_PLAN.md).
10. Review the [changelog](CHANGELOG.md) for repository history.

GitHub enforcement is active and verified. The clean-room Phase 0 audit passed
through pull request #11, the release candidate passed through pull request
#12, and the immutable `v0.1.0` engineering-foundation release is published.
A document is added only when it contains substantive guidance; empty
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

[Knowledge Manager 1.0 Phase 1](CURRENT_SPRINT.md) is complete. Pull request #49
merged the validated metadata-only Knowledge Registry library at
`4ed2ac283e4df6aec30b67f7c4aa50338924c435`; the
[Phase 1 closeout](docs/KNOWLEDGE_MANAGER_1_PHASE_1_CLOSEOUT.md) records the
post-merge evidence and exclusions.

No active implementation sprint is authorized. Ingestion, external
information, memory integration, embeddings, Qdrant writes, services,
deployment, document uploads, and autonomous promotion remain excluded. JCS
remains deferred and is not a dependency. All changes use short-lived branches,
pull-request review, and small, understandable commits.

The permanent plan-to-closeout role sequence is defined by the
[Project Coordination Protocol](docs/governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md).
The protocol does not authorize Sprint 006, deployment, or live-system work.

The [Git workflow](docs/GIT_WORKFLOW.md) defines the branch and review
lifecycle. The [Definition of Done](docs/DEFINITION_OF_DONE.md) applies to
every change. Run `python scripts/validate_docs.py` before committing and
report the result in the pull request.
