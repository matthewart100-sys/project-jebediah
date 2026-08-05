import pytest

from collector.document_admission import (
    DocumentFormat,
    FormatDetectionState,
)

from .synthetic_fixtures import (
    AMBIGUOUS,
    DETECTOR_UNAVAILABLE,
    NOW,
    TRUNCATED,
    UNSUPPORTED,
    VALID_DOCX_MARKER,
    VALID_MARKDOWN,
    VALID_PDF_MARKER,
    VALID_TXT,
    ScriptedFormatDetector,
    build_envelope,
    build_policies,
)


@pytest.mark.parametrize(
    ("payload", "safe_name", "media_type", "expected_format"),
    [
        (
            VALID_TXT,
            "synthetic.txt",
            "text/plain",
            DocumentFormat.TXT,
        ),
        (
            VALID_MARKDOWN,
            "synthetic.md",
            "text/markdown",
            DocumentFormat.MARKDOWN,
        ),
        (
            VALID_PDF_MARKER,
            "synthetic.pdf",
            "application/pdf",
            DocumentFormat.PDF,
        ),
        (
            VALID_DOCX_MARKER,
            "synthetic.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            DocumentFormat.DOCX,
        ),
    ],
)
def test_supported_synthetic_signatures_are_detected(
    payload,
    safe_name,
    media_type,
    expected_format,
):
    result = ScriptedFormatDetector().detect(
        payload,
        build_envelope(
            supplied_name=safe_name,
            safe_name=safe_name,
            claimed_media_type=media_type,
        ),
        "attempt-1",
        "detection-1",
        build_policies().resources,
        NOW,
    )
    assert result.state is FormatDetectionState.DETECTED
    assert result.detected_format is expected_format


@pytest.mark.parametrize(
    ("payload", "expected_state", "reason_code"),
    [
        (
            UNSUPPORTED,
            FormatDetectionState.UNSUPPORTED,
            "unsupported_format",
        ),
        (
            TRUNCATED,
            FormatDetectionState.UNSUPPORTED,
            "truncated_input",
        ),
        (
            AMBIGUOUS,
            FormatDetectionState.AMBIGUOUS,
            "ambiguous_format",
        ),
        (
            DETECTOR_UNAVAILABLE,
            FormatDetectionState.UNAVAILABLE,
            "detector_unavailable",
        ),
    ],
)
def test_nonconclusive_detection_never_reports_supported(
    payload,
    expected_state,
    reason_code,
):
    result = ScriptedFormatDetector().detect(
        payload,
        build_envelope(),
        "attempt-1",
        "detection-1",
        build_policies().resources,
        NOW,
    )
    assert result.state is expected_state
    assert result.detected_format is None
    assert result.reason_code == reason_code


@pytest.mark.parametrize(
    ("safe_name", "media_type"),
    [
        ("spoofed.txt", "application/pdf"),
        ("spoofed.pdf", "text/plain"),
    ],
)
def test_extension_or_media_type_spoofing_is_unsupported(
    safe_name,
    media_type,
):
    result = ScriptedFormatDetector().detect(
        VALID_PDF_MARKER,
        build_envelope(
            supplied_name=safe_name,
            safe_name=safe_name,
            claimed_media_type=media_type,
        ),
        "attempt-1",
        "detection-1",
        build_policies().resources,
        NOW,
    )
    assert result.state is FormatDetectionState.UNSUPPORTED
    assert result.reason_code == "type_mismatch"


def test_path_traversal_metadata_is_unsupported():
    result = ScriptedFormatDetector().detect(
        VALID_TXT,
        build_envelope(supplied_name="../synthetic.txt"),
        "attempt-1",
        "detection-1",
        build_policies().resources,
        NOW,
    )
    assert result.state is FormatDetectionState.UNSUPPORTED
    assert result.reason_code == "path_traversal"
