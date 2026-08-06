# Phase 3B Lifecycle and Recovery Specification

**Status:** Accepted architecture specification; no implementation, custody,
live information, backup, restore, deployment, or runtime mutation authorized

**Reconciliation:** These lifecycle and recovery requirements remain binding
future constraints under
[CA-2026-08-06-P3B-RECONCILIATION](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md).
Pull request #60 does not establish conformance or operational readiness.

## Purpose

This specification makes Phase 3B custody, cryptography, retention, deletion,
legal hold, reconciliation, backup, restore, and key rotation deterministic.

## Runtime boundary

All content-bearing runtime state lives in one operator-selected runtime
directory outside Git. The directory contains:

- `metadata.sqlite3`, WAL, and shared-memory files;
- encrypted object files under opaque identities;
- one wrapped stable content master-key file;
- versioned non-secret configuration;
- an integrity-protected trust registry containing public keys only; and
- the local projection of backup and deletion state.

Encrypted backup sets live on separately selected local media. A content-free,
append-only recovery-authority ledger lives at a third independently controlled
local path outside both the runtime directory and every backup set. It contains
monotonic generations, opaque backup identities and inventory digests, manifest
digests, backup reservation/completion/abort records, deletion intents, backup
revocations, purge results, and deletion completions. Each checkpoint is signed
by a trusted Ed25519 recovery-authority key whose private key is absent from the
runtime and backups. Only the public verification key is in the trust registry.

The recovery authority also retains the latest generation and ledger-head hash
in independent non-rollback custody, not in the ledger, runtime, or backups.
For restore, the runtime creates a random challenge. The authority returns a
short-lived signed attestation containing that challenge, environment identity,
latest generation, ledger-head hash, issue time, and expiry. A valid older
ledger prefix cannot satisfy an attestation for the authority's current head.

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
6. in one SQLite transaction, insert the receipt, object, content identity,
   transition, and authenticated event-chain records, then commit; and
7. return a safe receipt to the browser.

If steps 2-5 fail, temporary ciphertext is removed and the attempt records a
safe failure. A crash after step 5 but before step 6 leaves a decryptable orphan
that startup reconciliation identifies by its authenticated object header. A
crash during step 6 rolls back the entire SQLite transaction, so no state
mutation can commit without its audit event. Review, hold, reset, deletion,
rotation, backup, restore, and reconciliation mutations use the same atomic
state-plus-event rule.

Deletion commits a tombstone and ineligibility state before destroying the
wrapped DEK and ciphertext. A failed physical delete remains a visible
`cleanup_failed` obligation and is retried; user-visible completion is not
reported until verification succeeds.

## Reconciliation

Startup reconciliation first creates a random challenge and verifies a
short-lived recovery-authority attestation of the current generation and
ledger-head hash against the external ledger. It then verifies that freshly
attested ledger against the local projection before permitting content access
or accepting a mutation. Missing, expired, replayed, mismatched, or unverifiable
attestation, a rolled-back ledger, or coordinated rollback of the ledger and
local projection fails closed:

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
- state mutation without its required event, or an event without its required
  state mutation: stop mutations and require operator recovery;
- signed deletion intent or backup revocation newer than local state: atomically
  mark the scope ineligible, write local tombstones and audit evidence, deny
  content access, and resume required object and backup purge;
- local deletion state newer than or inconsistent with the signed ledger: stop
  access and mutations pending recovery-authority reconciliation;
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

Every operation that could read, decrypt, display, review, or mutate retained
content checks the deadline and hold state before object access. If the deadline
has passed, the operation denies content access and atomically marks the subject
ineligible and records an audit event regardless of hold state. Without a hold,
the same transaction creates a cleanup obligation and the operation attempts
synchronous cleanup. With a hold, encrypted material and its wrapped DEK remain
preserved, but decryption, display, review, and consumer use stay denied.
Physical cleanup failure remains `cleanup_failed`; expiry never permits
continued display until restart.

Audit events and tombstones are immutable within bounded audit epochs. Epoch
rollover is an explicit local lifecycle operation. Before a closed epoch may be
pruned, every event and tombstone in it must be at least 365 days old and no
applicable hold may remain. Pruning is one transaction that:

1. verifies the complete epoch hash/HMAC chain;
2. writes a subject-free closure anchor into the successor epoch containing the
   prior epoch identity, terminal hash/HMAC, time bounds, event count, policy
   identity, and intended deletion;
3. deletes the whole eligible epoch, never selected rows;
4. records and verifies the pruning result in the successor epoch; and
5. leaves the closure anchor under its own 365-day retention period.

