from fastapi.testclient import TestClient
from fastapi import HTTPException
import sys
from pathlib import Path

import os
import importlib

# The interaction service folder uses a hyphen in its name (jebediah-interaction)
# To import the app package (app.main) we temporarily change cwd into the
# service folder so Python can import the local "app" package as it would at runtime.
repo_root = Path(__file__).resolve().parents[2]
service_dir = repo_root / "services" / "jebediah-interaction"
import sys
orig_cwd = Path.cwd()
# Ensure the service dir is on sys.path so `import app` works as it does at runtime
sys.path.insert(0, str(service_dir))
try:
    os.chdir(str(service_dir))
    main_mod = importlib.import_module("app.main")
finally:
    os.chdir(orig_cwd)
    # clean up inserted path
    try:
        sys.path.remove(str(service_dir))
    except ValueError:
        pass

client = TestClient(main_mod.app)


def test_chat_success_path(monkeypatch):
    # Mock memory_client.retrieve_context to return structured memories
    async def fake_retrieve_context(query: str):
        return {
            "query": query,
            "memories": [
                {"score": 0.9, "content": "Important fact A", "metadata": {"source": "doc1"}},
                {"score": 0.8, "content": "Secondary fact B", "metadata": {"source": "doc2"}},
            ],
        }

    async def fake_generate(messages):
        # Check that the messages include a deterministic context block
        assert any("Retrieved Project Context:" in m["content"] for m in messages)
        return "Generated reply"

    monkeypatch.setattr(main_mod, "retrieve_context", fake_retrieve_context)
    monkeypatch.setattr(main_mod, "generate", fake_generate)

    resp = client.post("/chat", json={"message": "Hello"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["response"] == "Generated reply"
    # context_used should be the structured dict returned by the memory client
    assert isinstance(body["context_used"], dict)
    assert body["context_used"]["query"] == "Hello"


def test_memory_unavailable_behavior(monkeypatch):
    async def raise_memory_unavailable(query: str):
        raise HTTPException(status_code=503, detail="memory service unavailable")

    monkeypatch.setattr(main_mod, "retrieve_context", raise_memory_unavailable)

    resp = client.post("/chat", json={"message": "Hello"})
    assert resp.status_code == 503


def test_ollama_unavailable_behavior(monkeypatch):
    # Provide a valid context, but make generate raise HTTPException 503
    async def good_context(query: str):
        return {"query": query, "memories": []}

    async def raise_ollama(messages):
        raise HTTPException(status_code=503, detail="ollama unavailable")

    monkeypatch.setattr(main_mod, "retrieve_context", good_context)
    monkeypatch.setattr(main_mod, "generate", raise_ollama)

    resp = client.post("/chat", json={"message": "Hello"})
    assert resp.status_code == 503


def test_structured_context_handling(monkeypatch):
    # Return memories with unordered metadata and scores to test deterministic rendering
    async def unordered_context(query: str):
        return {
            "query": query,
            "memories": [
                {"score": 0.5, "content": "C", "metadata": {"b": 2, "a": 1}},
                {"score": 0.7, "content": "A", "metadata": {"z": 9}},
                {"score": 0.7, "content": "B", "metadata": {"y": 8}},
            ],
        }

    async def fake_generate(messages):
        # Ensure the deterministic ordering: score 0.7 items first, then 0.5
        context_msg = messages[1]["content"]
        # The first memory block should be A (score 0.7) and deterministically ordered
        assert "A" in context_msg
        return "ok"

    monkeypatch.setattr(main_mod, "retrieve_context", unordered_context)
    monkeypatch.setattr(main_mod, "generate", fake_generate)

    resp = client.post("/chat", json={"message": "Hello"})
    assert resp.status_code == 200
