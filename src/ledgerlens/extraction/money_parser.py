import re
from decimal import Decimal, InvalidOperation


def parse_money(value: str | None) -> Decimal | None:
    if not value:
        return None

    text = value.strip()

    pattern = r"""
        ^(?:[A-Z]{3}|[\$\u20AC\u00A3\u00A5\u20B9])? # Optional currency
        \s*
        (                                          # CAPTURE: the number
            \d{1,3}(?:,\d{3})+(?:\.\d{1,2})?       # Numbers with commas
            |
            \d+(?:\.\d{1,2})?                      # Plain numbers
        )
    """

    match = re.fullmatch(pattern, text, re.VERBOSE)
    if not match:
        return None

    amount_str = match.group(1).strip()
    clean_num = amount_str.replace(",", "")

    try:
        return Decimal(clean_num)
    except InvalidOperation:
        return None
