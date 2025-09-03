# app/utils/pdf.py
from io import BytesIO
import fitz  # PyMuPDF
import httpx

async def get_pdf_from_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()  # Raise exception if failed
        return response.content

async def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts and returns text from a PDF file represented as bytes.

    Args:
        file_bytes (bytes): The PDF file content in bytes.

    Returns:
        str: Extracted text from the PDF.
    """
    try:
        with fitz.open(stream=BytesIO(file_bytes), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        # Optional: handle specific error logging here
        print(f"Error extracting PDF text: {e}")
        return ""


# import fitz  # PyMuPDF
# from typing import Union

# def extract_text_from_pdf(file_path_or_file) -> str:
#     """
#     Extracts and returns text content from a PDF.
    
#     Args:
#         file_path_or_file (str or file-like): Path to PDF file or a Django InMemoryUploadedFile object.
    
#     Returns:
#         str: Extracted text from the PDF.
#     """
#     text = ""

#     # Check if input is a file-like object (e.g., from Django)
#     if hasattr(file_path_or_file, "read"):
#         doc = fitz.open(stream=file_path_or_file.read(), filetype="pdf")
#     else:
#         doc = fitz.open(file_path_or_file)

#     for page in doc:
#         text += page.get_text()
#     doc.close()

#     return text.strip()
