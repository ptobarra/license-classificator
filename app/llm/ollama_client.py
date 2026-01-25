import json
import httpx
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

SYSTEM = (
    "You classify software license names into exactly one typology: "
    "Productivity, Design, Communication, Development, Finance, Marketing. "
    "Return strict JSON only."
)


def _prompt(name: str) -> str:
    return f"""
Classify this license name: "{name}"

Rules:
- typology must be one of: {sorted(ALLOWED)}
- explanation must be <= 150 characters
Return JSON like:
{{"typology":"...", "explanation":"..."}}
""".strip()


class OllamaClient(LLMClient):
    async def classify_license(self, license_name: str) -> LLMResult:
        url = f"{settings.ollama_base_url}/api/generate"
        payload = {
            "model": settings.ollama_model,
            "prompt": _prompt(license_name),
            "system": SYSTEM,
            "stream": False,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()

        # Ollama returns {"response": "...json..."}
        raw = data.get("response", "").strip()
        obj = json.loads(raw)

        typology = obj.get("typology", "").strip()
        explanation = obj.get("explanation", "").strip()[:150]

        if typology not in ALLOWED:
            typology = "Productivity"  # safe fallback
            explanation = (
                explanation or "Fallback classification due to invalid model output."
            )[:150]

        return LLMResult(typology=typology, explanation=explanation)
