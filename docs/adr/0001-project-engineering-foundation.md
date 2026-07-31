# ADR 0001: Project Engineering Foundation

## Status

Accepted

## Date

2026-07-31

## Context

Project Jebediah is transitioning from infrastructure experimentation into a
maintainable software platform.

Future subsystems require consistent engineering practices.

Without a shared standard, components may develop incompatible patterns,
security weaknesses, and unnecessary technical debt.

## Decision

Adopt Project Jebediah Engineering Standard v1.0 as the baseline engineering
policy.

The standard governs:

- repository practices
- code quality
- testing expectations
- security boundaries
- documentation requirements
- AI-assisted development review

## Consequences

Positive:

- consistent development practices
- easier maintenance
- safer future expansion
- clearer review process

Negative:

- additional upfront documentation
- slower initial implementation

## Alternatives Considered

### No formal standard

Rejected because the platform is expected to grow across multiple subsystems.

### Define standards per subsystem

Rejected because common engineering rules should not be repeatedly recreated.

## Review

This ADR does not define application architecture.
It defines the engineering process used to build application architecture.
