# crm-rag-eval — RAG Evaluation for CRM & Customer Support

[![PyPI](https://img.shields.io/pypi/v/crm-rag-eval.svg)](https://pypi.org/project/crm-rag-eval/)
[![CI](https://github.com/chitralabs/crm-rag-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/chitralabs/crm-rag-eval/actions)
[![codecov](https://codecov.io/gh/chitralabs/crm-rag-eval/graph/badge.svg)](https://codecov.io/gh/chitralabs/crm-rag-eval)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Downloads](https://img.shields.io/pypi/dm/crm-rag-eval.svg)](https://pypi.org/project/crm-rag-eval/)

**The only RAG evaluation toolkit purpose-built for CRM and customer support AI — with business-risk scoring, 250 synthetic CRM Q&A pairs, and hallucination detection that maps to real operational consequences.**

> ⚠️ **Disclaimer:** This is an independent open-source project created by the author in a personal capacity. It contains no proprietary code, no employer intellectual property, no customer data, and no internal architecture from any organization. All datasets are fully synthetic. Not affiliated with any employer past or present.

---

## The Problem with Generic RAG Evaluation in Customer Support

You've deployed a LangChain or LlamaIndex RAG chatbot to handle customer support. Ragas says your faithfulness score is 0.82. Sounds great — until your chatbot tells a customer:

- *"Yes, you can get a full refund anytime"* — for a non-refundable item
- *"Your SLA guarantees 99.99% uptime"* — when your contract says 99.9%
- *"Go ahead and delete your account"* — without warning about data loss

**Generic RAG evaluators score answers. `crm-rag-eval` scores business risk.**

A hallucinated refund policy isn't just a wrong answer — it's a customer dispute, a chargeback, and a support escalation. `crm-rag-eval` is the first open-source RAG evaluation toolkit that maps LLM hallucinations to CRM operational consequences using a 4-tier business-risk taxonomy.

---

## Why crm-rag-eval vs Ragas, DeepEval, and TruLens?

| Feature | Ragas | DeepEval | TruLens | **crm-rag-eval** |
|---|---|---|---|---|
| Answer relevance | ✅ | ✅ | ✅ | ✅ |
| Groundedness / faithfulness | ✅ | ✅ | ✅ | ✅ |
| Hallucination risk scoring | ✅ | ✅ | ✅ | ✅ |
| **CRM domain synthetic dataset (250 items)** | ❌ | ❌ | ❌ | ✅ |
| **Business-risk scoring (CRITICAL/HIGH/MEDIUM/LOW)** | ❌ | ❌ | ❌ | ✅ |
| **CRM domain escalation rules (billing, SLA, GDPR)** | ❌ | ❌ | ❌ | ✅ |
| **Refund / cancellation / account-action risk detection** | ❌ | ❌ | ❌ | ✅ |
| **No LLM required for core evaluation** | ❌ | ❌ | ❌ | ✅ |
| LangChain integration | ✅ | ✅ | ✅ | ✅ |
| LlamaIndex integration | ✅ | ✅ | ✅ | ✅ |
| Ollama / local LLM support | ❌ | ❌ | ❌ | ✅ |
| Multi-strategy benchmark leaderboard | ❌ | ❌ | ❌ | ✅ |

---

## Installation

```bash
pip install crm-rag-eval
```

Works out of the box with Python 3.9+. No GPU required. No OpenAI key needed for core evaluation.

**Optional integrations:**

```bash
pip install "crm-rag-eval[langchain]"    # LangChain RetrievalQA
pip install "crm-rag-eval[llamaindex]"   # LlamaIndex QueryEngine
pip install "crm-rag-eval[ollama]"       # Ollama local LLM (zero data egress)
```

---

## Quick Start — Evaluate a RAG Response in 60 Seconds

```python
from crm_rag_eval import CRMRagEvaluator, RAGSample

evaluator = CRMRagEvaluator()

results = evaluator.evaluate([
    RAGSample(
        question="Can I get a refund if I cancel my annual subscription?",
        generated_answer="Yes, you can get a full refund at any time, no questions asked.",
        retrieved_contexts=["Annual subscriptions are non-refundable after 30 days."],
        ground_truth_answer="Refunds on annual plans are only available within 30 days of purchase.",
    )
])

print(results.summary())
# crm-rag-eval Summary — 1 samples
#   Avg groundedness    : 0.143       ← Answer not supported by context
#   Avg hallucin. risk  : 0.857       ← High hallucination detected
#   Avg overall score   : 0.241
#   Business risk dist. : {'critical': 1}
#   ⚠️  1 CRITICAL risk response(s) detected — do not serve!

evaluator.report(results, "report.html")   # Color-coded HTML report
```

---

## Business-Risk Scoring — The Core Differentiator

`crm-rag-eval` includes 11 CRM-specific risk rules that map RAG failures to operational consequences:

| Risk Tier | When Triggered | Real-World Consequence |
|---|---|---|
| 🟢 **LOW** | Grounded, complete answer | Safe to serve |
| 🟡 **MEDIUM** | Partial grounding or missing context | May confuse customer, add disclaimer |
| 🔴 **HIGH** | Wrong policy guidance, invented SLA terms | Review before serving, risk of dispute |
| 🚨 **CRITICAL** | Unauthorized financial action, GDPR violation, account deletion guidance | **Do NOT serve — escalate to human agent** |

**CRITICAL triggers include:**
- Hallucinated refund/cancellation policies → unauthorized chargebacks
- Wrong SLA compensation terms → incorrect service credits
- Incorrect account deletion guidance → irreversible data loss
- GDPR deletion confirmation without proper verification

```python
from crm_rag_eval import BusinessRiskScorer, MetricScores

scorer = BusinessRiskScorer()
assessment = scorer.score(metrics, question="Process a refund on my account")

print(assessment.risk_level)          # RiskLevel.CRITICAL
print(assessment.recommended_action)  # "DO NOT serve — escalate to human agent"
print(assessment.triggered_rules)     # ["hallucination_critical", "zero_groundedness_financial"]
```

---

## 250 Synthetic CRM FAQ Dataset

A domain-specific synthetic dataset for benchmarking CRM RAG systems — the first of its kind in open source.

```python
from crm_rag_eval import load_faq_dataset

# All 250 Q&A pairs across 5 CRM domains
faqs = load_faq_dataset()

# Filter by domain
billing_faqs = load_faq_dataset(domains=["billing"])
sla_faqs     = load_faq_dataset(domains=["sla"])

# Filter by business risk level
high_risk = load_faq_dataset(risk_levels=["high", "critical"])

# Filter by difficulty (for staged evaluation)
hard_cases = load_faq_dataset(difficulty="hard")
```

**Dataset coverage:**

| Domain | Items | Risk Profile | Example Questions |
|---|---|---|---|
| `billing` | 50 | low → critical | Duplicate charges, unauthorized billing, refund policies |
| `returns` | 50 | low → high | Damaged goods, international returns, warranty claims |
| `sla` | 50 | high → critical | Uptime guarantees, SLA credits, RTO/RPO, P1 incidents |
| `account_access` | 50 | medium → critical | Ownership transfer, account deletion, API key rotation |
| `product_support` | 50 | low → critical | GDPR deletion, webhook failures, email unsubscribes |

> All data is fully synthetic — fictional company names, fictional policy documents, zero real customer data.

---

## Benchmark Your RAG Stack

Compare BM25, dense retrieval, and hybrid strategies on the CRM FAQ dataset:

```python
from crm_rag_eval.benchmarks.leaderboard import run_benchmark

results = run_benchmark(
    strategies={
        "BM25 (keyword)":      my_bm25_retriever,
        "Dense (OpenAI ada)":  my_dense_retriever,
        "Hybrid BM25+Dense":   my_hybrid_retriever,
        "Reranked (Cohere)":   my_reranked_retriever,
    },
    domains=["billing", "sla", "account_access"],
)

results.print_leaderboard()
# ══════════════════════════════════════════════════════════════
#   crm-rag-eval BENCHMARK LEADERBOARD  (150 samples)
# ══════════════════════════════════════════════════════════════
# 🥇 Reranked (Cohere)      0.847  0.891  0.109  ...
# 🥈 Hybrid BM25+Dense      0.781  0.823  0.177  ...
# 🥉 Dense (OpenAI ada)     0.734  0.762  0.238  ...
# #4 BM25 (keyword)         0.612  0.643  0.357  ...

results.to_markdown("BENCHMARK.md")   # Paste in README or blog post
```

---

## LangChain Integration — Evaluate Your Customer Support Chain

```python
from langchain.chains import RetrievalQA
from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

# Your existing LangChain chain
chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

# Evaluate against CRM FAQ benchmark
faq_items = load_faq_dataset(domains=["billing", "returns"], risk_levels=["high", "critical"])
evaluator = CRMRagEvaluator()

samples = []
for item in faq_items[:20]:
    result = chain.invoke({"query": item.question})
    samples.append(RAGSample(
        question=item.question,
        generated_answer=result["result"],
        retrieved_contexts=[doc.page_content for doc in result["source_documents"]],
        ground_truth_answer=item.answer,
        ground_truth_sources=item.ground_truth_sources,
    ))

report = evaluator.evaluate(samples)
print(report.summary())
evaluator.report(report, "langchain_crm_eval.html")

# Flag CRITICAL responses before they reach customers
for r in report.critical_samples():
    print(f"CRITICAL: {r.sample.question}")
    print(f"  Generated: {r.sample.generated_answer[:80]}")
    print(f"  Action: {r.risk.recommended_action}")
```

See [examples/langchain_example.py](examples/langchain_example.py) for a complete integration.

---

## LlamaIndex Integration

```python
from llama_index.core import VectorStoreIndex
from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

faq_items = load_faq_dataset(domains=["sla"])
samples = []
for item in faq_items[:10]:
    response = query_engine.query(item.question)
    samples.append(RAGSample(
        question=item.question,
        generated_answer=str(response),
        retrieved_contexts=[n.get_content() for n in response.source_nodes],
        ground_truth_answer=item.answer,
    ))

evaluator = CRMRagEvaluator()
report = evaluator.evaluate(samples)
evaluator.report(report, "llamaindex_sla_eval.html")
```

See [examples/llamaindex_example.py](examples/llamaindex_example.py) for a complete integration.

---

## Ollama Integration — Evaluate Local LLMs (No Data Leaves Your Machine)

Privacy-conscious enterprises can evaluate RAG pipelines using fully local inference with Ollama:

```bash
ollama pull llama3
ollama serve
```

```python
from examples.ollama_example import evaluate_ollama_rag

# Runs entirely on your hardware — zero API calls, zero data egress
report = evaluate_ollama_rag(model="llama3", domain="billing", n_samples=20)
print(report.summary())
```

See [examples/ollama_example.py](examples/ollama_example.py) for setup details.

---

## Evaluation Metrics

| Metric | Description | Why it matters for CRM |
|---|---|---|
| `answer_relevance` | Token overlap between question and answer | Off-topic answers frustrate customers |
| `groundedness` | Fraction of answer sentences supported by retrieved context | Ungrounded = hallucinated policy |
| `context_precision` | Fraction of retrieved chunks relevant to the question | Irrelevant chunks = distracted LLM |
| `context_recall` | Fraction of ground-truth answer content in retrieved context | Missing context = incomplete answer |
| `hallucination_risk` | `1 − groundedness` | Direct measure of confabulation risk |
| `source_coverage` | Fraction of ground-truth sources retrieved | Policy gaps = wrong guidance |
| `latency_ms` | Response time in milliseconds | SLA compliance for real-time support |

---

## CLI — Try It in 30 Seconds

```bash
pip install crm-rag-eval

# Run a demo evaluation with 4 CRM scenarios
crm-rag-eval demo

# List available synthetic datasets
crm-rag-eval datasets list

# Preview the billing FAQ dataset
crm-rag-eval datasets show faq --domain billing --limit 5

# Preview high-risk support tickets
crm-rag-eval datasets show tickets --limit 10
```

---

## Support Ticket Dataset

49 synthetic support tickets with resolution steps, covering CRM escalation workflows:

```python
from crm_rag_eval import load_ticket_dataset

# All 49 tickets
tickets = load_ticket_dataset()

# High-priority billing and compliance tickets
critical = load_ticket_dataset(
    categories=["billing", "product_support"],
    priorities=["critical", "high"]
)

for t in critical:
    print(f"[{t.priority.upper()}] {t.subject}")
    print(f"  Risk: {t.risk_level}")
    print(f"  Resolution: {', '.join(t.resolution_steps[:2])}")
```

---

## Use Cases

- **Pre-deployment testing** — catch CRITICAL hallucinations before your support chatbot goes live
- **Retrieval strategy comparison** — benchmark BM25 vs dense vs hybrid on CRM-specific questions
- **Regression testing** — add `crm-rag-eval` to CI/CD to gate every RAG pipeline change
- **SLA compliance** — monitor hallucination rates on SLA-related queries specifically
- **GDPR audit prep** — flag any RAG response that gives incorrect data deletion guidance
- **Vendor evaluation** — compare OpenAI, Anthropic, and Ollama on your CRM domain

---

## Related Projects

- [chitralabs/sheetz](https://github.com/chitralabs/sheetz) — Excel/CSV processing in Java with one line (21⭐ on Maven Central)
- [chitralabs/schemamatch](https://github.com/chitralabs/schemamatch) — Tabular dataset diffing engine (Java)
- [chitralabs/paperstat](https://github.com/chitralabs/paperstat) — Publication-ready statistical comparison tables for IEEE/ACM/Elsevier

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add synthetic FAQ items, new metrics, or integrations.

**Areas where contributions are especially welcome:**
- New CRM domain datasets (e-commerce, healthcare, fintech)
- Additional RAG framework integrations (Haystack, CrewAI, AutoGen)
- LLM-judge metric implementations
- Multi-language FAQ datasets

---

## Citation

If you use crm-rag-eval in research or production, please cite:

```bibtex
@software{crm_rag_eval_2026,
  author  = {Ganesan, Chitrapradha},
  title   = {crm-rag-eval: RAG Evaluation for CRM and Customer Support with Business-Risk Scoring},
  year    = {2026},
  url     = {https://github.com/chitralabs/crm-rag-eval},
  license = {Apache-2.0},
  version = {1.1.0}
}
```

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

© 2026 — Independent open-source project. All datasets are fully synthetic.
Not affiliated with any employer past or present.

---

*Keywords: RAG evaluation, CRM AI, customer support LLM, hallucination detection, LangChain evaluation, LlamaIndex evaluation, RAG hallucination, synthetic dataset, business risk scoring, RAG benchmark, retrieval augmented generation evaluation, CRM chatbot testing, Ragas alternative, DeepEval alternative*
