import requests
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "worldbank_indicators.csv"

YEARS = range(2016, 2026)

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "SP.POP.TOTL": "population",
    "GB.XPD.RSDV.GD.ZS": "rd_expenditure_percent_gdp",
    "SE.XPD.TOTL.GD.ZS": "education_expenditure_percent_gdp",
    "IT.NET.USER.ZS": "internet_users_percent",
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
}


def fetch_indicator(indicator_code, indicator_name):
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/"
        f"{indicator_code}?format=json&per_page=20000"
    )

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        print(f"Failed to fetch {indicator_name}")
        return pd.DataFrame()

    data = response.json()

    if len(data) < 2:
        return pd.DataFrame()

    rows = []

    for item in data[1]:
        year = int(item["date"])

        if year in YEARS:
            rows.append({
                "country_name": item["country"]["value"],
                "country_code": item["countryiso3code"],
                "year": year,
                indicator_name: item["value"],
            })

    return pd.DataFrame(rows)


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    final_df = None

    for code, name in INDICATORS.items():
        print(f"Downloading {name}...")
        df = fetch_indicator(code, name)

        if final_df is None:
            final_df = df
        else:
            final_df = final_df.merge(
                df,
                on=["country_name", "country_code", "year"],
                how="outer"
            )

    final_df.sort_values(["country_name", "year"], inplace=True)
    final_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("\nDone!")
    print(f"Saved {len(final_df)} rows to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()