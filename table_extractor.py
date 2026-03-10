import camelot
import os

PDF_PATH = "data/source_docs/IMF_Qatar_Report.pdf"
OUTPUT_DIR = "data/processed/tables/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📊 Extracting tables...")

tables = camelot.read_pdf(PDF_PATH, pages="all", flavor="stream")

print(f"✔️ Detected {len(tables)} tables.")

for i, t in enumerate(tables):
    csv_path = f"{OUTPUT_DIR}table_{i+1}.csv"
    t.to_csv(csv_path)
    print(f"💾 Saved: table_{i+1}.csv")

print("\n🎉 Table extraction completed.")