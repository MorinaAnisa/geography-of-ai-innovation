import time
import requests
import pandas as pd
from pathlib import Path
from datetime import date

BASE_URL = "https://api.openalex.org/works"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "openalex_ai_papers.csv"

# We download a balanced sample from each year.
YEARS = range(2016, 2026)

# Start with 1000 per year = 10,000 total.
# Later you can increase to 2000 per year.
RECORDS_PER_YEAR = 1000

# OpenAlex allows up to 200 records per page.
PER_PAGE = 200

# OpenAlex concept ID for Artificial Intelligence.
AI_CONCEPT_ID = "C154945302"

# Optional, but recommended. Put your email here.
MAILTO = ""


def extract_paper_info(work, download_year):
    """
    This function takes one paper record from OpenAlex
    and keeps only the columns we need for analysis.
    """

    authorships = work.get("authorships", [])

    countries = set()
    institutions = set()
    authors = []

    for authorship in authorships:
        author = authorship.get("author", {})

        if author.get("display_name"):
            authors.append(author["display_name"])

        for institution in authorship.get("institutions", []):
            if institution.get("display_name"):
                institutions.add(institution["display_name"])

            if institution.get("country_code"):
                countries.add(institution["country_code"])

    concepts = [
        concept.get("display_name")
        for concept in work.get("concepts", [])
        if concept.get("display_name")
    ]

    return {
        "openalex_id": work.get("id"),
        "doi": work.get("doi"),
        "title": work.get("display_name"),
        "publication_year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "type": work.get("type"),
        "cited_by_count": work.get("cited_by_count"),
        "is_open_access": work.get("open_access", {}).get("is_oa"),

        # These are stored as semicolon-separated text for now.
        "authors": "; ".join(authors),
        "countries": "; ".join(sorted(countries)),
        "institutions": "; ".join(sorted(institutions)),
        "concepts": "; ".join(concepts),

        # These will help us later with collaboration analysis.
        "countries_count": len(countries),
        "institutions_count": len(institutions),
        "authors_count": len(authors),

        # Reproducibility metadata.
        "download_date": date.today().isoformat(),
        "download_batch_year": download_year,
    }


def download_year(year):
    """
    Downloads papers for one specific year.
    This gives us a balanced dataset instead of only the top search results.
    """

    rows = []
    cursor = "*"
    downloaded = 0

    params = {
        # We filter by AI concept and publication year.
        "filter": f"concepts.id:{AI_CONCEPT_ID},publication_year:{year},language:en",

        "per-page": PER_PAGE,

        # We only request the fields we need.
        # This makes each API response smaller and cleaner.
        "select": (
            "id,doi,display_name,publication_year,publication_date,type,"
            "cited_by_count,open_access,authorships,concepts"
        ),
    }

    if MAILTO:
        params["mailto"] = MAILTO

    print(f"\nDownloading year {year}...")

    while downloaded < RECORDS_PER_YEAR:
        params["cursor"] = cursor

        response = requests.get(BASE_URL, params=params, timeout=60)

        if response.status_code == 429:
            print("Rate limit reached. Stop for today and continue tomorrow.")
            break

        if response.status_code != 200:
            print("Request failed.")
            print("Status:", response.status_code)
            print(response.text)
            break

        data = response.json()
        works = data.get("results", [])

        if not works:
            print(f"No more results for {year}.")
            break

        for work in works:
            rows.append(extract_paper_info(work, year))

        downloaded += len(works)
        cursor = data.get("meta", {}).get("next_cursor")

        print(f"{year}: downloaded {downloaded} records")

        if cursor is None:
            break

        # Small pause so we do not hammer the API.
        time.sleep(0.5)

    return rows[:RECORDS_PER_YEAR]


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_rows = []

    for year in YEARS:
        year_rows = download_year(year)
        all_rows.extend(year_rows)

    df = pd.DataFrame(all_rows)

    if not df.empty:
        df.drop_duplicates(subset=["openalex_id"], inplace=True)

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("\nDone!")
    print(f"Saved {len(df)} rows to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()