from io import BytesIO

import pytest
from fastapi import UploadFile

from app.services.file_validation import FileProcessingError, validate_upload


def test_validation_rejects_unsupported_extensions():
    upload = UploadFile(
        filename="data.docx",
        file=BytesIO(b"data"),
        headers={"content-type": "application/octet-stream"},
    )
    with pytest.raises(FileProcessingError, match="TXT or PDF") as error:
        validate_upload(upload)
    assert error.value.code == "UNSUPPORTED_FILE_TYPE"


def test_validation_accepts_plain_text():
    upload = UploadFile(
        filename="data.txt", file=BytesIO(b"text"), headers={"content-type": "text/plain"}
    )
    assert validate_upload(upload) == ".txt"
