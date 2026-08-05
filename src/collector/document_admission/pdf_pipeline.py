from __future__ import annotations

import re
from datetime import datetime

from .failures import InspectionFailed, PolicyViolation, ResourceLimitExceeded
from .interfaces import DocumentWorkerRunner
from .models import (
    ExtractionQuality,
    Phase3BInspectionArtifact,
    Phase3BPageCapture,
)
from .policies import Phase3BPolicyBundle
from .worker_protocol import coerce_worker_result


_TEXT_PATTERN = re.compile(rb"SYNTHETIC-TEXT\[(\d+)\]:(.+)")
_OCR_PATTERN = re.compile(rb"SYNTHETIC-OCR\[(\d+)\]:(.+)")


class InProcessSyntheticWorkerRunner(DocumentWorkerRunner):
    def run(self, worker_kind: str, payload: bytes) -> dict[str, object]:
        if worker_kind == "scanner":
            if b"EICAR" in payload:
                return {
                    "status": "reviewable",
                    "pages": (),
                    "warnings": ("scanner_positive",),
                    "findings": ("scanner_positive",),
                    "native_text_sufficient": False,
                }
            return {
                "status": "clean",
                "pages": (),
                "warnings": (),
                "findings": (),
                "native_text_sufficient": False,
            }
        if worker_kind == "inspector":
            warnings: list[str] = []
            findings: list[str] = []
            if b"SYNTHETIC-ENCRYPTED" in payload:
                findings.append("encrypted_pdf")
            if (
                b"SYNTHETIC-JAVASCRIPT" in payload
                or b"/JavaScript" in payload
                or b"/OpenAction" in payload
            ):
                findings.append("active_content")
            pages = [
                {
                    "page_number": int(match.group(1)),
                    "method": "native",
                    "text": match.group(2).decode("utf-8").strip(),
                }
                for match in _TEXT_PATTERN.finditer(payload)
            ]
            native_text_sufficient = bool(pages)
            if not pages:
                warnings.append("native_text_missing")
            return {
                "status": "reviewable",
                "pages": tuple(pages),
                "warnings": tuple(warnings),
                "findings": tuple(findings),
                "native_text_sufficient": native_text_sufficient,
            }
        if worker_kind == "ocr":
            pages = [
                {
                    "page_number": int(match.group(1)),
                    "method": "ocr",
                    "text": match.group(2).decode("utf-8").strip(),
                }
                for match in _OCR_PATTERN.finditer(payload)
            ]
            if not pages:
                pages = (
                    {
                        "page_number": 1,
                        "method": "ocr",
                        "text": "synthetic ocr unavailable",
                    },
                )
            return {
                "status": "reviewable",
                "pages": tuple(pages),
                "warnings": ("ocr_fallback_used",),
                "findings": (),
                "native_text_sufficient": False,
            }
        raise InspectionFailed("unknown_worker_kind", worker_kind)


class Phase3BPDFPipeline:
    def __init__(
        self,
        policy: Phase3BPolicyBundle,
        runner: DocumentWorkerRunner,
    ) -> None:
        self._policy = policy
        self._runner = runner

    def inspect_payload(
        self,
        submission_id: str,
        media_type: str,
        payload: bytes,
        inspected_at: datetime,
    ) -> Phase3BInspectionArtifact:
        if media_type != self._policy.allowed_media_type:
            raise PolicyViolation("media_type_not_allowed", submission_id)
        if len(payload) > self._policy.max_pdf_bytes:
            raise ResourceLimitExceeded("max_pdf_bytes_exceeded", submission_id)
        if not payload.startswith(b"%PDF-"):
            raise PolicyViolation("invalid_pdf_signature", submission_id)

        scanner = coerce_worker_result(
            "scanner",
            self._runner.run("scanner", payload),
            created_at=inspected_at,
        )
        inspector = coerce_worker_result(
            "inspector",
            self._runner.run("inspector", payload),
            created_at=inspected_at,
        )

        page_map: dict[int, Phase3BPageCapture] = {
            page.page_number: Phase3BPageCapture(
                page_number=page.page_number,
                method=page.method,
                text=page.text,
                warnings=inspector.warnings,
                limitations=inspector.findings,
            )
            for page in inspector.pages
        }
        native_text_sufficient = inspector.native_text_sufficient
        warnings = list(scanner.warnings + inspector.warnings)
        findings = list(scanner.findings + inspector.findings)
        if not native_text_sufficient:
            ocr = coerce_worker_result(
                "ocr",
                self._runner.run("ocr", payload),
                created_at=inspected_at,
            )
            warnings.extend(ocr.warnings)
            for page in ocr.pages:
                page_map[page.page_number] = Phase3BPageCapture(
                    page_number=page.page_number,
                    method=page.method,
                    text=page.text,
                    warnings=ocr.warnings,
                    limitations=tuple(findings),
                )

        pages = tuple(page_map[index] for index in sorted(page_map))
        if not pages:
            raise InspectionFailed("no_reviewable_pages", submission_id)
        extraction_quality = (
            ExtractionQuality.COMPLETE
            if native_text_sufficient and not findings
            else ExtractionQuality.PARTIAL
        )
        return Phase3BInspectionArtifact(
            artifact_id=f"artifact-{submission_id}",
            submission_id=submission_id,
            extraction_quality=extraction_quality,
            pages=pages,
            warnings=tuple(sorted(set(warnings))),
            omissions=("phase3c_consumer_absent",),
            limitations=(
                "Synthetic PDF inspection only.",
                "No governed knowledge promotion occurs in Phase 3B.",
            ),
            native_text_sufficient=native_text_sufficient,
            created_at=inspected_at,
        )
