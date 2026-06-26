"""Extract text content from PDF files using PyMuPDF."""

from pathlib import Path

import pymupdf


class PDFResult:
    """Extraction result holding the full text and page count."""

    __slots__ = ("text", "page_count")

    def __init__(self, text: str, page_count: int) -> None:
        self.text = text
        self.page_count = page_count


def extract_text(pdf_bytes: bytes) -> PDFResult:
    """Return the full text and page count of a PDF given its raw bytes.

    Pages are joined with a double newline so the caller can treat
    the text as a single string.
    """
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = [page.get_text() for page in doc]
    page_count = doc.page_count
    doc.close()
    return PDFResult(text="\n\n".join(pages), page_count=page_count)


def extract_text_from_path(path: Path) -> PDFResult:
    """Convenience wrapper that reads a PDF from a file path."""
    return extract_text(path.read_bytes())
