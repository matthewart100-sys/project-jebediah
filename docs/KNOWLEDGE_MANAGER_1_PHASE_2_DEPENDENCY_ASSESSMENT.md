# Knowledge Manager 1.0 Phase 2 Dependency Assessment

**Status:** Proposed

**Date:** 2026-08-05

**Applies to:** The bounded synthetic implementation candidate in the
[Phase 2 Synthetic Implementation Activation](KNOWLEDGE_MANAGER_1_PHASE_2_SYNTHETIC_IMPLEMENTATION_ACTIVATION.md)

## Decision

The candidate adds **no dependency** and changes no dependency manifest or lock
file.

The authorized implementation uses only the Python standard library at runtime
and the repository's existing pytest dependency for tests. Detector, scanner,
parser, sandbox, external binary, persistence, service, and network technologies
remain unselected and unauthorized.

This is a deliberate security and reproducibility boundary, not a claim that the
standard library can safely parse or isolate untrusted production documents.

## Required capabilities

| Capability | Dependency | Purpose | Versioning | License | Maintenance status | Windows and Linux | Deterministic installation | Requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Immutable records, enums, ABCs, typing, time, byte hashing, and process-local maps | Python standard library | Implement the exact contracts, SHA-256 synthetic integrity, and in-memory adapters | Repository requirement `Python >=3.12`; implementation must remain compatible with the locked development environment | Python Software Foundation License | Part of supported Python versions; repository compilation and full-suite evidence is required | Required on both platforms supported by Python | Selected interpreter plus repository lock and build configuration | Required |
| Deterministic test execution | Existing `pytest>=8.0` development dependency | Execute unit, contract, failure, and package-boundary tests | Existing project constraint and `uv.lock`; no change permitted | MIT | Existing accepted project dependency; current repository suite is passing | Supported in current Windows development and Linux CI-compatible Python environments | Existing `uv.lock`; `uv --system-certs lock --check` must produce no change | Required for tests only |
| Documentation, links, sensitive values, and repository hygiene | Existing `scripts/validate_docs.py` | Validate the documentation-only package and later implementation documentation | Versioned in the repository | Project source under repository terms | Maintained by the repository | Python standard-library behavior on Windows and Linux | Exact reviewed repository script | Required validation |

No package installation is required for this documentation task.

## Standard-library modules allowed

The implementation may use only:

- `abc`
- `collections.abc`
- `dataclasses`
- `datetime`
- `enum`
- `hashlib`
- `re`
- `typing`

Additional standard-library imports require implementation-review justification.
The following remain prohibited even though they are standard library:

- `socket`, `urllib`, `http`, or other network clients;
- `subprocess`, `multiprocessing`, or shell execution;
- filesystem discovery through `glob`, recursive `pathlib` use, or directory
  walking;
- `zipfile`, XML parsers, or other container/parser mechanisms in the authorized
  candidate; and
- serialization that could persist payload bytes or extracted content.

## Deferred technology classes

These are not proposed dependencies and must not be added during the synthetic
candidate:

| Technology class | Potential future purpose | Current decision | Required future review |
| --- | --- | --- | --- |
| PDF parser | Structure validation and bounded extraction | Deferred; no parser implementation | Exact library/version, license, maintenance, CVE history, unsafe-feature surface, deterministic install, Windows/Linux behavior, resource limits, isolation, and rollback |
| DOCX/OOXML parser | Bounded package inspection and extraction | Deferred; no archive or XML implementation | Exact library/version, license, maintenance, decompression/traversal/XML controls, isolation, deterministic install, and rollback |
| MIME or file-signature detector | Format identification | Deferred; interfaces and scripted outcomes only | Signature source, update process, platform consistency, spoofing behavior, license, and failure default |
| Malware scanner | Malicious-content evaluation | Deferred; no live scanning | Product/version, signatures, update authority, offline behavior, false-positive/negative policy, licensing, evidence handling, Windows/Linux support, and unavailable behavior |
| Macro/active-content tooling | Detect unsupported active content | Deferred; inert markers and scripted outcomes only | Exact detection coverage, safe non-execution proof, license, maintenance, parser dependencies, and isolation |
| Process or container sandbox | Isolate a selected parser | Deferred; interface only | OS mechanism, least privilege, filesystem/network/process denial, quotas, termination, cleanup, observability, platform parity, and escape threat review |
| Durable quarantine or evidence store | Production persistence and recovery | Prohibited in this phase | Information owner, component and operational owner, retention, deletion, backup, restore, reconciliation, migration, security, and ADR impact |
| API, queue, service, watcher, or scheduler | Runtime receipt and processing | Prohibited in this phase | Interface ownership, authentication, authorization, rate/capacity policy, operations, deployment, and separate implementation authorization |

No dependency may be selected merely because it is convenient or already
installed locally.

## Security implications

The no-new-dependency decision:

- eliminates new transitive packages and external binaries from this milestone;
- prevents accidental parser or scanner execution;
- keeps tests offline and reproducible;
- avoids cross-platform differences caused by native bindings; and
- keeps removal and rollback limited to repository files.

It does not mitigate vulnerabilities in a future parser or sandbox. The
[Phase 2 Threat Model](KNOWLEDGE_MANAGER_1_PHASE_2_THREAT_MODEL.md) therefore
keeps parser exploitation, archive abuse, active content, and isolation as
unimplemented controls that block real-document work.

## Supply-chain validation

Implementation review must prove:

```text
git diff --exit-code <base>..<head> -- pyproject.toml uv.lock
uv --system-certs lock --check
```

It must also scan imports under `src/collector/document_admission` and fail if a
third-party, network, service, parser, scanner, container, Qdrant, Ollama,
FastAPI, registry, memory, or runtime module appears.

## Removal and rollback ownership

Codex - Implementation Engineer owns removal of the bounded candidate during
implementation. Work Mode validates the exact dependency and import boundary.
The Chief Architect decides any exception. No external package, binary,
signature database, service, or stored state requires cleanup.

## Reconsideration gate

A dependency decision reopens architecture and security review before code when
it would:

- execute against document bytes;
- parse PDF, OOXML, XML, archives, macros, or active content;
- add native code or an external binary;
- create process, container, filesystem, or network isolation;
- add persistence, a service, or runtime composition; or
- change `pyproject.toml` or `uv.lock`.

The revised proposal must record every field required by the activation
directive: purpose, version strategy, license, maintenance, security,
Windows/Linux compatibility, deterministic installation, and whether the
dependency is required or optional.
