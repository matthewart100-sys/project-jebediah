from __future__ import annotations

import re
from datetime import datetime

from .failures import PolicyViolation, ResourceLimitExceeded
from .models import (
    ExtractionQuality,
    Phase3BInspectionArtifact,
    Phase3BPageCapture,
)
from .policies import Phase3BPolicyBundle


_TEXT_PATTERN = re.compile(rb"SYNTHETIC-TEXT\[(\d+)\]:(.+)")


class Phase3BPDFPipeline:
    def __init__(self, policy: Phase3BPolicyBundle) -> None:
        self._policy = policy

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

        warnings: list[str] = []
        limitations: list[str] = []
        if b"EICAR" in payload:
            warnings.append("scanner_positive")
            limitations.append("scanner_positive")
        if b"SYNTHETIC-ENCRYPTED" in payload:
            limitations.append("encrypted_pdf")
        if (
            b"SYNTHETIC-JAVASCRIPT" in payload
            or b"/JavaScript" in payload
            or b"/OpenAction" in payload
        ):
            limitations.append("active_content")

        pages = tuple(
            Phase3BPageCapture(
                page_number=int(match.group(1)),
                method="native",
                text=match.group(2).decode("utf-8").strip(),
                warnings=tuple(warnings),
                limitations=tuple(limitations),
            )
            for match in _TEXT_PATTERN.finditer(payload)
        )
        native_text_sufficient = bool(pages)
        if not native_text_sufficient:
            warnings.append("native_text_unavailable")
            pages = (
                Phase3BPageCapture(
                    page_number=1,
                    method="native",
                    text="native text unavailable in synthetic fixture",
                    warnings=tuple(warnings),
                    limitations=tuple(limitations),
                ),
            )

        extraction_quality = (
            ExtractionQuality.COMPLETE
            if native_text_sufficient and not limitations
            else ExtractionQuality.PARTIAL
        )
        return Phase3BInspectionArtifact(
            artifact_id=f"artifact-{submission_id}",
            submission_id=submission_id,
            extraction_quality=extraction_quality,
            pages=pages,
            warnings=tuple(sorted(set(warnings))),
            omissions=(),
            limitations=(
                "Synthetic PDF inspection only.",
                "Only in-process native-text synthetic fixtures are supported.",
            ),
            native_text_sufficient=native_text_sufficient,
            created_at=inspected_at,
        )
