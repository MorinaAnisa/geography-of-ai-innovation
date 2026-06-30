"""
clean_data.py

Cleans the raw OpenAlex and World Bank datasets.

Important:
- This script does NOT merge the datasets.
- It does NOT overwrite raw data.
- It saves cleaned versions into data/processed/.
"""

import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OPENALEX_RAW = PROJECT_ROOT / "data" / "raw" / "openalex_ai_papers.csv"
WORLDBANK_RAW = PROJECT_ROOT / "data" / "raw" / "worldbank_indicators.csv"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OPENALEX_CLEAN = PROCESSED_DIR / "openalex_clean.csv"
WORLDBANK_CLEAN = PROCESSED_DIR / "worldbank_clean.csv"


def clean_openalex(df):
    """
    Cleans OpenAlex publication-level data.
    """

    df = df.copy()

    # Remove full duplicate rows, just in case.
    df = df.drop_duplicates()

    # Remove duplicate OpenAlex IDs.
    df = df.drop_duplicates(subset=["openalex_id"])

    # Strip whitespace from text columns.
    text_columns = [
        "openalex_id", "doi", "title", "type", "authors",
        "countries", "institutions", "concepts", "download_date"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Convert dates.
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")
    df["download_date"] = pd.to_datetime(df["download_date"], errors="coerce")

    # Convert numeric columns.
    numeric_columns = [
        "publication_year", "cited_by_count", "countries_count",
        "institutions_count", "authors_count", "download_batch_year"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep only expected years.
    df = df[df["publication_year"].between(2016, 2025)]

    # Remove rows without OpenAlex ID or publication year.
    df = df.dropna(subset=["openalex_id", "publication_year"])

    return df


def clean_worldbank(df):
    """
    Cleans World Bank country-year data.
    """

    df = df.copy()

    # Remove full duplicate rows.
    df = df.drop_duplicates()

    # Strip whitespace from text columns.
    for col in ["country_name", "country_code"]:
        df[col] = df[col].astype("string").str.strip()

    # Convert year and numeric columns.
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    numeric_columns = [
        "gdp_current_usd",
        "population",
        "rd_expenditure_percent_gdp",
        "education_expenditure_percent_gdp",
        "internet_users_percent",
        "gdp_per_capita_current_usd",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep only expected years.
    df = df[df["year"].between(2016, 2025)]

    # Remove rows without country code.
    df = df.dropna(subset=["country_code"])

    # Remove World Bank aggregate regions.
    # These are not individual countries and would distort country-level analysis.
    aggregate_codes = {
        "AFE", "AFW", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA",
        "ECS", "EMU", "EUU", "FCS", "HIC", "HPC", "IBD", "IBT", "IDA",
        "IDB", "IDX", "INX", "LAC", "LCN", "LDC", "LIC", "LMC", "LMY",
        "LTE", "MEA", "MIC", "MNA", "NAC", "OED", "OSS", "PRE", "PSS",
        "PST", "SAS", "SSA", "SSF", "SST", "TEA", "TEC", "TLA", "TMN",
        "TSA", "TSS", "UMC", "WLD"
    }

    df = df[~df["country_code"].isin(aggregate_codes)]

    return df


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw datasets...")
    openalex_df = pd.read_csv(OPENALEX_RAW)
    worldbank_df = pd.read_csv(WORLDBANK_RAW)

    print("Cleaning OpenAlex data...")
    openalex_clean = clean_openalex(openalex_df)

    print("Cleaning World Bank data...")
    worldbank_clean = clean_worldbank(worldbank_df)

    openalex_clean.to_csv(OPENALEX_CLEAN, index=False, encoding="utf-8")
    worldbank_clean.to_csv(WORLDBANK_CLEAN, index=False, encoding="utf-8")

    print("\nCleaning complete.")
    print(f"OpenAlex cleaned rows: {len(openalex_clean)}")
    print(f"World Bank cleaned rows: {len(worldbank_clean)}")
    print("\nSaved files:")
    print(OPENALEX_CLEAN)
    print(WORLDBANK_CLEAN)


if __name__ == "__main__":
    main()