"""HTTP adapter for the configured generation model."""

from __future__ import annotations

import os

import httpx
from fastapi import HTTPException


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/")
MODEL_NAME = os.getenv("GENERATION_MODEL", "qwen3:8b")
GENERATION_TIMEOUT_SECONDS = float(
    os.getenv("GENERATION_TIMEOUT_SECONDS", "75")
)
GENERATION_KEEP_ALIVE = os.getenv("GENERATION_KEEP_ALIVE", "30m").strip() or "30m"


async def generate(
    messages: list[dict[str, str]],
    *,
    max_output_tokens: int | None = None,
) -> str:
    payload: dict[str, object] = {
        "model": MODEL_NAME,
        "stream": False,
        "think": False,
        "keep_alive": GENERATION_KEEP_ALIVE,
        "messages": messages,
    }
    if max_output_tokens is not None:
        payload["options"] = {"num_predict": max_output_tokens}
    try:
        async with httpx.AsyncClient(timeout=GENERATION_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json=payload,
            )
            response.raise_for_status()
            decoded = response.json()
            content = decoded["message"]["content"]
    except httpx.TimeoutException as error:
        raise HTTPException(
            status_code=503,
            detail="generation model timed out",
        ) from error
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=503,
            detail="generation model unavailable",
        ) from error
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(status_code=503, detail="generation model response invalid")
    return content.strip()
