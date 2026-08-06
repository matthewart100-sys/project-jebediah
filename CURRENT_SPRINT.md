# Current Sprint

## Active sprint

**Name:** B0 - Canonical Repository Recovery

**Status:** Recovery implemented and validated on a review branch; not
canonical until independently reviewed, approved, and merged

**Canonical base:** `b1d8dea531ad0b82171cb0f3f3979323b712a5de`

**Implementation authority:** None

**Deployment status:** Unauthorized

**Information-use status:** Synthetic or real document use, VBA access, model
use, knowledge promotion, memory/Qdrant projection, retrieval, grounded
answers, and public exposure are unauthorized.

## Active milestone question

Can Project Jebediah restore the reviewed pre-PR60 implementation baseline by
normal revert while retaining the canonical reconciliation decision and
leaving every runtime and deployment unchanged?

## Authorized milestone boundary

The separate Chief Architect B0 execution authorization dated 2026-08-06
authorizes:

- one normal revert of `991929beb6026511e07b6cb7954e1c9e400b9cb5`;
- preservation of the canonical reconciliation record and authority status;
- preservation of pull requests #59 and #60 as audit and salvage evidence;
- the reusable Master Execution Framework and minimum status synchronization;
- complete validation and one non-draft pull request; and
- preparation of exact review and next-phase handoffs.

This sprint does **not** authorize:

- Phase B1 or later implementation;
- a reset, rebase, force update, merge, deployment, or runtime mutation;
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
6. The normal revert is reviewable as an ordinary commit and does not rewrite
   history.
7. Required code, test, dependency, compilation, documentation, boundary, and
   repository-hygiene validation passes.
8. One non-draft pull request is opened for independent exact-head Work Mode
   review and a later separate Chief Architect merge decision.

## Next authority gate

After the B0 pull request is opened, work stops for independent exact-head Work
Mode review. A separate Chief Architect decision is required for the unchanged
pull-request head. B1 remains future and unauthorized.
