# JCS Specification

**Status:** Proposed

**Component maturity:** Named

**Decision state:** JCS-01 through JCS-10 unresolved; no accepted JCS ADR

**Last reviewed:** 2026-07-31

## Review warning

This artifact is a Milestone C1 decision-framing proposal. It is not current
architecture and does not define what `JCS` stands for, assign JCS a
responsibility, approve information authority, establish a consumer contract,
or authorize implementation.

Statements labeled **Proposed** are candidates for review. They become
authoritative only after the required evidence, ADRs, Chief Architect review,
maintainer decision, canonical integration, and merge gates in the
[JCS Definition Implementation Plan](JCS_DEFINITION_PLAN.md) are satisfied.

## Purpose of this proposal

This first proposal gives maintainers and reviewers one substantive artifact
for deciding whether JCS should exist, which problem could justify a component
boundary, and what evidence is still missing. It owns the proposed JCS
definition as it evolves through Phase 1. Existing canonical documents retain
authority for architecture, terminology, data, security, operations, testing,
and project status until accepted decisions update them.

Milestone C1 requires this proposal to cover:

- Evidence and uncertainty
- Name and purpose alternatives
- Scope and explicit non-goals as proposals
- Responsibility alternatives
- Consumer hypotheses
- JCS-01 through JCS-10 decision framing
- ADR trigger assessment
- Evidence needed for the next gate

Later milestones may add accepted information, interaction, lifecycle,
security, operations, and assurance requirements only after their
prerequisites are met.

## Authority and roles

| Responsibility | Current owner |
| --- | --- |
| Project purpose and final decisions | Maintainer |
| Architectural framing and required review | Chief Architect |
| Evidence gathering, proposal quality, and validation | Lead Engineer |
| JCS component ownership | Unassigned pending specification |
| JCS information ownership | Unassigned; no domain is assigned to JCS |
| JCS operational ownership | Unassigned; no runtime exists |

The Chief Architect may review decision quality but does not manufacture
maintainer intent. The Lead Engineer may compare alternatives but does not
select project purpose. A proposal cannot grant itself authority.

## Evidence and uncertainty

### Verified facts

- Reviewed GitHub `main` is authoritative engineering memory.
- Project Genesis is complete and the documentation-only `v0.1.0` foundation
  release is published.
- The repository contains no Project Jebediah application, infrastructure
  definition, runtime schema, product workflow, or product test.
- `JCS` is a preserved working name for a future foundational subsystem at
  **Named** maturity.
- Current canonical documentation leaves the JCS expansion, purpose,
  responsibility, information authority, consumers, interfaces, guarantees,
  deployment, and implementation unresolved.
- The roadmap requires an accepted JCS specification before collector
  dependency.
- The active plan authorizes a **Proposed** specification and proposed ADRs
  only during Milestone C1.
- No numbered Project Jebediah ADR has been accepted.

### Reported facts

Bootstrap material reports broader intent for a local-first AI platform and
future collectors, knowledge, Digital Twin, automation, and reasoning
capabilities. It also reports a home-lab environment containing named products
and infrastructure. These reports do not define JCS, prove a consumer need,
or assign any product a role.

A C1 inquiry through the user-designated Chief Architect reported that no
explicit maintainer statement was available for:

- The JCS expansion
- The exact problem JCS should solve
- The responsibility JCS should own
- Explicit responsibility exclusions
- Intended JCS consumers

This is a reported inquiry result, not proof that no historical statement ever
existed. The specification treats each item as **Unknown** until the maintainer
provides an explicit decision through the approved collaboration path.

### Working assumptions

| Assumption | Bounded use | Risk | Confirmation or invalidation |
| --- | --- | --- | --- |
| `JCS` can remain a neutral working label during C1. | Keeps repository references stable while alternatives are compared. | The acronym may bias reviewers toward an unsupported meaning. | JCS-01 explicitly compares retain, expand, rename, and defer alternatives. |
| Responsibility should drive the final name. | Orders analysis without selecting a responsibility. | The maintainer may already intend a name or problem not present in current evidence. | Explicit maintainer input confirms or replaces the ordering. |
| One coherent responsibility is preferable to an umbrella "core." | Applies approved architecture principles to alternative evaluation. | A real cross-cutting responsibility may be rejected too early. | Alternatives must show a named consumer, authority boundary, and consequence before reviewers narrow them. |
| C1 can be useful without selecting a winner. | Produces a reviewable decision package despite missing maintainer intent. | The proposal could be mistaken for progress without a decision. | C1 acceptance requires explicit framing review and a recorded evidence gap; later milestones remain gated. |

