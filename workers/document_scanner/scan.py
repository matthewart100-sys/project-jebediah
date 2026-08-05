from __future__ import annotations

import json
import sys


def main() -> int:
    payload = sys.stdin.buffer.read()
    warnings: list[str] = []
    findings: list[str] = []
    if b"EICAR" in payload:
        warnings.append("scanner_positive")
        findings.append("scanner_positive")
    json.dump(
        {
            "status": "reviewable" if findings else "clean",
            "pages": [],
            "warnings": warnings,
            "findings": findings,
            "native_text_sufficient": False,
        },
        sys.stdout,
        sort_keys=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
