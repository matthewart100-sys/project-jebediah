# Organizational Intelligence Phase 3A Validation Requirements

**Status:** Proposed architecture validation contract

**Program phase:** Organizational Intelligence Product Program Phase 3A -
Executive Dashboard and Product Shell

**Planning date:** 2026-08-05

**Canonical planning base:**
`58f40054faba1167c25d828186e74d66e6c0681b`

**Decision owner:** Chief Architect

**Independent reviewer:** Work Mode

## Purpose

These requirements define the evidence needed to accept the proposed Phase 3A
architecture package and, after separate authorization, the Executive Product
Shell implementation.

They refine, but do not weaken, the accepted Organizational Intelligence
Validation Requirements. Every inherited evidence, provenance, uncertainty,
authority, lifecycle, safety, and failure-state rule remains binding.

Passing this contract demonstrates only a deterministic synthetic local product
shell. It does not validate live organizational intelligence, production
security, operational readiness, deployment, or executive usefulness with a
representative organization.

## Authority and evidence rules

1. Architecture and implementation reviews each apply to one immutable exact
   head.
2. The implementation author does not act as independent reviewer.
3. A changed head requires fresh validation and review.
4. Review evidence records exact base, head, commands, results, and limitations.
5. A passing test cannot authorize a capability excluded by architecture.
6. No validation may use a real organization, person, address, account, source,
   document, credential, private path, or private topology.
7. No test or smoke check may access an external or current runtime service.
8. Deployment, live-information, and implementation-merge authority remain
   separate decisions.

## Architecture package validation

Before architecture publication:

- ADR 0015, the Phase 3A plan, validation requirements, threat model,
  dependency assessment, and bounded authorization exist at one head.
- The package names outcome, non-goals, user journeys, routes, view models,
  state handling, synthetic boundary, threat controls, dependencies,
  accessibility, tests, rollback, stop conditions, and exact file scope.
- Current sprint, status, roadmap, architecture, repository standards,
  component registry, indexes, and Phase 2 terminal state agree.
- ADR 0015 remains Proposed.
- The Executive Product Shell remains Named.
- No implementation sprint or source-tree creation is claimed.
- No source, test, dependency, lock, service, workflow, container,
  infrastructure, or deployment file changes.

Required checks:

```text
git status --short --branch
uv run --frozen python scripts/validate_docs.py
git diff --check
git diff --name-only <base>...HEAD
```

The architecture manifest must exactly match the 19-file documentation-only
list in the Phase 3A plan.

### Decision activation validation

After Work Mode approves the Proposed exact head and the Chief Architect adopts
it, one bounded activation commit may:

- change the ADR, plan, validation, threat, dependency, and authorization
  statuses to their adopted states;
- record exact pull request, head, Work Mode disposition, and Chief Architect
  decision evidence;
- advance the Executive Product Shell from **Named** to **Specified** and assign
  Maintainer accountability;
- reconcile architecture, status, sprint, roadmap, changelog, indexes, and
  glossary with accepted-but-not-yet-implemented scope; and
- state that implementation authority becomes effective only after the exact
  activation head merges to canonical `main`.

It may not change a contract, route, model, state, dependency, threat control,
test, capability, authority boundary, rollback rule, stop condition, or file
manifest.

Because activation changes the head:

1. rerun every architecture-package check;
2. obtain a fresh **APPROVED** disposition from the same independent Work Mode
   reviewer;
3. obtain a separate Chief Architect decision approving the exact activation
   head for merge; and
4. merge only that unchanged activation head.

Assigning another reviewer is neither required nor permitted unless the original
reviewer fails under the documented replacement rule.

## Implementation validation layers

### Layer 0 - baseline

Before implementation:

- canonical `main` contains the accepted architecture package;
- the implementation branch starts from the recorded canonical merge commit;
- worktree is clean;
- `apps/jebediah_executive` is absent;
- architecture and authorization status are accepted and exact;
- documentation validation passes;
- frozen dependency resolution passes;
- all existing Python tests pass; and
- no real-information input is available to the work.

