# Safe VBA Evidence Preparation Guide

**Status:** Proposed documentation-only operator guidance

**Decision owner:** Chief Architect

**Operational custody owner:** Unresolved; must be assigned before use

**Applies to:** Local preparation for a future, separately authorized Knowledge
Manager document-inspection phase

**Does not authorize:** Inspection, hashing, extraction, submission, ingestion,
registration, retrieval, or use of real VBA material

## Purpose

This guide defines a safe, local-only preparation pattern for future
organizational evidence. It provides blank inventory structures and review
checklists without establishing a live intake path.

This guide does not change source authority. An originating VBA source remains
authoritative for its records. A locally staged artifact would be only a
candidate evidentiary snapshot. Jebediah, the future Knowledge Vault, the
Knowledge Registry, storage systems, parsers, and AI output do not become
authoritative merely by receiving or describing it.

**VBA documents remain outside Jebediah until Knowledge Manager Phase 2 document inspection is separately reviewed and authorized.**

## Preconditions

Do not use this guide with real documents until all of the following are true:

- this preparation package is accepted and merged;
- the Chief Architect has explicitly authorized local preparation for the named
  information domain without authorizing inspection or ingestion;
- an organizational information owner has approved the local preparation
  activity and location;
- an operational custodian is named;
- sensitivity, privacy, legal, consent, retention, and deletion rules are
  documented;
- the originating source authority and intended use are known;
- access is limited to approved operators;
- the local location is outside this public repository, every issue and pull
  request, chat attachments, and model prompts, without exception;
- the approved access-controlled root is not in a consumer synchronization
  folder; and
- the operator has a private escalation route for sensitive uncertainty.

If any precondition is unresolved, stop. Record only the unresolved control,
not document content or sensitive values, through an approved private process.

## Recommended local staging structure

An authorized custodian may create this structure under an approved,
access-controlled local root. The placeholder is not a literal path:

