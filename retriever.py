import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "indexing/vectorstore/"

def get_collection():
    """Load the Chroma collection containing stored embeddings."""
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_collection("qatar_chunks")


def embed_query(query):
    """Convert query text to embedding vector."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode([query])[0].tolist()


def retrieve_top_k(query, k=3):
    """Retrieve the top K most relevant chunks for the query."""
    print(f"🔍 Searching: '{query}'\n")
    
    collection = get_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    print(f"📌 Top {k} Results:\n")

    for i, (doc, score) in enumerate(zip(documents, distances), start=1):
        print(f"--- Result {i} (Score: {score:.4f}) ---")
        print(doc[:400], "...")  # preview first 400 chars
        print()

    return documents


if __name__ == "__main__":
    # Test the system with a realistic question
    test_query = "What does the IMF say about Qatar's 2024 economic outlook?"
    retrieve_top_k(test_query)