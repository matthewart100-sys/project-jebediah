from fastapi import FastAPI
from pydantic import BaseModel

from .memory_client import retrieve_context
from .context_builder import build_messages
from .ollama_client import generate


app = FastAPI(
    title="Jebediah Interaction Gateway",
    version="0.1.0"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "jebediah-interaction"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    context = await retrieve_context(
        request.message
    )

    messages = build_messages(
        request.message,
        context
    )

    response = await generate(
        messages
    )

    return {
        "response": response,
        "context_used": context
    }
