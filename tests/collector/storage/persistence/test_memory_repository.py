from collector.storage.persistence import MemoryRepository
from collector.adapters.text import adapt_text_record


def test_memory_repository_stores_and_retrieves():

    repository = MemoryRepository()

    processed = adapt_text_record(
        source_id="test.txt",
        content="hello jebediah",
        revision="1",
    )

    identity = repository.save(processed)

    assert repository.contains(identity)

    stored = repository.find(identity)

    assert stored == processed