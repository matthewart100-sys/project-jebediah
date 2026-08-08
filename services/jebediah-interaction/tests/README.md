# OCR test gates

Automated unit coverage verifies native-text preference and explicit OCR runtime failure states. Production acceptance additionally requires a Docker build and a live image-only PDF because Tesseract/Poppler execution is an operating-system integration boundary.

Required live checks:

- `tesseract --version` and `pdftoppm -v` succeed inside `jebediah-interaction`.
- `/health` returns 200 after rebuild.
- searchable PDFs continue to use native extraction.
- image-only `Scanned Image 1.pdf` reaches `review_pending` rather than `pdf_contains_no_extractable_text`.
- candidate content is not queryable before human approval.
- approval promotes the candidate and the same question returns a grounded answer with provenance.
