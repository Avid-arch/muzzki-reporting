# main.py
from pathlib import Path
import pandas as pd
import os
from datetime import datetime

# ----------------------------
# Helpers / Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def data_path(filename):
    return DATA_DIR / filename

# ----------------------------
# Validation functions
# ----------------------------
def load_data(file_path):
    return pd.read_csv(file_path)

def find_duplicates(df, key_column):
    return df[df.duplicated(subset=[key_column], keep=False)]

def find_missing_values(df):
    return df[df.isnull().any(axis=1)]

def compare_systems(df_a, df_b, key_column):
    df_a = df_a.set_index(key_column)
    df_b = df_b.set_index(key_column)

    only_in_a = df_a.loc[~df_a.index.isin(df_b.index)].reset_index()
    only_in_b = df_b.loc[~df_b.index.isin(df_a.index)].reset_index()

    common_keys = df_a.index.intersection(df_b.index)
    mismatches = []

    for key in common_keys:
        row_a = df_a.loc[key]
        row_b = df_b.loc[key]
        if not row_a.equals(row_b):
            mismatches.append({
                "id": key,
                "system_a": row_a.to_dict(),
                "system_b": row_b.to_dict()
            })

    return only_in_a, only_in_b, mismatches

def run_validation(file_a_path, file_b_path, key_column="id"):
    df_a = load_data(file_a_path)
    df_b = load_data(file_b_path)

    results = {}
    results["duplicates_a"] = find_duplicates(df_a, key_column)
    results["duplicates_b"] = find_duplicates(df_b, key_column)
    results["missing_a"] = find_missing_values(df_a)
    results["missing_b"] = find_missing_values(df_b)
    results["only_in_a"], results["only_in_b"], results["mismatches"] = compare_systems(df_a, df_b, key_column)

    return results

def save_reports(results):
    # Always ensure reports folder exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)  # <--- creates the folder if missing

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Save DataFrame-style results
    for key, value in results.items():
        if key == "mismatches":
            df = pd.DataFrame(value)
        else:
            df = value if isinstance(value, pd.DataFrame) else pd.DataFrame()
        out_file = REPORTS_DIR / f"{key}_{timestamp}.csv"
        df.to_csv(out_file, index=False)

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print("Validator running...\n")

    # filenames in your repo/data folder (adjust if you rename)
    file_a = data_path("system_a.csv")
    file_b = data_path("system_b.csv")
    key_column = "id"

    if not file_a.exists() or not file_b.exists():
        print("ERROR: data files not found. Expected:")
        print(f" - {file_a}")
        print(f" - {file_b}")
        raise SystemExit(1)

    results = run_validation(file_a, file_b, key_column)

    # summary
    print("=== VALIDATION SUMMARY ===")
    print(f"Duplicates in A: {len(results['duplicates_a'])}")
    print(f"Duplicates in B: {len(results['duplicates_b'])}")
    print(f"Missing values in A: {len(results['missing_a'])}")
    print(f"Missing values in B: {len(results['missing_b'])}")
    print(f"Records only in A: {len(results['only_in_a'])}")
    print(f"Records only in B: {len(results['only_in_b'])}")
    print(f"Mismatched records: {len(results['mismatches'])}\n")

    save_reports(results)
    print(f"Detailed CSV reports saved in '{REPORTS_DIR.resolve()}' folder.")