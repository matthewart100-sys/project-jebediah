# Organizational Intelligence Interface Specification

**Status:** Proposed

**Maturity:** Review target only; no implementation or deployment authorized

## Purpose

This specification defines a bounded executive interface for a nonprofit
leader who needs to understand organizational state without navigating the
underlying technical system. It defines responsibilities, evidence rules,
failure behavior, and acceptance criteria before any user-interface or service
implementation is selected.

The interface is a read-only consumer of approved information. It does not
become authoritative merely because it presents, summarizes, or ranks that
information.

## Intended outcome

The first useful interface must answer four questions plainly:

1. What is happening?
2. What needs attention?
3. What does Jebediah know?
4. What should happen next?

Each answer must expose its evidence, freshness, uncertainty, and limits. When
the project lacks admissible information, the interface must say so instead of
inventing a complete answer.

## Scope

This proposal governs:

- The executive-facing information structure for the four questions
- A read-only organizational-intelligence read model
- Evidence, citation, freshness, uncertainty, and degraded-state behavior
- The boundary between deterministic facts, derived summaries, action
  candidates, and human decisions
- Accessibility, privacy, security, and validation requirements for the first
  interface foundation

## Non-goals

This proposal does not:

- Select a frontend framework, visual design system, API protocol, model,
  database, hosting platform, or deployment topology
- Authorize ingestion or use of live organizational information
- Replace original authoritative sources, reviewed GitHub records, or runtime
  systems of record
- Approve actions, create commitments, change organizational records, or
  trigger automation
- Activate the Phase 6 Reasoning Engine or define general autonomous agents
- Treat model output, rankings, or recommendations as verified facts
- Resolve authentication, user roles, data classification, retention, or
  operational ownership for a live deployment

## User and responsibility boundary

The initial user is an authorized nonprofit executive or delegate seeking an
organizational briefing. The interface owns presentation, navigation, and
faithful representation of the approved read model. It does not own source
truth, ingestion, verification, knowledge derivation, or action execution.

The interface must remain useful without requiring the user to understand
collectors, embeddings, Qdrant, provenance schemas, or model-serving details.
Technical diagnostic detail belongs in a separate operator surface.

## Information eligibility

An item may appear in an ordinary executive view only when all of the
following are true:

- Its information domain, producer, consumer, and intended use are approved.
- The source or canonical record is identifiable.
- Any derived representation has admissible input provenance and a recorded
  transformation identity.
- Its lifecycle permits ordinary retrieval.
- Its classification permits display to the current user.
- Required freshness and validation rules have been evaluated.

Quarantined, rejected, failed, deleted, superseded, or unauthorized material
must not appear as ordinary evidence. A separately authorized diagnostic view
may expose sanitized processing state without exposing protected content.

## Organizational-intelligence read model

The interface consumes a structured read model rather than querying source
systems or parsing documents directly. The future component specification and
interface decision must define the concrete transport. At minimum, each
presented item needs:

| Field | Meaning |
| --- | --- |
| Stable item identifier | Identifies the presented read-model item |
| Section | One of `happening`, `attention`, `know`, or `next` |
| Plain-language statement | The bounded claim shown to the user |
| Evidence classification | Verified fact, reported fact, working assumption, open question, or derived summary |
| Source references | Safe references to every source required to support the claim |
| Source observation time | When the represented source state applied, when known |
| Retrieved or assembled time | When the read model was produced |
| Freshness state | Current, aging, stale, unknown, or not applicable under an approved policy |
| Confidence basis | Why the item is shown with its stated confidence; never a truth score |
| Lifecycle state | Whether the item is active, superseded, archived, or otherwise eligible |
| Transformation identity | The versioned derivation used when the item is not a direct fact |
| Limitation | Material missing evidence, conflict, uncertainty, or scope restriction |
| Permitted next step | A navigation or human-review option, not an autonomous action |

Missing values remain explicitly missing. The read model must not manufacture
source times, confidence, owners, or next steps to make a card appear complete.

## The four executive questions

### What is happening?

This section presents current, bounded organizational state and recent changes
from admissible evidence. It distinguishes the time the source state applied
from the time it was retrieved or summarized. Stale or conflicting state is
visible and cannot be silently collapsed into a single current fact.

### What needs attention?

This section presents condition-based attention items whose rule, evidence,
urgency basis, owner when known, and review deadline when known are visible.
An attention item is a request for human review. Ranking does not grant action
authority, and absence from the section does not prove that no risk exists.

### What does Jebediah know?

This section presents material changes, decisions, risks, opportunities, and
knowledge gaps supported by admissible evidence. It states the covered
information domains and material limits so that “Jebediah knows” cannot imply
complete organizational knowledge or factual certainty. Direct facts, reported
facts, derived summaries, assumptions, and open questions must remain
distinguishable.

### What should happen next?

