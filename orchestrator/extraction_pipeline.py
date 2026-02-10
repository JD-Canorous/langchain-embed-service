import fitz

from router.smart_router import route_pdf
from extractors.fast_lane import FastLaneExtractor
from extractors.deep_lane import DeepLaneExtractor


class ExtractionPipeline:

    def __init__(self):

        self.fast_extractor = FastLaneExtractor()
        self.deep_extractor = DeepLaneExtractor()

    def run(self, pdf_path):

        lanes = route_pdf(pdf_path)

        doc = fitz.open(pdf_path)

        results = []

        for page_number, lane in lanes.items():

            if lane == "fast_lane":

                page_result = self.fast_extractor.extract_page(
                    pdf_path,
                    page_number
                )

            else:

                # Deep lane works whole document
                page_result = self.deep_extractor.extract_document(pdf_path)

                # Break loop since deep lane handles full doc
                results.append(page_result)
                break

            results.append(page_result)

        return results
