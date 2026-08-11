import re


def normalize_ocr_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    raw_text = raw_text.replace("\r\n", "\n")
    raw_text = raw_text.replace("\r", "\n")
    raw_text = re.sub(r"\n{3,}", "\n\n", raw_text)

    cleaned_text = normalize_line(raw_text)

    cleaned_text = cleaned_text.strip()

    return cleaned_text


def normalize_line(text: str) -> str:
    normalized_lines = []
    stripped_lines = text.splitlines()
    for line in stripped_lines:
        line = line.strip()
        collapsed = re.sub(r"[ \t]{2,}", " ", line)
        normalized_lines.append(collapsed)
    joined_text = "\n".join(normalized_lines)

    return joined_text
