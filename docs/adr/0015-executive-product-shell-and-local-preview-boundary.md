# ADR 0015: Executive Product Shell and Local Preview Boundary

**Status:** Accepted

**Decision level:** System

**Date:** 2026-08-05

**Decision owner:** Chief Architect

**Required reviewers:** Independent Work Mode architecture review, then Chief
Architect final decision

## Decision summary

Define the **Executive Product Shell** as a new human-experience component that
renders an immutable evidence-bearing executive briefing and owns only
presentation, navigation, and deterministic synthetic demonstration behavior.

For Phase 3A, implement it as a Python 3.12-or-newer, standard-library-only,
server-rendered application under `apps/jebediah_executive`. Its development
preview binds only to `127.0.0.1`, accepts no files or free-form organizational
content, uses no external service, persists no state, and consumes only compiled
synthetic briefing fixtures.

This decision specifies a local product demonstration boundary. It does not
specify the future production read-model assembler, live transport,
authentication, deployment, or organizational-information authority.

## ADR trigger and level

ADR 0012 deliberately left the concrete executive component, presentation
technology, read-model interface, and hosting boundary unresolved. Phase 3A
must choose those responsibilities before implementation.

The choice is a **System** decision because it establishes:

- a stable component name and responsibility;
- a new `apps/` source boundary;
- a human-facing trust boundary;
- a local preview process and interface contract; and
- a lasting dependency and packaging direction.

## Context

### Repository Verified

- Canonical `main` at
  `58f40054faba1167c25d828186e74d66e6c0681b` contains no frontend framework,
  browser application, JavaScript package manifest, or executive-interface
  implementation.
- ADR 0012 accepts a read-only executive interface over an evidence-bearing
  read model and forbids presentation from acquiring source, verification,
  ingestion, derivation, or action authority.
- The accepted interface contract requires `happening`, `attention`, `know`,
  and `next` sections; evidence, freshness, uncertainty, limitations, and
  degraded states; and deterministic usefulness without a model.
- Knowledge Manager 1.0 Phase 2 is terminally closed. Its document-admission
  package is synthetic-only, disconnected, non-operational, and accepts no live
  input.
- The root Python project requires Python 3.12 or newer. The repository already
  uses `pytest`, but no frontend or accessibility dependency is selected.

### Reported facts

- No deployment environment, production browser support matrix, identity
  provider, operational owner, or live organizational source has been verified.

### Working assumptions

- A local, server-rendered demonstration can validate the four-question
  executive experience without selecting production transport or deployment.
- Progressive enhancement is unnecessary for the first synthetic shell if all
  routes and interactions work with ordinary links over loopback.
- A dependency-free implementation is sufficient for the bounded Phase 3A
  product and reduces supply-chain and build risk.

### Open questions

| Question | Resolution gate |
| --- | --- |
| Which component assembles production organizational read models? | Separate component specification before any live adapter |
| Which users may view each class of organizational information? | Authentication, authorization, classification, and information-owner decision |
| Which deployment topology and browser support policy apply? | Separate deployment and operations authorization |
| Is generated assistance appropriate for live use? | Separate interaction, model, privacy, evaluation, and cost decision |

These questions do not block a compiled synthetic local demonstration. They
block live information, production integration, and deployment.

## Scope

- Executive Product Shell component responsibility
- Phase 3A source and application boundary
- Immutable synthetic briefing input contract
- Local loopback preview behavior
- Server-rendered navigation and interaction strategy
- Security, data, dependency, recovery, and test boundaries

## Non-goals

- Real organizational information, files, or free-form content
- A production read-model assembly component
- Collector, Knowledge Registry, Memory Service, Qdrant, Ollama, n8n, or Open
  WebUI integration
- Authentication, authorization, user management, analytics, or exports
- Durable state, cookies, sessions, preferences, or saved views
- Production hosting, TLS, network exposure, containerization, or deployment
- Autonomous action, approval, recommendation execution, or record mutation
- Phase 3B, 3C, or 3D implementation

## Decision drivers

- The primary user needs calm, readable, evidence-first orientation.
- Every displayed claim must preserve the accepted evidence and uncertainty
  contract.
- The shell must be runnable and testable without live services or information.
- The public repository must not gain unnecessary dependencies or generated
  build artifacts.
- The implementation must fail visibly and remain reversible.
- A local preview must not be mistaken for a deployable service.

## Considered alternatives

### JavaScript framework and client-side application

React, Vue, Svelte, or another framework could provide a mature component
ecosystem. This would introduce a new language toolchain, package manifest,
transitive dependencies, build output, client state, and supply-chain surface
before the product requires them.