Commands:

```text
uv lock --check
uv run --frozen python scripts/validate_docs.py
uv run --frozen pytest
```

### Layer 1 - model contract

`test_models.py` must prove:

- all records are frozen;
- all collections are immutable;
- enum fields reject unknown values;
- item sections are exactly `happening`, `attention`, `know`, and `next`;
- evidence classifications are exactly `verified_fact`, `reported_fact`,
  `working_assumption`, `open_question`, or `derived_summary`;
- freshness is exactly `current`, `aging`, `stale`, `unknown`, or
  `not_applicable`;
- uncertainty is exactly `bounded`, `incomplete`, `conflicting`, `unknown`, or
  `not_applicable`;
- lifecycle is exactly `active`, `superseded`, or `archived`, and every ordinary
  briefing item is active;
- knowledge kind is required only for `know` and uses the exact five-value
  contract;
- next-item kinds are exactly `decision_required`, `organizational_gate`,
  `action_candidate`, or `informational_attention`;
- next kind is required only for `next` items;
- next context is required only for `next` items and matches the exact permitted
  context-to-kind table;
- decision owner remains optional and missing owner renders as not yet assigned;
- authority requirement and permitted next step are explicit for every
  `attention` and `next` item;
- permitted next step is only `navigate` or `human_review`;
- attention-to-next relationships reference existing same-briefing identities,
  are one-way, and reject self-reference, duplicates, cycles, and a
  `next_kind` on the attention item;
- display order is positive and unique inside each section;
- priority basis is required only for `attention` and `next`;
- review deadlines are missing or timezone-aware;
- evidence claims require one or more safe source references;
- missing evidence cannot be represented as grounded;
- derived items require transformation identity;
- timestamps are timezone-aware;
- freshness is derived from the fixed briefing clock rather than wall time;
- limitations and uncertainty explanations are non-empty;
- conflicting items retain all competing references;
- superseded, archived, held, rejected, failed, unauthorized, unavailable, and
  deleted records are not ordinarily eligible;
- coverage sets are sorted and unique, counts are derived, and held coverage
  exposes sanitized subject labels without held content;
- source references reject paths, URLs, locators, unbounded authority, and
  non-synthetic identities;
- every workspace kind-state pair matches the exact matrix in the plan;
- `eligible_for_briefing` is true only for `(source_record, eligible)` or
  `(knowledge_object, eligible)`;
- `accepted`, `ready`, and `review_approved` do not imply truth, general
  eligibility, action authority, or shell-owned transition behavior;
- activity entries use fabricated role labels and exact workspace result states;
- Ask response IDs are the three allowlisted presets, grounded responses require
  evidence, and insufficient or failed responses cannot contain an answer;
- priority, unresolved-decision, organizational-gate, upcoming-30-day-deadline,
  recent-30-day-evidence-update, and eligible-source counts are derived, never
  fixture-entered; and
- model construction rejects external URLs, file paths, free-form HTML,
  executable action verbs, and unsafe identities.

### Layer 2 - synthetic fixture

`test_fixtures.py` must prove:

- the only ordinary scenario is `synthetic-nonprofit-demo-v1`;
- every identity is visibly synthetic and stable;
- the fixture is byte-for-byte deterministic across constructions;
- the fixed clock is unchanged by system time;
- no real-looking organization, person, address, account, locator, credential,
  source, or document identifier is present;
- all four executive sections have eligible content;
- all four next-item kinds are represented;
- all five knowledge kinds and all five permitted next contexts are represented;
- attention items link to separate next records without carrying `next_kind`;
- bounded, incomplete, conflicting, unknown, and not-applicable uncertainty
  examples are represented;
- current, aging, stale, unknown, and not-applicable freshness are represented;
- missing, conflicting, stale, held, unavailable, and partial evidence are
  represented;
