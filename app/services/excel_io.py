import os
import pandas as pd
from app.db.models import License
from app.core.config import settings


def read_licenses_from_xlsx(path: str) -> list[License]:
    """
    Read and parse software license data from an Excel file.

    Expects an Excel file with two columns:
    - "License ID": Integer identifier for the license
    - "License Description": Textual description of the license

    Args:
        path: File path to the Excel (.xlsx) file containing license data

    Returns:
        A list of License model instances with license_id and license_description populated.
        Other fields (typology, explanation, decided_by) remain None until classification.

    Raises:
        FileNotFoundError: If the specified Excel file does not exist
        KeyError: If required columns are missing from the Excel file
        ValueError: If license_id cannot be converted to integer

    Example:
        >>> licenses = read_licenses_from_xlsx("licenses.xlsx")
        >>> len(licenses)
        42
        >>> licenses[0].license_description
        'Microsoft Office 365'
    """
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
    """
    Export classified license records to an Excel file.

    Creates an Excel file with classified license data including typology,
    explanation, and decision source (LLM or manual). The output directory
    is created automatically if it doesn't exist.

    Args:
        records: List of License model instances to export, including both
                 base data and classification results

    Returns:
        The absolute file path to the generated Excel file as configured in
        settings.output_xlsx_path (default: "output/output.xlsx")

    Output columns:
        - "License ID": Integer identifier for the license
        - "License Description": Textual description of the license
        - "Typology": Assigned business category (Productivity, Design, etc.)
        - "Explanation": Natural language rationale (<=150 characters)
        - "Decided By": Classification source ("llm" or "manual")

    Example:
        >>> from app.db.models import License
        >>> licenses = [
        ...     License(license_id=1, license_description="MS Office",
        ...             typology="Productivity", explanation="Office suite",
        ...             decided_by="llm")
        ... ]
        >>> path = export_to_xlsx(licenses)
        >>> print(path)
        'output/output.xlsx'

    Note:
        Uses settings from [`app.core.config.settings`](app/core/config.py) for
        output directory and file path configuration.
    """
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
