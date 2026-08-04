import os
import httpx
from fastapi import HTTPException


MEMORY_URL = os.getenv(
    "MEMORY_URL",
    "http://jebediah-memory:8000"
)


async def retrieve_context(query: str) -> str:
    payload = {
        "source_identity": "interaction-gateway",
        "content": query,
        "memory_type": "context",
        "importance": 0.5
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{MEMORY_URL}/memory/context",
            json=payload,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Map memory service 5xx/503 to a clear 503 at the interaction
            # gateway so callers see the dependency outage rather than an
            # internal server error.
            status = exc.response.status_code if exc.response is not None else 503
            raise HTTPException(status_code=status, detail="memory service unavailable") from exc

        data = response.json()

        # Return structured JSON so callers can consume memory results programmatically
        # instead of relying on raw Python string conversion which is non-deterministic
        # and loses structure. The memory service returns a dict with keys like
        # {"query": ..., "memories": [...]}
        return data
