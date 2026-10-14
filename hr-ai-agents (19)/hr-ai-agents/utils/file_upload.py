"""Handle uploaded files (PDF, images, text) for chat."""

from typing import Tuple
import io

SUPPORTED = ["pdf", "txt", "png", "jpg", "jpeg", "webp", "csv", "docx"]


def file_extension(name: str) -> str:
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


def extract_text_from_upload(uploaded_file) -> Tuple[str, str]:
    """
    Returns (extracted_text_or_description, status_message).
    Always tries to return usable text for resume screening.
    """
    name = uploaded_file.name
    ext = file_extension(name)
    data = uploaded_file.read()
    try:
        uploaded_file.seek(0)
    except Exception:
        pass

    if ext in ("txt", "csv", "md", "log"):
        try:
            text = data.decode("utf-8", errors="ignore").strip()
            if not text:
                return "", f"File **{name}** is empty."
            return text[:12000], f"Loaded text from **{name}** ({len(text)} chars)"
        except Exception as e:
            return "", f"Could not read text file: {e}"

    if ext == "pdf":
        # Try real PDF parse first
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            pages = []
            for page in reader.pages[:15]:
                pages.append(page.extract_text() or "")
            text = "\n".join(pages).strip()
            if text:
                return text[:12000], f"Extracted text from PDF **{name}** ({len(reader.pages)} pages)"
            return (
                f"[PDF uploaded: {name}, {len(reader.pages)} page(s). No extractable text — may be scanned.]",
                f"PDF **{name}** has no selectable text (scanned image PDF).",
            )
        except Exception as e:
            # Fallback: maybe bytes are plain text saved as .pdf
            try:
                text = data.decode("utf-8", errors="ignore").strip()
                if len(text) > 50 and not text.startswith("%PDF"):
                    return text[:12000], f"Read **{name}** as text (PDF parse failed: {e})"
            except Exception:
                pass
            return (
                f"[PDF file uploaded: {name}, size {len(data)} bytes. Could not extract text: {e}]",
                f"PDF **{name}** could not be parsed. Try a .txt export or text-based PDF.",
            )

    if ext == "docx":
        try:
            import zipfile
            from xml.etree import ElementTree as ET
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                xml = z.read("word/document.xml")
            tree = ET.fromstring(xml)
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            texts = [n.text for n in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if n.text]
            text = " ".join(texts).strip()
            if text:
                return text[:12000], f"Extracted text from Word **{name}**"
            return "", f"Word file **{name}** had no text."
        except Exception as e:
            return "", f"Could not read Word file: {e}"

    if ext in ("png", "jpg", "jpeg", "webp"):
        return (
            f"[Image uploaded: {name}, size {len(data)} bytes. "
            "This is a photo of a document. For accurate scoring, upload a text PDF or .txt resume.]",
            f"Image **{name}** uploaded. Text cannot be read from photos without OCR — use PDF/TXT for best results.",
        )

    # Unknown extension: try as text
    try:
        text = data.decode("utf-8", errors="ignore").strip()
        if len(text) > 20:
            return text[:12000], f"Loaded **{name}** as text"
    except Exception:
        pass
    return "", f"Unsupported or unreadable file type: .{ext}"


def build_prompt_with_file(user_text: str, file_text: str, filename: str) -> str:
    """Combine user message with extracted file content for the screener."""
    user_text = (user_text or "").strip()
    if not user_text:
        user_text = f"Screen resume for the uploaded file {filename}"
    # Ensure screener keywords are present so tool router picks resume screener
    if "screen" not in user_text.lower() and "resume" not in user_text.lower():
        user_text = f"Screen resume. {user_text}"
    return (
        f"{user_text}\n\n"
        f"--- Uploaded file: {filename} ---\n"
        f"{file_text[:8000]}\n"
        f"--- End of file ---"
    )
