"""
LangChain integration example for crm-rag-eval.

Wraps a LangChain RetrievalQA chain and evaluates it against
the synthetic CRM FAQ dataset.

Requirements:
    pip install crm-rag-eval "crm-rag-eval[langchain]"
    export OPENAI_API_KEY=your-key   # or use Ollama for local
"""

from __future__ import annotations
import time
from typing import Any, List, Optional


def evaluate_langchain_chain(
    chain: Any,
    questions: Optional[List[str]] = None,
    domain: Optional[str] = None,
    output_report: str = "langchain_eval_report.html",
) -> "EvaluationReport":
    """
    Evaluate a LangChain RetrievalQA chain against CRM FAQ questions.

    Parameters
    ----------
    chain        : LangChain RetrievalQA or similar chain with .invoke() method
    questions    : questions to evaluate (defaults to FAQ dataset questions)
    domain       : CRM domain filter for FAQ dataset
    output_report: path for HTML report output

    Returns
    -------
    EvaluationReport
    """
    from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

    faq_items = load_faq_dataset(domains=[domain] if domain else None)
    eval_questions = questions or [item.question for item in faq_items[:20]]

    samples = []
    for i, question in enumerate(eval_questions):
        faq = faq_items[i] if i < len(faq_items) else None

        t0 = time.time()
        try:
            result = chain.invoke({"query": question})
            answer = result.get("result", "") if isinstance(result, dict) else str(result)
            source_docs = result.get("source_documents", []) if isinstance(result, dict) else []
        except Exception as e:
            answer = f"[Error: {e}]"
            source_docs = []
        latency_ms = (time.time() - t0) * 1000

        contexts = [doc.page_content for doc in source_docs]
        source_ids = [doc.metadata.get("source", "") for doc in source_docs]

        samples.append(RAGSample(
            question=question,
            generated_answer=answer,
            retrieved_contexts=contexts,
            ground_truth_answer=faq.answer if faq else None,
            ground_truth_sources=faq.ground_truth_sources if faq else [],
            retrieved_source_ids=source_ids,
            latency_ms=latency_ms,
        ))

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples, domains=[domain] * len(samples) if domain else None)
    evaluator.report(report, output_report)
    print(report.summary())
    return report


# ---------------------------------------------------------------------------
# Minimal runnable demo (no real LangChain chain needed)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

    print("crm-rag-eval × LangChain integration demo")
    print("(Uses mock answers — replace with real chain.invoke() in production)\n")

    faq_items = load_faq_dataset(domains=["billing"])[:5]
    samples = [
        RAGSample(
            question=item.question,
            generated_answer=item.answer,  # mock: perfect answer
            retrieved_contexts=[item.answer],
            ground_truth_answer=item.answer,
            ground_truth_sources=item.ground_truth_sources,
            retrieved_source_ids=item.ground_truth_sources,
            latency_ms=400 + i * 50,
        )
        for i, item in enumerate(faq_items)
    ]

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples)
    print(report.summary())
    evaluator.report(report, "langchain_demo_report.html")
