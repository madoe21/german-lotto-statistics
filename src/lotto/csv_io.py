from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .config import GameConfig


class DataPaths:
    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def draws(self, game: GameConfig) -> Path:
        return self.data_dir / f"{game.cli_name}_draws.csv"

    def stats_file(self, game: GameConfig, suffix: str) -> Path:
        return self.data_dir / f"{game.cli_name}_{suffix}.csv"


def iso_to_de(date_key: str) -> str:
    return datetime.strptime(date_key, "%Y-%m-%d").strftime("%d.%m.%Y")


def de_to_iso(date_label: str) -> str:
    return datetime.strptime(date_label, "%d.%m.%Y").strftime("%Y-%m-%d")


def read_existing_draw_dates(draws_file: Path) -> set[str]:
    existing: set[str] = set()
    if not draws_file.exists() or draws_file.stat().st_size == 0:
        return existing

    with draws_file.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            date_text = (row or {}).get("Date", "").strip()
            if not date_text:
                continue
            try:
                existing.add(de_to_iso(date_text))
            except ValueError:
                continue
    return existing


def append_row(draws_file: Path, headers: list[str], row: dict[str, str]) -> None:
    has_content = draws_file.exists() and draws_file.stat().st_size > 0
    with draws_file.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        if not has_content:
            writer.writeheader()
        writer.writerow(row)


def write_csv(path: Path, headers: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
