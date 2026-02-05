from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
import os
import tempfile


app = FastAPI(title="PDF Complexity Analyzer")


# ---------------- CONFIG ---------------- #
CONFIG = {
    "weights": {
        "text_density": 2,
        "layout_complexity": 3,
        "image_complexity": 3,
        "font_complexity": 2
    },
    "thresholds": {
        "high_text_density": 2000
    }
}


# ---------------- ANALYZER FUNCTION ---------------- #
def analyze_pdf_complexity(file_path, config=CONFIG):

    doc = fitz.open(file_path)

    total_text = 0
    total_images = 0
    total_drawings = 0
    fonts = set()
    pages = doc.page_count

    for page in doc:

        text = page.get_text() or ""
        total_text += len(text)

        total_images += len(page.get_images(full=True))

        total_drawings += len(page.get_drawings())

        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line.get("spans", []):
                        fonts.add(span["font"])

    avg_text_density = total_text / pages if pages else 0

    score = 0
    score += (
        avg_text_density / config["thresholds"]["high_text_density"]
    ) * config["weights"]["text_density"]

    score += total_drawings * config["weights"]["layout_complexity"]
    score += total_images * config["weights"]["image_complexity"]
    score += len(fonts) * config["weights"]["font_complexity"]

    return {
        "pages": pages,
        "total_text_characters": total_text,
        "average_text_density": avg_text_density,
        "image_count": total_images,
        "layout_objects": total_drawings,
        "unique_fonts": len(fonts),
        "complexity_score": round(score, 2)
    }


# ---------------- API ROUTE ---------------- #
@app.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = analyze_pdf_complexity(temp_path)
        return result

    finally:
        os.remove(temp_path)


@app.get("/health")
def health_check():
    return {"status": "ok"}