- every count on the overview derives from the same fixture;
- every preset Ask response cites exact fixture references or returns
  insufficient or failed;
- no fixture content claims a current organizational state; and
- no current runtime package is imported or invoked.

### Layer 3 - rendering

`test_rendering.py` must prove:

- every rendered document has a unique title, language, charset, viewport,
  skip link, header, navigation, main landmark, and footer;
- heading levels are ordered and each page has one level-one heading;
- current navigation state is visible and programmatic;
- the **Synthetic demonstration** and no-action labels appear on every page;
- fixed clock, coverage scope, limitations, and disconnected boundary are
  visible;
- evidence classification, safe references, freshness, uncertainty,
  limitations, and authority appear for every applicable item;
- attention remains informational attention and displays a related decision,
  gate, or action kind only from its separate linked next item;
- knowledge kinds, next kinds, and next contexts are presented in plain language
  without changing their enum value;
- source references are local disclosures rather than external links;
- conflicting evidence presents each competing source;
- missing evidence does not produce a positive claim;
- no uncertainty percentage, model confidence, retrieval score, truth score,
  or unsupported verification label appears;
- all fixture and route values are HTML-escaped;
- CSS is local, bounded, and contains visible focus, responsive, reduced-motion,
  and print rules;
- ready, loading, empty, partial, stale, insufficient, held, failed,
  unauthorized, unavailable, and disconnected states are distinguishable
  without color alone; and
- Ask responses display grounded, insufficient, or failed state plus evidence,
  coverage, uncertainty, limitations, synthetic status, and no-action boundary;
  and
- `grounded` is explicitly limited to cited eligible fabricated-fixture records
  and never presented as real-world verification, completeness, or action
  safety.

### Layer 4 - route and application behavior

`test_routes.py` and `test_app.py` must prove:

- only these routes or fixed subroutes resolve:

  ```text
  /
  /attention
  /knowledge
  /next
  /workspace
  /ask
  /ask/<allowlisted-preset-id>
  /board
  /states
  /states/<allowlisted-state-id>
  /static/styles.css
  ```

- route matching uses decoded, normalized allowlists;
- traversal, encoded traversal, backslashes, duplicate separators, null bytes,
  and unknown route values return a safe 404;
- GET returns expected content;
- HEAD returns matching status and headers with an empty body;
- POST, PUT, PATCH, DELETE, CONNECT, OPTIONS, and TRACE return 405 with an
  explicit `Allow: GET, HEAD`;
- request bodies are never read;
- every query string returns 400;
- no query parameter supplies a selector, content, path, URL, host, file, or
  free-form prompt;
- Host and Origin headers do not affect content, links, redirects, response
  headers, route selection, or logs, and every product link remains relative;
- the application does not set a cookie or session;
- the application does not persist state;
- errors return a sanitized synthetic failure page;
- stylesheet bytes have a fixed content type and cannot select another file;
- responses include:
  - a restrictive Content Security Policy;
  - `Referrer-Policy: no-referrer`;
  - `X-Content-Type-Options: nosniff`;
  - `Cache-Control: no-store`;
  - no permissive cross-origin header; and
- the server entry point binds literal `127.0.0.1`, exposes no host override,
  accepts only an integer port from 1024 through 65535, and fails visibly on
  bind error;
- the request handler replaces the standard server's raw request-line logging
  and records only method, normalized allowlisted route identity or
  `unrecognized`, and status; and
- captured logs never contain raw path, query, headers, body, fixture content,
  control characters, or an unknown identifier.

### Layer 5 - executive workflows

Component tests must prove these complete synthetic workflows:

1. **Executive orientation**
   - open overview;
   - identify organizational status and limitations;
   - inspect an attention item and any separately linked next-item kind; and
   - follow its evidence reference.

2. **Decision preparation**
   - open next items;
   - distinguish a decision from an organizational gate and action candidate;
   - identify decision owner and authority requirement; and
   - observe that no execution control exists.

