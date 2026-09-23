from moex_feature_platform.clients.moex_iss import MoexIssClient
from moex_feature_platform.storage.raw import RawStorage


client = MoexIssClient()
storage = RawStorage()

pages = client.get_history_raw(
    engine="currency",
    market="selt",
    board="CETS",
    date="2026-08-21",
)

print(f"Pages received: {len(pages)}")

for page_number, payload in enumerate(pages):
    path = storage.save_history_page(
        engine="currency",
        market="selt",
        board="CETS",
        trade_date="2026-08-21",
        page_number=page_number,
        payload=payload,
    )

    print(f"Saved: {path}")