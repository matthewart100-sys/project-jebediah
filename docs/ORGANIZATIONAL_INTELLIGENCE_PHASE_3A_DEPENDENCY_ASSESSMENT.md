# Organizational Intelligence Phase 3A Dependency Assessment

**Status:** Proposed

**Decision:** Standard-library-only Phase 3A implementation

**Date:** 2026-08-05

## Purpose

This assessment determines whether the Executive Product Shell requires a new
framework, package manager, runtime dependency, frontend dependency, or lock-file
change.

## Repository baseline

- Python 3.12 or newer is already required.
- The root project uses `pytest` for tests.
- No JavaScript package manifest, frontend build chain, or browser framework
  exists.
- FastAPI and Uvicorn are selected only for existing bounded service contexts.
- The root lock contains the current Python dependency graph.
- No dashboard package, design system, template engine, accessibility engine, or
  browser test dependency is selected.

Existing dependency presence does not authorize reuse across an unrelated
component boundary.

## Required capabilities

Phase 3A needs:

- immutable typed view models;
- deterministic synthetic fixtures;
- route parsing and dispatch;
- safe HTML escaping;
- semantic HTML rendering;
- one reviewed local stylesheet;
- loopback-only local HTTP preview;
- safe response headers;
- deterministic unit and component tests; and
- local browser smoke validation.

It does not need:

- client-side state management;
- bundling or transpilation;
- virtual DOM or hydration;
- database or cache;
- authentication;
- WebSocket or background jobs;
- model, retrieval, or vector clients;
- document parsing; or
- production hosting.

## Options

### Python standard library

Candidate modules:

- `dataclasses`
- `enum`
- `html`
- `http`
- `importlib.resources`
- `json`
- `logging`
- `time`
- `typing`
- `urllib.parse`
- `wsgiref.simple_server`

**Benefits:** Existing runtime, no dependency or lock change, deterministic
contract tests, minimal supply-chain surface, direct safe rendering, and simple
rollback.

**Costs:** Limited routing and template ergonomics, no production hardening, and
repository-owned accessibility checks.

### Existing FastAPI dependency

**Benefits:** Established request routing and response types.

**Costs:** It belongs to existing development/service contexts, implies a
service-shaped boundary, still needs HTML templating decisions, and provides no
value required by the fixed synthetic route set.

**Disposition:** Not selected.

### Jinja or another template engine

**Benefits:** Familiar template organization and escaping features.

**Costs:** New dependency and template execution surface for a small fixed
renderer. Project-critical escaping would move behind a new boundary.

**Disposition:** Not selected.

### React, Vue, Svelte, or another browser framework

**Benefits:** Component ecosystem and rich client interactions.

**Costs:** New language toolchain, package manifest, transitive graph, build
artifacts, browser state, supply-chain ownership, and upgrade work. None is
required for the server-rendered synthetic experience.

**Disposition:** Not selected.

### Third-party accessibility or end-to-end browser tooling

**Benefits:** Broader automated standards and interaction coverage.

**Costs:** New browser/runtime dependencies and CI configuration. The first
bounded implementation can combine semantic markup, repository-owned checks,
HTTP component tests, and integrated-browser manual smoke evidence.

**Disposition:** Deferred. A later accepted tool may be added if repository-owned
checks prove insufficient.

## Selected dependency boundary

Phase 3A uses:

- the existing Python interpreter;
- Python standard-library runtime modules;
- existing `pytest` test infrastructure; and
- the existing documentation validator.

It adds:

- no runtime dependency;
- no development dependency;
- no frontend package;
- no external asset;
- no package manager;
- no build step;
- no generated bundle;
- no container;
- no GitHub Action; and
- no lock-file change.

The implementation must not modify:

- `requirements.txt`;
- `uv.lock`;
- service requirement files; or
- dependency groups in `pyproject.toml`.

The implementation may add an `apps/` source tree only after ADR 0015 is
accepted. It does not add a distributable package or change the Collector
distribution.

## License and provenance

No new third-party artifact or license is introduced. HTML, CSS, Python source,
fixtures, and tests are authored project artifacts. No remote font, icon,
image, stylesheet, script, or copied design-system asset is permitted.

## Update and removal ownership

The Maintainer is accountable for the repository implementation. Standard
library compatibility follows the project Python version policy. Removal is a
reviewed revert or deletion of the bounded app, tests, and direct
documentation.

## Validation

Implementation validation must prove:

- dependency and lock manifests are byte-for-byte unchanged;
- application source imports only allowlisted standard-library modules and its
  own package;
- no external URL or asset reference exists;
- no frontend build artifact exists; and
- the full existing frozen-lock verification still passes.

## Reconsideration triggers

Return to architecture and dependency review if Phase 3A cannot meet an accepted
requirement without:

- client scripting;
- a production HTTP server;
- a template engine;
- authentication;
- a database or saved state;
- a browser automation package;
- a design-system package;
- a new Python dependency; or
- a JavaScript package manifest.

No such need is currently supported by repository evidence.
