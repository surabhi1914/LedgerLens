import re

# Supported ISO currency codes
SUPPORTED_CODES = ("USD", "EUR", "GBP", "INR")


SYMBOL_TO_CODE = {
    "$": "USD",
    "€": "EUR",
    "£": "GBP",
    "₹": "INR",
}


def extract_currency(text: str | None) -> str | None:
    if not text:
        return None

    codes_pattern = r"\b(" + "|".join(SUPPORTED_CODES) + r")\b"
    code_match = re.search(codes_pattern, text, flags=re.IGNORECASE)

    if code_match:
        return code_match.group(1).upper()

    for symbol, code in SYMBOL_TO_CODE.items():
        if symbol in text:
            return code

    return None
