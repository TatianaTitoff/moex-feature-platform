import requests

URL = "https://iss.moex.com/iss/history/engines/currency/markets/selt/boards/CETS/securities.json"

params = {
    "from": "2026-08-20",
    "till": "2026-08-20",
    "start": 0,
    "iss.meta": "off",
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

import pandas as pd

history = data["history"]

df = pd.DataFrame(
    history["data"],
    columns=history["columns"],
)

params["start"] = 100

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data_page_2 = response.json()

history_page_2 = data_page_2["history"]

df_page_2 = pd.DataFrame(
    history_page_2["data"],
    columns=history_page_2["columns"],
)

print("\nSecond page:")
print(df_page_2.head())
print(df_page_2.shape)

print("\nRows with trades on second page:")
print((df_page_2["NUMTRADES"] > 0).sum())

print("\nRows without trades on second page:")
print((df_page_2["NUMTRADES"] == 0).sum())

print(df.head())
print()
print(df.shape)
print()
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nRows with trades:")
print((df["NUMTRADES"] > 0).sum())

print("\nRows without trades:")
print((df["NUMTRADES"] == 0).sum())

print("Top-level keys:")
print(list(data.keys()))

inactive = df[df["NUMTRADES"] == 0]

print("\nInstruments without trades:")
print(
    inactive[
        ["SHORTNAME", "SECID", "NUMTRADES", "WAPRICE"]
    ].to_string(index=False)
)

df_all = pd.concat([df, df_page_2], ignore_index=True)

print(df_all.shape)
print((df_all["NUMTRADES"] > 0).sum())
print((df_all["NUMTRADES"] == 0).sum())


print("\nBlocks:")
for key, value in data.items():
    if isinstance(value, dict):
        print(f"\n[{key}]")
        print("Keys:", list(value.keys()))

        if "columns" in value:
            print("Columns:", value["columns"])

        if "data" in value:
            print("Rows:", len(value["data"]))
            print("First 3 rows:")
            for row in value["data"][:3]:
                print(row)