# Changelog

All notable changes to crm-rag-eval are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.1.0] - TBD

### Added
- Expanded FAQ dataset from 50 to 250 items (50 per domain)
- `difficulty` field on FAQItem (easy / medium / hard)
- `load_faq_dataset(difficulty=...)` filter parameter
- Benchmark module (`benchmarks/leaderboard.py`) with leaderboard output
- LlamaIndex integration example (`examples/llamaindex_example.py`)
- Ollama (local LLM) integration example (`examples/ollama_example.py`)
- CONTRIBUTING.md and GitHub issue templates
- `.gitignore`

## [1.0.0] - 2026-06-17

### Added
- `CRMRagEvaluator` main public API with `evaluate()` and `report()`
- `MetricsEngine` with 7 metrics: answer_relevance, groundedness,
  context_precision, context_recall, hallucination_risk, source_coverage, latency
- `BusinessRiskScorer` with 4-tier CRM risk taxonomy (LOW/MEDIUM/HIGH/CRITICAL)
  and 11 domain-aware rules with keyword escalation for financial/account queries
- Synthetic FAQ dataset: 50 Q&A pairs across 5 CRM domains
- Synthetic ticket dataset: 20 support tickets with resolution steps
- `HtmlReporter`: self-contained HTML report with color-coded risk tiers
- CLI: `crm-rag-eval demo`, `datasets list`, `datasets show`
- LangChain integration example
- pytest test suite (25 tests, >85% coverage target)
- GitHub Actions CI (Python 3.9–3.12) + PyPI publish workflow (OIDC)
- README with comparison table vs Ragas, DeepEval, TruLens
- LICENSE (Apache 2.0) and disclaimer in README and HTML output

[Unreleased]: https://github.com/chitralabs/crm-rag-eval/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/chitralabs/crm-rag-eval/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/chitralabs/crm-rag-eval/releases/tag/v1.0.0
