from datetime import date, timedelta
from typing import Any

import requests


class MoexIssClient:
    """Client for retrieving data from the MOEX ISS API."""

    def __init__(self, base_url: str = "https://iss.moex.com/iss") -> None:
        self.base_url = base_url.rstrip("/")

    def get_history(
        self,
        engine: str,
        market: str,
        board: str,
        date: str,
    ) -> list[dict[str, Any]]:
        """Retrieve all historical records for the requested date."""

        url = (
            f"{self.base_url}/history/"
            f"engines/{engine}/"
            f"markets/{market}/"
            f"boards/{board}/"
            f"securities.json"
        )

        start = 0
        rows: list[dict[str, Any]] = []

        while True:
            params = {
                "date": date,
                "start": start,
                "iss.meta": "off",
            }

            response = requests.get(
                url,
                params=params,
                timeout=30,
            )
            response.raise_for_status()

            payload = self._get_history_page(
                engine=engine,
                market=market,
                board=board,
                date=date,
                start=start,
                                            )

            history = payload["history"]
            columns = history["columns"]
            page = history["data"]

            rows.extend(
                dict(zip(columns, row))
                for row in page
            )

            cursor = payload["history.cursor"]["data"][0]

            total = cursor[1]
            page_size = cursor[2]

            start += page_size

            if start >= total:
                break

        return rows

    def get_history_range(
        self,
        engine: str,
        market: str,
        board: str,
        date_from: str,
        date_to: str,
    ) -> list[dict[str, Any]]:
        """Retrieve historical records for a calendar date range."""

        start_date = date.fromisoformat(date_from)
        end_date = date.fromisoformat(date_to)

        all_rows: list[dict[str, Any]] = []

        current_date = start_date

        while current_date <= end_date:
            rows = self.get_history(
                engine=engine,
                market=market,
                board=board,
                date=current_date.isoformat(),
            )

            all_rows.extend(rows)
            current_date += timedelta(days=1)

        return all_rows

    def _get_history_page(
        self,
        engine: str,
        market: str,
        board: str,
        date: str,
        start: int,
                            ) -> dict[str, Any]:
        """Fetch one raw page from MOEX ISS."""
        url = (
        f"{self.base_url}/history/engines/"
        f"{engine}/markets/{market}/boards/{board}/securities.json"
        )

        params = {
        "date": date,
        "start": start,
        "iss.meta": "off",
        }

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        return response.json()

    def get_history_raw(
        self,
        engine: str,
        market: str,
        board: str,
        date: str,
    ) -> list[dict[str, Any]]:
        """Retrieve raw MOEX ISS response pages for a date."""
        pages: list[dict[str, Any]] = []
        start = 0

        while True:
            payload = self._get_history_page(
                engine=engine,
                market=market,
                board=board,
                date=date,
                start=start,
            )

            pages.append(payload)

            cursor = payload["history.cursor"]

            columns = cursor["columns"]
            data = cursor["data"][0]

            cursor_data = dict(zip(columns, data))

            total = cursor_data["TOTAL"]
            page_size = cursor_data["PAGESIZE"]

            start += page_size

            if start >= total:
                break

        return pages