from __future__ import annotations

from datetime import datetime

from .durable_repository import Phase3BDurableRepository
from .models import Phase3BSubmissionDetail, ReviewDecision


class Phase3BReviewService:
    def __init__(self, repository: Phase3BDurableRepository) -> None:
        self._repository = repository

    def apply(
        self,
        submission_id: str,
        decision: ReviewDecision,
        note: str,
        reviewed_at: datetime,
    ) -> Phase3BSubmissionDetail:
        self._repository.append_review(
            submission_id,
            decision,
            note,
            reviewed_at,
        )
        return self._repository.submission_detail(submission_id)
