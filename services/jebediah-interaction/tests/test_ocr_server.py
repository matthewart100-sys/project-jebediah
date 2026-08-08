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


class _MixedReader:
    def __init__(self, _stream, *, strict: bool = True) -> None:
        self.pages = [
            _Page("Native page one text"),
            _Page(""),
            _Page("Native page three text"),
        ]


def test_grounded_answer_budget_allows_complete_concise_response():
    assert 64 <= ocr_server.GOVERNED_ANSWER_MAX_TOKENS <= 512
    assert ocr_server.main.GOVERNED_ANSWER_MAX_TOKENS == ocr_server.GOVERNED_ANSWER_MAX_TOKENS
    assert ocr_server.GOVERNED_ANSWER_MAX_TOKENS > 32


def test_native_pdf_text_does_not_invoke_ocr(monkeypatch):
    monkeypatch.setattr(ocr_server, "PdfReader", _Reader)
    monkeypatch.setattr(
        ocr_server,
        "_run",
        lambda *_args, **_kwargs: pytest.fail("OCR must not run for searchable PDFs"),
    )
    payload = b"%PDF-1.7\nsynthetic\n%%EOF"
    assert ocr_server.extract_pdf_text(payload) == "Native searchable PDF text"


def test_mixed_pdf_preserves_native_pages_and_ocrs_only_missing_page(monkeypatch, tmp_path):
    monkeypatch.setattr(ocr_server, "PdfReader", _MixedReader)
    monkeypatch.setattr(ocr_server, "OCR_SCRATCH_ROOT", str(tmp_path))
    calls: list[int] = []

    def fake_ocr(_source, page_number, _root, *, timeout):
        calls.append(page_number)
        assert timeout > 0
        return "OCR page two text"

    monkeypatch.setattr(ocr_server, "_ocr_page", fake_ocr)
    payload = b"%PDF-1.7\nsynthetic\n%%EOF"
    result = ocr_server.extract_pdf_text(payload)
    assert calls == [2]
    assert result == "Native page one text OCR page two text Native page three text"


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


def test_ocr_scratch_fails_closed_when_memory_root_unavailable(monkeypatch, tmp_path):
    missing = tmp_path / "missing"
    monkeypatch.setattr(ocr_server, "OCR_SCRATCH_ROOT", str(missing))
    with pytest.raises(HTTPException) as caught:
        ocr_server._scratch_parent()
    assert caught.value.status_code == 503
    assert caught.value.detail == "ocr_scratch_unavailable"
