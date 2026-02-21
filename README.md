# Automated Weekly Reporting — muzzki-reporting

Small ETL + reporting demo that cleans multi-platform CSV exports, validates data, and generates an Excel weekly report. Suitable as a demo project for QA / data pipeline work.

## What this repo does (TL;DR)
1. `src/clean.py` — reads CSVs in `data/`, normalizes columns and dates, removes duplicates, outputs `data/cleaned/combined_cleaned.csv`.
2. `src/report.py` — reads cleaned CSV and generates `output/weekly_report.xlsx` (Daily Summary, Raw Data, Summary).
3. `tests/` — basic pytest tests that validate the cleaning logic.

## Quick start (Linux / macOS)
```bash
# make sure you are in repo root
./run.sh
# run tests
pytest -q