from enum import Enum


class StorageDecision(str, Enum):
    """
    Allowed outcomes from Collector storage policy evaluation.
    """

    ACCEPT = "accept"
    UPDATE = "update"
    DUPLICATE = "duplicate"
    REJECT = "reject"
    REVIEW = "review"