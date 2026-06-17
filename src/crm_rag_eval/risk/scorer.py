"""
CRM Business-Risk Scorer — the core differentiator of crm-rag-eval.

Maps RAG evaluation failures to real operational consequences in CRM
and customer-support contexts.

Risk tiers:
  LOW      — grounded, complete, correct answer
  MEDIUM   — incomplete or partially ungrounded answer
  HIGH     — invented policy, wrong guidance, wrong SLA terms
  CRITICAL — unauthorized financial action, account takeover risk,
             GDPR violation, or wrong refund/cancellation instruction
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict

from ..metrics.engine import MetricScores


class RiskLevel(str, Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessment:
    """Business-risk assessment for a single RAG response."""

    sample_id: str
    risk_level: RiskLevel
    risk_score: float          # 0.0 (no risk) – 1.0 (max risk)
    triggered_rules: List[str]
    explanation: str
    recommended_action: str


# ---------------------------------------------------------------------------
# Risk rules — each rule is a named check with a threshold
# ---------------------------------------------------------------------------

@dataclass
class RiskRule:
    name: str
    description: str
    risk_level: RiskLevel
    weight: float = 1.0


_RULES: List[RiskRule] = [
    # CRITICAL rules
    RiskRule(
        name="hallucination_critical",
        description="Hallucination risk > 0.7 — answer likely contains invented content",
        risk_level=RiskLevel.CRITICAL,
        weight=2.0,
    ),
    RiskRule(
        name="zero_groundedness_financial",
        description="Groundedness = 0 and question is financial/account-related",
        risk_level=RiskLevel.CRITICAL,
        weight=2.0,
    ),
    RiskRule(
        name="no_source_coverage_policy",
        description="Source coverage = 0 for a policy/SLA/billing question",
        risk_level=RiskLevel.CRITICAL,
        weight=2.0,
    ),

    # HIGH rules
    RiskRule(
        name="low_groundedness",
        description="Groundedness < 0.4 — answer likely ungrounded",
        risk_level=RiskLevel.HIGH,
        weight=1.5,
    ),
    RiskRule(
        name="high_hallucination_risk",
        description="Hallucination risk > 0.5",
        risk_level=RiskLevel.HIGH,
        weight=1.5,
    ),
    RiskRule(
        name="low_context_recall",
        description="Context recall < 0.3 — critical answer content missing from retrieval",
        risk_level=RiskLevel.HIGH,
        weight=1.0,
    ),

    # MEDIUM rules
    RiskRule(
        name="medium_groundedness",
        description="Groundedness between 0.4 and 0.7 — partial grounding",
        risk_level=RiskLevel.MEDIUM,
        weight=1.0,
    ),
    RiskRule(
        name="low_context_precision",
        description="Context precision < 0.5 — irrelevant chunks retrieved",
        risk_level=RiskLevel.MEDIUM,
        weight=0.75,
    ),
    RiskRule(
        name="low_answer_relevance",
        description="Answer relevance < 0.3 — answer may not address the question",
        risk_level=RiskLevel.MEDIUM,
        weight=0.75,
    ),

    # LOW (informational only)
    RiskRule(
        name="high_latency",
        description="Latency > 2000ms — response may be slow for SLA requirements",
        risk_level=RiskLevel.LOW,
        weight=0.25,
    ),
    RiskRule(
        name="partial_source_coverage",
        description="Source coverage between 0.3 and 0.7 — not all relevant sources retrieved",
        risk_level=RiskLevel.LOW,
        weight=0.5,
    ),
]

# Map CRM domains to elevated risk categories
_HIGH_STAKES_KEYWORDS = {
    "critical": [
        "refund", "charge", "unauthorized", "account deletion", "delete account",
        "transfer ownership", "gdpr", "fraud", "sla breach", "service credit",
        "financial", "payment", "bank", "security", "locked", "suspicious",
    ],
    "high": [
        "cancel", "password", "login", "permission", "role", "admin",
        "billing", "invoice", "downtime", "breach", "missing refund",
        "sla", "rto", "rpo",
    ],
}


class BusinessRiskScorer:
    """
    Scores the business risk of a RAG response in a CRM context.

    Usage::

        scorer = BusinessRiskScorer()
        assessment = scorer.score(metric_scores, question="What is my refund policy?")
    """

    def __init__(self, custom_rules: Optional[List[RiskRule]] = None):
        self.rules = _RULES + (custom_rules or [])

    def score(
        self,
        metrics: MetricScores,
        question: str = "",
        domain: Optional[str] = None,
    ) -> RiskAssessment:
        """
        Compute business risk for a single evaluated sample.

        Parameters
        ----------
        metrics  : MetricScores from the metrics engine
        question : original question text (used for keyword-based escalation)
        domain   : CRM domain (billing, returns, sla, account_access, product_support)
        """
        triggered: List[RiskRule] = []
        q_lower = question.lower()

        # Evaluate each rule
        for rule in self.rules:
            if self._check_rule(rule, metrics, q_lower, domain):
                triggered.append(rule)

        # Determine overall risk level and score
        risk_level, risk_score = self._aggregate_risk(triggered, q_lower)

        return RiskAssessment(
            sample_id=metrics.sample_id,
            risk_level=risk_level,
            risk_score=round(risk_score, 4),
            triggered_rules=[r.name for r in triggered],
            explanation=self._explain(triggered, metrics),
            recommended_action=self._recommend(risk_level, triggered),
        )

    def score_batch(
        self,
        metric_scores: List[MetricScores],
        questions: Optional[List[str]] = None,
        domains: Optional[List[str]] = None,
    ) -> List[RiskAssessment]:
        questions = questions or [""] * len(metric_scores)
        domains   = domains   or [None] * len(metric_scores)
        return [
            self.score(m, q, d)
            for m, q, d in zip(metric_scores, questions, domains)
        ]

    # ------------------------------------------------------------------
    # Rule evaluation
    # ------------------------------------------------------------------

    def _check_rule(
        self,
        rule: RiskRule,
        m: MetricScores,
        q_lower: str,
        domain: Optional[str],
    ) -> bool:
        is_high_stakes_critical = any(kw in q_lower for kw in _HIGH_STAKES_KEYWORDS["critical"])
        is_high_stakes_high     = any(kw in q_lower for kw in _HIGH_STAKES_KEYWORDS["high"])

        if rule.name == "hallucination_critical":
            return m.hallucination_risk > 0.7 and is_high_stakes_critical

        if rule.name == "zero_groundedness_financial":
            return m.groundedness == 0.0 and is_high_stakes_critical

        if rule.name == "no_source_coverage_policy":
            return m.source_coverage == 0.0 and (is_high_stakes_critical or is_high_stakes_high)

        if rule.name == "low_groundedness":
            return m.groundedness < 0.4

        if rule.name == "high_hallucination_risk":
            return m.hallucination_risk > 0.5

        if rule.name == "low_context_recall":
            return m.context_recall is not None and m.context_recall < 0.3

        if rule.name == "medium_groundedness":
            return 0.4 <= m.groundedness < 0.7

        if rule.name == "low_context_precision":
            return m.context_precision < 0.5

        if rule.name == "low_answer_relevance":
            return m.answer_relevance < 0.3

        if rule.name == "high_latency":
            return m.latency_ms is not None and m.latency_ms > 2000

        if rule.name == "partial_source_coverage":
            return 0.3 <= m.source_coverage < 0.7

        return False

    def _aggregate_risk(
        self, triggered: List[RiskRule], q_lower: str
    ) -> tuple[RiskLevel, float]:
        if not triggered:
            return RiskLevel.LOW, 0.05

        # Highest rule level wins
        level_priority = {
            RiskLevel.CRITICAL: 4,
            RiskLevel.HIGH: 3,
            RiskLevel.MEDIUM: 2,
            RiskLevel.LOW: 1,
        }
        max_level = max(triggered, key=lambda r: level_priority[r.risk_level]).risk_level

        # Weighted score
        total_weight = sum(r.weight for r in triggered)
        max_possible = sum(r.weight for r in self.rules)
        score = min(total_weight / max_possible, 1.0)

        # Escalate score for high-stakes questions
        if any(kw in q_lower for kw in _HIGH_STAKES_KEYWORDS["critical"]):
            score = min(score * 1.5, 1.0)

        return max_level, score

    def _explain(self, triggered: List[RiskRule], m: MetricScores) -> str:
        if not triggered:
            return (
                f"Answer appears grounded (groundedness={m.groundedness:.2f}, "
                f"hallucination_risk={m.hallucination_risk:.2f}). No risk rules triggered."
            )
        parts = [r.description for r in triggered]
        return " | ".join(parts)

    def _recommend(self, level: RiskLevel, triggered: List[RiskRule]) -> str:
        if level == RiskLevel.CRITICAL:
            return (
                "DO NOT serve this response to the customer. "
                "Escalate to a human agent immediately. "
                "Review retrieved context and regenerate with additional grounding."
            )
        if level == RiskLevel.HIGH:
            return (
                "Flag for human review before serving. "
                "Improve retrieval: ensure policy documents are indexed and retrieved. "
                "Consider adding a disclaimer to the response."
            )
        if level == RiskLevel.MEDIUM:
            return (
                "Consider adding a disclaimer or directing customer to a human agent. "
                "Review context chunking strategy to improve recall."
            )
        return "Response appears safe to serve. Monitor latency if flagged."
