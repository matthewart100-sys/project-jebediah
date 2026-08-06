"""HTTP adapter for the configured generation model."""

from __future__ import annotations

import os

import httpx
from fastapi import HTTPException


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/")
MODEL_NAME = os.getenv("GENERATION_MODEL", "qwen3:8b")


async def generate(messages: list[dict[str, str]]) -> str:
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": MODEL_NAME, "stream": False, "messages": messages},
            )
            response.raise_for_status()
            decoded = response.json()
            content = decoded["message"]["content"]
    except (httpx.HTTPError, KeyError, TypeError, ValueError) as error:
        raise HTTPException(
            status_code=503,
            detail="generation model unavailable",
        ) from error
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(status_code=503, detail="generation model response invalid")
    return content.strip()