This section presents approved plans, unresolved gates, and bounded action
candidates in priority order under a visible rule. Every candidate identifies
whether it is navigation, review, drafting, or a separately governed external
action. “Should” expresses a supported proposal for human decision, not system
authority. The initial interface may navigate or prepare information, but it
must not execute an organizational or external action.

## Assistance boundary

A conversational or generated summary may be added only after its separate
interaction architecture is accepted. Such assistance must:

- Use only the eligible read model or other explicitly approved context
- Treat retrieved content as untrusted data, not instructions
- Cite supporting items and reveal material uncertainty
- Refuse to claim knowledge that the eligible evidence does not support
- Avoid changing verification, lifecycle, priority, or action authority
- Keep generated output derived and non-authoritative

Deterministic assembly must remain available for the core briefing even when a
model is unavailable. Model failure cannot erase the underlying evidence or
turn an incomplete answer into apparent success.

## User-visible states

The interface must represent at least these conditions:

- **Ready:** eligible evidence was assembled successfully.
- **Partial:** one or more approved inputs are unavailable or incomplete, and
  the affected sections are identified.
- **Stale:** evidence exceeds an approved freshness threshold.
- **Insufficient evidence:** no admissible basis supports the requested
  answer.
- **Unauthorized:** the user or intended use lacks required access.
- **Unavailable:** the read model cannot be assembled safely.

Empty state is not failure when no eligible item exists. It must still state
the coverage and time boundary so that “nothing eligible was found” is not
misread as “nothing is happening.”

## Accessibility and language

The first interface must support keyboard operation, meaningful focus order,
programmatic names, sufficient contrast, text resizing, non-color status
cues, and clear error identification. Plain-language summaries come first;
evidence and technical detail remain available through progressive disclosure.

Dates and times must include their timezone or an unambiguous user-local
rendering. Relative time alone is insufficient for evidence or audit views.

## Security and privacy

- Authentication, authorization, and classification are mandatory before any
  live organizational view is deployed.
- Source content is never placed in client code, URLs, logs, analytics, or
  error messages without explicit approval for that exposure.
- Citations use safe references and do not reveal private storage topology.
- The ordinary executive view follows least privilege and cannot become an
  administrative back door.
- Prompt, retrieval, export, and rendering paths treat external content as
  untrusted and defend against instruction injection and active content.

## Failure and recovery

Read-model assembly must fail visibly by source and section. A last-known view
may be shown only when its capture time and stale state are prominent. A failed
refresh must not overwrite the last known usable view with an apparently empty
success.

The interface itself owns no authoritative state. Preferences or saved views,
if later approved, require separate ownership, retention, backup, and recovery
decisions.

## Dependencies and authorization gates

Implementation waits for all applicable gates:

1. Acceptance of ADR 0011 or an approved replacement for the Knowledge Vault
   authority boundary
2. Acceptance of Proposed ADR 0012 for the interface read-model boundary
3. Acceptance of the document-admission decision when document-derived
   evidence is in scope
4. Approval of initial information domains, owners, producers, consumers,
   classification, retention, and freshness policies
5. A component responsibility and interface contract for read-model assembly
6. Security and privacy threat review
7. Work Mode architecture review, Chief Architect acceptance, proposal merge,
   and separate sprint authorization

## Acceptance criteria for this specification

The proposal is review-ready when:

- All four executive questions have bounded semantics.
- Source facts, derived summaries, assumptions, open questions, and action
  candidates cannot be confused through the contract.
- Every presented claim can expose provenance, time, freshness, and limits.
- Empty, partial, stale, unauthorized, and unavailable states are defined.
- The interface cannot directly ingest sources, mutate authoritative records,
  or execute external actions.
- No implementation technology or live information use is authorized by the
  proposal.
- Validation requirements trace these obligations to future evidence.

## Open questions

| Question | Owner or gate |
| --- | --- |
| Which organizational domain is the first bounded pilot? | Chief Architect scope decision plus information-owner approval |
| Who may access each class of organizational information? | Information owner and security review |
| What freshness thresholds apply to each fact type? | Domain specification and information owner |
| Which read-model component owns assembly and operational support? | Accepted component specification |
| Which actions may later progress beyond navigation or drafting? | Separate Phase 5 authority decision |
| Is generated assistance needed in the first implementation? | Sprint selection after interaction-architecture disposition |

These questions block implementation where applicable. They do not prevent
review of the proposed responsibility and evidence boundaries.

## Related documents

- [Current Architecture](ARCHITECTURE.md)
- [Data Ownership](DATA_OWNERSHIP.md)
- [Organizational Document Ingestion Specification](ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
- [Organizational Intelligence Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_VALIDATION_REQUIREMENTS.md)
- [ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md)
- [Proposed ADR 0012](adr/0012-executive-organizational-intelligence-interface-boundary.md)
- [Project Coordination Protocol](governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md)
