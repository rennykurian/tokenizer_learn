# Tokenizer Application

React + TypeScript frontend and FastAPI + Python backend. All tokenizer behavior and
statistics are authoritative in the backend. The Custom Tokenizer vocabulary is held in
process memory and is cleared when the backend process restarts.

## Run locally

Backend (Python 3.11+):

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend (Node.js 20+):

```powershell
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` only when the backend is hosted somewhere other than
`http://127.0.0.1:8000/api/v1`. Copy `.env.example` to `.env` for backend overrides.
The default upload limit is 10 MiB. Supported Tiktoken encodings are returned by the backend
`/api/v1/encodings` endpoint. Uploaded files are processed in memory and not saved.
The custom vocabulary is shared by requests handled by one backend process and is cleared
when that process restarts; each separate worker process has its own vocabulary.

## Tests

```powershell
cd backend
pytest
```

```powershell
cd frontend
npm test
npm run build
npm run test:e2e
```

Install Playwright Chromium on a new machine with `npx playwright install chromium`.