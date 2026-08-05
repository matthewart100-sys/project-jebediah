# Phase 3B Governed Intake Threat Model

**Status:** Proposed; no real-information or deployment authorization

## Assets

- signed source-authorization and legal-hold records;
- source bytes and content identity;
- encrypted quarantine objects;
- extracted native and OCR evidence;
- review decisions and provenance;
- retention, deletion, and tombstone evidence;
- encryption, signing, session, and CSRF key material;
- SQLite state and audit chain;
- worker images, seccomp policy, scanner signatures, and OCR language data;
- backups and recovery state; and
- operator trust in visible state and limitations.

## Trust boundaries

1. Chief Architect and information/legal authority to signed public decision
   records.
2. Browser-selected bytes and receipt to loopback host.
3. Loopback session and forms to the Executive Product Shell.
4. Host orchestration to encrypted object and SQLite custody.
5. Decrypted bounded bytes to scanner worker.
6. Decrypted bounded bytes to native PDF worker.
7. Eligible pages to OCR worker.
8. Untrusted worker JSON back to host.
9. Encrypted runtime state to backup media and restored staging.
10. Phase 3B review output to the absent Phase 3C consumer.

## Threat matrix

| Threat | Primary controls | Failure behavior |
| --- | --- | --- |
| Unauthorized or replayed upload | Ed25519 receipt, trust registry, unique receipt ID, reservation before bytes, expiry, single use | Deny without reading body; safe audit event |
| Server path acquisition or traversal | Browser-pushed bytes only; no server path field; opaque object paths | Reject request/schema |
| Loopback CSRF or DNS rebinding | Random bootstrap token, strict session cookie, CSRF token, literal Host/Origin allowlist, no-referrer | `403`, no mutation |
| Oversized/chunked request exhaustion | 20 MiB streaming cap, timeouts, bounded headers/body, one concurrent upload | Abort, delete temporary ciphertext |
| Malicious or malformed PDF | Offline ClamAV, qpdf no-repair check, active-content traversal, strict extraction, isolated workers | Reject, hold, or evaluation failure |
| PDF JavaScript, launch, XFA, forms, attachment, portfolio, or rich media | Explicit inventory and reject policy; no viewer execution | `rejected` with safe reason |
| External links or references | No worker network, no fetch, URLs excluded from derived output and logs | Warning or reject by policy |
| Parser/container escape | Rootless non-root OCI, no network/mounts/secrets, read-only root, dropped caps, no-new-privileges, seccomp, immutable image | Stop pipeline; incident review |
| Resource bomb | cgroup memory/CPU/PID, wall timeout, tmpfs, page/object/stream/output limits | Fail closed with reached limit |
| OCR prompt/content confusion | OCR is data only, no model/tool path, visible method/quality/limitations | Held until review |
| Worker output injection | Byte cap, strict JSON schema, closed vocabularies, UTF-8 validation, HTML escaping | `processing_failed` |
| Plaintext leakage | streaming encryption/decryption, tmpfs-only worker scratch, no host plaintext file, sanitized logs | Stop and treat as incident |
| Ciphertext tampering | AES-GCM tags, object identity AAD, SHA-256 check, reconciliation | Hold and deny access |
| Weak/lost passphrase | Argon2id, interactive entry, no persistence, named custody/recovery gate | Deny unlock; visible data-loss risk |
| Nonce/key reuse | random DEK, versioned nonce prefix/counter, uniqueness tests | Refuse write |
| Audit manipulation or mutation/event split | atomic SQLite state-plus-event transaction, immutable epochs, hash/HMAC chain, authenticated whole-epoch pruning, external signatures for authority | Roll back together; stop mutations on verification failure |
| Malicious authorized operator | least privilege, external signed authority, safe audit, explicit review; HMAC not claimed as non-repudiation | Residual risk; separate operator/authority roles |
| SQLite/WAL metadata disclosure | no content/private locators, OS ACL, required full-volume encryption for live use | Stop live use if control absent |
| Duplicate confusion | separate submission occurrence, content digest, source identity, explicit supersession | Hold conflict; no automatic current version |
| Approval mistaken for truth | visible authority labels, review vocabulary, no Phase 3C consumer | No downstream eligibility |
| Deletion claimed before completion | tombstone-first, DEK destruction, verified object removal, backup obligations | `cleanup_failed`, visible blocker |
| Legal hold bypass | separately signed hold/lift authority, deletion guard, append-only evidence | Deny deletion; hold never restores expired consumption |
| Deleted data restored | registered backup identities and opaque inventories, mandatory verified purge before deletion completion, tombstones in backup/restore | Keep deletion `cleanup_failed` while any applicable set remains; deny unregistered or purge-obligated restore |
| Expired content remains visible in a long-running process | deadline check before every decrypt/display/review/mutation; ineligibility regardless of hold; synchronous cleanup only when not held | Deny content before access; retain encrypted held material without consumption |
| Backup theft/corruption | encrypted objects, no passphrase, HMAC manifest, access-controlled volume | Reject restore |
| Supply-chain compromise | exact locks/digests, SBOM, SCA, signatures, minimal images, offline runtime | Block build/use |
| Scanner false negative | scanner is evidence only; structural and policy checks remain independent | No safety claim |
| Stale scanner signatures | max-age policy and recorded identity | `evaluation_failed` |
| Synthetic/live fixture confusion | separate generated trust roots, conspicuous fixture labels, environment guard | Deny cross-environment load |
| External network use | `--network none`, browser request audit, CI network-isolation assertion | Stop and block acceptance |
| Phase 3C authority creep | no registry/model/Qdrant imports, no output transport, package tests | Test/implementation failure |

