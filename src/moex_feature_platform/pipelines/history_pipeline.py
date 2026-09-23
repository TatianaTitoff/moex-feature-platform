import json
from pathlib import Path

from moex_feature_platform.core.data_quality import validate_history
from moex_feature_platform.transform.history_normalizer import (
    normalize_history_pages,
)

import pandas as pd

from moex_feature_platform.clients.moex_iss import MoexIssClient
from moex_feature_platform.storage.raw import RawStorage

from datetime import date, timedelta

def process_raw_history(raw_directory: str) -> tuple:
    """Normalize raw history pages and run data quality checks."""
    directory = Path(raw_directory)

    payloads = []

    for file_path in sorted(directory.glob("page-*.json")):
        with file_path.open("r", encoding="utf-8") as file:
            payloads.append(json.load(file))

    df = normalize_history_pages(payloads)

    dq_result = validate_history(df)

    return df, dq_result

def save_processed_history(
    df: pd.DataFrame,
    output_path: str,
    ) -> Path:
    """Save normalized MOEX history as Parquet."""
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, index=False)

    return path

def ingest_history_date(
    client: MoexIssClient,
    raw_storage: RawStorage,
    trade_date: str,
    engine: str = "currency",
    market: str = "selt",
    board: str = "CETS",
    force: bool = False,
    ) -> dict[str, object]:
    """Ingest and process MOEX history for one calendar date."""

        # Путь к итоговому Parquet для конкретной даты.
    output_path = Path(
        f"data/processed/moex-fx/history/"
        f"{trade_date[:4]}/{trade_date[5:7]}/"
        f"{trade_date}.parquet"
    )

    # Если дата уже обработана, повторно не обращаемся к API.
    # force=True позволяет обойти эту проверку.
    if output_path.exists() and not force:
        return {
            "trade_date": trade_date,
            "status": "already_processed",
        }
    
    pages = client.get_history_raw(
        engine=engine,
        market=market,
        board=board,
        date=trade_date,
    )

    df = normalize_history_pages(pages)

    # MOEX сообщает общее количество строк,
    # доступных для данного запроса.
    #
    # pages[0] — ответ первой страницы.
    # ["history.cursor"] — блок метаданных пагинации.
    # ["data"][0] — первая строка этого блока:
    # [INDEX, TOTAL, PAGESIZE].
    # [1] — значение TOTAL.

    expected_rows = pages[0]["history.cursor"]["data"][0][1]

    if df.empty:
        return {
            "trade_date": trade_date,
            "status": "no_data",
            "row_count": 0,
        }

    for page_number, payload in enumerate(pages):
        raw_storage.save_history_page(
            engine=engine,
            market=market,
            board=board,
            trade_date=trade_date,
            page_number=page_number,
            payload=payload,
        )

    dq_result = validate_history(df)

    # Сохраняем в DQ число строк, заявленное источником.
    dq_result["source_total_rows"] = expected_rows

    # Фиксируем нарушение, если фактическое количество
    # строк не совпадает с TOTAL из ответа MOEX.
    # int(True) = 1, int(False) = 0.
    dq_result["pagination_mismatch"] = int(
        len(df) != expected_rows
    )
    
    # Сохраняем результат DQ независимо от того,
    # прошли данные проверку или нет.
    save_history_dq(
    trade_date=trade_date,
    dq_result=dq_result,
    )

        # Проверяем только метрики, описывающие нарушения.
    # Количество строк само по себе ошибкой не является.
    failure_metrics = [
        "duplicate_rows",
        "duplicate_secid_trade_date",
        "trades_without_waprice",
        "no_trades_with_waprice",
        "pagination_mismatch",
    ]

    if any(dq_result[name] > 0 for name in failure_metrics):
        return {
            "trade_date": trade_date,
            "status": "dq_failed",
            "dq": dq_result,
        }

    save_processed_history(df, output_path)

    return {
        "trade_date": trade_date,
        "status": "success",
        "row_count": len(df),
        "dq": dq_result,
    }

def ingest_history_range(
    client: MoexIssClient,
    raw_storage: RawStorage,
    date_from: str,
    date_to: str,
    force: bool = False,
    ) -> list[dict[str, object]]:
    """Ingest MOEX history for a calendar date range."""

    # Преобразуем строки YYYY-MM-DD в объекты date.
    start_date = date.fromisoformat(date_from)
    end_date = date.fromisoformat(date_to)

    if start_date > end_date:
        raise ValueError("date_from must not be later than date_to")

    results = []
    current_date = start_date

    # Последовательно обрабатываем каждый календарный день,
    # включая выходные и праздники.
    while current_date <= end_date:

        result = ingest_history_date(
            client=client,
            raw_storage=raw_storage,
            trade_date=current_date.isoformat(),
            force=force,
        )

        results.append(result)

        # Переходим к следующему календарному дню.
        current_date += timedelta(days=1)

    return results

def save_history_dq(
    trade_date: str,
    dq_result: dict[str, object],
) -> Path:
    """Save daily data quality metrics as JSON."""

    # Формируем путь к отчёту за конкретную дату.
    path = Path(
        f"data/quality/moex-fx/history/"
        f"{trade_date[:4]}/{trade_date[5:7]}/"
        f"{trade_date}.json"
    )

    # Создаём родительские директории, если их ещё нет.
    # parents=True — разрешает создать всю цепочку директорий.
    # exist_ok=True — не считает ошибкой существующую директорию.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Формируем содержимое отчёта.
    report = {
        "trade_date": trade_date,
        **dq_result,
    }

    # Записываем Python-словарь в JSON-файл.
    with path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return path