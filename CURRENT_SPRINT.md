# Current Sprint

## Active sprint

**Name:** P1 - Synthetic Organizational Learning Pilot Planning

**Status:** Planning active; documentation-only package proposed for exact-head
review

**Canonical base:** `37dd437617ed731340e9fd3da6cab0b1c49f7b4a`

**Planning authority:**
[`CA-2026-08-06-P1-PLANNING`](docs/governance/CHIEF_ARCHITECT_P1_PLANNING_AUTHORIZATION.md)

**Implementation authority:** None

**Deployment status:** Unauthorized

**Information-use status:** Real organizational information, VBA material,
arbitrary files, knowledge promotion, retrieval, grounded answers, model use,
memory or Qdrant projection, deployment, and public exposure are unauthorized.
Planning fixtures and examples must be fabricated and synthetic.

## Active milestone question

Can Project Jebediah produce a decision-complete plan for the first bounded,
end-to-end synthetic Organizational Intelligence learning loop without
changing accepted architecture, application code, runtime state, deployment,
or information-use authority?

## Authorized planning boundary

The Chief Architect directive `CA-2026-08-06-P1-PLANNING` authorizes:

- the complete synthetic P1 implementation plan, work breakdown, dependency
  analysis, testing strategy, execution order, branch strategy, and review
  strategy;
- documentation-only Proposed architecture reconciliation through Foundational
  ADR 0018 and System ADRs 0019 and 0020;
- bounded file- and function-level salvage analysis of historical pull
  requests #59 and #60;
- an exact future implementation manifest, rollback, stop conditions, and
  execution handoff; and
- validation and publication of one review-ready planning pull request.

This sprint does **not** authorize:

- application, test, dependency, lock, workflow, runtime, database,
  infrastructure, or deployment changes;
- implementation of P1 or any B1-through-O1 milestone;
- acceptance of ADRs 0018, 0019, or 0020;
- real organizational information, VBA material, arbitrary documents, model
  use, memory or Qdrant projection, public exposure, or operation; or
- acceptance, merge, execution, or dependency on pull request #63 or its
  separately Proposed ADR 0017.

## Success criteria

1. One implementation-ready plan defines the complete before-submission,
   approval, approved-only retrieval, grounded-answer, and reset journey.
2. Proposed ADRs 0018 through 0020 make the bounded sequencing, promotion,
   read-model, and deterministic-retrieval decisions explicit without changing
   current accepted architecture.
3. The threat model, validation requirements, dependency and salvage
   assessment, exact file manifest, work breakdown, and execution handoff agree.
4. Canonical status and navigation documents distinguish completed B0,
   authorized P1 planning, Proposed P1 design, and absent implementation,
   deployment, and information-use authority.
5. Historical pull requests #59 and #60 remain evidence only, and pull request
   #63 remains a separate noncanonical proposal.
6. `python scripts/validate_docs.py` and `git diff --check` pass for the exact
   documentation-only head.
7. One exact-head handoff is ready for independent architecture review and a
   later Chief Architect decision.

## Next authority gate

After the planning pull request is complete, work stops for independent
exact-head Work Mode architecture review under current ADR 0005. The Chief Architect must separately accept the
unchanged planning head and Proposed ADRs before they can become canonical.
Even a merged planning package grants no implementation authority; P1
implementation requires a later explicit authorization naming the canonical
planning merge commit and exact implementation scope.