## Privacy controls

- The upload route streams bytes without logging multipart names or payloads.
- The server ignores the client filename except for a bounded, non-persisted
  display value during the active response.
- SQLite and logs use opaque IDs and safe reason codes only.
- Extracted evidence is encrypted and rendered only after authenticated review
  access.
- HTML escapes content and applies restrictive CSP, frame, MIME, referrer, and
  cache headers.
- Browser storage, analytics, telemetry, export, clipboard automation, and
  external resources are absent.
- The real-source gate forbids PHI, clinical, credential, banking, and unrelated
  sensitive information.

## Residual risks

- A fully compromised local OS account can read plaintext while the store is
  unlocked and can forge HMAC-protected audit events. External authority
  signatures limit but do not eliminate this risk.
- PDF engines, ClamAV, Poppler, Tesseract, Podman, the kernel, and cryptographic
  libraries may contain unknown vulnerabilities.
- Malware scanning cannot prove safety.
- Native extraction and OCR may omit, reorder, or misrecognize content.
- The first slice has one operator and no independent approval witness.
- Passphrase loss may make encrypted evidence unrecoverable.
- Local backups extend physical erasure up to thirty days, although tombstones
  remove online eligibility immediately.
- Board names and roles remain personal information.
- Loopback reduces exposure but is not a production authentication or deployment
  boundary.

These risks are accepted only for a separately authorized, local, one-document
pilot after implementation review. They do not authorize production or general
organizational ingestion.

## Security validation

Required adversarial cases include receipt forgery/replay/revocation, CSRF,
Host/Origin manipulation, oversized and interrupted multipart streams, EICAR,
encrypted/malformed/active PDFs, object bombs, parser timeout/OOM/PID pressure,
worker output injection, network attempts, plaintext-disk scans, corrupt
ciphertext/audit/backup, wrong keys, held deletion, tombstone restore, and
package import attempts into registry, memory, model, Qdrant, or network clients.

## Review triggers

Fresh architecture and security review is required for:

- another information domain, organization, operator, or classification;
- DOCX or another format;
- higher limits or broader active-content acceptance;
- another parser, scanner, OCR engine, cryptographic primitive, key service, or
  container runtime;
- networked, remote, multi-user, unattended, or deployed operation;
- an API, export, downstream consumer, model, retrieval, or action path;
- changing retention, deletion, backup, hold, or audit semantics; or
- evidence that the residual risks cannot be bounded locally.
