# Contributing to crm-rag-eval

Thank you for your interest in contributing! This document explains how to get started.

> **Note:** All datasets in this project are fully synthetic and must remain so.
> Do not add real customer data, company-specific knowledge bases, or any proprietary content.

---

## Ways to Contribute

- **Expand the synthetic dataset** — add more Q&A pairs, support tickets, or new CRM domains
- **Improve metrics** — add new evaluation metrics or improve existing heuristics
- **Integrations** — add examples for new RAG frameworks (LlamaIndex, Haystack, etc.)
- **Benchmarks** — contribute benchmark results from real retrieval systems
- **Bug fixes** — fix issues or improve test coverage
- **Documentation** — improve the README, docstrings, or add tutorials

---

## Development Setup

```bash
# Clone the repo
git clone https://github.com/chitralabs/crm-rag-eval.git
cd crm-rag-eval

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=crm_rag_eval
```

---

## Adding to the Synthetic Dataset

The FAQ and ticket datasets live in `src/crm_rag_eval/datasets/`. Each entry follows this schema:

```python
{
    "question": "...",
    "answer": "...",
    "keywords": ["keyword1", "keyword2"],
    "risk_level": "low | medium | high | critical",
    "ground_truth_sources": ["fictional_doc_v1.pdf#section1"],
    "difficulty": "easy | medium | hard",
}
```

**Rules for new entries:**
- All content must be fully synthetic — fictional company names, fictional document references
- `ground_truth_sources` should reference plausible-looking policy document names
- `risk_level` must be calibrated to the actual business risk of a wrong answer
- `difficulty` reflects how hard the question is to answer correctly from context

---

## Adding a New Integration

Add your integration example to `examples/`. Follow the pattern in `langchain_example.py`:

1. Accept a retriever/engine as a parameter
2. Load FAQ items from `load_faq_dataset()`
3. Call `CRMRagEvaluator().evaluate(samples)`
4. Call `evaluator.report(report, output_path)` to write HTML output
5. Return the `EvaluationReport`

---

## Pull Request Process

1. Fork the repo and create a branch: `git checkout -b feat/my-improvement`
2. Make your changes with tests
3. Ensure tests pass: `pytest tests/ -v`
4. Ensure coverage stays above 85%: `pytest --cov=crm_rag_eval --cov-fail-under=85`
5. Open a pull request against `develop`

---

## Code Style

- Python 3.9+ compatible
- Type hints on all public functions
- Docstrings on all public classes and functions
- Line length ≤ 100 characters

---

## License

By contributing, you agree that your contributions will be licensed under the
[Apache License 2.0](LICENSE).

This is an independent open-source project. Contributions must not contain
proprietary code, employer IP, or real customer data.
