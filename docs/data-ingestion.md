# Data Ingestion

## MOEX ISS Historical Data

The platform retrieves historical market data from the MOEX ISS API.

The initial endpoint used for currency market data:

- Engine: `currency`
- Market: `selt`
- Board: `CETS`

### Request parameters

For the selected historical endpoint, the requested trading date is provided using the `date` parameter.

The client also uses the `start` parameter to paginate through the API response.

Example:

```text
date=2026-08-21
start=0
```
### Non-trading dates

The historical endpoint returns records for available trading dates rather than for every calendar date.

This was verified using the period `2026-08-21` to `2026-08-24`:

- `2026-08-21` — 200 records returned;
- `2026-08-22` — no records returned;
- `2026-08-23` — no records returned;
- `2026-08-24` — 200 records returned.

Non-trading dates must therefore not be interpreted as missing market data. The ingestion process should preserve the distinction between calendar dates and actual trading dates.

### Requested date validation

For date-specific historical requests, the returned `TRADEDATE` must match the requested date.

Two outcomes are considered valid:

- the requested trading date is returned in the historical data;
- no records are returned because the requested date is non-trading.

Data returned for a different `TRADEDATE` must be treated as an ingestion error.

### Pagination

The API response contains a history.cursor block with:

INDEX — starting position of the current page;
TOTAL — total number of available records;
PAGESIZE — maximum number of records returned per page.

The MoexIssClient automatically requests subsequent pages until all records are retrieved.

### Historical records and instrument universe

The `history` endpoint returns one historical record per instrument included in the requested board.

For the tested configuration (`currency / selt / CETS`):

- `securities` endpoint returned 200 instruments;
- historical data for `2026-08-21` returned 200 records;
- each returned `SECID` was unique for the selected date.

This indicates that the historical dataset represents instrument-level daily observations rather than individual trade executions.

The current dataset grain is:

> One record represents one instrument (`SECID`) for one trading date (`TRADEDATE`).

### Instrument reference data

The MOEX ISS API provides a separate `securities` data block containing reference information about instruments, including `SECID`, `SHORTNAME`, `STATUS` and other instrument attributes.

The `history` data block contains historical market observations for the requested date.

The two datasets can be related using `SECID`.

The instrument status does not determine whether an instrument has trades on a particular day. In the tested sample, the majority of instruments had `STATUS = A` while still having `NUMTRADES = 0` on some dates.

Therefore, records with `NUMTRADES = 0` must not be automatically classified as invalid or removed. Their treatment depends on the intended analytical or ML use case.

One historical `SECID` (`USDRUB_FWD`) was not present in the current `securities` reference response and therefore received a missing `STATUS` after the join. This case requires separate investigation.

### Historical instrument coverage

The current `securities` reference data does not necessarily contain every instrument that appears in historical data.

This was verified using `USDRUB_FWD` (`SHORTNAME = USDRUB_LTV`):

- the instrument appears in historical data for the tested dates;
- the instrument is not present in the current `securities` response;
- the instrument history endpoint reports an available history range from `2012-04-23` to `2026-08-26`.

Therefore, current instrument reference data must not be treated as a complete historical instrument dimension.

Historical instrument attributes may require a separate historical reference dataset or instrument-level history.

### Historical date range

The client provides a range-based ingestion method that iterates through calendar dates and retrieves historical data for each date.

Non-trading dates return an empty result and do not add records to the resulting dataset.

This approach keeps calendar handling separate from the market data itself and avoids creating artificial records for non-trading dates.

### API parameter validation

During initial exploration, the client incorrectly used the from and till parameters for this endpoint.

As a result, requests for different dates returned the same latest available trading date.

The implementation was corrected to use the endpoint-specific date parameter.

This demonstrated the need to validate that the requested date matches the TRADEDATE values returned by the API.

