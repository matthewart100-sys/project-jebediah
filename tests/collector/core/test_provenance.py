from collector.core.provenance import CollectorProvenance


def test_provenance_defaults_version():
    provenance = CollectorProvenance(
        source_type="chat",
        source_id="test-001",
    )

    assert provenance.collector_version == "1.0"
    assert provenance.source_type == "chat"