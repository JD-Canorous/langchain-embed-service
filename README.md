# PDF Complexity Analyzer (API)

This repository provides a FastAPI-based HTTP API for analyzing PDF document
complexity. The analysis includes text density, layout complexity, image
count, and unique fonts used.

## Features

- POST `/analyze` — Upload a PDF (multipart/form-data) and receive the
  complexity metrics as JSON.
- GET `/health` — Simple health/readiness check.

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS / Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run (development)

Start the API server with `uvicorn`:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive docs at `http://127.0.0.1:8000/docs`.

## API

- `POST /analyze` — multipart file upload with form field `file`. Returns JSON:

  - `pages`, `total_text_characters`, `average_text_density`,
    `image_count`, `layout_objects`, `unique_fonts`, `complexity_score`

- `GET /health` — returns `{ "status": "ok" }`.

## Notes

- The analyzer uses PyMuPDF (`fitz`) for parsing PDFs. If installation of
  `pymupdf` fails (build tools required on some platforms), consider using a
  pre-built wheel or switching to `pdfplumber`.
- This repo is API-only; the previous Flask-based UI was removed — the
  `templates/` folder is no longer used.

## File Structure (important files)

```
├── app.py              # FastAPI application + analyzer
├── requirements.txt    # Python dependencies
├── samplepdf.pdf       # Example PDF used for testing
```
