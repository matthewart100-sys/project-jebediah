# Knowledge Manager 1.0 Phase 1 Validation Requirements

**Status:** Accepted

**Accepted:** 2026-08-04

**Phase:** Knowledge Registry Foundation

**Date:** 2026-08-04

**Applies to:** The bounded implementation authorized by the
[Phase 1 Implementation Plan](KNOWLEDGE_MANAGER_1_PHASE_1_IMPLEMENTATION_PLAN.md)

**Authorization state:** Normative for the authorized Phase 1 implementation;
no excluded information use, runtime, or deployment is authorized

## Purpose

These requirements define the evidence needed to review the authorized
metadata-only Knowledge Registry implementation. Passing tests proves only the
tested domain and repository contracts. It does not authorize external
information, prove source claims, establish a Knowledge Vault service, or grant
runtime or action authority.

## Evidence baseline

At planning base `c5693f5995738ddd62acfef7782728dcf815b146`:

- The selected development environment is Python 3.14.5.
- The project requires Python 3.12 or newer.
- `python -m pytest -q` passes 142 tests.
- Workspace problem inspection reports no current source or test problems.
- No Knowledge Registry package, producer, consumer, store, or data exists.

Implementation review must rerun the baseline from the accepted implementation
base and record any legitimate count change.

## Validation principles

- Use only synthetic identifiers, policy labels, and timestamps.
- Test failures and invalid state explicitly; do not rely only on happy paths.
- Do not start Qdrant, Ollama, Docker, a service, or a network dependency.
- Do not load documents, fixtures derived from organizational information, or
  source or derived content.
- Validate authority semantics in code contracts and documentation; a passing
  serializer or repository round trip cannot establish truth.
- Test package separation mechanically rather than relying on reviewer intent.
- Treat an unexpected dependency, integration, runtime surface, or mutable
  transition as a stop condition.

## Required test organization

The implementation adds:

```text
tests/collector/knowledge/
    registry/
        test_models.py
        test_repository.py
        test_package_boundaries.py
```

Tests must use the existing pytest configuration and dependencies. No new test
tool may be added.

## Domain model validation

### Valid construction

Tests must prove that:

- A registry record can be constructed from fixed typed metadata.
- Input source, evidence, and permitted-use sequences become immutable tuples.
- A source reference accepts a revision, an observation time, or both.
- All retained datetimes are timezone-aware.
- Pending, approved, and rejected human-review records retain their exact
  stated state.
- Current, aging, stale, unknown, and not-applicable freshness values retain
  their exact stated state.
- Bounded, incomplete, conflicting, unknown, and not-applicable uncertainty
  values retain their exact stated state and explanation.
- Registered, superseded, archived, and invalidated lifecycle records retain
  their exact state, actor, time, and reason.
- A superseded lifecycle retains its successor object identity.
- Equal records compare equal and are safe to use as immutable values.

### Identifier and policy-label failures

Parameterized tests must reject empty and whitespace-only values for:

- Object identity and object kind.
- Source identity and authority scope.
- Transformation identity and version.
- Evidence identity.
- Producer identity.
- Information domain.
- Information-owner identity.
- Classification.
- Each permitted-consumer identifier.
- Each permitted-use identifier.
- Retention-policy identity.
- Deletion-policy identity.
- Freshness-policy identity.
- Invalidation-policy identity.
- Review-policy identity.
- Uncertainty explanation and every supplied uncertainty limitation.
- Reviewer identity and rationale when a decision requires them.
- Lifecycle recording actor, reason, and successor identity when required.

The implementation must not trim and accept an otherwise empty value, generate
a replacement, or substitute a default.

### Collection failures

Tests must reject:

- No source references.
- No evidence references.
- No permitted consumers.
- No permitted uses.
- A required uncertainty evidence or limitation collection that is empty.
- A collection containing an invalid item.

Duplicate source, evidence, permitted-consumer, or permitted-use identifiers
must be rejected. Sequence normalization must not silently remove ambiguity.

### Time and source-context failures

Tests must reject:

