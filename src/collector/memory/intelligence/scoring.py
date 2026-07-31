from .models import MemoryScore, RetentionLevel


class MemoryScorer:
    """
    Calculates memory importance and retention priority.

    This layer does not store memories.
    It only evaluates significance.
    """

    def score(
        self,
        importance: float,
    ) -> MemoryScore:

        if importance >= 0.8:
            retention = RetentionLevel.HIGH

        elif importance >= 0.5:
            retention = RetentionLevel.MEDIUM

        else:
            retention = RetentionLevel.LOW

        return MemoryScore(
            importance=importance,
            retention=retention,
        )