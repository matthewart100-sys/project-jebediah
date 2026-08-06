# Repository Standards

## Purpose

These standards define how Project Jebediah organizes and protects its
version-controlled artifacts. The repository must remain understandable,
reviewable, recoverable, and safe for a future contributor who has no access to
prior conversations.

This document owns repository paths, artifact placement, dependency manifests,
generated content, and repository hygiene. It does not own branch naming,
documentation-writing rules, or application architecture:

- Branch and commit policy belongs to [Git Workflow](GIT_WORKFLOW.md).
- Documentation ownership and style belong to
  [Documentation Standards](DOCUMENTATION_STANDARDS.md).
- Engineering behavior belongs to
  [Engineering Standards](ENGINEERING_STANDARDS.md).

## Governing principles

- GitHub `main` is the authoritative project record.
- Every tracked artifact has a clear purpose and owner.
- Text-based, reviewable formats are preferred.
- Empty scaffolding and speculative directory trees are prohibited.
- Generated artifacts are minimized and identifiable.
- Secrets and private operational data never enter version control.
- Dependencies and binary artifacts require explicit justification.
- Removing or relocating canonical content requires migration of references.

## Root ownership

The repository root is reserved for entry points and project-wide governance:

| Path | Responsibility |
| --- | --- |
| `README.md` | Primary project entry point |
| `PROJECT_STATUS.md` | Current verified and clearly labeled reported state |
| `CURRENT_SPRINT.md` | One active sprint |
| `ROADMAP.md` | Strategic sequence and phase gates |
| `CHANGELOG.md` | Notable delivered changes and releases |
| `CONTRIBUTING.md` | Contributor onboarding and contribution lifecycle |
| `SECURITY.md` | Public security policy and reporting route |
| `AGENTS.md` | Tool-agnostic AI entry point |
| `CODEX_BOOTSTRAP.md` | Codex-specific operational instructions |
| `.editorconfig` | Cross-editor text defaults |
| `.gitattributes` | Git text and artifact behavior |
| `.gitignore` | Untracked local and generated artifacts |

Do not add another root-level policy when an existing canonical owner can
contain or link to the information.

## Directory ownership

### `docs/`

Contains durable architecture, engineering, process, reference, and governance
documentation. Its internal ownership and navigation rules are defined by
Documentation Standards.

### `.ai/`

Contains cross-tool AI collaboration material that does not belong in the
tool-agnostic root entry point. It must link to canonical project standards
rather than duplicate them.

### `.github/`

Contains GitHub-specific issue forms, pull-request templates, workflows,
ownership configuration, and repository automation. GitHub workflow files must
use pinned, reviewed dependencies.

### `docker/`

Reserved for reviewed container build and composition artifacts. It is created
only when the project has approved container configuration to track. Secrets,
runtime data, local volumes, and mutable state do not belong here.

### `scripts/`

Reserved for maintained developer and operator utilities. Every script must
have a documented purpose, safe invocation, failure behavior, and supported
environment. One-off personal commands do not become project scripts.

`scripts/validate_docs.py` is the canonical repository-quality entry point. It
uses the Python standard library, returns a nonzero exit status on failure, and
is supported locally and in the pinned GitHub Actions environment.

### `workflows/`

Reserved for version-controlled Project Jebediah automation definitions, such
as approved n8n exports. It is distinct from `.github/workflows/`. The format,
credentials boundary, import process, and source-of-truth behavior must be
approved before this directory is created.

### `schemas/`

Reserved for machine-readable interface and data schemas after their ownership
and versioning policy are approved. A schema must identify its consumer,
compatibility policy, and validation path.

### `tests/`

Reserved for cross-component, integration, end-to-end, fixture, or repository
tests that do not belong beside a future implementation module. Test placement
may be refined when a language and source layout are approved.

### Source directories

`src/collector/` contains the tested Python Collector package.
`services/jebediah-memory/` contains the memory-service runtime candidate.
`services/jebediah-interaction/` contains the canonical interaction gateway
that coordinates governed admission, human promotion, workspace-filtered
memory retrieval, model generation, and its existing chat compatibility routes.
`apps/` is reserved for independently runnable, user-facing applications whose
component, language, entry point, dependency, test, security, operations, and
ownership boundaries are approved. Accepted ADR 0015 assigns
`apps/jebediah_executive/` to the synthetic Executive Product Shell. That path
now holds the implemented synthetic, standard-library-only, loopback local
preview on canonical `main`; the component is not Operational and grants no
live-information, integration, action, or deployment authority.
New source or service trees still require an approved responsibility, language,
build, test, packaging, and ownership boundary; existing trees do not authorize
speculative peers.

