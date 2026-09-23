from moex_feature_platform.clients.moex_iss import MoexIssClient
from moex_feature_platform.storage.raw import RawStorage
from moex_feature_platform.pipelines.history_pipeline import (
    ingest_history_date,
)


client = MoexIssClient()
raw_storage = RawStorage()

result = ingest_history_date(
    client=client,
    raw_storage=raw_storage,
    trade_date="2026-07-01",
)

print(result)