import re


def extract_invoice_number(text: str) -> str | None:
    if not text:
        return None

    pattern = r"""
        \b(?:invoice|inv)\b                    # Word boundaries around invoice/inv
        \s*                                    # Zero or more whitespace
        (?:                                    # Optional qualifier group
            no\.?|number|\#|id                 # no, no., number, #, or id
        )?                                     # Qualifier is optional (intentional)
        \s*                                    # Zero or more whitespace
        [:/-]?                                 # Optional separator: colon, slash, or hyphen
        \s*                                    # Zero or more whitespace
        (?=[A-Z0-9/\-]*\d)                     # Lookahead: must contain at least one digit
        ([A-Z0-9/\-]+)                         # Capture: letters, digits, /, and -
    """

    match = re.search(pattern, text, re.VERBOSE | re.IGNORECASE)
    return match.group(1) if match else None
