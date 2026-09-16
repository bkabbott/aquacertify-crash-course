#!/usr/bin/env bash
# One-time setup: creates a private Python folder (.venv) and installs the
# two add-ons the course uses: mysql-connector-python and openpyxl.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "==> creating .venv with $(python3 --version)"
  python3 -m venv .venv
fi
echo "==> installing add-ons"
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

echo
echo "All set. Each time you open a terminal here, run:"
echo "    source .venv/bin/activate"
echo "Then try:"
echo "    python3 scripts/01_connect.py"
