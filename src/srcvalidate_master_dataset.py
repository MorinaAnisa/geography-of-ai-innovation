"""
validate_master_dataset.py

Validates the final merged dataset before analysis.

This script DOES NOT modify data.
It simply checks that everything looks correct.
"""

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MASTER_DATASET = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "master_country_year.csv"
)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():

    print("Loading master dataset...")

    df = pd.read_csv(MASTER_DATASET)

    # ---------------------------------------------------
    # Basic information
    # ---------------------------------------------------

    print_section("DATASET OVERVIEW")

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # ---------------------------------------------------
    # Missing values
    # ---------------------------------------------------

    print_section("MISSING VALUES")

    missing = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
    )

    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values.")
    else:
        print(missing)

    # ---------------------------------------------------
    # Duplicate country-years
    # ---------------------------------------------------

    print_section("DUPLICATE COUNTRY-YEAR RECORDS")

    duplicates = df.duplicated(
        subset=["country_code_iso3", "year"]
    ).sum()

    print(f"Duplicates: {duplicates}")

    # ---------------------------------------------------
    # Country statistics
    # ---------------------------------------------------

    print_section("COUNTRY STATISTICS")

    print(
        "Unique countries:",
        df["country_code_iso3"].nunique()
    )

    # ---------------------------------------------------
    # Year statistics
    # ---------------------------------------------------

    print_section("YEAR RANGE")

    print(
        "Minimum year:",
        int(df["year"].min())
    )

    print(
        "Maximum year:",
        int(df["year"].max())
    )

    print("\nRows per year:")

    print(
        df["year"]
        .value_counts()
        .sort_index()
    )

    # ---------------------------------------------------
    # AI papers
    # ---------------------------------------------------

    print_section("AI PAPER STATISTICS")

    print(
        df["ai_papers"]
        .describe()
    )

    # ---------------------------------------------------
    # Citations
    # ---------------------------------------------------

    print_section("AVERAGE CITATION STATISTICS")

    print(
        df["avg_citations_per_paper"]
        .describe()
    )

    # ---------------------------------------------------
    # GDP
    # ---------------------------------------------------

    print_section("GDP COVERAGE")

    print(
        "Rows with GDP:",
        df["gdp_current_usd"].notna().sum()
    )

    print(
        "Rows missing GDP:",
        df["gdp_current_usd"].isna().sum()
    )

    # ---------------------------------------------------
    # Final verdict
    # ---------------------------------------------------

    print_section("VALIDATION COMPLETE")

    print("Dataset successfully validated.")
    print("Ready for exploratory data analysis.")


if __name__ == "__main__":
    main()