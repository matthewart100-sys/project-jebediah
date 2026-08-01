# Documentation Standards

## Purpose

Documentation is Project Jebediah's durable engineering memory. These standards
define canonical ownership, evidence labels, structure, style, linking,
maintenance, and review so repository knowledge remains reliable without prior
chat history.

This document owns documentation policy. Branch naming belongs to
[Git Workflow](GIT_WORKFLOW.md), repository paths and artifacts belong to
[Repository Standards](REPOSITORY_STANDARDS.md), and completion criteria belong
to the [Definition of Done](DEFINITION_OF_DONE.md).

## Documentation principles

- Documentation is part of the product and system.
- One canonical document owns each shared concept.
- Current truth is separated from plans and history.
- Verified facts are separated from reports and assumptions.
- Unknowns are explicit and actionable.
- Text-based, diffable formats are preferred.
- Links replace copied policy.
- Documentation changes with the reality it describes.
- Placeholder documents are prohibited.
- AI-authored content meets the same evidence and review standard as human
  content.

## Canonical ownership

| Concept | Canonical owner |
| --- | --- |
| Project entry and onboarding route | `README.md` |
| Mission and enduring manifesto | `docs/MISSION_AND_MANIFESTO.md` |
| Current project reality | `PROJECT_STATUS.md` |
| Active sprint | `CURRENT_SPRINT.md` |
| Strategic phase sequence | `ROADMAP.md` |
| Notable changes and releases | `CHANGELOG.md` |
| Contributor lifecycle | `CONTRIBUTING.md` |
| Branches, commits, pull requests, merge | `docs/GIT_WORKFLOW.md` |
| Sprint methodology | `docs/SPRINT_PROCESS.md` |
| Universal completion criteria | `docs/DEFINITION_OF_DONE.md` |
| Repository paths and artifacts | `docs/REPOSITORY_STANDARDS.md` |
| Language-independent engineering quality | `docs/ENGINEERING_STANDARDS.md` |
| Documentation policy | `docs/DOCUMENTATION_STANDARDS.md` |
| Project Genesis execution | `docs/genesis/PROJECT_GENESIS_PLAN.md` |
| JCS definition phase execution | `docs/JCS_DEFINITION_PLAN.md` |
| Proposed and future accepted JCS contract | `docs/JCS_SPECIFICATION.md` |
| Chief Architect review evidence and decision | `docs/reviews/ARCHITECT_REVIEW_TEMPLATE.md` |
| Architecture principles | `docs/ARCHITECTURE_PRINCIPLES.md` |
| Current architecture | `docs/ARCHITECTURE.md` |
| Memory-service architecture | `docs/ARCHITECTURE_MEMORY_SYSTEM.md` |
| Architecture decisions | `docs/adr/` |
| Shared project terminology | `docs/reference/GLOSSARY.md` |
| Component identity, maturity, and ownership | `docs/reference/COMPONENT_REGISTRY.md` |
| Tool-agnostic AI onboarding | `AGENTS.md` |
| Codex operations | `CODEX_BOOTSTRAP.md` |
| Human and AI collaboration | `.ai/COLLABORATION.md` |
| AI memory policy | `docs/AI_MEMORY_CONTRACT.md` |
| Data ownership categories | `docs/DATA_OWNERSHIP.md` |
| Digital Twin intent | `docs/design/DIGITAL_TWIN_POSITION.md` |
| Security policy | `SECURITY.md` |
| Testing philosophy | `docs/TESTING_PHILOSOPHY.md` |
| Operations philosophy | `docs/OPERATIONS_PHILOSOPHY.md` |
| Release process | `docs/RELEASE_PROCESS.md` |

When a document needs a concept owned elsewhere, summarize only the local
implication and link to the owner. Do not create a second policy.

## Document locations

### Repository root

Use for high-visibility entry points and frequently updated project governance:
README, status, sprint, roadmap, changelog, contribution, security, and
AI-agent entry files.

### `docs/`

Use for durable architecture, standards, process, design, and reference
material.

### `docs/adr/`

Use for immutable decision records once the ADR framework is approved. Current
architecture still updates when an ADR changes the system.

### `docs/genesis/`

Use for the approved Project Genesis implementation plan and durable Phase 0
audit evidence.

### `docs/releases/`

Use for version-specific release checklists and reviewed release notes.
Release artifacts link to the canonical release policy instead of duplicating
it.

### Implementation-adjacent documentation

Use near future code or configuration only when the audience and lifecycle are
owned by that component. Repository-wide policy remains in canonical docs.

## Required evidence categories

Architecture, design, status, data, and operations documents separate:

### Verified facts

Supported by repository state, inspected configuration, tests, or validated
system evidence. State the evidence when it is not obvious.

### Reported facts

Provided by a trusted source but not independently verified. Identify the
source category and validation need without exposing private conversation
content.

### Working assumptions

Temporary premises used for bounded progress. State impact, risk, and the
condition that confirms or invalidates the assumption.

### Open questions

Unresolved matters with importance and a resolution gate, owner, or next
evidence. Do not use a bare `TBD` when the question can be described.

Do not present a plan, report, assumption, or chat claim as implemented fact.

## Document status

Use a status label when readers need to distinguish lifecycle:

