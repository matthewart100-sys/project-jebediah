from ..adapters.text import adapt_text_record
from ..policy.storage_policy import StoragePolicy
from ..policy.decisions import StorageDecision
from ..storage.memory_sink import InMemorySink
from .result import CollectorResult


class CollectorService:

    def __init__(
        self,
        storage=None,
        policy=None,
    ):
        self.storage = storage or InMemorySink()
        self.policy = policy or StoragePolicy()


    def ingest(
        self,
        source_type: str,
        source_id: str,
        content: str,
        revision: str,
        metadata=None,
    ):

        processed = adapt_text_record(
            source_id=source_id,
            content=content,
            revision=revision,
            metadata=metadata,
        )

        existing = self.storage.get(
            processed.identity
        )

        policy_result = self.policy.evaluate(
            incoming=processed.record,
            existing=existing,
        )

        stored = False

        if policy_result.decision in (
            StorageDecision.ACCEPT,
            StorageDecision.UPDATE,
        ):
            self.storage.store(processed)
            stored = True


        return CollectorResult(
    	    record=processed.record,
   	    decision=policy_result,
    	    stored=stored,
        )
