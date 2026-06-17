"""
crm-rag-eval — Evaluate RAG systems for CRM and customer-support use cases
with synthetic datasets and business-risk scoring.

Quick start::

    from crm_rag_eval import CRMRagEvaluator, RAGSample

    evaluator = CRMRagEvaluator()
    results = evaluator.evaluate([
        RAGSample(
            question="What is the refund policy?",
            generated_answer="Refunds are available within 30 days.",
            retrieved_contexts=["Refunds for unused months are available within 30 days."],
        )
    ])
    print(results.summary())

Disclaimer:
    This is an independent open-source project. All datasets are synthetic.
    Not affiliated with any employer past or present.
"""

from .evaluator import CRMRagEvaluator, EvaluationReport, EvaluationResult
from .metrics.engine import RAGSample, MetricScores, MetricsEngine
from .risk.scorer import BusinessRiskScorer, RiskAssessment, RiskLevel, RiskRule
from .datasets.faq import load_faq_dataset, load_faq_as_dicts
from .datasets.tickets import load_ticket_dataset

__version__ = "1.0.0"
__all__ = [
    "CRMRagEvaluator",
    "EvaluationReport",
    "EvaluationResult",
    "RAGSample",
    "MetricScores",
    "MetricsEngine",
    "BusinessRiskScorer",
    "RiskAssessment",
    "RiskLevel",
    "RiskRule",
    "load_faq_dataset",
    "load_faq_as_dicts",
    "load_ticket_dataset",
]
