# Phase 3B Dependency Assessment

**Status:** Accepted architecture dependency selection; no dependency
installation, lock change, implementation, deployment, or runtime use is
authorized

**Reconciliation:** This assessment remains a future milestone constraint under
[CA-2026-08-06-P3B-RECONCILIATION](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md).
Repository dependencies introduced by pull request #60 are not retroactively
approved by this document.

## Purpose

Select the smallest dependency set that can provide authenticated durable
custody, strict native PDF inspection, offline malware scanning, and bounded
local OCR without cloud processing.

## Selected boundary

| Capability | Selection | Boundary |
| --- | --- | --- |
| Host encryption, signatures, KDF, AEAD, HKDF | `cryptography` 50.x | Python host dependency, exactly locked by `uv.lock` |
| Durable metadata | Python `sqlite3` / SQLite | Standard library; runtime SQLite version recorded |
| Container execution | Rootless Podman 6.x on Linux cgroups v2 | Operator and CI prerequisite, not imported by application code |
| PDF structural validation | qpdf 12.x | Native worker image only; recovery disabled |
| PDF native extraction | `pypdf` 6.x | Native worker image only; strict and resource-bounded |
| Malware scanning | ClamAV 1.5.x | Separate scanner image; offline signature bundle |
| PDF rasterization for OCR | Poppler `pdftoppm` 25.x | OCR worker image only |
| OCR | Tesseract 5.x plus pinned English language data | OCR worker image only |

Exact patch versions, distributions, image digests, hashes, and transitive
artifacts are selected and locked during implementation. Architecture adopts
compatible release lines, not whatever is newest at runtime.

## Verified upstream facts

As checked from official package/release metadata on 2026-08-05:

- `cryptography` publishes Python 3.12-compatible releases under
  Apache-2.0/BSD-3-Clause terms and provides Ed25519, Argon2id, AES-GCM, and HKDF.
- `pypdf` publishes Python 3.12-compatible BSD-3-Clause releases and documents
  that page content streams can require extreme memory, which is why worker and
  stream limits are mandatory.
- qpdf provides PDF structural checking and a recovery-suppression mode suitable
  for rejecting rather than repairing malformed inputs.
- ClamAV publishes GPL-2.0 scanner releases and supports offline scanning with a
  separately managed signature database.
- Tesseract is Apache-2.0 and performs local OCR; Poppler provides local PDF page
  rendering.
- Podman supports rootless containers, no-network execution, read-only
  filesystems, capability dropping, no-new-privileges, seccomp, tmpfs, and
  cgroup resource controls when the host delegates controllers correctly.

Release metadata is reverified immediately before implementation locking.
Documentation does not claim that a release line is vulnerability-free.

## Why these dependencies

### `cryptography`

The standard library does not provide the required AEAD, Argon2id, Ed25519, or
safe key-wrapping primitives. One maintained dependency is safer than custom
cryptography. Host code uses high-level recipes and narrowly reviewed
primitives; it does not implement cryptographic algorithms.

### qpdf plus `pypdf`

qpdf provides a mature native structural checker with repair suppression.
`pypdf` provides page-oriented native text extraction and location callbacks.
Using both increases supply-chain surface but keeps structural acceptance
separate from extraction and allows each result to be recorded. Both execute
inside the same tightly bounded native PDF worker and are subject to the same
SCA, image, and CVE gates.

### ClamAV

A file parser is not a malware scanner. ClamAV provides an independently
versioned scanner decision. A clean result is only evidence. Scanner
unavailability or stale signatures fails evaluation.

### Poppler plus Tesseract

OCR requires rasterization and an OCR engine. These tools remain in a separate
worker invoked only after native extraction is insufficient. This avoids adding
OCR libraries to the host process or sending document bytes to a cloud service.

### Podman

Plain subprocess limits do not provide sufficient filesystem, network,
capability, namespace, or cgroup isolation. Rootless Podman is selected for the
local Linux/Podman-machine boundary. It is not a production deployment
selection.

## Rejected alternatives

- **Standard library only:** cannot provide required cryptography or parse PDF.
- **pikepdf in addition to qpdf:** duplicates the qpdf binding without a required
  host API for this slice.
- **PyMuPDF:** combines extraction and rendering conveniently but introduces a
  licensing and single-parser concentration decision unnecessary for the first
  slice.
- **OCRmyPDF:** useful for searchable-PDF production but adds orchestration and
  output behavior not needed when Phase 3B persists bounded evidence units.
- **Cloud OCR or malware API:** violates local-only and data-minimization
  boundaries.
- **Docker daemon:** a privileged long-lived daemon is unnecessary when rootless
  Podman satisfies the local worker contract.
- **Native parser subprocess without OCI isolation:** insufficient for untrusted
  real documents.
- **DOCX libraries:** DOCX is deliberately deferred, so `python-docx`, `lxml`,
  `defusedxml`, `oletools`, and `msoffcrypto` are not introduced.
- **A browser framework or JavaScript package chain:** server-rendered multipart
  forms and progressive HTML are sufficient.

## Supply-chain requirements

Implementation must:

- lock exact Python distributions and hashes in `uv.lock`;
- pin OCI base images and worker images by immutable digest;
- record qpdf, ClamAV, Poppler, Tesseract, language-data, and scanner-signature
  identities;
- generate and retain an SBOM for each worker image;
- verify package/image signatures where upstream supports them;
- document every applicable license and redistribution obligation;
- scan host dependencies and images for known vulnerabilities;
- block Critical or exploitable High findings unless a reviewed exception names
  exposure and compensating controls;
- build without copying repository secrets or runtime data into images;
- run workers with no network even when images contain networking libraries; and
- prove removal of any unused package.

## Update ownership

The Maintainer owns dependency selection, lock updates, image rebuilds, license
review, scanner-signature policy, and vulnerability response. An implementation
update changing a major release line, parser, scanner, renderer, OCR engine,
container runtime, cryptographic primitive, or license returns to architecture
review.

## Rollback

Rollback restores the prior reviewed `uv.lock` and immutable worker image
digests, then reruns all cryptographic compatibility, persisted-object,
container, parser, OCR, and browser tests. A version that cannot read existing
encrypted objects or schema state cannot be rolled back without reviewed
migration or complete authorized reset.
