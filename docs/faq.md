# Frequently Asked Questions — crm-rag-eval

## What is crm-rag-eval?

`crm-rag-eval` is a Python library for evaluating Retrieval-Augmented Generation (RAG) systems in CRM and customer support contexts. Unlike generic RAG evaluation tools such as Ragas, DeepEval, or TruLens, `crm-rag-eval` adds a **business-risk scoring layer** that maps hallucinations to real operational consequences: unauthorized refunds, incorrect SLA terms, GDPR violations, and account access failures.

## How is crm-rag-eval different from Ragas?

Ragas measures whether an answer is faithful to retrieved context. `crm-rag-eval` takes the next step: it asks *what happens in a CRM context when the answer is wrong?* A hallucinated refund policy is not just a faithfulness failure — it is a potential chargeback, a compliance risk, and a customer support escalation. `crm-rag-eval` scores these consequences using 11 domain-specific rules and a four-tier risk taxonomy (LOW / MEDIUM / HIGH / CRITICAL).

## Do I need an OpenAI API key to use crm-rag-eval?

No. The core evaluation engine uses token-overlap heuristics and requires no external LLM calls. You can run a full evaluation pipeline, including business-risk scoring and HTML report generation, with zero API keys. Optional LLM-judge metrics and Ollama integration are available for more advanced use cases.

## What CRM domains does the synthetic dataset cover?

The 250-item FAQ dataset covers five CRM domains:
- **Billing** — subscription charges, refund policies, invoice disputes, payment failures
- **Returns** — return windows, damaged goods, exchange policies, warranty claims
- **SLA** — uptime guarantees, SLA credits, RTO/RPO, P1 incident response
- **Account Access** — password reset, 2FA, ownership transfer, account deletion
- **Product Support** — webhook failures, GDPR deletion, CSV import, API rate limits

## What is business-risk scoring?

Business-risk scoring is the process of mapping a RAG evaluation failure to a real-world consequence in your business domain. In a CRM context, a wrong answer about a refund policy has very different consequences from a wrong answer about how to enable dark mode. `crm-rag-eval` assigns one of four risk tiers to each evaluated response:

| Tier | Meaning |
|---|---|
| 🟢 LOW | Safe to serve. Minimal consequence if incorrect. |
| 🟡 MEDIUM | Consider adding a disclaimer or human review. |
| 🔴 HIGH | High chance of customer dispute or financial error. Review before serving. |
| 🚨 CRITICAL | Do not serve. Escalate to human agent immediately. |

## Can I use crm-rag-eval with LangChain?

Yes. `crm-rag-eval` has a native LangChain integration. Pass the output of any `RetrievalQA` or `ConversationalRetrievalChain` to `CRMRagEvaluator.evaluate()` and receive full metrics plus business-risk scores. See [examples/langchain_example.py](../examples/langchain_example.py) for a complete working example.

## Can I use crm-rag-eval with LlamaIndex?

Yes. Pass the output of any LlamaIndex `QueryEngine` to `CRMRagEvaluator.evaluate()`. Source nodes from the response are automatically used for context evaluation. See [examples/llamaindex_example.py](../examples/llamaindex_example.py).

## Can I evaluate a local LLM with Ollama?

Yes. The [Ollama integration](../examples/ollama_example.py) allows you to evaluate RAG pipelines built on local models (Llama 3, Mistral, Gemma 2) with zero API calls and zero data leaving your infrastructure. This is useful for privacy-conscious enterprise deployments.

## Is the dataset real customer data?

No. All 250 FAQ items and 49 support tickets are **fully synthetic** — generated programmatically with fictional company names, fictional policy documents, and fictional customer scenarios. No real customer data, no proprietary content, no employer intellectual property is included.

## How do I add crm-rag-eval to my CI/CD pipeline?

Add `crm-rag-eval` as a test dependency and run evaluations as part of your test suite. Fail the build if the hallucination rate on high-risk questions exceeds a threshold:

```python
report = evaluator.evaluate(samples, domains=["billing", "sla"])
critical = len(report.critical_samples())
assert critical == 0, f"{critical} CRITICAL risk responses detected — pipeline blocked"
```

## What Python versions are supported?

Python 3.9, 3.10, 3.11, and 3.12. Tested via GitHub Actions CI on every commit.

## How do I contribute a new CRM domain?

See [CONTRIBUTING.md](../CONTRIBUTING.md). New domains should follow the existing schema: question, answer, keywords, risk_level (low/medium/high/critical), ground_truth_sources (fictional document references), and difficulty (easy/medium/hard).

## Where can I find the changelog?

See [CHANGELOG.md](../CHANGELOG.md) for version history and upgrade notes.
