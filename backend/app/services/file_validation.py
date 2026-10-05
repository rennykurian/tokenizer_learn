from fastapi import UploadFile

from app.core.config import get_settings


class FileProcessingError(ValueError):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def validate_upload(upload: UploadFile) -> str:
    settings = get_settings()
    suffix = (upload.filename or "").lower().rsplit(".", 1)
    extension = f".{suffix[-1]}" if len(suffix) > 1 else ""
    if extension not in settings.allowed_extensions:
        raise FileProcessingError("UNSUPPORTED_FILE_TYPE", "Upload a TXT or PDF file.")
    upload.file.seek(0, 2)
    size = upload.file.tell()
    upload.file.seek(0)
    if size > settings.max_upload_bytes:
        raise FileProcessingError(
            "FILE_TOO_LARGE", "The file exceeds the 10 MiB upload limit.", status_code=413
        )
    if extension == ".pdf" and upload.content_type not in (
        "application/pdf",
        "application/octet-stream",
    ):
        raise FileProcessingError("INVALID_PDF", "The uploaded PDF could not be validated.")
    if extension == ".txt" and upload.content_type not in (
        "text/plain",
        "application/octet-stream",
    ):
        raise FileProcessingError("UNSUPPORTED_FILE_TYPE", "Upload a plain TXT file.")
    return extension
