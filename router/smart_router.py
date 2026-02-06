from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
import os
import tempfile
import uuid


app = FastAPI(title="LangChain Embed Service - Smart Router")


# ---------------- CONFIG ---------------- #

CONFIG = {
    "weights": {
        "text_density": 2,
        "layout_complexity": 3,
        "image_complexity": 3,
        "font_complexity": 2
    },
    "thresholds": {
        "high_text_density": 2000,
        "routing_score_threshold": 10   # decide fast vs deep
    }
}


# ---------------- PAGE COMPLEXITY ANALYZER ---------------- #

def analyze_page_complexity(page, config=CONFIG):

    text = page.get_text() or ""
    text_length = len(text)

    images = page.get_images(full=True)
    drawings = page.get_drawings()

    fonts = set()
    page_dict = page.get_text("dict")

    for block in page_dict.get("blocks", []):
        if "lines" in block:
            for line in block["lines"]:
                for span in line.get("spans", []):
                    fonts.add(span["font"])

    # ----- SCORE CALCULATION ----- #

    score = 0

    score += (
        text_length / config["thresholds"]["high_text_density"]
    ) * config["weights"]["text_density"]

    score += len(drawings) * config["weights"]["layout_complexity"]
    score += len(images) * config["weights"]["image_complexity"]
    score += len(fonts) * config["weights"]["font_complexity"]

    score = round(score, 2)

    # ----- ROUTING DECISION ----- #

    lane = (
        "deep"
        if score >= config["thresholds"]["routing_score_threshold"]
        else "fast"
    )

    return {
        "text_characters": text_length,
        "image_count": len(images),
        "layout_objects": len(drawings),
        "unique_fonts": len(fonts),
        "complexity_score": score,
        "lane": lane
    }


# ---------------- DOCUMENT ROUTER ---------------- #

def route_pdf(file_path):

    doc = fitz.open(file_path)
    document_id = str(uuid.uuid4())

    pages = []

    for page_number, page in enumerate(doc):

        page_result = analyze_page_complexity(page)

        pages.append({
            "page_number": page_number + 1,
            **page_result
        })

    return {
        "document_id": document_id,
        "total_pages": len(pages),
        "pages": pages
    }


# ---------------- API ROUTE ---------------- #

@app.post("/route")
async def route_pdf_endpoint(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(await file.read())
        temp_path = temp.name

    try:
        result = route_pdf(temp_path)
        return result

    finally:
        os.remove(temp_path)


# ---------------- HEALTH CHECK ---------------- #

@app.get("/health")
def health_check():
    return {"status": "ok"}
