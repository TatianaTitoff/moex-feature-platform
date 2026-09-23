from moex_feature_platform.clients.moex_iss import MoexIssClient
from moex_feature_platform.core.dataframe import records_to_dataframe
from moex_feature_platform.core.data_quality import validate_market_data

import pandas as pd
import requests

client = MoexIssClient()

dates = [
    "2026-08-21",
    "2026-08-22",
    "2026-08-23",
    "2026-08-24",
]

client = MoexIssClient()

rows = client.get_history_range(
    engine="currency",
    market="selt",
    board="CETS",
    date_from="2026-08-21",
    date_to="2026-08-24",
)

df_all = records_to_dataframe(rows)

dq_result = validate_market_data(df_all)

print("\nDQ result:")
for check, result in dq_result.items():
    print(f"{check}: {result}")
    
print("Total rows:", len(df_all))
print("\nRows by TRADEDATE:")
print(df_all.groupby("TRADEDATE").size())


##df_all = pd.concat(frames, ignore_index=True)

print("\nRows by TRADEDATE:")
print(df_all.groupby("TRADEDATE").size())

print(
    "\nUnique SECID + TRADEDATE:",
    df_all[["SECID", "TRADEDATE"]].drop_duplicates().shape[0],
)

print("Total rows:", len(df_all))

print(
    "Duplicate SECID + TRADEDATE:",
    df_all.duplicated(["SECID", "TRADEDATE"]).sum(),
)


print("\nUSDRUB_FWD history:")
print(
    df_all.loc[
        df_all["SECID"] == "USDRUB_FWD",
        [
            "SECID",
            "TRADEDATE",
            "SHORTNAME",
            "OPEN",
            "LOW",
            "HIGH",
            "CLOSE",
            "NUMTRADES",
            "WAPRICE",
        ],
    ].to_string(index=False)
)


print("\nNUMTRADES / WAPRICE consistency by date:")

for date in dates:
    df_date = df_all[df_all["TRADEDATE"] == date]

    trades_without_waprice = (
        (df_date["NUMTRADES"] > 0)
        & df_date["WAPRICE"].isna()
    ).sum()

    no_trades_with_waprice = (
        (df_date["NUMTRADES"] == 0)
        & df_date["WAPRICE"].notna()
    ).sum()

    print(
        f"{date}: "
        f"trades without WAPRICE = {trades_without_waprice}, "
        f"no trades with WAPRICE = {no_trades_with_waprice}"
    )

print("\nRows by TRADEDATE:")
print(df_all.groupby("TRADEDATE").size())

print(
    "\nUnique SECID + TRADEDATE:",
    df_all[["SECID", "TRADEDATE"]].drop_duplicates().shape[0],
)

print(
    "Total rows:",
    len(df_all),
)

print(
    "Duplicate SECID + TRADEDATE:",
    df_all.duplicated(["SECID", "TRADEDATE"]).sum(),
)




print("\nInstrument activity by SHORTNAME prefix:")

df_all["INSTRUMENT_PREFIX"] = (
    df_all["SHORTNAME"]
    .str.split("_")
    .str[0]
)

activity = (
    df_all.groupby("INSTRUMENT_PREFIX")
    .agg(
        instruments=("SECID", "nunique"),
        traded=("NUMTRADES", lambda x: (x > 0).sum()),
        not_traded=("NUMTRADES", lambda x: (x == 0).sum()),
    )
    .sort_values("instruments", ascending=False)
)

print(activity)

securities_url = (
    "https://iss.moex.com/iss/engines/currency/"
    "markets/selt/boards/CETS/securities.json"
)

securities_params = {
    "iss.meta": "off",
}

response = requests.get(
    securities_url,
    params=securities_params,
    timeout=30,
)
response.raise_for_status()

securities_payload = response.json()

securities = securities_payload["securities"]

securities_df = pd.DataFrame(
    securities["data"],
    columns=securities["columns"],
)

historical_secids = set(df_all["SECID"].unique())
current_secids = set(securities_df["SECID"].unique())

historical_not_in_current = historical_secids - current_secids

print("\nHistorical SECIDs:", len(historical_secids))
print("Current SECIDs:", len(current_secids))
print(
    "Historical SECIDs absent from current securities:",
    len(historical_not_in_current),
)

print("\nSECIDs absent from current securities:")
print(sorted(historical_not_in_current))

