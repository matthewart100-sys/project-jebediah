from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

from .crypto import (
    EncryptedObject,
    MasterKeyEnvelope,
    audit_hmac_hex,
    create_master_key_envelope,
    decrypt_object,
    encrypted_object_from_json,
    encrypted_object_to_json,
    encrypt_object,
    envelope_from_dict,
    envelope_to_dict,
    hash_content_identity,
    unlock_master_key,
)
from .failures import DocumentAdmissionConflict, DocumentAdmissionNotFound
from .models import (
    ContentIdentity,
    ExtractionQuality,
    Phase3BAuditEntry,
    Phase3BInspectionArtifact,
    Phase3BPageCapture,
    Phase3BRecoveryReport,
    Phase3BReviewAnnotation,
    Phase3BState,
    Phase3BSubmissionDetail,
    Phase3BSubmissionRecord,
    Phase3BWorkspaceSnapshot,
    ReviewDecision,
    SignedSourceAuthorizationReceipt,
)


_STATE_BY_DECISION = {
    ReviewDecision.APPROVE: Phase3BState.REVIEW_APPROVED,
    ReviewDecision.REJECT: Phase3BState.REVIEW_REJECTED,
    ReviewDecision.CORRECT: Phase3BState.REVIEW_CORRECTION_REQUESTED,
    ReviewDecision.SUPERSEDE: Phase3BState.SUPERSEDED,
}


