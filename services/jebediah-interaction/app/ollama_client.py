import os
import httpx


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

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]
