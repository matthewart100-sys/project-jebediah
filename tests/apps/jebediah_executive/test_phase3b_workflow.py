from datetime import datetime, timezone

from apps.jebediah_executive.app import create_app
from apps.jebediah_executive.models import (
    Phase3BReviewEntryView,
    Phase3BSubmissionDetailView,
    Phase3BSubmissionState,
    Phase3BSubmissionSummary,
    Phase3BWorkspaceView,
)


class _WorkflowService:
    def __init__(self) -> None:
        self.summary = Phase3BSubmissionSummary(
            submission_id="demo-submission-1",
            title="Synthetic roster PDF",
            state=Phase3BSubmissionState.READY_FOR_REVIEW,
            received_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            sha256_hex="a" * 64,
            byte_count=128,
            duplicate_of=None,
            warnings=("ocr_fallback_used",),
        )

    def workspace_page(self) -> Phase3BWorkspaceView:
        return Phase3BWorkspaceView(
            generated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
            submissions=(self.summary,),
            recent_events=("submission_accepted",),
            limitations=("Synthetic only.",),
        )

    def submission_page(self, submission_id: str) -> Phase3BSubmissionDetailView | None:
        if submission_id != self.summary.submission_id:
            return None
        return Phase3BSubmissionDetailView(
            summary=self.summary,
            native_text_sufficient=False,
            page_count=2,
            review_entries=(
                Phase3BReviewEntryView(
                    decision="approve",
                    note="Approved",
                    created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                ),
            ),
            warnings=("ocr_fallback_used",),
            limitations=("Synthetic only.",),
        )

    def admit_pdf(self, **kwargs):  # pragma: no cover - not used here
        raise AssertionError("not used")

    def review_submission(self, **kwargs):  # pragma: no cover - not used here
        raise AssertionError("not used")

    def delete_submission(self, submission_id: str):  # pragma: no cover - not used
        raise AssertionError(submission_id)

    def recover(self) -> None:  # pragma: no cover - not used here
        return None


def test_phase3b_operator_workflow_pages_are_rendered() -> None:
    app = create_app(workspace_service=_WorkflowService())
    captured: dict[str, object] = {}

    def start_response(status: str, headers):
        captured["status"] = status
        captured["headers"] = headers

    workspace_body = b"".join(
        app(
            {
                "REQUEST_METHOD": "GET",
                "PATH_INFO": "/workspace",
                "QUERY_STRING": "",
                "wsgi.input": None,
                "SERVER_NAME": "127.0.0.1",
                "SERVER_PORT": "8765",
            },
            start_response,
        )
    )
    assert captured["status"] == "200 OK"
    assert b"Admit synthetic PDF" in workspace_body

    detail_body = b"".join(
        app(
            {
                "REQUEST_METHOD": "GET",
                "PATH_INFO": "/workspace/submissions/demo-submission-1",
                "QUERY_STRING": "",
                "wsgi.input": None,
                "SERVER_NAME": "127.0.0.1",
                "SERVER_PORT": "8765",
            },
            start_response,
        )
    )
    assert captured["status"] == "200 OK"
    assert b"Record review decision" in detail_body
