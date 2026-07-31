from collector.policy.decisions import StorageDecision


def test_storage_decisions_exist():

    assert StorageDecision.ACCEPT.value == "accept"
    assert StorageDecision.UPDATE.value == "update"
    assert StorageDecision.DUPLICATE.value == "duplicate"
    assert StorageDecision.REJECT.value == "reject"
    assert StorageDecision.REVIEW.value == "review"