**Disposition:** Rejected for Phase 3A. Reconsider only when an approved product
need cannot be met by the bounded server-rendered shell.

### FastAPI with a template engine

FastAPI exists in a current development/service dependency group and could serve
HTML. A template engine would still add or select another dependency, and using
the existing memory-service framework would risk implying a shared service,
deployment, or runtime boundary.

**Disposition:** Rejected for Phase 3A. Existing dependency presence does not
establish executive-product ownership or operational suitability.

### Static HTML and CSS only

Static pages would minimize runtime behavior but would not provide a strongly
typed briefing contract, deterministic route behavior, state validation, or a
testable interaction boundary.

**Disposition:** Rejected as the complete product shell. Static assets remain
part of the selected server-rendered design.

### Standard-library server-rendered local application

Python frozen dataclasses and enums can enforce the read-model contract.
`wsgiref.simple_server`, `html`, `urllib.parse`, and `importlib.resources` can
provide a loopback-only preview and safe rendering without a new dependency.
Ordinary links and allowlisted synthetic state and preset-response paths provide
complete keyboard operation without client scripting.

**Disposition:** Selected.

## Decision

### Component responsibility

The **Executive Product Shell** owns:

- semantic presentation of one immutable `ExecutiveBriefing`;
- route selection and navigation;
- evidence, uncertainty, freshness, limitation, and authority rendering;
- deterministic selection among compiled synthetic scenarios;
- local preview response headers and safe error presentation; and
- no authoritative or durable state.

The component does not own:

- source records or source truth;
- read-model production from live sources;
- factual verification or knowledge derivation;
- priority, uncertainty, lifecycle, or authority decisions;
- identity, access, retention, or deployment; or
- external actions.

Acceptance of this ADR and its component specification advances the Executive
Product Shell to **Specified**, not Implemented or Operational.

On acceptance, the Maintainer is accountable for the repository component. The
Lead Product Engineer acts only in the canonical Implementation Engineer role
for separately authorized implementation. No operational owner is assigned
because deployment and operation are excluded.

### Source and entry-point boundary

Phase 3A source is located under:

```text
apps/
    __init__.py
    jebediah_executive/
        __init__.py
        __main__.py
        app.py
        fixtures.py
        models.py
        rendering.py
        routes.py
        static/
            styles.css
```

The local entry point is:

```text
python -m apps.jebediah_executive
```

The preview:

- binds only to literal loopback address `127.0.0.1`;
- accepts an optional validated local port;
- provides no host override;
- uses GET and HEAD only;
- has no upload, body-processing, cookie, or session path;
- makes no network call;
- writes no file or database;
- logs only method, allowlisted route identifier, status, and duration; and
- is a development preview, not deployment or operational evidence.

### Briefing provider boundary

The application consumes a `BriefingProvider` protocol that returns an immutable
`ExecutiveBriefing`. Phase 3A includes exactly one implementation:
`SyntheticBriefingProvider`.

The synthetic provider:

- selects from compiled, versioned, obviously fabricated scenarios;
- accepts only allowlisted scenario and preset-question identifiers;
- never reads files, environment-provided content, URLs, databases, services,
  Collector records, registry records, memory records, or model output;
- never accepts free-form user content; and
- raises an explicit unavailable or not-found result for unknown identifiers
  without echoing them.

This provider is not the future production read-model assembler. A live adapter
requires a new accepted component and interface decision.

### Rendering boundary

Rendering uses semantic server-generated HTML and one local CSS asset. It uses
no JavaScript, remote font, image, stylesheet, analytics, or third-party asset.

Every dynamic string is escaped before HTML output. Routes, scenarios, and
preset questions are allowlisted identifiers. No input influences a filesystem
path, import, template name, response header, command, or external locator.

Responses include at least:

- `Content-Security-Policy` denying all external resources and framing;
- `Referrer-Policy: no-referrer`;
- `X-Content-Type-Options: nosniff`;
- `Cache-Control: no-store`; and
- a UTF-8 content type.

### Product routes

| Route | Responsibility |
| --- | --- |
| `/` | Executive overview and four-question summary |
| `/attention` | Attention queue and evidence-bearing review items |
| `/knowledge` | Coverage, known subjects, gaps, conflicts, stale and held information |
| `/next` | Bounded next-step and decision-support items |
| `/workspace` | Synthetic source, document, quarantine, review, lineage, and activity status |
| `/ask` and `/ask/<preset-id>` | Preset synthetic questions and one allowlisted evidence-grounded demonstration response |
| `/board` | Simplified board presentation view |
| `/states` and `/states/<state-id>` | Demonstration gallery and one allowlisted ready, loading, empty, partial, stale, insufficient, held, failed, unauthorized, unavailable, or disconnected state |
| `/static/styles.css` | Local reviewed stylesheet |

