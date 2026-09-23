import json
from pathlib import Path

from moex_feature_platform.transform.history_normalizer import (
    normalize_history_pages,
)


# Исходные ответы MOEX за проблемную дату.
# Используем RAW, а не Parquet, поскольку processed для этой даты
# не был создан из-за нарушения DQ.
raw_directory = Path(
    "data/raw/currency-selt/history/2026/03/2026-03-20"
)

# Читаем все сохранённые страницы ответа API.
payloads = []

for file_path in sorted(raw_directory.glob("page-*.json")):
    with file_path.open("r", encoding="utf-8") as file:
        payloads.append(json.load(file))

# Восстанавливаем исходную таблицу из RAW JSON.
df = normalize_history_pages(payloads)

# Выбираем записи, для которых были сделки,
# но отсутствует средневзвешенная цена WAPRICE.
problem_rows = df.loc[
    (df["NUMTRADES"] > 0)
    & (df["WAPRICE"].isna())
]

print("Problem rows:", len(problem_rows))

# Показываем все значения проблемных строк без усечения колонок.
print(problem_rows.to_string(index=False))

import pandas as pd


secid = "BYNRUBTODTOM"

# Соседние торговые даты.
dates = [
    "2026-03-19",
    "2026-03-23",
]

for trade_date in dates:

    # Для соседних дат читаем processed Parquet:
    # они успешно прошли DQ и были опубликованы.
    path = Path(
        f"data/processed/moex-fx/history/"
        f"{trade_date[:4]}/{trade_date[5:7]}/"
        f"{trade_date}.parquet"
    )

    day_df = pd.read_parquet(path)

    instrument = day_df.loc[
        day_df["SECID"] == secid
    ]

    print(instrument.to_string(index=False))