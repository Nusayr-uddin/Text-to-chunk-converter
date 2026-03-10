import os
import pandas as pd

TABLE_DIR = "data/processed/tables/"
OUTPUT = "data/processed/table_text.txt"

print("🔄 Converting tables to formatted text...")

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

table_text = []

for file in os.listdir(TABLE_DIR):
    if file.endswith(".csv"):
        file_path = os.path.join(TABLE_DIR, file)

        try:
            df = pd.read_csv(file_path)

            formatted = f"\n--- Extracted Table: {file} ---\n"
            formatted += df.to_string(index=False)

            table_text.append(formatted)

            print(f"📄 Processed {file}")

        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")

# Save text
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n\n".join(table_text))

print(f"\n💾 Saved table text to: {OUTPUT}")