3. **Knowledge boundary**
   - open knowledge coverage;
   - distinguish known, missing, conflicting, stale, and held information; and
   - inspect safe lineage in the workspace.

4. **Ask boundary**
   - select a grounded preset and inspect evidence;
   - select an insufficient preset and observe no answer fabrication;
   - select a failed preset and observe visible failure; and
   - confirm no free-form input exists.

5. **Board preparation**
   - open board view;
   - inspect status, priorities, risks, opportunities, decisions, evidence, and
     limitations; and
   - print without losing labels or evidence references.

6. **Failure awareness**
   - open the state gallery;
   - inspect every required state; and
   - confirm each preserves the synthetic and no-action boundary.

### Layer 6 - accessibility and usability

`test_accessibility.py` and browser smoke evidence must cover:

- semantic region and heading structure;
- keyboard-reachable skip link and navigation;
- logical keyboard order;
- persistent visible focus;
- programmatic current-page state;
- descriptive link and disclosure names;
- status and error text independent of color;
- fixed design tokens reproduce the documented contrast ratios;
- normal text meets 4.5:1 and large text and non-text indicators meet 3:1;
- non-inline interactive targets are at least 44 by 44 CSS pixels;
- text usable at 200 percent browser zoom;
- narrow layout at 320 CSS pixels without hidden required content or
  two-dimensional page scrolling;
- wide layout at 1280 CSS pixels without excessive line length;
- reduced-motion behavior;
- board print preview retaining evidence, limitations, and synthetic label; and
- plain-language review of each page against the target-user description.

These checks provide bounded engineering evidence and do not claim WCAG
certification or representative-user validation.

### Layer 7 - security, privacy, and isolation

Tests and static checks must prove:

- no socket client, HTTP client, subprocess, dynamic import, template engine,
  parser, scanner, model, vector, database, serialization store, or filesystem
  content-read capability exists in the package;
- only the reviewed CSS resource is opened by the package;
- the server host is not configurable;
- no environment variable, credential, cookie, session, identifier, content, or
  request body is logged;
- no form, textarea, editable field, upload control, or drag-and-drop target
  renders;
- no external URL or subresource is present;
- no current Collector, registry, memory, model, service, workflow, or
  integration package is imported;
- no protected runtime package or test changes; and
- no real or sensitive value enters source, tests, documentation, screenshots,
  logs, commit messages, PR text, or review evidence.

### Layer 8 - package and dependency boundaries

`test_package_boundaries.py` must inspect the full Executive Product Shell
source tree and reject:

- imports outside the Python standard library and package-local modules;
- imports from `collector`, `jebediah_memory`, current service packages, Qdrant,
  Ollama, FastAPI, Uvicorn, or workflow integrations;
- dynamic imports;
- executable shell or subprocess surfaces;
- outbound socket or HTTP clients;
- persistence or database clients;
- file-content reads other than the exact package-local CSS path;
- dependency metadata or lock changes;
- unexpected generated artifacts; and
- source files outside the exact implementation manifest.

### Layer 9 - regression and repository integrity

Required implementation-head commands:

```text
uv run --frozen pytest tests/apps/jebediah_executive
uv run --frozen pytest
uv run --frozen python -m compileall -q apps/jebediah_executive tests/apps/jebediah_executive
uv lock --check
uv run --frozen python scripts/validate_docs.py
git diff --check
```

Additional manifest checks must prove:

- exactly 31 authorized implementation files changed;
- exactly 9 application files, 9 test files, and 13 direct documentation files
  changed;
- no dependency, lock, service, workflow, container, infrastructure, deployment,
  or protected package file changed; and
- no untracked implementation artifact remains.

## Browser smoke procedure

Browser smoke validation uses a clean local process and no external system.

1. Start the exact reviewed application:

   ```text
   uv run --frozen python -m apps.jebediah_executive --port 8765
   ```

