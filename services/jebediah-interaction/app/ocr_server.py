"""Governed OCR bootstrap for the interaction service.

This module keeps the existing admission API intact while extending PDF extraction
with a bounded, local-only OCR fallback for image-only/scanned PDFs. Native PDF
text remains preferred. OCR output follows the same review_pending custody and
human-promotion boundary as every other extracted document.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

import uvicorn
from fastapi import HTTPException
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from . import main

OCR_MAX_PAGES = int(os.getenv("JEBEDIAH_OCR_MAX_PAGES", "25"))
OCR_DPI = int(os.getenv("JEBEDIAH_OCR_DPI", "200"))
OCR_TIMEOUT_SECONDS = int(os.getenv("JEBEDIAH_OCR_TIMEOUT_SECONDS", "90"))
OCR_LANGUAGE = os.getenv("JEBEDIAH_OCR_LANGUAGE", "eng")
OCR_MIN_CHARACTERS = int(os.getenv("JEBEDIAH_OCR_MIN_CHARACTERS", "8"))


def _normalize(content: str) -> str:
    return " ".join(
        re.findall(r"[A-Za-z0-9][A-Za-z0-9 .,;:()'/-]*", content)
    ).strip()


def _run(command: list[str], *, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={"PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin")},
        )
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail="ocr_runtime_unavailable") from error
    except subprocess.TimeoutExpired as error:
        raise HTTPException(status_code=422, detail="ocr_timeout") from error
    except subprocess.CalledProcessError as error:
        raise HTTPException(status_code=422, detail="ocr_processing_failed") from error


def extract_pdf_text(payload: bytes) -> str:
    """Extract native text, falling back to bounded Tesseract OCR when necessary."""
    if not payload.startswith(b"%PDF-") or b"%%EOF" not in payload[-2048:]:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure")

    try:
        reader = PdfReader(BytesIO(payload), strict=True)
        if len(reader.pages) > OCR_MAX_PAGES:
            raise HTTPException(status_code=422, detail="pdf_page_limit_exceeded")
        native = _normalize("\n".join(page.extract_text() or "" for page in reader.pages))
    except HTTPException:
        raise
    except (PdfReadError, ValueError, TypeError) as error:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure") from error

    # Prefer deterministic native extraction. OCR is only a fallback when the
    # document contains no meaningful machine-readable text layer.
    if len(native) >= OCR_MIN_CHARACTERS:
        return native

    with tempfile.TemporaryDirectory(prefix="jebediah-ocr-") as temporary:
        root = Path(temporary)
        source = root / "source.pdf"
        page_prefix = root / "page"
        source.write_bytes(payload)

        _run(
            [
                "pdftoppm",
                "-f", "1",
                "-l", str(OCR_MAX_PAGES),
                "-r", str(OCR_DPI),
                "-png",
                "-singlefile" if len(reader.pages) == 1 else "-png",
                str(source),
                str(page_prefix),
            ],
            timeout=OCR_TIMEOUT_SECONDS,
        )

        images = sorted(root.glob("page*.png"))
        if not images:
            raise HTTPException(status_code=422, detail="ocr_render_failed")

        extracted: list[str] = []
        remaining = OCR_TIMEOUT_SECONDS
        for image in images[:OCR_MAX_PAGES]:
            result = _run(
                [
                    "tesseract",
                    str(image),
                    "stdout",
                    "-l", OCR_LANGUAGE,
                    "--oem", "1",
                    "--psm", "3",
                ],
                timeout=max(5, remaining),
            )
            extracted.append(result.stdout)
            remaining = max(5, remaining - 5)

    normalized = _normalize("\n".join(extracted))
    if len(normalized) < OCR_MIN_CHARACTERS:
        raise HTTPException(status_code=422, detail="ocr_contains_no_extractable_text")
    return normalized


# The existing route calls main._extract_pdf_text. Rebind only that extraction
# boundary; admission authorization, encrypted candidate custody, review_pending,
# promotion, workspace isolation, and provenance remain unchanged.
main._extract_pdf_text = extract_pdf_text


if __name__ == "__main__":
    uvicorn.run(main.app, host="0.0.0.0", port=8001)
