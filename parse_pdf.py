import fitz
import os

# Path to input PDF
PDF_PATH = "data/source_docs/IMF_Qatar_Report.pdf"

def extract_text_from_pdf(pdf_path):
    """Extracts text from each page in the PDF."""
    doc = fitz.open(pdf_path)
    pages_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages_text.append({"page": page_num+1, "text": text})

    return pages_text

if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF not found: {PDF_PATH}")
    else:
        print("📄 Loading PDF...")
        text_data = extract_text_from_pdf(PDF_PATH)
        print(f"✔️ Successfully extracted text from {len(text_data)} pages.")

        # Save result
        output_file = "data/processed/raw_text.txt"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            for entry in text_data:
                f.write(f"\n\n--- Page {entry['page']} ---\n")
                f.write(entry["text"])

        print(f"💾 Saved extracted text to: {output_file}")