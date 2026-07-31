# Current Sprint

## Genesis Sprint 6: Genesis Audit and Foundation Release

**Target window:** 2026-07-30 through 2026-08-12

**Status:** In progress

## Sprint goal

Demonstrate that a new engineer or AI can clone Project Jebediah, understand
its mission, current reality, architecture, standards, and contribution
process from GitHub alone, then publish the reviewed foundation as `v0.1.0`.

## Context

Project Genesis Milestones 0 through 6 have established the source of truth,
working methodology, AI collaboration and memory, architecture and
information boundaries, lifecycle philosophies, repository validation, safe
security reporting, and proportionate `main` protection.

The final milestone must test the foundation as a coherent system of
documentation. Passing individual pull requests is necessary but does not
prove that the combined repository is complete, consistent, discoverable, or
usable by a fresh reader.

## Committed scope

### Checkpoint A: Foundation audit

- Map every required Project Genesis topic to its canonical substantive
  document.
- Audit cross-document status, ownership, terminology, links, evidence
  categories, and roadmap consistency.
- Run all automated repository checks on reviewed `main`.
- Review the repository tree for placeholders, duplicated policy, bootstrap
  artifacts, sensitive information, and stale claims.
- Derive a release-readiness checklist from
  [Release Process](docs/RELEASE_PROCESS.md) without duplicating that policy.

### Checkpoint B: Clean-room onboarding

- Give a fresh human or AI the repository entry point without chat history,
  bootstrap PDFs, or the onboarding ZIP.
- Require the reader to explain mission, current maturity, architecture,
  information ownership, decision process, contribution lifecycle, security
  route, operations, release, and next work.
- Record questions, wrong inferences, navigation failures, and evidence.
- Correct material documentation gaps through reviewable changes.
- Add a concise memory-promotion example to
  [AI Memory Contract](docs/AI_MEMORY_CONTRACT.md) only if the exercise shows
  it improves correct onboarding.

### Checkpoint C: `v0.1.0` foundation release

- Confirm all Phase 0 exit criteria and the derived release checklist.
- Finalize project status, sprint outcome, roadmap state, and changelog.
- Obtain explicit Chief Architect approval of the complete foundation.
- Merge the approved release change to `main`.
- Create and push an annotated `v0.1.0` tag at the verified merge commit.
- Create and verify a GitHub release whose notes state that it is an
  engineering-foundation release with no Project Jebediah application.

The audit and release may use separate pull requests when corrections would
otherwise make review too large.

## Non-goals

- Application, JCS, collector, knowledge graph, Digital Twin, automation,
  Reasoning Engine, or infrastructure implementation
- Verification or publication of private home-lab configuration
- Selecting a product language, framework, protocol, schema, or deployment
  mechanism
- Claiming operational or software capability that the repository does not
  contain
- Publishing a software license without an explicit maintainer decision
- Treating a successful automated check as a substitute for clean-room review

## Acceptance criteria

- Every required Genesis foundation topic maps to a substantive canonical
  document.
- Canonical documents agree about phase, current state, evidence, ownership,
  workflow, security reporting, and next work.
- `python scripts/validate_docs.py`, `git diff --check`, and the required
  GitHub check pass.
- A clean-room reader can accurately explain the repository without bootstrap
  materials or conversation history.
- Every material onboarding failure is corrected or assigned with an owner
  and resolution gate.
- The release checklist is satisfied with exact evidence.
- The Chief Architect approves the complete foundation and release.
- The `v0.1.0` tag and GitHub release point to the exact approved commit and
  clearly describe the release boundary.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Milestone 6A: repository-owned quality gate | Complete | Pull request #9 approved by the Chief Architect and merged |
| Milestone 6B: verified GitHub control plane | Complete | Private reporting and `main` protection enabled and read back through the GitHub API |
| Checkpoint A: foundation audit | In progress | Genesis Sprint 6 |
| Checkpoint B: clean-room onboarding | Complete | Two independent repository-only AI reviews passed with no material blocker |
| Checkpoint C: `v0.1.0` foundation release | Pending | Begins only after audit and clean-room criteria pass |

## Dependencies

- `main` remains the only project source of truth.
- The `documentation-quality` check and effective GitHub protections remain
  operational.
- The [Release Process](docs/RELEASE_PROCESS.md) owns release policy.
- The [Definition of Done](docs/DEFINITION_OF_DONE.md) remains the universal
  completion gate.
- The Chief Architect receives exact audit artifacts, corrections, validation,
  and release evidence.
- The maintainer retains final authorization for the public tag and GitHub
  release.

## Risks

| Risk | Response |
| --- | --- |
| Prior checkpoint approvals obscure cross-document conflict | Audit the repository as one reader-facing system, not as isolated diffs. |
| The author cannot perform a genuinely fresh review | Use a separate clean-room reader with no conversation history and record its independent output. |
| The audit produces a large unfocused pull request | Separate evidence and correction checkpoints while keeping one explicit release gate. |
| A checklist becomes duplicated policy | Derive a release-specific checklist that links to canonical standards. |
| Documentation implies application readiness | State the foundation-only boundary in status, changelog, tag, and release notes. |
| A tag targets an unreviewed or failing commit | Tag only the verified merged commit after all required checks and approval. |
| The public repository remains unlicensed | Treat public visibility and reuse permission as distinct; keep the license decision open. |

## Update rule

Update this file when audit scope, evidence, dependencies, risk, or release
readiness changes. At sprint close:

1. Record audit and clean-room outcomes in durable repository evidence.
2. Resolve or explicitly assign every material failure.
3. Finalize status, roadmap, changelog, and release notes.
4. Verify the exact release commit before tagging.
5. Open Phase 1 planning only after the foundation release is verified.
