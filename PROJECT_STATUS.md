# Project Status

**Phase:** Phase 2: Collector and memory foundation

**Status:** Sprint 004 merged; Sprint 005 implementation validation blocked;
deployment unverified

**Last reviewed:** 2026-08-01

## Summary

Project Jebediah has established its permanent engineering memory and
repository quality controls in GitHub. The Project Genesis foundation is
published as `v0.1.0`. The repository now contains a Python Collector package,
unit tests, and a Dockerized semantic memory service using FastAPI, Ollama, and
Qdrant adapter boundaries.

Milestone C1 found no evidence-supported JCS purpose, responsibility, consumer,
or boundary. Pull request #18 therefore merged the **DEFER JCS** outcome at
`5895e8f5896cf0687a43c978ec2f17da53d6b78c`. JCS remains **Named**, its
specification remains **Proposed**, and Collector work has no JCS dependency.

Sprint 003 added memory consolidation, an intelligence governor, confidence
and retention scoring, metadata enrichment, Qdrant persistence, and semantic
retrieval. Sprint 004 merged additive provenance, lifecycle, and
retrieval-ranking foundations. Sprint 005 architecture is accepted and its
bounded repository implementation has consolidated the duplicate memory,
Qdrant, and embedding paths while preserving Sprint 004 behavior. Repository
implementation is verified by source and tests. A clean locked wheel/import
smoke passes. Quality Control corrections now canonicalize Ollama's bare API
digest, reverify model identity for every embedding, and reject post-scan
Qdrant identity or vector drift before semantic candidates are returned. The
complete 142-test suite passes, but the mandatory container build remains
unverified because no container runtime is available. Deployment and
live-service operation are not verified.

The initial GitHub baseline was commit
`e42edd0c67e144b556adb77416a1e079eb106b93`, which contained only a one-line
`README.md`. Project Genesis work proceeded from that baseline through
reviewed pull requests.

## Verified facts

- The authoritative repository is
  `matthewart100-sys/project-jebediah`.
- The default branch is `main`.
- The repository is public.
- Project Genesis Phase 0 is complete.
- The repository contains a Python Collector package, a memory-service source
  tree, Docker service artifacts, and automated tests.
- The untouched Sprint 004 baseline passed 53 unit tests with `pytest`; the
  Sprint 004 implementation expands the suite to 66 passing tests.
- The corrected uncommitted Sprint 005 candidate passes 142 tests, including
  model-digest drift and post-scan Qdrant compatibility regressions.
- Sprint 004 merged into `main` at
  `ea0b5f8d0dc829dd9722850ef6940abda0bcdb60`.
- Repository evidence does not verify that the service is deployed or that
  live Qdrant, Ollama, n8n, or home-lab state matches the tracked candidate.
- The first Genesis source-of-truth checkpoint was approved by the Chief
  Architect and merged through pull request #1.
- Genesis Sprint 1 established the planning, contribution, repository,
  engineering, and documentation methodology through approved pull requests
  #2 and #3.
- Milestone 3 established AI onboarding, collaboration, and durable memory
  through approved pull request #4.
- Milestone 4A established architecture principles, current conceptual
  architecture, terminology, component ownership, and ADR governance through
  approved pull request #5.
- Milestone 4B established information ownership and the Digital Twin position
  through approved pull request #6.
- Milestone 5A established testing and security governance through approved
  pull request #7.
- Milestone 5B established operations, release, and repository-hygiene
  governance through approved pull request #8.
- Milestone 6A established structured contribution intake and executable
  documentation-quality enforcement through approved pull request #9.
- The `documentation-quality` workflow succeeded on merged `main` at commit
  `76470977988e95c99f1667e74312d22dc8befe9b`.
- The complete Project Genesis topic, consistency, and clean-room audit was
  approved by the Chief Architect and merged through pull request #11 at
  commit `5c92b5920341c954e51452ff8760ea4aaef3e5bc`.
- The `documentation-quality` workflow succeeded on that merged audit commit
  in GitHub Actions run `30597270334`.
- Pull request #12 finalized the release candidate and merged at
  `978fa7f0ad855986e6bef39b373b6d9e5a9def53`.
- GitHub Actions run `30597710090` succeeded on that exact merged release
  commit.
- Annotated tag `v0.1.0` has tag object
  `c564b4d32c9869aaa21d4c5c7bc6809450a182f1` and targets
  `978fa7f0ad855986e6bef39b373b6d9e5a9def53`.