- Naive creation, observation, review, or lifecycle times.
- A source reference with neither source revision nor observation time.
- Naive effective, freshness-evaluation, or expiration times.
- Any implementation-generated current time when the caller omitted required
  evidence.

Time ordering is not inferred in Phase 1 because policy semantics are not
approved. Adding an ordering rule is a scope change and requires plan revision
before implementation.

### Human-review evidence matrix

| State | Reviewer | Decision time | Rationale | Expected |
| --- | --- | --- | --- | --- |
| `pending` | absent | absent | absent | Valid |
| `pending` | present | any | any | Invalid |
| `pending` | any | present | any | Invalid |
| `pending` | any | any | present | Invalid |
| `approved` | present | aware | present | Valid |
| `approved` | absent or empty | any | any | Invalid |
| `approved` | any | absent or naive | any | Invalid |
| `approved` | any | any | absent or empty | Invalid |
| `rejected` | present | aware | present | Valid |
| `rejected` | absent or empty | any | any | Invalid |
| `rejected` | any | absent or naive | any | Invalid |
| `rejected` | any | any | absent or empty | Invalid |

Tests must also prove that repository registration does not change
`pending` to `approved`, populate decision evidence, or alter lifecycle.

### Lifecycle evidence matrix

Tests must prove:

- Every lifecycle state requires a recording actor, aware time, and reason.
- `superseded` requires a non-empty successor identity different from the
  record's own object identity.
- `registered`, `archived`, and `invalidated` reject a successor identity.
- Registration preserves lifecycle metadata exactly.
- No repository method transitions lifecycle state or manufactures lifecycle
  evidence.

### Freshness and uncertainty matrix

Tests must prove:

- Missing freshness evidence is represented explicitly as `unknown`, not
  inferred as `current`.
- Registration does not change freshness state or times.
- `bounded` requires at least one evidence identifier.
- `incomplete` requires at least one material missing-evidence limitation.
- `conflicting` requires at least two evidence identifiers.
- `unknown` requires a limitation explaining why another state cannot be
  established.
- `not_applicable` retains an explanation and is not treated as `bounded`.
- Every evidence identifier referenced by uncertainty exists in the record's
  provenance evidence collection.
- Numeric confidence, probability, retrieval rank, and model self-confidence
  are absent from the contract.

The implementation must not infer time ordering beyond the accepted contract.
If it rejects an expiration or effective-time combination, that rule must be
documented and added to this matrix before implementation review.

### Authority-negative checks

The domain model must have no field or property named or documented as:

- Truth probability.
- Factual certainty.
- Numeric truth confidence or probability.
- Promotion authority.
- Retrieval eligibility.
- Action authority.
- Source correction authority.

No automatic numeric confidence value may be introduced. Evidence and
limitations remain explicit rather than compressed into a truth-like score.

## Repository contract validation

Run the same behavioral assertions against every Phase 1 repository adapter.
Phase 1 is expected to have only the in-memory reference adapter.

Tests must prove:

- Registering a valid record makes `contains` true.
- `find` returns the equal immutable record.
- Missing identities produce `False` and `None`.
- Re-registering the equal record is idempotent.
- Registering different metadata under the same object identity raises
  `KnowledgeRegistryConflict`.
- A conflict does not overwrite the original record.
- Empty or whitespace-only lookup identities raise an explicit validation
  error.
- Registration does not mutate the supplied record.
- A returned record cannot be used to mutate repository state.
- No repository method performs review, lifecycle transition, search,
  retrieval, update, delete, or action.

The adapter must not claim durability, thread safety, process sharing, or
recovery behavior.

## Package and dependency validation

`test_package_boundaries.py` must inspect Python imports under
`src/collector/knowledge/` and fail if they include:

- `collector.memory`
- Existing Collector pipelines, adapters, or runtime composition
- `qdrant_client`
- Ollama or embedding modules
- `collector.service`
- Any new third-party package

The test must also prove that existing source modules outside
`collector.knowledge` do not import the new registry package.

Reviewers must inspect:

- `pyproject.toml` and `uv.lock` for no change.
- Existing memory model, governance, repository, Qdrant payload, pipeline, and
  runtime files for no change.
- The public exports for no accidental root-package or memory-package
  integration.

