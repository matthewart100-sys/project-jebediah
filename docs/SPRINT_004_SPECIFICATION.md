# Sprint 004 Specification: Memory Governance and Intelligence Expansion

**Status:** Active implementation specification

**Deployment status:** Not authorized by this sprint

## Objective

Extend the existing memory system with small, explicit foundations for
provenance, lifecycle awareness, and future retrieval ranking without
replacing the current Collector, memory pipeline, embedding adapter, Qdrant
storage, or API.

Sprint 003 established semantic embeddings, persistent vector memory, the
runtime memory API, consolidation, intelligence scoring, confidence
evaluation, retention scoring, and metadata enrichment. Sprint 004 makes that
stored and retrieved information more explainable.

## Architectural constraints

- Preserve existing service and module boundaries.
- Keep existing request fields and response fields compatible.
- Add governance metadata without changing memory identity.
- Treat Qdrant payloads and embeddings as derived information, not implicit
  source authority.
- Read legacy payloads safely without requiring a destructive migration.
- Keep ranking policy deterministic and semantic-only until a later decision
  defines multi-factor behavior.
- Do not automate lifecycle transitions or deletion in this sprint.

## Phase 1: Memory provenance

Every newly persisted memory must have provenance information that can answer
where it came from and why its current confidence was assigned.

The foundation supports:

| Field | Meaning |
| --- | --- |
| `source` | Origin category used by confidence evaluation, distinct from the existing stable `source_identity` |
| `creator` | Optional actor or system that created the source information |
| `creation_context` | Optional bounded context explaining how the memory was created |
| `confidence_basis` | Explainable reason for the current confidence score |
| `verification_state` | `unverified`, `verified`, or `disputed` |
| `supporting_evidence` | Optional evidence references; not raw evidence contents |

The existing `MemoryItem.created_at` remains the memory creation time. The
existing `source_identity` remains the stable source identifier. Neither field
is renamed or repurposed.

When a legacy caller supplies no provenance, the runtime derives `source` from
`source_identity`, records the memory as `unverified`, and preserves empty
optional fields. A missing value is not presented as verified information.

## Phase 2: Memory lifecycle awareness

Every memory has one lifecycle state:

- `active`: available under the current memory contract
- `reinforced`: supported by later compatible evidence
- `superseded`: replaced by a newer memory while retained for history
- `archived`: preserved but no longer considered current by a future policy

The lifecycle foundation also supports a reinforcement count, an optional
`superseded_by` memory identifier, and an optional lifecycle-change time.

New memories default to `active`. This sprint does not infer reinforcement,
select superseding memories, archive records automatically, filter retrieval
by lifecycle, or permanently delete information. Those behaviors require
separate policy, transition, and recovery decisions.

## Phase 3: Retrieval-ranking preparation

Retrieval candidates expose these independent signals to an internal ranking
boundary:

- semantic relevance
- confidence
- importance
- creation time for future recency evaluation
- lifecycle state

The initial ranker orders candidates only by semantic relevance. This
preserves current API behavior while allowing a future reviewed ranker to use
the other signals without changing Qdrant search or the public response
contract at the same time.

## Persistence and compatibility

Qdrant payloads add top-level `provenance` and `lifecycle` objects. Existing
payload fields remain unchanged.

Repository reads must support payloads created before Sprint 004:

- missing provenance becomes `source=<source_identity>` and `unverified`
- missing lifecycle becomes `active`
- missing optional retrieval signals remain unknown rather than fabricated

No collection recreation, vector rewrite, or live-data backfill is required
for this foundation.

## API compatibility

The store request may add optional provenance inputs while retaining every
existing required field. Omitted new fields use safe defaults.

To preserve existing behavior, an omitted API `source` uses the prior
`user` assumption. Legacy domain objects and stored payloads instead derive a
missing provenance source from their stable `source_identity`.

The store and context endpoints retain their existing status values and
response fields. Newly stored payloads may include the additive governance
objects. The context endpoint continues to expose semantic similarity as its
`score`.

## Non-goals

- Replacing Qdrant, Ollama, FastAPI, or the current memory pipeline
- Redesigning deterministic Collector identity
- Defining a multi-factor ranking formula or weights
- Automatically verifying claims
- Automatically reinforcing, superseding, archiving, or deleting memories
- Building a knowledge graph or relationship inference engine
- Migrating or rewriting existing live data
- Deploying the service or changing a live environment
- Adding autonomous collectors or actions

## Acceptance criteria

1. Existing `MemoryItem` construction remains valid.
2. Newly persisted memories receive provenance and an active lifecycle by
   default.
3. Confidence basis is retained when the intelligence pipeline produces it.
4. All requested provenance and lifecycle concepts have typed, documented
   representations.
5. Qdrant serialization preserves new fields and reads legacy payloads.
6. Retrieval candidates expose all five future ranking signals.
7. The default ranker preserves semantic relevance ordering.
8. Existing store and context response fields remain present.
9. Existing tests pass and focused governance, persistence, retrieval, and API
   compatibility tests are added.
10. Documentation validation and `git diff --check` pass.
11. No credentials, personal data, private address, or live memory content is
    added.
12. The exact uncommitted diff is reviewed before any commit.

## ADR assessment

No new ADR is required for this sprint. The change implements provenance and
lifecycle metadata already required by the active data-ownership and memory
architecture rules. It adds no new information authority, service boundary,
retention or deletion policy, deployment topology, or breaking public
interface. A future lifecycle transition policy, automatic verification,
multi-factor ranking policy, or authority change must reassess the ADR gate.

## Review focus

Reviewers should verify that the change is additive, legacy payloads remain
readable, provenance does not imply truth, lifecycle states do not silently
perform transitions, and retrieval remains semantic-only until a later
reviewed policy exists.
