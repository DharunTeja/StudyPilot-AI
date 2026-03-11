import os
import re
from typing import Optional
from PyPDF2 import PdfReader
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None


class DocumentProcessor:
    """Handles extraction and cleaning of text from various input formats."""

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def extract_from_image(file_path: str) -> str:
        """Extract text from an image using OCR."""
        if pytesseract is None:
            raise ImportError(
                "pytesseract is not installed. Install it with: pip install pytesseract"
            )
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from image: {str(e)}")

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """Clean and normalize extracted text."""
        if not raw_text:
            return ""

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', raw_text)

        # Remove special characters that don't add meaning
        text = re.sub(r'[^\w\s.,;:!?\-\'\"()\[\]{}/\\@#$%&*+=<>~`^|]', '', text)

        # Fix sentence spacing
        text = re.sub(r'\.(?=[A-Z])', '. ', text)

        # Remove redundant newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()

    @staticmethod
    def segment_sentences(text: str) -> list:
        """Split text into sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @classmethod
    def process_file(cls, file_path: str, file_type: str) -> str:
        """Process a file based on its type and return cleaned text. Uses Gemini as a strong OCR fallback."""
        raw_text = ""
        try:
            if file_type == "pdf":
                raw_text = cls.extract_from_pdf(file_path)
            elif file_type in ["png", "jpg", "jpeg", "bmp", "tiff", "webp"]:
                # If tesseract is missing, we just rely on Gemini fallback
                try:
                    raw_text = cls.extract_from_image(file_path)
                except:
                    pass
            elif file_type == "txt":
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_text = f.read()
            else:
                pass
        except Exception:
            pass

        # Brilliant Fallback: If PyPDF2/Tesseract failed or were blocked, use Gemini 1.5 Flash File Vision API
        if not raw_text.strip() and file_type in ["pdf", "png", "jpg", "jpeg", "webp"]:
            try:
                import google.generativeai as genai
                from app.config import settings
                import time
                
                genai.configure(api_key=settings.GEMINI_API_KEY)
                
                # Upload to Gemini File API
                uploaded_file = genai.upload_file(file_path)
                
                # Wait briefly for processing (if needed for larger PDFs)
                time.sleep(2)
                
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([
                    "You are a professional OCR engine. Please extract ALL the text from this document accurately. Do not add any introductory or conversational text, just return the raw text you see in the document.",
                    uploaded_file
                ])
                
                raw_text = response.text
                
                # Cleanup Cloud Space
                genai.delete_file(uploaded_file.name)
            except Exception as e:
                print(f"Gemini OCR Fallback failed: {e}")

        return cls.clean_text(raw_text)

    @classmethod
    def process_text(cls, text: str) -> str:
        """Process raw text input and return cleaned text."""
        return cls.clean_text(text)
