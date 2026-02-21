# src/clean.py
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE / "data"
OUT_DIR = BASE / "data" / "cleaned"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names, parse dates, drop rows with no date,
    remove duplicates by ('post_id','date') if post_id exists,
    convert numeric fields and fill missing with 0.
    """
    # standardize column names
    df = df.rename(columns=lambda c: c.strip().lower())

    # common renames
    col_map = {}
    for candidate in ['postid', 'post_id', 'id']:
        if candidate in df.columns:
            col_map[candidate] = 'post_id'
    for candidate in ['imprs', 'impressions', 'views']:
        if candidate in df.columns:
            col_map[candidate] = 'impressions'
    for candidate in ['eng', 'engagement', 'likes']:
        if candidate in df.columns:
            col_map[candidate] = 'engagement'
    df = df.rename(columns=col_map)

    # parse dates robustly
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    else:
        possible = [c for c in df.columns if 'date' in c or 'time' in c or 'created' in c]
        if possible:
            df['date'] = pd.to_datetime(df[possible[0]], errors='coerce')

    # drop rows with no parsable date
    df = df.dropna(subset=['date'])

    # remove duplicates if post_id exists
    if 'post_id' in df.columns:
        df = df.drop_duplicates(subset=['post_id', 'date'])

    # ensure numeric columns
    for col in ['impressions', 'engagement']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # sort by date
    df = df.sort_values(by='date').reset_index(drop=True)
    return df

def clean_all() -> pd.DataFrame:
    """
    Read CSVs in data/, normalize each, and output combined CSV in data/cleaned/
    """
    files = sorted(INPUT_DIR.glob("*.csv"))
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception as e:
            print(f"WARNING: failed to read {f}: {e}")
            continue
        df_clean = normalize(df)
        dfs.append(df_clean)

    if not dfs:
        print("No CSV files found or no data after cleaning.")
        return pd.DataFrame()

    combined = pd.concat(dfs, ignore_index=True)
    out_path = OUT_DIR / "combined_cleaned.csv"
    combined.to_csv(out_path, index=False)
    print(f"Cleaned combined CSV written to: {out_path}  (rows: {len(combined)})")
    return combined

if __name__ == "__main__":
    clean_all()