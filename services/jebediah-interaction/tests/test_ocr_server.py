from __future__ import annotations

import subprocess

import pytest
from fastapi import HTTPException

from app import ocr_server


class _Page:
    def __init__(self, text: str) -> None:
        self._text = text

    def extract_text(self) -> str:
        return self._text


class _Reader:
    def __init__(self, _stream, *, strict: bool = True) -> None:
        self.pages = [_Page("Native searchable PDF text")]


def test_native_pdf_text_does_not_invoke_ocr(monkeypatch):
    monkeypatch.setattr(ocr_server, "PdfReader", _Reader)
    monkeypatch.setattr(
        ocr_server,
        "_run",
        lambda *_args, **_kwargs: pytest.fail("OCR must not run for searchable PDFs"),
    )
    payload = b"%PDF-1.7\nsynthetic\n%%EOF"
    assert ocr_server.extract_pdf_text(payload) == "Native searchable PDF text"


def test_invalid_pdf_is_rejected_before_ocr():
    with pytest.raises(HTTPException) as caught:
        ocr_server.extract_pdf_text(b"not-a-pdf")
    assert caught.value.detail == "invalid_pdf_structure"


def test_missing_ocr_binary_has_explicit_failure(monkeypatch):
    def missing(*_args, **_kwargs):
        raise FileNotFoundError("tesseract")

    monkeypatch.setattr(subprocess, "run", missing)
    with pytest.raises(HTTPException) as caught:
        ocr_server._run(["tesseract", "x", "stdout"], timeout=5)
    assert caught.value.status_code == 503
    assert caught.value.detail == "ocr_runtime_unavailable"


def test_ocr_timeout_has_explicit_failure(monkeypatch):
    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="tesseract", timeout=5)

    monkeypatch.setattr(subprocess, "run", timeout)
    with pytest.raises(HTTPException) as caught:
        ocr_server._run(["tesseract", "x", "stdout"], timeout=5)
    assert caught.value.detail == "ocr_timeout"
