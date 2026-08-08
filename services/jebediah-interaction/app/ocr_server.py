"""Governed OCR bootstrap for the interaction service.

Extends the existing admission API with bounded local OCR for scanned PDF pages.
Native text is preserved page-by-page; only pages without meaningful native text
are rasterized and OCR'd. Scratch data prefers a memory-backed filesystem and is
always removed when the request finishes.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import time
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
OCR_SCRATCH_ROOT = os.getenv("JEBEDIAH_OCR_SCRATCH_ROOT", "/dev/shm")


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


def _scratch_parent() -> str | None:
    root = Path(OCR_SCRATCH_ROOT)
    if root.is_dir() and os.access(root, os.W_OK):
        return str(root)
    # Fail closed rather than silently placing plaintext evidence on a persistent
    # filesystem. Operators may point JEBEDIAH_OCR_SCRATCH_ROOT at another tmpfs.
    raise HTTPException(status_code=503, detail="ocr_scratch_unavailable")


def _ocr_page(source: Path, page_number: int, root: Path, *, timeout: int) -> str:
    prefix = root / f"page-{page_number}"
    _run(
        [
            "pdftoppm",
            "-f", str(page_number),
            "-l", str(page_number),
            "-r", str(OCR_DPI),
            "-png",
            "-singlefile",
            str(source),
            str(prefix),
        ],
        timeout=timeout,
    )
    image = prefix.with_suffix(".png")
    if not image.is_file():
        raise HTTPException(status_code=422, detail="ocr_render_failed")
    result = _run(
        [
            "tesseract", str(image), "stdout",
            "-l", OCR_LANGUAGE,
            "--oem", "1",
            "--psm", "3",
        ],
        timeout=timeout,
    )
    return _normalize(result.stdout)


def extract_pdf_text(payload: bytes) -> str:
    """Preserve native text and OCR only image-only pages, in document order."""
    if not payload.startswith(b"%PDF-") or b"%%EOF" not in payload[-2048:]:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure")

    try:
        reader = PdfReader(BytesIO(payload), strict=True)
        pages = list(reader.pages)
        page_count = len(pages)
        if page_count == 0:
            raise HTTPException(status_code=422, detail="invalid_pdf_structure")
        if page_count > OCR_MAX_PAGES:
            raise HTTPException(status_code=422, detail="pdf_page_limit_exceeded")
        native_pages = [_normalize(page.extract_text() or "") for page in pages]
    except HTTPException:
        raise
    except (PdfReadError, ValueError, TypeError) as error:
        raise HTTPException(status_code=422, detail="invalid_pdf_structure") from error

    missing_pages = [
        index for index, text in enumerate(native_pages, start=1)
        if len(text) < OCR_MIN_CHARACTERS
    ]
    if not missing_pages:
        return " ".join(native_pages).strip()

    started = time.monotonic()
    with tempfile.TemporaryDirectory(
        prefix="jebediah-ocr-", dir=_scratch_parent()
    ) as temporary:
        root = Path(temporary)
        source = root / "source.pdf"
        source.write_bytes(payload)
        final_pages = list(native_pages)
        for page_number in missing_pages:
            remaining = OCR_TIMEOUT_SECONDS - int(time.monotonic() - started)
            if remaining <= 0:
                raise HTTPException(status_code=422, detail="ocr_timeout")
            page_timeout = max(1, min(remaining, OCR_TIMEOUT_SECONDS))
            final_pages[page_number - 1] = _ocr_page(
                source, page_number, root, timeout=page_timeout
            )

    normalized = " ".join(text for text in final_pages if text).strip()
    if len(normalized) < OCR_MIN_CHARACTERS:
        raise HTTPException(status_code=422, detail="ocr_contains_no_extractable_text")
    return normalized


# Rebind only the extraction boundary. Authentication, encrypted candidate
# custody, review_pending state, workspace isolation, human approval, promotion,
# and grounded retrieval remain controlled by the existing canonical routes.
main._extract_pdf_text = extract_pdf_text


if __name__ == "__main__":
    uvicorn.run(main.app, host="0.0.0.0", port=8001)
