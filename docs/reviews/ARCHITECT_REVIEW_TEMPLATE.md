# Chief Architect Review Template

## Purpose

Use this template for milestone checkpoints and changes that affect project
identity, canonical documentation, architecture principles, component
boundaries, data ownership, infrastructure topology, security posture, or
other lasting technical direction.

The review must be based on actual artifacts. A summary without the diff or
changed files is not sufficient evidence for approval.

## Review request

### Change

- Repository identity and authoritative remote:
- Workstream:
- Pull request:
- Base branch and commit:
- Head branch and commit:
- Compare or diff target:
- Milestone or issue:

### Intended outcome

Describe what changes and why.

### Scope and non-goals

List what is included and explicitly excluded.

### Evidence package

Provide at least one:

- Accessible pull-request diff
- Git compare link
- Patch from the merge base to the head
- Exact contents of every changed file

Also include:

- Commit list
- Validation commands and results
- Work Mode review disposition, reviewer independence, and blocker status
- Chief Architect disposition for any blocker not corrected in the artifacts
- Relevant ADRs
- Known facts, reported facts, working assumptions, and open questions

## Chief Architect review checklist

- [ ] Design intent is preserved.
- [ ] No speculative implementation is presented as approved architecture.
- [ ] No architectural decision is undocumented.
- [ ] Documentation hierarchy is valid.
- [ ] Canonical ownership is maintained.
- [ ] Documentation is not duplicated.
- [ ] ADR impact and decision level are assessed.
- [ ] Roadmap impact is unchanged or documented.
- [ ] Backward compatibility and migration impact are addressed when relevant.
- [ ] Unknowns are explicitly labeled.
- [ ] Cross-links resolve and documents do not contradict one another.
- [ ] Work Mode review was performed by a distinct review instance that did
      not author or materially modify the reviewed artifacts.
- [ ] Every Work Mode blocker is corrected or has the explicit disposition
      required by the Project Coordination Protocol.
- [ ] Security, data ownership, operations, recovery, and observability impacts
      are considered where relevant.
- [ ] The change is maintainable by a future engineer or AI using the
      repository alone.
- [ ] The applicable Definition of Done is satisfied.

## Required decision

Work Mode review is required evidence but is not the final decision. The Chief
Architect returns exactly one:

### APPROVED TO MERGE

The artifacts satisfy the checkpoint and may merge. State what milestone or
next work is authorized.

### REVISIONS REQUIRED

List exact file-level or policy changes required before approval. Distinguish
blocking changes from recommendations.

### APPROVED TO CONTINUE WITHOUT MERGE

Explain why work may continue while the current pull request remains open and
identify the later merge gate.

## Review record

Record the decision and its evidence in the pull request. Recommendations that
are accepted for later work must be added to the sprint, roadmap, plan, issue
tracker, or canonical standards so they do not remain only in conversation
history.
