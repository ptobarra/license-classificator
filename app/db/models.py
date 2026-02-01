from sqlmodel import SQLModel, Field
from typing import Optional


class License(SQLModel, table=True):
    """
    SQLModel representing a software license with classification metadata.

    This model stores both the raw license data ingested from Excel and the
    classification results from LLM inference or manual review. It serves as
    the single source of truth for license typology assignments and supports
    human-in-the-loop override workflows.

    Attributes:
        license_id: Unique integer identifier for the license (primary key)
        license_description: Textual name/description of the software license
        typology: Assigned business category from the allowed set:
                  (Productivity, Design, Communication, Development, Finance, Marketing).
                  None until classified.
        explanation: Natural language rationale for the typology assignment.
                     Must be ≤150 characters. None until classified.
        decided_by: Classification source indicator. Either "llm" for automated
                    classification or "manual" for human override. None until classified.
                    Manual decisions always take precedence over LLM outputs.

    Table name: license (auto-generated from class name)

    Example:
        >>> license = License(
        ...     license_id=1,
        ...     license_description="Microsoft Office 365",
        ...     typology="Productivity",
        ...     explanation="Office productivity suite",
        ...     decided_by="llm"
        ... )
        >>> license.license_id
        1

    Note:
        The `decided_by` field enables audit trails and prevents LLM from
        overwriting manual corrections. See [`LicenseRepo.update_llm`](app/db/repo.py)
        for override logic.
    """

    license_id: int = Field(primary_key=True)
    license_description: str

    typology: Optional[str] = None
    explanation: Optional[str] = None  # must be <= 150 chars
    decided_by: Optional[str] = None  # "llm" or "manual"
