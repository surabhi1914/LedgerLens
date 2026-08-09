from dataclasses import dataclass
from io import BytesIO

import pymupdf
from PIL import Image

from ledgerlens.config import settings


@dataclass
class DocumentPreview:
    is_successful: bool
    image: Image.Image | None = None
    error_message: str | None = None
    page_count: int | None = None


def create_document_preview(file_bytes, extension) -> DocumentPreview:

    if not file_bytes:
        return DocumentPreview(
            is_successful=False,
            image=None,
            error_message="The uploaded document is empty.",
            page_count=None,
        )

    extension = normalize_extension(extension)

    if extension in settings.allowed_document_extensions:
        return doc_handling(file_bytes)
    elif extension in settings.allowed_image_extensions:
        return image_handling(file_bytes)
    else:
        return DocumentPreview(
            is_successful=False,
            image=None,
            error_message=f"The document format {extension} is not supported.",
            page_count=None,
        )


def image_handling(file_bytes) -> DocumentPreview:

    try:
        image = Image.open(BytesIO(file_bytes))
        if image.mode != "RGB":
            image = image.convert("RGB")
        return DocumentPreview(
            is_successful=True, image=image.copy(), error_message=None, page_count=1
        )
    except Exception:
        return DocumentPreview(
            is_successful=False,
            image=None,
            error_message="The uploaded image could not be opened.",
            page_count=None,
        )


def doc_handling(file_bytes: bytes) -> DocumentPreview:
    doc = None
    try:
        doc = pymupdf.open(stream=BytesIO(file_bytes), filetype="pdf")
        page_count = len(doc)

        if page_count == 0:
            return DocumentPreview(
                is_successful=False,
                image=None,
                error_message="Document is corrupted. No pages in the document.",
                page_count=None,
            )

        first_page = doc[0]
        try:
            mat = pymupdf.Matrix(1.5, 1.5)  # Scale for readability
            pix = first_page.get_pixmap(matrix=mat)
            image_bytes = pix.tobytes("ppm")

            # Process rendered image bytes
            preview_res = image_handling(image_bytes)

            # If image processing failed, return its error result as-is
            if not preview_res.is_successful:
                return preview_res

            # Override page_count with the actual PDF length
            preview_res.page_count = page_count
            return preview_res

        except Exception:
            return DocumentPreview(
                is_successful=False,
                image=None,
                error_message="The PDF could not be rendered.",
                page_count=None,
            )

    except Exception:
        return DocumentPreview(
            is_successful=False,
            image=None,
            error_message="The PDF could not be opened.",
            page_count=None,
        )

    finally:
        if doc is not None:
            doc.close()


def normalize_extension(extension) -> str:
    ex = extension.strip()
    ex = ex.lower()
    ex = ex.lstrip(".")

    return ex
