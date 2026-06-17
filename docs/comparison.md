# crm-rag-eval vs Ragas vs DeepEval vs TruLens

## TL;DR

Use **Ragas, DeepEval, or TruLens** when you need general-purpose RAG evaluation across any domain.

Use **crm-rag-eval** when you are building a RAG system for CRM, customer support, billing, SLA management, or account services — and you need to know whether a hallucinated response will cause a business incident, not just a bad user experience.

---

## Detailed Comparison

### Ragas

**Best for:** General RAG evaluation with LLM-as-judge metrics. Strong community, many integrations.

**Limitations for CRM:**
- No domain-specific synthetic datasets for customer support
- Faithfulness score tells you if an answer is grounded — it does not tell you if an ungrounded answer will cause a chargeback
- Requires an LLM (OpenAI, Bedrock, etc.) for most metrics
- No concept of business risk tiers

**When to use alongside crm-rag-eval:** Use Ragas for overall pipeline benchmarking and crm-rag-eval for CRM-domain regression testing.

### DeepEval

**Best for:** Teams who want a structured, assertion-based testing framework for LLM apps with LangChain and LlamaIndex.

**Limitations for CRM:**
- No CRM-specific evaluation dataset
- Metrics are domain-agnostic: wrong refund guidance and wrong navigation guidance receive the same score
- Requires OpenAI API for most metrics

**When to use alongside crm-rag-eval:** Use DeepEval for unit testing of individual RAG components; use crm-rag-eval for end-to-end CRM scenario coverage.

### TruLens

**Best for:** Teams who want deep tracing and observability of LLM pipelines with LangChain (TruChain) or LlamaIndex (TruLlama).

**Limitations for CRM:**
- RAG Triad (groundedness, context relevance, answer relevance) is powerful but domain-agnostic
- No CRM synthetic dataset
- No business-risk escalation rules

**When to use alongside crm-rag-eval:** Use TruLens for pipeline-level observability; use crm-rag-eval for CRM domain regression testing.

---

## Feature Matrix

| | Ragas | DeepEval | TruLens | **crm-rag-eval** |
|---|---|---|---|---|
| Faithfulness / groundedness | ✅ | ✅ | ✅ | ✅ |
| Answer relevance | ✅ | ✅ | ✅ | ✅ |
| Context precision | ✅ | ✅ | ✅ | ✅ |
| Context recall | ✅ | ✅ | ✅ | ✅ |
| Hallucination risk | ✅ | ✅ | ✅ | ✅ |
| **Business-risk scoring** | ❌ | ❌ | ❌ | ✅ |
| **CRM domain dataset** | ❌ | ❌ | ❌ | ✅ |
| **CRITICAL / HIGH / MEDIUM / LOW tiers** | ❌ | ❌ | ❌ | ✅ |
| **Billing / SLA / GDPR escalation rules** | ❌ | ❌ | ❌ | ✅ |
| No LLM required for core evaluation | ❌ | ❌ | ❌ | ✅ |
| LangChain integration | ✅ | ✅ | ✅ | ✅ |
| LlamaIndex integration | ✅ | ✅ | ✅ | ✅ |
| Ollama / local LLM evaluation | ❌ | ❌ | ❌ | ✅ |
| Multi-strategy benchmark leaderboard | ❌ | ❌ | ❌ | ✅ |
| Synthetic CRM FAQ dataset (250 items) | ❌ | ❌ | ❌ | ✅ |
| Support ticket dataset with resolution steps | ❌ | ❌ | ❌ | ✅ |
| CI/CD integration with risk-gating | ❌ | ✅ | ❌ | ✅ |
| License | Apache 2.0 | Apache 2.0 | MIT | Apache 2.0 |

---

## Complementary Usage

`crm-rag-eval` is not a replacement for general RAG evaluation tools — it is a specialization. Many teams use it alongside Ragas or DeepEval:

```python
# Use Ragas for overall quality benchmarking
ragas_scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy])

# Use crm-rag-eval for CRM-specific risk gating
crm_report = CRMRagEvaluator().evaluate(crm_samples)
crm_report.critical_samples()  # Block these from reaching customers
```

See the [Quick Start guide](../README.md#quick-start) for complete usage examples.