## Creation rule

A directory is created only with its first real artifact. Do not add:

- Empty directories
- Placeholder `README.md` files
- `.gitkeep` files whose only purpose is preserving a speculative path
- Empty package manifests
- Configuration copied from a template without a current consumer

Document planned ownership in canonical standards until content is ready.

## Naming

- Directory names use lowercase words separated by hyphens unless an external
  tool requires a different convention.
- Python import-package directories use valid lowercase identifiers with
  underscores where word separation is needed.
- Canonical project Markdown files use descriptive uppercase names with
  underscores where established by the Genesis plan.
- Reference and design filenames identify their subject rather than their
  author or date.
- ADR filenames follow the numbering policy in the
  [ADR Process](adr/README.md).
- Do not use names such as `new`, `final`, `latest`, `copy`, or version suffixes
  as a substitute for version control.
- Tool-required names, including `.github/workflows`, take precedence only
  within that tool's boundary.

## Text and line endings

- UTF-8 is the canonical text encoding.
- Repository text uses LF line endings through `.gitattributes`.
- Files end with one newline.
- Trailing whitespace is prohibited except when a canonical format explicitly
  requires it.
- Contributors must avoid drive-by whole-file line-ending changes.

`.editorconfig` expresses compatible editor defaults. `.gitignore` excludes
local secrets, editor state, logs, caches, temporary files, and root-level
runtime or recovery data; it does not make ignored content safe to expose.

## Binary artifacts

Binary files are accepted only when:

- The repository must distribute or preserve the artifact.
- A reviewable source format is unavailable or insufficient.
- Licensing and provenance are known.
- Size and update frequency are appropriate for Git.
- The pull request explains why external artifact storage is not preferable.

Bootstrap ZIP, PDF, and Word files are historical inputs, not canonical project
documentation. Their durable requirements belong in Markdown.

Large models, vector databases, backups, logs, runtime exports containing
private data, and generated build outputs must not be committed.

## Generated content

Generated artifacts must identify:

- Their source
- The command or workflow that regenerates them
- Whether they are reviewed or machine-consumed
- Why they must be version controlled

Generated output must not be edited by hand. If generated and source artifacts
diverge, the generating source wins after validation.

## Dependency manifests

Do not add a package or dependency manifest until a real tool or implementation
requires it.

Every dependency addition must document:

- Purpose and consumer
- Version or pinning strategy
- License compatibility
- Security and supply-chain considerations
- Upgrade and removal ownership

Lock files are tracked when the selected ecosystem uses them to provide
reproducibility. Do not hand-edit lock files.

## Configuration and secrets

- Commit safe defaults and sanitized examples, not active secrets.
- Secret values are supplied through an approved external mechanism.
- Example environment files use unmistakably fake values.
- Public files must not contain private IP addresses, hostnames, tokens,
  credentials, personal identifiers, or exploitable topology.
- Local overrides and runtime state belong in ignored files or external
  systems.
- A secret discovered in history is treated as compromised and rotated; simply
  deleting the current line is insufficient.

## Schema and workflow changes

Machine-consumed schemas and workflow exports require:

- A canonical tracked source
- Validation
- Compatibility and migration assessment
- Credential sanitization
- Human-readable change explanation
- Rollback or re-import expectations

Direct changes to a live workflow or data contract must be reconciled into the
repository immediately through the approved process.

## Moving and removing content

Before moving or deleting a tracked artifact:

1. Identify all repository references and consumers.
2. Preserve history with a normal Git move when practical.
3. Update links and navigation in the same change.
4. Document replacement or deprecation.
5. Verify no operational process still depends on the old path.

Do not preserve obsolete duplicated files "just in case." Git history is the
archive; current `main` should describe current truth.

## Repository checks

Every repository change evaluates:

- `python scripts/validate_docs.py`
- `git diff --check`
- Markdown and local-link integrity for documentation
- Secret and sensitive-information exposure
- Generated or binary artifact policy
- Dependency-manifest impact
- Canonical status, sprint, roadmap, and changelog impact
- The [Definition of Done](DEFINITION_OF_DONE.md)

The `documentation-quality` GitHub Actions job runs the repository validator
for pull requests and pushes to `main`. It is deliberately dependency-free and
does not replace human semantic, architecture, or sensitive-data review.

## Exceptions

An exception must state the constraint, risk, owner, and planned resolution in
the pull request. Exceptions do not silently redefine repository policy.
