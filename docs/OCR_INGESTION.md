# Governed OCR ingestion

Bonsaai treats scanned/image-only PDFs as first-class evidence.

## Runtime behavior

1. Validate PDF structure and enforce the admission byte limit already applied by the API.
2. Enforce a bounded PDF page count (`JEBEDIAH_OCR_MAX_PAGES`, default 25).
3. Prefer the PDF's native text layer when it contains meaningful text.
4. If native extraction is empty/insufficient, rasterize pages locally with Poppler and OCR them locally with Tesseract.
5. Normalize and validate OCR output. Empty OCR output is rejected rather than promoted as evidence.
6. Store successful extracted text as an encrypted `review_pending` admission candidate.
7. Preserve the existing human approval/promotion boundary. OCR never auto-promotes knowledge.

No document contents are sent to an external OCR service.

## Resource controls

- `JEBEDIAH_OCR_MAX_PAGES` (default `25`)
- `JEBEDIAH_OCR_DPI` (default `200`)
- `JEBEDIAH_OCR_TIMEOUT_SECONDS` (default `90`)
- `JEBEDIAH_OCR_LANGUAGE` (default `eng`)
- `JEBEDIAH_OCR_MIN_CHARACTERS` (default `8`)

## Explicit failures

- `ocr_runtime_unavailable`
- `ocr_timeout`
- `ocr_processing_failed`
- `ocr_render_failed`
- `ocr_contains_no_extractable_text`
- `pdf_page_limit_exceeded`

These states fail closed and do not create promoted organizational knowledge.

## Acceptance

The live acceptance test is the previously failing image-only `Scanned Image 1.pdf`: it must pass OCR, enter `review_pending`, remain unavailable to grounded QA before approval, become available only after human promotion, and support a grounded answer with provenance afterward.
