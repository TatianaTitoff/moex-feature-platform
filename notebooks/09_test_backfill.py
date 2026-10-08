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
    date_from="2021-09-01",
    date_to="2026-09-30",
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
# Учитываем оба варианта успешной загрузки:
# без предупреждений и с некритическими нарушениями DQ.
new_rows = sum(
    result.get("row_count", 0)
    for result in results
    if result["status"] in (
        "success",
        "success_with_warnings",
    )
)

print("New rows:", new_rows)

# Выбираем из результатов только даты с нарушениями DQ.
failed_dates = [
    result
    for result in results
    if result["status"] == "dq_failed"
]

if failed_dates:
    print("\nDATA QUALITY FAILURES:")

    for result in failed_dates:
        print("Date:", result["trade_date"])

        # Выводим только ненулевые метрики нарушений.
        # row_count и source_total_rows не являются ошибками.
        for name, value in result["dq"].items():
            if name not in ("row_count", "source_total_rows") and value > 0:
                print(f"  {name}: {value}")


warning_results = []

for result in results:
    if result["status"] == "success_with_warnings":
        warning_results.append(result)

print("\nWarnings by metric:")

warning_counts = {}

for result in warning_results:
    dq = result["dq"]

    for metric_name, value in dq.items():

        # Нас интересуют только ненулевые DQ-показатели.
        if value > 0:
            if metric_name not in (
                "row_count",
                "source_total_rows",
            ):
                warning_counts[metric_name] = (
                    warning_counts.get(metric_name, 0)
                    + value
                )

print(warning_counts)