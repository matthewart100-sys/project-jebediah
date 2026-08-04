from fastapi import FastAPI
from pydantic import BaseModel

from .memory_client import retrieve_context
from .context_builder import build_messages
from .ollama_client import generate


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Jebediah Interaction Gateway",
    version="0.1.0"
)

# Allow the (browser-based) Open WebUI to call this service. In production,
# restrict origins via the ALLOWED_ORIGINS environment variable or a configuration
# management system. Default to all origins for local demo convenience.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# OpenAI-compatible adapter for Open WebUI and similar clients
class OpenAIChatCompletionRequest(BaseModel):
    model: str | None = None
    messages: list[dict] | None = None
    prompt: str | None = None


@app.post("/v1/chat/completions")
async def openai_chat_completions(request: OpenAIChatCompletionRequest):
    """Minimal OpenAI-compatible endpoint that routes through the canonical
    interaction flow: retrieve memory context, assemble messages, and call the
    existing generation adapter. This preserves memory retrieval and evidence
    usage rather than bypassing the memory layer.
    """

    # Determine user message text from OpenAI-style input
    user_text = None
    if request.messages:
        # Prefer the last user-role message; fall back to the last message content
        for msg in reversed(request.messages):
            role = (msg.get("role") or "").lower()
            if role == "user":
                user_text = msg.get("content")
                break
        if user_text is None and len(request.messages) > 0:
            user_text = request.messages[-1].get("content")

    if not user_text and request.prompt:
        user_text = request.prompt

    if not user_text:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="no user message provided")

    # Preserve existing memory retrieval
    context = await retrieve_context(user_text)

    # Reuse existing deterministic context builder
    model_messages = build_messages(user_text, context)

    # Call existing generation adapter
    response_text = await generate(model_messages)

    # Return a minimal OpenAI-compatible response
    import time
    import uuid

    created = int(time.time())
    resp = {
        "id": f"jeb-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": created,
        "model": "jebediah",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text,
                },
                "finish_reason": "stop",
            }
        ],
        # usage is optional; left minimal for demo
        "usage": {},
    }

    return resp


@app.get("/v1/models")
def openai_models():
    """Return a minimal OpenAI-compatible models list containing the
    single public model 'jebediah' so Open WebUI can discover it automatically.
    """
    import time

    now = int(time.time())
    return {
        "object": "list",
        "data": [
            {
                "id": "jebediah",
                "object": "model",
                "created": now,
                "owned_by": "project-jebediah",
                "permissions": [],
            }
        ],
    }
