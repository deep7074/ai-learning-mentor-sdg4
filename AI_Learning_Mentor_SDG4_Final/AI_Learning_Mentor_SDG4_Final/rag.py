import re
from pypdf import PdfReader

def extract_pdf_text(file_bytes):
    import io
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages)

def clean_text(text):
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()

def retrieve_context(query, notes, max_chars=6000):
    if not notes:
        return ""

    terms = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
    scored = []

    for note in notes:
        content = clean_text(note["content"])
        lower = content.lower()
        score = sum(lower.count(term) for term in terms if len(term) > 2)
        scored.append((score, note["filename"], content))

    scored.sort(reverse=True, key=lambda x: x[0])

    chunks = []
    used = 0
    for score, filename, content in scored:
        if not content:
            continue
        snippet = content[: min(2200, max_chars - used)]
        if snippet:
            chunks.append(f"[Source: {filename}]\n{snippet}")
            used += len(snippet)
        if used >= max_chars:
            break

    return "\n\n".join(chunks)
