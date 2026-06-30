import pandas as pd
import pycountry
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OPENALEX_COUNTRY_YEAR = PROJECT_ROOT / "data" / "processed" / "openalex_country_year.csv"
WORLDBANK_CLEAN = PROJECT_ROOT / "data" / "processed" / "worldbank_clean.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "master_country_year.csv"


def iso2_to_iso3(code):
    if pd.isna(code):
        return None

    code = str(code).strip().upper()

    try:
        country = pycountry.countries.get(alpha_2=code)
        return country.alpha_3 if country else None
    except Exception:
        return None


def main():
    print("Loading datasets...")

    openalex = pd.read_csv(OPENALEX_COUNTRY_YEAR)
    worldbank = pd.read_csv(WORLDBANK_CLEAN)

    print("Converting OpenAlex ISO-2 country codes to ISO-3...")

    openalex["country_code_iso3"] = openalex["country_code"].apply(iso2_to_iso3)

    missing_codes = (
        openalex[openalex["country_code_iso3"].isna()]["country_code"]
        .dropna()
        .unique()
    )

    if len(missing_codes) > 0:
        print("\nWarning: Some OpenAlex country codes were not mapped:")
        print(missing_codes)
    else:
        print("All OpenAlex country codes mapped successfully.")

    print("Merging datasets...")

    master = openalex.merge(
        worldbank,
        left_on=["country_code_iso3", "year"],
        right_on=["country_code", "year"],
        how="left"
    )

    master.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("\nMerge complete.")
    print(f"Saved {len(master)} rows to:")
    print(OUTPUT_PATH)

    print("\nRows with matched World Bank data:")
    print(master["country_name"].notna().sum())

    print("\nRows without matched World Bank data:")
    print(master["country_name"].isna().sum())


if __name__ == "__main__":
    main()