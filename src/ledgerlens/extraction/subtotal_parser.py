import re
from decimal import Decimal

from ledgerlens.extraction.money_parser import parse_money


def extract_subtotal(text: str | None) -> Decimal | None:
    if not text:
        return None

    text = text.strip()

    pattern = r"""
         # Subtotal, Sub Total, Sub-total, sub_total
        \b sub[\s\-_]*total \b                 
        # Optional separators (spaces, colons, dashes, hashes)
        [\s:\-\#]*                              

        (                                       
            # Uppercase currency code or symbol
            (?:[A-Z]{3}|[\$\u20AC\u00A3\u00A5\u20B9])? 
            \s*
            (?:
                \d{1,3}(?:,\d{3})+(?:\.\d{1,2})? # Numbers with commas
                |
                \d+(?:\.\d{1,2})?               # Plain numbers
            )
        )
    """

    match = re.search(pattern, text, flags=re.VERBOSE | re.IGNORECASE)
    if not match:
        return None

    candidate_str = match.group(1).strip()

    return parse_money(candidate_str)
