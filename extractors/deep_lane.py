import boto3
import os
import uuid
import io
from datetime import datetime
from dotenv import load_dotenv
from pdf2image import convert_from_path
from botocore.exceptions import ClientError
from botocore.config import Config

load_dotenv()


class DeepLaneExtractor:

    def __init__(self):
        config = Config(
            retries={'max_attempts': 3, 'mode': 'adaptive'},
            connect_timeout=10,
            read_timeout=60
        )
        
        self.textract = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
            config=config
        )

    def extract_document(self, file_path):
        document_id = str(uuid.uuid4())
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        uploaded_timestamp = datetime.utcnow().isoformat()

        try:
            # Convert PDF to images with explicit poppler_path
            images = convert_from_path(
                file_path,
                poppler_path=r"C:\poppler-25.12.0\Library\bin"
            )
            all_text = []

            # Process each page
            for page_num, image in enumerate(images, 1):
                # Convert image to PNG bytes
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)

                # Send to Textract
                response = self.textract.analyze_document(
                    Document={"Bytes": buffer.getvalue()},
                    FeatureTypes=["LAYOUT"]
                )

                blocks = response.get("Blocks", [])
                page_text = self.extract_text_from_blocks(blocks)
                all_text.append(page_text)

            # Combine all pages
            combined_text = "\n".join(all_text)
            cleaned_text = self.clean_text(combined_text)
            processing_timestamp = datetime.utcnow().isoformat()

            return {
                "document_id": document_id,
                "file_name": file_name,
                "file_size": file_size,
                "processing_lane": "deep_lane",
                "uploaded_timestamp": uploaded_timestamp,
                "processing_timestamp": processing_timestamp,
                "text": cleaned_text,
                "pages_processed": len(images)
            }
        except ClientError as e:
            raise Exception(f"AWS Textract error: {e.response['Error']['Message']}")
        except Exception as e:
            raise Exception(f"Document extraction failed: {str(e)}")

    def extract_text_from_blocks(self, blocks):
        lines = []
        for block in blocks:
            if block["BlockType"] == "LINE":
                lines.append(block["Text"])
        return "\n".join(lines)

    def clean_text(self, text):
        return " ".join(text.split())