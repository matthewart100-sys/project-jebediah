from collector.memory.intelligence import ConfidenceEvaluator


def test_user_statement_has_high_confidence():

    evaluator = ConfidenceEvaluator()

    result = evaluator.evaluate(
        source="user"
    )

    assert result.value == 0.9
    assert result.reason == "explicit user statement"


def test_repeated_memory_has_higher_confidence():

    evaluator = ConfidenceEvaluator()

    result = evaluator.evaluate(
        source="user",
        repeated=True,
    )

    assert result.value == 0.95
    assert result.reason == "confirmed multiple times"


def test_inferred_memory_has_lower_confidence():

    evaluator = ConfidenceEvaluator()

    result = evaluator.evaluate(
        source="unknown"
    )

    assert result.value == 0.5