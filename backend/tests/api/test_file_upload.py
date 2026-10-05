from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_txt_upload_returns_extracted_text():
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("notes.txt", "hello world", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["text"] == "hello world"
    assert response.json()["source_type"] == "txt"


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("notes.docx", b"not supported", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_upload_rejects_oversized_file(monkeypatch):
    from app.core.config import Settings

    monkeypatch.setattr(
        "app.services.file_validation.get_settings", lambda: Settings(max_upload_bytes=4)
    )
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("notes.txt", b"12345", "text/plain")},
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "FILE_TOO_LARGE"


def test_pdf_upload_rejects_invalid_pdf():
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("broken.pdf", b"not a pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_PDF"


def test_pdf_upload_rejects_pdf_without_extractable_text():
    import fitz

    document = fitz.open()
    document.new_page()
    content = document.tobytes()
    document.close()
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("image-only.pdf", content, "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "PDF_NO_TEXT"


def test_pdf_upload_extracts_text():
    import fitz

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "hello from pdf")
    content = document.tobytes()
    document.close()
    response = client.post(
        "/api/v1/files/extract",
        files={"file": ("notes.pdf", content, "application/pdf")},
    )

    assert response.status_code == 200
    assert "hello from pdf" in response.json()["text"]
