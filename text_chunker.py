import os
from pathlib import Path

RAW_TEXT_FILE = "data/processed/raw_text.txt"
CHUNK_OUTPUT_FILE = "data/processed/text_chunks.txt"

# Chunk size settings
MAX_CHARS = 1200
OVERLAP = 200


def load_raw_text():
    """Load text from raw_text.txt and split into meaningful lines."""
    if not os.path.exists(RAW_TEXT_FILE):
        raise FileNotFoundError(f"Raw text file not found at {RAW_TEXT_FILE}")

    with open(RAW_TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Normalize text: remove excessive blank lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return lines


def create_chunks(lines):
    """Create chunks using line/paragraph-based grouping."""
    chunks = []
    current_chunk = ""

    for line in lines:
        # If adding the next line would exceed max size → save and reset
        if len(current_chunk) + len(line) + 1 > MAX_CHARS:
            chunks.append(current_chunk.strip())

            # overlap logic: take last part of previous chunk
            current_chunk = current_chunk[-OVERLAP:]

        current_chunk += " " + line

    # Append the final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def save_chunks(chunks):
    """Save final chunk list to output file."""
    os.makedirs(Path(CHUNK_OUTPUT_FILE).parent, exist_ok=True)

    with open(CHUNK_OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, start=1):
            f.write(f"\n\n--- CHUNK {i} ---\n")
            f.write(chunk)

    print(f"💾 Saved {len(chunks)} chunks → {CHUNK_OUTPUT_FILE}")


if __name__ == "__main__":
    print("📄 Loading raw text...")
    lines = load_raw_text()

    print("✂️ Creating paragraph-based chunks...")
    chunks = create_chunks(lines)

    print(f"📦 Total Chunks Created: {len(chunks)}")

    save_chunks(chunks)