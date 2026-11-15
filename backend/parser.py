import io
import re
from typing import Tuple

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

class PDFExtractionError(Exception):
    """Custom exception raised when resume text extraction fails."""
    pass

def validate_pdf_file(filename: str, file_bytes: bytes) -> None:
    """Validates file extension, magic bytes, and size."""
    if not filename.lower().endswith(".pdf"):
        raise PDFExtractionError("Invalid file type. SkillGraph accepts PDF documents only (.pdf).")
    
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        size_mb = round(len(file_bytes) / (1024 * 1024), 2)
        raise PDFExtractionError(f"File size exceeds limit: {size_mb} MB. Maximum allowed size is 5 MB.")
    
    if not file_bytes.startswith(b"%PDF"):
        raise PDFExtractionError("Corrupted or invalid PDF format. Header does not match standard PDF signature.")

def clean_extracted_text(raw_text: str) -> str:
    """Cleans up formatting, excessive whitespaces, and odd control characters."""
    if not raw_text:
        return ""
    text = re.sub(r'[\r\f\v]', '\n', raw_text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_text_from_pdf_bytes(file_bytes: bytes) -> Tuple[str, str]:
    """
    Extracts text from PDF bytes in-memory using pdfplumber with lazy PyMuPDF fallback.
    Returns: (cleaned_text, method_used)
    Raises: PDFExtractionError with descriptive messages for empty or scanned files.
    """
    import pdfplumber

    extracted_text = ""
    method_used = "pdfplumber"

    # Attempt 1: pdfplumber
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages_text = []
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages_text.append(t)
            extracted_text = "\n".join(pages_text)
    except Exception:
        extracted_text = ""

    # Attempt 2: PyMuPDF fallback if pdfplumber yielded empty or failed
    if not extracted_text.strip():
        try:
            import pymupdf as fitz
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            pages_text = []
            for page in doc:
                t = page.get_text()
                if t:
                    pages_text.append(t)
            extracted_text = "\n".join(pages_text)
            method_used = "pymupdf_fallback"
        except Exception:
            pass

    cleaned = clean_extracted_text(extracted_text)

    # Scanned PDF or blank check
    if not cleaned or len(cleaned.strip()) < 40:
        raise PDFExtractionError(
            "No readable text could be extracted from this PDF. It appears to be an image-only or scanned document. "
            "Please upload a text-based PDF or use the 'Paste Resume Text' option below."
        )

    return cleaned, method_used
