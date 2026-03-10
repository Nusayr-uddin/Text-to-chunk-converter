from sentence_transformers import SentenceTransformer
import fitz

print("\n--- Testing PDF Loading ---")
try:
    doc = fitz.open("data/source_docs/IMF_Qatar_Report.pdf")
    print(f"PDF loaded successfully with {len(doc)} pages.")
except Exception as e:
    print("PDF not found or error loading PDF:", e)

print("\n--- Testing Embedding Model ---")
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = model.encode("This is a test.")
    print("Embedding generated successfully!")
    print("First 5 values:", emb[:5])
except Exception as e:
    print("Embedding model failed:", e)

print("\n--- Environment looks OK if no errors above ---\n")
