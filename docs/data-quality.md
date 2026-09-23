# Data Quality

## Purpose

This document defines the initial data quality checks and observations for MOEX market data ingestion.

The current rules are based on exploratory analysis of the MOEX ISS historical data endpoint and will be expanded as more dates, instruments and data sources are investigated.

## Initial Dataset

The first exploratory dataset was retrieved from:

- Engine: `currency`
- Market: `selt`
- Board: `CETS`
- Endpoint: MOEX ISS historical securities data
- Trade date: `2026-08-21`

The API returned 200 records in total. The data was retrieved through two pages with a page size of 100 records.

## Data Quality Checks

### 1. Exact duplicate rows

All columns were checked for completely identical rows.

**Result for `2026-08-21`:**

- Records: 200
- Exact duplicate rows: 0

**Initial rule:**

Exact duplicate rows are considered technical duplicates and should not be retained in the curated dataset.

This rule applies only to fully identical rows. Records with the same instrument and date but different field values require separate investigation.

### 2. Missing values

Missing values were profiled by column rather than treated as a single generic data quality problem.

For the initial dataset:

| Column      | Missing values |
| ----------- | -------------: |
| `BOARDID`   |              0 |
| `TRADEDATE` |              0 |
| `SHORTNAME` |              0 |
| `SECID`     |              0 |
| `OPEN`      |              0 |
| `LOW`       |              0 |
| `HIGH`      |              0 |
| `CLOSE`     |              0 |
| `NUMTRADES` |              0 |
| `WAPRICE`   |            177 |

Missing values must be interpreted according to the semantic meaning of the corresponding field. A missing value is not automatically considered a data quality error.

### 3. `NUMTRADES` / `WAPRICE` consistency

The initial dataset was checked for consistency between the number of trades and the weighted average price.

Observed results:

- Records with `NUMTRADES > 0`: 23
- Records with `NUMTRADES > 0` and missing `WAPRICE`: 0
- Records with `NUMTRADES = 0` and non-missing `WAPRICE`: 0
- Records with `NUMTRADES = 0` and missing `WAPRICE`: 177

The observed data is therefore internally consistent:

```text
NUMTRADES > 0
    → WAPRICE is present

NUMTRADES = 0
    → WAPRICE is missing
```

This relationship is currently treated as an observed data consistency pattern rather than a fully validated business rule. It must be checked across additional trading dates before being promoted to a mandatory DQ rule.

### 4. Dataset grain

The dataset grain was validated across 4 trading dates:

- `2026-08-18`
- `2026-08-19`
- `2026-08-20`
- `2026-08-21`

The resulting dataset contained 800 records.

Observed results:

- Unique `SECID + TRADEDATE` combinations: 800
- Duplicate `SECID + TRADEDATE` combinations: 0
- Records per trading date: 200

Based on this validation, the dataset grain is:

> One record represents one instrument (`SECID`) for one trading date (`TRADEDATE`).

This grain is validated for the tested historical sample and will be revalidated as the ingestion scope expands.

### Automated DQ checks

Basic data quality checks are implemented as reusable validation functions.

The current checks cover:

- exact duplicate rows;
- duplicate `SECID + TRADEDATE` combinations;
- consistency between `NUMTRADES` and `WAPRICE`;
- required columns;
- unexpected columns.

The validation layer reports data quality results separately from data transformation or cleaning.