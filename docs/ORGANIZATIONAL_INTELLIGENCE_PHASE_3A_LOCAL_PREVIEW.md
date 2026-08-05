# Organizational Intelligence Phase 3A - Local Preview Operator Guide

This guide explains how to run and inspect the Phase 3A Executive Product Shell
on a local workstation. The shell is a synthetic demonstration only. It is
disconnected from any Collector, memory service, vector store, model runtime, or
organizational information. It performs no organizational action and accepts no
real information.

The preview:

- has no authentication or TLS;
- is unsuitable for network exposure;
- accepts no real information;
- provides no availability or recovery commitment;
- is not a deployment; and
- is not Operational.

Repository maturity for this component is **Implemented**, not Operational.
The exact independently reviewed implementation is canonical on `main`. This
guide describes local inspection, not a production runbook.

## Prerequisites

- A local clone of this repository on a trusted workstation.
- Python 3.12 or newer.
- No network access is required, expected, or used.

The shell imports only the Python standard library and its own package modules.
No package manager, virtual environment, dependency synchronization, lock,
service, or credential is required.

## Start command

From the repository root, start the reviewed application on an explicit local
port in the range 1024-65535:

```text
python -B -m apps.jebediah_executive --port 8765
```

The process binds only to the loopback address `127.0.0.1`. There is no host,
environment, data-source, file, service, or credential option. The `--port`
argument is the only application option. Python's `-B` option disables bytecode
cache writes. The command does not invoke a package manager, discover or
synchronize the repository project environment, or fetch dependencies.

On startup the process reports its loopback location and a synthetic-only
boundary. If the chosen port is outside the allowed range, startup fails before
any bind. If the port is already in use, startup fails visibly and the process
exits with a non-zero status.

## Open the preview

Open the loopback URL in a local browser:

```text
http://127.0.0.1:8765/
```

Only requests to `127.0.0.1:8765` and allowlisted paths are served. The `Host`
and `Origin` headers do not affect any response, link, header, route, or log.

## Approved demonstration routes

The shell serves a fixed set of routes. There are no trailing-slash aliases and
every query string is rejected.

- `/` - executive overview
- `/attention` - what needs attention
- `/knowledge` - what is known
- `/next` - what happens next
- `/workspace` - working set and lifecycle states
- `/ask` - preset Ask index
- `/ask/grounded-priorities`
- `/ask/insufficient-program-outcomes`
- `/ask/failed-source-review`
- `/board` - print-friendly board view
- `/states` - state gallery
- `/states/{ready|loading|empty|partial|stale|insufficient-evidence|held|failed|unauthorized|unavailable|disconnected}`
- `/static/styles.css` - the single local stylesheet

Only `GET` and `HEAD` are supported. Any other method returns `405` with an
`Allow: GET, HEAD` header and the request body is never read.

## Deterministic smoke check

Run this bounded local smoke check after starting the process. It uses a clean
local process and no external system.

1. Confirm the process reports only a loopback location and a synthetic
   boundary.
2. Open `http://127.0.0.1:8765/` and complete all six executive workflows:
   overview, attention, knowledge, next, workspace, and Ask.
3. Check the 320- and 1280-CSS-pixel layouts, 200 percent zoom, keyboard-only
   navigation, visible focus, reduced motion, and the board print preview.
4. Confirm every page shows the synthetic-demonstration badge, the disconnected
   and no-action boundary, the fixed synthetic clock, the scenario label, and
   the coverage and limitations.
5. Inspect browser network activity and confirm every request targets
   `127.0.0.1:8765` and only allowlisted paths, with no external request.
6. Request one unknown route, for example `http://127.0.0.1:8765/unknown`, and
   confirm a safe `404` with no reflected path.
7. Request one route with a query string, for example
   `http://127.0.0.1:8765/attention?x=1`, and confirm a visible `400`
   invalid-request page.
8. Confirm no file, cookie, storage record, cache commitment, or external
   request was created.

Screenshots, if captured, contain only the fabricated scenario and remain
review evidence rather than product validation.

## Clean shutdown

Stop the process from the terminal that started it with `Ctrl+C`. The process
shuts down cleanly and exits with a zero status. No state, file, cookie, cache,
or record persists after shutdown.

## Troubleshooting

The following guidance intentionally avoids any private topology, address,
credential, or organizational detail.

- **Startup fails immediately with a port message.** The port is outside the
  allowed 1024-65535 range. Choose a port within the range.
- **Startup fails with an address-in-use message and a non-zero exit.** Another
  local process holds the chosen port. Choose a different local port.
- **The browser shows a `400` page.** A query string was sent. Request the
  route without any query string.
- **The browser shows a `404` page.** The path is not on the allowlist, or it
  contained traversal, encoded traversal, backslashes, duplicate separators, or
  a null byte. Use an approved route exactly as listed.
- **The browser shows a `405` page.** A method other than `GET` or `HEAD` was
  used. Use `GET`.
- **The stylesheet does not load.** Confirm the process is running and request
  `/static/styles.css` directly. The page remains readable without styling.

If a problem is not resolved by the steps above, stop the process and review the
[Phase 3A Validation Requirements](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_VALIDATION_REQUIREMENTS.md).

## Stop conditions

Stop the preview and escalate through the governing protocol before continuing
if any of the following occur:

- the preview appears to reach or claim any external, current, or organizational
  system;
- any real organizational name, person, address, credential, or topology
  appears;
- any page claims live, current, verified, complete, production, operational, or
  organization-specific data;
- any page claims that Jebediah decided, approved, commanded, executed, sent,
  submitted, changed, or completed an organizational action;
- any request creates a file, cookie, storage record, or external request; or
- any control that accepts input, uploads, or triggers an action appears.

These stop conditions align with the
[Phase 3A Threat Model](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_THREAT_MODEL.md) and
the [Phase 3A Product Shell Plan](ORGANIZATIONAL_INTELLIGENCE_PHASE_3A_PRODUCT_SHELL_PLAN.md).
