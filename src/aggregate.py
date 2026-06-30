"""
aggregate_data.py

Aggregates cleaned OpenAlex publication-level data into country-year data.

Input:
- data/processed/openalex_clean.csv

Output:
- data/processed/openalex_country_year.csv
"""

import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OPENALEX_CLEAN = PROJECT_ROOT / "data" / "processed" / "openalex_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "openalex_country_year.csv"


def main():
    print("Loading cleaned OpenAlex data...")
    df = pd.read_csv(OPENALEX_CLEAN)

    print("Preparing country-level rows...")

    # Remove rows without country information.
    df = df.dropna(subset=["countries"])

    # Split semicolon-separated countries into lists.
    df["countries"] = df["countries"].astype(str).str.split(";")

    # Create one row per paper-country pair.
    # Example:
    # Paper A: US; DE
    # becomes:
    # Paper A - US
    # Paper A - DE
    exploded = df.explode("countries")

    # Clean country code spacing.
    exploded["country_code"] = exploded["countries"].astype(str).str.strip()

    # Remove empty country codes.
    exploded = exploded[
        exploded["country_code"].notna()
    ]

    exploded = exploded[
        (exploded["country_code"] != "") &
        (exploded["country_code"] != "nan")
    ]

    print("Aggregating by country and year...")

    country_year = (
        exploded
        .groupby(["country_code", "publication_year"])
        .agg(
            ai_papers=("openalex_id", "nunique"),
            total_citations=("cited_by_count", "sum"),
            avg_citations_per_paper=("cited_by_count", "mean"),
            median_citations_per_paper=("cited_by_count", "median"),
            avg_authors_per_paper=("authors_count", "mean"),
            avg_institutions_per_paper=("institutions_count", "mean"),
            international_collaboration_rate=("countries_count", lambda x: (x > 1).mean())
        )
        .reset_index()
    )

    # Rename publication_year to year so it matches World Bank later.
    country_year = country_year.rename(columns={"publication_year": "year"})

    # Round easier-to-read numeric columns.
    round_cols = [
        "avg_citations_per_paper",
        "median_citations_per_paper",
        "avg_authors_per_paper",
        "avg_institutions_per_paper",
        "international_collaboration_rate",
    ]

    country_year[round_cols] = country_year[round_cols].round(4)

    country_year.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("\nAggregation complete.")
    print(f"Saved {len(country_year)} rows to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()