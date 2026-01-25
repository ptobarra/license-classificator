from sqlmodel import SQLModel, Field
from typing import Optional


class License(SQLModel, table=True):
    license_id: int = Field(primary_key=True)
    license_description: str

    typology: Optional[str] = None
    explanation: Optional[str] = None  # must be <= 150 chars
    decided_by: Optional[str] = None  # "llm" or "manual"
