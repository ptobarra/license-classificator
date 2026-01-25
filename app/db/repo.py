from sqlmodel import Session, select
from app.db.models import License


class LicenseRepo:
    def upsert_many(self, session: Session, licenses: list[License]) -> None:
        for lic in licenses:
            existing = session.get(License, lic.license_id)
            if existing:
                existing.license_description = lic.license_description
            else:
                session.add(lic)
        session.commit()

    def list_all(self, session: Session) -> list[License]:
        return session.exec(select(License).order_by(License.license_id)).all()

    def get(self, session: Session, license_id: int) -> License | None:
        return session.get(License, license_id)

    def update_manual(
        self, session: Session, license_id: int, typology: str, explanation: str
    ) -> License:
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
