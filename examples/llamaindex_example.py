"""
LlamaIndex integration example for crm-rag-eval.

Evaluates a LlamaIndex query engine against the synthetic CRM FAQ dataset.

Requirements:
    pip install crm-rag-eval "crm-rag-eval[llamaindex]"
    export OPENAI_API_KEY=your-key
"""

from __future__ import annotations
import time
from typing import Any, List, Optional


def evaluate_llamaindex_engine(
    query_engine: Any,
    domain: Optional[str] = None,
    n_samples: int = 20,
    output_report: str = "llamaindex_eval_report.html",
) -> "EvaluationReport":
    """
    Evaluate a LlamaIndex query engine against CRM FAQ questions.

    Parameters
    ----------
    query_engine  : LlamaIndex QueryEngine with .query() method
    domain        : CRM domain filter (billing, returns, sla, account_access, product_support)
    n_samples     : number of FAQ items to evaluate
    output_report : path for HTML report output

    Returns
    -------
    EvaluationReport
    """
    from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

    faq_items = load_faq_dataset(domains=[domain] if domain else None)[:n_samples]
    samples = []

    for item in faq_items:
        t0 = time.time()
        try:
            response = query_engine.query(item.question)
            answer = str(response)
            # Extract source nodes if available
            source_nodes = getattr(response, "source_nodes", [])
            contexts = [node.get_content() for node in source_nodes]
            source_ids = [node.node_id for node in source_nodes]
        except Exception as e:
            answer = f"[Error: {e}]"
            contexts, source_ids = [], []
        latency_ms = (time.time() - t0) * 1000

        samples.append(RAGSample(
            question=item.question,
            generated_answer=answer,
            retrieved_contexts=contexts,
            ground_truth_answer=item.answer,
            ground_truth_sources=item.ground_truth_sources,
            retrieved_source_ids=source_ids,
            latency_ms=latency_ms,
        ))

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples, domains=[domain] * len(samples) if domain else None)
    evaluator.report(report, output_report)
    print(report.summary())
    return report


# ---------------------------------------------------------------------------
# Runnable demo (mock — no real LlamaIndex engine)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

    print("crm-rag-eval × LlamaIndex integration demo")
    print("(Uses mock answers — replace with real query_engine.query() in production)\n")

    faq_items = load_faq_dataset(domains=["sla", "billing"])[:5]
    samples = [
        RAGSample(
            question=item.question,
            generated_answer=item.answer,
            retrieved_contexts=[item.answer],
            ground_truth_answer=item.answer,
            ground_truth_sources=item.ground_truth_sources,
            retrieved_source_ids=item.ground_truth_sources,
            latency_ms=300 + i * 80,
        )
        for i, item in enumerate(faq_items)
    ]

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples)
    print(report.summary())
    evaluator.report(report, "llamaindex_demo_report.html")
