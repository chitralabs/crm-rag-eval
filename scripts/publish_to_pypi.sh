#!/bin/bash
# Manual PyPI publish script (fallback if OIDC isn't set up yet)
# Run this locally with your PyPI API token.
#
# Usage:
#   export PYPI_TOKEN=pypi-your-token-here
#   bash scripts/publish_to_pypi.sh

set -e

echo "Building crm-rag-eval..."
pip install build twine -q
python -m build

echo "Checking package..."
python -m twine check dist/*

echo "Uploading to PyPI..."
python -m twine upload dist/* \
  --username __token__ \
  --password "$PYPI_TOKEN" \
  --non-interactive

echo "Done! https://pypi.org/project/crm-rag-eval/"
