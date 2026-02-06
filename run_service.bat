@echo off

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting FastAPI Service...
uvicorn app.main:app --reload

pause
