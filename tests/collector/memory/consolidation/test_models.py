from collector.memory.consolidation.models import (
    ConsolidationAction,
    ConsolidationDecision,
)


def test_consolidation_decision_contract():

    decision = ConsolidationDecision(
        action=ConsolidationAction.PROMOTE,
        score=0.9,
        confidence=0.95,
        duplicate=False,
        reason="high value memory",
    )

    assert decision.action == ConsolidationAction.PROMOTE
    assert decision.score == 0.9
    assert decision.confidence == 0.95