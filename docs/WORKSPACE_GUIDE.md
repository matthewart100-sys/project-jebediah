# Bonsaai Workspace Guide

> **Historical pull request #60 audit and salvage artifact — do not execute.**
> This file is non-authoritative and grants no implementation, operations, or
> deployment permission. See the
> [Phase 3B reconciliation decision](governance/CHIEF_ARCHITECT_PHASE_3B_RECONCILIATION_DECISION.md).

## Purpose

Operational workspaces let one Executive Shell run demonstration, development,
and production environments without code changes or redeployment.

## Workspace modes

### Demonstration

- Banner: `Demonstration Mode` (blue)
- Data source: synthetic fixtures only
- Safety: live runtime mutation is blocked
- Control: `Reset Demo` restores pristine synthetic state

### Development

- Banner: `Development Environment` (orange)
- Data source: governed runtime in development-isolated roots
- Diagnostics: enabled

### Production

- Banner: `Production Workspace` (green)
- Data source: governed runtime only
- Synthetic workspace content: disabled

## Organization configuration

Current in-repo profiles:

- `demo-organization` → Demo Organization
- `back-pack-kidz` → Back Pack Kidz
- `virginia-b-andes` → Virginia B. Andes

Each profile includes:

- organization name
- logo text
- theme
- description
- knowledge root label
- runtime root label
- governance policy label

## Selection and persistence

- Workspace and organization selectors are available on the Executive Dashboard.
- Selection persists in runtime state at `JEBEDIAH_RUNTIME_ROOT`.
- Startup defaults are configurable with:
  - `BONSAAI_WORKSPACE_MODE`
  - `BONSAAI_DEFAULT_WORKSPACE`
  - `BONSAAI_ORGANIZATION_ID`

## Separation strategy

- Demonstration uses synthetic-only provider state.
- Development and production use separate runtime directories by
  `organization_id/workspace_mode`.
- Semantic collection names are namespaced by organization and workspace mode.
