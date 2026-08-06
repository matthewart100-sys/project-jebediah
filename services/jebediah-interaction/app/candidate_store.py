"""Encrypted durable custody for pending interaction admission candidates."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import sqlite3

from cryptography.fernet import Fernet, InvalidToken


class CandidateStoreError(RuntimeError):
    """Candidate custody could not be read or updated safely."""


@dataclass(frozen=True)
class AdmissionCandidate:
    candidate_id: str
    source_record_id: str
    organization_id: str
    workspace_mode: str
    file_name: str
    content: str
    promoted_memory_id: str | None = None
    governance_state: str = "review_pending"


class CandidateStore:
    def __init__(self, database_path: Path, encryption_key: str) -> None:
        if not encryption_key:
            raise CandidateStoreError("interaction_state_key_required")
        try:
            self._fernet = Fernet(encryption_key.encode("ascii"))
        except (ValueError, UnicodeEncodeError) as error:
            raise CandidateStoreError("interaction_state_key_invalid") from error
        self._database_path = database_path
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS admission_candidates (
                    candidate_id TEXT PRIMARY KEY,
                    source_record_id TEXT NOT NULL,
                    organization_id TEXT NOT NULL,
                    workspace_mode TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    encrypted_content BLOB NOT NULL,
                    promoted_memory_id TEXT,
                    governance_state TEXT NOT NULL DEFAULT 'review_pending'
                )
                """
            )
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(admission_candidates)"
                ).fetchall()
            }
            if "governance_state" not in columns:
                connection.execute(
                    """
                    ALTER TABLE admission_candidates
                    ADD COLUMN governance_state TEXT NOT NULL DEFAULT 'review_pending'
                    """
                )

    def store(self, candidate: AdmissionCandidate) -> None:
        encrypted_content = self._fernet.encrypt(candidate.content.encode("utf-8"))
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO admission_candidates (
                    candidate_id,
                    source_record_id,
                    organization_id,
                    workspace_mode,
                    file_name,
                    encrypted_content,
                    promoted_memory_id,
                    governance_state
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    candidate.candidate_id,
                    candidate.source_record_id,
                    candidate.organization_id,
                    candidate.workspace_mode,
                    candidate.file_name,
                    encrypted_content,
                    candidate.promoted_memory_id,
                    candidate.governance_state,
                ),
            )

    def get(self, candidate_id: str) -> AdmissionCandidate | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT candidate_id, source_record_id, organization_id,
                       workspace_mode, file_name, encrypted_content,
                       promoted_memory_id, governance_state
                FROM admission_candidates
                WHERE candidate_id = ?
                """,
                (candidate_id,),
            ).fetchone()
        if row is None:
            return None
        try:
            content = self._fernet.decrypt(row["encrypted_content"]).decode("utf-8")
        except (InvalidToken, UnicodeDecodeError) as error:
            raise CandidateStoreError("candidate_content_decryption_failed") from error
        return AdmissionCandidate(
            candidate_id=row["candidate_id"],
            source_record_id=row["source_record_id"],
            organization_id=row["organization_id"],
            workspace_mode=row["workspace_mode"],
            file_name=row["file_name"],
            content=content,
            promoted_memory_id=row["promoted_memory_id"],
            governance_state=row["governance_state"],
        )

    def mark_promoted(self, candidate_id: str, memory_id: str) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE admission_candidates
                SET promoted_memory_id = ?, governance_state = 'promoted'
                WHERE candidate_id = ?
                  AND governance_state IN ('review_pending', 'promoted')
                  AND (promoted_memory_id IS NULL OR promoted_memory_id = ?)
                """,
                (memory_id, candidate_id, memory_id),
            )
        if cursor.rowcount != 1:
            raise CandidateStoreError("candidate_promotion_conflict")

    def mark_rejected(self, candidate_id: str) -> None:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE admission_candidates
                SET governance_state = 'rejected'
                WHERE candidate_id = ?
                  AND governance_state IN ('review_pending', 'rejected')
                  AND promoted_memory_id IS NULL
                """,
                (candidate_id,),
            )
        if cursor.rowcount != 1:
            raise CandidateStoreError("candidate_rejection_conflict")


_candidate_store: CandidateStore | None = None


def get_candidate_store() -> CandidateStore:
    global _candidate_store
    if _candidate_store is None:
        database_path = Path(
            os.getenv(
                "INTERACTION_STATE_PATH",
                "/var/lib/jebediah-interaction/state.sqlite3",
            )
        )
        _candidate_store = CandidateStore(
            database_path,
            os.getenv("INTERACTION_STATE_KEY", ""),
        )
    return _candidate_store
