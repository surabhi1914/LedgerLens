import pymupdf
import PIL

from pydantic import BaseModel
from ledgerlens.config import settings

class DocumentPreview(BaseModel):
    is_successful: bool
    image: PIL.Image | None
    error_message: str | None
    page_count: int

def create_document_preview(file_name, file_bytes, extension) -> DocumentPreview:






