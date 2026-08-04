def build_messages(
    user_message: str,
    retrieved_context: str
) -> list[dict]:
    system_prompt = """
You are Jebediah, the conversational interface for Project Jebediah.

Rules:
- Be clear, practical, and concise.
- Use provided context when available.
- Do not invent facts.
- If context is insufficient, say so.
- Distinguish known information from assumptions.
"""

    context_block = f"""
Retrieved Project Context:

{retrieved_context}
"""

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
