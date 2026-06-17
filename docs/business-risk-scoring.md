# Business-Risk Scoring for CRM RAG Systems

## Why Standard RAG Metrics Are Not Enough for Customer Support

Standard RAG evaluation metrics — faithfulness, answer relevance, context recall — measure whether an LLM response is technically correct. They do not measure whether an incorrect response will cause a **business incident**.

In a customer support context, the same faithfulness score of 0.5 can mean:

| Scenario | Faithfulness | Business Consequence |
|---|---|---|
| Chatbot describes the wrong UI navigation path | 0.5 | Confused user, 1 extra support ticket |
| Chatbot states wrong refund policy | 0.5 | Unauthorized chargeback, finance dispute |
| Chatbot gives wrong SLA credit terms | 0.5 | Contract dispute, potential litigation |
| Chatbot incorrectly confirms GDPR deletion | 0.5 | Regulatory penalty, GDPR breach notification |

`crm-rag-eval` introduces **business-risk scoring** to close this gap.

---

## The Four Risk Tiers

### 🟢 LOW

The answer is grounded and complete. If incorrect, the consequence is minimal — a confused user who asks a follow-up question or checks documentation themselves.

**Examples:** How to navigate the dashboard, how to download an invoice, what file formats are supported for import.

**Recommended action:** Serve the response normally.

### 🟡 MEDIUM

The answer is partially grounded or missing important context. An incorrect response may confuse the customer or lead to a follow-up support ticket, but is unlikely to cause a financial or security incident.

**Examples:** How to set up an automation rule, how to configure email notification preferences, how to segment a contact list.

**Recommended action:** Consider adding a disclaimer ("If you have further questions, contact our support team") or routing to a human agent for sensitive customers.

### 🔴 HIGH

The answer is poorly grounded or contains significant hallucination on a policy-sensitive question. An incorrect response could cause a financial dispute, an access control error, or a customer escalation.

**Examples:** Wrong cancellation policy, incorrect password reset procedure, wrong account-tier permissions.

**Recommended action:** Route to human review before serving. Log the response for audit. Improve retrieval context for this question category.

### 🚨 CRITICAL

The answer is ungrounded or hallucinated on a question with severe business consequences. Serving this response could trigger an unauthorized financial action, a GDPR violation, an account takeover risk, or an irreversible data loss.

**Examples:** Incorrect refund authorization ("yes, full refund anytime"), wrong SLA credit amount, incorrect GDPR deletion confirmation, wrong account ownership transfer procedure.

**Recommended action:** **Do not serve this response.** Escalate to a human agent immediately. Log the failure for RAG pipeline improvement.

---

## The 11 CRM Risk Rules

`crm-rag-eval` evaluates each RAG response against 11 domain-specific rules:

| Rule | Trigger | Risk Tier |
|---|---|---|
| `hallucination_critical` | Hallucination risk > 0.7 on a financial/account question | CRITICAL |
| `zero_groundedness_financial` | Groundedness = 0 on a financial or account-related question | CRITICAL |
| `no_source_coverage_policy` | Source coverage = 0 on a policy/SLA/billing question | CRITICAL |
| `low_groundedness` | Groundedness < 0.4 | HIGH |
| `high_hallucination_risk` | Hallucination risk > 0.5 | HIGH |
| `low_context_recall` | Context recall < 0.3 (critical answer content missing) | HIGH |
| `medium_groundedness` | Groundedness between 0.4 and 0.7 | MEDIUM |
| `low_context_precision` | Context precision < 0.5 (irrelevant chunks retrieved) | MEDIUM |
| `low_answer_relevance` | Answer relevance < 0.3 | MEDIUM |
| `high_latency` | Latency > 2000ms | LOW |
| `partial_source_coverage` | Source coverage between 0.3 and 0.7 | LOW |

---

## High-Stakes Keyword Escalation

For questions containing high-stakes CRM keywords, risk scores are automatically escalated. For example, a question about "refund" or "unauthorized charge" with moderate hallucination risk receives a higher final risk score than the same hallucination rate on a low-stakes question.

**CRITICAL escalation keywords:**
`refund`, `charge`, `unauthorized`, `account deletion`, `delete account`, `transfer ownership`, `gdpr`, `fraud`, `sla breach`, `service credit`, `financial`, `payment`, `bank`, `security`, `locked`, `suspicious`

**HIGH escalation keywords:**
`cancel`, `password`, `login`, `permission`, `role`, `admin`, `billing`, `invoice`, `downtime`, `breach`, `missing refund`, `sla`, `rto`, `rpo`

---

## Customizing Risk Rules

You can add your own domain-specific risk rules:

```python
from crm_rag_eval import BusinessRiskScorer, RiskRule, RiskLevel

custom_rules = [
    RiskRule(
        name="wrong_tier_pricing",
        description="Hallucination on enterprise pricing questions",
        risk_level=RiskLevel.CRITICAL,
        weight=2.0,
    ),
    RiskRule(
        name="wrong_integration_credentials",
        description="Wrong API credential guidance",
        risk_level=RiskLevel.HIGH,
        weight=1.5,
    ),
]

scorer = BusinessRiskScorer(custom_rules=custom_rules)
evaluator = CRMRagEvaluator(custom_risk_rules=custom_rules)
```

---

## Integration with CI/CD

Use business-risk scoring to gate RAG pipeline deployments:

```python
import pytest
from crm_rag_eval import CRMRagEvaluator, load_faq_dataset

def test_no_critical_hallucinations_on_billing():
    """RAG pipeline must not produce CRITICAL responses on billing questions."""
    faq_items = load_faq_dataset(domains=["billing"], risk_levels=["high", "critical"])
    
    samples = [evaluate_with_your_rag(item) for item in faq_items[:20]]
    report = CRMRagEvaluator().evaluate(samples)
    
    critical_count = len(report.critical_samples())
    assert critical_count == 0, (
        f"{critical_count} CRITICAL-risk responses detected on billing questions. "
        f"Review: {[r.sample.question for r in report.critical_samples()]}"
    )
```
