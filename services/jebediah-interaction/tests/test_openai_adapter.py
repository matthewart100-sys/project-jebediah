import pytest
from httpx import AsyncClient

from app import main


@pytest.mark.asyncio
async def test_openai_endpoint_available(monkeypatch):
    async def fake_retrieve_context(text):
        return {"memories": []}

    async def fake_generate(messages):
        return "response text"

    monkeypatch.setattr(main, "retrieve_context", fake_retrieve_context)
    monkeypatch.setattr(main, "generate", fake_generate)

    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        r = await ac.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "Hello"}]})

    assert r.status_code == 200
    j = r.json()
    assert "choices" in j
    assert j["choices"][0]["message"]["content"] == "response text"


@pytest.mark.asyncio
async def test_openai_endpoint_missing_message():
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        r = await ac.post("/v1/chat/completions", json={})

    assert r.status_code == 400


@pytest.mark.asyncio
async def test_openai_flow_invokes_memory_and_generate(monkeypatch):
    called = {}

    async def fake_retrieve_context(text):
        called['retrieved_text'] = text
        return {"memories": [{"id": "m1", "content": "mem content"}]}

    async def fake_generate(messages):
        called['generate_messages'] = messages
        return "generated reply"

    monkeypatch.setattr(main, "retrieve_context", fake_retrieve_context)
    monkeypatch.setattr(main, "generate", fake_generate)

    payload = {"messages": [{"role": "system", "content": "You are helpful."}, {"role": "user", "content": "What can you do?"}]}

    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        r = await ac.post("/v1/chat/completions", json=payload)

    assert r.status_code == 200
    assert called.get('retrieved_text') == "What can you do?"
    assert isinstance(called.get('generate_messages'), list)
    # Ensure generate returned value is reflected in response
    j = r.json()
    assert j["choices"][0]["message"]["content"] == "generated reply"
