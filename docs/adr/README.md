# Architecture Decision Record Process

**Status:** Active

## Purpose

Architecture Decision Records (ADRs) preserve why Project Jebediah made
lasting technical and structural choices. They make alternatives,
consequences, evidence, and supersession visible without using conversation
history as decision memory.

The [current architecture](../ARCHITECTURE.md) describes what is approved now.
ADRs explain why it became approved. An ADR does not excuse stale current
documentation.

## When an ADR is required

Create an ADR for a lasting decision that materially affects:

- Architecture principles or project-wide constraints
- System or component responsibilities and boundaries
- Authoritative data ownership, provenance, retention, or consistency
- Public or cross-component interfaces and compatibility
- Deployment topology or an independently operated service
- Security posture, trust boundaries, identity, or authorization
- Core languages, frameworks, databases, workflow platforms, or model-serving
  technologies
- Recovery, migration, or operational strategy
- A long-lived exception to an engineering standard
- A meaningful reversal or supersession of an accepted decision

An ADR is usually unnecessary for:

- Editorial corrections that do not change meaning
- Routine implementation inside approved boundaries
- A local, reversible choice with no compatibility or operational consequence
- Experiments that cannot affect production or durable data and are clearly
  time-bounded

When uncertain, document the trigger assessment in the pull request. The
Chief Architect may raise or lower the required level based on impact.

## Decision levels

### Foundational

A project-wide decision that changes enduring principles, major platform
direction, roadmap ordering, authority, or a constraint inherited by several
systems.

Foundational ADRs require Work Mode architecture review and final Chief
Architect acceptance. Dependent implementation waits for acceptance.

### System

A decision defining a subsystem's responsibility, major boundary, data
authority, public interface, deployment model, or critical technology.

System ADRs require Work Mode architecture review and final Chief Architect
acceptance. Dependent components wait for acceptance.

### Implementation

A lasting lower-level choice within approved architecture, such as a
compatibility strategy, persistence pattern, or significant dependency whose
consequences outlive one code change.

Implementation ADRs use normal technical review plus Work Mode review and
final Chief Architect acceptance. Review depth remains proportional to the
choice's boundary and risk.

Decision level reflects scope and consequence, not the number of changed
files.

## Status lifecycle

| Status | Meaning |
| --- | --- |
| Proposed | Under review and not authoritative |
| Accepted | Approved and binding within its scope |
| Rejected | Considered and deliberately not selected |
| Superseded | Replaced by a later accepted ADR |
| Deprecated | Still present but scheduled for replacement |
| Withdrawn | Removed from consideration before a decision |

Accepted, rejected, and superseded ADRs are immutable decision history.
Correct spelling or broken links without changing meaning; use a new ADR to
change the decision. Add supersession links to both records when a later ADR
replaces an earlier one.

## Numbering and filenames

- Use one repository-wide sequence.
- Use four digits followed by a concise lowercase hyphenated title:
  `0001-example-decision.md`.
- Determine the next number from all tracked ADR filenames, including rejected
  and superseded records.
- Never reuse a number.
- `0000-template.md` is the template and is not a decision.
- A proposed ADR receives its final number before review so links remain
  stable.

## Workflow

1. **Identify the trigger.** State the problem, scope, urgency, evidence, and
   why an ADR is required.
2. **Choose the level.** Explain why the consequence is Foundational, System,
   or Implementation.
3. **Copy the template.** Assign the next number and replace every instruction
   with substantive content.
4. **Describe context honestly.** Separate verified facts, reported facts,
   working assumptions, and open questions.
5. **Compare alternatives.** Include retaining the current design when it is a
   real option.
6. **State the decision.** Make the chosen boundary and behavior precise
   enough to guide implementation without adding unrelated design.
7. **Analyze consequences.** Cover data, security, operations, recovery,
   compatibility, tests, cost, and reversibility as applicable.
8. **Update current documents.** Change architecture, glossary, component
   registry, data ownership, standards, status, and roadmap where the accepted
   decision changes their meaning.
9. **Review actual artifacts.** Obtain Work Mode architecture review and use the
   [Chief Architect Review Template](../reviews/ARCHITECT_REVIEW_TEMPLATE.md)
   for the final Chief Architect decision when required.
10. **Record the result.** Set the ADR status only after the Chief Architect
    decision, record review evidence in the pull request, and merge through the
    [Git Workflow](../GIT_WORKFLOW.md).
