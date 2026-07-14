"""Document text extraction for supported upload types.

Turns uploaded bytes into plain text. PDF parsing imports ``pypdf`` lazily so the
rest of the app (and most tests) don't pull it in. TXT/MD/CSV are decoded as
UTF-8 text — good enough for retrieval over their content.
"""

from __future__ import annotations

from copilot.domain.exceptions import CopilotError

SUPPORTED_EXTENSIONS = {"pdf", "md", "txt", "csv"}


class UnsupportedDocumentError(CopilotError):
    """The uploaded file type cannot be ingested."""


def _extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def load_text(filename: str, data: bytes, content_type: str | None = None) -> str:
    ext = _extension(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedDocumentError(
            f"Unsupported document type {ext!r}. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    if ext == "pdf":
        return _load_pdf(data)
    return data.decode("utf-8", errors="ignore")


def _load_pdf(data: bytes) -> str:
    import io

    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