- Proposed
- Accepted
- Active
- Superseded
- Deprecated
- Historical

Do not add metadata mechanically to every document. Status and review dates
must help readers make a decision and must be maintained when present. Git
history already records authorship and modification time.

## Structure

Every substantive document should make its purpose clear near the beginning.
Use the smallest structure that supports its audience:

- One H1 matching the document subject
- Purpose or context
- Normative guidance or current information
- Boundaries and non-goals where ambiguity is likely
- Evidence categories where required
- Decisions, dependencies, risks, or maintenance rules as relevant
- Links to canonical related documents

Do not create sections solely to fill a template.

## Writing style

- Write direct, specific sentences.
- Prefer active voice.
- Use `must` for requirements, `should` for recommended defaults, and `may`
  for permitted choices.
- Define uncommon terms and acronyms at first use.
- Distinguish current behavior from future intent.
- Explain why a constraint exists when the reason prevents misuse.
- Avoid promotional language, vague assurances, and conversation references.
- Use examples only when they clarify a rule.
- Keep lists parallel and tables bounded.
- Use exact dates in `YYYY-MM-DD` when a date affects interpretation.

Terms such as "simple," "secure," "scalable," "production-ready," or
"temporary" require concrete meaning in context.

## Markdown

- Use GitHub-flavored Markdown.
- Use ATX headings (`#`, `##`, `###`).
- Use fenced code blocks with a language when known.
- Use backticks for paths, commands, identifiers, and literal values.
- Use relative links for repository content.
- Use descriptive link text instead of raw paths when prose permits.
- Keep one blank line around headings, lists, tables, and code blocks.
- End files with one newline.
- Avoid trailing whitespace and manual HTML unless Markdown cannot express the
  requirement accessibly.

Run `python scripts/validate_docs.py` locally. The `documentation-quality`
GitHub Actions job applies the same repository-owned checks to pull requests
and pushes to `main`. Its current checks cover required canonical files,
Markdown structure, balanced fences, local link targets, final newlines,
trailing whitespace, common sensitive values, and prohibited runtime,
bootstrap, or archive artifacts.

Automation enforces deterministic structure. It does not determine whether a
document is accurate, appropriately scoped, or architecturally sound.

## Links and navigation

- Link to the canonical owner at the first useful reference.
- Verify local targets in the same change.
- Update inbound links when moving content.
- Do not link to an untracked local file, personal cloud path, or transient
  conversation.
- External links must be necessary and should point to stable, authoritative
  sources.
- `docs/README.md` indexes current canonical documentation.
- The root README provides the shortest safe onboarding route.

Paths shown as future targets in a plan use inline code rather than broken
links until the file exists.

## Diagrams

- Prefer text-based Mermaid diagrams for version control and review.
- Provide a short prose explanation and do not make the diagram the only
  source of a critical rule.
- Name boundaries and relationships without inventing unapproved
  implementation.
- Keep diagrams readable in GitHub's renderer.
- Store a binary diagram only when a text representation is insufficient and
  the source is also preserved.

## Commands and examples

- Commands must identify the expected environment and effect.
- Use fake, non-sensitive values.
- Avoid destructive commands unless necessary, narrowly scoped, and explained.
- Examples must not be mistaken for approved production configuration.
- Validate examples when practical.
- Do not use screenshots as the only record of text or configuration.

## Decisions and rationale

Current architecture documents describe the system that is approved now. ADRs
record why lasting architecture decisions were made. Plans describe intended
work. Changelogs record delivered outcomes.

Update all affected categories in one pull request. An ADR alone does not make
stale current architecture acceptable.

## Reviews

Review documentation for:

- Correct canonical owner
- Factual support and evidence labels
- Consistency with architecture, status, sprint, roadmap, and ADRs
- Clear audience and purpose
- Actionable requirements
- Security and privacy exposure
- Valid links and navigation
- Duplication and terminology drift
- Maintenance responsibility
- Applicable Definition of Done

Architecture-significant documentation uses the
[Chief Architect Review Template](reviews/ARCHITECT_REVIEW_TEMPLATE.md) and
provides actual artifacts.

## Maintenance and drift

When project reality changes:

1. Identify every canonical document affected.
2. Update those documents with the implementation.
3. Update status, sprint, roadmap, and changelog only where their meaning
   changes.
4. Remove or supersede obsolete guidance.
5. Verify links and terminology.

If two canonical documents conflict, stop dependent work and resolve the
conflict. Do not select the convenient rule silently.

## Deprecation and history

- Mark a document deprecated only when readers still need a transition period.
- Link to its replacement.
- Remove obsolete content after references and consumers migrate.
- Use Git history for old versions rather than keeping files named `old`,
  `final`, or `archive`.
- ADRs follow their own immutable supersession model.

## AI-authored documentation

AI contributors must:

- Read canonical repository context first.
- Cite repository evidence in the pull request.
- Label conversation-derived claims as reported until promoted through review.
- Avoid copying chat transcripts into canonical docs.
- Link to the Definition of Done rather than restating it.
- Provide actual changed files for review.
- Record accepted decisions in GitHub before relying on them later.

## Exceptions

Document the reason, reader impact, owner, and resolution condition. A
formatting or ownership exception requires review and does not create a new
standard automatically.
