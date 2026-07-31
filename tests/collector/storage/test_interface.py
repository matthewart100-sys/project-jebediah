from collector.storage import StorageSink


def test_storage_sink_is_abstract():

    assert StorageSink.__abstractmethods__ == {
        "store",
        "get",
        "exists",
    }