import asyncio
from io import BytesIO

import fitz
import pytest
from fastapi import UploadFile

from app.services.document_extraction import extract_document
from app.services.file_validation import FileProcessingError


def make_pdf(text: str | None = None) -> bytes:
    document = fitz.open()
    page = document.new_page()
    if text:
        page.insert_text((72, 72), text)
    content = document.tobytes()
    document.close()
    return content


def upload_pdf(content: bytes) -> UploadFile:
    return UploadFile(
        filename="sample.pdf", file=BytesIO(content), headers={"content-type": "application/pdf"}
    )


def test_extracts_text_from_pdf():
    result = asyncio.run(extract_document(upload_pdf(make_pdf("unit test text"))))

    assert "unit test text" in result.text
    assert result.source_type == "pdf"


def test_rejects_corrupted_pdf():
    with pytest.raises(FileProcessingError, match="invalid or corrupted"):
        asyncio.run(extract_document(upload_pdf(b"%PDF-not valid")))


def test_rejects_pdf_without_extractable_text():
    with pytest.raises(FileProcessingError, match="No extractable text"):
        asyncio.run(extract_document(upload_pdf(make_pdf())))
