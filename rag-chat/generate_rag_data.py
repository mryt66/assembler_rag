import fitz
import re
import json
from pathlib import Path
import sys

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
        for b in blocks:
            text = b[4].strip()
            if text:
                full_text += text + "\n"
    return full_text

def smart_chunking(text):
    sections = re.split(r'\n(?=\d{1,2}[\.\)]\s+[A-Z])', text)
    chunks = []
    for sec in sections:
        paras = re.split(r'\n\s*\n', sec)
        for p in paras:
            clean = p.strip()
            if len(clean) > 100:
                chunks.append(clean)
    return chunks

def make_json_chunks(chunks, filename):
    json_chunks = []
    for chunk in chunks:
        json_chunks.append({
            "content": chunk,
            "source": Path(filename).name,
            "tags": [],
            "type": "unknown"
        })
    return json_chunks

def make_prg_chunk(text, filename):
    return [{
        "content": text.strip(),
        "source": Path(filename).name,
        "tags": [],
        "type": "prg"
    }]

def process_pdf_folder(folder_path):
    folder = Path(folder_path)
    all_chunks = []
    pdfs = list(folder.glob("*.pdf"))
    if not pdfs:
        print(f"No PDF files found in {folder_path}")
        return []
    pdfs.sort(key=lambda x: x.name)
    for pdf_file in pdfs:
        print(f"Processing PDF: {pdf_file.name}")
        raw_text = extract_text_blocks(pdf_file)
        chunks = smart_chunking(raw_text)
        json_chunks = make_json_chunks(chunks, pdf_file.name)
        all_chunks.extend(json_chunks)
    return all_chunks

def process_prg_folder(folder_path):
    folder = Path(folder_path)
    all_chunks = []
    prgs = list(folder.glob("*.prg"))
    if not prgs:
        print(f"No .prg files found in {folder_path}")
        return []
    prgs.sort(key=lambda x: x.name)
    for prg_file in prgs:
        print(f"Processing PRG: {prg_file.name}")
        text = prg_file.read_text(encoding='utf-8', errors='ignore')
        chunk = make_prg_chunk(text, prg_file.name)
        all_chunks.extend(chunk)
    return all_chunks

def main():
    pdf_folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("./data/pdfs")
    prg_folder = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    output_jsonl = "output_chunks.jsonl"

    all_chunks = process_pdf_folder(pdf_folder)
    
    if prg_folder:
        all_chunks += process_prg_folder(prg_folder)

    with open(output_jsonl, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Finished. {len(all_chunks)} total chunks written to {output_jsonl}")

if __name__ == "__main__":
    main()
