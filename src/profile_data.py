"""
profile_data.py

Profiles the raw OpenAlex and World Bank datasets.
This script does NOT clean or merge data.
It only creates reports so we understand the data quality first.
"""

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OPENALEX_PATH = PROJECT_ROOT / "data" / "raw" / "openalex_ai_papers.csv"
WORLDBANK_PATH = PROJECT_ROOT / "data" / "raw" / "worldbank_indicators.csv"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def profile_dataset(df, dataset_name):
    report = []

    report.append(f"DATA PROFILE REPORT: {dataset_name}")
    report.append("=" * 60)

    report.append(f"\nRows: {df.shape[0]}")
    report.append(f"Columns: {df.shape[1]}")

    report.append("\nCOLUMN TYPES")
    report.append("-" * 60)
    report.append(str(df.dtypes))

    report.append("\nMISSING VALUES")
    report.append("-" * 60)
    missing = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percent": (df.isna().mean() * 100).round(2)
    })
    report.append(str(missing.sort_values("missing_percent", ascending=False)))

    report.append("\nDUPLICATES")
    report.append("-" * 60)
    report.append(f"Full duplicate rows: {df.duplicated().sum()}")

    if "openalex_id" in df.columns:
        report.append(f"Duplicate OpenAlex IDs: {df['openalex_id'].duplicated().sum()}")

    if "doi" in df.columns:
        report.append(f"Duplicate DOIs: {df['doi'].dropna().duplicated().sum()}")

    report.append("\nNUMERIC SUMMARY")
    report.append("-" * 60)
    report.append(str(df.describe(include="number").T))

    report.append("\nCATEGORICAL SUMMARY")
    report.append("-" * 60)
    report.append(str(df.describe(include="object").T))

    return "\n".join(report)


def main():
    openalex_df = pd.read_csv(OPENALEX_PATH)
    worldbank_df = pd.read_csv(WORLDBANK_PATH)

    openalex_report = profile_dataset(openalex_df, "OpenAlex AI Papers")
    worldbank_report = profile_dataset(worldbank_df, "World Bank Indicators")

    (REPORT_DIR / "openalex_profile_report.txt").write_text(openalex_report, encoding="utf-8")
    (REPORT_DIR / "worldbank_profile_report.txt").write_text(worldbank_report, encoding="utf-8")

    print("Profiling complete.")
    print("Reports saved to:")
    print(REPORT_DIR)


if __name__ == "__main__":
    main()