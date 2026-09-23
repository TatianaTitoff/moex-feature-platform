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

## Source Completeness

The pipeline compares the number of received history rows with
the TOTAL value reported by the MOEX ISS pagination cursor.

A mismatch is recorded as `pagination_mismatch = 1`.

Incomplete datasets must not be published to the processed layer.

## July–August 2026 Observations

- July: 23 trading dates, 4,600 records.
- August: 21 trading dates, 4,200 records.
- Both months contain 200 records per trading date.
- The August dataset contains 473 records with actual trades.
- Most historical records describe instruments without trades on that date.

Pagination completeness has been verified for the requested dataset.
Completeness of the instrument universe requires separate validation.

## DQ Incident: Missing WAPRICE on 2026-03-20

### Context

During the historical backfill for January–June 2026, the pipeline
detected a data quality violation on 2026-03-20.

The backfill returned:

- success: 122 dates
- no_data: 58 dates
- dq_failed: 1 date

### Detected Issue

The MOEX ISS API returned 201 history records for 2026-03-20.

The daily DQ report recorded:

| Metric | Value |
|---|---:|
| row_count | 201 |
| source_total_rows | 201 |
| pagination_mismatch | 0 |
| duplicate_rows | 0 |
| duplicate_secid_trade_date | 0 |
| trades_without_waprice | 1 |
| no_trades_with_waprice | 0 |

One instrument had `NUMTRADES > 0` while `WAPRICE` was missing.

The pagination completeness check passed, indicating that the number
of retrieved records matched the total reported by the API.

### Pipeline Behavior

The pipeline:

1. Saved the original MOEX ISS response pages in RAW JSON.
2. Saved the daily DQ report.
3. Returned `dq_failed` for 2026-03-20.
4. Did not publish processed Parquet for the affected date.
5. Continued processing subsequent calendar dates.

The incident did not stop the entire historical backfill.

### Investigation Findings

The affected instrument was identified as BYNRUBTODTOM,
a Belarusian rouble FX swap.

Neighboring trading dates were examined:

| Date | NUMTRADES | WAPRICE |
|---|---:|---:|
| 2026-03-19 | 3 | 0.0011 |
| 2026-03-20 | 3 | null |
| 2026-03-23 | 3 | 0.0043 |

Zero values were also observed in the OHLC fields on neighboring
dates with valid WAPRICE values.

Therefore, zero prices must not be automatically interpreted
as missing data.

The exact reason for the missing WAPRICE on 2026-03-20
remains unconfirmed.

### Resolution

The affected instrument was identified as BYNRUBTODTOM,
a Belarusian rouble FX swap.

The record contains three trades, zero OHLC values and missing WAPRICE.
The exact reason for the missing WAPRICE remains unconfirmed.

The DQ policy was updated:

- Pagination mismatch and duplicate business keys remain blocking errors.
- Missing WAPRICE with NUMTRADES > 0 is treated as a warning.
- The original record is preserved without imputing the missing price.
- A warning does not prevent publication of other observations for the date.

After reprocessing, `2026-03-20` was published with:

- status: success_with_warnings
- row_count: 201
- trades_without_waprice: 1
- pagination_mismatch: 0

### Lessons Learned

- A successful API request does not guarantee valid business data.
- Pagination completeness and semantic data quality are separate checks.
- A single date-level DQ failure can be isolated without stopping
  the entire backfill.
- DQ reports and original RAW responses are necessary for investigating
  historical data anomalies.

  ### Affected Record

The investigation identified the following MOEX ISS history record:

| Field | Value |
|---|---|
| TRADEDATE | 2026-03-20 |
| SECID | BYNRUBTODTOM |
| SHORTNAME | BYN_TODTOM |
| NUMTRADES | 3 |
| OPEN | 0 |
| LOW | 0 |
| HIGH | 0 |
| CLOSE | 0 |
| WAPRICE | null |

The record reports three trades but contains no usable price
information in the retrieved fields.

The existing DQ rule correctly identified the inconsistency.

The root cause has not yet been established. The affected date
remains excluded from the processed layer pending investigation.