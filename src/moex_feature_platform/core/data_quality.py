import pandas as pd


EXPECTED_COLUMNS = [
    "BOARDID",
    "TRADEDATE",
    "SHORTNAME",
    "SECID",
    "OPEN",
    "LOW",
    "HIGH",
    "CLOSE",
    "NUMTRADES",
    "WAPRICE",
]


def count_duplicate_rows(df: pd.DataFrame) -> int:
    """Count exact duplicate rows."""
    return int(df.duplicated().sum())


def count_missing_values(df: pd.DataFrame) -> pd.Series:
    """Count missing values in each column."""
    return df.isna().sum()

def validate_history(df: pd.DataFrame) -> dict[str, object]:
    """Run basic data quality checks for MOEX history data."""
    duplicate_rows = count_duplicate_rows(df)

    duplicate_secid_trade_date = int(
        df.duplicated(subset=["SECID", "TRADEDATE"]).sum()
    )

    trades_without_waprice = int(
        ((df["NUMTRADES"] > 0) & (df["WAPRICE"].isna())).sum()
    )

    no_trades_with_waprice = int(
        ((df["NUMTRADES"] == 0) & (df["WAPRICE"].notna())).sum()
    )

    return {
        "row_count": len(df),
        "duplicate_rows": duplicate_rows,
        "duplicate_secid_trade_date": duplicate_secid_trade_date,
        "trades_without_waprice": trades_without_waprice,
        "no_trades_with_waprice": no_trades_with_waprice,
    }


def validate_market_data(df: pd.DataFrame) -> dict:
    """Run basic data quality checks for market data."""

    duplicate_rows = count_duplicate_rows(df)

    duplicate_keys = int(
        df.duplicated(["SECID", "TRADEDATE"]).sum()
    )

    trades_without_waprice = int(
        (
            (df["NUMTRADES"] > 0)
            & df["WAPRICE"].isna()
        ).sum()
    )

    no_trades_with_waprice = int(
        (
            (df["NUMTRADES"] == 0)
            & df["WAPRICE"].notna()
        ).sum()
    )

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    return {
        "row_count": len(df),
        "duplicate_rows": duplicate_rows,
        "duplicate_secid_trade_date": duplicate_keys,
        "trades_without_waprice": trades_without_waprice,
        "no_trades_with_waprice": no_trades_with_waprice,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
    }