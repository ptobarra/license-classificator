from dataclasses import dataclass


@dataclass
class LLMResult:
    typology: str
    explanation: str  # <= 150 chars


class LLMClient:
    async def classify_license(self, license_name: str) -> LLMResult:
        raise NotImplementedError
