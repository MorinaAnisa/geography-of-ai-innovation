# Geography of AI Innovation

An end-to-end data science project investigating how economic and technological factors influence national AI research output across the world.

The project combines publication data from the OpenAlex API with socioeconomic indicators from the World Bank API to explore global patterns of AI research productivity using data collection, cleaning, exploratory analysis, and statistical modeling.

---

# Research Question

**Which national characteristics are most strongly associated with AI research output between 2016 and 2025?**

Specifically, the project investigates whether factors such as GDP, population, internet usage, research and development expenditure, and education expenditure help explain differences in AI publication output across countries.

---

# Objectives

- Collect AI publication data using the OpenAlex API
- Collect national socioeconomic indicators from the World Bank API
- Build a reproducible data collection and preprocessing pipeline
- Analyze global AI research productivity
- Compare research output across countries
- Evaluate citation impact
- Examine AI research output relative to population size
- Investigate relationships between AI research and national indicators
- Build and interpret multiple linear regression models
- Produce reproducible visualizations and statistical findings

---

# Dataset Sources

## OpenAlex

Publication metadata including:

- AI publications
- Authors
- Institutions
- Countries
- Citation counts
- Publication dates

API:
https://api.openalex.org

---

## World Bank Open Data

National indicators including:

- GDP
- GDP per capita
- Population
- Internet users (%)
- R&D expenditure (% GDP)
- Education expenditure (% GDP)

API:
https://api.worldbank.org

---

# Methodology

The project follows a complete data science workflow:

1. Data Collection
   - Download AI publications from OpenAlex
   - Download socioeconomic indicators from the World Bank

2. Data Preparation
   - Data cleaning
   - Country code harmonization
   - Missing value handling
   - Dataset validation
   - Aggregation by country and year

3. Exploratory Data Analysis
   - AI publications by country
   - AI papers per million inhabitants
   - Citation analysis
   - GDP vs AI output
   - Correlation analysis

4. Statistical Analysis
   - Pearson correlation
   - Multiple Linear Regression
   - OLS Regression
   - Variance Inflation Factor (VIF)
   - Standardized regression coefficients

---

# Key Findings

- GDP is the strongest predictor of national AI research output.
- The multiple regression model explains approximately **87%** of the variation in AI publication output (**R² = 0.873**).
- Internet penetration shows a small but statistically significant positive association with AI research productivity.
- Population exhibits a small negative association after controlling for GDP.
- R&D expenditure and education expenditure were not statistically significant within the available dataset.

---

# Repository Structure

```text
geography-of-ai-innovation/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── documentation/
│
├── notebooks/
│
├── reports/
│
├── src/
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

# Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- scikit-learn
- statsmodels
- Jupyter Notebook
- OpenAlex API
- World Bank API
- Git

---

# Reproducibility

To reproduce this project:

1. Clone the repository.
2. Install the required dependencies.
3. Run the data collection scripts.
4. Execute the data cleaning pipeline.
5. Run the exploratory analysis notebook.

---

# Future Work

Potential extensions include:

- Incorporating UNESCO R&D datasets
- Including WIPO AI patent data
- Expanding to the complete OpenAlex dataset
- Applying panel regression models
- Building an interactive dashboard
- Creating global choropleth maps of AI research activity

---

# Author

**Anisa Morina**

Applied IT Student

Data Science • Artificial Intelligence • Machine Learning