from typing import List, Dict
from pydantic import BaseModel


class PageExtraction(BaseModel):
    page_number: int
    text: str
    images: List[str]
    metadata: Dict


class DocumentExtraction(BaseModel):
    document_id: str
    pages: List[PageExtraction]
