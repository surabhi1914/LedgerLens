import re
from datetime import date, datetime


def extract_invoice_date(text: str) -> date | None:
    if not text:
        return None

    # Pattern for: Invoice Date, Inv Date, Invoice Dt, etc.
    pattern1 = r"""
        \b(?:invoice|inv)\b                    # Whole word "invoice" or "inv"
        \s+                                    # At least one whitespace
        (?:date|dt|dated)                     # date, dt, or dated
        \s*                                    # Optional whitespace
        [:/-]?                                 # Optional separator
        \s*                                    # Optional whitespace
        (                                      # CAPTURE GROUP: the date
            \d{1,2}[/-]\d{1,2}[/-]\d{4}       # MM/DD/YYYY or MM-DD-YYYY
            |
            \d{4}-\d{1,2}-\d{1,2}             # YYYY-MM-DD only (hyphens)
        )
    """

    # Pattern for: Date of Invoice
    pattern2 = r"""
        \bdate\b                               # Whole word "date"
        \s+                                    # At least one whitespace
        \bof\b                                 # Whole word "of"
        \s+                                    # At least one whitespace
        \binvoice\b                            # Whole word "invoice"
        \s*                                    # Optional whitespace
        [:/-]?                                 # Optional separator
        \s*                                    # Optional whitespace
        (                                      # CAPTURE GROUP: the date
            \d{1,2}[/-]\d{1,2}[/-]\d{4}       # MM/DD/YYYY or MM-DD-YYYY
            |
            \d{4}-\d{1,2}-\d{1,2}             # YYYY-MM-DD only (hyphens)
        )
    """

    # Try pattern1 first (Invoice Date, Inv Date, etc.)
    match = re.search(pattern1, text, re.VERBOSE | re.IGNORECASE)
    if not match:
        # Try pattern2 (Date of Invoice)
        match = re.search(pattern2, text, re.VERBOSE | re.IGNORECASE)

    if not match:
        return None

    # One capture group contains the date
    date_str = match.group(1).strip()

    # Try supported formats in order
    formats = [
        "%m/%d/%Y",  # 08/02/2026
        "%m-%d-%Y",  # 08-02-2026
        "%Y-%m-%d",  # 2026-08-02
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None
