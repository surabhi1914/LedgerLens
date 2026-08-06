from pathlib import Path

from pydantic import BaseModel

from ledgerlens.config import settings


class ValidationResult(BaseModel):
    is_valid: bool
    error_message: str | None = None
    extension: str | None = None


def validate_upload(
    file_name: str,
    file_size_bytes: int,
) -> ValidationResult:
    # Validate the uploaded file for extension and size
    allowed_extensions = (
        settings.allowed_document_extensions + settings.allowed_image_extensions
    )
    allowed_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    file_name = file_name.strip()
    if not file_name:
        return ValidationResult(
            is_valid=False,
            error_message="File name is empty.",
            extension="",
        )

    extension = normalize_extension(file_name)

    if not extension:
        return ValidationResult(
            is_valid=False,
            error_message="File extension is missing.",
            extension=extension,
        )

    stem_error = verify_file_stem(file_name)
    if stem_error:
        return ValidationResult(
            is_valid=False,
            error_message=stem_error,
            extension=extension,
        )

    size_error = verify_file_size(file_size_bytes, allowed_size_bytes)
    if size_error:
        return ValidationResult(
            is_valid=False,
            error_message=size_error,
            extension=extension,
        )

    extension_error = verify_file_extension(extension, allowed_extensions)
    if extension_error:
        return ValidationResult(
            is_valid=False,
            error_message=extension_error,
            extension=extension,
        )

    return ValidationResult(
        is_valid=True,
        error_message=None,
        extension=extension,
    )


def normalize_extension(file_name: str) -> str:
    # Normalize the file extension to lowercase and return it
    extension = Path(file_name).suffix
    extension = extension.lower()
    extension = extension.lstrip(".")  # Remove the leading dot from the extension

    return extension


def verify_file_extension(
    extension: str, allowed_extensions: tuple[str, ...]
) -> str | None:
    # Check if the file extension is in the allowed extensions

    error_message = None
    if extension not in allowed_extensions:
        error_message = (
            f"File extension '{extension}' is not allowed. "
            f"Allowed extensions: {', '.join(allowed_extensions)}."
        )

    return error_message


def verify_file_size(file_size_bytes: int, allowed_size_bytes: int) -> str | None:
    # Check if the file size is within the allowed limit
    e = None
    if file_size_bytes < 0:
        e = f"File size '{file_size_bytes}' is invalid. File size cannot be negative."

    elif file_size_bytes == 0:
        e = f"File size '{file_size_bytes}' is invalid. File size cannot be zero."

    elif file_size_bytes > allowed_size_bytes:
        e = (
            f"File size '{file_size_bytes}' exceeds the allowed limit."
            f" Allowed size: '{allowed_size_bytes}' bytes."
        )

    return e


def verify_file_stem(file_name: str) -> str | None:
    # Check if the file stem (name without extension) is not empty

    e = None
    stem = Path(file_name).stem
    if stem.startswith("."):
        e = "File name (stem) cannot start with a dot."
    elif not stem:
        e = "File name (stem) cannot be empty."
    else:
        e = None

    return e
