from .models import ConfidenceScore


class ConfidenceEvaluator:
    """
    Evaluates how trustworthy a memory source is.

    This layer does not create memories.
    It only scores confidence.
    """

    def evaluate(
        self,
        source: str,
        repeated: bool = False,
    ) -> ConfidenceScore:

        if repeated:
            return ConfidenceScore(
                value=0.95,
                reason="confirmed multiple times",
            )

        if source == "user":
            return ConfidenceScore(
                value=0.9,
                reason="explicit user statement",
            )

        if source == "system":
            return ConfidenceScore(
                value=0.75,
                reason="system observation",
            )

        return ConfidenceScore(
            value=0.5,
            reason="inferred information",
        )