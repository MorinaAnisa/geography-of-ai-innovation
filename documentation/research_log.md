# Research Log

---

## June 25

### Switched from Semantic Scholar to OpenAlex

**Decision**

Use OpenAlex as the primary publication data source instead of Semantic Scholar.

**Reason**

OpenAlex provides richer publication metadata, better author and institution information, citation counts, and unrestricted API access.

---

## June 25

### Changed sampling strategy

**Decision**

Download a balanced sample of publications from each year (2016–2025) instead of downloading the first 50,000 available records.

**Reason**

This reduces temporal bias and ensures that all publication years are represented equally in the analysis.

---

## June 26

### Selected World Bank as the socioeconomic data source

**Decision**

Use the World Bank API to obtain national indicators including GDP, GDP per capita, population, internet usage, R&D expenditure, and education expenditure.

**Reason**

The World Bank provides standardized, internationally comparable indicators with broad country coverage.

---

## June 26

### Aggregate publications by country and year

**Decision**

Transform publication-level OpenAlex records into country-year observations before merging with the World Bank dataset.

**Reason**

The World Bank data is reported at the country-year level, requiring the publication data to be aggregated to the same level of analysis.

---

## June 27

### Standardize country identifiers

**Decision**

Convert OpenAlex ISO-2 country codes to ISO-3 format before merging datasets.

**Reason**

The World Bank dataset uses ISO-3 country codes. Standardizing country identifiers ensures accurate dataset integration.

---

## June 27

### Exclude aggregate regions from World Bank data

**Decision**

Remove regional and aggregate entries (e.g., "World", "High Income", "European Union") from the dataset.

**Reason**

The study focuses exclusively on individual countries.

---

## June 28

### Handle missing values through complete-case analysis

**Decision**

Use complete observations for the multiple regression model.

**Reason**

Several socioeconomic indicators contain substantial missing values. Restricting the regression to complete observations avoids introducing bias through imputation.

---

## June 29

### Evaluate AI productivity using multiple indicators

**Decision**

Measure AI research performance using:
- Number of publications
- Average citations per paper
- AI papers per million inhabitants

**Reason**

Publication count alone does not capture research quality or productivity relative to population size.

---

## June 30

### Include both machine learning and statistical regression

**Decision**

Use both scikit-learn and statsmodels.

**Reason**

Scikit-learn provides predictive modeling and standardized coefficients, while statsmodels provides statistical inference including p-values, confidence intervals, F-statistics, and adjusted R².

---

## June 30

### Assess multicollinearity

**Decision**

Calculate Variance Inflation Factors (VIF) for all predictors before interpreting regression coefficients.

**Reason**

This ensures that highly correlated predictors do not distort coefficient estimates.

---

## June 30

### Standardize regression coefficients

**Decision**

Standardize both the predictor variables and the response variable before comparing regression coefficients.

**Reason**

Standardized coefficients allow direct comparison of the relative importance of predictors measured on different scales.

---