import re
from decimal import Decimal

from ledgerlens.extraction.money_parser import parse_money


def extract_total(text: str | None) -> Decimal | None:

    if not text:
        return None

    money_pattern = r"""
        [\s:\-\#]*
        (
            (?:[A-Z]{3}|[\$\u20AC\u00A3\u00A5\u20B9])?
            \s*
            (?:
                \d{1,3}(?:,\d{3})+(?:\.\d{1,2})?
                |
                \d+(?:\.\d{1,2})?
            )
        )
        (?!\d|[\.,]\d)
        (?!\s*\%)
    """

    explicit_labels = [
        r"\b grand \s+ total \b",
        r"\b (?:amount|balance|total) \s+ due \b",
        r"\b invoice \s+ total \b",
    ]

    for label in explicit_labels:
        pattern = f"{label}{money_pattern}"
        match = re.search(pattern, text, flags=re.VERBOSE | re.IGNORECASE)
        if match:
            candidate_str = match.group(1).strip()
            result = parse_money(candidate_str)
            if result is not None:
                return result

    fallback_pattern = f"^\s* total \\b {money_pattern}"
    match = re.search(
        fallback_pattern,
        text,
        flags=re.VERBOSE | re.IGNORECASE | re.MULTILINE,
    )
    if match:
        candidate_str = match.group(1).strip()
        return parse_money(candidate_str)

    return None