No trailing-slash alias or query string is accepted. No route mutates state or
executes an action.

### Information categories

| Information | Category | Owner in Phase 3A | Retention and recovery |
| --- | --- | --- | --- |
| Compiled synthetic briefing fixtures | Reviewed demonstration source artifact; not organizational truth | Executive Product Shell repository component | Git history; removed by reviewed revert |
| Rendered HTML response | Temporary derived presentation | Request process | Response lifetime only |
| Preset Ask response | Derived synthetic demonstration output | Executive Product Shell repository component | Compiled fixture; no runtime persistence |
| Route and status log fields | Temporary operational metadata | Local preview process | Process output only; no content or locator |
| Real organizational information | Prohibited | No owner assigned | Must not enter the component |

### Failure and degraded behavior

- Invalid routes return a calm, sanitized 404 page.
- Unknown scenario or question identifiers return explicit failed or
  insufficient-evidence state without echoing input.
- Fixture or contract failure stops application startup or returns unavailable;
  it never renders partial values as ready.
- Loading is a demonstration state, not a hidden background fetch.
- Empty state states scope and coverage.
- Partial, stale, insufficient, held, failed, unauthorized, unavailable, and
  disconnected states remain visibly distinct.
- The component has no last-known persistent state and therefore makes no
  recovery or backup claim.

## Consequences

### Positive

- The full product experience is locally runnable with no new dependency.
- View-model and authority invariants remain deterministic and testable.
- No browser build chain or client-side state is introduced.
- Local preview cannot silently connect to current runtime candidates.
- Rollback is a repository revert with no data or deployment cleanup.

### Negative

- Server-rendered interactions are less dynamic than a client framework.
- The local preview is unsuitable for network deployment.
- Accessibility checks use repository-owned static and interaction tests rather
  than a third-party audit engine.
- A future production interface may require a migration to another transport or
  frontend technology.

### Neutral

- The read-model semantics remain compatible with ADR 0012.
- The implementation language does not determine future deployment technology.
- Generated assistance remains simulated; no model boundary is selected.

## Security and privacy impact

The application creates a local human-facing rendering boundary but no approved
live disclosure boundary. The Phase 3A threat model owns concrete abuse cases.
Loopback-only binding, no free-form input, escaping, allowlisted routes, local
assets, safe headers, and no persistence minimize risk.

The preview provides no authentication and therefore must not be exposed on a
network or used with real information.

## Operations and recovery impact

If this ADR is accepted, the component becomes **Specified**, not Operational.
The implementation may prove local process start, route health, and clean
shutdown only. It must not claim availability, service objectives, backup,
deployment, monitoring, incident support, or production recovery.

Rollback deletes or reverts the bounded source, tests, and documentation. There
is no migration, durable state, external resource, credential, or service to
recover.

## Compatibility and migration

No existing runtime imports the new component, and the component imports no
Collector, Knowledge Registry, memory, service, Qdrant, Ollama, or workflow
module. Existing packages, APIs, dependencies, and lock files remain unchanged.

The future production read-model interface may replace the synthetic provider
only through a separately accepted versioned contract and migration plan.

## Validation

Validation is defined in the
[Phase 3A Validation Requirements](../ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_VALIDATION_REQUIREMENTS.md).
Tests must cover models, fixtures, routes, rendering, headers, keyboard
navigation, accessibility structure, degraded states, package boundaries,
forbidden capabilities, and local browser workflows.

## Rollback

Before merge, abandon the branch. After merge, use a reviewed revert of the
bounded Phase 3A implementation and reconcile canonical documentation. No data,
credential, deployment, service, or external cleanup applies.

## Follow-up gates

- Fresh Work Mode review of the status-activation head
- Chief Architect exact activation-head architecture merge decision
- Canonical architecture merge before implementation starts
- Independent implementation review and exact-head merge approval
- Terminal Phase 3A closeout
- Separate decisions for any live adapter, real information, authentication,
  deployment, model, action, or Phase 3B work

## Supersession

**Supersedes:** None

**Superseded by:** None

## Review record

One independent read-only Work Mode reviewer approved exact planning head
`5aa79d0d8f8aeab89d4a0acc4056a8f94ce329d7` with no Blocking, High, Medium, or
Low findings. The Chief Architect accepted this ADR and authorized only the
bounded status-and-decision-evidence activation edit on 2026-08-05.

Because activation changes the head, architecture merge remains gated by fresh
review from the same Work Mode reviewer and a separate Chief Architect exact-head
merge decision.
