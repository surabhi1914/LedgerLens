import re

# Document headers and common field labels that should never be selected as a vendor
IGNORE_PATTERNS = [
    # Document headers
    r"^\s*(?:tax\s+)?invoice\s*$",
    r"^\s*receipt\s*$",
    r"^\s*bill\s*$",
    r"^\s*statement\s*$",
    # Explicit vendor labels (prevents Stage B fallback from picking up "Vendor: 123456")
    r"^\s*(?:vendor|supplier|seller|from)\b",
    # Common field labels
    r"^\s*invoice\s*(?:no\.?|number|\#|date|total|amount)",
    r"^\s*(?:bill|ship)\s*to",
    r"^\s*(?:date|total|subtotal|tax|amount\s+due|balance\s+due)",
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
