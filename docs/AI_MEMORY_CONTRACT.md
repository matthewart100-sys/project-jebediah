# AI Memory Contract

## Purpose

This contract makes the repository—not human recollection, chat history, or
model memory—the enduring project memory for Project Jebediah.

It defines memory layers, promotion rules, prohibited content, session
orientation, handoffs, conflict resolution, and recovery expectations for all
human and AI contributors.

## Core contract

Information that future work depends on must be recorded in the correct
reviewed GitHub artifact. If a decision, fact, assumption, constraint, or
procedure exists only in conversation, it is not durable project memory.

GitHub authority does not make every committed statement true. Canonical
documents must still label evidence and pass review.

## Memory layers

### Canonical current memory

Reviewed `main` contains:

- Current project status
- Active sprint and roadmap
- Current architecture and standards
- Accepted, non-superseded policies
- Current operations, security, and release guidance
- Reference definitions and component ownership

Canonical documents describe what contributors should rely on now.

### Decision memory

The [ADR process](adr/README.md) and reviewed pull requests record why lasting
choices were made, alternatives considered, consequences, and review evidence.

ADRs preserve decision history. Pull requests preserve implementation and
review history. Neither excuses stale current architecture.

### Work-planning memory

Current sprint, roadmap, issues, and draft pull requests record intended or
in-progress work. They do not prove implementation exists.

### Operational evidence

Tests, validated configuration, sanitized inventories, logs, metrics, and
incident records can support facts. Evidence containing sensitive data may
remain in an approved private system while GitHub stores a safe conclusion,
location, owner, and verification method.

### Ephemeral working context

Chats, temporary notes, terminal output, local scratch files, and model context
support active work but are not authoritative. They may be lost, incomplete,
wrong, or inaccessible to a future session.

## What must become durable

Record in GitHub when future work depends on:

- Mission, principles, and product intent
- Current capabilities and limitations
- Architecture, boundaries, interfaces, and ownership
- Accepted decisions and consequences
- Verified and reported environment facts
- Working assumptions and resolution gates
- Data authority, provenance, retention, and classification
- Security constraints and threat decisions
- Operational procedures, recovery, and rollback
- Test strategy and acceptance criteria
- Sprint commitments and roadmap changes
- Incidents, lessons, and owned follow-up actions
- Accepted Chief Architect recommendations
- Deprecation, migration, and release decisions

Select the canonical owner using
[Documentation Standards](DOCUMENTATION_STANDARDS.md).

## What must not become public repository memory

Do not commit:

- Secrets, tokens, keys, passwords, or authentication codes
- Personal identifiers or private communications
- Private IP addresses, hostnames, or exploitable topology
- Raw sensitive logs, prompts, model transcripts, or user data
- Database contents, vector-store data, backups, or model weights
- Unreviewed chat transcripts presented as decisions
- Copyrighted or licensed material without permission
- Large generated artifacts without repository-policy justification
- Speculation disguised as current architecture

Store sensitive evidence in an approved private system and commit only the safe
conclusion, ownership, and retrieval or verification guidance.

## Promoting conversation into memory

When a chat, meeting, or tool session produces durable information:

1. Extract the decision, fact, assumption, question, or action.
2. Remove conversational noise and sensitive content.
3. Classify it as verified fact, reported fact, working assumption, open
   question, proposal, or accepted decision.
4. Select the canonical document.
5. Add rationale, evidence, impact, owner, and resolution gate as appropriate.
6. Use an ADR when the information contains a lasting architectural decision.
7. Review the change against current architecture and standards.
8. Merge through the Git workflow.
9. Rely on the repository version in future sessions.

Do not commit a transcript when a concise maintained statement is sufficient.

## Session startup

An AI session establishes context by:

1. Reading the [AI entry point](../AGENTS.md).
2. Following its mandatory orientation order.
3. Inspecting the repository, branch, and uncommitted state.
4. Reading relevant issues, pull requests, architecture, ADRs, and tests.
5. Identifying facts, assumptions, open questions, and the current authority
   gate.
6. Verifying unstable external state when the task depends on it.

The maintainer should not need to reproduce prior chat history for discoverable
project context.

## Working memory during a task

During active work:

- Keep scope, decisions, and validation visible.
- Preserve unrelated changes.
- Record accepted scope changes promptly.
- Treat model recall as a hypothesis until supported.
- Do not assume another agent can see the same chat, browser, or local scratch
  state.
- Prefer links to canonical docs over copied policy.
- Capture evidence needed for review without exposing sensitive content.

## Session close and handoff

Before ending a significant task:

- Commit or clearly preserve authorized work.
- Update canonical documents affected by the result.
- Record exact validation.
- Record the formal review decision.
- Add accepted follow-up recommendations to a durable owner.
- State remaining risk, assumptions, and next authority.
- Identify uncommitted local state if any.

The handoff format is defined in the
[AI Collaboration Standard](../.ai/COLLABORATION.md); completion is governed
by the [Definition of Done](DEFINITION_OF_DONE.md).

## AI-authored documentation

AI-generated content is maintained like human-authored content:

- It has a canonical owner.
- Claims require evidence labels.
- Reviewers receive actual artifacts.
- Duplication is replaced with links.
- Stale content is updated or removed.
- Accepted decisions are not attributed to model authority alone.
- Generated volume is not evidence of completeness.

An AI must not create documentation solely to make the repository appear
complete.

## Conflict resolution

When memory sources conflict:

1. Identify the canonical owner for the subject.
2. Compare GitHub `main`, accepted ADRs, current evidence, and proposed work.
3. Distinguish stale documentation from a new unmerged proposal.
4. Stop dependent implementation.
5. Obtain the responsible decision.
6. Update all affected canonical documents in one reviewed change.

Do not use the newest chat statement automatically. Recency without review is
not authority.

## Recovery

Project memory is recoverable when:

- Canonical documentation is version controlled.
- Decisions have rationale and supersession history.
- Configuration and procedures identify their sources.
- Sensitive evidence has an owned private location.
- GitHub branches, tags, and releases follow documented policy.
- A clean-room reader can reconstruct current context.

Backups and export of GitHub-hosted project memory will be addressed by the
future operations philosophy and release process.

## Memory-quality review

Reviewers ask:

- Could a future contributor act safely from this information?
- Is current state separated from plans and history?
- Are facts supported and assumptions labeled?
- Does one canonical document own the concept?
- Are accepted decisions and recommendations durable?
- Has sensitive or conversational noise been excluded?
- Are links and references recoverable?
- Would the repository remain understandable if this chat disappeared?

If the last answer is no, the memory contract is not satisfied.
