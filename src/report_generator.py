# report_generator.py
import pandas as pd
import os
from datetime import datetime

def generate_summary_report(report_folder="reports", output_file=None):
    """
    Combines all CSV reports from the validator into a single summary Excel file.
    """
    os.makedirs(report_folder, exist_ok=True)
    csv_files = [f for f in os.listdir(report_folder) if f.endswith(".csv")]
    
    if not csv_files:
        print("No CSV reports found in folder.")
        return

    summary_data = []

    for file in csv_files:
        df = pd.read_csv(os.path.join(report_folder, file))
        summary_data.append({
            "report_name": file,
            "num_records": len(df),
            "columns": ", ".join(df.columns)
        })

    summary_df = pd.DataFrame(summary_data)

    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_file = os.path.join(report_folder, f"summary_report_{timestamp}.csv")

    summary_df.to_csv(output_file, index=False)
    print(f"Summary report generated: {output_file}")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    generate_summary_report()
