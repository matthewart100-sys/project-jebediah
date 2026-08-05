# Organizational Intelligence Phase 3A Threat Model

**Status:** Proposed

**Scope:** Executive Product Shell synthetic local preview only

**Date:** 2026-08-05

**Security owner:** Maintainer accountable for the repository candidate

## Purpose

This threat model defines the assets, actors, boundaries, abuse cases, controls,
tests, residual risks, and stop conditions for the Phase 3A Executive Product
Shell. It does not authorize live information, network deployment, or production
security claims.

## Protected assets

- Accuracy of evidence, uncertainty, freshness, limitation, and authority labels
- Separation between synthetic fixtures and real organizational information
- Human understanding and final decision authority
- Repository source, tests, and reviewed fixture provenance
- Local workstation resources used by the preview
- Absence of secrets, private locators, personal data, and operational topology

## Actors

| Actor | Authority |
| --- | --- |
| Local demonstration operator | Start and stop the preview; select compiled synthetic views, states, and preset responses |
| Nonprofit executive demonstration user | Navigate and inspect synthetic views; no system or organizational authority granted |
| Executive Product Shell | Present immutable synthetic briefing data; no source, approval, or action authority |
| Repository reviewer | Review public source and synthetic evidence |
| Untrusted local requester | May attempt malformed routes or identifiers; receives no privileged behavior |
| External service or model | Not present and not authorized |

## Trust boundaries

1. Command line to preview startup configuration
2. Local HTTP request to WSGI application
3. Allowlisted route, state, and preset-response selection
4. Immutable synthetic provider to view-model validation
5. View model to HTML renderer
6. Reviewed local stylesheet to browser
7. Human interpretation of evidence and authority labels

No authorized boundary reaches a file upload, source document, database,
network service, model, vector store, workflow, or external action.

## Threat and control matrix

| Threat | Prevention | Safe failure | Required evidence | Residual risk |
| --- | --- | --- | --- | --- |
| Real organizational information enters the demo | No file input, text area, free-form prompt, POST route, clipboard import, environment content, or live adapter | Unknown request identifiers are rejected without echo | Route, HTML, package, and forbidden-capability tests | A person could modify source locally; that modified tree is outside reviewed evidence |
| Synthetic content is mistaken for live intelligence | Persistent synthetic banner, scenario identity, fabricated source labels, fixed synthetic clock, explicit limitations | Every page retains synthetic and disconnected labels | Renderer and browser journey tests | A screenshot can be removed from context; committed copy and product language reduce but cannot eliminate misuse |
| Evidence or uncertainty labels are omitted | Frozen model validation requires every material field and section contract | Invalid briefing cannot render ready | Model, fixture, and mutation-negative tests | Human readers may still misunderstand qualitative uncertainty |
| Action candidate is mistaken for authorization | Required kind, authority requirement, owner, permitted navigation, and no mutation routes | Missing authority metadata rejects the item | Model and route tests | The interface cannot control decisions made outside it |
| HTML or template injection | Escape every dynamic value; no raw HTML field; no client script | Invalid values render as text or fail model validation | Adversarial rendering tests | Browser implementation defects remain possible |
| Path traversal or arbitrary resource access | Fixed route table and one fixed package resource; no request-derived path | Unknown route returns sanitized 404 | Route and package-boundary tests | None within reviewed code path |
| Query or header injection | Reject every query string; never reflect unknown values; fixed headers; replace raw server access logs with normalized route logging | Reject requests with any query or ambiguous path selector | Request, header, and captured-log tests | Malformed requests remain possible from local processes but yield no content or raw request log |
| Host-header or origin confusion | Never use request host or origin in content, links, redirects, headers, or logs; render relative local links; set no CORS permission | Host value is ignored and no absolute URL is generated | Host-header variation and rendered-output tests | Browser extensions and manually modified local code remain outside reviewed behavior |
| Network exposure without authentication | Literal `127.0.0.1` binding with no host option; documentation forbids proxies and exposure | Startup refuses non-loopback configuration | Entry-point tests and operator guide | Other local users or processes may reach loopback; real information remains prohibited |
| Clickjacking or external embedding | CSP `frame-ancestors 'none'` and no external assets | Browser refuses framing under compliant implementation | Header tests | Old or non-compliant browsers are not an approved target |
| External content or asset fetch | CSP `default-src 'none'`; local CSS only; no URLs in source references | Missing asset leaves content readable | Static scan and browser network inspection | Browser extensions are outside component control |
| Stale, partial, empty, held, failed, or disconnected state appears ready | One explicit top-level state and required section impact; state-specific rendering | Contract conflict fails closed | State matrix and renderer tests | Synthetic scenarios do not prove live dependency behavior |
| Numeric score implies truth | No numeric confidence field; qualitative enum only | Unknown state rejected | Model and rendered-text scans | CSS prominence can still influence perception; usability review checks hierarchy |
| Missing evidence is fabricated for visual completeness | Fixture builders require explicit missing and limitation values; no default claim generator | Insufficient-evidence view | Fixture and negative model tests | Demonstration fixtures are curated and cannot prove future data quality |
| Resource exhaustion through routes | GET/HEAD only; bounded path/query length; fixed fixtures; no body reads; no recursion or external calls | Return 400/414 or close request | Boundary tests with oversized paths and repeated parameters | Standard-library server is single-process and not a production denial-of-service control |
| Sensitive values enter logs | Custom request handler records only method, normalized allowlisted route identity or `unrecognized`, and status; errors are sanitized | Generic error code and safe message | Captured-log tests with hostile paths, queries, headers, and control characters plus sensitive-value scan | Python or host-level diagnostics outside the app require normal workstation controls |
| Cache exposes a prior view | `Cache-Control: no-store`; no cookies, local storage, service worker, or application cache | Browser refetches compiled fixture | Header and source scans | Browser history may retain route names, which contain no organizational content |
| Dependency or build supply-chain compromise | No new runtime, frontend, font, icon, test, or build dependency | Implementation stops if a dependency becomes necessary | Lock and manifest checks | Existing Python interpreter and repository toolchain remain trusted dependencies |
| Model or retrieval output is treated as evidence | No model, prompt, retrieval, embedding, Qdrant, Ollama, or memory import | Preset synthetic response only | Package and prohibited-import tests | Demonstration wording must remain clearly synthetic |
| Local preview is called deployed or operational | Component maturity remains Implemented at most; preview guide names limitations | Documentation gate blocks deployment claim | Canonical consistency review | A user may expose it manually; that action is unauthorized and unsupported |

