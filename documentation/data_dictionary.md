# Data Dictionary

This document describes all variables used throughout the project.

---

# OpenAlex Dataset

**Dataset:** `data/raw/openalex_ai_papers.csv`

**Source:** OpenAlex API

**Unit of Analysis:** One row represents one AI-related research publication.

| Column                | Type    | Description                                                       |
| --------------------- | ------- | ----------------------------------------------------------------- |
| `openalex_id`         | String  | Unique identifier assigned by OpenAlex to each publication.       |
| `doi`                 | String  | Digital Object Identifier (DOI) of the publication.               |
| `title`               | String  | Title of the publication.                                         |
| `publication_year`    | Integer | Year the publication was released.                                |
| `publication_date`    | Date    | Full publication date (YYYY-MM-DD).                               |
| `type`                | String  | Publication type (article, preprint, review, book chapter, etc.). |
| `cited_by_count`      | Integer | Total number of citations received by the publication.            |
| `is_open_access`      | Boolean | Indicates whether the publication is openly accessible.           |
| `authors`             | String  | Semicolon-separated list of publication authors.                  |
| `countries`           | String  | ISO country codes representing author affiliations.               |
| `institutions`        | String  | Institutions affiliated with the publication authors.             |
| `concepts`            | String  | Research concepts assigned by OpenAlex.                           |
| `countries_count`     | Integer | Number of unique countries represented in the publication.        |
| `institutions_count`  | Integer | Number of unique institutions represented in the publication.     |
| `authors_count`       | Integer | Number of publication authors.                                    |
| `download_date`       | Date    | Date on which the dataset was downloaded.                         |
| `download_batch_year` | Integer | Publication year batch used during data collection.               |

---

# World Bank Dataset

**Dataset:** `data/raw/worldbank_indicators.csv`

**Source:** World Bank API

**Unit of Analysis:** One row represents one country in one year.

| Column                              | Type    | Description                                                                    |
| ----------------------------------- | ------- | ------------------------------------------------------------------------------ |
| `country_name`                      | String  | Official World Bank country or economy name.                                   |
| `country_code`                      | String  | ISO-3 country code.                                                            |
| `year`                              | Integer | Observation year.                                                              |
| `gdp_current_usd`                   | Float   | Gross Domestic Product in current US dollars.                                  |
| `population`                        | Float   | Total population.                                                              |
| `rd_expenditure_percent_gdp`        | Float   | Gross domestic expenditure on research and development as a percentage of GDP. |
| `education_expenditure_percent_gdp` | Float   | Government expenditure on education as a percentage of GDP.                    |
| `internet_users_percent`            | Float   | Percentage of the population using the Internet.                               |
| `gdp_per_capita_current_usd`        | Float   | Gross Domestic Product per capita in current US dollars.                       |

---

# Notes

* The OpenAlex dataset contains **publication-level observations**, where each row represents one research publication.
* The World Bank dataset contains **country-year observations**, where each row represents one country in one year.
* The datasets remain separate during the data acquisition and cleaning stages.
* They will be merged only after aggregating the publication-level data into country-year observations.
