import fitz
from fastapi import UploadFile

from app.schemas.tokenization import ExtractedDocument
from app.services.file_validation import FileProcessingError, validate_upload


async def extract_document(upload: UploadFile) -> ExtractedDocument:
    extension = validate_upload(upload)
    content = await upload.read()
    if extension == ".txt":
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise FileProcessingError(
                "INVALID_TEXT", "The TXT file must use UTF-8 text encoding."
            ) from error
        return ExtractedDocument(text=text, source_type="txt")
    if not content.startswith(b"%PDF-"):
        raise FileProcessingError("INVALID_PDF", "The uploaded PDF could not be read.")
    try:
        with fitz.open(stream=content, filetype="pdf") as document:
            text = "\n".join(page.get_text("text") for page in document)
    except (fitz.FileDataError, fitz.EmptyFileError, RuntimeError) as error:
        raise FileProcessingError(
            "INVALID_PDF", "The uploaded PDF is invalid or corrupted."
        ) from error
    if not text.strip():
        raise FileProcessingError("PDF_NO_TEXT", "No extractable text was found in this PDF.")
    return ExtractedDocument(text=text, source_type="pdf")
