import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qa.generator import retrieve_chunks as retrieve_relevant_chunks
from qa.generator import generate_answer as generate_response
import time
import json
import json
import os

RESULTS_PATH = "evaluation/results.json"

def evaluate_query(query, ground_truth=None):
    result = {"query": query}

    # ⏱ Measure Retrieval
    t0 = time.time()
    chunks = retrieve_relevant_chunks(query)
    retrieval_time = time.time() - t0

    # ⏱ Measure Generation
    t1 = time.time()
    answer = generate_response(query, chunks)
    generation_time = time.time() - t1

    # 📊 Metrics
    result["retrieval_time_seconds"] = round(retrieval_time, 3)
    result["generation_time_seconds"] = round(generation_time, 3)
    result["total_latency_seconds"] = round(retrieval_time + generation_time, 3)
    result["retrieved_chunks"] = len(chunks)
    result["answer"] = answer

    # 📌 Scoring System
    result["citation_present"] = int("Chunk" in answer or "Page" in answer)
    result["completeness"] = int(len(answer.split()) > 10)
    result["faithfulness"] = int("Not enough information" not in answer)

    # Relevance score based on shared keywords
    relevance = sum(word.lower() in " ".join(chunks).lower() for word in query.split())
    result["context_relevance"] = min(relevance / 5, 1)  # normalized 0–1

    # Final score
    result["final_score"] = round(
        (result["citation_present"] +
         result["completeness"] +
         result["faithfulness"] +
         result["context_relevance"]) / 4, 2
    )

    return result


def evaluate_batch(queries):
    results = [evaluate_query(q) for q in queries]

    os.makedirs(os.path.dirname(RESULTS_PATH), exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=4)

    return results


if __name__ == "__main__":
    SAMPLE_QUERIES = [
        "What is Qatar's GDP forecast?",
        "Which table lists fiscal balance?",
        "What does the inflation chart show?",
        "What does Figure 2 refer to?"
    ]

    print("\n🧪 Running Custom RAG Evaluation...\n")
    results = evaluate_batch(SAMPLE_QUERIES)

    for r in results:
        print(f"❓ {r['query']}")
        print(f"⭐ Score: {r['final_score']} / 1.0")
        print(f"⏱ Latency: {r['total_latency_seconds']} sec\n")