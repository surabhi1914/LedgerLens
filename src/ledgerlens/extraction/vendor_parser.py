import re

# Document headers and common field labels that should never be selected as a vendor
IGNORE_PATTERNS = [
    # Document headers
    r"^\s*(?:tax\s+)?invoice\b",
    r"^\s*receipt\b",
    r"^\s*bill\b",
    r"^\s*statement\b",
    # Explicit vendor labels
    r"^\s*(?:vendor|supplier|seller|from)\b",
    # Common field labels & headers
    r"^\s*invoice\s*(?:no\.?|number|\#|date|total|amount)\b",
    r"^\s*(?:bill|ship)\s*to\b",
    # Dates & Financial Summary Labels
    (
        r"^\s*(?:due\s+date|payment\s+date|ship\s+date|billing\s+date|date|"
        r"total|subtotal|tax|amount\s+due|balance\s+due)\b"
    ),
    # Contact Information & Address Labels
    r"^\s*(?:address|tel|telephone|phone|email|site|website)\b",
]
# Combined compiled pattern for performance
_IGNORE_RE = re.compile("|".join(IGNORE_PATTERNS), flags=re.IGNORECASE)


def is_plausible_vendor(candidate: str | None) -> bool:
    if not candidate:
        return False

    candidate = candidate.strip()
    if not candidate:
        return False

    # Must contain at least one alphabetic character
    if not re.search(r"[a-zA-Z]", candidate):
        return False

    # Must not be a known ignored header or field label
    if _IGNORE_RE.search(candidate):
        return False

    return True


def extract_vendor(text: str | None) -> str | None:
    if not text:
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None

    label_pattern = r"^\s*(?:vendor|supplier|seller|from)[\s:\-\#]+(.+)$"
    for line in lines:
        match = re.match(label_pattern, line, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if is_plausible_vendor(candidate):
                return candidate

    for line in lines[:5]:
        if is_plausible_vendor(line):
            return line

    return None
