# Phase 3B Local Operator Guide

This guide covers the synthetic-only local operator workflow for Phase 3B
Milestone 1.

## Launch

Run the Executive Product Shell locally with:

`python -B -m apps.jebediah_executive --port 8765`

The shell remains loopback-only and synthetic-only.

## Milestone 1 workflow

1. Open the loopback shell.
2. Navigate to the workspace page.
3. Submit one synthetic PDF with a synthetic receipt identifier.
4. Review the sanitized submission detail page.
5. Record an approve, reject, correct, or supersede decision.
6. Run the recovery sweep when validating expiry and missing-object handling.

No server-side source path, remote fetch, or real organizational document is
accepted.
