from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .failures import DocumentAdmissionValidationError
from .models import _normalize_string_tuple, _require_aware, _require_non_empty


@dataclass(frozen=True)
class WorkerPageResult:
    page_number: int
    method: str
    text: str

    def __post_init__(self) -> None:
        if type(self.page_number) is not int or self.page_number <= 0:
            raise DocumentAdmissionValidationError("invalid_page_number")
        if self.method not in {"native", "ocr"}:
            raise DocumentAdmissionValidationError("invalid_page_method")
        _require_non_empty(self.text, "text")


@dataclass(frozen=True)
class WorkerResult:
    worker_kind: str
    status: str
    pages: tuple[WorkerPageResult, ...]
    warnings: tuple[str, ...]
    findings: tuple[str, ...]
    native_text_sufficient: bool
    created_at: datetime

    def __post_init__(self) -> None:
        _require_non_empty(self.worker_kind, "worker_kind")
        if self.status not in {"clean", "infected", "reviewable"}:
            raise DocumentAdmissionValidationError("invalid_worker_status")
        if not isinstance(self.pages, tuple):
            raise DocumentAdmissionValidationError("invalid_pages")
        for page in self.pages:
            if not isinstance(page, WorkerPageResult):
                raise DocumentAdmissionValidationError("invalid_pages")
        object.__setattr__(
            self,
            "warnings",
            _normalize_string_tuple(self.warnings, "warnings"),
        )
        object.__setattr__(
            self,
            "findings",
            _normalize_string_tuple(self.findings, "findings"),
        )
        if type(self.native_text_sufficient) is not bool:
            raise DocumentAdmissionValidationError(
                "invalid_native_text_sufficient"
            )
        _require_aware(self.created_at, "created_at")


def coerce_worker_result(
    worker_kind: str,
    payload: dict[str, object],
    *,
    created_at: datetime,
) -> WorkerResult:
    if set(payload.keys()) != {
        "status",
        "pages",
        "warnings",
        "findings",
        "native_text_sufficient",
    }:
        raise DocumentAdmissionValidationError("invalid_worker_payload_shape")
    pages = tuple(
        WorkerPageResult(
            page_number=int(item["page_number"]),
            method=str(item["method"]),
            text=str(item["text"]),
        )
        for item in payload["pages"]
    )
    return WorkerResult(
        worker_kind=worker_kind,
        status=str(payload["status"]),
        pages=pages,
        warnings=tuple(str(value) for value in payload["warnings"]),
        findings=tuple(str(value) for value in payload["findings"]),
        native_text_sufficient=bool(payload["native_text_sufficient"]),
        created_at=created_at,
    )
