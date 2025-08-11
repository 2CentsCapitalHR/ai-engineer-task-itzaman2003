import os
import requests
import json
from pathlib import Path
from urllib.parse import urlparse
from docx import Document as DocxDocument
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import re

# Links from Data Sources
SOURCE_LINKS = [
    "https://assets.adgm.com/download/assets/adgm-ra-resolution-multiple-incorporate-shareholders-LTD-incorporation-v2.docx/186a12846c3911efa4e6c6223862cd87",
    "https://www.adgm.com/documents/registration-authority/registration-and-incorporation/checklist/private-company-limited-by-guarantee-non-financial-services-20231228.pdf",
    "https://www.adgm.com/legal-framework/guidance-and-policy-statements",
    "https://assets.adgm.com/download/assets/Branch-Non+Financial+Services+20231228.pdf/c5bd08c65a4411efb9d83a701912a93f",
    "https://assets.adgm.com/download/assets/Private+Company+Limited+by+Guarantee+Non-Financial+Services+20231228.pdf/1e6186444b1a11ef94edde7a1988e667",
    "https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract+-+ER+2019+-+Short+Version+(May+2024).docx/33b57a92ecfe11ef97a536cc36767ef8",
    "https://www.adgm.com/documents/office-of-data-protection/templates/adgm-dpr-2021-appropriate-policy-document.pdf",
    "https://www.adgm.com/operating-in-adgm/obligations-of-adgm-registered-entities/annual-filings/annual-accounts",
    "https://www.adgm.com/operating-in-adgm/post-registration-services/letters-and-permits",
    "https://en.adgm.thomsonreuters.com/rulebook/7-company-incorporation-package"
]


SAVE_DIR = Path("data/adgm_sources")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url: str) -> Path:
    parsed = urlparse(url)
    fname = Path(parsed.path).name or "index.html"
    local_path = SAVE_DIR / fname
    if not local_path.exists():
        r = requests.get(url)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)
    return local_path

def extract_text_from_docx(path: Path) -> str:
    doc = DocxDocument(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def extract_text_from_pdf(path: Path) -> str:
    text_parts = []
    pdf = fitz.open(path)
    for page in pdf:
        text_parts.append(page.get_text())
    return "\n".join(text_parts)

def extract_text_from_html(path: Path) -> str:
    with open(path, "rb") as f:
        soup = BeautifulSoup(f, "html.parser")
    for s in soup(["script", "style"]):
        s.extract()
    return re.sub(r"\s+", " ", soup.get_text(separator="\n")).strip()

def chunk_text(text: str, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Process all sources
dataset = []
for url in SOURCE_LINKS:
    try:
        local_path = download_file(url)
        ext = local_path.suffix.lower()

        if ext == ".docx":
            text = extract_text_from_docx(local_path)
        elif ext == ".pdf":
            text = extract_text_from_pdf(local_path)
        elif ext in [".html", ".htm", ""]:
            text = extract_text_from_html(local_path)
        else:
            print(f"Skipping unsupported: {local_path}")
            continue

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            dataset.append({
                "source_url": url,
                "local_file": str(local_path),
                "chunk_id": i,
                "content": chunk
            })
        print(f"Processed {url} → {len(chunks)} chunks")
    except Exception as e:
        print(f"Error with {url}: {e}")

# Save dataset as JSON
with open("adgm_reference_chunks.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"Saved {len(dataset)} chunks to adgm_reference_chunks.json")
