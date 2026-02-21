# src/report.py
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CLEANED = BASE / "data" / "cleaned" / "combined_cleaned.csv"
OUT_DIR = BASE / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def make_report():
    if not CLEANED.exists():
        print("Cleaned data not found. Run src/clean.py first (or run ./run.sh).")
        return

    df = pd.read_csv(CLEANED, parse_dates=['date'])
    # Example aggregations: daily totals and simple engagement rate
    df['date_only'] = df['date'].dt.date
    agg = df.groupby('date_only').agg({
        'impressions': 'sum' if 'impressions' in df.columns else 'count',
        'engagement': 'sum' if 'engagement' in df.columns else 'count'
    }).reset_index().rename(columns={'date_only': 'date'})

    # Add engagement rate safely
    if 'impressions' in agg.columns and 'engagement' in agg.columns:
        agg['engagement_rate'] = (agg['engagement'] / agg['impressions']).fillna(0)

    report_path = OUT_DIR / "weekly_report.xlsx"
    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        agg.to_excel(writer, sheet_name="Daily Summary", index=False)
        df.to_excel(writer, sheet_name="Raw Data", index=False)

        # add a short summary sheet
        summary = {
            'total_rows': [len(df)],
            'total_impressions': [int(df['impressions'].sum())] if 'impressions' in df.columns else [None],
            'total_engagement': [int(df['engagement'].sum())] if 'engagement' in df.columns else [None]
        }
        pd.DataFrame(summary).to_excel(writer, sheet_name="Summary", index=False)

    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    make_report()