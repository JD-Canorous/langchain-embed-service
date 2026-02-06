import fitz
import uuid


class FastLaneExtractor:

    def extract_page(self, pdf_path, page_number):

        doc = fitz.open(pdf_path)
        page = doc[page_number - 1]

        # -------- TEXT --------
        text = page.get_text() or ""

        # -------- IMAGE EXTRACTION --------
        images = []
        image_list = page.get_images(full=True)

        for img in image_list:
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            image_name = f"img_{uuid.uuid4()}.png"
            pix.save(image_name)

            images.append(image_name)

        doc.close()

        return {
            "page_number": page_number,
            "text": text,
            "images": images
        }
