#!/usr/bin/env python3
"""
Upload the crm-rag-eval synthetic FAQ dataset to HuggingFace Hub.

Usage:
    pip install huggingface_hub datasets
    export HF_TOKEN=hf_your_token_here
    python scripts/upload_to_huggingface.py

Your HF token: https://huggingface.co/settings/tokens
Set namespace below to your HF username (e.g. "chitrapradha" or "chitralabs")
"""

import os
import json
from pathlib import Path

HF_NAMESPACE = "chitralabs"          # ← change to your HF username/org
DATASET_NAME = "crm-rag-eval-faq"   # the dataset repo name on HF

def main():
    try:
        from huggingface_hub import HfApi, create_repo
        import datasets
    except ImportError:
        print("Install with: pip install huggingface_hub datasets")
        raise

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise EnvironmentError("Set HF_TOKEN environment variable first.\nGet one at: https://huggingface.co/settings/tokens")

    api = HfApi()
    repo_id = f"{HF_NAMESPACE}/{DATASET_NAME}"

    # 1. Create the dataset repo on HF (idempotent)
    print(f"Creating dataset repo: {repo_id}")
    try:
        create_repo(repo_id=repo_id, repo_type="dataset", token=token, exist_ok=True)
        print(f"  ✓ Repo ready at https://huggingface.co/datasets/{repo_id}")
    except Exception as e:
        print(f"  Repo creation: {e}")

    # 2. Upload the dataset card (README.md with YAML frontmatter)
    readme_path = Path(__file__).parent.parent / "datasets" / "README.md"
    print(f"Uploading dataset card from {readme_path}")
    api.upload_file(
        path_or_fileobj=str(readme_path),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
    )
    print("  ✓ Dataset card uploaded")

    # 3. Build and upload the actual data as Parquet (HF standard)
    sys_path_fix = str(Path(__file__).parent.parent / "src")
    import sys; sys.path.insert(0, sys_path_fix)
    from crm_rag_eval.datasets.faq import load_faq_as_dicts

    items = load_faq_as_dicts()
    print(f"  Loading {len(items)} FAQ items...")

    # Convert to HF Dataset and save as Parquet
    import datasets as hf_datasets
    ds = hf_datasets.Dataset.from_list(items)

    # Save locally as parquet first
    parquet_path = Path("/tmp/crm_rag_eval_faq.parquet")
    ds.to_parquet(str(parquet_path))
    print(f"  Saved {len(items)} rows to {parquet_path}")

    # Upload the parquet file
    api.upload_file(
        path_or_fileobj=str(parquet_path),
        path_in_repo="data/train-00000-of-00001.parquet",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
    )
    print("  ✓ Data uploaded as Parquet")

    # 4. Upload ticket dataset too
    from crm_rag_eval.datasets.tickets import load_ticket_dataset
    tickets = load_ticket_dataset()
    ticket_dicts = [
        {
            "id": t.id, "priority": t.priority, "category": t.category,
            "subject": t.subject, "body": t.body,
            "expected_resolution": t.expected_resolution,
            "resolution_steps": t.resolution_steps,
            "risk_level": t.risk_level, "tags": t.tags,
        }
        for t in tickets
    ]
    ds_tickets = hf_datasets.Dataset.from_list(ticket_dicts)
    ticket_parquet = Path("/tmp/crm_rag_eval_tickets.parquet")
    ds_tickets.to_parquet(str(ticket_parquet))
    api.upload_file(
        path_or_fileobj=str(ticket_parquet),
        path_in_repo="data/tickets-00000-of-00001.parquet",
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
    )
    print(f"  ✓ Ticket dataset uploaded ({len(ticket_dicts)} tickets)")

    print(f"\n✅ Done! Dataset live at:")
    print(f"   https://huggingface.co/datasets/{repo_id}")
    print(f"\nDownload counter starts now. Share this URL for EB-1A evidence.")


if __name__ == "__main__":
    main()
