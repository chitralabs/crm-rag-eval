---
annotations_creators:
  - expert-generated
language_creators:
  - expert-generated
language:
  - en
license: apache-2.0
multilinguality:
  - monolingual
size_categories:
  - n<1K
source_datasets:
  - original
task_categories:
  - question-answering
  - text-retrieval
task_ids:
  - extractive-qa
  - open-domain-qa
tags:
  - crm
  - customer-support
  - rag-evaluation
  - synthetic
  - risk-scoring
  - hallucination-detection
pretty_name: CRM RAG Evaluation FAQ Dataset
---

# CRM RAG Evaluation FAQ Dataset

**Part of the [crm-rag-eval](https://github.com/chitralabs/crm-rag-eval) toolkit.**

## Dataset Description

A synthetic CRM FAQ dataset designed for evaluating Retrieval-Augmented Generation (RAG) systems
in customer-support and CRM contexts. Unlike generic QA benchmarks, this dataset annotates each
item with:

- **Business risk level** — `low`, `medium`, `high`, `critical`
- **Ground-truth source documents** — fictional policy document references
- **Difficulty** — `easy`, `medium`, `hard`
- **Keywords** — key terms for retrieval evaluation

> ⚠️ **All data is fully synthetic.** No real customer data, no proprietary content, no real
> company information. Generated for testing RAG evaluation pipelines.

## Dataset Structure

### Data Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique ID (e.g., `faq-BIL-001`) |
| `domain` | string | CRM domain: `billing`, `returns`, `sla`, `account_access`, `product_support` |
| `question` | string | Customer question |
| `answer` | string | Ground-truth answer |
| `keywords` | list[str] | Key terms |
| `risk_level` | string | Business risk: `low`, `medium`, `high`, `critical` |
| `ground_truth_sources` | list[str] | Fictional policy document references |
| `difficulty` | string | Question difficulty: `easy`, `medium`, `hard` |

### Data Splits

| Split | Size |
|---|---|
| All | 250 |

### Domain Distribution

| Domain | Items | Risk Profile |
|---|---|---|
| `billing` | 50 | Mix of low → critical (duplicate charges, unauthorized billing) |
| `returns` | 50 | Mix of low → high (damaged goods, international returns) |
| `sla` | 50 | Mostly high → critical (uptime guarantees, RTO/RPO, SLA credits) |
| `account_access` | 50 | Mix of medium → critical (ownership transfer, account deletion) |
| `product_support` | 50 | Mix of low → critical (GDPR deletion, webhook failures) |

### Risk Level Distribution

| Risk Level | Count | Description |
|---|---|---|
| `low` | ~80 | Safe to answer; wrong answer causes minimal harm |
| `medium` | ~100 | Partial errors may confuse customer |
| `high` | ~55 | Wrong answer may cause financial or access harm |
| `critical` | ~15 | Wrong answer may trigger unauthorized actions, GDPR violations |

## Usage

### With crm-rag-eval (recommended)

```python
from crm_rag_eval import load_faq_dataset, load_faq_as_dicts

# Load all 250 items
items = load_faq_dataset()

# Filter by domain
billing_items = load_faq_dataset(domains=["billing"])

# Filter by risk level
high_risk = load_faq_dataset(risk_levels=["high", "critical"])

# Filter by difficulty
hard_items = load_faq_dataset(difficulty="hard")

# As plain dicts (for serialization)
data = load_faq_as_dicts()
```

### As a benchmark baseline

```python
from crm_rag_eval import CRMRagEvaluator, RAGSample, load_faq_dataset

faq_items = load_faq_dataset(domains=["billing", "sla"])
evaluator = CRMRagEvaluator()

# Evaluate your RAG system
samples = [
    RAGSample(
        question=item.question,
        generated_answer=your_rag.answer(item.question),
        retrieved_contexts=your_rag.retrieve(item.question),
        ground_truth_answer=item.answer,
        ground_truth_sources=item.ground_truth_sources,
    )
    for item in faq_items
]

report = evaluator.evaluate(samples)
print(report.summary())
```

## Dataset Creation

### Curation Rationale

Existing RAG evaluation benchmarks (Natural Questions, TriviaQA, HotpotQA) are designed for
general-purpose QA. They do not capture the business-risk dimension of CRM responses, where
a wrong answer about an SLA, refund, or account action can have real financial and legal
consequences.

This dataset was designed to fill that gap by providing:
1. Domain-specific CRM questions across 5 real-world support categories
2. Business-risk annotations calibrated to CRM operational consequences
3. Ground-truth fictional source document references for source-coverage evaluation

### Source Data

All Q&A pairs were created synthetically by domain experts in CRM and customer support.
No real customer data, internal systems, or proprietary knowledge bases were used.

### Annotations

- `risk_level` is assigned based on the potential business impact of an incorrect RAG response
- `ground_truth_sources` reference fictional policy documents with plausible names and section numbers
- `difficulty` reflects the complexity of answering the question correctly from retrieved context

## Considerations for Using the Data

### Limitations

- All data is synthetic and may not reflect the exact policies of any real company
- The dataset is English-only
- Coverage is limited to the 5 defined CRM domains

### Disclaimer

This dataset was created by the author in a personal capacity. It is not affiliated with any
employer, past or present, and contains no proprietary information.

## Citation

If you use this dataset, please cite the crm-rag-eval toolkit:

```bibtex
@software{crm_rag_eval_2026,
  author = {Ganesan, Chitrapradha},
  title = {crm-rag-eval: CRM RAG Evaluation Toolkit with Business-Risk Scoring},
  year = {2026},
  url = {https://github.com/chitralabs/crm-rag-eval},
  license = {Apache-2.0}
}
```
