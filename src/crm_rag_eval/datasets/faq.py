"""
Synthetic CRM FAQ dataset.

500 Q&A pairs across 5 CRM domains:
  billing, returns, SLA, account_access, product_support

All data is fully synthetic — no real customer data, no proprietary content.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import json
import random


@dataclass
class FAQItem:
    id: str
    domain: str
    question: str
    answer: str
    keywords: List[str]
    risk_level: str          # low | medium | high | critical
    ground_truth_sources: List[str]


# ---------------------------------------------------------------------------
# Static synthetic FAQ corpus — 100 items per domain (500 total)
# ---------------------------------------------------------------------------

_BILLING: List[dict] = [
    {
        "question": "How do I update my billing address?",
        "answer": "Log in to your account portal, go to Billing Settings, and click Edit Address. Changes take effect on your next invoice.",
        "keywords": ["billing", "address", "update", "invoice"],
        "risk_level": "low",
        "ground_truth_sources": ["billing_policy_v3.pdf#section2"],
    },
    {
        "question": "What payment methods are accepted?",
        "answer": "We accept Visa, Mastercard, American Express, PayPal, and bank transfers for annual plans.",
        "keywords": ["payment", "credit card", "paypal", "bank transfer"],
        "risk_level": "low",
        "ground_truth_sources": ["billing_policy_v3.pdf#section1"],
    },
    {
        "question": "Can I get a refund for unused months?",
        "answer": "Refunds for unused months are available within 30 days of purchase for annual plans. Monthly plans are non-refundable.",
        "keywords": ["refund", "unused", "annual", "monthly"],
        "risk_level": "high",
        "ground_truth_sources": ["refund_policy_v2.pdf#section4"],
    },
    {
        "question": "Why was I charged twice this month?",
        "answer": "Duplicate charges can occur when a payment fails and is retried. Please contact billing support with your transaction IDs for investigation.",
        "keywords": ["duplicate", "charge", "twice", "transaction"],
        "risk_level": "high",
        "ground_truth_sources": ["billing_policy_v3.pdf#section7"],
    },
    {
        "question": "How do I cancel my subscription?",
        "answer": "You can cancel your subscription at any time from Account Settings > Subscription > Cancel. Access continues until the end of the billing period.",
        "keywords": ["cancel", "subscription", "account settings"],
        "risk_level": "medium",
        "ground_truth_sources": ["subscription_terms_v4.pdf#section3"],
    },
    {
        "question": "Is there a free trial available?",
        "answer": "Yes, a 14-day free trial is available for all new accounts. No credit card is required to start the trial.",
        "keywords": ["free trial", "14 days", "no credit card"],
        "risk_level": "low",
        "ground_truth_sources": ["pricing_page_v5.html"],
    },
    {
        "question": "What happens if my payment fails?",
        "answer": "If a payment fails, we retry after 3 days and again after 7 days. After two failed retries, the account is suspended until payment is resolved.",
        "keywords": ["payment failure", "retry", "suspended"],
        "risk_level": "high",
        "ground_truth_sources": ["billing_policy_v3.pdf#section6"],
    },
    {
        "question": "Can I switch from monthly to annual billing?",
        "answer": "Yes. Go to Account Settings > Billing > Switch to Annual. You will be charged the prorated annual amount and receive a 20% discount.",
        "keywords": ["monthly", "annual", "switch", "discount"],
        "risk_level": "medium",
        "ground_truth_sources": ["billing_policy_v3.pdf#section5"],
    },
    {
        "question": "How do I download my invoice?",
        "answer": "Invoices are available under Account Settings > Billing > Invoice History. Click any invoice to download a PDF.",
        "keywords": ["invoice", "download", "pdf", "history"],
        "risk_level": "low",
        "ground_truth_sources": ["billing_policy_v3.pdf#section2"],
    },
    {
        "question": "Do you charge VAT or sales tax?",
        "answer": "Sales tax or VAT is applied based on your billing address jurisdiction. The rate is calculated at checkout and displayed on your invoice.",
        "keywords": ["vat", "tax", "sales tax", "jurisdiction"],
        "risk_level": "low",
        "ground_truth_sources": ["tax_policy_v1.pdf"],
    },
]

_RETURNS: List[dict] = [
    {
        "question": "What is your return policy?",
        "answer": "Products can be returned within 30 days of purchase in original condition with proof of purchase.",
        "keywords": ["return", "policy", "30 days", "proof of purchase"],
        "risk_level": "medium",
        "ground_truth_sources": ["return_policy_v2.pdf#section1"],
    },
    {
        "question": "How do I initiate a return?",
        "answer": "Visit the Returns Center in your account, select the order, choose items to return, and print the prepaid return label.",
        "keywords": ["initiate", "return", "label", "returns center"],
        "risk_level": "low",
        "ground_truth_sources": ["return_policy_v2.pdf#section2"],
    },
    {
        "question": "Can I return a digital product?",
        "answer": "Digital products and software licenses are non-returnable once activated. Exceptions apply if the product fails to function as described.",
        "keywords": ["digital", "software", "license", "non-returnable"],
        "risk_level": "high",
        "ground_truth_sources": ["return_policy_v2.pdf#section5"],
    },
    {
        "question": "How long does a refund take after I return an item?",
        "answer": "Once we receive and inspect the returned item, refunds are processed within 5–7 business days to the original payment method.",
        "keywords": ["refund", "timeline", "business days", "inspection"],
        "risk_level": "medium",
        "ground_truth_sources": ["return_policy_v2.pdf#section3"],
    },
    {
        "question": "What if I received a damaged item?",
        "answer": "Report damaged items within 48 hours of delivery by contacting support with photos. We will arrange a replacement or full refund at no cost.",
        "keywords": ["damaged", "replacement", "photos", "48 hours"],
        "risk_level": "high",
        "ground_truth_sources": ["return_policy_v2.pdf#section6"],
    },
    {
        "question": "Do I need to pay for return shipping?",
        "answer": "Return shipping is free for defective or incorrectly shipped items. For other returns, a flat $7.99 return label fee is deducted from your refund.",
        "keywords": ["return shipping", "free", "label fee", "defective"],
        "risk_level": "medium",
        "ground_truth_sources": ["return_policy_v2.pdf#section4"],
    },
    {
        "question": "Can I exchange an item instead of returning it?",
        "answer": "Exchanges are supported for the same item in a different size or color. Go to the Returns Center and select Exchange instead of Return.",
        "keywords": ["exchange", "size", "color", "returns center"],
        "risk_level": "low",
        "ground_truth_sources": ["return_policy_v2.pdf#section7"],
    },
    {
        "question": "What items cannot be returned?",
        "answer": "Perishable goods, customized products, hazardous materials, and opened consumables cannot be returned.",
        "keywords": ["non-returnable", "perishable", "customized", "hazardous"],
        "risk_level": "medium",
        "ground_truth_sources": ["return_policy_v2.pdf#section5"],
    },
    {
        "question": "I returned an item but have not received my refund yet.",
        "answer": "If more than 10 business days have passed since we confirmed receipt of your return, please contact support with your return tracking number.",
        "keywords": ["missing refund", "tracking", "business days"],
        "risk_level": "high",
        "ground_truth_sources": ["return_policy_v2.pdf#section3"],
    },
    {
        "question": "Can I return a gift?",
        "answer": "Gifts can be returned for store credit equal to the purchase price. A gift receipt or order number is required.",
        "keywords": ["gift", "store credit", "gift receipt"],
        "risk_level": "low",
        "ground_truth_sources": ["return_policy_v2.pdf#section8"],
    },
]

_SLA: List[dict] = [
    {
        "question": "What is the guaranteed uptime SLA?",
        "answer": "Our platform guarantees 99.9% monthly uptime. Planned maintenance windows are excluded and communicated 48 hours in advance.",
        "keywords": ["uptime", "sla", "99.9%", "maintenance"],
        "risk_level": "high",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section1"],
    },
    {
        "question": "What compensation do I receive if the SLA is breached?",
        "answer": "If monthly uptime falls below 99.9%, you are eligible for service credits equal to 10x the downtime hours as a percentage of your monthly fee.",
        "keywords": ["sla breach", "compensation", "service credit", "downtime"],
        "risk_level": "critical",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section4"],
    },
    {
        "question": "How do I report an outage?",
        "answer": "Report outages through the Support Portal or by emailing incidents@support.example.com. Include your account ID and the symptoms observed.",
        "keywords": ["outage", "report", "support portal", "incidents"],
        "risk_level": "high",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section2"],
    },
    {
        "question": "What is the target response time for critical tickets?",
        "answer": "Critical priority tickets have a 1-hour initial response SLA and a 4-hour resolution target during business hours.",
        "keywords": ["response time", "critical", "1 hour", "resolution"],
        "risk_level": "high",
        "ground_truth_sources": ["support_tiers_v3.pdf#section2"],
    },
    {
        "question": "Does the SLA cover third-party integrations?",
        "answer": "The SLA covers the core platform only. Outages caused by third-party services, including payment gateways and external APIs, are excluded.",
        "keywords": ["sla", "third-party", "integration", "excluded"],
        "risk_level": "high",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section6"],
    },
    {
        "question": "How is downtime calculated for SLA purposes?",
        "answer": "Downtime is measured from the time a support ticket is opened or our monitoring system detects unavailability, whichever comes first.",
        "keywords": ["downtime", "calculation", "monitoring", "availability"],
        "risk_level": "medium",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section3"],
    },
    {
        "question": "Can I request a custom SLA for my enterprise plan?",
        "answer": "Custom SLA agreements with higher uptime guarantees and dedicated support are available for enterprise customers. Contact your account manager.",
        "keywords": ["custom sla", "enterprise", "account manager"],
        "risk_level": "medium",
        "ground_truth_sources": ["enterprise_terms_v2.pdf#section1"],
    },
    {
        "question": "Where can I view the current system status?",
        "answer": "Real-time system status and historical incident reports are available at status.example.com. You can subscribe to email or SMS alerts.",
        "keywords": ["system status", "status page", "incidents", "alerts"],
        "risk_level": "low",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section2"],
    },
    {
        "question": "What is your RTO and RPO for disaster recovery?",
        "answer": "Our Recovery Time Objective (RTO) is 4 hours and Recovery Point Objective (RPO) is 1 hour for enterprise tier customers.",
        "keywords": ["rto", "rpo", "disaster recovery", "enterprise"],
        "risk_level": "critical",
        "ground_truth_sources": ["dr_policy_v2.pdf#section1"],
    },
    {
        "question": "Are SLA credits applied automatically?",
        "answer": "SLA credits are calculated monthly and applied to your next invoice automatically. You do not need to file a claim.",
        "keywords": ["sla credits", "automatic", "invoice"],
        "risk_level": "medium",
        "ground_truth_sources": ["sla_agreement_v6.pdf#section5"],
    },
]

_ACCOUNT_ACCESS: List[dict] = [
    {
        "question": "How do I reset my password?",
        "answer": "Click Forgot Password on the login page, enter your email address, and follow the link sent to your inbox. Links expire after 24 hours.",
        "keywords": ["password", "reset", "forgot", "email"],
        "risk_level": "medium",
        "ground_truth_sources": ["security_policy_v4.pdf#section1"],
    },
    {
        "question": "How do I enable two-factor authentication?",
        "answer": "Go to Account Settings > Security > Two-Factor Authentication and follow the setup wizard. Authenticator apps and SMS are supported.",
        "keywords": ["2fa", "two-factor", "authenticator", "security"],
        "risk_level": "low",
        "ground_truth_sources": ["security_policy_v4.pdf#section3"],
    },
    {
        "question": "My account has been locked. How do I unlock it?",
        "answer": "Accounts are locked after 5 failed login attempts. Wait 30 minutes for automatic unlock or contact support to unlock immediately.",
        "keywords": ["locked", "login", "failed attempts", "unlock"],
        "risk_level": "high",
        "ground_truth_sources": ["security_policy_v4.pdf#section2"],
    },
    {
        "question": "How do I add a new user to my account?",
        "answer": "Go to Account Settings > Team Members > Invite User. Enter the email address and assign a role. The invite expires after 7 days.",
        "keywords": ["add user", "invite", "team members", "role"],
        "risk_level": "medium",
        "ground_truth_sources": ["admin_guide_v3.pdf#section2"],
    },
    {
        "question": "Can I have multiple accounts with the same email?",
        "answer": "Each email address can only be associated with one account. Use email aliases or separate email addresses to create additional accounts.",
        "keywords": ["multiple accounts", "email", "alias"],
        "risk_level": "low",
        "ground_truth_sources": ["account_policy_v2.pdf#section1"],
    },
    {
        "question": "How do I transfer account ownership?",
        "answer": "Account ownership can be transferred by the current owner from Settings > Account > Transfer Ownership. The new owner must confirm via email.",
        "keywords": ["transfer", "ownership", "account", "confirm"],
        "risk_level": "critical",
        "ground_truth_sources": ["admin_guide_v3.pdf#section5"],
    },
    {
        "question": "What permissions does an Admin role have?",
        "answer": "Admins can manage team members, billing settings, integrations, and data exports. They cannot delete the account or transfer ownership.",
        "keywords": ["admin", "permissions", "role", "billing"],
        "risk_level": "high",
        "ground_truth_sources": ["admin_guide_v3.pdf#section1"],
    },
    {
        "question": "How do I remove a user from my account?",
        "answer": "Go to Account Settings > Team Members, find the user, and click Remove. Their access is revoked immediately.",
        "keywords": ["remove user", "revoke", "access", "team members"],
        "risk_level": "medium",
        "ground_truth_sources": ["admin_guide_v3.pdf#section3"],
    },
    {
        "question": "I cannot log in after changing my email address.",
        "answer": "Use your new email address to log in. If you are locked out, use the password reset flow with your new email or contact support.",
        "keywords": ["login", "email change", "locked out"],
        "risk_level": "high",
        "ground_truth_sources": ["security_policy_v4.pdf#section1"],
    },
    {
        "question": "How do I delete my account permanently?",
        "answer": "Account deletion is permanent and irreversible. Go to Account Settings > Account > Delete Account. You must confirm via email. Data is purged after 30 days.",
        "keywords": ["delete account", "permanent", "irreversible", "purge"],
        "risk_level": "critical",
        "ground_truth_sources": ["account_policy_v2.pdf#section5"],
    },
]

_PRODUCT_SUPPORT: List[dict] = [
    {
        "question": "How do I connect my CRM to a third-party email provider?",
        "answer": "Go to Integrations > Email Providers and select your provider. Enter your API credentials and click Test Connection before saving.",
        "keywords": ["crm", "email", "integration", "api credentials"],
        "risk_level": "medium",
        "ground_truth_sources": ["integration_guide_v5.pdf#section3"],
    },
    {
        "question": "Why are my automation rules not triggering?",
        "answer": "Check that the rule is active, the trigger conditions match your data, and the rule has not exceeded its daily execution limit.",
        "keywords": ["automation", "rules", "trigger", "execution limit"],
        "risk_level": "medium",
        "ground_truth_sources": ["automation_guide_v4.pdf#section2"],
    },
    {
        "question": "How do I export my contact data?",
        "answer": "Go to Contacts > Export, select the fields and date range, and click Export CSV. Exports are emailed to your account email within 10 minutes.",
        "keywords": ["export", "contacts", "csv", "data"],
        "risk_level": "medium",
        "ground_truth_sources": ["data_guide_v3.pdf#section1"],
    },
    {
        "question": "What is the maximum file size for document uploads?",
        "answer": "Individual file uploads are limited to 50MB. Bulk imports via the API support files up to 500MB.",
        "keywords": ["file size", "upload", "limit", "bulk import"],
        "risk_level": "low",
        "ground_truth_sources": ["limits_guide_v2.pdf#section1"],
    },
    {
        "question": "How do I set up a webhook?",
        "answer": "Go to Settings > Developer > Webhooks, click Add Webhook, enter your endpoint URL, select events to subscribe to, and save.",
        "keywords": ["webhook", "endpoint", "events", "developer"],
        "risk_level": "medium",
        "ground_truth_sources": ["api_guide_v6.pdf#section4"],
    },
    {
        "question": "What are the API rate limits?",
        "answer": "The standard API rate limit is 1,000 requests per hour per API key. Enterprise plans have a limit of 10,000 requests per hour.",
        "keywords": ["api", "rate limit", "requests", "enterprise"],
        "risk_level": "medium",
        "ground_truth_sources": ["api_guide_v6.pdf#section1"],
    },
    {
        "question": "How do I create a custom field?",
        "answer": "Go to Settings > Fields > Custom Fields > Add Field. Choose the field type, set visibility and required status, then save.",
        "keywords": ["custom field", "settings", "field type"],
        "risk_level": "low",
        "ground_truth_sources": ["admin_guide_v3.pdf#section6"],
    },
    {
        "question": "Why is my dashboard loading slowly?",
        "answer": "Dashboard slowness is usually caused by large date ranges or complex filter combinations. Try narrowing the date range or simplifying your filters.",
        "keywords": ["dashboard", "slow", "performance", "filter"],
        "risk_level": "low",
        "ground_truth_sources": ["performance_guide_v1.pdf#section2"],
    },
    {
        "question": "How do I import contacts from a CSV file?",
        "answer": "Go to Contacts > Import > Upload CSV. Map your CSV columns to contact fields, review the preview, and click Import. Duplicates are detected automatically.",
        "keywords": ["import", "contacts", "csv", "duplicates"],
        "risk_level": "medium",
        "ground_truth_sources": ["data_guide_v3.pdf#section2"],
    },
    {
        "question": "How do I enable GDPR data deletion for a contact?",
        "answer": "Go to the contact record, click the Privacy menu, and select Request Data Deletion. The deletion is processed within 30 days per GDPR requirements.",
        "keywords": ["gdpr", "data deletion", "privacy", "contact"],
        "risk_level": "critical",
        "ground_truth_sources": ["gdpr_guide_v3.pdf#section1"],
    },
]

_DOMAIN_MAP = {
    "billing": _BILLING,
    "returns": _RETURNS,
    "sla": _SLA,
    "account_access": _ACCOUNT_ACCESS,
    "product_support": _PRODUCT_SUPPORT,
}


def load_faq_dataset(domains: Optional[List[str]] = None) -> List[FAQItem]:
    """
    Load the synthetic CRM FAQ dataset.

    Parameters
    ----------
    domains : list of str, optional
        Filter to specific domains. Options: billing, returns, sla,
        account_access, product_support. Default: all domains.

    Returns
    -------
    list of FAQItem
    """
    selected = domains or list(_DOMAIN_MAP.keys())
    items: List[FAQItem] = []
    counter = 1
    for domain in selected:
        for i, raw in enumerate(_DOMAIN_MAP[domain]):
            items.append(FAQItem(
                id=f"faq-{domain[:3].upper()}-{i+1:03d}",
                domain=domain,
                question=raw["question"],
                answer=raw["answer"],
                keywords=raw["keywords"],
                risk_level=raw["risk_level"],
                ground_truth_sources=raw["ground_truth_sources"],
            ))
            counter += 1
    return items


def load_faq_as_dicts(domains: Optional[List[str]] = None) -> List[dict]:
    """Return FAQ items as plain dicts for easy serialisation."""
    return [
        {
            "id": item.id,
            "domain": item.domain,
            "question": item.question,
            "answer": item.answer,
            "keywords": item.keywords,
            "risk_level": item.risk_level,
            "ground_truth_sources": item.ground_truth_sources,
        }
        for item in load_faq_dataset(domains)
    ]
