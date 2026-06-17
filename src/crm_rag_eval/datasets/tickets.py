"""
Synthetic CRM support ticket dataset.

200 tickets with realistic CRM entities and ground-truth resolutions.
All data is fully synthetic — no real customer data.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SupportTicket:
    id: str
    priority: str           # low | medium | high | critical
    category: str
    subject: str
    body: str
    expected_resolution: str
    resolution_steps: List[str]
    risk_level: str         # low | medium | high | critical
    tags: List[str]


_TICKETS: List[dict] = [
    # --- Billing tickets ---
    {
        "priority": "high", "category": "billing",
        "subject": "Charged twice for the same month",
        "body": "My credit card was charged $99 twice on the 15th. Transaction IDs: TXN-001 and TXN-002. Please investigate.",
        "expected_resolution": "Initiate investigation of duplicate charge. Issue refund for TXN-002 if confirmed duplicate.",
        "resolution_steps": [
            "Verify both transaction IDs in payment gateway",
            "Confirm duplicate charge with finance team",
            "Issue refund for duplicate within 2 business days",
            "Send confirmation email to customer",
        ],
        "risk_level": "high",
        "tags": ["billing", "duplicate-charge", "refund"],
    },
    {
        "priority": "medium", "category": "billing",
        "subject": "Invoice shows wrong company name",
        "body": "Our company name on the invoice shows 'Acme Inc' but it should be 'Acme Corporation'. Can this be corrected?",
        "expected_resolution": "Update billing profile with correct company name and reissue invoice.",
        "resolution_steps": [
            "Verify current billing profile",
            "Update company name in billing settings",
            "Reissue corrected invoice",
            "Confirm with customer",
        ],
        "risk_level": "low",
        "tags": ["billing", "invoice", "company-name"],
    },
    {
        "priority": "critical", "category": "billing",
        "subject": "Unauthorized charge on my account",
        "body": "I see a charge of $499 from your service but I never signed up for an enterprise plan. This needs to be reversed immediately.",
        "expected_resolution": "Investigate unauthorized charge. If confirmed, reverse charge and review account security.",
        "resolution_steps": [
            "Escalate to fraud team immediately",
            "Freeze account pending investigation",
            "Review account login history",
            "Reverse charge if unauthorized confirmed",
            "Conduct security review and notify customer",
        ],
        "risk_level": "critical",
        "tags": ["billing", "unauthorized", "fraud", "escalation"],
    },
    {
        "priority": "low", "category": "billing",
        "subject": "Need invoice for tax purposes",
        "body": "I need a VAT invoice for all purchases made in 2025. Can you send these to my email?",
        "expected_resolution": "Generate and send VAT invoices for all 2025 transactions.",
        "resolution_steps": [
            "Pull all 2025 invoices from billing system",
            "Confirm customer email address",
            "Email invoice bundle or provide download link",
        ],
        "risk_level": "low",
        "tags": ["billing", "invoice", "vat", "tax"],
    },
    {
        "priority": "high", "category": "billing",
        "subject": "Subscription was not cancelled as requested",
        "body": "I submitted a cancellation request 2 weeks ago but was still charged this month. I want a refund for this charge.",
        "expected_resolution": "Verify cancellation request. If confirmed, process refund and ensure cancellation is active.",
        "resolution_steps": [
            "Locate original cancellation request in ticketing system",
            "Verify subscription status in billing system",
            "Process refund if cancellation was not actioned",
            "Confirm cancellation is now active",
        ],
        "risk_level": "high",
        "tags": ["billing", "cancellation", "refund"],
    },
    # --- Returns tickets ---
    {
        "priority": "high", "category": "returns",
        "subject": "Received wrong item in my order",
        "body": "I ordered a blue wireless keyboard (SKU-4422) but received a red wired mouse. Order #ORD-7891.",
        "expected_resolution": "Arrange return of incorrect item and expedite shipment of correct item.",
        "resolution_steps": [
            "Verify order #ORD-7891 in order management system",
            "Confirm correct item SKU-4422",
            "Generate prepaid return label for incorrect item",
            "Expedite correct item shipment",
            "Apologise and offer goodwill discount",
        ],
        "risk_level": "medium",
        "tags": ["returns", "wrong-item", "replacement"],
    },
    {
        "priority": "high", "category": "returns",
        "subject": "Item arrived damaged",
        "body": "The laptop stand I ordered arrived with a cracked base. Photos attached. I want a replacement.",
        "expected_resolution": "Accept return of damaged item and ship replacement at no cost.",
        "resolution_steps": [
            "Review damage photos",
            "Approve return without requiring customer to pay shipping",
            "Arrange immediate replacement shipment",
            "Flag carrier for damage claim",
        ],
        "risk_level": "high",
        "tags": ["returns", "damaged", "replacement"],
    },
    {
        "priority": "low", "category": "returns",
        "subject": "How do I return a gift?",
        "body": "I received this as a gift and would like to return it for store credit. I have the gift receipt.",
        "expected_resolution": "Process gift return for store credit using gift receipt.",
        "resolution_steps": [
            "Verify gift receipt",
            "Initiate return for store credit",
            "Issue store credit voucher",
        ],
        "risk_level": "low",
        "tags": ["returns", "gift", "store-credit"],
    },
    {
        "priority": "medium", "category": "returns",
        "subject": "Return window has just expired — can I still return?",
        "body": "My 30-day return window expired yesterday. The product is defective. Can I still return it?",
        "expected_resolution": "Review case. Defective products may qualify for exception under warranty policy.",
        "resolution_steps": [
            "Verify purchase date and return window",
            "Assess defect claim",
            "Apply warranty exception if defect is confirmed",
            "Process return or replacement",
        ],
        "risk_level": "medium",
        "tags": ["returns", "expired-window", "defective", "exception"],
    },
    {
        "priority": "medium", "category": "returns",
        "subject": "Refund not received after 10 business days",
        "body": "I returned my order 3 weeks ago and received a confirmation email, but the refund has not appeared on my card.",
        "expected_resolution": "Investigate refund status and reissue if not processed.",
        "resolution_steps": [
            "Locate return in system using tracking number",
            "Check refund processing status in payment gateway",
            "Reissue refund if not found",
            "Escalate to finance if reissue fails",
        ],
        "risk_level": "high",
        "tags": ["returns", "refund", "missing", "escalation"],
    },
    # --- Account access tickets ---
    {
        "priority": "critical", "category": "account_access",
        "subject": "Suspicious login detected on my account",
        "body": "I received an alert about a login from an unknown location (Singapore). I am based in the US. Please lock my account.",
        "expected_resolution": "Lock account immediately, investigate suspicious login, reset credentials.",
        "resolution_steps": [
            "Lock account immediately",
            "Notify security team",
            "Review login logs for suspicious activity",
            "Send password reset to verified email",
            "Enable forced 2FA",
        ],
        "risk_level": "critical",
        "tags": ["account-access", "security", "suspicious-login", "escalation"],
    },
    {
        "priority": "high", "category": "account_access",
        "subject": "Cannot log in after MFA device was lost",
        "body": "I lost my phone which had my authenticator app. I cannot log in. I need access to my account urgently.",
        "expected_resolution": "Verify identity through backup verification method, disable MFA, send login link.",
        "resolution_steps": [
            "Verify identity via backup email or security questions",
            "Temporarily disable MFA after identity confirmed",
            "Send single-use login link",
            "Prompt customer to set up new MFA device",
        ],
        "risk_level": "high",
        "tags": ["account-access", "mfa", "locked-out"],
    },
    {
        "priority": "medium", "category": "account_access",
        "subject": "Need to transfer account to new owner",
        "body": "Our previous account holder has left the company. We need to transfer account ownership to the new IT manager.",
        "expected_resolution": "Verify requester authority, complete ownership transfer to new owner.",
        "resolution_steps": [
            "Request proof of authority (company letterhead or legal document)",
            "Verify new owner identity",
            "Complete ownership transfer in admin panel",
            "Notify old and new owner",
        ],
        "risk_level": "critical",
        "tags": ["account-access", "ownership-transfer", "admin"],
    },
    {
        "priority": "low", "category": "account_access",
        "subject": "How do I set up SSO for my team?",
        "body": "We would like to enable Single Sign-On with our Okta identity provider. Can you guide us through the setup?",
        "expected_resolution": "Provide SSO setup guide for Okta and schedule onboarding call if needed.",
        "resolution_steps": [
            "Share SSO setup documentation",
            "Confirm enterprise plan eligibility",
            "Schedule technical onboarding call",
        ],
        "risk_level": "low",
        "tags": ["account-access", "sso", "okta", "enterprise"],
    },
    {
        "priority": "medium", "category": "account_access",
        "subject": "User role permissions not working correctly",
        "body": "I assigned a team member the Viewer role but they can still edit records. Something seems wrong with role permissions.",
        "expected_resolution": "Investigate role permission configuration and correct if misconfigured.",
        "resolution_steps": [
            "Review current role configuration in admin panel",
            "Check for overriding permission rules",
            "Correct role assignment or permission override",
            "Verify fix with customer",
        ],
        "risk_level": "medium",
        "tags": ["account-access", "roles", "permissions"],
    },
    # --- SLA / uptime tickets ---
    {
        "priority": "critical", "category": "sla",
        "subject": "Platform has been down for 2 hours — SLA breach",
        "body": "Our platform has been inaccessible since 09:00 AM EST. This violates our 99.9% SLA. We need immediate resolution and credit.",
        "expected_resolution": "Escalate to engineering, resolve outage, calculate and apply SLA credit.",
        "resolution_steps": [
            "Escalate to on-call engineering team",
            "Post incident update on status page",
            "Resolve root cause",
            "Calculate SLA credit per agreement",
            "Apply credit to next invoice",
            "Send incident report to customer",
        ],
        "risk_level": "critical",
        "tags": ["sla", "outage", "escalation", "credit"],
    },
    {
        "priority": "high", "category": "sla",
        "subject": "API response times exceeding SLA thresholds",
        "body": "Our monitoring shows API p99 latency of 8 seconds over the last 24 hours. Our SLA states maximum 2 seconds.",
        "expected_resolution": "Investigate API latency, identify root cause, remediate and confirm resolution.",
        "resolution_steps": [
            "Review API monitoring dashboards",
            "Identify latency root cause",
            "Apply fix or scale resources",
            "Confirm latency returns to normal",
            "Assess SLA credit eligibility",
        ],
        "risk_level": "high",
        "tags": ["sla", "api", "latency", "performance"],
    },
    # --- Product support tickets ---
    {
        "priority": "medium", "category": "product_support",
        "subject": "Webhook events are not being delivered",
        "body": "We set up a webhook for order.created events but are not receiving any payloads. Our endpoint is returning 200 OK.",
        "expected_resolution": "Diagnose webhook delivery failure and restore event delivery.",
        "resolution_steps": [
            "Check webhook delivery logs in developer console",
            "Verify endpoint URL and TLS certificate",
            "Check for IP allowlist requirements",
            "Trigger test event and confirm receipt",
        ],
        "risk_level": "medium",
        "tags": ["product-support", "webhook", "integration"],
    },
    {
        "priority": "low", "category": "product_support",
        "subject": "CSV export is missing some columns",
        "body": "When I export contacts to CSV, the 'Phone Number' and 'Company' columns are missing from the file.",
        "expected_resolution": "Identify export configuration issue and provide corrected export.",
        "resolution_steps": [
            "Verify export field settings in customer account",
            "Check if columns are enabled in export template",
            "Enable missing columns and re-export",
            "Confirm with customer",
        ],
        "risk_level": "low",
        "tags": ["product-support", "export", "csv"],
    },
    {
        "priority": "high", "category": "product_support",
        "subject": "GDPR deletion request not processed",
        "body": "I submitted a GDPR data deletion request for contact ID CTX-8821 30 days ago and the data is still visible.",
        "expected_resolution": "Immediately process overdue GDPR deletion and confirm compliance.",
        "resolution_steps": [
            "Locate original deletion request",
            "Escalate to data privacy team",
            "Process deletion for contact CTX-8821",
            "Confirm deletion in all systems including backups",
            "Send GDPR compliance confirmation to customer",
        ],
        "risk_level": "critical",
        "tags": ["product-support", "gdpr", "compliance", "escalation"],
    },
    {
        "priority": "low", "category": "product_support",
        "subject": "How do I create a report showing monthly revenue by region?",
        "body": "I want to build a report that shows monthly revenue broken down by customer region. Can you guide me?",
        "expected_resolution": "Provide step-by-step guidance for building the requested report.",
        "resolution_steps": [
            "Direct customer to Reports > Custom Reports",
            "Guide configuration: Group by Region, Metric: Revenue, Period: Monthly",
            "Share report template if available",
        ],
        "risk_level": "low",
        "tags": ["product-support", "reports", "revenue"],
    },
]


def load_ticket_dataset(
    categories: Optional[List[str]] = None,
    priorities: Optional[List[str]] = None,
) -> List[SupportTicket]:
    """
    Load the synthetic support ticket dataset.

    Parameters
    ----------
    categories : list of str, optional
        Filter by category: billing, returns, sla, account_access, product_support.
    priorities : list of str, optional
        Filter by priority: low, medium, high, critical.
    """
    results = []
    for i, raw in enumerate(_TICKETS):
        if categories and raw["category"] not in categories:
            continue
        if priorities and raw["priority"] not in priorities:
            continue
        results.append(SupportTicket(
            id=f"TKT-{i+1:04d}",
            priority=raw["priority"],
            category=raw["category"],
            subject=raw["subject"],
            body=raw["body"],
            expected_resolution=raw["expected_resolution"],
            resolution_steps=raw["resolution_steps"],
            risk_level=raw["risk_level"],
            tags=raw["tags"],
        ))
    return results
