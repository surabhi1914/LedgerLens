import re
from decimal import Decimal

from ledgerlens.extraction.money_parser import parse_money


def extract_tax(text: str | None) -> Decimal | None:
    if not text:
        return None

    pattern = r"""
        \b (?:sales\s*tax|tax(?:\s*amount)?|vat|gst|hst) \b
        (?!\s*(?:rate|id|number|no\.?|\#|\%))
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

    match = re.search(pattern, text, flags=re.VERBOSE | re.IGNORECASE)
    if not match:
        return None

    candidate_str = match.group(1).strip()

    return parse_money(candidate_str)
