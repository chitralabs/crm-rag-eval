"""
Ollama integration example for crm-rag-eval.

Evaluates a local RAG pipeline using Ollama for privacy-conscious
enterprise deployments — no data leaves your machine.

Requirements:
    pip install crm-rag-eval ollama chromadb
    ollama pull llama3          # or any model
    ollama serve                # start Ollama server
"""

from __future__ import annotations
import time
from typing import Any, List, Optional


def evaluate_ollama_rag(
    model: str = "llama3",
    domain: Optional[str] = None,
    n_samples: int = 10,
    output_report: str = "ollama_eval_report.html",
) -> "EvaluationReport":
    """
    Run a simple Ollama RAG evaluation against CRM FAQ questions.

    This example uses a naive retrieve-by-keyword approach for demo purposes.
    Replace with a real vector store (ChromaDB, FAISS) for production use.

    Parameters
    ----------
    model         : Ollama model name (e.g., "llama3", "mistral", "gemma2")
    domain        : CRM domain filter
    n_samples     : number of FAQ items to evaluate
    output_report : path for HTML report output
    """
    try:
        import ollama as ollama_client
    except ImportError:
        raise ImportError(
            "ollama is required for this example. Install with: pip install ollama"
        )

    from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

    faq_items = load_faq_dataset(domains=[domain] if domain else None)[:n_samples]
    # Build a naive in-memory knowledge base from the FAQ
    knowledge_base = [{"question": item.question, "answer": item.answer} for item in faq_items]

    samples = []
    for item in faq_items:
        # Naive retrieval: keyword overlap
        scores = []
        q_words = set(item.question.lower().split())
        for kb_item in knowledge_base:
            kb_words = set(kb_item["question"].lower().split())
            scores.append((len(q_words & kb_words), kb_item["answer"]))
        scores.sort(reverse=True)
        top_contexts = [s[1] for s in scores[:3]]

        # Build RAG prompt
        context_str = "\n\n".join(f"Context {i+1}: {c}" for i, c in enumerate(top_contexts))
        prompt = (
            f"You are a helpful CRM support assistant. "
            f"Answer the following question using only the provided context.\n\n"
            f"{context_str}\n\n"
            f"Question: {item.question}\n"
            f"Answer:"
        )

        t0 = time.time()
        try:
            response = ollama_client.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response["message"]["content"].strip()
        except Exception as e:
            answer = f"[Error: {e}]"
        latency_ms = (time.time() - t0) * 1000

        samples.append(RAGSample(
            question=item.question,
            generated_answer=answer,
            retrieved_contexts=top_contexts,
            ground_truth_answer=item.answer,
            ground_truth_sources=item.ground_truth_sources,
            retrieved_source_ids=[],
            latency_ms=latency_ms,
        ))

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples, domains=[domain] * len(samples) if domain else None)
    evaluator.report(report, output_report)
    print(report.summary())
    return report


if __name__ == "__main__":
    print("crm-rag-eval × Ollama integration")
    print("Requires: ollama serve + ollama pull llama3")
    print("Run: python ollama_example.py\n")
    # Uncomment to run:
    # evaluate_ollama_rag(model="llama3", domain="billing", n_samples=5)
    print("Edit and uncomment evaluate_ollama_rag() call above to run with Ollama.")
