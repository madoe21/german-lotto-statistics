from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .api_client import LottoBrandenburgApiClient
from .config import GameConfig
from .csv_io import append_row, iso_to_de, read_existing_draw_dates


@dataclass
class ScrapeStats:
    added: int = 0
    skipped_existing: int = 0
    skipped_date_filter: int = 0
    skipped_no_result: int = 0
    errors: int = 0


class LotteryScraperService:
    def __init__(self, api: LottoBrandenburgApiClient, game: GameConfig, draws_file: Path) -> None:
        self.api = api
        self.game = game
        self.draws_file = draws_file

    def _normalize_numbers(self, values: object, count: int) -> list[str]:
        if not isinstance(values, list):
            return []

        normalized: list[str] = []
        for item in values:
            if item is None:
                continue
            normalized.append(str(item).strip())
            if len(normalized) >= count:
                break
        return normalized

    def _extract_special(self, result: dict) -> list[str]:
        if self.game.api_game_type == "EURO":
            return self._normalize_numbers(
                result.get("sortedSecondaryWinningDigits") or result.get("secondaryWinningDigits"),
                self.game.special_count,
            )

        if self.game.api_game_type == "LOTTO":
            super_number = result.get("superNumber")
            return [str(super_number)] if super_number is not None and str(super_number).strip() else []

        return []

    def _row_from_result(self, date_key: str, result: dict) -> dict[str, str] | None:
        main = self._normalize_numbers(
            result.get("sortedWinningDigits") or result.get("winningDigits"),
            self.game.main_count,
        )
        special = self._extract_special(result)

        if len(main) != self.game.main_count or len(special) != self.game.special_count:
            return None

        row: dict[str, str] = {"Date": iso_to_de(date_key)}
        for index, value in enumerate(main, start=1):
            row[f"Number{index}"] = value

        if self.game.special_count == 2:
            row["Euro1"] = special[0]
            row["Euro2"] = special[1]
        else:
            row["Superzahl"] = special[0]

        return row

    def _min_year(self, existing_dates: set[str], from_date: str | None) -> str | None:
        """Determine the earliest year we still need to fetch from the API.

        If existing data is present, we only need the year of the latest
        existing draw onward (new draws can only appear after that).
        A --from-date flag narrows this further.  Returns *None* when
        there is no constraint (= fetch everything, e.g. first run).
        """
        candidates: list[str] = []
        if existing_dates:
            candidates.append(max(existing_dates)[:4])
        if from_date:
            candidates.append(datetime.strptime(from_date, "%d.%m.%Y").strftime("%Y"))
        return max(candidates) if candidates else None

    def run(self, from_date: str | None = None) -> ScrapeStats:
        existing_dates = read_existing_draw_dates(self.draws_file)
        min_date = datetime.strptime(from_date, "%d.%m.%Y").date() if from_date else None
        stats = ScrapeStats()

        min_year = self._min_year(existing_dates, from_date)

        all_years = sorted(self.api.get_draw_years(self.game.api_game_type))
        years = [y for y in all_years if min_year is None or y >= min_year]

        for year in years:
            draw_dates = self.api.get_draw_dates(self.game.api_game_type, year)
            for date_key in sorted(draw_dates.keys()):
                if min_date and datetime.strptime(date_key, "%Y-%m-%d").date() < min_date:
                    stats.skipped_date_filter += 1
                    continue

                if date_key in existing_dates:
                    stats.skipped_existing += 1
                    continue

                try:
                    result = self.api.get_draw_result(self.game.api_game_type, date_key)
                except RuntimeError:
                    stats.errors += 1
                    continue

                if not result:
                    stats.skipped_no_result += 1
                    continue

                row = self._row_from_result(date_key, result)
                if not row:
                    stats.skipped_no_result += 1
                    continue

                append_row(self.draws_file, self.game.draw_headers, row)
                existing_dates.add(date_key)
                stats.added += 1

        return stats
