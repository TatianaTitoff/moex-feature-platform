from typing import Any

import pandas as pd


def normalize_history_payload(payload: dict[str, Any]) -> pd.DataFrame:
    """Convert one raw MOEX ISS history response into a DataFrame."""
    history = payload["history"]

    columns = history["columns"]
    data = history["data"]

    return pd.DataFrame(data, columns=columns)

def normalize_history_pages(
    payloads: list[dict[str, Any]],
                            ) -> pd.DataFrame:
    """Convert multiple raw MOEX ISS history pages into one DataFrame."""
    frames = [
        normalize_history_payload(payload)
        for payload in payloads
    ]

    return pd.concat(frames, ignore_index=True)