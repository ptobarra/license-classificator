import os
import pandas as pd
from app.db.models import License
from app.core.config import settings


def read_licenses_from_xlsx(path: str) -> list[License]:
    df = pd.read_excel(path)
    # Expect columns: "License ID", "License Description"
    df.columns = [c.strip() for c in df.columns]
    items: list[License] = []
    for _, row in df.iterrows():
        items.append(
            License(
                license_id=int(row["License ID"]),
                license_description=str(row["License Description"]).strip(),
            )
        )
    return items


def export_to_xlsx(records: list[License]) -> str:
    os.makedirs(settings.output_dir, exist_ok=True)
    out_path = settings.output_xlsx_path

    df = pd.DataFrame(
        [
            {
                "License ID": r.license_id,
                "License Description": r.license_description,
                "Typology": r.typology,
                "Explanation": r.explanation,
                "Decided By": r.decided_by,
            }
            for r in records
        ]
    )

    df.to_excel(out_path, index=False)
    return out_path
