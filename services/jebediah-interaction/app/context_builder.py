def build_messages(
    user_message: str,
    retrieved_context: dict
) -> list[dict]:
    """Construct messages for the generation model.

    Accepts retrieved_context as structured JSON (the memory service response)
    and produces a deterministic, human-readable context block sorted by
    relevance score to ensure reproducible assembly.
    """
    system_prompt = """
You are Jebediah, the conversational interface for Project Jebediah.

Rules:
- Be clear, practical, and concise.
- Use provided context when available.
- Do not invent facts.
- If context is insufficient, say so.
- Distinguish known information from assumptions.
"""

    # Build a deterministic context block from structured memories
    memories = []
    if isinstance(retrieved_context, dict):
        mems = retrieved_context.get("memories") or []
        # Sort by score descending, then by content to break ties deterministically
        try:
            sorted_mems = sorted(
                mems,
                key=lambda m: (-(m.get("score") or 0), m.get("content") or "")
            )
        except Exception:
            sorted_mems = mems

        for m in sorted_mems:
            score = m.get("score")
            content = m.get("content")
            metadata = m.get("metadata")
            memories.append({"score": score, "content": content, "metadata": metadata})

    # Render the context block deterministically
    if memories:
        context_lines = ["Retrieved Project Context:"]
        for idx, m in enumerate(memories, start=1):
            context_lines.append(f"[{idx}] score={m['score']}")
            context_lines.append(m["content"] or "")
            # Include metadata keys in sorted order for determinism
            meta = m.get("metadata") or {}
            if isinstance(meta, dict) and meta:
                for k in sorted(meta.keys()):
                    context_lines.append(f"- {k}: {meta[k]}")
            context_lines.append("")
        context_block = "\n".join(context_lines)
    else:
        context_block = "Retrieved Project Context:\n\n<no relevant memories>"

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "system",
            "content": context_block
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
