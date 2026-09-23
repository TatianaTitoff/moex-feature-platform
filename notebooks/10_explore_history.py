from pathlib import Path

import pandas as pd


# Директория, в которой лежат все августовские Parquet-файлы.
directory = Path(
    "data/processed/moex-fx/history/2026/08"
)

# glob("*.parquet") возвращает пути ко всем Parquet-файлам
# непосредственно в указанной директории.
# sorted() упорядочивает пути по имени файла.
files = sorted(directory.glob("*.parquet"))

print("Parquet files:", len(files))

if not files:
    raise FileNotFoundError(
        f"No Parquet files found in {directory}"
    )

# Читаем каждый файл в отдельный DataFrame.
# Затем pd.concat объединяет их по строкам.
df = pd.concat(
    [pd.read_parquet(file) for file in files],
    ignore_index=True,
)

from moex_feature_platform.core.data_quality import validate_history
from moex_feature_platform.pipelines.history_pipeline import save_history_dq


# Группируем августовскую историю по дате торгов.
# Каждая группа — отдельный DataFrame за конкретный день.
for trade_date, day_df in df.groupby("TRADEDATE"):

    dq_result = validate_history(day_df)

    report_path = save_history_dq(
        trade_date=trade_date,
        dq_result=dq_result,
    )

    print("DQ report saved:", report_path)
    
print("\nDataset shape:", df.shape)
print("Trading dates:", df["TRADEDATE"].nunique())
print("Unique instruments:", df["SECID"].nunique())

print("\nColumn types:")
print(df.dtypes)

# Добавляем временный аналитический признак:
# происходили ли сделки по инструменту в этот день?
df["is_traded"] = df["NUMTRADES"] > 0

print("\nTrading activity:")
print("Rows with trades:", df["is_traded"].sum())
print("Rows without trades:", (~df["is_traded"]).sum())

print("\nActive instruments by date:")
print(
    df.groupby("TRADEDATE")["is_traded"].sum()
)

print("\nMost actively traded instruments:")

instrument_activity = (
    df.groupby("SECID")
    .agg(
        traded_days=("is_traded", "sum"),
        total_trades=("NUMTRADES", "sum"),
    )
    .sort_values(
        "total_trades",
        ascending=False,
    )
)

print(instrument_activity.head(20))

print("\nData quality across the month:")

print(
    "Duplicate SECID + TRADEDATE:",
    df.duplicated(
        subset=["SECID", "TRADEDATE"]
    ).sum(),
)

print(
    "Rows with trades but missing WAPRICE:",
    (
        df["is_traded"]
        & df["WAPRICE"].isna()
    ).sum(),
)

import json

from moex_feature_platform.clients.moex_iss import MoexIssClient


# Проверяем несколько исторических дат, а не только одну.
dates_to_check = [
    "2026-08-03",
    "2026-08-21",
    "2026-08-31",
]

for trade_date in dates_to_check:

    raw_directory = Path(
        f"data/raw/currency-selt/history/"
        f"{trade_date[:4]}/{trade_date[5:7]}/{trade_date}"
    )

    page_files = sorted(raw_directory.glob("page-*.json"))

    print(f"\nDate: {trade_date}")
    print("Saved pages:", len(page_files))

    all_secids = []

    for page_file in page_files:

        # Читаем исходный JSON, сохранённый без нормализации.
        with page_file.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        # В cursor названия полей и значения хранятся отдельно.
        cursor_block = payload["history.cursor"]

        cursor = dict(
            zip(
                cursor_block["columns"],
                cursor_block["data"][0],
            )
        )

        # Смотрим, сколько записей действительно лежит на странице.
        history = payload["history"]

        rows = history["data"]

        # Определяем позицию SECID по названию колонки,
        # а не предполагаем, что SECID всегда находится под индексом 3.
        secid_index = history["columns"].index("SECID")

        page_secids = [
            row[secid_index]
            for row in rows
        ]

        all_secids.extend(page_secids)

        print(
            page_file.name,
            "cursor:", cursor,
            "rows:", len(rows),
        )

    print("Total received rows:", len(all_secids))
    print("Unique SECIDs:", len(set(all_secids)))


client = MoexIssClient()

# Проверяем, не отдаёт ли API данные после двухсотой записи.
# _get_history_page — наш внутренний метод клиента.
# Для разовой диагностики его можно вызвать напрямую.
payload = client._get_history_page(
    engine="currency",
    market="selt",
    board="CETS",
    date="2026-08-31",
    start=200,
)

print("\nManual request with start=200")
print("Rows returned:", len(payload["history"]["data"]))
print("Cursor:", payload["history.cursor"]["data"])