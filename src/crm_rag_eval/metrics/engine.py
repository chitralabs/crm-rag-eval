"""
RAG evaluation metrics for CRM use cases.

Metrics implemented (no LLM dependency for core scoring):
  - answer_relevance      : semantic overlap between question and answer
  - groundedness          : answer claims supported by retrieved context
  - context_precision     : fraction of retrieved chunks that are relevant
  - context_recall        : fraction of ground-truth sources retrieved
  - hallucination_risk    : inverse of groundedness (0=no risk, 1=high risk)
  - source_coverage       : how many ground-truth sources were retrieved
  - latency               : response time in milliseconds
"""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class RAGSample:
    """One evaluation sample: a question + RAG pipeline output."""

    question: str
    generated_answer: str
    retrieved_contexts: List[str]          # text of retrieved chunks
    ground_truth_answer: Optional[str] = None
    ground_truth_sources: List[str] = field(default_factory=list)
    retrieved_source_ids: List[str] = field(default_factory=list)
    latency_ms: Optional[float] = None


@dataclass
class MetricScores:
    """Scores for a single RAG sample across all metrics."""

    sample_id: str
    answer_relevance: float      # 0–1
    groundedness: float          # 0–1
    context_precision: float     # 0–1
    context_recall: float        # 0–1
    hallucination_risk: float    # 0–1 (higher = more risky)
    source_coverage: float       # 0–1
    latency_ms: Optional[float]

    @property
    def overall_score(self) -> float:
        """Weighted composite score (higher = better)."""
        weights = {
            "answer_relevance": 0.25,
            "groundedness": 0.30,
            "context_precision": 0.15,
            "context_recall": 0.15,
            "source_coverage": 0.15,
        }
        return (
            self.answer_relevance   * weights["answer_relevance"]
            + self.groundedness     * weights["groundedness"]
            + self.context_precision * weights["context_precision"]
            + self.context_recall   * weights["context_recall"]
            + self.source_coverage  * weights["source_coverage"]
        )


class MetricsEngine:
    """
    Computes RAG evaluation metrics without requiring an LLM.

    Uses token-overlap heuristics for semantic similarity.
    For production use, swap in an LLM judge by subclassing and
    overriding ``_semantic_similarity``.
    """

    def __init__(self, latency_threshold_ms: float = 2000.0):
        self.latency_threshold_ms = latency_threshold_ms

    def evaluate(self, sample: RAGSample, sample_id: str = "sample") -> MetricScores:
        ar  = self._answer_relevance(sample)
        grd = self._groundedness(sample)
        cp  = self._context_precision(sample)
        cr  = self._context_recall(sample)
        sc  = self._source_coverage(sample)

        return MetricScores(
            sample_id=sample_id,
            answer_relevance=ar,
            groundedness=grd,
            context_precision=cp,
            context_recall=cr,
            hallucination_risk=round(1.0 - grd, 4),
            source_coverage=sc,
            latency_ms=sample.latency_ms,
        )

    def evaluate_batch(self, samples: List[RAGSample]) -> List[MetricScores]:
        return [self.evaluate(s, f"sample-{i+1:04d}") for i, s in enumerate(samples)]

    # ------------------------------------------------------------------
    # Individual metrics
    # ------------------------------------------------------------------

    def _answer_relevance(self, sample: RAGSample) -> float:
        """Token overlap between question keywords and answer."""
        q_tokens = self._tokenize(sample.question)
        a_tokens = self._tokenize(sample.generated_answer)
        return self._jaccard(q_tokens, a_tokens)

    def _groundedness(self, sample: RAGSample) -> float:
        """Fraction of answer sentences that are supported by at least one context chunk."""
        sentences = self._split_sentences(sample.generated_answer)
        if not sentences:
            return 0.0
        if not sample.retrieved_contexts:
            return 0.0

        all_context = " ".join(sample.retrieved_contexts).lower()
        supported = 0
        for sent in sentences:
            sent_tokens = self._tokenize(sent)
            ctx_tokens  = self._tokenize(all_context)
            overlap = len(sent_tokens & ctx_tokens) / max(len(sent_tokens), 1)
            if overlap >= 0.3:
                supported += 1

        return round(supported / len(sentences), 4)

    def _context_precision(self, sample: RAGSample) -> float:
        """Fraction of retrieved contexts that are relevant to the question."""
        if not sample.retrieved_contexts:
            return 0.0
        q_tokens = self._tokenize(sample.question)
        relevant = sum(
            1 for ctx in sample.retrieved_contexts
            if self._jaccard(q_tokens, self._tokenize(ctx)) >= 0.1
        )
        return round(relevant / len(sample.retrieved_contexts), 4)

    def _context_recall(self, sample: RAGSample) -> float:
        """Fraction of ground-truth answer content covered by retrieved contexts."""
        if not sample.ground_truth_answer:
            return 1.0   # can't penalise without ground truth
        gt_tokens  = self._tokenize(sample.ground_truth_answer)
        ctx_tokens = self._tokenize(" ".join(sample.retrieved_contexts))
        if not gt_tokens:
            return 1.0
        covered = len(gt_tokens & ctx_tokens) / len(gt_tokens)
        return round(covered, 4)

    def _source_coverage(self, sample: RAGSample) -> float:
        """Fraction of known ground-truth sources that were retrieved."""
        if not sample.ground_truth_sources:
            return 1.0
        retrieved = set(sample.retrieved_source_ids)
        covered = sum(1 for s in sample.ground_truth_sources if s in retrieved)
        return round(covered / len(sample.ground_truth_sources), 4)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> set:
        stopwords = {
            "the","a","an","is","it","in","on","at","to","of","and","or",
            "for","with","my","i","we","you","this","that","was","are","be",
            "have","do","not","can","will","your","our","their",
        }
        tokens = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
        return {t for t in tokens if t not in stopwords and len(t) > 2}

    @staticmethod
    def _jaccard(a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        return round(len(a & b) / len(a | b), 4)

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
