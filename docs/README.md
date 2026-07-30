# Project Jebediah Documentation

This directory contains the durable technical, process, and governance memory
for Project Jebediah. GitHub Markdown is preferred because it is reviewable,
searchable, linkable, and version controlled.

## Current canonical documents

- [Mission and Manifesto](MISSION_AND_MANIFESTO.md) defines why the project
  exists and the principles that must survive implementation choices.
- [Project Genesis Plan](genesis/PROJECT_GENESIS_PLAN.md) defines the approved
  Phase 0 organization, delivery order, risks, and acceptance criteria.
- [Project Status](../PROJECT_STATUS.md) distinguishes current truth from
  reported facts, assumptions, and unresolved questions.
- [Changelog](../CHANGELOG.md) records notable repository changes and releases.
- [Repository README](../README.md) is the primary entry point.

Only documents that exist and contain substantive guidance are linked here.
This index will grow as each approved Genesis milestone is completed.

## Documentation authority

Repository documents serve different purposes:

1. `PROJECT_STATUS.md` records current verified reality.
2. Architecture and standards documents define current technical and process
   expectations.
3. Accepted, non-superseded Architecture Decision Records explain decisions
   and their consequences.
4. Sprint and roadmap documents describe intended work.
5. Issues and pull requests record proposals, reviews, and work history.
6. External bootstrap artifacts and conversations are historical context only.

The documents must agree. An accepted decision that changes architecture also
requires the current architecture documentation to change in the same pull
request. Contributors may not choose whichever conflicting statement is most
convenient.

## Evidence categories

Architecture, design, data, and operations documents must distinguish:

- **Verified facts:** supported by repository or validated system evidence.
- **Reported facts:** provided by a trusted source but not independently
  validated.
- **Working assumptions:** temporary premises used to make bounded progress.
- **Open questions:** unresolved matters with an owner or resolution gate.

Unsupported statements must not be presented as established truth.

## Planned permanent documentation

The approved Genesis plan will add substantive documents for:

- Architecture and architecture principles
- Repository and engineering standards
- Git workflow and sprint methodology
- Documentation standards and Definition of Done
- Testing, security, operations, and release philosophy
- AI collaboration and the AI memory contract
- Data ownership
- Digital Twin intent
- ADR governance with foundational, system, and implementation decision levels
- Reference material including terminology and a component registry

These paths are documented in the Genesis plan. They are not created until
their content is ready for review.

## Bootstrap-material policy

The onboarding ZIP, Word document, and Genesis PDFs are not copied into this
directory as canonical sources. Binary and conversational sources are
difficult to review and can drift from the repository. Their requirements must
instead be promoted into maintained Markdown through normal pull requests.
