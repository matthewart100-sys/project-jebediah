# Organizational Intelligence Phase 3B Completion Directive

**Status:** Active implementation directive on branch `docs/phase3b-milestone1-implementation-activation`

**Decision authority:** Chief Architect (chat directive, 2026-08-05)

**Purpose:** Complete the first operational governed organizational-intelligence implementation by replacing synthetic shell providers with governed runtime behavior while preserving the existing Executive Product Shell information architecture.

## Scope

This directive authorizes bounded completion work across the existing shell modules:

- Executive Dashboard
- Knowledge Manager
- Organizational Intelligence
- Organizational Memory
- Governance
- Audit
- Administration

The interface architecture remains in place; implementation replaces synthetic runtime behavior where already supported by repository boundaries.

## Implementation intent

The implementation prioritizes:

1. governed document admission flow integration through the shell;
2. explicit lifecycle and governance state transitions with audit evidence;
3. runtime-backed executive evidence retrieval and explainable responses;
4. runtime-backed evidence, provenance, and audit displays;
5. staged reduction of synthetic provider dependencies;
6. preservation of human authority and no autonomous approval.

## Constraints

- Preserve accepted ADR boundaries.
- Do not bypass governance, lifecycle, or audit boundaries.
- Do not introduce duplicate services or alternate storage architectures.
- Keep routes, navigation, and primary layouts stable.
- Keep decisions explicit and testable.

## Required validation

- Existing relevant test suites remain passing.
- New integration tests cover replaced runtime behavior.
- Documentation validation and whitespace checks remain passing.
- Changes remain reviewable and rollback-safe.

## Notes

- This directive supersedes the branch-local milestone interpretation that limited implementation to synthetic-intake-only behavior.
- Canonical `main` remains authoritative until this branch is reviewed and merged.
