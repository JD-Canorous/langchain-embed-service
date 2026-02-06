from router.smart_router import route_pdf
from extractors.fast_lane import FastLaneExtractor

# Deep lane will be plugged later
# from extractors.deep_lane import DeepLaneExtractor


class ExtractionPipeline:

    def __init__(self):
        self.fast_extractor = FastLaneExtractor()
        # self.deep_extractor = DeepLaneExtractor()

    def run(self, pdf_path):

        # -------- STEP 1 : ROUTER --------
        routing_result = route_pdf(pdf_path)

        document_id = routing_result["document_id"]
        page_routes = routing_result["pages"]

        extracted_pages = []

        # -------- STEP 2 : PAGE EXTRACTION --------
        for page_info in page_routes:

            page_number = page_info["page_number"]
            lane = page_info["lane"]

            if lane == "fast":

                page_result = self.fast_extractor.extract_page(
                    pdf_path,
                    page_number
                )

            else:
                # Placeholder until deep lane implemented
                page_result = {
                    "page_number": page_number,
                    "text": "",
                    "images": [],
                    "metadata": {
                        "lane": "deep",
                        "status": "Deep lane not implemented yet"
                    }
                }

            extracted_pages.append(page_result)

        # -------- STEP 3 : RETURN UNIFIED OUTPUT --------
        return {
            "document_id": document_id,
            "pages": extracted_pages
        }
