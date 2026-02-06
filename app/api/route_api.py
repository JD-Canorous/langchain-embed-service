from fastapi import APIRouter, UploadFile, File
import tempfile
import os

from orchestrator.extraction_pipeline import ExtractionPipeline

router_api = APIRouter()
pipeline = ExtractionPipeline()


@router_api.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = pipeline.run(temp_path)
        return result

    finally:
        os.remove(temp_path)
