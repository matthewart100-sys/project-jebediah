#!/usr/bin/env python3
"""Validate Project Jebediah's documentation and repository hygiene."""

from __future__ import annotations

import ipaddress
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".ai/COLLABORATION.md",
    ".editorconfig",
    ".gitattributes",
    ".github/ISSUE_TEMPLATE/architecture.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/docs-quality.yml",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODEX_BOOTSTRAP.md",
    "CONTRIBUTING.md",
    "CURRENT_SPRINT.md",
    "PROJECT_STATUS.md",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "docs/AI_MEMORY_CONTRACT.md",
    "docs/ARCHITECTURE.md",
    "docs/ARCHITECTURE_PRINCIPLES.md",
    "docs/DATA_OWNERSHIP.md",
    "docs/DEFINITION_OF_DONE.md",
    "docs/DOCUMENTATION_STANDARDS.md",
    "docs/ENGINEERING_STANDARDS.md",
    "docs/GIT_WORKFLOW.md",
    "docs/MISSION_AND_MANIFESTO.md",
    "docs/OPERATIONS_PHILOSOPHY.md",
    "docs/README.md",
    "docs/RELEASE_PROCESS.md",
    "docs/REPOSITORY_STANDARDS.md",
    "docs/SPRINT_PROCESS.md",
    "docs/TESTING_PHILOSOPHY.md",
    "docs/adr/0000-template.md",
    "docs/adr/README.md",
    "docs/design/DIGITAL_TWIN_POSITION.md",
    "docs/genesis/GENESIS_FOUNDATION_AUDIT.md",
    "docs/genesis/PROJECT_GENESIS_PLAN.md",
    "docs/reference/COMPONENT_REGISTRY.md",
    "docs/reference/GLOSSARY.md",
    "docs/releases/v0.1.0/CHECKLIST.md",
    "docs/releases/v0.1.0/RELEASE_NOTES.md",
    "docs/reviews/ARCHITECT_REVIEW_TEMPLATE.md",
    "scripts/validate_docs.py",
)

FORBIDDEN_ROOT_DIRECTORIES = {
    "backups",
    "data",
    "logs",
    "runtime",
    "temp",
    "tmp",
}

BOOTSTRAP_NAME_FRAGMENTS = (
    "genesis_vol",
    "codex_plan_mode_bootstrap",
    "codex_initialization_prompt",
    "jebediah_codex_onboarding_pack",
)

ARCHIVE_SUFFIXES = {
    ".7z",
    ".rar",
    ".tar",
    ".tgz",
    ".zip",
}

# Add an exact repository-relative path only after the repository-standard
# exception and its rationale are approved in the same pull request.
APPROVED_ARCHIVE_PATHS: set[str] = set()

TEXT_SCAN_SUFFIXES = {
    ".ini",
    ".json",
    ".md",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

# The validator itself contains these detection expressions and is excluded
# from the sensitive-value scan below to prevent self-matches.
SENSITIVE_VALUE_PATTERNS = (
    (
        "private key",
        re.compile(r"-----BEGIN (?:EC |OPENSSH |PGP |RSA )?PRIVATE KEY-----"),
    ),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("OpenAI-style secret key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "generic assigned secret",
        re.compile(
            r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|token)\b"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9+/_.=-]{16,}"
        ),
    ),
)

IPV4_CANDIDATE = re.compile(
    r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"
)
RFC1918_NETWORKS = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
)

