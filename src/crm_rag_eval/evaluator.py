"""
CRMRagEvaluator — main public API class.

Usage::

    from crm_rag_eval import CRMRagEvaluator, RAGSample

    evaluator = CRMRagEvaluator()

    results = evaluator.evaluate([
        RAGSample(
            question="What is your refund policy?",
            generated_answer="Refunds are available within 30 days.",
            retrieved_contexts=["Refunds for unused months are available within 30 days."],
            ground_truth_answer="Refunds for unused months are available within 30 days of purchase.",
        )
    ])

    evaluator.report(results, "report.html")
    print(results.summary())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict

from .metrics.engine import MetricScores, MetricsEngine, RAGSample
from .risk.scorer import BusinessRiskScorer, RiskAssessment, RiskLevel


@dataclass
class EvaluationResult:
    """Container for the full evaluation output of one sample."""
    sample: RAGSample
    metrics: MetricScores
    risk: RiskAssessment


@dataclass
class EvaluationReport:
    """Aggregated results for a batch evaluation."""
    results: List[EvaluationResult]

    def summary(self) -> str:
        n = len(self.results)
        risk_counts: Dict[str, int] = {}
        for r in self.results:
            k = r.risk.risk_level.value
            risk_counts[k] = risk_counts.get(k, 0) + 1

        avg_ground = sum(r.metrics.groundedness for r in self.results) / max(n, 1)
        avg_hall   = sum(r.metrics.hallucination_risk for r in self.results) / max(n, 1)
        avg_overall= sum(r.metrics.overall_score for r in self.results) / max(n, 1)

        lines = [
            f"crm-rag-eval Summary — {n} samples",
            f"  Avg groundedness    : {avg_ground:.3f}",
            f"  Avg hallucin. risk  : {avg_hall:.3f}",
            f"  Avg overall score   : {avg_overall:.3f}",
            f"  Business risk dist. : {risk_counts}",
        ]
        critical = risk_counts.get("critical", 0)
        high     = risk_counts.get("high", 0)
        if critical > 0:
            lines.append(f"  ⚠️  {critical} CRITICAL risk response(s) detected — do not serve!")
        if high > 0:
            lines.append(f"  ⚠️  {high} HIGH risk response(s) — review before serving.")
        return "\n".join(lines)

    def critical_samples(self) -> List[EvaluationResult]:
        return [r for r in self.results if r.risk.risk_level == RiskLevel.CRITICAL]

    def to_dict(self) -> List[dict]:
        output = []
        for r in self.results:
            output.append({
                "sample_id": r.metrics.sample_id,
                "question": r.sample.question,
                "generated_answer": r.sample.generated_answer,
                "metrics": {
                    "answer_relevance": r.metrics.answer_relevance,
                    "groundedness": r.metrics.groundedness,
                    "context_precision": r.metrics.context_precision,
                    "context_recall": r.metrics.context_recall,
                    "hallucination_risk": r.metrics.hallucination_risk,
                    "source_coverage": r.metrics.source_coverage,
                    "latency_ms": r.metrics.latency_ms,
                    "overall_score": r.metrics.overall_score,
                },
                "risk": {
                    "level": r.risk.risk_level.value,
                    "score": r.risk.risk_score,
                    "triggered_rules": r.risk.triggered_rules,
                    "explanation": r.risk.explanation,
                    "recommended_action": r.risk.recommended_action,
                },
            })
        return output


class CRMRagEvaluator:
    """
    Main evaluator class for crm-rag-eval.

    Parameters
    ----------
    latency_threshold_ms : float
        Latency above which the HIGH_LATENCY rule triggers (default 2000ms).
    custom_risk_rules : list
        Additional risk rules to append to the default rule set.
    """

    def __init__(
        self,
        latency_threshold_ms: float = 2000.0,
        custom_risk_rules: Optional[list] = None,
    ):
        self._metrics = MetricsEngine(latency_threshold_ms=latency_threshold_ms)
        self._risk    = BusinessRiskScorer(custom_rules=custom_risk_rules)

    def evaluate(
        self,
        samples: List[RAGSample],
        questions: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
    ) -> EvaluationReport:
        """
        Evaluate a batch of RAG samples.

        Parameters
        ----------
        samples   : list of RAGSample
        questions : question strings for risk scoring (defaults to sample.question)
        domains   : CRM domain per sample for risk scoring
        """
        metric_scores = self._metrics.evaluate_batch(samples)
        questions_    = questions or [s.question for s in samples]
        risk_scores   = self._risk.score_batch(metric_scores, questions_, domains)

        results = [
            EvaluationResult(sample=s, metrics=m, risk=r)
            for s, m, r in zip(samples, metric_scores, risk_scores)
        ]
        return EvaluationReport(results=results)

    def report(
        self,
        evaluation: EvaluationReport,
        output_path: str,
    ) -> None:
        """Write an HTML evaluation report to output_path."""
        from .formatters.html_report import write_html_report
        write_html_report(
            metric_scores=[r.metrics for r in evaluation.results],
            risk_assessments=[r.risk for r in evaluation.results],
            output_path=output_path,
        )
        print(f"Report written to {output_path}")
