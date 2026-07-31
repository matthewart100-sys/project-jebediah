from collector.storage.adapters import RepositoryAdapter
from collector.storage.persistence import MemoryRepository
from collector.adapters.text import adapt_text_record


def test_repository_adapter_stores_and_retrieves():

    repository = MemoryRepository()

    adapter = RepositoryAdapter(
        repository=repository
    )

    processed = adapt_text_record(
        source_id="adapter-test.txt",
        content="Hello adapter",
        revision="1",
    )

    identity = adapter.store(processed)

    assert identity == processed.identity

    retrieved = adapter.get(identity)

    assert retrieved is not None
    assert retrieved.record.content == "Hello adapter"


def test_repository_adapter_checks_existence():

    repository = MemoryRepository()

    adapter = RepositoryAdapter(
        repository=repository
    )

    processed = adapt_text_record(
        source_id="exists.txt",
        content="exists",
        revision="1",
    )

    assert adapter.exists(processed.identity) is False

    adapter.store(processed)

    assert adapter.exists(processed.identity) is True