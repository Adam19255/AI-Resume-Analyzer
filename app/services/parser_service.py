import fitz  # PyMuPDF
import docx
import re

async def parse_resume_file(file):
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        text = _parse_pdf(content)
    elif file.filename.lower().endswith(".docx"):
        text = _parse_docx(content)
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
    # Returns normalized text (whitespace cleanup, etc.).
    return clean_text(text)

def _parse_pdf(content):
    with fitz.open(stream=content, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)

def _parse_docx(content):
    with open("temp.docx", "wb") as f:
        f.write(content)
    d = docx.Document("temp.docx")
    return "\n".join(p.text for p in d.paragraphs)

def clean_text(t):
    t = re.sub(r'\s+', ' ', t)
    return t.strip()
