from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    print(f"\n>>> {command}")

    result = subprocess.run(
        command,
        cwd=ROOT,
        shell=True,
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"\nFAILED: {command}")
        sys.exit(result.returncode)


def write_file(path, content):
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        content.strip() + "\n",
        encoding="utf-8",
    )

    print(f"Created {path}")


def main():

    print("=== Project Jebediah Loop 3 Pipeline Runner ===")

    # Safety checks
    run("git branch --show-current")

    branch = subprocess.check_output(
        "git branch --show-current",
        cwd=ROOT,
        shell=True,
        text=True,
    ).strip()

    if branch != "architect/collector-core":
        print(
            f"Wrong branch: {branch}\n"
            "Expected: architect/collector-core"
        )
        sys.exit(1)

    # Create pipeline files

    write_file(
        "src/collector/core/pipeline.py",
        r'''
from pydantic import BaseModel

from ..identity import generate_revision_id
from ..models import CollectorRecord
from .normalization import (
    normalize_content,
    normalize_metadata,
)
from .provenance import CollectorProvenance
from .validation import validate_record


class ProcessedCollectorRecord(BaseModel):
    record: CollectorRecord
    provenance: CollectorProvenance
    identity: str


def process_record(
    source_type: str,
    source_id: str,
    content: str,
    revision: str,
    metadata: dict | None = None,
) -> ProcessedCollectorRecord:

    metadata = metadata or {}

    normalized_content = normalize_content(content)
    normalized_metadata = normalize_metadata(metadata)

    validate_record(
        source_type,
        source_id,
        normalized_content,
    )

    record = CollectorRecord(
        source_type=source_type,
        source_id=source_id,
        content=normalized_content,
        revision=revision,
        metadata=normalized_metadata,
    )

    provenance = CollectorProvenance(
        source_type=source_type,
        source_id=source_id,
    )

    identity = generate_revision_id(record)

    return ProcessedCollectorRecord(
        record=record,
        provenance=provenance,
        identity=identity,
    )
'''
    )


    write_file(
        "tests/collector/core/test_pipeline.py",
        r'''
from collector.core.pipeline import process_record


def test_pipeline_processes_record():

    result = process_record(
        source_type="chat",
        source_id="test-001",
        content="  Hello   Jebediah ",
        revision="1",
        metadata={
            "b": "2",
            "a": "1",
        },
    )

    assert result.record.content == "Hello Jebediah"
    assert result.record.metadata == {
        "a": "1",
        "b": "2",
    }

    assert result.provenance.source_id == "test-001"
    assert len(result.identity) == 64
'''
    )


    print("\n=== Running validation ===")

    run("uv run pytest")
    run("python scripts/validate_docs.py")
    run("git diff --check")

    print("\n=== Staging changes ===")

    run(
        "git add "
        "src/collector/core/pipeline.py "
        "tests/collector/core/test_pipeline.py"
    )

    print("\n=== Final status ===")

    run("git status --short")
    run("git diff --cached --stat")

    print(
        "\nLoop 3 pipeline files created and validated."
        "\nReview before committing."
    )


if __name__ == "__main__":
    main()