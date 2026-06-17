"""
crm-rag-eval CLI

Usage:
    crm-rag-eval demo                     # run a demo evaluation
    crm-rag-eval datasets list            # list available datasets
    crm-rag-eval datasets show faq        # preview FAQ dataset
    crm-rag-eval datasets show tickets    # preview ticket dataset
"""

from __future__ import annotations
import json
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

app  = typer.Typer(help="CRM RAG Evaluation Toolkit — crm-rag-eval")
ds   = typer.Typer(help="Dataset commands")
app.add_typer(ds, name="datasets")

console = Console()


@app.command()
def demo():
    """Run a quick demo evaluation with synthetic data and print the report."""
    from .evaluator import CRMRagEvaluator
    from .metrics.engine import RAGSample

    rprint("[bold blue]crm-rag-eval demo[/bold blue] — running 4 sample evaluations...\n")

    samples = [
        RAGSample(
            question="What is the refund policy for annual plans?",
            generated_answer="Refunds for unused months are available within 30 days of purchase for annual plans.",
            retrieved_contexts=["Refunds for unused months are available within 30 days of purchase for annual plans. Monthly plans are non-refundable."],
            ground_truth_answer="Refunds for unused months are available within 30 days of purchase for annual plans.",
            ground_truth_sources=["refund_policy_v2.pdf#section4"],
            retrieved_source_ids=["refund_policy_v2.pdf#section4"],
            latency_ms=420,
        ),
        RAGSample(
            question="Can I get a refund if my subscription was not cancelled?",
            generated_answer="Yes, you can always get a full refund for any reason at any time regardless of plan.",
            retrieved_contexts=["Cancellations take effect at the end of the billing period."],
            ground_truth_answer="Refunds for missed cancellations depend on when the cancellation request was submitted.",
            ground_truth_sources=["refund_policy_v2.pdf#section4", "subscription_terms_v4.pdf#section3"],
            retrieved_source_ids=["subscription_terms_v4.pdf#section3"],
            latency_ms=890,
        ),
        RAGSample(
            question="What compensation do I get if the SLA is breached?",
            generated_answer="You get 50% off your next month's bill if there is any downtime.",
            retrieved_contexts=["Our platform guarantees 99.9% monthly uptime."],
            ground_truth_answer="Service credits equal to 10x the downtime hours as a percentage of the monthly fee.",
            ground_truth_sources=["sla_agreement_v6.pdf#section4"],
            retrieved_source_ids=[],
            latency_ms=1200,
        ),
        RAGSample(
            question="How do I reset my password?",
            generated_answer="Click Forgot Password on the login page, enter your email, and follow the reset link. Links expire after 24 hours.",
            retrieved_contexts=["Click Forgot Password on the login page, enter your email address, and follow the link sent to your inbox. Links expire after 24 hours."],
            ground_truth_answer="Click Forgot Password, enter your email, follow the reset link.",
            ground_truth_sources=["security_policy_v4.pdf#section1"],
            retrieved_source_ids=["security_policy_v4.pdf#section1"],
            latency_ms=310,
        ),
    ]

    evaluator = CRMRagEvaluator()
    report = evaluator.evaluate(samples)

    # Rich table
    table = Table(title="CRM RAG Evaluation Results", show_lines=True)
    table.add_column("Sample", style="cyan")
    table.add_column("Groundedness")
    table.add_column("Halluc. Risk")
    table.add_column("Overall")
    table.add_column("Business Risk", style="bold")

    risk_styles = {
        "low": "green", "medium": "yellow",
        "high": "red", "critical": "bold red"
    }

    for r in report.results:
        style = risk_styles.get(r.risk.risk_level.value, "white")
        table.add_row(
            r.metrics.sample_id,
            f"{r.metrics.groundedness:.3f}",
            f"{r.metrics.hallucination_risk:.3f}",
            f"{r.metrics.overall_score:.3f}",
            f"[{style}]{r.risk.risk_level.value.upper()}[/{style}]",
        )

    console.print(table)
    console.print(f"\n[bold]{report.summary()}[/bold]")

    out = "crm_rag_eval_demo_report.html"
    evaluator.report(report, out)
    rprint(f"\n[green]✓ HTML report saved to {out}[/green]")


@ds.command("list")
def datasets_list():
    """List available synthetic datasets."""
    table = Table(title="Available Datasets")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Domains")
    table.add_column("Size")
    table.add_column("Command")
    table.add_row("faq",     "FAQ Q&A",         "billing, returns, sla, account_access, product_support", "50 items (10 per domain)", "crm-rag-eval datasets show faq")
    table.add_row("tickets", "Support Tickets",  "billing, returns, sla, account_access, product_support", "20 tickets",               "crm-rag-eval datasets show tickets")
    console.print(table)


@ds.command("show")
def datasets_show(
    name: str = typer.Argument(..., help="Dataset name: faq | tickets"),
    domain: str = typer.Option(None, help="Filter by domain"),
    limit: int = typer.Option(5, help="Max items to show"),
):
    """Preview a synthetic dataset."""
    if name == "faq":
        from .datasets.faq import load_faq_dataset
        items = load_faq_dataset(domains=[domain] if domain else None)[:limit]
        table = Table(title=f"FAQ Dataset (showing {len(items)})")
        table.add_column("ID", style="cyan")
        table.add_column("Domain")
        table.add_column("Risk")
        table.add_column("Question")
        table.add_column("Answer")
        for item in items:
            table.add_row(item.id, item.domain, item.risk_level,
                          item.question[:60], item.answer[:80])
        console.print(table)

    elif name == "tickets":
        from .datasets.tickets import load_ticket_dataset
        items = load_ticket_dataset(categories=[domain] if domain else None)[:limit]
        table = Table(title=f"Ticket Dataset (showing {len(items)})")
        table.add_column("ID", style="cyan")
        table.add_column("Priority")
        table.add_column("Category")
        table.add_column("Risk")
        table.add_column("Subject")
        for item in items:
            table.add_row(item.id, item.priority, item.category, item.risk_level, item.subject)
        console.print(table)

    else:
        rprint(f"[red]Unknown dataset: {name}. Use: faq | tickets[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
