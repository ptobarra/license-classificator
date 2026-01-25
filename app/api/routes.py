from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel

from app.core.config import settings
from app.db.session import get_session
from app.db.repo import LicenseRepo
from app.services.excel_io import read_licenses_from_xlsx, export_to_xlsx
from app.services.classifier import get_llm_client

router = APIRouter()
repo = LicenseRepo()


class ManualUpdate(BaseModel):
    typology: str
    explanation: str


@router.post("/classify")
async def classify_all(session: Session = Depends(get_session)):
    # 1) Ingest from Excel (upsert base data)
    items = read_licenses_from_xlsx(settings.input_xlsx_path)
    repo.upsert_many(session, items)

    # 2) Classify using LLM (skip manual overrides)
    llm = get_llm_client()
    records = repo.list_all(session)

    for r in records:
        if r.decided_by == "manual":
            continue
        result = await llm.classify_license(r.license_description)
        repo.update_llm(session, r.license_id, result.typology, result.explanation)

    # 3) Export output.xlsx
    updated = repo.list_all(session)
    out_path = export_to_xlsx(updated)

    return {"count": len(updated), "output_xlsx": out_path}


@router.get("/licenses")
def list_licenses(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.patch("/licenses/{license_id}")
def update_license(
    license_id: int, body: ManualUpdate, session: Session = Depends(get_session)
):
    try:
        updated = repo.update_manual(
            session, license_id, body.typology, body.explanation
        )
        return updated
    except ValueError:
        raise HTTPException(status_code=404, detail="License not found")
