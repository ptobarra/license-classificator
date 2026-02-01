from sqlmodel import Session, select, col
from app.db.models import License


class LicenseRepo:
    """
    Repository for managing License entity persistence and business logic.

    Provides data access methods for license classification workflows, including
    batch ingestion, manual overrides, and LLM-based classification updates with
    human-in-the-loop protection.

    Methods:
        upsert_many: Bulk insert or update license records from Excel ingestion
        list_all: Retrieve all licenses ordered by ID
        get: Fetch a single license by ID
        update_manual: Apply human-curated classification (override-safe)
        update_llm: Apply LLM classification (respects manual overrides)

    Example:
        >>> from sqlmodel import Session
        >>> from app.db.session import engine
        >>> repo = LicenseRepo()
        >>> with Session(engine) as session:
        ...     licenses = repo.list_all(session)
        ...     repo.update_manual(session, 1, "Productivity", "Office suite")
    """

    def upsert_many(self, session: Session, licenses: list[License]) -> None:
        """
        Insert new licenses or update descriptions for existing ones.

        Used during Excel ingestion to sync license_id and license_description
        without overwriting classification metadata (typology, explanation, decided_by).

        Args:
            session: Active SQLModel database session
            licenses: List of License instances to upsert (must have license_id)

        Example:
            >>> from app.services.excel_io import read_licenses_from_xlsx
            >>> licenses = read_licenses_from_xlsx("licenses.xlsx")
            >>> repo.upsert_many(session, licenses)
        """
        for lic in licenses:
            existing = session.get(License, lic.license_id)
            if existing:
                existing.license_description = lic.license_description
            else:
                session.add(lic)
        session.commit()

    def list_all(self, session: Session) -> list[License]:
        """
        Retrieve all licenses from the database, ordered by license_id.

        Returns:
            List of all License records, including classification metadata

        Example:
            >>> licenses = repo.list_all(session)
            >>> len(licenses)
            42
        """
        return list(
            session.exec(select(License).order_by(col(License.license_id))).all()
        )

    def get(self, session: Session, license_id: int) -> License | None:
        """
        Fetch a single license by its primary key.

        Args:
            session: Active SQLModel database session
            license_id: Primary key of the license to retrieve

        Returns:
            License instance if found, None otherwise

        Example:
            >>> license = repo.get(session, 123)
            >>> if license:
            ...     print(license.license_description)
        """
        return session.get(License, license_id)

    def update_manual(
        self, session: Session, license_id: int, typology: str, explanation: str
    ) -> License:
        """
        Apply human-curated classification to a license.

        Sets decided_by to "manual", which prevents future LLM updates from
        overwriting this classification. This enables human-in-the-loop correction
        workflows and audit trails for business-critical decisions.

        Args:
            session: Active SQLModel database session
            license_id: Primary key of the license to update
            typology: Business category (must be from allowed set)
            explanation: Natural language rationale (truncated to 150 chars)

        Returns:
            Updated License instance with manual classification applied

        Raises:
            ValueError: If license_id does not exist in database

        Example:
            >>> license = repo.update_manual(
            ...     session, 1, "Productivity", "Corrected by domain expert"
            ... )
            >>> license.decided_by
            'manual'

        Note:
            Once a license is marked as "manual", [`update_llm`](app/db/repo.py)
            will skip it to preserve human decisions.
        """
        lic = session.get(License, license_id)
        if not lic:
            raise ValueError("License not found")
        lic.typology = typology
        lic.explanation = explanation[:150]
        lic.decided_by = "manual"
        session.add(lic)
        session.commit()
        session.refresh(lic)
        return lic

    def update_llm(
        self, session: Session, license_id: int, typology: str, explanation: str
    ) -> None:
        """
        Apply LLM-generated classification to a license (respects manual overrides).

        Updates classification metadata only if the license has not been manually
        classified. This ensures human decisions always take precedence over
        automated inference, enabling safe LLM retraining and batch reclassification.

        Args:
            session: Active SQLModel database session
            license_id: Primary key of the license to update
            typology: LLM-assigned business category
            explanation: LLM-generated rationale (truncated to 150 chars)

        Behavior:
            - If license not found: silently returns (idempotent)
            - If decided_by == "manual": skips update (preserves human override)
            - Otherwise: updates typology, explanation, and sets decided_by="llm"

        Example:
            >>> result = await llm_client.classify_license("MS Office")
            >>> repo.update_llm(session, 1, result.typology, result.explanation)

        Note:
            Called by [`classify_all`](app/api/routes.py) during batch processing.
            Manual classifications are protected via the decided_by guard.
        """
        lic = session.get(License, license_id)
        if not lic:
            return
        if lic.decided_by == "manual":
            return  # respect manual overrides
        lic.typology = typology
        lic.explanation = explanation[:150]
        lic.decided_by = "llm"
        session.add(lic)
        session.commit()