INLINE_LINK = re.compile(r"!?\[[^\]]*]\(([^)\n]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+]:\s*(\S+)", re.MULTILINE)
H1 = re.compile(r"^# (?!#)\S.*$", re.MULTILINE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
TRAILING_WHITESPACE = re.compile(rb"[ \t]+$", re.MULTILINE)


def tracked_files() -> list[Path]:
    """Return tracked repository files using Git as the authority."""
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    return [
        REPOSITORY_ROOT / raw.decode("utf-8")
        for raw in result.stdout.split(b"\0")
        if raw
    ]


def repository_path(path: Path) -> str:
    """Return a stable POSIX-style path relative to the repository."""
    return path.relative_to(REPOSITORY_ROOT).as_posix()


def line_number(content: bytes, offset: int) -> int:
    """Return the one-based line number containing a byte offset."""
    return content.count(b"\n", 0, offset) + 1


def content_outside_fences(text: str) -> tuple[str, list[str]]:
    """Blank fenced content and report malformed or unclosed fences."""
    output: list[str] = []
    errors: list[str] = []
    active_marker: str | None = None
    active_length = 0

    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if active_marker is None:
                active_marker = marker[0]
                active_length = len(marker)
            elif marker[0] == active_marker and len(marker) >= active_length:
                active_marker = None
                active_length = 0
            output.append("\n" if line.endswith("\n") else "")
            continue

        output.append(line if active_marker is None else ("\n" if line.endswith("\n") else ""))

    if active_marker is not None:
        errors.append(
            f"unclosed fenced code block using {active_marker * active_length}"
        )

    return "".join(output), errors


def extract_link_target(raw_target: str) -> str:
    """Remove optional Markdown title syntax from a link target."""
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def validate_local_links(path: Path, text: str, errors: list[str]) -> None:
    """Verify local Markdown link destinations exist."""
    targets = [match.group(1) for match in INLINE_LINK.finditer(text)]
    targets.extend(match.group(1) for match in REFERENCE_LINK.finditer(text))

    for raw_target in targets:
        target = unquote(extract_link_target(raw_target))
        if not target or target.startswith("#"):
            continue

        split = urlsplit(target)
        if split.scheme or split.netloc:
            continue

        local_part = split.path.replace("\\", "/")
        if not local_part:
            continue

        if local_part.startswith("/"):
            destination = REPOSITORY_ROOT / local_part.lstrip("/")
        else:
            destination = path.parent / local_part

        if not destination.resolve().exists():
            errors.append(
                f"{repository_path(path)}: unresolved local link "
                f"{raw_target!r}"
            )


def validate_markdown(path: Path, errors: list[str]) -> None:
    """Validate one Markdown file."""
    raw = path.read_bytes()
    relative = repository_path(path)

    if not raw.strip():
        errors.append(f"{relative}: file is empty")
        return
    if not raw.endswith(b"\n"):
        errors.append(f"{relative}: missing final newline")

    trailing = TRAILING_WHITESPACE.search(raw)
    if trailing:
        errors.append(
            f"{relative}:{line_number(raw, trailing.start())}: trailing whitespace"
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{relative}: not valid UTF-8 ({exc})")
        return

    structural_text, fence_errors = content_outside_fences(text)
    errors.extend(f"{relative}: {message}" for message in fence_errors)

    h1_count = len(H1.findall(structural_text))
    if h1_count != 1:
        errors.append(
            f"{relative}: expected exactly one level-one heading; found {h1_count}"
        )

    validate_local_links(path, structural_text, errors)


def validate_tracked_content(files: list[Path], errors: list[str]) -> None:
    """Reject tracked runtime material, bootstrap artifacts, and archives."""
    for path in files:
        relative = repository_path(path)
        parts = Path(relative).parts
        lowered = relative.lower()

        if parts and parts[0].lower() in FORBIDDEN_ROOT_DIRECTORIES:
            errors.append(
                f"{relative}: runtime, local data, logs, and recovery material "
                "must not be tracked"
            )

        if any(fragment in lowered for fragment in BOOTSTRAP_NAME_FRAGMENTS):
            errors.append(
                f"{relative}: bootstrap material must remain outside the "
                "authoritative repository"
            )

        if (
            path.suffix.lower() in ARCHIVE_SUFFIXES
            and relative not in APPROVED_ARCHIVE_PATHS
        ):
            errors.append(
                f"{relative}: archive files require removal or an approved "
                "repository-standard exception"
            )


def validate_sensitive_values(files: list[Path], errors: list[str]) -> None:
    """Flag common credentials and private IPv4 addresses in tracked text."""
    validator_path = Path(__file__).resolve()

    for path in files:
        if path.resolve() == validator_path or path.suffix.lower() not in TEXT_SCAN_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        relative = repository_path(path)
        for label, pattern in SENSITIVE_VALUE_PATTERNS:
            match = pattern.search(text)
            if match:
                number = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"{relative}:{number}: possible {label}; remove it and "
                    "rotate the value if real"
                )

        for match in IPV4_CANDIDATE.finditer(text):
            try:
                address = ipaddress.ip_address(match.group(0))
            except ValueError:
                continue
            if any(address in network for network in RFC1918_NETWORKS):
                number = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"{relative}:{number}: private IPv4 address must not be "
                    "stored in the public repository"
                )


def main() -> int:
    """Run all repository validation and return a process exit code."""
    errors: list[str] = []

    for required in REQUIRED_FILES:
        if not (REPOSITORY_ROOT / required).is_file():
            errors.append(f"{required}: required canonical file is missing")

    try:
        files = tracked_files()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: unable to enumerate tracked files: {exc}", file=sys.stderr)
        return 2

    validate_tracked_content(files, errors)

    markdown_files = sorted(
        (path for path in files if path.suffix.lower() == ".md"),
        key=repository_path,
    )
    for path in markdown_files:
        validate_markdown(path, errors)

    validate_sensitive_values(files, errors)

    if errors:
        print(
            f"Documentation validation failed with {len(errors)} error(s):",
            file=sys.stderr,
        )
        for error in sorted(errors):
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Documentation validation passed: "
        f"{len(markdown_files)} Markdown files and {len(files)} tracked files checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
