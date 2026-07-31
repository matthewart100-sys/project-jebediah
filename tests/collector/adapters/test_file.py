from pathlib import Path

from collector.adapters import adapt_file_record


def test_file_adapter_reads_text_file(tmp_path: Path):

    test_file = tmp_path / "example.md"

    test_file.write_text(
        "  Hello   Jebediah file  ",
        encoding="utf-8",
    )

    result = adapt_file_record(
        source_id="file-001",
        file_path=str(test_file),
        revision="1",
    )

    assert result.record.source_type == "text"
    assert result.record.source_id == "file-001"
    assert result.record.content == "Hello Jebediah file"

    assert result.record.metadata["file_name"] == "example.md"
    assert result.record.metadata["file_extension"] == ".md"

    assert result.provenance.source_type == "text"
    assert result.identity
