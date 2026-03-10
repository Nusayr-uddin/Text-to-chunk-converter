import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load env variables
load_dotenv()

# Initialize components
DB_DIR = "indexing/vectorstore/"
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_collection("qatar_chunks")

import torch
torch.set_default_device("cpu")

embedder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Qatar IMF Assistant", page_icon="📘")
st.title("📘 Qatar IMF Economic Report Assistant")


def retrieve_chunks(query, k=4):
    embedding = embedder.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return results["documents"][0]


def get_llm_answer(query, chunks):
    context = "\n\n---\n".join(chunks)

    prompt = f"""
Use ONLY the following context to answer the question. 
If unsure, say: "Not enough information in the document."

Context:
{context}

Question: {query}

Provide citations like (Chunk 1), (Chunk 2).
"""

    response = llm.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# UI
query = st.text_input("Ask a question about the report:")

if st.button("Search"):
    if query.strip():
        st.write("⏳ Retrieving information...")
        
        chunks = retrieve_chunks(query)
        
        st.write("🧠 Generating answer...")
        answer = get_llm_answer(query, chunks)
        
        st.success(answer)

        with st.expander("📄 Retrieved Context"):
            for i, c in enumerate(chunks, start=1):
                st.write(f"**Chunk {i}:**")
                st.write(c)
                st.write("---")
    else:
        st.warning("Please enter a question.")