## Compatibility validation

The implementation must preserve:

- Construction and equality behavior of `MemoryItem`.
- Existing memory provenance and lifecycle serialization.
- Existing memory repository and semantic repository signatures.
- Existing Qdrant payload compatibility.
- Existing Collector and service composition.

The primary evidence is an unchanged diff for those files plus the full
regression suite. If a memory compatibility failure occurs, Phase 1 stops; it
does not authorize a compatibility shim or memory refactor.

## Commands and expected evidence

Run from the repository root with the selected project Python executable:

1. Targeted registry tests:

   ```text
   python -m pytest tests/collector/knowledge/registry -q
   ```

2. Full regression suite:

   ```text
   python -m pytest -q
   ```

3. Import smoke check:

   ```text
   python -c "from collector.knowledge.registry import KnowledgeRegistryRecord"
   ```

4. Documentation validation:

   ```text
   python scripts/validate_docs.py
   ```

5. Whitespace validation:

   ```text
   git diff --check <accepted-base>...HEAD
   ```

6. Change-scope inspection:

   ```text
   git diff --name-status <accepted-base>...HEAD
   ```

The pull request records the exact Python executable or environment class,
accepted base, tested head, command, result, and date. The GitHub
`documentation-quality` check must also pass.

## Evidence matrix

| Requirement | Required evidence |
| --- | --- |
| Typed metadata contract | Model diff and focused positive tests |
| Invalid metadata fails closed | Parameterized negative tests |
| Human decisions remain human | Review evidence matrix tests and no transition API |
| Registry does not imply truth | Contract text, no confidence score, authority-negative inspection |
| Repository is storage-neutral | Three-method interface and adapter contract tests |
| Identity conflict is visible | Typed-conflict and no-overwrite tests |
| No memory duplication or integration | Domain-shape review, dependency tests, unchanged memory files |
| No runtime or technology selection | Diff manifest, dependency files unchanged, no service or adapter imports |
| Existing behavior remains intact | Full regression suite |
| Documentation is coherent | Documentation validator, link checks, diff check, consistency review |

## Stop conditions

Implementation and review stop if:

- ADR 0014 or the plan is not accepted at the implementation base.
- Canonical sprint authority does not authorize Phase 1.
- Any source or derived content is added to the registry model or fixtures.
- External information is acquired, retained, transformed, or tested.
- Registry code imports memory, Qdrant, embeddings, service, or runtime code.
- Existing code imports the registry.
- A durable store, network surface, configuration, dependency, or deployment is
  added.
- Repository registration changes review or lifecycle state.
- Approval lacks identified human decision evidence.
- An unapproved state is treated as retrieval-eligible or actionable.
- Existing memory behavior, payloads, or signatures change.
- Required tests or checks fail.
- The implementation diff exceeds the exact accepted file and behavior scope.

A stop condition requires plan revision, Work Mode re-review, and Chief
Architect disposition. It must not be bypassed with a fallback, broad
exception, or success-shaped default.

## Implementation-review packet

The Implementation Engineer must provide:

- Repository identity and pull-request URL.
- Accepted plan and ADR commit.
- Exact implementation base and head commits.
- Complete changed-file manifest.
- Domain and repository API summary.
- Targeted and full test commands and results.
- Package and dependency evidence.
- Documentation and diff-check results.
- Confirmation that fixtures are synthetic.
- Confirmation that no external information, runtime, memory integration,
  durable state, or deployment was added.
- Known limitations and residual risks.
- Rollback point.
- One requested Work Mode disposition.

Work Mode reviews the actual diff and evidence, not this plan alone. The Chief
Architect may approve merge only after all blocking findings are resolved or
receive a permitted written disposition under the
[Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md).

## Phase completion boundary

Passing validation means only that the reviewed code can represent and retain
synthetic governed registry metadata through an in-memory reference adapter.

It does not authorize:

- Knowledge ingestion or learning.
- External information use.
- A durable Knowledge Vault.
- Registry producers or consumers.
- Memory, retrieval, model, interface, or action integration.
- Deployment or operations.

Those capabilities require separate architecture, plans, validation, and exact
authorization.