11. **Implement afterward.** Foundational and System implementation begins
    only after acceptance. A bounded Implementation ADR may accompany its
    first implementation when reviewers can evaluate both safely.

## Evidence requirements

An ADR distinguishes:

- **Verified facts** supported by repository, test, measurement, or inspected
  system evidence
- **Reported facts** that still require verification
- **Working assumptions** with impact and confirmation conditions
- **Open questions** with owners or resolution gates

Evidence must be sufficient for the decision's risk. Benchmarks identify
method and environment. Operational claims identify sanitized evidence.
Security-sensitive evidence may remain private while the ADR records the safe
conclusion, owner, and verification method.

## Decision quality

An acceptable ADR:

- Frames one coherent decision
- Names scope and non-goals
- Identifies affected owners and consumers
- Uses criteria tied to project needs
- Compares credible alternatives
- States positive, negative, and neutral consequences
- Explains failure and rollback
- Identifies follow-up work without hiding incomplete prerequisites
- Uses no secret or private operational detail

Do not write an ADR to rationalize a completed implementation after the fact.
Repository emergency implementation follows the bounded declaration,
authorization, deferred-review, and merge gates in the
[Project Coordination Protocol](../governance/JEBEDIAH_PROJECT_COORDINATION_PROTOCOL.md).
If separately authorized operational containment must precede an ADR, record
the exception, immediate evidence, and follow-up decision explicitly without
using containment to authorize repository architecture or scope changes.

## Relationship to project memory

The [AI Memory Contract](../AI_MEMORY_CONTRACT.md) governs promotion from
ephemeral context into durable GitHub artifacts. An architectural conclusion
that future work depends on belongs in an ADR and the affected current
document, not only in a chat, meeting note, pull-request comment, or model
memory.

Pull requests preserve review and implementation history. The ADR preserves
decision rationale. Current architecture preserves the resulting present
state.

## Security and privacy

Public ADRs must not contain credentials, private addresses, personal data,
raw sensitive logs, exploit-ready topology, or confidential threat details.
Record sanitized conclusions and the owner of any approved private evidence.
Security concerns do not justify omitting the existence and consequence of a
decision.

## Decision log

- [ADR 0001: Project Engineering Foundation](0001-project-engineering-foundation.md)
  is accepted and establishes the shared engineering-policy baseline.
- [ADR 0002: Canonical Memory Domain and Dependency Direction](0002-canonical-memory-domain-and-dependency-direction.md)
  is accepted and selects one memory-domain owner and dependency direction.
- [ADR 0003: Qdrant Repository, Collection, and Payload Consolidation](0003-qdrant-repository-collection-and-payload-consolidation.md)
  is accepted and defines Qdrant's temporary durable-record and semantic-index
  roles.
- [ADR 0004: Embedding Model Identity and Vector Compatibility](0004-embedding-model-identity-and-vector-compatibility.md)
  is accepted and pins the embedding provider, model artifact, geometry, and
  compatibility contract.
- [ADR 0005: Project Coordination and Role Authority](0005-project-coordination-and-role-authority.md)
  is accepted and defines the permanent multi-role authority, workflow,
  reviewer-independence, blocker-disposition, and handoff decision.
- [ADR 0011: Knowledge Vault Authority and Boundary Model](0011-knowledge-vault-authority-and-boundary-model.md)
  is accepted and defines a derived governed knowledge repository boundary
  without implementation, external information use, or source authority.
- [ADR 0012: Executive Organizational Intelligence Interface Boundary](0012-executive-organizational-intelligence-interface-boundary.md)
  is accepted and defines a read-only, evidence-bearing executive read-model
  boundary without ingestion or action authority.
- [ADR 0013: Governed Organizational Document Admission Boundary](0013-governed-organizational-document-admission-boundary.md)
  is accepted and defines quarantine-first PDF, DOCX, TXT, and Markdown
  admission without granting source authority or live information use.
- [ADR 0014: Knowledge Registry Domain Boundary](0014-knowledge-registry-domain-boundary.md)
  is proposed and would define a metadata-only registry library without
  content, memory integration, durable storage, runtime use, or source
  authority.
- [ADR 0000](0000-template.md) remains the maintained template and is not a
  decision.

Update this section in the same pull request that adds or changes an ADR's
status.
