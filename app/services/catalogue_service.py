"""Service for processing catalogue data."""

import io
import json
import logging

import pytesseract
from fastapi import UploadFile  # Added import
from openai import OpenAI
from PIL import Image

from app.core import database
from app.core.config import settings

# Set Tesseract path (split to avoid E501)
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust if different
)

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class CatalogueService:
    """Handles catalogue processing and database operations."""

    @staticmethod
    def extract_text_from_image(file):
        """Extract text from an uploaded image using Tesseract OCR."""
        try:
            image = Image.open(io.BytesIO(file))
            text = pytesseract.image_to_string(image)
            logger.info(f"Extracted text from image: {text[:100]}...")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            raise

    @staticmethod
    def convert_text_to_specs_and_id(text):
        """Convert raw text to structured JSON specs and extract product ID using OpenAI."""
        prompt = (
            "You are an expert in extracting product information from text. "
            "Given the following text extracted from a catalogue or image, "
            "identify the product ID (e.g., model name or identifier) and "
            "convert the specifications into a structured JSON format.\n\n"
            "Include keys like 'cpu', 'ram', 'storage', 'display', 'camera', etc., "
            "where applicable. If a specification is missing, omit it from the JSON.\n\n"
            "Return a JSON object with 'product_id' and 'specifications' keys.\n\n"
            f"Text: {text}\n\n"
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI that extracts structured data."},
                    {"role": "user", "content": prompt},
                ],
            )
            json_str = response.choices[0].message.content.strip()
            if json_str.startswith("```json") and json_str.endswith("```"):
                json_str = json_str[7:-3].strip()
            result = json.loads(json_str)
            if "product_id" not in result or "specifications" not in result:
                raise ValueError("OpenAI response missing 'product_id' or 'specifications'")
            logger.info(
                f"Extracted product_id: {result['product_id']}, specs: {result['specifications']}"
            )
            return result["product_id"], result["specifications"]
        except Exception as e:
            logger.error(f"Error converting text to JSON specs and ID: {e}")
            raise

    @staticmethod
    async def process_catalogue(file: UploadFile, product_category_name: str):
        """Process catalogue/image, extract product ID and specs, and insert into products table."""
        try:
            text = CatalogueService.extract_text_from_image(file.file.read())
            product_id, specs = CatalogueService.convert_text_to_specs_and_id(text)

            with database.get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT product_id FROM products WHERE product_id = ?",
                    (product_id,),
                )
                if cursor.fetchone():
                    cursor.execute(
                        "UPDATE products SET specifications = ? WHERE product_id = ?",
                        (json.dumps(specs), product_id),
                    )
                else:
                    cursor.execute(
                        "INSERT INTO products (product_id, product_category_name, specifications) "
                        "VALUES (?, ?, ?)",
                        (product_id, product_category_name, json.dumps(specs)),
                    )
                conn.commit()
                logger.info(f"Inserted/Updated product {product_id} with specs")
            return {
                "status": "success",
                "product_id": product_id,
                "specifications": specs,
            }
        except Exception as e:
            logger.error(f"Error processing catalogue: {e}")
            raise
