# Current Sprint

## Active sprint

**Name:** Phase 3B Reconciliation Canonicalization

**Status:** Active documentation-only recovery package under Chief Architect
decision `CA-2026-08-06-P3B-RECONCILIATION`

**Canonical base:** `991929beb6026511e07b6cb7954e1c9e400b9cb5`

**Implementation authority:** None

**Deployment status:** Unauthorized

**Information-use status:** Synthetic or real document use, VBA access, model
use, knowledge promotion, memory/Qdrant projection, retrieval, grounded
answers, and public exposure are unauthorized.

## Active milestone question

Can Project Jebediah make the accepted Phase 3B reconciliation decision durable
and restore one unambiguous repository authority state without changing code,
executing the selected revert, or mutating any runtime?

## Authorized milestone boundary

This sprint authorizes:

- one documentation-only canonicalization package;
- the formal Chief Architect reconciliation record;
- supersession and historical-status corrections;
- the revised B0-B3, C0-C2, D1-D2, and O1 milestone sequence;
- preservation of pull requests #59 and #60 as audit and salvage evidence;
- documentation of, but not execution of, the selected future normal revert;
  and
- documentation, local-link, sensitive-content, and whitespace validation.

This sprint does **not** authorize:

- code, tests, dependencies, locks, workflows, Docker, Caddy, services, or
  scripts;
- a revert, cherry-pick, reset, rebase, force update, merge, or deployment;
- implementation of any revised milestone;
- real documents or VBA access;
- Phase 3B, Phase 3C, Phase 3D, workspace, identity, model, promotion, memory,
  Qdrant, retrieval, grounded-answer, or public-exposure work; or
- any runtime, server, container, DNS, certificate, database, or external-state
  mutation.

## Success criteria

1. The exact documentation manifest states one consistent current authority.
2. ADR 0016 remains Accepted and unbroadened.
3. The Completion Directive is Superseded and Milestone 1 is Historical.
4. The revised milestone sequence and future ADR gates are recorded.
5. Pull requests #59 and #60 remain preserved and explicitly non-deployable.
6. The future revert plan is exact but unexecuted and unauthorized.
7. Only Markdown changes are present, and required documentation validation
   passes.
8. One non-draft pull request receives independent exact-head Work Mode review
   and then a separate Chief Architect merge decision.

## Next authority gate

After this package is committed and pushed, work stops for independent Work
Mode review. A separate Chief Architect decision is required for the unchanged
documentation head. Even after this package merges, a separate future Chief
Architect authorization is required before the selected revert may begin.
