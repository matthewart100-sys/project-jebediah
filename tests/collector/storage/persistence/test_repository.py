from collector.storage.persistence import RecordRepository


def test_repository_contract_exists():

    assert RecordRepository is not None