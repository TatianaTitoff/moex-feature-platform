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
    """Convert multiple MOEX ISS history pages into one DataFrame."""

    if not payloads:
        raise ValueError("No MOEX history pages provided")

    # Названия колонок берём из первой страницы ответа MOEX.
    columns = payloads[0]["history"]["columns"]

    # Сюда будем собирать строки со всех страниц.
    rows = []

    for payload in payloads:
        history = payload["history"]

        # Проверяем, что структура колонок одинакова
        # на всех страницах одного ответа.
        if history["columns"] != columns:
            raise ValueError(
                "MOEX history columns differ between pages"
            )

        # extend добавляет в список все элементы другого списка.
        # В отличие от append, он не создаёт вложенный список.
        rows.extend(history["data"])

    # Создаём один DataFrame сразу из всех полученных строк.
    return pd.DataFrame(rows, columns=columns)