class Phase3BDurableRepository:
    def __init__(self, root_dir: str | Path, passphrase: str) -> None:
        self._root_dir = Path(root_dir)
        self._root_dir.mkdir(parents=True, exist_ok=True)
        self._objects_dir = self._root_dir / "objects"
        self._objects_dir.mkdir(exist_ok=True)
        self._db_path = self._root_dir / "metadata.sqlite3"
        self._master_key_path = self._root_dir / "master-key.json"
        self._master_key = self._load_or_create_master_key(passphrase)
        self._initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _load_or_create_master_key(self, passphrase: str) -> bytes:
        if self._master_key_path.exists():
            envelope = envelope_from_dict(
                json.loads(self._master_key_path.read_text(encoding="utf-8"))
            )
            return unlock_master_key(passphrase, envelope)
        envelope, master_key = create_master_key_envelope(passphrase)
        self._master_key_path.write_text(
            json.dumps(
                envelope_to_dict(envelope),
                sort_keys=True,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
        return master_key

    def _initialize_schema(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS receipts (
                    receipt_id TEXT PRIMARY KEY,
                    signed_payload_json TEXT NOT NULL,
                    reserved_at TEXT NOT NULL,
                    used_at TEXT
                );
                CREATE TABLE IF NOT EXISTS submissions (
                    submission_id TEXT PRIMARY KEY,
                    receipt_id TEXT NOT NULL UNIQUE,
                    state TEXT NOT NULL,
                    content_digest_hex TEXT NOT NULL,
                    byte_count INTEGER NOT NULL,
                    media_type TEXT NOT NULL,
                    duplicate_of TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    deleted_at TEXT,
                    latest_review_decision TEXT
                );
                CREATE TABLE IF NOT EXISTS objects (
                    object_id TEXT PRIMARY KEY,
                    submission_id TEXT NOT NULL UNIQUE,
                    kind TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    digest_hex TEXT NOT NULL,
                    byte_count INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    deleted_at TEXT
                );
                CREATE TABLE IF NOT EXISTS inspection_artifacts (
                    submission_id TEXT PRIMARY KEY,
                    artifact_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS review_annotations (
                    annotation_id TEXT PRIMARY KEY,
                    submission_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    actor_id TEXT NOT NULL,
                    reason_code TEXT NOT NULL,
                    note TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    prior_annotation_id TEXT
                );
                CREATE TABLE IF NOT EXISTS audit_entries (
                    event_id TEXT PRIMARY KEY,
                    submission_id TEXT NOT NULL,
                    event_kind TEXT NOT NULL,
                    prior_state TEXT,
                    next_state TEXT,
                    reason_code TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    audit_mac_hex TEXT NOT NULL
                );
                """
            )

    def admit(
        self,
        signed_receipt: SignedSourceAuthorizationReceipt,
        media_type: str,
        payload: bytes,
        admitted_at: datetime,
    ) -> Phase3BSubmissionRecord:
        receipt = signed_receipt.receipt
        submission_id = f"submission-{receipt.receipt_id}"
        content_identity = hash_content_identity(payload)
        if (
            receipt.expected_sha256 is not None
            and receipt.expected_sha256 != content_identity.digest_hex
        ):
            raise DocumentAdmissionConflict(
                "receipt_digest_mismatch",
                receipt.receipt_id,
            )
        duplicate_of = self._existing_submission_for_digest(
            content_identity.digest_hex
        )
        object_id = f"object-{receipt.receipt_id}"
        encrypted = encrypt_object(
            self._master_key,
            object_id=object_id,
            kind="source_pdf",
            payload=payload,
            created_at=admitted_at,
        )
        object_path = self._objects_dir / f"{object_id}.json"
        object_path.write_text(
            encrypted_object_to_json(encrypted),
            encoding="utf-8",
        )
        expires_at = admitted_at + timedelta(days=30)
        payload_json = json.dumps(
            {
                "receipt": asdict(receipt),
                "signature_b64": signed_receipt.signature_b64,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
        with self._connect() as connection:
            if connection.execute(
                "SELECT 1 FROM receipts WHERE receipt_id = ?",
                (receipt.receipt_id,),
            ).fetchone():
                raise DocumentAdmissionConflict(
                    "receipt_replayed",
                    receipt.receipt_id,
                )
            connection.execute(
                """
                INSERT INTO receipts (receipt_id, signed_payload_json, reserved_at, used_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    receipt.receipt_id,
                    payload_json,
                    admitted_at.isoformat(),
                    admitted_at.isoformat(),
                ),
            )
            connection.execute(
                """
                INSERT INTO submissions (
                    submission_id, receipt_id, state, content_digest_hex, byte_count,
                    media_type, duplicate_of, created_at, expires_at, updated_at,
                    deleted_at, latest_review_decision
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)
                """,
                (
                    submission_id,
                    receipt.receipt_id,
                    Phase3BState.ACCEPTED.value,
                    content_identity.digest_hex,
                    content_identity.byte_count,
                    media_type,
                    duplicate_of,
                    admitted_at.isoformat(),
                    expires_at.isoformat(),
                    admitted_at.isoformat(),
                ),
            )
            connection.execute(
                """
                INSERT INTO objects (
                    object_id, submission_id, kind, file_name, digest_hex,
                    byte_count, created_at, deleted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
                """,
                (
                    object_id,
                    submission_id,
                    "source_pdf",
                    object_path.name,
                    encrypted.payload_digest_hex,
                    encrypted.payload_size,
                    admitted_at.isoformat(),
                ),
            )
            self._append_audit(
                connection,
                Phase3BAuditEntry(
                    event_id=f"{submission_id}-quarantined",
                    submission_id=submission_id,
                    event_kind="submission_quarantined",
                    prior_state=None,
                    next_state=Phase3BState.QUARANTINED,
                    reason_code="receipt_reserved",
                    recorded_at=admitted_at,
                ),
            )
            self._append_audit(
                connection,
                Phase3BAuditEntry(
                    event_id=f"{submission_id}-accepted",
                    submission_id=submission_id,
                    event_kind="submission_accepted",
                    prior_state=Phase3BState.QUARANTINED,
                    next_state=Phase3BState.ACCEPTED,
                    reason_code=(
                        "duplicate_submission"
                        if duplicate_of is not None
                        else "synthetic_pdf_admitted"
                    ),
                    recorded_at=admitted_at,
                ),
            )
        return self._record_from_submission_row(
            self._submission_row(submission_id)
        )

    def read_payload(self, submission_id: str) -> bytes:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT file_name FROM objects WHERE submission_id = ?",
                (submission_id,),
            ).fetchone()
        if row is None:
            raise DocumentAdmissionNotFound("object_not_found", submission_id)
        object_path = self._objects_dir / str(row["file_name"])
        encrypted = encrypted_object_from_json(
            object_path.read_text(encoding="utf-8")
        )
        return decrypt_object(self._master_key, encrypted)

    def store_inspection(
        self,
        submission_id: str,
        artifact: Phase3BInspectionArtifact,
        stored_at: datetime,
    ) -> Phase3BSubmissionRecord:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO inspection_artifacts (submission_id, artifact_json)
                VALUES (?, ?)
                """,
                (
                    submission_id,
                    json.dumps(
                        asdict(artifact),
                        sort_keys=True,
                        separators=(",", ":"),
                        default=str,
                    ),
                ),
            )
            self._update_state(
                connection,
                submission_id,
                prior_state=Phase3BState.ACCEPTED,
                next_state=Phase3BState.READY_FOR_REVIEW,
                reason_code="inspection_artifact_stored",
                recorded_at=stored_at,
            )
        return self._record_from_submission_row(self._submission_row(submission_id))

    def append_review(
        self,
        submission_id: str,
        decision: ReviewDecision,
        note: str,
        reviewed_at: datetime,
    ) -> Phase3BReviewAnnotation:
        prior = self._latest_annotation(submission_id)
        annotation = Phase3BReviewAnnotation(
            annotation_id=f"{submission_id}-{decision.value}-{int(reviewed_at.timestamp())}",
            submission_id=submission_id,
            decision=decision,
            actor_id="phase3b-local-operator",
            reason_code=f"review_{decision.value}",
            note=note,
            created_at=reviewed_at,
            prior_annotation_id=None if prior is None else prior.annotation_id,
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO review_annotations (
                    annotation_id, submission_id, decision, actor_id, reason_code,
                    note, created_at, prior_annotation_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    annotation.annotation_id,
                    annotation.submission_id,
                    annotation.decision.value,
                    annotation.actor_id,
                    annotation.reason_code,
                    annotation.note,
                    annotation.created_at.isoformat(),
                    annotation.prior_annotation_id,
                ),
            )
            next_state = _STATE_BY_DECISION[decision]
            current = self._state_for_submission(connection, submission_id)
            self._update_state(
                connection,
                submission_id,
                prior_state=current,
                next_state=next_state,
                reason_code=annotation.reason_code,
                recorded_at=reviewed_at,
                latest_review_decision=decision.value,
            )
        return annotation

    def delete_submission(
        self,
        submission_id: str,
        deleted_at: datetime,
        reason_code: str,
    ) -> Phase3BSubmissionRecord:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT file_name FROM objects WHERE submission_id = ?",
                (submission_id,),
            ).fetchone()
            if row is None:
                raise DocumentAdmissionNotFound("submission_not_found", submission_id)
            object_path = self._objects_dir / str(row["file_name"])
            if object_path.exists():
                object_path.unlink()
            current = self._state_for_submission(connection, submission_id)
            connection.execute(
                """
                UPDATE submissions
                SET state = ?, deleted_at = ?, updated_at = ?
                WHERE submission_id = ?
                """,
                (
                    Phase3BState.DELETED.value,
                    deleted_at.isoformat(),
                    deleted_at.isoformat(),
                    submission_id,
                ),
            )
            connection.execute(
                "UPDATE objects SET deleted_at = ? WHERE submission_id = ?",
                (deleted_at.isoformat(), submission_id),
            )
            self._append_audit(
                connection,
                Phase3BAuditEntry(
                    event_id=f"{submission_id}-deleted-{int(deleted_at.timestamp())}",
                    submission_id=submission_id,
                    event_kind="submission_deleted",
                    prior_state=current,
                    next_state=Phase3BState.DELETED,
                    reason_code=reason_code,
                    recorded_at=deleted_at,
                ),
            )
        return self._record_from_submission_row(self._submission_row(submission_id))

    def workspace_snapshot(self, generated_at: datetime) -> Phase3BWorkspaceSnapshot:
        with self._connect() as connection:
            submissions = tuple(
                self._record_from_submission_row(row)
                for row in connection.execute(
                    "SELECT * FROM submissions ORDER BY updated_at DESC"
                ).fetchall()
            )
            entries = tuple(
                self._audit_entry_from_row(row)
                for row in connection.execute(
                    "SELECT * FROM audit_entries ORDER BY recorded_at DESC LIMIT 20"
                ).fetchall()
            )
        return Phase3BWorkspaceSnapshot(
            submissions=submissions,
            recent_audit_entries=entries,
            warnings=(),
            generated_at=generated_at,
        )

    def submission_detail(self, submission_id: str) -> Phase3BSubmissionDetail:
        row = self._submission_row(submission_id)
        with self._connect() as connection:
            artifact_row = connection.execute(
                "SELECT artifact_json FROM inspection_artifacts WHERE submission_id = ?",
                (submission_id,),
            ).fetchone()
            review_rows = connection.execute(
                """
                SELECT * FROM review_annotations
                WHERE submission_id = ?
                ORDER BY created_at ASC
                """,
                (submission_id,),
            ).fetchall()
            audit_rows = connection.execute(
                """
                SELECT * FROM audit_entries
                WHERE submission_id = ?
                ORDER BY recorded_at ASC
                """,
                (submission_id,),
            ).fetchall()
        artifact = None
        if artifact_row is not None:
            values = json.loads(str(artifact_row["artifact_json"]))
            artifact = Phase3BInspectionArtifact(
                artifact_id=str(values["artifact_id"]),
                submission_id=str(values["submission_id"]),
                extraction_quality=ExtractionQuality(
                    values["extraction_quality"]
                ),
                pages=tuple(
                    Phase3BPageCapture(
                        page_number=int(page["page_number"]),
                        method=str(page["method"]),
                        text=str(page["text"]),
                        warnings=tuple(page["warnings"]),
                        limitations=tuple(page["limitations"]),
                    )
                    for page in values["pages"]
                ),
                warnings=tuple(values["warnings"]),
                omissions=tuple(values["omissions"]),
                limitations=tuple(values["limitations"]),
                native_text_sufficient=bool(values["native_text_sufficient"]),
                created_at=datetime.fromisoformat(str(values["created_at"])),
            )
        annotations = tuple(
            Phase3BReviewAnnotation(
                annotation_id=str(review_row["annotation_id"]),
                submission_id=str(review_row["submission_id"]),
                decision=ReviewDecision(str(review_row["decision"])),
                actor_id=str(review_row["actor_id"]),
                reason_code=str(review_row["reason_code"]),
                note=str(review_row["note"]),
                created_at=datetime.fromisoformat(str(review_row["created_at"])),
                prior_annotation_id=review_row["prior_annotation_id"],
            )
            for review_row in review_rows
        )
        return Phase3BSubmissionDetail(
            record=self._record_from_submission_row(row),
            inspection_artifact=artifact,
            review_annotations=annotations,
            audit_entries=tuple(
                self._audit_entry_from_row(audit_row) for audit_row in audit_rows
            ),
        )

    def recover(self, recovered_at: datetime) -> Phase3BRecoveryReport:
        reconciled: list[str] = []
        cleanup_failed: list[str] = []
        expired: list[str] = []
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM submissions").fetchall()
            for row in rows:
                submission_id = str(row["submission_id"])
                state = Phase3BState(str(row["state"]))
                if row["deleted_at"] is None and recovered_at >= datetime.fromisoformat(
                    str(row["expires_at"])
                ):
                    expired.append(submission_id)
                    self._update_state(
                        connection,
                        submission_id,
                        prior_state=state,
                        next_state=Phase3BState.EXPIRED,
                        reason_code="retention_expired",
                        recorded_at=recovered_at,
                    )
                    self._delete_submission_in_connection(
                        connection,
                        submission_id,
                        recovered_at,
                        "expiry_cleanup_completed",
                    )
                    continue
                object_row = connection.execute(
                    "SELECT file_name FROM objects WHERE submission_id = ?",
                    (submission_id,),
                ).fetchone()
                if object_row is None:
                    continue
                object_path = self._objects_dir / str(object_row["file_name"])
                if row["deleted_at"] is None and not object_path.exists():
                    cleanup_failed.append(submission_id)
                    self._update_state(
                        connection,
                        submission_id,
                        prior_state=state,
                        next_state=Phase3BState.CLEANUP_FAILED,
                        reason_code="missing_object_during_recovery",
                        recorded_at=recovered_at,
                    )
                else:
                    reconciled.append(submission_id)
        return Phase3BRecoveryReport(
            reconciled_submission_ids=tuple(sorted(set(reconciled))),
            cleanup_failed_submission_ids=tuple(sorted(set(cleanup_failed))),
            expired_submission_ids=tuple(sorted(set(expired))),
            recovered_at=recovered_at,
        )

    def _delete_submission_in_connection(
        self,
        connection: sqlite3.Connection,
        submission_id: str,
        deleted_at: datetime,
        reason_code: str,
    ) -> None:
        row = connection.execute(
            "SELECT file_name FROM objects WHERE submission_id = ?",
            (submission_id,),
        ).fetchone()
        if row is None:
            raise DocumentAdmissionNotFound("submission_not_found", submission_id)
        object_path = self._objects_dir / str(row["file_name"])
        if object_path.exists():
            object_path.unlink()
        current = self._state_for_submission(connection, submission_id)
        connection.execute(
            """
            UPDATE submissions
            SET state = ?, deleted_at = ?, updated_at = ?
            WHERE submission_id = ?
            """,
            (
                Phase3BState.DELETED.value,
                deleted_at.isoformat(),
                deleted_at.isoformat(),
                submission_id,
            ),
        )
        connection.execute(
            "UPDATE objects SET deleted_at = ? WHERE submission_id = ?",
            (deleted_at.isoformat(), submission_id),
        )
        self._append_audit(
            connection,
            Phase3BAuditEntry(
                event_id=f"{submission_id}-deleted-{int(deleted_at.timestamp())}",
                submission_id=submission_id,
                event_kind="submission_deleted",
                prior_state=current,
                next_state=Phase3BState.DELETED,
                reason_code=reason_code,
                recorded_at=deleted_at,
            ),
        )

    def _submission_row(self, submission_id: str) -> sqlite3.Row:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM submissions WHERE submission_id = ?",
                (submission_id,),
            ).fetchone()
        if row is None:
            raise DocumentAdmissionNotFound("submission_not_found", submission_id)
        return row

    def _existing_submission_for_digest(self, digest_hex: str) -> str | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT submission_id
                FROM submissions
                WHERE content_digest_hex = ? AND deleted_at IS NULL
                ORDER BY created_at ASC
                LIMIT 1
                """,
                (digest_hex,),
            ).fetchone()
        return None if row is None else str(row["submission_id"])

    def _latest_annotation(
        self, submission_id: str
    ) -> Phase3BReviewAnnotation | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM review_annotations
                WHERE submission_id = ?
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (submission_id,),
            ).fetchone()
        if row is None:
            return None
        return Phase3BReviewAnnotation(
            annotation_id=str(row["annotation_id"]),
            submission_id=str(row["submission_id"]),
            decision=ReviewDecision(str(row["decision"])),
            actor_id=str(row["actor_id"]),
            reason_code=str(row["reason_code"]),
            note=str(row["note"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            prior_annotation_id=row["prior_annotation_id"],
        )

    def _state_for_submission(
        self, connection: sqlite3.Connection, submission_id: str
    ) -> Phase3BState:
        row = connection.execute(
            "SELECT state FROM submissions WHERE submission_id = ?",
            (submission_id,),
        ).fetchone()
        if row is None:
            raise DocumentAdmissionNotFound("submission_not_found", submission_id)
        return Phase3BState(str(row["state"]))

    def _record_from_submission_row(
        self, row: sqlite3.Row
    ) -> Phase3BSubmissionRecord:
        return Phase3BSubmissionRecord(
            submission_id=str(row["submission_id"]),
            receipt_id=str(row["receipt_id"]),
            state=Phase3BState(str(row["state"])),
            content_identity=ContentIdentity(
                digest_policy_id="phase3b-sha256",
                digest_policy_version="1",
                algorithm="sha256",
                digest_hex=str(row["content_digest_hex"]),
                byte_count=int(row["byte_count"]),
            ),
            media_type=str(row["media_type"]),
            byte_count=int(row["byte_count"]),
            duplicate_of=row["duplicate_of"],
            created_at=datetime.fromisoformat(str(row["created_at"])),
            expires_at=datetime.fromisoformat(str(row["expires_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
            deleted_at=(
                None
                if row["deleted_at"] is None
                else datetime.fromisoformat(str(row["deleted_at"]))
            ),
            latest_review_decision=(
                None
                if row["latest_review_decision"] is None
                else ReviewDecision(str(row["latest_review_decision"]))
            ),
        )

    def _audit_entry_from_row(self, row: sqlite3.Row) -> Phase3BAuditEntry:
        return Phase3BAuditEntry(
            event_id=str(row["event_id"]),
            submission_id=str(row["submission_id"]),
            event_kind=str(row["event_kind"]),
            prior_state=(
                None
                if row["prior_state"] is None
                else Phase3BState(str(row["prior_state"]))
            ),
            next_state=(
                None
                if row["next_state"] is None
                else Phase3BState(str(row["next_state"]))
            ),
            reason_code=str(row["reason_code"]),
            recorded_at=datetime.fromisoformat(str(row["recorded_at"])),
        )

    def _append_audit(
        self,
        connection: sqlite3.Connection,
        entry: Phase3BAuditEntry,
    ) -> None:
        connection.execute(
            """
            INSERT INTO audit_entries (
                event_id, submission_id, event_kind, prior_state, next_state,
                reason_code, recorded_at, audit_mac_hex
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.event_id,
                entry.submission_id,
                entry.event_kind,
                None if entry.prior_state is None else entry.prior_state.value,
                None if entry.next_state is None else entry.next_state.value,
                entry.reason_code,
                entry.recorded_at.isoformat(),
                audit_hmac_hex(
                    self._master_key,
                    json.dumps(
                        asdict(entry),
                        sort_keys=True,
                        default=str,
                    ).encode("utf-8"),
                ),
            ),
        )

    def _update_state(
        self,
        connection: sqlite3.Connection,
        submission_id: str,
        *,
        prior_state: Phase3BState,
        next_state: Phase3BState,
        reason_code: str,
        recorded_at: datetime,
        latest_review_decision: str | None = None,
    ) -> None:
        connection.execute(
            """
            UPDATE submissions
            SET state = ?, updated_at = ?, latest_review_decision = COALESCE(?, latest_review_decision)
            WHERE submission_id = ?
            """,
            (
                next_state.value,
                recorded_at.isoformat(),
                latest_review_decision,
                submission_id,
            ),
        )
        self._append_audit(
            connection,
            Phase3BAuditEntry(
                event_id=f"{submission_id}-{next_state.value}-{int(recorded_at.timestamp())}",
                submission_id=submission_id,
                event_kind="state_transition",
                prior_state=prior_state,
                next_state=next_state,
                reason_code=reason_code,
                recorded_at=recorded_at,
            ),
        )
