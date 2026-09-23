from moex_feature_platform.clients.moex_iss import MoexIssClient
from moex_feature_platform.storage.raw import RawStorage
from moex_feature_platform.pipelines.history_pipeline import (
    ingest_history_range,
)

client = MoexIssClient()
raw_storage = RawStorage()

results = ingest_history_range(
    client=client,
    raw_storage=raw_storage,
    date_from="2026-07-01",
    date_to="2026-07-31",
)

for result in results:
    print(
        result["trade_date"],
        result["status"],
        result.get("row_count", "-"),
    )

from collections import Counter

# Считаем, сколько раз встретился каждый статус загрузки.
# Counter работает со списками и другими итерируемыми объектами.
status_counts = Counter(result["status"] for result in results)

print("\nBackfill summary:")

for status, count in status_counts.items():
    print(f"{status}: {count}")

# Суммируем число строк только для дат, загруженных в этом запуске.
new_rows = sum(
    result.get("row_count", 0)
    for result in results
    if result["status"] == "success"
)

print("New rows:", new_rows)