- The non-draft, non-prerelease
  [`v0.1.0` engineering-foundation release](https://github.com/matthewart100-sys/project-jebediah/releases/tag/v0.1.0)
  was published at `2026-07-31T02:00:05Z` with the reviewed notes and no
  attached artifacts.
- Official `actions/checkout` release `v7.0.1` uses Node 24 at verified commit
  `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- Pull request #14 updated only that immutable pin and merged at
  `901764375d7a81f99f1ce9ccfd7f2c25a0fcf349`.
- GitHub Actions run `30598348588` succeeded on that exact `main` commit with
  no check annotations; branch protection still requires the same strict
  `documentation-quality` context and its prior controls.
- Pull request #15 recorded that verification, closed the workflow-maintenance
  checkpoint, and merged at
  `4086a6c8195226ef237bfa11d6fac0e9fa4edfff`.
- GitHub Actions run `30633931649` succeeded on that exact `main` commit with
  no annotations; branch protection read-back remained unchanged.
- Pull request #16 added the complete JCS definition implementation plan,
  received Chief Architect approval at exact head
  `53504ba7865e02235b3ddcf5228b40ca972b7d68`, and merged at
  `b785bbc71421da84568f2d2be00d877d4e67bdb6`.
- GitHub Actions run `30634584406` succeeded on that exact `main` commit with
  no annotations. The approved plan authorizes only a proposed JCS
  specification and proposed ADRs under Milestone C1.
- Pull request #17 activated the approved plan, closed Phase 1 Sprint 1, and
  opened the C1 framing sprint at merged commit
  `13756d97081e45684564accb666703845017800d`.
- GitHub Actions run `30635006984` succeeded on that exact `main` commit with
  no annotations.
- Draft pull request #18 contains the first proposed JCS framing artifact at
  `5dea1aea6e8b264b74c05b063157f72e863fff54`; its required check passed in run
  `30635469490`. The Chief Architect approved continued C1 work without merge,
  kept C2 blocked, and identified missing maintainer purpose, consumer,
  boundary, and failure-consequence evidence.
- Pull request #19 made the four permitted C1 outcomes, no-JCS baseline,
  evidence-gap treatment, and outcome-record requirements canonical at merged
  commit `2b8e1a318062ce7e5f029cd32521bc655db87712`.
- GitHub Actions run `30636066645` succeeded on that exact `main` commit with
  no annotations.
- Pull request #18 merged the reviewed **DEFER JCS** outcome at
  `5895e8f5896cf0687a43c978ec2f17da53d6b78c`, closing Milestone C1 while
  keeping JCS **Named**, its specification **Proposed**, C2 blocked, and
  implementation unauthorized.
- GitHub API read-back on 2026-07-30 confirms that private vulnerability
  reporting is enabled.
- GitHub API read-back on 2026-07-30 confirms that `main` requires pull
  requests, strict success of `documentation-quality`, and conversation
  resolution; blocks force pushes and deletion; requires zero approving
  reviews; and does not enforce restrictions on administrators.
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
- Phase 0 selected no application language, framework, API protocol, data
  schema, or deployment mechanism.
- Development releases use the approved `0.x` semantic-versioning range.

## Open questions

| Question | Why it matters | Resolution gate |
| --- | --- | --- |
| What does JCS stand for, own, and guarantee? | Collectors and later knowledge components must not depend on an undefined contract. | Deferred after C1; reconsider only when an explicit purpose, named consumer and need, candidate responsibility and boundary, and failure consequence are available for review. |
| Which reported infrastructure components are currently running and how are they configured? | Architecture and operations documents must distinguish desired state from actual state. | Perform a sanitized infrastructure inventory. |
| Which future component owns each concrete information item? | Categories and responsibilities are defined, but JCS and other components remain unspecified. | Map authority in the relevant component specifications before implementation. |
| What data classifications and privacy constraints apply? | A public repository and local AI platform create disclosure and retention risks. | Complete data classification and threat-model work before ingesting data. |
| Which software license should govern the public repository? | Public visibility does not grant reuse rights. | Maintainer selects a license before inviting external reuse. |
| What bounded subject and use case should the first Digital Twin support? | The conceptual position and exclusions are defined, but an implementation scope is not. | Approve a future Digital Twin specification after its entry gates are met. |

## Current work

The active
[Sprint 005 Implementation Plan](docs/SPRINT_005_IMPLEMENTATION_PLAN.md)
implements the accepted architecture consolidation without deployment.

The current review must verify:

- The canonical memory-domain dependency direction is implemented without a
  service-local shadow package.
- Qdrant option A is implemented behind one canonical adapter.
- The accepted embedding model identity and compatibility contract is
  enforced.
- Keep Sprint 004 provenance, lifecycle, verification, API, and semantic-only
  ranking behavior unchanged.
- Separate compatible legacy payload reading from incompatible vector
  geometry migration.
- No accepted compatibility or validation gate failed.
- Keep deployment and live-data changes outside Sprint 005.

JCS remains deferred. The Collector and memory service do not depend on JCS,
and Sprint 005 does not reopen JCS C1 or authorize JCS C2.

## Phase 0 completion evidence

Phase 0 demonstrated that a new engineer or AI can use this repository alone
to explain:

- The mission, principles, current state, and roadmap
- Verified facts, reported facts, assumptions, and open questions
- The intended platform layers and named subsystems
- The architectural decision process
- Contribution, Git, sprint, testing, security, operations, and release rules
- The AI collaboration and memory contract
- The universal Definition of Done

The repository passed its documentation-quality checks and two independent
clean-room reviews before the foundation was tagged. The release checklist
records the exact publication evidence.

## Maintenance rule

Every pull request that changes project reality must update this file when its
statements would otherwise become inaccurate. Status claims must be supported
by repository evidence or labeled as reported or assumed.
