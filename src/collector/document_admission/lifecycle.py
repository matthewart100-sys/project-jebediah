"""Milestone 1 lifecycle operations: expiry, deletion, and reconciliation.

Only the capabilities named for the Synthetic Intake and Custody Foundation
are implemented here: retention-deadline expiry with synchronous cleanup,
explicit deletion of one submission's custody objects, and startup
reconciliation. Legal hold, backup/restore, epoch pruning, and passphrase
rotation are later-milestone concerns and are not implemented.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .durable_repository import SqliteDurableRepository
from .failures import ExpiredContent
from .models import CustodyObjectRecord, ReconciliationFinding
from .policies import RetentionPolicy


@dataclass(frozen=True)
class LifecycleCleanupOutcome:
    object_id: str
    deleted: bool
    reason_code: str


def is_expired(
    record: CustodyObjectRecord,
    checked_at: datetime,
) -> bool:
    """Return whether a custody record has passed its retention deadline."""

    if checked_at.tzinfo is None:
        raise ExpiredContent("invalid_naive_checked_at")
    return checked_at >= record.retention_deadline


def deny_if_expired(
    record: CustodyObjectRecord,
    checked_at: datetime,
) -> None:
    """Raise ``ExpiredContent`` if content access is not permitted.

    Every operation that would decrypt, display, review, or otherwise
    consume retained content must call this before object access,
    regardless of legal hold. A legal hold changes only whether the
    ciphertext is destroyed, never whether expired content may be
    consumed.
    """

    if is_expired(record, checked_at):
        raise ExpiredContent("retention_deadline_passed", record.object_id)


def expire_and_cleanup(
    repository: SqliteDurableRepository,
    retention: RetentionPolicy,
    checked_at: datetime,
) -> tuple[LifecycleCleanupOutcome, ...]:
    """Tombstone every active, non-held object past its retention deadline.

    A legal hold preserves encrypted material and its wrapped key but still
    denies further content access; ``deny_if_expired`` enforces the denial
    independently of whether this cleanup step has run.
    """

    outcomes: list[LifecycleCleanupOutcome] = []
    for record in repository.list_active():
        if not is_expired(record, checked_at):
            continue
        if record.legal_hold:
            outcomes.append(
                LifecycleCleanupOutcome(
                    object_id=record.object_id,
                    deleted=False,
                    reason_code="retained_under_legal_hold",
                )
            )
            continue
        repository.tombstone(
            record.object_id,
            "retention_deadline_expired",
            checked_at,
        )
        outcomes.append(
            LifecycleCleanupOutcome(
                object_id=record.object_id,
                deleted=True,
                reason_code="retention_deadline_expired",
            )
        )
    return tuple(outcomes)


def delete_submission(
    repository: SqliteDurableRepository,
    admission_attempt_id: str,
    deleted_at: datetime,
) -> tuple[LifecycleCleanupOutcome, ...]:
    """Reset scope: delete every active object for one submission.

    An active legal hold on any in-scope object blocks the whole submission
    scope without partial effect, matching the Lifecycle and Recovery
    Specification's reset behavior.
    """

    if not admission_attempt_id:
        raise ExpiredContent("invalid_admission_attempt_id")

    in_scope = tuple(
        record
        for record in repository.list_active()
        if record.admission_attempt_id == admission_attempt_id
    )
    if any(record.legal_hold for record in in_scope):
        return tuple(
            LifecycleCleanupOutcome(
                object_id=record.object_id,
                deleted=False,
                reason_code="blocked_by_legal_hold",
            )
            for record in in_scope
        )

    outcomes: list[LifecycleCleanupOutcome] = []
    for record in in_scope:
        repository.tombstone(
            record.object_id,
            "operator_requested_deletion",
            deleted_at,
        )
        outcomes.append(
            LifecycleCleanupOutcome(
                object_id=record.object_id,
                deleted=True,
                reason_code="operator_requested_deletion",
            )
        )
    return tuple(outcomes)


def reconcile_on_startup(
    repository: SqliteDurableRepository,
    checked_at: datetime,
) -> tuple[ReconciliationFinding, ...]:
    """Run local startup reconciliation before permitting further mutation.

    This delegates to the durable repository's local reconciliation, which
    covers the Milestone 1 cases: retained, held-for-integrity-failure, and
    deleted-orphan. External recovery-authority ledger attestation is a
    later-milestone concern and is never consulted here.
    """

    return repository.reconcile(checked_at)
