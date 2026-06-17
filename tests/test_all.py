"""Tests for crm-rag-eval core components."""

import pytest
from crm_rag_eval import (
    CRMRagEvaluator, RAGSample, load_faq_dataset, load_ticket_dataset,
    BusinessRiskScorer, RiskLevel, MetricsEngine,
)


# ---- Dataset tests -------------------------------------------------------

def test_faq_dataset_loads():
    items = load_faq_dataset()
    assert len(items) == 50
    domains = {item.domain for item in items}
    assert domains == {"billing", "returns", "sla", "account_access", "product_support"}


def test_faq_dataset_filter_by_domain():
    items = load_faq_dataset(domains=["billing"])
    assert all(item.domain == "billing" for item in items)
    assert len(items) == 10


def test_faq_risk_levels_valid():
    items = load_faq_dataset()
    valid = {"low", "medium", "high", "critical"}
    assert all(item.risk_level in valid for item in items)


def test_ticket_dataset_loads():
    tickets = load_ticket_dataset()
    assert len(tickets) > 0


def test_ticket_dataset_filter():
    tickets = load_ticket_dataset(categories=["billing"])
    assert all(t.category == "billing" for t in tickets)


def test_ticket_has_resolution_steps():
    tickets = load_ticket_dataset()
    assert all(len(t.resolution_steps) > 0 for t in tickets)


# ---- Metrics engine tests ------------------------------------------------

def make_sample(**kwargs):
    defaults = dict(
        question="What is the refund policy?",
        generated_answer="Refunds are available within 30 days for annual plans.",
        retrieved_contexts=["Refunds for unused months are available within 30 days of purchase for annual plans."],
        ground_truth_answer="Refunds for unused months are available within 30 days.",
        ground_truth_sources=["refund_policy_v2.pdf#section4"],
        retrieved_source_ids=["refund_policy_v2.pdf#section4"],
        latency_ms=500.0,
    )
    defaults.update(kwargs)
    return RAGSample(**defaults)


def test_metrics_scores_range():
    engine = MetricsEngine()
    sample = make_sample()
    scores = engine.evaluate(sample)
    for attr in ["answer_relevance", "groundedness", "context_precision",
                 "context_recall", "hallucination_risk", "source_coverage"]:
        val = getattr(scores, attr)
        assert 0.0 <= val <= 1.0, f"{attr}={val} out of range"


def test_hallucination_risk_inverse_of_groundedness():
    engine = MetricsEngine()
    sample = make_sample()
    scores = engine.evaluate(sample)
    assert abs(scores.hallucination_risk - (1 - scores.groundedness)) < 0.001


def test_perfect_retrieval_high_scores():
    engine = MetricsEngine()
    sample = make_sample(
        generated_answer="Refunds for unused months are available within 30 days of purchase for annual plans.",
        retrieved_contexts=["Refunds for unused months are available within 30 days of purchase for annual plans."],
    )
    scores = engine.evaluate(sample)
    assert scores.groundedness > 0.5
    assert scores.source_coverage == 1.0


def test_no_context_zero_groundedness():
    engine = MetricsEngine()
    sample = make_sample(retrieved_contexts=[])
    scores = engine.evaluate(sample)
    assert scores.groundedness == 0.0
    assert scores.hallucination_risk == 1.0


def test_overall_score_range():
    engine = MetricsEngine()
    scores = engine.evaluate(make_sample())
    assert 0.0 <= scores.overall_score <= 1.0


# ---- Business risk scorer tests ------------------------------------------

def test_low_risk_for_grounded_answer():
    from crm_rag_eval.metrics.engine import MetricScores
    scorer = BusinessRiskScorer()
    ms = MetricScores(
        sample_id="x", answer_relevance=0.8, groundedness=0.9,
        context_precision=0.85, context_recall=0.9, hallucination_risk=0.1,
        source_coverage=1.0, latency_ms=400,
    )
    result = scorer.score(ms, question="How do I reset my password?")
    assert result.risk_level in (RiskLevel.LOW, RiskLevel.MEDIUM)


def test_critical_risk_for_ungrounded_financial():
    from crm_rag_eval.metrics.engine import MetricScores
    scorer = BusinessRiskScorer()
    ms = MetricScores(
        sample_id="x", answer_relevance=0.2, groundedness=0.0,
        context_precision=0.1, context_recall=0.0, hallucination_risk=1.0,
        source_coverage=0.0, latency_ms=3000,
    )
    result = scorer.score(ms, question="Process an unauthorized refund on my account")
    assert result.risk_level == RiskLevel.CRITICAL


def test_triggered_rules_populated():
    from crm_rag_eval.metrics.engine import MetricScores
    scorer = BusinessRiskScorer()
    ms = MetricScores(
        sample_id="x", answer_relevance=0.1, groundedness=0.1,
        context_precision=0.1, context_recall=0.1, hallucination_risk=0.9,
        source_coverage=0.0, latency_ms=5000,
    )
    result = scorer.score(ms, question="What is the refund policy?")
    assert len(result.triggered_rules) > 0


def test_recommended_action_critical():
    from crm_rag_eval.metrics.engine import MetricScores
    scorer = BusinessRiskScorer()
    ms = MetricScores(
        sample_id="x", answer_relevance=0.0, groundedness=0.0,
        context_precision=0.0, context_recall=0.0, hallucination_risk=1.0,
        source_coverage=0.0, latency_ms=None,
    )
    result = scorer.score(ms, question="Unauthorized charge refund immediately")
    assert "DO NOT" in result.recommended_action or "Escalate" in result.recommended_action


# ---- End-to-end evaluator tests ------------------------------------------

def test_end_to_end_evaluation():
    evaluator = CRMRagEvaluator()
    samples = [make_sample(), make_sample(retrieved_contexts=[])]
    report = evaluator.evaluate(samples)
    assert len(report.results) == 2
    for r in report.results:
        assert r.metrics is not None
        assert r.risk is not None


def test_summary_output():
    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate([make_sample()])
    summary = report.summary()
    assert "crm-rag-eval" in summary
    assert "groundedness" in summary


def test_html_report_writes(tmp_path):
    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate([make_sample()])
    out = str(tmp_path / "report.html")
    evaluator.report(report, out)
    content = open(out).read()
    assert "crm-rag-eval" in content
    assert "<table>" in content


def test_to_dict_structure():
    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate([make_sample()])
    d = report.to_dict()
    assert len(d) == 1
    assert "metrics" in d[0]
    assert "risk" in d[0]
    assert "groundedness" in d[0]["metrics"]
    assert "level" in d[0]["risk"]


def test_critical_samples_filter():
    from crm_rag_eval.metrics.engine import MetricScores
    from crm_rag_eval.risk.scorer import RiskAssessment
    from crm_rag_eval.evaluator import EvaluationResult, EvaluationReport

    critical_risk = RiskAssessment(
        sample_id="x", risk_level=RiskLevel.CRITICAL, risk_score=0.95,
        triggered_rules=["hallucination_critical"],
        explanation="test", recommended_action="escalate",
    )
    low_risk = RiskAssessment(
        sample_id="y", risk_level=RiskLevel.LOW, risk_score=0.05,
        triggered_rules=[], explanation="ok", recommended_action="serve",
    )
    s = make_sample()
    engine = MetricsEngine()
    ms = engine.evaluate(s)
    r1 = EvaluationResult(sample=s, metrics=ms, risk=critical_risk)
    r2 = EvaluationResult(sample=s, metrics=ms, risk=low_risk)
    rpt = EvaluationReport(results=[r1, r2])
    assert len(rpt.critical_samples()) == 1
