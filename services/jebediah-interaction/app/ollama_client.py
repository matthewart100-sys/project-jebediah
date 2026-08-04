import os
import httpx
from fastapi import HTTPException


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://100.110.120.15:11434"
)

MODEL_NAME = os.getenv(
    "GENERATION_MODEL",
    "qwen3:8b"
)


async def generate(messages: list[dict]) -> str:
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=300) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            # Map remote generation failures to 503 so callers can treat model
            # unavailability as a dependency outage rather than an internal error.
            status = exc.response.status_code if exc.response is not None else 503
            raise HTTPException(status_code=503, detail="generation model unavailable") from exc

        data = response.json()

        return data["message"]["content"]
