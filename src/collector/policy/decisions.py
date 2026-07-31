from dataclasses import dataclass
from enum import Enum


class StorageAction(str, Enum):
    ACCEPT = "accept"
    UPDATE = "update"
    DUPLICATE = "duplicate"
    REVIEW = "review"
    REJECT = "reject"


@dataclass(frozen=True)
class StorageDecision:
    """
    Concrete storage decision.

    Contains:
    - action
    - reason
    """

    action: str
    reason: str = ""

    @property
    def value(self):
        return self.action


StorageDecision.ACCEPT = StorageDecision(
    action=StorageAction.ACCEPT.value,
    reason="accept record",
)

StorageDecision.UPDATE = StorageDecision(
    action=StorageAction.UPDATE.value,
    reason="update record",
)

StorageDecision.DUPLICATE = StorageDecision(
    action=StorageAction.DUPLICATE.value,
    reason="duplicate record",
)

StorageDecision.REVIEW = StorageDecision(
    action=StorageAction.REVIEW.value,
    reason="review record",
)

StorageDecision.REJECT = StorageDecision(
    action=StorageAction.REJECT.value,
    reason="reject record",
)