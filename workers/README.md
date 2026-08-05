# Synthetic document workers

These worker artifacts are bounded fixtures for Phase 3B Milestone 1 only.

- `document_scanner` flags only the synthetic `EICAR` marker.
- `pdf_inspector` extracts only `SYNTHETIC-TEXT[n]:...` markers.
- `pdf_ocr` extracts only `SYNTHETIC-OCR[n]:...` markers.

They are not general-purpose scanners, parsers, or OCR engines.
