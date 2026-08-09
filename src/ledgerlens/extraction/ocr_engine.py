from dataclasses import dataclass

import pytesseract
from PIL import Image


@dataclass
class OCRResult:
    is_successful: bool
    text: str | None
    error_message: str | None


def extract_text(image: Image.Image | None) -> OCRResult:

    if not image:
        return OCRResult(is_successful=False, text=None, error_message="No Image found")

    if image.mode not in ["RGB", "RGBA"]:
        image = image.convert("RGB")

    try:
        text = pytesseract.image_to_string(image)

        text = text.strip()

        if not text:
            return OCRResult(
                is_successful=False,
                text="",
                error_message="No readable text was detected in the document.",
            )
        return OCRResult(is_successful=True, text=text, error_message=None)

    except Exception:
        return OCRResult(
            is_successful=False,
            text=None,
            error_message="Unable to extract text from the document",
        )
