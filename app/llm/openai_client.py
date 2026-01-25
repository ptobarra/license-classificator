# If using OpenAI, install openai and create .env with key.

import json
from app.core.config import settings
from app.llm.base import LLMClient, LLMResult

ALLOWED = {
    "Productivity",
    "Design",
    "Communication",
    "Development",
    "Finance",
    "Marketing",
}


class OpenAIClient(LLMClient):
    async def classify_license(self, license_name: str) -> LLMResult:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY missing")

        # Lazy import so repo works without OpenAI installed
        # TODO: If using OpenAI, install openai and create .env with key.
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)

        msg = f"""
Classify "{license_name}" into exactly one of:
Productivity, Design, Communication, Development, Finance, Marketing.
Return strict JSON: {{"typology":"...", "explanation":"<=150 chars"}}
""".strip()

        resp = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "Return strict JSON only. No prose."},
                {"role": "user", "content": msg},
            ],
            temperature=0,
        )

        # raw = resp.choices[0].message.content.strip()
        content = resp.choices[0].message.content or ""
        raw = content.strip()
        obj = json.loads(raw)
        typology = obj.get("typology", "").strip()
        explanation = obj.get("explanation", "").strip()[:150]

        if typology not in ALLOWED:
            typology = "Productivity"
            explanation = (
                explanation or "Fallback classification due to invalid model output."
            )[:150]

        return LLMResult(typology=typology, explanation=explanation)
