import json
from pathlib import Path

from moex_feature_platform.transform.history_normalizer import (
    normalize_history_pages,
)
from moex_feature_platform.core.data_quality import validate_history


directory = Path(
    "data/raw/currency-selt/history/2026/08/2026-08-21"
)

payloads = []

for file_path in sorted(directory.glob("page-*.json")):
    with file_path.open("r", encoding="utf-8") as file:
        payloads.append(json.load(file))

df = normalize_history_pages(payloads)

result = validate_history(df)

print("Data quality result:")

for name, value in result.items():
    print(f"{name}: {value}")