# crm-rag-eval

[![PyPI](https://img.shields.io/pypi/v/crm-rag-eval.svg)](https://pypi.org/project/crm-rag-eval/)
[![CI](https://github.com/chitralabs/crm-rag-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/chitralabs/crm-rag-eval/actions)
[![codecov](https://codecov.io/gh/chitralabs/crm-rag-eval/graph/badge.svg)](https://codecov.io/gh/chitralabs/crm-rag-eval)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

**Evaluate RAG systems for CRM and customer-support use cases using synthetic datasets and business-risk scoring.**

> ⚠️ **Disclaimer:** This is an independent open-source project created by the author in a personal capacity. It contains no proprietary code, no employer intellectual property, no customer data, and no internal architecture from any organization. All datasets are fully synthetic. Not affiliated with any employer past or present.

---

## Why crm-rag-eval?

Existing RAG evaluation tools (Ragas, DeepEval, TruLens) tell you if an answer is **grounded**. They don't tell you if a wrong answer will cause a customer to receive an **unauthorized refund**, incorrect **SLA terms**, or trigger an **unauthorized account action**.

`crm-rag-eval` fills this gap:

| Feature | Ragas | DeepEval | TruLens | **crm-rag-eval** |
|---|---|---|---|---|
| Answer relevance | ✅ | ✅ | ✅ | ✅ |
| Groundedness / faithfulness | ✅ | ✅ | ✅ | ✅ |
| Hallucination risk | ✅ | ✅ | ✅ | ✅ |
| **CRM synthetic dataset** | ❌ | ❌ | ❌ | ✅ |
| **Business-risk scoring** | ❌ | ❌ | ❌ | ✅ |
| **CRM domain escalation rules** | ❌ | ❌ | ❌ | ✅ |
| **CRITICAL / HIGH / MEDIUM / LOW tiers** | ❌ | ❌ | ❌ | ✅ |
| No LLM required for core evaluation | ❌ | ❌ | ❌ | ✅ |

---

## Installation

```bash
pip install crm-rag-eval
```

---

## Quick Start

```python
from crm_rag_eval import CRMRagEvaluator, RAGSample

evaluator = CRMRagEvaluator()

results = evaluator.evaluate([
    RAGSample(
        question="What is your refund policy?",
        generated_answer="Refunds are available within 30 days for annual plans.",
        retrieved_contexts=["Refunds for unused months are available within 30 days of purchase."],
        ground_truth_answer="Refunds for unused months are available within 30 days of purchase for annual plans.",
    )
])

print(results.summary())
evaluator.report(results, "report.html")
```

### Business-risk output
```
crm-rag-eval Summary — 1 samples
  Avg groundedness    : 0.714
  Avg hallucin. risk  : 0.286
  Avg overall score   : 0.681
  Business risk dist. : {'low': 1}
```

---

## Business-Risk Scoring

The risk scorer maps RAG failures to CRM operational consequences:

| Risk Level | Trigger | Example |
|---|---|---|
| 🟢 **LOW** | Grounded, complete answer | Password reset instructions |
| 🟡 **MEDIUM** | Partially ungrounded or incomplete | Missing some refund conditions |
| 🔴 **HIGH** | Invented policy or wrong guidance | Wrong SLA compensation terms |
| 🚨 **CRITICAL** | Unauthorized financial/account action risk | "Yes, get a full refund anytime" for non-refundable items |

```python
from crm_rag_eval import BusinessRiskScorer, RiskLevel

scorer = BusinessRiskScorer()
# Returns CRITICAL for ungrounded answers on financial questions
assessment = scorer.score(metrics, question="Process a refund on my account")
print(assessment.risk_level)          # RiskLevel.CRITICAL
print(assessment.recommended_action)  # "DO NOT serve — escalate to human agent"
```

---

## Synthetic Datasets

### CRM FAQ Dataset (50 Q&A pairs)
```python
from crm_rag_eval import load_faq_dataset

faqs = load_faq_dataset(domains=["billing", "sla"])
for faq in faqs[:3]:
    print(faq.question, "→", faq.risk_level)
```

Domains: `billing`, `returns`, `sla`, `account_access`, `product_support`

### Support Ticket Dataset (20 tickets)
```python
from crm_rag_eval import load_ticket_dataset

tickets = load_ticket_dataset(priorities=["critical", "high"])
for t in tickets:
    print(t.subject, "→", t.risk_level)
```

---

## CLI

```bash
# Run a demo evaluation
crm-rag-eval demo

# List available datasets
crm-rag-eval datasets list

# Preview FAQ dataset
crm-rag-eval datasets show faq --domain billing --limit 5
```

---

## Integrations

- [LangChain example](examples/langchain_example.py)
- LlamaIndex example *(coming in v1.1)*
- Ollama (local LLM) example *(coming in v1.1)*
- ChromaDB + FAISS benchmark *(coming in v1.1)*

---

## Metrics

| Metric | Description |
|---|---|
| `answer_relevance` | Token overlap between question and answer |
| `groundedness` | Fraction of answer sentences supported by retrieved context |
| `context_precision` | Fraction of retrieved chunks relevant to the question |
| `context_recall` | Fraction of ground-truth answer covered by retrieved context |
| `hallucination_risk` | `1 - groundedness` |
| `source_coverage` | Fraction of ground-truth sources retrieved |
| `latency_ms` | Response latency in milliseconds |

---

## Related Projects

- [chitralabs/schemamatch](https://github.com/chitralabs/schemamatch) — Tabular dataset diff (Java)
- [chitralabs/sheetz](https://github.com/chitralabs/sheetz) — Excel/CSV in Java with one line
- [chitralabs/paperstat](https://github.com/chitralabs/paperstat) — Publication-ready stat tables

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

© 2026 — Independent open-source project. All datasets are synthetic.
