from moex_feature_platform.pipelines.history_pipeline import (
    process_raw_history,
)


raw_directory = (
    "data/raw/currency-selt/history/2026/08/2026-08-21"
)

df, dq_result = process_raw_history(raw_directory)

print("DataFrame shape:", df.shape)
print()
print("Data quality result:")

for name, value in dq_result.items():
    print(f"{name}: {value}")


from moex_feature_platform.pipelines.history_pipeline import (
    save_processed_history,
)

output_path = (
    "data/processed/moex-fx/history/"
    "2026/08/2026-08-21.parquet"
)

if all(
    value == 0
    for name, value in dq_result.items()
    if name != "row_count"
):
    saved_path = save_processed_history(df, output_path)
    print("Saved:", saved_path)
else:
    print("DQ failed. Processed file was not saved.")