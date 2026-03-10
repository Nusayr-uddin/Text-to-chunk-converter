import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

CHUNKS_FILE = "data/processed/text_chunks.txt"
DB_DIR = "indexing/vectorstore/"


def load_chunks():
    """Load extracted text chunks from file."""
    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(f"❌ Chunk file not found at: {CHUNKS_FILE}")

    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        content = f.read().split("--- CHUNK ")
        for entry in content[1:]:
            try:
                num, text = entry.split("---\n", 1)
                chunks.append(text.strip())
            except ValueError:
                continue

    print(f"📄 Loaded {len(chunks)} chunks.")
    return chunks


def create_embeddings(chunks):
    """Generate embeddings and store them in ChromaDB."""
    print("🧠 Loading SentenceTransformer embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("📦 Initializing vector database (Chroma)...")
    client = chromadb.PersistentClient(path=DB_DIR)

    # Create or load a collection
    collection = client.get_or_create_collection(
        name="qatar_chunks",
        metadata={"hnsw:space": "cosine"}  # similarity metric
    )

    print("⚙️ Generating embeddings (this may take a minute)...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    print("🧩 Storing embeddings in ChromaDB...")
    for i, (text, emb) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[text],
            embeddings=[emb.tolist()]
        )

    print(f"💾 Embeddings successfully stored in: {DB_DIR}")


if __name__ == "__main__":
    print("🚀 Starting embedding process...")
    chunks = load_chunks()
    create_embeddings(chunks)
    print("✅ Embedding process completed!")

chart_path = "data/processed/chart_metadata.txt"
if os.path.exists(chart_path):
    with open(chart_path, "r", encoding="utf-8") as f:
        chunks.append(f.read())
    print("📈 Included chart metadata in embeddings.")