## Security headers

Every HTML response must include:

```text
Content-Security-Policy: default-src 'none'; style-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
Cache-Control: no-store
```

The stylesheet response uses `nosniff` and `no-store`. No response sets a cookie
or cross-origin permission.

## Privacy and information boundary

All committed fixtures are authored synthetic data with obvious labels and no
real person, address, account, document, organization, or external locator.
Fixture review includes a sensitive-value and private-detail scan.

The Ask surface provides preset synthetic questions only. The workspace provides
compiled status metadata only. The application has no feature capable of
opening, copying, moving, hashing, parsing, inspecting, uploading, storing,
embedding, indexing, summarizing, or retrieving a real document.

## Security validation

Implementation review must reproduce:

- escaping tests using markup, template, command, URL, and control-character
  payloads;
- route traversal, duplicate-selector, unknown-selector, oversized-path, and
  unsupported-method tests;
- safe header and no-cookie assertions;
- forbidden import, network, subprocess, filesystem-source, persistence,
  upload, parser, model, and service scans;
- captured logging checks;
- dependency and lock no-change verification;
- browser network inspection confirming only loopback HTML and CSS requests; and
- repository sensitive-value and private-detail scans.

## Residual risk

- Loopback is not an authentication boundary against another local process.
- The standard-library WSGI server is not hardened or supported for production.
- Repository-owned accessibility and security checks do not replace later
  independent production testing.
- A synthetic demonstration cannot validate live classification, access,
  retention, source integrity, or operational recovery.

These risks are acceptable only because Phase 3A contains no real information,
has no network deployment, and grants no organizational or action authority.

## Stop conditions

Stop and request revised architecture if implementation requires:

- real or user-provided organizational content;
- a file, upload, parser, OCR, scanner, model, retrieval, database, or external
  service;
- a non-loopback bind or proxy;
- authentication, credentials, secrets, analytics, exports, or persistence;
- a new dependency or build chain;
- mutable decisions, approvals, actions, or organizational records;
- a weaker CSP, unescaped HTML path, or request-derived filesystem access; or
- a security claim beyond the tested synthetic local-preview boundary.

## Review and maintenance

Work Mode reviews this threat model with the complete exact-head architecture
package. Any live adapter, identity boundary, deployment topology, generated
assistance, saved state, export, or action capability requires a new threat
review.
