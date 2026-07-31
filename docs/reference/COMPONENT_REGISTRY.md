# Component Registry

**Status:** Active

## Purpose

This registry is the canonical inventory of named Project Jebediah components
and preserved environment elements. It records identity, maturity,
responsibility, and component ownership without pretending that planned or
reported items are implemented.

Repository-path ownership belongs to
[Repository Standards](../REPOSITORY_STANDARDS.md). Component ownership is
accountability for purpose, interfaces, state, lifecycle, operations,
recovery, and deprecation. The two ownership models are deliberately separate.

## Maturity states

| State | Meaning |
| --- | --- |
| Active foundation | A reviewed governance or documentation capability exists in `main` |
| Reported | Bootstrap material claims the element exists, but repository evidence has not verified it |
| Named | Design intent preserves a name, but no approved responsibility contract exists |
| Specified | Responsibilities and boundaries are approved, but implementation is not claimed |
| Implemented | Repository evidence shows an implementation exists |
| Operational | Approved evidence shows the implementation is deployed and supportable |
| Deprecated | A replacement or removal path is active |
| Retired | The element is no longer current and remains only in history |

A component advances only through reviewed evidence. Planned roadmap placement
does not advance maturity.

## Ownership states

- **Maintainer accountable:** the maintainer owns the current governance or
  verified component.
- **Unassigned pending specification:** no implementation owner is assigned
  because the component's contract is not approved.
- **Reported operator unknown:** bootstrap material reports a product or asset,
  but operational ownership has not been verified.

An unassigned component must not acquire implicit ownership through whichever
person or agent implements first.

## Registry

| Component or element | Class | Maturity | Current approved responsibility | Component owner | Next gate |
| --- | --- | --- | --- | --- | --- |
| Project Genesis foundation | Governance capability | Active foundation | Preserve project identity, standards, architecture governance, planning, and durable engineering memory | Maintainer accountable | Phase 0 exit audit |
| GitHub repository | Engineering-memory boundary | Active foundation | Own reviewed project documentation, decisions, history, and future safe source artifacts | Maintainer accountable | GitHub enforcement and recovery policy |
| Dell PowerEdge R420 | Reported infrastructure asset | Reported | No responsibility is approved; bootstrap material reports it as the physical host | Reported operator unknown | Sanitized infrastructure audit |
| Proxmox | Reported infrastructure platform | Reported | No responsibility is approved; bootstrap material reports virtualization use | Reported operator unknown | Sanitized infrastructure audit |
| Ubuntu virtual machine | Reported compute guest | Reported | No responsibility is approved; bootstrap material reports a guest environment | Reported operator unknown | Sanitized infrastructure audit |
| Docker | Reported runtime product | Reported | No responsibility is approved; bootstrap material reports container use | Reported operator unknown | Sanitized infrastructure audit and deployment decision |
| n8n | Reported automation product | Reported | No Project Jebediah responsibility is approved | Reported operator unknown | Automation architecture decision |
| Qdrant | Reported data product | Reported | No Project Jebediah responsibility or data authority is approved | Reported operator unknown | Knowledge architecture and data ownership decision |
| Ollama | Reported model product | Reported | No Project Jebediah responsibility or model-serving guarantee is approved | Reported operator unknown | Reasoning architecture decision |
| JCS | Named future subsystem | Named | Definition and specification must precede implementation and collector dependency | Unassigned pending specification | Phase 1 JCS specification |
| Collector Engine | Named future subsystem | Named | Future controlled ingestion from approved sources | Unassigned pending specification | JCS and data ownership approval |
| Knowledge Graph | Named future subsystem | Named | Future representation of traceable entities and relationships | Unassigned pending specification | Stable collector and knowledge contracts |
| Digital Twin | Named future concept | Named | Future bounded, time-aware, provenance-rich representation of selected relevant state; conceptual position only | Unassigned pending specification | Bounded use case and component specification under the Digital Twin position |
| Automation | Named future capability | Named | Future controlled actions from trusted state and policy | Unassigned pending specification | State, authority, and action-boundary approval |
| Reasoning Engine | Named future subsystem | Named | Future bounded reasoning over trusted knowledge and state | Unassigned pending specification | Knowledge and action boundaries plus evaluation requirements |

## Required information for a specified component

Before a component becomes **Specified**, its canonical documentation must
identify:

- Stable name and purpose
- Scope and explicit non-goals
- Component owner and operational owner
- Consumers and dependencies
- Inputs, outputs, side effects, and interfaces
- Authoritative, cached, derived, and temporary information under
  [Data Ownership](../DATA_OWNERSHIP.md)
- Trust boundaries and required privileges
- Failure, timeout, retry, partial-success, and stale-state behavior
- Configuration and secret boundaries
- Health, logging, metrics, and alert ownership
- Backup, restore, migration, rollback, and deprecation expectations
- Test and acceptance evidence
- Relevant ADRs

The fields may link to a component specification rather than duplicating it in
this registry.

## Registry update rules

- Add an element when architecture or an accepted ADR gives it a stable
  identity.
- Update maturity only with repository or validated operational evidence.
- Update component ownership in the same change that assigns or transfers
  responsibility.
- Update current architecture when a component relationship changes.
- Do not expose private hostnames, addresses, credentials, or exploitable
  topology.
- Remove retired rows only when no current reader needs them; Git history
  preserves the prior registry.

## Current limitations

No Project Jebediah application component is specified, implemented, or
verified operational. The reported environment requires an audit. The Digital
Twin has an approved conceptual position but no bounded specification; all
named future subsystems still require their roadmap-phase specifications.
