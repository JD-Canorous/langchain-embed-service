@echo off
setlocal

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
  call venv\Scripts\activate.bat
) else (
  echo WARNING: venv not found. Running with system Python.
)

echo Starting FastAPI app...
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
