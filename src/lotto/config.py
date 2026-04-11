from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GameConfig:
    cli_name: str
    label: str
    api_game_type: str
    main_count: int
    main_min: int
    main_max: int
    special_count: int
    special_min: int
    special_max: int
    special_label: str
    main_threshold_percent: float
    special_threshold_percent: float
    special_pair_min_percent: float

    @property
    def draw_headers(self) -> list[str]:
        headers = ["Date"] + [f"Number{i}" for i in range(1, self.main_count + 1)]
        if self.special_count == 2:
            headers += ["Euro1", "Euro2"]
        elif self.special_count == 1:
            headers += ["Superzahl"]
        return headers


GAMES: Dict[str, GameConfig] = {
    "eurojackpot": GameConfig(
        cli_name="eurojackpot",
        label="Eurojackpot",
        api_game_type="EURO",
        main_count=5,
        main_min=1,
        main_max=50,
        special_count=2,
        special_min=1,
        special_max=12,
        special_label="Eurozahlen",
        main_threshold_percent=9.5,
        special_threshold_percent=8.0,
        special_pair_min_percent=1.0,
    ),
    "lotto": GameConfig(
        cli_name="lotto",
        label="LOTTO 6aus49",
        api_game_type="LOTTO",
        main_count=6,
        main_min=1,
        main_max=49,
        special_count=1,
        special_min=0,
        special_max=9,
        special_label="Superzahl",
        main_threshold_percent=12.0,
        special_threshold_percent=9.5,
        special_pair_min_percent=0.0,
    ),
}

ALIASES = {
    "euro": "eurojackpot",
    "ej": "eurojackpot",
    "eurojackpot": "eurojackpot",
    "lotto": "lotto",
    "6aus49": "lotto",
    "6aus 49": "lotto",
}


def parse_game(value: str) -> GameConfig:
    key = ALIASES.get(value.strip().lower())
    if not key:
        raise ValueError("Unsupported game. Use 'eurojackpot' or 'lotto' (alias: '6aus49').")
    return GAMES[key]