Restore reapplies epoch eligibility and pruning before activation, so an older
backup cannot revive expired audit rows or tombstones. A held epoch remains
intact even when that retains unrelated safe metadata in the same epoch.

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
- identifies every registered backup set whose opaque inventory contains the
  scope and creates a purge obligation for each;
- obtains and durably stores a signed monotonic recovery-ledger checkpoint that
  records the deletion intent and revokes every applicable backup identity
  before destroying online content;
- physically purges and verifies every applicable backup set before reporting
  deletion complete, then obtains and appends the signed monotonic
  `deletion_completed` checkpoint;
- retains only safe audit/tombstone evidence; and
- never reactivates a superseded version.

An unavailable, missing, or unverifiable applicable backup remains a visible
`cleanup_failed` obligation; normal thirty-day expiry is not deletion
completion. An active legal hold returns a visible blocked result and changes
nothing.

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
2. verifies the latest independently retained signed recovery-ledger checkpoint;
3. assigns a unique backup-set identity and opaque inventory, obtains a signed
   next-generation `backup_reserved` checkpoint, durably appends it to the
   recovery ledger, and atomically registers the same pending identity in
   SQLite with its audit event;
4. performs a SQLite online backup/snapshot containing that registration;
5. copies encrypted objects and wrapped master-key material;
6. includes configuration, trust-registry identity, and tombstones;
7. creates a canonical manifest with lengths and SHA-256 identities;
8. authenticates the manifest with the audit HMAC key;
9. verifies the copy, obtains and appends a signed `backup_completed` checkpoint
   containing the manifest digest, and atomically records completion in the live
   runtime; and
10. resumes mutations.

The passphrase is never in the backup. Backup media is access-controlled,
volume-encrypted, outside Git, and owned by the authorized operator. The backup
deadline is recorded and cleanup is verified. Copying a backup outside this
registered inventory is prohibited. Deletion of a scope requires physical purge
and absence verification of every registered backup set containing it; no such
set may remain after deletion is reported complete.

Failure or interruption before a signed `backup_completed` checkpoint leaves a
pending registration. Reconciliation removes partial media, verifies its
absence, obtains and appends a signed next-generation `backup_aborted`
checkpoint, and atomically closes the SQLite registration with an audit event.
If `backup_completed` is already in the authoritative ledger, reconciliation
instead verifies the complete media and manifest and atomically completes the
local registration; it never changes that completed ledger entry to aborted. A
verified aborted registration does not block later deletion. If media state,
ledger continuity, completion, or the signed abort cannot be verified, the
registration remains visible `cleanup_failed` and mutations that depend on it
are denied.

## Restore and recovery

Restore is interactive and uses an empty staging directory:

1. generate a random restore challenge and obtain a short-lived signed
   recovery-authority attestation of the current generation and ledger-head hash
   from the authority's independent non-rollback register;
2. obtain the current recovery-authority ledger from its independently
   controlled path and verify its signatures, monotonic chain, trust role, and
   exact match to the challenge-bound attested head;
3. deny a stale, expired, replayed, missing, rolled-back, malformed, or
   unverifiable ledger or attestation;
4. verify the current ledger history contains a completed entry for the
   candidate backup identity and no later abort or revocation;
5. verify manifest identity and HMAC;
6. verify the SQLite snapshot and schema version;
7. unlock the stable master key;
8. authenticate every encrypted object without exposing content to logs;
9. verify audit-chain epochs and apply all later ledger deletion intents,
   revocations, purge results, and tombstones;
10. reconcile references and retention deadlines;
11. reapply deletions and expiry;
12. run a read-only synthetic smoke check;
13. atomically activate staging; and
14. retain the prior directory only under its existing retention policy.

Restore refuses an unregistered, aborted, revoked, or purge-obligated backup
set. A byte-for-byte pre-deletion copy still carries an identity revoked by the
current independently retained checkpoint and cannot restore. Because deletion
cannot complete until every applicable registered set is verified absent, no
pre-deletion backup remains eligible to restore deleted content. If an
applicable set cannot be located and purged, deletion stays `cleanup_failed` and
no completion claim is permitted.

Lost passphrase plus unavailable recovery material makes content unrecoverable.
That is a fail-closed security outcome but an operational data-loss event. The
later real-source decision must name passphrase custody, recovery ownership,
recovery-authority role and public key, and independent ledger custody. Loss or
unavailability of the current ledger or its authority blocks restore rather than
permitting rollback to backup-local state.

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
