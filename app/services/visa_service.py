import json
import os
from typing import Optional
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/visa_requirements.json")

def load_data() -> dict:
    with open(DATA_PATH) as f:
        return json.load(f)


def get_corridor(from_country: str, to_country: str, purpose: str) -> Optional[dict]:
    data = load_data()
    key = f"{from_country.upper()}-{to_country.upper()}-{purpose}"
    return data.get(key)


async def get_ai_tips(corridor_data: dict, occupation: Optional[str], duration_days: Optional[int]) -> list[str]:
    context = json.dumps(corridor_data, indent=2)
    user_context = f"Occupation: {occupation or 'not specified'}. Duration: {duration_days or 'not specified'} days."

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a visa documentation assistant. Based on the corridor data provided, "
                    "suggest 3-5 applicant-specific tips. You MUST NOT invent fees, dates, or rules not in the data. "
                    "Respond ONLY with JSON: {\"tips\": [\"tip1\", \"tip2\", ...]}"
                )
            },
            {
                "role": "user",
                "content": f"Corridor data:\n{context}\n\nApplicant context: {user_context}"
            }
        ],
        max_tokens=400,
    )

    result = json.loads(response.choices[0].message.content)
    return result.get("tips", [])
