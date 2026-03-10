import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load secrets from .env if available

DB_DIR = "indexing/vectorstore/"

client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_collection("qatar_chunks")

# Load Sentence Transformer Model
import torch
torch.set_default_device("cpu")

embed_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# Load OpenAI API Key (or other provider later)
api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=api_key)


def retrieve_chunks(query, k=4):
    """Retrieve the top K relevant chunks from vector database."""
    query_embedding = embed_model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results["documents"][0]


def generate_answer(question, context_chunks):
    """Ask an LLM to answer using the retrieved context only."""
    
    context_text = "\n\n---\n".join(context_chunks)

    prompt = f"""
You are an AI assistant answering questions based ONLY on the provided context.

If the answer is not in the context, respond: "The document does not contain enough information."

Context:
{context_text}

Question: {question}

Answer with clear citations like (Chunk 1), (Chunk 2), etc.
"""

    response = llm.chat.completions.create(
        model="gpt-4.1-mini",  # Lightweight but accurate model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    user_question = input("\n💬 Ask a question about the IMF report: ")

    print("\n🔍 Retrieving relevant information...\n")
    retrieved = retrieve_chunks(user_question)

    print("🧠 Generating answer...\n")
    answer = generate_answer(user_question, retrieved)

    print("📌 Answer:\n")
    print(answer)