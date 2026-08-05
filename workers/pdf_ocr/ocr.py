from __future__ import annotations

import json
import re
import sys


OCR_PATTERN = re.compile(rb"SYNTHETIC-OCR\[(\d+)\]:(.+)")


def main() -> int:
    payload = sys.stdin.buffer.read()
    pages = [
        {
            "page_number": int(match.group(1)),
            "method": "ocr",
            "text": match.group(2).decode("utf-8").strip(),
        }
        for match in OCR_PATTERN.finditer(payload)
    ]
    if not pages:
        pages = [{"page_number": 1, "method": "ocr", "text": "synthetic ocr unavailable"}]
    json.dump(
        {
            "status": "reviewable",
            "pages": pages,
            "warnings": ["ocr_fallback_used"],
            "findings": [],
            "native_text_sufficient": False,
        },
        sys.stdout,
        sort_keys=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
