"""Governed OCR bootstrap for the interaction service.

Extends the existing admission API with bounded local OCR for scanned PDFs.
Native PDF text is always preferred. OCR output enters the exact same encrypted
review_pending custody and human-promotion boundary as native extraction.
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
    """Extract native text, falling back to Tesseract for image-only PDFs."""
    if not payload.startswith(b"%PDF-") or b"%%EOF" not in payload[-2048:]:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure")

    try:
        reader = PdfReader(BytesIO(payload), strict=True)
        page_count = len(reader.pages)
        if page_count == 0:
            raise HTTPException(status_code=422, detail="invalid_pdf_structure")
        if page_count > OCR_MAX_PAGES:
            raise HTTPException(status_code=422, detail="pdf_page_limit_exceeded")
        native = _normalize("\n".join(page.extract_text() or "" for page in reader.pages))
    except HTTPException:
        raise
    except (PdfReadError, ValueError, TypeError) as error:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure") from error

    if len(native) >= OCR_MIN_CHARACTERS:
        return native

    with tempfile.TemporaryDirectory(prefix="jebediah-ocr-") as temporary:
        root = Path(temporary)
        source = root / "source.pdf"
        page_prefix = root / "page"
        source.write_bytes(payload)

        raster_command = [
            "pdftoppm",
            "-f", "1",
            "-l", str(page_count),
            "-r", str(OCR_DPI),
            "-png",
        ]
        if page_count == 1:
            raster_command.append("-singlefile")
        raster_command.extend([str(source), str(page_prefix)])
        _run(raster_command, timeout=OCR_TIMEOUT_SECONDS)

        images = sorted(root.glob("page*.png"))
        if not images:
            raise HTTPException(status_code=422, detail="ocr_render_failed")

        extracted: list[str] = []
        per_page_timeout = max(10, OCR_TIMEOUT_SECONDS // max(1, len(images)))
        for image in images[:OCR_MAX_PAGES]:
            result = _run(
                [
                    "tesseract", str(image), "stdout",
                    "-l", OCR_LANGUAGE,
                    "--oem", "1",
                    "--psm", "3",
                ],
                timeout=per_page_timeout,
            )
            extracted.append(result.stdout)

    normalized = _normalize("\n".join(extracted))
    if len(normalized) < OCR_MIN_CHARACTERS:
        raise HTTPException(status_code=422, detail="ocr_contains_no_extractable_text")
    return normalized


# Rebind only the extraction boundary. Authentication, encrypted candidate
# custody, review_pending state, workspace isolation, human approval, promotion,
# and grounded retrieval remain controlled by the existing canonical routes.
main._extract_pdf_text = extract_pdf_text


if __name__ == "__main__":
    uvicorn.run(main.app, host="0.0.0.0", port=8001)
