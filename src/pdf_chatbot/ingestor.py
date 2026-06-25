"""Extract text content from PDF files using PyMuPDF."""

from pathlib import Path

import pymupdf


def extract_text(pdf_bytes: bytes) -> str:
    """Return the full text of a PDF given its raw bytes.

    Pages are joined with a double newline so the caller can treat
    the result as a single string.
    """
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n\n".join(pages)


def extract_text_from_path(path: Path) -> str:
    """Convenience wrapper that reads a PDF from a file path."""
    return extract_text(path.read_bytes())
