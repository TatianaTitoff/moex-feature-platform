import pandas as pd


def records_to_dataframe(records: list[dict]) -> pd.DataFrame:
    """Convert API records into a pandas DataFrame."""
    return pd.DataFrame(records)