```text
<approved-local-staging-root>\
|-- 10_candidates_not_submitted\
|-- 20_inventory\
|-- 30_local_review_hold\
|-- 40_local_excluded\
`-- 90_operator_notes\
```

These folder names describe local preparation only:

- `10_candidates_not_submitted` contains potential future candidates that have
  not been submitted to or evaluated by Jebediah.
- `20_inventory` contains the private working inventory and provenance
  worksheet.
- `30_local_review_hold` separates candidates whose authority, sensitivity,
  version, ownership, or permitted use is unresolved.
- `40_local_excluded` identifies material that the information owner has
  excluded from the proposed activity. It is not the system admission state
  `rejected`.
- `90_operator_notes` contains sanitized operational notes only. It must not
  become a substitute for authoritative source or provenance records.

None of these folders is an accepted, ingested, registered, or retrievable
Jebediah location. Do not create any folder named `accepted` or use a local
folder move to imply an admission decision.

## Filename and identifier conventions

Preserve each supplied document filename as evidence. Do not rename the source
artifact merely to fit a Jebediah convention. Assign a separate local candidate
identifier in the inventory:

```text
KM1-<local-batch-id>-<four-digit-sequence>
```

Use a non-sensitive local batch identifier. Do not encode a person's name,
case number, medical identifier, credential, source-system secret, or document
content in the identifier or path.

Recommended private worksheet names are:

```text
KM1_<local-batch-id>_document_inventory.<approved-format>
KM1_<local-batch-id>_provenance_intake.<approved-format>
```

The organization must select and approve the worksheet format and storage
location. These names do not create an upload, API, or parser contract.

## Blank document-inventory template

Create one row per candidate in an approved private worksheet. Keep the
repository copy blank.

| Field | Blank value |
| --- | --- |
| Local candidate ID | |
| Supplied filename | |
| Supplied extension | |
| Originating source authority label | |
| Source record or document reference | |
| Source revision or version label | |
| Source observation time and timezone | |
| Intended information domain | |
| Intended use | |
| Sensitivity review status | |
| Duplicate or version review status | |
| Local preparation status | |
| Assigned custodian role | |
| Sanitized limitation note | |

Do not add extracted text, document summaries, file bytes, hashes, credentials,
personal identifiers, or private source locations to this template during the
preparation-only phase.

## Blank provenance-intake worksheet

Complete this worksheet only after the information owner approves its private
handling. Use organizational roles rather than personal details where the
governance record permits.

| Field | Blank value |
| --- | --- |
| Local candidate ID | |
| Originating source authority | |
| Source owner role | |
| Authorized submitter role | |
| Collection or creation context | |
| Source reference | |
| Source revision or observed-at time | |
| Intended information domain | |
| Intended consumers | |
| Permitted uses | |
| Prohibited uses | |
| Sensitivity classification | |
| Privacy, legal, or consent policy reference | |
| Retention and deletion policy reference | |
| Required human-review role | |
| Known provenance limitations | |
| Known version limitations | |
| Private escalation reference | |

Blank fields are unresolved; they are not permission to infer, default, or
accept the missing value.

## Sensitivity and prohibited-data checklist

Before a candidate is copied into any approved staging location, the
information owner or delegated reviewer must determine whether it may contain:

- credentials, tokens, keys, secrets, or authentication material;
- personal identifiers or contact details;
- health, medical, safeguarding, or similarly sensitive personal information;
- payroll, financial, legal-privilege, disciplinary, or human-resources
  information;
- private addresses, infrastructure details, exploitable topology, or
  vulnerability information;
- restricted third-party, customer, supplier, or licensed material;
- data subject to deletion, litigation-hold, consent, contractual, or
  jurisdictional constraints;
- active content, macros, executable payloads, or links to externally fetched
  content; or
- information whose originating authority, ownership, or intended use is
  unclear.

An affirmative or uncertain result does not authorize copying, inspection, or
submission. Place only the local candidate identifier in the approved private
review process and wait for the authorized owner. Do not record the sensitive
value in this repository, an issue, a pull request, chat, or model prompt.

## Duplicate and version-review checklist

Preparation may compare only supplied metadata. It must not inspect content or
calculate a real-file hash.

- Confirm that each candidate has one local candidate identifier.
- Preserve the supplied filename, source reference, revision label, and
  observation time separately.
- Flag matching filenames as possible duplicates, not proven duplicates.
- Flag conflicting revision labels or observation times for owner review.
- Do not choose a "latest" or "authoritative" copy without the originating
  source authority's rule.
- Do not delete or overwrite a candidate because another file appears similar.
- Record an ambiguous relationship as local review hold.
- Defer byte-level digesting and duplicate determination to a separately
  authorized inspection design.

## Local preparation workflow

1. Confirm every precondition in this guide.
2. Create an empty approved local structure outside the repository.
3. Create blank private inventory and provenance worksheets.
4. Assign non-sensitive local candidate identifiers.
5. Perform the metadata-only sensitivity and version checks.
6. Under the explicit local-preparation authorization, place unresolved
   candidates in the approved organizational-custody review-hold location
   without inspecting their content.
7. Stop before hashing, file-type sniffing, malware scanning, parsing,
   extraction, submission, or connection to Jebediah.

The operator must not describe a locally prepared candidate as accepted,
rejected, validated, safe, registered, ingested, or learned.

## Phase 2 readiness checklist

Real document inspection remains blocked until repository evidence confirms:

- the Phase 1 Knowledge Registry implementation and closeout are merged;
- the Phase 2 architecture package is accepted at an exact reviewed head;
- the Chief Architect has authorized a bounded Phase 2 implementation;
- the first information domain, source authority, producer, submitter,
  consumer, and intended-use contracts are approved;
- privacy, legal, consent, retention, deletion, and audit rules are approved;
- component and operational ownership are assigned;
- quarantine, malware, macro, file-type, parser-isolation, resource-limit, and
  recovery controls are accepted and validated with synthetic fixtures;
- storage and evidence-retention decisions have completed their required ADR
  and review gates; and
- a separate Chief Architect decision explicitly authorizes any real VBA
  inspection after synthetic validation.

An implementation-ready pipeline does not itself authorize real documents.

## Boundaries and rollback

This guide creates no application state and requires no repository rollback
beyond reverting this documentation proposal. Any future cleanup of approved
private local staging is owned by the assigned custodian and must follow the
applicable retention, deletion, legal-hold, and evidence-preservation policy.
This guide does not authorize an agent to delete or alter local organizational
material.

## Related authority

- [ADR 0011](adr/0011-knowledge-vault-authority-and-boundary-model.md) defines
  the source and derived authority boundary.
- [ADR 0013](adr/0013-governed-organizational-document-admission-boundary.md)
  defines the accepted quarantine-first admission boundary.
- [Organizational Document Ingestion Specification](ORGANIZATIONAL_DOCUMENT_INGESTION_SPECIFICATION.md)
  defines the future admission states and fail-closed behavior.
- [Data Ownership](DATA_OWNERSHIP.md) defines ownership and authority
  constraints.
- [Security Policy](../SECURITY.md) defines repository security reporting and
  prohibited public evidence.
