from pathlib import Path
from typing import Any
import json


class RawStorage:
    def __init__(self, base_dir: str = "data/raw") -> None:
        self.base_dir = Path(base_dir)

    def save_history_page(
        self,
        engine: str,
        market: str,
        board: str,
        trade_date: str,
        page_number: int,
        payload: dict[str, Any],
    ) -> Path:
        """Save one raw MOEX ISS response page as JSON."""
        year = trade_date[:4]
        month = trade_date[5:7]

        directory = (
            self.base_dir
            / f"{engine}-{market}"
            / "history"
            / year
            / month
            / trade_date
        )

        directory.mkdir(parents=True, exist_ok=True)

        file_path = directory / f"page-{page_number:03d}.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return file_path