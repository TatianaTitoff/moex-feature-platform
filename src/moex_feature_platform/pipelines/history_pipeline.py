import json
from pathlib import Path

from moex_feature_platform.core.data_quality import validate_history
from moex_feature_platform.transform.history_normalizer import (
    normalize_history_pages,
)

import pandas as pd

def process_raw_history(raw_directory: str) -> tuple:
    """Normalize raw history pages and run data quality checks."""
    directory = Path(raw_directory)

    payloads = []

    for file_path in sorted(directory.glob("page-*.json")):
        with file_path.open("r", encoding="utf-8") as file:
            payloads.append(json.load(file))

    df = normalize_history_pages(payloads)

    dq_result = validate_history(df)

    return df, dq_result

def save_processed_history(
    df: pd.DataFrame,
    output_path: str,
    ) -> Path:
    """Save normalized MOEX history as Parquet."""
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, index=False)

    return path