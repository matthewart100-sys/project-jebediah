from __future__ import annotations

from datetime import datetime

from .durable_repository import Phase3BDurableRepository
from .models import Phase3BRecoveryReport, Phase3BSubmissionDetail


class Phase3BLifecycleService:
    def __init__(self, repository: Phase3BDurableRepository) -> None:
        self._repository = repository

    def delete(
        self,
        submission_id: str,
        deleted_at: datetime,
        *,
        reason_code: str,
    ) -> Phase3BSubmissionDetail:
        self._repository.delete_submission(
            submission_id,
            deleted_at,
            reason_code,
        )
        return self._repository.submission_detail(submission_id)

    def recover(self, recovered_at: datetime) -> Phase3BRecoveryReport:
        return self._repository.recover(recovered_at)