### Open questions

Every JCS decision remains open. The [decision register](#decision-register)
owns its evidence need and gate. Missing maintainer intent blocks acceptance of
JCS-01 and JCS-02; it does not block comparing alternatives.

## Repository-constrained requirements

These requirements are already binding because their canonical owners are
accepted. They constrain the proposal without supplying the missing JCS
answer.

1. JCS must be defined and specified before implementation or collector
   dependency.
2. A component boundary must own one coherent responsibility, state,
   lifecycle, failure isolation, and operational accountability.
3. Scope, non-goals, consumers, and dependencies must be explicit.
4. Information authority must be assigned by concrete domain; no component is
   authoritative by implication.
5. Conceptual interactions must define meaning, validation, failure,
   compatibility, authority, and observability before implementation syntax.
6. Trust boundaries, least privilege, data minimization, safe failure, and
   human authority must remain explicit.
7. Durable guarantees require owned recovery and proportionate validation.
8. Reported products and infrastructure must not drive the conceptual
   contract before verification and review.
9. JCS remains **Named** until the complete specification and triggered ADRs
   are accepted.
10. Specification activity is not implementation or operational evidence.

## Evaluation criteria

Reviewers will compare each alternative against the same criteria.

| Criterion | Question |
| --- | --- |
| Problem necessity | Is there a concrete problem that existing conceptual owners do not already cover? |
| Responsibility coherence | Can the responsibility be stated without "and everything else" clauses? |
| Consumer evidence | Is there a named person or future component with a specific need? |
| Boundary clarity | What remains owned by collectors, knowledge, Digital Twin, automation, reasoning, user experience, and repository governance? |
| Information authority | Can authority remain explicit and domain-specific rather than defaulting to JCS? |
| Failure independence | Does a JCS boundary clarify failure, or create a central point with unclear consequences? |
| Local-first alignment | Does the option preserve controlled authority, replaceability, and recovery without forcing deployment? |
| Simplicity | Is a new component justified over retaining the current undefined state or placing responsibility elsewhere? |
| Testability | Could a future implementation demonstrate its guarantees without relying on subjective success? |
| Evolution | Can the boundary change through owned contracts without making every later component depend on internals? |

## JCS-01: name and problem alternatives

**Decision status:** Open

**Maintainer intent:** Unknown

**Current conclusion:** No specific expansion of `JCS` is supported by
repository or explicit maintainer evidence.

### Alternative A: retain `JCS` as an unresolved working label

Continue using the current label while purpose, responsibility, and boundaries
are investigated.

**Potential value:** Preserves documentation continuity and lets the problem
drive terminology.

**Risk:** Readers may infer meaning or centrality from the acronym.

**Evidence needed:** Maintainer purpose, consumer problem, and responsibility
analysis.

### Alternative B: expand `JCS` after a purpose is supported

Select an expansion only after evidence supports the underlying problem and
responsibility. No candidate expansion is proposed yet.

**Potential value:** A meaningful expansion may improve communication while
preserving the familiar label.

**Risk:** An acronym-first process may force the architecture to fit a desired
name.

**Evidence needed:** Accepted purpose, explicit maintainer intent, and a
comparison showing the expansion describes the selected responsibility.

### Alternative C: rename the subsystem after responsibility is accepted

Replace `JCS` with a descriptive name derived from the accepted boundary.

**Potential value:** Best protection against legacy naming bias.

**Risk:** Requires migration of repository references and may reduce continuity
during the transition.

**Evidence needed:** Accepted responsibility boundary and terminology-impact
review.

### Alternative D: defer the final name until specification acceptance

Use a neutral working label through Phase 1 and select the final name only
when the complete contract is ready for acceptance.

**Potential value:** Preserves maximum decision flexibility.

**Risk:** Extends temporary ambiguity and makes intermediate discussion less
intuitive.

**Evidence needed:** Milestone C4 consistency review and maintainer decision.

## Candidate problem hypotheses

These hypotheses exist to test whether a JCS component boundary is justified.
They are not statements of project need.

| Hypothesis | Question to test | Evidence required | Current status |
| --- | --- | --- | --- |
| Coordination gap | Do separately owned future components require one bounded coordinator rather than direct contracts or an existing automation owner? | Named participants, coordination state, failure consequence, and alternatives | Unsupported hypothesis |
| Context-continuity gap | Is there durable context that no knowledge, repository-memory, or reasoning owner should hold? | Concrete information, authority, lifecycle, consumer, and overlap analysis | Unsupported hypothesis |
| Contract/governance gap | Does a runtime or conceptual owner need to enforce cross-component guarantees beyond repository governance? | Enforced behavior, consumers, authority, and failure evidence | Unsupported hypothesis |
| Another bounded problem | Does maintainer intent identify a different coherent problem? | Explicit maintainer statement and repository compatibility review | Unknown |
| No JCS problem | Can the named future subsystem be removed or deferred because other owners cover every demonstrated need? | Consumer review and consequence of no component | Credible baseline |

The no-JCS or defer alternative remains credible. A preserved name does not
prove that a component should exist.

## JCS-02: responsibility alternatives

**Decision status:** Open

**Dependency:** JCS-01 problem framing and explicit maintainer intent

### Alternative A: retain undefined responsibility

Keep JCS at **Named** maturity and make no responsibility assignment.

**Potential value:** Avoids accidental architecture while evidence is missing.

**Risk:** Collector and later subsystem planning cannot rely on JCS.

**Required evidence to leave this alternative:** A specific problem, consumer,
and boundary that justify a separate component.

### Alternative B: bounded coordination responsibility

**Proposed hypothesis:** JCS could coordinate a specifically named interaction
between independently owned components.

**Potential value:** May centralize one real coordination policy and make
partial failure visible.

**Risks:** Can become an "everything manager," duplicate Automation, or create
unnecessary central coupling.

**Required evidence:** Named participants, precise coordination responsibility,
state ownership, human authority, failure consequence, and comparison with
direct contracts and Automation ownership.

### Alternative C: bounded context-continuity responsibility

**Proposed hypothesis:** JCS could own a narrowly defined continuity concern
that is not repository memory, source collection, knowledge representation,
Digital Twin state, or model context.

**Potential value:** May give one owner to a real cross-session or
cross-component continuity problem.

**Risks:** Overlaps the AI Memory Contract, Knowledge Graph, Digital Twin,
Reasoning Engine, or an authoritative data owner; may silently collect broad
personal or project information.

**Required evidence:** Concrete information domain, authoritative source,
consumer, retention, privacy, deletion, failure, and proof that existing owners
do not cover it.

### Alternative D: bounded contract or runtime-governance responsibility

**Proposed hypothesis:** JCS could own enforcement of a small set of runtime
guarantees or cross-component rules rather than business processing.

**Potential value:** May keep important guarantees explicit and independently
testable.

**Risks:** Confuses repository governance with runtime behavior, adds a
component without an operational need, or becomes a policy catch-all.

**Required evidence:** Specific enforceable rule, affected consumers, runtime
authority, failure mode, and why each participant cannot enforce its own
contract.

### Alternative E: another coherent responsibility

Allow an evidence-backed responsibility not represented above.

**Potential value:** Avoids constraining discovery to inherited hypotheses.

**Risk:** A vague escape hatch may bypass disciplined comparison.

**Required evidence:** The same problem, consumer, boundary, authority,
failure, simplicity, and testability evidence required for every alternative.

## Proposed scope of the final specification

The following is a proposal for what the accepted specification should
eventually own, regardless of which JCS alternative is selected:

- Confirmed name and problem
- One coherent responsibility and explicit exclusions
- Component and operational ownership
- Named consumers and dependencies
- Concrete information responsibility, including an explicit "none" where
  appropriate
- Implementation-independent interaction requirements
- Failure, degraded-state, stale-state, retry, and recovery guarantees
- Trust, security, privacy, and human/AI authority boundaries
- Configuration, health, observability, lifecycle, and retirement expectations
- Risk-based conformance and future implementation acceptance criteria
- Accepted ADR links and deferred decision list

This scope proposal does not claim that JCS will own each category. It requires
the accepted specification to answer each category or explain why it does not
apply.

## Proposed non-goals

Unless a later evidence-backed decision deliberately changes the boundary, the
JCS specification should explicitly avoid treating JCS as:

- A synonym for Project Jebediah as a whole
- An owner of all project information or engineering memory
- A generic database, vector store, knowledge graph, cache, or model memory
- The Collector Engine or owner of every source integration
- The Digital Twin or authoritative copy of represented state
- The Automation capability or a general workflow engine
- The Reasoning Engine, AI persona, prompt history, or autonomous decision
  maker
- The infrastructure, service mesh, container platform, host manager, or
  deployment control plane
- Automatic permission to act on authoritative, derived, stale, or model
  information
- A reason to select a language, protocol, schema, database, model, or
  deployment during definition framing

These are **Proposed** exclusions for review, not accepted JCS boundaries.

## Consumer hypotheses

No consumer dependency is approved. Each row is a question that a later
decision must confirm or reject.

| Potential consumer | Hypothesized need | Evidence required | Current status |
| --- | --- | --- | --- |
| Maintainer or operator | Understand or control one bounded project concern | Named decision or operational task and consequence | Unknown |
| Collector Engine | Rely on a pre-existing conceptual guarantee | Exact guarantee and why Data Ownership plus a direct contract are insufficient | Dependency prohibited pending specification |
| Knowledge Graph | Receive or resolve defined state or identity | Concrete domain, source, owner, and relationship boundary | Unknown |
| Digital Twin | Consume stable information with authority and freshness | Approved Digital Twin use case and source mapping | Deferred by Digital Twin entry gates |
| Automation | Observe a trusted condition or request a bounded coordination action | Separate information and action authority plus failure behavior | Unknown; no action authorized |
| Reasoning Engine | Use validated context or system state | Evidence, provenance, permissions, freshness, and evaluation need | Unknown |
| User experience | Explain one JCS-owned state or request human approval | Defined human task and interpretation risk | Unknown |

The list does not prove that these components should depend on JCS. It exists
to make unsupported coupling visible.

## Decision register

| ID | Decision question | Current status | Evidence or decision needed | Gate |
| --- | --- | --- | --- | --- |
| JCS-01 | What does `JCS` stand for, and what problem does it solve? | Open; explicit maintainer intent unknown | Maintainer purpose, consumer problem, name alternatives | Chief Architect framing and maintainer decision |
| JCS-02 | What coherent responsibility does JCS own, and what is excluded? | Open; alternatives only | JCS-01 direction, consumer evidence, boundary comparison | Proposed System ADR before dependent boundaries |
| JCS-03 | Which information, if any, is JCS authoritative for? | Open; no authority assigned | Concrete domain, source, owner, conflict, freshness, retention, recovery | Milestone C2 data review and accepted ADR as triggered |
| JCS-04 | Who consumes JCS guarantees, and what remains owned elsewhere? | Open; hypotheses only | Named consumer, exact need, alternative owner | Milestone C2 boundary review |
| JCS-05 | Which conceptual interactions are required? | Open; no interaction approved | Accepted responsibility and consumer need | Milestone C2; System ADR for cross-component contract |
| JCS-06 | What failure and recovery guarantees apply? | Open | Accepted responsibility, consequence, information category | Milestone C3 lifecycle review |
| JCS-07 | Which trust, privacy, and human/AI authority boundaries apply? | Open; foundation policy only | Concrete data and action consequences | Milestone C3 security review and ADR as triggered |
| JCS-08 | What must operators observe and own? | Open; no runtime owner | Deployment-independent operational questions and accepted boundary | Milestone C3 operations review |
| JCS-09 | What evidence proves implementation conformance? | Open | Accepted guarantees and representative failure cases | Milestone C3 assurance review |
| JCS-10 | Which technology and deployment choices remain deferred? | Open; all current choices deferred | Evidence that a choice is indispensable to the conceptual contract | Explicit deferral list; later ADR if required |

## ADR trigger assessment

No numbered ADR is created in this C1 proposal.

The repository has enough evidence to conclude that an accepted JCS
responsibility, information-authority, cross-component interaction, or trust
boundary would require a **System** ADR by default. A **Foundational** ADR is
required only if the choice changes project-wide principles, roadmap direction,
human authority, or an authority model inherited by several systems.

The repository does not yet have a proposed selected course for JCS-01 or
JCS-02. Creating a numbered ADR with an empty decision would violate the ADR
template and the no-placeholder rule. A proposed ADR should be created only
after maintainer intent and C1 framing identify a candidate decision precise
enough to compare and review.

| Decision | Current assessment | Why no ADR file exists yet |
| --- | --- | --- |
| JCS-01 name and problem | Likely System; Foundational only for project-wide change | No explicit maintainer intent or supported name/purpose candidate |
| JCS-02 responsibility and exclusions | System | No responsibility alternative is selected for proposal |
| JCS-03 information authority | System; possibly Foundational for project-wide authority | No concrete information domain or owner is proposed |
| JCS-04/JCS-05 consumers and interactions | System when a cross-component contract is proposed | No consumer need or interaction is established |
| JCS-07 trust and authority | System; Foundational if human or project-wide authority changes | No concrete data or action boundary is proposed |
| Technology and deployment | Later System or Implementation as consequence requires | Explicitly deferred and not needed for C1 framing |

## Evidence needed from the maintainer

The following questions cannot be answered from current repository evidence:

1. Was `JCS` intended to have a specific expansion, or is it a temporary
   label?
2. Which human or project problem motivated preserving JCS as a future
   subsystem?
3. What outcome would make JCS valuable?
4. Which responsibility should JCS own, if any?
5. Which responsibilities must it never absorb?
6. Which person or future component would first depend on its guarantee?
7. What failure would show that the JCS concept is unnecessary or wrongly
   bounded?

Until this evidence is promoted into the proposal and reviewed, JCS-01 and
JCS-02 cannot advance to a candidate decision.

## Deferred work

| Milestone | Work deliberately deferred from C1 | Entry condition |
| --- | --- | --- |
| C2 | Concrete information mappings, consumer boundaries, and conceptual interaction requirements | JCS-01/JCS-02 candidate direction and Chief Architect framing authorization |
| C3 | Failure, recovery, security, privacy, operations, and conformance requirements | Accepted or reviewable responsibility and information consequences |
| C4 | Current architecture, glossary, registry maturity, data ownership, roadmap, and changelog integration | Internally complete proposed specification and required ADRs |
| C5 | Specification acceptance and Phase 1 closure | Complete artifacts, passing checks, Chief Architect approval, maintainer authority |
| Later implementation | Schemas, APIs, protocols, code, tests, infrastructure, and deployment | Accepted specification plus separately approved implementation plan and sprint |

## C1 review questions

The Chief Architect framing review must answer:

- Does this proposal keep explicit maintainer intent **Unknown** rather than
  filling it with inference?
- Are the naming and problem alternatives credible and neutral?
- Are the responsibility alternatives coherent enough for maintainer review
  without becoming architecture claims?
- Is retaining or removing the JCS concept treated as a real alternative?
- Are proposed non-goals useful safeguards without pre-deciding the selected
  responsibility?
- Are consumer rows visibly hypotheses rather than dependencies?
- Are ADR levels proportionate, and is deferring numbered ADR creation
  justified?
- Which exact evidence is blocking a candidate direction?
- May Milestone C2 begin, or must JCS-01/JCS-02 remain in C1?

## C1 acceptance criteria

Milestone C1 is complete only when:

- This proposal remains substantive, **Proposed**, and non-authoritative.
- Verified facts, reports, assumptions, open questions, hypotheses, and
  proposed statements are distinguishable.
- No unsupported expansion, responsibility, information authority, consumer
  dependency, interaction, or technology is asserted.
- Alternatives include retain, rename, defer, another bounded responsibility,
  and no-JCS or no-change positions where credible.
- The JCS-01 through JCS-10 register identifies evidence, owners, and gates.
- The ADR assessment explains both likely levels and why no placeholder ADR is
  created.
- Documentation ownership and navigation identify this proposal without
  treating it as accepted architecture.
- Repository validation and `git diff --check` pass.
- The Chief Architect reviews the exact complete artifacts and returns a
  formal framing decision with every recommendation disposition recorded.

Milestone C1 completion does not accept a JCS definition. Dependent work may
begin only if the formal review identifies the exact next authorized scope.

## Maintenance

Update this proposal as evidence and decisions progress through the active
plan. Accepted choices must update their existing canonical owners and
required ADRs in the same reviewed change. Rejected alternatives remain
concise decision evidence; unresolved matters keep an owner and gate.

Do not leave an accepted JCS conclusion only in conversation or a pull-request
comment. Promote it into this specification, the applicable ADR, and every
affected current document before dependent work.
