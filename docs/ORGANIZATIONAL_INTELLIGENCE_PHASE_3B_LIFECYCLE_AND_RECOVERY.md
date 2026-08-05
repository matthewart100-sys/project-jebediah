# Phase 3B Lifecycle and Recovery Specification

**Status:** Proposed; no implementation, live information, or deployment
authorized

## Purpose

This specification makes Phase 3B custody, cryptography, retention, deletion,
legal hold, reconciliation, backup, restore, and key rotation deterministic.

## Runtime boundary

All state lives in one operator-selected runtime directory outside Git. The
directory contains:

- `metadata.sqlite3`, WAL, and shared-memory files;
- encrypted object files under opaque identities;
- one wrapped stable content master-key file;
- versioned non-secret configuration;
- an integrity-protected trust registry containing public keys only; and
- operator-created encrypted backup sets.

OS permissions restrict the directory to the runtime account. Full-volume
encryption is required for later real use because SQLite reveals timing, counts,
state, and policy metadata even though content and private locators are excluded.

## Object format and encryption

Each object uses:

- a versioned header;
- object kind and opaque object identity as authenticated associated data;
- random 256-bit DEK;
- random nonce prefix plus monotonic chunk counter;
- AES-256-GCM encrypted chunks;
- wrapped DEK under the stable content master key; and
- a final authenticated length and SHA-256 identity record.

The self-describing header stores KDF-independent wrapped-DEK material so an
object made durable before its SQLite transaction can be reconciled.

The stable content master key is generated from a cryptographically secure
random source. An operator passphrase derives a KEK using Argon2id with a random
salt and versioned parameters. The KEK wraps only the master key. Passphrase
rotation authenticates and rewraps the same master key; it does not rotate DEKs,
rewrite objects, or invalidate audit evidence.

HKDF derives a separate audit HMAC key from the stable master key. Key context
labels are versioned and disjoint. The audit HMAC protects integrity against
accidental corruption or an offline actor without the unlocked master key. It
does not prove non-repudiation against the authorized operator.

Plaintext passphrases, KEKs, master keys, DEKs, and decrypted source or output
bytes are never logged, persisted in SQLite, included in backups, passed to
workers as files, or committed.

## Transaction ordering

Creation uses:

1. validate authority and reserve the single-use receipt;
2. stream browser bytes directly into a same-filesystem encrypted temporary
   object while computing SHA-256 and enforcing the upload limit;
3. flush and `fsync` the object;
4. atomically replace it into its opaque final path;
5. `fsync` the object directory;
6. commit the SQLite receipt, object, content identity, and transition records;
7. append the event-chain record; and
8. return a safe receipt to the browser.

If steps 2-5 fail, temporary ciphertext is removed and the attempt records a
safe failure. A crash after step 5 but before step 6 leaves a decryptable orphan
that startup reconciliation identifies by its authenticated object header.

Deletion commits a tombstone and ineligibility state before destroying the
wrapped DEK and ciphertext. A failed physical delete remains a visible
`cleanup_failed` obligation and is retried; user-visible completion is not
reported until verification succeeds.

## Reconciliation

Startup reconciliation runs before accepting a mutation:

- committed row plus valid object: retain;
- committed row plus missing object: hold the subject and record integrity
  failure;
- committed row plus invalid object/tag/digest: hold and record integrity
  failure;
- valid orphan object plus reserved attempt: complete or delete according to the
  recorded transaction boundary;
- valid orphan without a reserved attempt: cryptographically delete and record a
  safe orphan tombstone;
- expired object without hold: run cleanup;
- tombstoned object still present: retry physical deletion;
- deleted object referenced by a restored backup: keep deleted and reapply the
  tombstone; and
- unverifiable state: stop mutations and require operator recovery.

Reconciliation never guesses admission, review, source authority, or consumer
eligibility.

## Retention profiles

Only `phase3b-board-roster-pilot-v1` is supported:

