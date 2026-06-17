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


# ---------------------------------------------------------------------------
# Additional tickets — expanded to 50 total
# ---------------------------------------------------------------------------
_TICKETS.extend([
    # Billing
    {
        "priority": "medium", "category": "billing",
        "subject": "Promo code not applied to my invoice",
        "body": "I entered promo code SAVE20 at checkout but my invoice does not reflect any discount. Order date: 2026-05-10.",
        "expected_resolution": "Verify promo code validity and manually apply credit if eligible.",
        "resolution_steps": [
            "Verify promo code SAVE20 in promotions system",
            "Check order date against code validity window",
            "Apply credit to current invoice if eligible",
            "Notify customer of resolution",
        ],
        "risk_level": "medium",
        "tags": ["billing", "promo-code", "discount"],
    },
    {
        "priority": "high", "category": "billing",
        "subject": "Annual plan renewed without notice",
        "body": "My annual plan auto-renewed for $1,188 without a reminder email. I wanted to cancel before renewal. I need a refund.",
        "expected_resolution": "Verify reminder was sent. If not, process refund per money-back guarantee policy.",
        "resolution_steps": [
            "Check email delivery logs for renewal reminder",
            "Verify renewal date and customer's cancellation intent",
            "Process refund if reminder was not sent or was sent late",
            "Confirm cancellation of plan going forward",
        ],
        "risk_level": "high",
        "tags": ["billing", "auto-renewal", "refund"],
    },
    {
        "priority": "low", "category": "billing",
        "subject": "Can I get an annual invoice for my accountant?",
        "body": "My accountant needs a single annual invoice showing all charges from Jan–Dec 2025 for tax filing purposes.",
        "expected_resolution": "Generate consolidated annual invoice for 2025.",
        "resolution_steps": [
            "Pull all 2025 invoices from billing system",
            "Generate consolidated invoice or provide download bundle",
            "Email to customer",
        ],
        "risk_level": "low",
        "tags": ["billing", "invoice", "annual", "tax"],
    },
    {
        "priority": "critical", "category": "billing",
        "subject": "Multiple accounts charged for the same subscription",
        "body": "Our company has been charged on three different account IDs (ACC-001, ACC-002, ACC-003) for what should be a single enterprise plan. Total overcharge: $4,500.",
        "expected_resolution": "Investigate account duplication, merge accounts, and refund overcharges.",
        "resolution_steps": [
            "Audit all three account IDs and billing history",
            "Escalate to enterprise billing team",
            "Merge accounts or credit overcharges",
            "Assign a dedicated account manager",
        ],
        "risk_level": "critical",
        "tags": ["billing", "duplicate-accounts", "enterprise", "escalation"],
    },
    {
        "priority": "medium", "category": "billing",
        "subject": "Need to update billing to a new company name after acquisition",
        "body": "Our company was acquired and we need all billing documents re-issued under the new entity name 'NewCo Ltd' from January 2026 onward.",
        "expected_resolution": "Update billing profile and reissue future invoices under new entity name.",
        "resolution_steps": [
            "Request legal documentation of acquisition",
            "Update billing profile with new entity name",
            "Note: historical invoices cannot be retroactively reissued",
            "Issue amended invoice for current period if required",
        ],
        "risk_level": "medium",
        "tags": ["billing", "company-name", "acquisition"],
    },
    # Returns
    {
        "priority": "high", "category": "returns",
        "subject": "Returned item marked as delivered but refund not issued",
        "body": "Tracking shows my return was delivered to your warehouse on May 3rd. It has been 15 business days and I have not received a refund.",
        "expected_resolution": "Locate return in warehouse, process overdue refund immediately.",
        "resolution_steps": [
            "Confirm delivery via carrier tracking",
            "Search warehouse receiving logs for the return",
            "Escalate to warehouse team if not found",
            "Process refund within 1 business day of confirmation",
        ],
        "risk_level": "high",
        "tags": ["returns", "missing-refund", "warehouse", "escalation"],
    },
    {
        "priority": "medium", "category": "returns",
        "subject": "Product broke after 3 months — still under warranty?",
        "body": "My laptop stand (SKU-7731) broke at the hinge after 3 months of normal use. Is this covered under warranty? How do I get a replacement?",
        "expected_resolution": "Assess warranty claim. If defect in materials, approve replacement.",
        "resolution_steps": [
            "Confirm purchase date (within 1-year warranty window)",
            "Request photo evidence of defect",
            "Assess if defect is from normal use vs. misuse",
            "Approve replacement if covered",
        ],
        "risk_level": "medium",
        "tags": ["returns", "warranty", "replacement"],
    },
    {
        "priority": "low", "category": "returns",
        "subject": "How do I return a bundle if one item is defective?",
        "body": "I bought a 3-item office bundle. One of the items (a webcam) is not working. Do I need to return the whole bundle?",
        "expected_resolution": "Confirm single-item replacement policy for bundle defects.",
        "resolution_steps": [
            "Verify bundle policy for partial defects",
            "Arrange replacement for defective item only",
            "Provide prepaid return label for defective item",
        ],
        "risk_level": "low",
        "tags": ["returns", "bundle", "defective", "replacement"],
    },
    {
        "priority": "medium", "category": "returns",
        "subject": "Return portal showing error when I try to initiate return",
        "body": "Every time I click 'Start Return' on order #ORD-9021 I get error code 403. I have been trying for 3 days.",
        "expected_resolution": "Investigate portal error, manually initiate return for customer.",
        "resolution_steps": [
            "Reproduce 403 error in the returns portal",
            "Escalate to engineering if portal issue",
            "Manually create RMA for order #ORD-9021",
            "Email return label directly to customer",
        ],
        "risk_level": "medium",
        "tags": ["returns", "portal-error", "manual-return"],
    },
    {
        "priority": "high", "category": "returns",
        "subject": "Customs seized my returned package — who is responsible?",
        "body": "I shipped my international return but customs seized the package at the border. Who covers the loss? I still want my refund.",
        "expected_resolution": "Investigate customs seizure, assess liability, and provide customer with resolution.",
        "resolution_steps": [
            "Request customs seizure documentation from customer",
            "Consult international returns policy on customs liability",
            "Escalate to legal/compliance if needed",
            "Determine if refund or store credit is appropriate",
        ],
        "risk_level": "high",
        "tags": ["returns", "international", "customs", "escalation"],
    },
    # Account access
    {
        "priority": "critical", "category": "account_access",
        "subject": "API key leaked in public GitHub repo — need emergency rotation",
        "body": "Our API key was accidentally committed to a public GitHub repo 2 hours ago. We need it revoked and replaced immediately.",
        "expected_resolution": "Revoke compromised API key immediately, issue new key, audit usage.",
        "resolution_steps": [
            "Revoke compromised API key immediately",
            "Audit API usage logs for the past 2 hours for suspicious activity",
            "Issue new API key",
            "Alert security team for further investigation",
            "Advise customer on key rotation best practices",
        ],
        "risk_level": "critical",
        "tags": ["account-access", "api-key", "security", "leaked", "escalation"],
    },
    {
        "priority": "high", "category": "account_access",
        "subject": "SCIM provisioning not deactivating users when removed from IdP",
        "body": "We removed 5 users from our Okta directory 3 days ago but they still have active access in the CRM.",
        "expected_resolution": "Investigate SCIM sync issue and manually deactivate affected users immediately.",
        "resolution_steps": [
            "Manually deactivate 5 users immediately",
            "Check SCIM integration logs for sync errors",
            "Escalate to engineering if SCIM webhook is failing",
            "Confirm fix with customer and monitor for 24 hours",
        ],
        "risk_level": "critical",
        "tags": ["account-access", "scim", "okta", "deprovisioning"],
    },
    {
        "priority": "medium", "category": "account_access",
        "subject": "User receiving permission denied on specific records",
        "body": "One of our Managers (user ID: USR-5521) cannot open deal records in the EMEA pipeline. Other managers have access.",
        "expected_resolution": "Diagnose and fix permission misconfiguration for USR-5521.",
        "resolution_steps": [
            "Review USR-5521 role and project assignments",
            "Check EMEA pipeline permission settings",
            "Compare with another Manager who has access",
            "Correct permission assignment",
            "Verify fix with customer",
        ],
        "risk_level": "medium",
        "tags": ["account-access", "permissions", "manager-role"],
    },
    {
        "priority": "low", "category": "account_access",
        "subject": "How do I enable SSO for a new subsidiary?",
        "body": "We acquired a subsidiary and want to extend our existing Okta SSO to their users under our account.",
        "expected_resolution": "Guide customer through adding subsidiary domain to existing SSO configuration.",
        "resolution_steps": [
            "Confirm enterprise plan covers subsidiary",
            "Guide customer to add subsidiary email domain to SSO allowlist",
            "Test SSO login for subsidiary user",
        ],
        "risk_level": "low",
        "tags": ["account-access", "sso", "okta", "subsidiary"],
    },
    {
        "priority": "high", "category": "account_access",
        "subject": "Bulk-imported users have wrong roles assigned",
        "body": "I imported 150 users via CSV and all were assigned the Viewer role instead of the Manager role I configured in the import template.",
        "expected_resolution": "Bulk-update 150 users to correct role assignment.",
        "resolution_steps": [
            "Verify CSV import template and role column mapping",
            "Bulk-update 150 users to Manager role via admin API",
            "Confirm with customer",
            "Identify and fix the CSV role mapping bug",
        ],
        "risk_level": "high",
        "tags": ["account-access", "bulk-import", "roles", "csv"],
    },
    # SLA / uptime
    {
        "priority": "critical", "category": "sla",
        "subject": "Data export API returning 500 errors for 6 hours",
        "body": "Our automated data pipeline has been failing since 03:00 AM UTC. Every call to /api/v2/exports returns HTTP 500. We have 4 hours of backup data at risk.",
        "expected_resolution": "Restore export API, investigate root cause, assess SLA credit.",
        "resolution_steps": [
            "Escalate to API on-call team immediately",
            "Restore export API service",
            "Post status page update",
            "Assess 6-hour window against SLA",
            "Calculate service credit and apply to next invoice",
            "Publish post-incident review within 5 business days",
        ],
        "risk_level": "critical",
        "tags": ["sla", "api", "outage", "escalation", "data-loss-risk"],
    },
    {
        "priority": "high", "category": "sla",
        "subject": "Webhook delivery delays causing missed customer follow-ups",
        "body": "Our webhooks for contact.updated events have been delayed by 30–90 minutes since yesterday. This is causing our sales team to miss follow-up windows.",
        "expected_resolution": "Investigate webhook queue, restore normal delivery, assess impact.",
        "resolution_steps": [
            "Check webhook delivery queue for backlog",
            "Identify root cause of queue delay",
            "Flush queue and restore real-time delivery",
            "Notify customer when restored",
            "Assess SLA credit eligibility for webhook SLA breach",
        ],
        "risk_level": "high",
        "tags": ["sla", "webhook", "delay", "queue"],
    },
    {
        "priority": "medium", "category": "sla",
        "subject": "Support ticket response time exceeded SLA — requesting credit",
        "body": "Ticket #TKT-8812 (Severity 2) was opened 8 hours ago with no response. Our SLA states 4-hour response for Severity 2.",
        "expected_resolution": "Respond to ticket immediately, acknowledge SLA breach, process credit.",
        "resolution_steps": [
            "Respond to TKT-8812 immediately",
            "Acknowledge SLA breach in response",
            "Calculate credit: 10x downtime hours as % of monthly fee",
            "Apply credit to next invoice",
        ],
        "risk_level": "high",
        "tags": ["sla", "ticket", "response-time", "credit"],
    },
    {
        "priority": "medium", "category": "sla",
        "subject": "How do I request a post-incident review?",
        "body": "We experienced an outage last week (incident INC-2241). I haven't received the post-incident review document yet. How do I request it?",
        "expected_resolution": "Provide post-incident review document and confirm publication timeline.",
        "resolution_steps": [
            "Locate incident INC-2241 and its status",
            "Confirm PIR is in progress (due within 5 business days)",
            "Email current draft or ETA to customer",
            "Share final PIR on status page when complete",
        ],
        "risk_level": "medium",
        "tags": ["sla", "post-incident-review", "pir"],
    },
    {
        "priority": "low", "category": "sla",
        "subject": "Clarify SLA for sandbox environment",
        "body": "We rely on our sandbox environment for CI/CD testing. Is the sandbox covered by the same uptime SLA as production?",
        "expected_resolution": "Clarify that sandbox is best-effort and not covered by production SLA.",
        "resolution_steps": [
            "Confirm sandbox is best-effort, no SLA coverage",
            "Point to relevant SLA agreement section",
            "Suggest customer use production with feature flags for critical testing",
        ],
        "risk_level": "low",
        "tags": ["sla", "sandbox", "ci-cd"],
    },
    # Product support
    {
        "priority": "high", "category": "product_support",
        "subject": "CRM data sync stopped after Salesforce OAuth token expired",
        "body": "Our Salesforce integration has not synced since Monday. We see error: OAuth token expired. Contacts are out of sync.",
        "expected_resolution": "Guide customer to reauthorize Salesforce OAuth token.",
        "resolution_steps": [
            "Confirm OAuth token expiry in integration logs",
            "Guide customer to Integrations > Salesforce > Reauthorize",
            "Trigger manual full sync to catch up missed changes",
            "Confirm sync is running",
        ],
        "risk_level": "high",
        "tags": ["product-support", "salesforce", "oauth", "integration"],
    },
    {
        "priority": "medium", "category": "product_support",
        "subject": "Email campaign showing 0% delivery rate",
        "body": "I sent a campaign to 2,000 contacts yesterday but the analytics dashboard shows 0% delivery. No bounces, no errors — just 0.",
        "expected_resolution": "Investigate email delivery failure, identify root cause, arrange resend.",
        "resolution_steps": [
            "Check email delivery logs for campaign ID",
            "Verify DKIM/SPF/DMARC status for sending domain",
            "Check if sending domain is on a blacklist",
            "Resolve deliverability issue",
            "Arrange resend of campaign",
        ],
        "risk_level": "high",
        "tags": ["product-support", "email", "deliverability", "campaign"],
    },
    {
        "priority": "low", "category": "product_support",
        "subject": "How do I create a report comparing two date ranges?",
        "body": "I want to compare deal close rates in Q1 2026 vs Q1 2025 in one report. Is this possible?",
        "expected_resolution": "Guide customer to use the date comparison feature in custom reports.",
        "resolution_steps": [
            "Direct customer to Reports > Custom Reports > Compare Periods",
            "Guide configuration: Base period Q1 2026, Compare period Q1 2025",
            "Metric: Deal close rate, Dimension: Stage",
            "Share screenshot or video tutorial link",
        ],
        "risk_level": "low",
        "tags": ["product-support", "reports", "date-comparison"],
    },
    {
        "priority": "high", "category": "product_support",
        "subject": "Contact import duplicated all records",
        "body": "I ran a CSV import of 5,000 contacts and now every contact is duplicated. I need the duplicates removed without losing the original data.",
        "expected_resolution": "Run bulk duplicate detection and merge, or roll back the import.",
        "resolution_steps": [
            "Identify the import job ID and timestamp",
            "Check if rollback is possible within 24-hour window",
            "If not, run bulk duplicate detection via admin API",
            "Merge duplicates preserving most recent data",
            "Confirm with customer when resolved",
        ],
        "risk_level": "high",
        "tags": ["product-support", "import", "duplicates", "contacts"],
    },
    {
        "priority": "critical", "category": "product_support",
        "subject": "Automation rule sent emails to unsubscribed contacts",
        "body": "A workflow automation sent a promotional email to 200 contacts who had previously unsubscribed. This may be a GDPR/CAN-SPAM violation.",
        "expected_resolution": "Halt automation, investigate scope, notify compliance team, contact affected users.",
        "resolution_steps": [
            "Halt the automation rule immediately",
            "Identify all 200 affected unsubscribed contacts",
            "Escalate to compliance/legal team",
            "Assess GDPR/CAN-SPAM breach scope",
            "Prepare breach notification if required",
            "Audit all automation rules for similar issues",
        ],
        "risk_level": "critical",
        "tags": ["product-support", "gdpr", "unsubscribe", "compliance", "escalation"],
    },
    {
        "priority": "medium", "category": "product_support",
        "subject": "Custom field values not appearing in exported CSV",
        "body": "I have 12 custom fields on contact records but when I export to CSV only the standard fields appear. Custom fields are missing.",
        "expected_resolution": "Identify CSV export custom field configuration issue and fix.",
        "resolution_steps": [
            "Check export template configuration for custom field inclusion",
            "Verify custom fields are marked as exportable in field settings",
            "Enable custom fields in export template",
            "Re-export and confirm with customer",
        ],
        "risk_level": "low",
        "tags": ["product-support", "export", "custom-fields", "csv"],
    },
    {
        "priority": "low", "category": "product_support",
        "subject": "Can the CRM send SMS notifications to contacts?",
        "body": "We want to send automated SMS reminders to contacts 24 hours before an appointment. Does the CRM support this natively or via integration?",
        "expected_resolution": "Clarify SMS capability and guide to relevant integration.",
        "resolution_steps": [
            "Confirm native SMS is not supported",
            "Direct customer to Integrations > Twilio or Vonage for SMS automation",
            "Share setup guide for SMS via telephony integration",
        ],
        "risk_level": "low",
        "tags": ["product-support", "sms", "automation", "integration"],
    },
    {
        "priority": "high", "category": "product_support",
        "subject": "Document signing requests not being delivered to signers",
        "body": "I sent 15 contract signing requests yesterday but none of the signers received the email. The requests show as 'Sent' in the CRM.",
        "expected_resolution": "Investigate signing email delivery, resend to affected signers.",
        "resolution_steps": [
            "Check e-signature email delivery logs",
            "Verify signing email domain is not on a blocklist",
            "Resend signing requests for all 15 contracts",
            "Confirm receipt with customer",
        ],
        "risk_level": "high",
        "tags": ["product-support", "document-signing", "email", "delivery"],
    },
])
