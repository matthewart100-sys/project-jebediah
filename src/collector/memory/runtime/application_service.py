from dataclasses import dataclass, replace
from typing import Mapping

from collector.embeddings import EmbeddingProvider

from ..models import MemoryItem
from ..persistence import (
    MemoryIndexWriteResult,
    SemanticMemoryRepository,
)
from ..pipeline import MemoryPipeline, MemoryPipelineResult
from ..retrieval import (
    RetrievalCandidate,
    RetrievalRanker,
    SemanticRetrievalRanker,
)


@dataclass(frozen=True)
class MemoryApplicationResult:
    pipeline: MemoryPipelineResult
    write: MemoryIndexWriteResult | None = None


class MemoryApplicationService:
    """Canonical orchestration for evaluation, embedding, and persistence."""

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        repository: SemanticMemoryRepository,
        pipeline: MemoryPipeline | None = None,
        retrieval_ranker: RetrievalRanker | None = None,
    ):
        self.embedding_provider = embedding_provider
        self.repository = repository
        self.pipeline = pipeline or MemoryPipeline()
        self.retrieval_ranker = retrieval_ranker or SemanticRetrievalRanker()

    def ensure_ready(self) -> None:
        self.embedding_provider.ensure_ready()
        verify = getattr(self.repository, "verify_vector_space", None)
        if verify is not None:
            verify()

    def store(self, memory: MemoryItem) -> MemoryApplicationResult:
        pipeline_result = self.pipeline.process(memory, persist=False)
        if not pipeline_result.accepted:
            return MemoryApplicationResult(pipeline=pipeline_result)

        vector = self.embedding_provider.embed(pipeline_result.memory.content)
        write = self.repository.index(
            pipeline_result.memory,
            vector,
            self.embedding_provider.identity,
        )
        return MemoryApplicationResult(
            pipeline=replace(pipeline_result, stored=True),
            write=write,
        )

    def context(
        self,
        content: str,
        limit: int = 5,
        metadata_filter: Mapping[str, str] | None = None,
    ) -> list[RetrievalCandidate]:
        vector = self.embedding_provider.embed(content)
        if metadata_filter is None:
            candidates = self.repository.search(
                vector,
                self.embedding_provider.identity,
                limit,
            )
        else:
            candidates = self.repository.search(
                vector,
                self.embedding_provider.identity,
                limit,
                metadata_filter=metadata_filter,
            )
        return self.retrieval_ranker.rank(candidates)