- incomplete receipt without quarantine: immediate cleanup;
- rejected or evaluation-failed content: seven days;
- held, accepted, processing, processing-failed, ready, and review artifacts:
  thirty days from receipt;
- safe audit records and tombstones: 365 days; and
- encrypted backups: thirty days.

The deadline is fixed when the receipt is accepted and cannot be extended by
retry, review, backup, restore, or duplicate upload. A new source version is a
new submission with its own authorization and deadline.

## Reset and deletion

Supported scopes are one submission, one source-record lineage, and the entire
local Phase 3B domain. All scopes require explicit operator confirmation and
produce before/after evidence.

Reset:

- blocks new transformation and review;
- marks current and future consumer eligibility false;
- tombstones source and derived objects;
- destroys applicable wrapped DEKs;
- deletes ciphertext and temporary material;
- invalidates active sessions and receipt reservations for the scope;
- records unresolved backups until their expiry or verified purge;
- retains only safe audit/tombstone evidence; and
- never reactivates a superseded version.

An active legal hold returns a visible blocked result and changes nothing.

## Legal hold

A legal-hold declaration or lift is a signed JSON record with:

- unique record identity;
- exact subject scope;
- authority role and signer key identity;
- reason code without sensitive narrative;
- effective time;
- optional expiry;
- retention policy identity; and
- signature.

Trusted hold/lift keys are separate roles in the public-key trust registry.
The operator may submit a signed record but cannot create the authority.
Expired holds are not silently lifted; expiry creates a pending lift check unless
the signed declaration expressly authorizes automatic expiry.

## Backups

Backup is an interactive local command. It:

1. blocks mutations;
2. performs a SQLite online backup/snapshot;
3. copies encrypted objects and wrapped master-key material;
4. includes configuration, trust-registry identity, and tombstones;
5. creates a canonical manifest with lengths and SHA-256 identities;
6. authenticates the manifest with the audit HMAC key;
7. verifies the copy; and
8. resumes mutations.

The passphrase is never in the backup. Backup media is access-controlled,
volume-encrypted, outside Git, and owned by the authorized operator. The backup
deadline is recorded and cleanup is verified.

## Restore and recovery

Restore is interactive and uses an empty staging directory:

1. verify manifest identity and HMAC;
2. verify the SQLite snapshot and schema version;
3. unlock the stable master key;
4. authenticate every encrypted object without exposing content to logs;
5. verify audit-chain epochs and tombstones;
6. reconcile references and retention deadlines;
7. reapply deletions and expiry;
8. run a read-only synthetic smoke check;
9. atomically activate staging; and
10. retain the prior directory only under its existing retention policy.

Lost passphrase plus unavailable recovery material makes content unrecoverable.
That is a fail-closed security outcome but an operational data-loss event. The
later real-source decision must name passphrase custody and recovery ownership.

## Rotation

Passphrase rotation requires the old and new passphrases, records a key-wrapper
epoch, rewraps the stable master key, verifies decryption, and atomically replaces
the wrapper. Historical object and audit keys remain stable.

Trust-key rotation adds a new signed registry version, preserves old public keys
for historical verification, records revocation effective times, and denies
new receipts from revoked keys. It does not invalidate correctly signed
historical evidence created before revocation unless the authority decision says
otherwise.

## Operations and incidents

The operator stops intake immediately on:

- key, trust-registry, audit-chain, object-integrity, or reconciliation failure;
- unexpected external network access;
- worker isolation or cgroup-control failure;
- private content in logs or metadata;
- malware/active-content policy bypass;
- incomplete deletion reported as success; or
- evidence that the selected file is outside the authorized classification.

The repository records only a sanitized conclusion. Sensitive incident evidence
uses the private security channel defined by `SECURITY.md`.

## Validation

Required validation includes interrupted writes at every transaction boundary,
wrong key and passphrase, nonce uniqueness, corrupt tags and headers, replay,
rotation, orphan handling, missing objects, expired retention, held deletion,
failed deletion, tombstone restore, complete reset, backup verification, restore
staging, and proof that no plaintext content appears on disk or in logs.
