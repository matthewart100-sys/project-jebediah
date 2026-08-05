from __future__ import annotations

import json
import re
import sys


TEXT_PATTERN = re.compile(rb"SYNTHETIC-TEXT\[(\d+)\]:(.+)")


def main() -> int:
    payload = sys.stdin.buffer.read()
    findings: list[str] = []
    warnings: list[str] = []
    if b"SYNTHETIC-ENCRYPTED" in payload:
        findings.append("encrypted_pdf")
    if b"SYNTHETIC-JAVASCRIPT" in payload or b"/JavaScript" in payload:
        findings.append("active_content")
    pages = [
        {
            "page_number": int(match.group(1)),
            "method": "native",
            "text": match.group(2).decode("utf-8").strip(),
        }
        for match in TEXT_PATTERN.finditer(payload)
    ]
    if not pages:
        warnings.append("native_text_missing")
    json.dump(
        {
            "status": "reviewable",
            "pages": pages,
            "warnings": warnings,
            "findings": findings,
            "native_text_sufficient": bool(pages),
        },
        sys.stdout,
        sort_keys=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
