from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from .config import GameConfig
from .csv_io import write_csv


@dataclass
class DrawRow:
    date: str
    numbers: list[int]
    special: list[int]


class LotteryAnalyzerService:
    def __init__(self, game: GameConfig, draws_file: Path, output_dir: Path) -> None:
        self.game = game
        self.draws_file = draws_file
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.draws: list[DrawRow] = []
        self.number_counter: Counter[int] = Counter()
        self.special_counter: Counter[int] = Counter()
        self.pair_counter: Counter[tuple[int, int]] = Counter()
        self.triple_counter: Counter[tuple[int, int, int]] = Counter()
        self.quad_counter: Counter[tuple[int, int, int, int]] = Counter()
        self.special_pair_counter: Counter[tuple[int, int]] = Counter()

    def _require_columns(self, headers: list[str], required: list[str]) -> None:
        missing = [col for col in required if col not in headers]
        if missing:
            raise RuntimeError(f"Missing CSV columns: {', '.join(missing)}")

    def _load_draws(self) -> None:
        if not self.draws_file.exists():
            raise RuntimeError(f"Draw file not found: {self.draws_file}")

        with self.draws_file.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            required = ["Date"] + [f"Number{i}" for i in range(1, self.game.main_count + 1)]
            if self.game.special_count == 2:
                required += ["Euro1", "Euro2"]
            else:
                required += ["Superzahl"]
            self._require_columns(headers, required)

            for row in reader:
                try:
                    numbers = [int(row[f"Number{i}"]) for i in range(1, self.game.main_count + 1)]
                    if self.game.special_count == 2:
                        special = [int(row["Euro1"]), int(row["Euro2"])]
                    else:
                        special = [int(row["Superzahl"])]
                except (TypeError, ValueError, KeyError):
                    continue

                if not all(self.game.main_min <= n <= self.game.main_max for n in numbers):
                    continue
                if not all(self.game.special_min <= n <= self.game.special_max for n in special):
                    continue

                self.draws.append(DrawRow(date=row["Date"], numbers=numbers, special=special))

    def _calculate(self) -> None:
        for draw in self.draws:
            sorted_main = sorted(draw.numbers)
            sorted_special = sorted(draw.special)

            self.number_counter.update(sorted_main)
            self.special_counter.update(sorted_special)

            self.pair_counter.update(combinations(sorted_main, 2))
            self.triple_counter.update(combinations(sorted_main, 3))
            self.quad_counter.update(combinations(sorted_main, 4))

            if self.game.special_count == 2:
                self.special_pair_counter.update([tuple(sorted_special)])

    def _percent(self, freq: int, denominator: int) -> float:
        return round((freq / denominator * 100.0) if denominator else 0.0, 2)

    def _save_number_stats(self, game_key: str) -> None:
        rows = []
        total_draws = len(self.draws)
        for number in range(self.game.main_min, self.game.main_max + 1):
            freq = self.number_counter.get(number, 0)
            rows.append(
                {
                    "Number": number,
                    "Frequency": freq,
                    "Percent": self._percent(freq, total_draws),
                }
            )
        rows.sort(key=lambda item: item["Frequency"], reverse=True)
        write_csv(
            self.output_dir / f"{game_key}_most_frequent_numbers.csv",
            ["Rank", "Number", "Frequency", "Percent"],
            [
                {"Rank": idx, "Number": row["Number"], "Frequency": row["Frequency"], "Percent": row["Percent"]}
                for idx, row in enumerate(rows, start=1)
            ],
        )

    def _save_special_stats(self, game_key: str) -> None:
        rows = []
        denominator = len(self.draws) * self.game.special_count
        for number in range(self.game.special_min, self.game.special_max + 1):
            freq = self.special_counter.get(number, 0)
            rows.append(
                {
                    "SpecialNumber": number,
                    "Frequency": freq,
                    "Percent": self._percent(freq, denominator),
                }
            )
        rows.sort(key=lambda item: item["Frequency"], reverse=True)
        write_csv(
            self.output_dir / f"{game_key}_most_frequent_special_numbers.csv",
            ["Rank", "SpecialNumber", "Frequency", "Percent"],
            [
                {
                    "Rank": idx,
                    "SpecialNumber": row["SpecialNumber"],
                    "Frequency": row["Frequency"],
                    "Percent": row["Percent"],
                }
                for idx, row in enumerate(rows, start=1)
            ],
        )

    def _save_combo_stats(self, game_key: str, size: int, counter: Counter[tuple[int, ...]]) -> None:
        top = counter.most_common(100)
        rows = []
        for idx, (combo, freq) in enumerate(top, start=1):
            rows.append(
                {
                    "Rank": idx,
                    "Combination": "-".join(str(num) for num in combo),
                    "Frequency": freq,
                    "Percent": self._percent(freq, len(self.draws)),
                }
            )
        name = {2: "pairs", 3: "triples", 4: "quadruples"}[size]
        write_csv(
            self.output_dir / f"{game_key}_most_frequent_{name}.csv",
            ["Rank", "Combination", "Frequency", "Percent"],
            rows,
        )

    def _save_special_pair_stats(self, game_key: str) -> None:
        if self.game.special_count != 2:
            return

        all_pairs = list(combinations(range(self.game.special_min, self.game.special_max + 1), 2))
        rows = []
        for pair in all_pairs:
            freq = self.special_pair_counter.get(pair, 0)
            rows.append(
                {
                    "Combination": f"{pair[0]}-{pair[1]}",
                    "Frequency": freq,
                    "Percent": self._percent(freq, len(self.draws)),
                }
            )
        rows.sort(key=lambda item: item["Frequency"], reverse=True)
        write_csv(
            self.output_dir / f"{game_key}_most_frequent_special_pairs.csv",
            ["Rank", "Combination", "Frequency", "Percent"],
            [
                {
                    "Rank": idx,
                    "Combination": row["Combination"],
                    "Frequency": row["Frequency"],
                    "Percent": row["Percent"],
                }
                for idx, row in enumerate(rows, start=1)
            ],
        )

    def _save_summary(self, game_key: str) -> None:
        rows = [
            {"Metric": "game", "Value": self.game.label},
            {"Metric": "draw_count", "Value": len(self.draws)},
            {"Metric": "top_main", "Value": str(self.number_counter.most_common(5))},
            {"Metric": "top_special", "Value": str(self.special_counter.most_common(5))},
            {"Metric": "top_pairs", "Value": str(self.pair_counter.most_common(5))},
        ]
        write_csv(self.output_dir / f"{game_key}_statistics_summary.csv", ["Metric", "Value"], rows)

    def run(self) -> int:
        self._load_draws()
        self._calculate()

        game_key = self.game.cli_name
        self._save_number_stats(game_key)
        self._save_special_stats(game_key)
        self._save_combo_stats(game_key, 2, self.pair_counter)
        self._save_combo_stats(game_key, 3, self.triple_counter)
        self._save_combo_stats(game_key, 4, self.quad_counter)
        self._save_special_pair_stats(game_key)
        self._save_summary(game_key)

        return len(self.draws)
