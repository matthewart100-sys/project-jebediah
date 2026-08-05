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
| Project Genesis foundation | Governance capability | Released foundation | Preserve project identity, standards, architecture governance, planning, and durable engineering memory | Maintainer accountable | Ongoing maintenance and Phase 1 evidence separation |
| GitHub repository | Engineering-memory boundary | Active engineering memory | Own reviewed project documentation, decisions, history, and safe source artifacts | Maintainer accountable | Ongoing maintenance and proposal review |
| Dell PowerEdge R420 | Reported infrastructure asset | Reported | No responsibility is approved; bootstrap material reports it as the physical host | Reported operator unknown | Sanitized infrastructure audit |
| Proxmox | Reported infrastructure platform | Reported | No responsibility is approved; bootstrap material reports virtualization use | Reported operator unknown | Sanitized infrastructure audit |
| Ubuntu virtual machine | Reported compute guest | Reported | No responsibility is approved; bootstrap material reports a guest environment | Reported operator unknown | Sanitized infrastructure audit |
| Docker | Reported runtime product | Reported | No responsibility is approved; bootstrap material reports container use | Reported operator unknown | Sanitized infrastructure audit and deployment decision |
| n8n | Reported automation product | Reported | No Project Jebediah responsibility is approved | Reported operator unknown | Automation architecture decision |
| Qdrant | Data-product adapter candidate | Implemented | Temporarily own acknowledged Memory Service payload records and their derived semantic vectors; no source-truth authority | Maintainer accountable for repository candidate; reported operator unverified | Sanitized collection, recovery, and deployment review |
| Ollama | Model-product adapter candidate | Implemented | Produce 768-value embeddings with the pinned `nomic-embed-text:v1.5` artifact behind the canonical adapter | Maintainer accountable for repository candidate; reported operator unverified | Pinned-artifact and deployment verification |
| JCS | Named deferred subsystem | Named | C1 outcome is **DEFER JCS**; Collector and memory candidates have no dependency | Unassigned pending reconsideration | Evidence-gated C1 reconsideration |
| Collector Engine | Controlled ingestion component | Implemented | Validate and normalize bounded text records, derive identity, preserve provenance, and coordinate storage; ADR 0013 and the accepted Phase 2 activation bound a disconnected synthetic document-admission repository package with no runtime or real-information authority; PR #53 merged that package as repository implementation | Maintainer accountable | Separate future decisions for deployment, live input, durable quarantine, parser/scanner selection, and runtime ownership |
| Jebediah Memory Service | Semantic memory component | Implemented | Govern memory candidates through one canonical package, persist one acknowledged Qdrant point, and retrieve semantic-only context | Maintainer accountable | Isolated integration and deployment decision |
| Knowledge Vault | Governed knowledge repository boundary | Named | ADR 0011 defines derived-repository authority; the bounded ADR 0014 metadata-only registry library is implemented without content, memory integration, durable storage, runtime use, or source authority | Unassigned pending component specification | Separately approve information domains, component and operational ownership, real producers and consumers, durable interfaces, security, operations, and recovery |
| Executive Product Shell | Human-experience component | Implemented | Present and navigate one immutable evidence-bearing executive briefing over compiled fabricated fixtures in a loopback-only local preview; no source, verification, derivation, approval, action, live-information, or deployment authority | Maintainer accountable | Independent implementation review and Chief Architect merge decision before the synthetic shell becomes canonical on `main` |
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

Collector and memory components and the metadata-only Knowledge Registry
library exist in the repository; none is verified operational. The reported
environment still requires an audit. The Knowledge Vault authority boundary is
accepted under ADR 0011, but the component remains **Named** and has no
component implementation, external information authorization, or operational
evidence. Accepted ADR 0013 defines a future quarantine-first Collector
admission boundary, and Accepted ADR 0012 defines a future executive read-model
consumer boundary. The Phase 2 planning, activation, disconnected synthetic
implementation, validation, and terminal closeout are canonical; they grant no
real-information, runtime, or deployment authority. The Executive Product Shell
is **Implemented** under Accepted ADR 0015 as a synthetic, standard-library-only,
loopback local preview on its working branch; it has no live information,
service, deployment, or operational evidence, and its implementation review and
merge remain gated.
VBA demonstration artifacts exist only on an unmerged proposal branch; their
evidence validation is pending, and no live organizational pilot is authorized.
The Digital Twin has an approved conceptual position but no bounded
specification, and the remaining named future subsystems require their
roadmap-phase specifications.
