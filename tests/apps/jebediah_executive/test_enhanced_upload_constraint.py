"""Regression coverage for enhanced governed upload form submission."""

from pathlib import Path

from apps.jebediah_executive import rendering as r


UPLOAD_JS = (Path(r.__file__).with_name("static") / "upload.js").read_text(encoding="utf-8")


def test_enhanced_uploader_disables_native_required_file_constraint() -> None:
    """Queued files live in JS after the native picker is cleared.

    The HTML ``required`` attribute remains useful for the no-JavaScript fallback,
    but enhanced mode must remove it before the picker value is cleared. Otherwise
    browser constraint validation blocks the form before ``submitQueue`` can run.
    """
    remove_required = 'fileInput.removeAttribute("required")'
    clear_picker = 'fileInput.value = ""'
    submit_handler = 'form.addEventListener("submit", submitQueue)'

    assert remove_required in UPLOAD_JS
    assert clear_picker in UPLOAD_JS
    assert submit_handler in UPLOAD_JS
    assert UPLOAD_JS.index(remove_required) < UPLOAD_JS.index(clear_picker)
