import fitz
import re
import os

PDF_PATH = "data/source_docs/IMF_Qatar_Report.pdf"
OUTPUT_PATH = "data/processed/chart_metadata.txt"

os.makedirs("data/processed/", exist_ok=True)

print("📈 Extracting chart / figure metadata...")

doc = fitz.open(PDF_PATH)
chart_entries = []

caption_pattern = r"(Figure|Chart|Exhibit|Graph|Fig)\s?\d+.*"

for page_num, page in enumerate(doc):
    text = page.get_text()
    matches = re.findall(caption_pattern, text, re.IGNORECASE)

    for match in matches:
        chart_entries.append(f"Page {page_num+1}: {match}")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(chart_entries))

print(f"💾 Saved chart metadata to: {OUTPUT_PATH}")