2. Verify the process reports only loopback location and synthetic boundary.
3. Open `http://127.0.0.1:8765/`.
4. Complete all six executive workflows.
5. Check 320- and 1280-CSS-pixel layouts, 200 percent zoom, keyboard-only
   navigation, visible focus, reduced motion, and board print preview.
6. Inspect browser network activity and confirm every request targets
   `127.0.0.1:8765` and only allowlisted paths.
7. Request one unknown route and verify safe 404.
8. Stop the process cleanly.
9. Confirm no file, cookie, storage record, cache commitment, or external
   request was created.

The PR records exact head, browser and operating-system versions, date, steps,
pass/fail result, and limitations. Screenshots, if used, contain only the
fabricated scenario and remain review evidence rather than product validation.

## Failure-injection matrix

| Injected condition | Required result |
| --- | --- |
| Unknown route | 404, sanitized page, no path reflection |
| Unsupported method | 405, `Allow: GET, HEAD`, body unread |
| Any query string | 400, visible invalid-request state, no raw query log |
| Invalid state ID | 404, no dynamic lookup |
| Invalid Ask preset ID | 404, no fallback answer |
| Unsafe fixture text in renderer test | Escaped literal text |
| Briefing model invariant violation | Typed construction failure |
| Held evidence | Visible held state, excluded from ordinary claim |
| Missing evidence | Insufficient state, no generated conclusion |
| Conflicting evidence | All conflicts and uncertainty visible |
| Stale evidence | Absolute freshness and limitation visible |
| Internal renderer failure | Sanitized failed state, no traceback |
| Port outside allowed range | Startup failure before bind |
| Port already in use | Visible startup failure and non-zero exit |

## Content assertions

Automated checks must reject:

- a claim that synthetic data is live, current, verified, complete, production,
  operational, or organization-specific;
- a claim that Jebediah decided, approved, commanded, executed, sent, submitted,
  changed, or completed an organizational action;
- omniscience language;
- unlabeled inference or recommendation;
- a source reference without safe synthetic identity;
- uncertainty expressed as a truth probability;
- action controls or action-success language;
- real organization names or personal information; and
- private paths, addresses, ports other than the documented local example,
  credentials, or topology.

## Review gates

### Architecture review

Work Mode returns exactly one disposition:

- **APPROVED**
- **REVISIONS REQUIRED**
- **BLOCKED**

Findings are categorized Blocking, High, Medium, or Low and cite exact
repository evidence. The Chief Architect decision follows only on the unchanged
approved head.

### Implementation review

The independent reviewer receives:

- exact base and head;
- complete diff;
- changed-file manifest;
- command results;
- browser smoke record;
- threat-control evidence;
- dependency and import evidence;
- known limitations; and
- confirmation that no real information was accessed.

No implementation merge occurs without exact-head Work Mode approval and a
separate exact-head Chief Architect merge decision.

## Post-merge validation

Immediately after implementation merge:

- fetch and identify exact canonical merge commit;
- verify expected source and documentation;
- rerun targeted tests, full suite, compilation, frozen lock, documentation,
  whitespace, exact manifest, package boundaries, sensitive-value scan, and
  capability-negative checks;
- repeat the local browser smoke procedure;
- confirm clean worktrees; and
- publish one terminal closeout if canonical governance requires it.

Do not create a recursive closeout.

## Completion criteria

Phase 3A is terminally complete only when:

1. accepted architecture and authorization are canonical;
2. the complete local synthetic shell is merged;
3. all automated and browser evidence passes;
4. Work Mode approved the exact implementation head;
5. the Chief Architect approved the exact implementation head for merge;
6. post-merge read-back passes;
7. one terminal documentation closeout is merged;
8. no unresolved Blocking, High, or Medium finding remains;
9. no real information was accessed;
10. no deployment occurred; and
11. no recursive closeout remains.

Until then, the product is a repository candidate or local preview, not an
Operational organizational-intelligence system.
