#!/usr/bin/env bash
# run.sh - run full pipeline locally
set -e

python3 -m venv .venv || true
# activate manually if you need to
# source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

python3 src/clean.py
python3 src/report.py

echo "Pipeline finished. Check output/weekly_report.xlsx"