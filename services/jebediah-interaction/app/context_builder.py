"""Deterministic model context assembly."""

from __future__ import annotations

from typing import Any


def build_messages(user_message: str, retrieved_context: dict[str, Any]) -> list[dict[str, str]]:
    memories = retrieved_context.get("memories", [])
    sorted_memories = sorted(
        (item for item in memories if isinstance(item, dict)),
        key=lambda item: (
            -(item.get("score") or 0),
            str(item.get("content") or ""),
        ),
    )
    context_lines = ["Retrieved governed organizational evidence:"]
    for index, memory in enumerate(sorted_memories, start=1):
        context_lines.append(f"[{index}] {memory.get('content') or ''}")
        metadata = memory.get("metadata")
        if isinstance(metadata, dict):
            for key in sorted(metadata):
                context_lines.append(f"- {key}: {metadata[key]}")

    return [
        {
            "role": "system",
            "content": (
                "Answer only from the supplied governed evidence. "
                "Do not invent facts. State when evidence is insufficient."
            ),
        },
        {"role": "system", "content": "\n".join(context_lines)},
        {"role": "user", "content": user_message},
    ]
