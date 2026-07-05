import json
from typing import AsyncGenerator, List
from openai import AsyncOpenAI
from app.config import settings
from app.services.visa_service import load_data

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are VisaMitra, a friendly and knowledgeable visa documentation assistant for Indian travelers.
You help users understand visa requirements, document checklists, and application processes.
You ONLY provide information grounded in the provided corridor data. Never invent fees, dates, or rules.
If you don't know something, say so and suggest the official embassy website.
Keep responses concise and actionable."""


async def stream_chat(message: str, corridor: str | None, history: List[dict]) -> AsyncGenerator[str, None]:
    # Ground with corridor data if available
    grounding = ""
    if corridor:
        data = load_data()
        corridor_data = data.get(corridor)
        if corridor_data:
            grounding = f"\n\nCorridor data for context:\n{json.dumps(corridor_data, indent=2)}"

    messages = [{"role": "system", "content": SYSTEM_PROMPT + grounding}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history[-10:]]
    messages.append({"role": "user", "content": message})

    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        max_tokens=600,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'content': delta})}\n\n"

    yield "data: [DONE]\n\n"
