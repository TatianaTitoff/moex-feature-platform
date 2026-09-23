import requests


url = (
    "https://iss.moex.com/iss/history/"
    "engines/currency/markets/selt/boards/CETS/securities.json"
)

params = {
    "date": "2026-08-21",
    "start": 0,
    "limit": 1000,
    "iss.meta": "off",
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

payload = response.json()

history = payload["history"]
cursor = payload["history.cursor"]

print("\nDirect API check:")
print("Rows returned:", len(history["data"]))
print("Cursor columns:", cursor["columns"])
print("Cursor data:", cursor["data"])