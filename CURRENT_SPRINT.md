# Current Sprint

## Phase 1 Sprint 1: Closeout, Workflow Maintenance, and JCS Planning

**Target window:** 2026-07-30 through 2026-08-12

**Status:** Active; implementation blocked

## Sprint goal

Close Project Genesis with durable publication evidence, remove the owned
GitHub Actions runtime warning through a separately reviewed maintenance
change, and produce an approval-ready implementation plan for the JCS
definition phase without defining or implementing JCS prematurely.

## Context

Project Genesis Phase 0 is complete. Annotated tag `v0.1.0` and its GitHub
release identify the reviewed engineering foundation at
`978fa7f0ad855986e6bef39b373b6d9e5a9def53`. No Project Jebediah application,
infrastructure definition, runtime workflow, domain schema, or supported
software exists.

The roadmap requires JCS definition before collector or application
implementation. The next work must convert the JCS open question into an
evidence-based plan before making architectural choices. A separate
post-release maintenance item must also update the pinned `actions/checkout`
revision because GitHub reports its Node 20 runtime as deprecated even though
the required check still passes.

GitHub's official `actions/checkout` repository identifies `v7.0.1`, published
on 2026-07-20, at verified commit
`3d3c42e5aac5ba805825da76410c181273ba90b1`. Its action metadata uses Node 24.
The maintenance checkpoint changes only that immutable pin and its version
comment.

## Committed scope

### Checkpoint A: Project Genesis closeout

- Record the exact `v0.1.0` tag object, target commit, GitHub release, release
  state, notes comparison, link verification, and artifact inventory.
- Mark Project Genesis milestones and Phase 0 complete.
- Close Genesis Sprint 6 with delivered outcomes, carryover, and process
  lessons.
- Open Phase 1 planning without authorizing implementation.

### Checkpoint B: documentation-workflow maintenance

- Verify the current official `actions/checkout` release and immutable commit
  from primary GitHub sources.
- Replace only the deprecated immutable checkout pin.
- Preserve workflow permissions, triggers, Python setup, validator command,
  required check name, and branch-protection context.
- Prove the updated workflow on a pull request and on merged `main`.
- Read back branch protection and record any warning or changed behavior.

### Checkpoint C: JCS definition implementation plan

- Re-read the canonical mission, status, roadmap, architecture, data,
  security, operations, testing, AI, contribution, and decision documents.
- Gather JCS requirements and unknowns from authoritative repository evidence
  and explicitly supplied maintainer context.
- Separate foundation, specification, implementation, and operational
  evidence.
- Define the proposed documentation owner, review sequence, milestones,
  dependencies, risks, assumptions, and acceptance criteria for JCS
  definition.
- Identify decisions that may require Foundational or System ADRs without
  selecting an answer prematurely.
- Present the complete JCS definition plan to the Chief Architect and stop for
  approval before creating a JCS specification.

## Non-goals

- JCS, collector, application, infrastructure, workflow, or schema
  implementation
- Selecting a programming language, framework, protocol, database, queue,
  model, or deployment mechanism
- Treating the reported home-lab environment as verified
- Defining JCS from bootstrap conversation memory rather than repository
  evidence
- Creating speculative specification, traceability, catalog, runbook, source,
  test, or infrastructure artifacts before approved content gives them an
  owner
- Using the successful foundation release as evidence of runtime capability

## Acceptance criteria

- The Phase 0 closeout pull request records every publication requirement as
  `Pass` with exact GitHub evidence.
- Canonical status, roadmap, registry, release, security, Genesis, sprint, and
  changelog documents agree that Phase 0 is complete and implementation
  remains blocked.
- The checkout-pin maintenance change uses an official immutable revision,
  passes `documentation-quality`, preserves least privilege and the required
  check name, and is verified on `main`.
- The JCS definition plan is substantive, maps every required output to an
  owner and review gate, records assumptions and unresolved decisions, and
  receives explicit Chief Architect approval.
- No JCS specification or implementation begins before that plan approval.

## Work status

| Work item | State | Evidence |
| --- | --- | --- |
| Project Genesis Phase 0 foundation | Complete | Pull requests #1 through #12, tag `v0.1.0`, and the verified GitHub release |
| Checkpoint A: Project Genesis closeout | Complete | This reviewed post-publication closeout records the tag, release, verification, and transition |
| Checkpoint B: documentation-workflow maintenance | In progress | Official `actions/checkout` `v7.0.1` commit and Node 24 metadata verified; pull-request and merged-main validation remain |
| Checkpoint C: JCS definition implementation plan | Pending | Begins after workflow maintenance; specification waits for plan approval |

## Dependencies

- `main` and GitHub remain the project source of truth.
- The published `v0.1.0` tag is immutable.
- Phase 0 closeout receives Chief Architect approval before unrelated work.
- Workflow dependency selection uses primary GitHub release and repository
  evidence.
- The [Roadmap](ROADMAP.md) and
  [Component Registry](docs/reference/COMPONENT_REGISTRY.md) keep JCS at
  **Named** maturity until a specification is approved.
- The [ADR Process](docs/adr/README.md) governs architectural choices.
- The [Definition of Done](docs/DEFINITION_OF_DONE.md) applies to every
  checkpoint.

## Risks

| Risk | Response |
| --- | --- |
| Closeout language overstates software maturity | Repeat that `v0.1.0` is an engineering-foundation release with no application or infrastructure. |
| Updating a pinned action changes enforcement behavior | Change only the verified immutable pin, compare metadata, retain the check name and permissions, and read back GitHub state. |
| JCS planning turns into an implicit design decision | Record alternatives and decision triggers; stop for approval before specification. |
| Reported infrastructure biases the JCS contract | Keep infrastructure claims reported until a sanitized audit verifies them. |
| New artifacts become placeholders | Create an artifact only when approved scope provides substantive content, ownership, and acceptance evidence. |
| Phase 1 treats foundation evidence as implementation evidence | Use the four evidence categories and require implementation-specific validation later. |

## Update and close rules

Update this file when checkpoint scope, evidence, assumptions, dependencies, or
risks change. At sprint close:

1. Record merged evidence for every completed checkpoint.
2. Carry incomplete work with an explicit reason and revised gate.
3. Record new risks and process lessons.
4. Update status, roadmap, registry, and changelog together.
5. Define the next sprint before beginning work outside approved scope.
