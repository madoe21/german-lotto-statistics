from __future__ import annotations

import argparse
from pathlib import Path

from lotto.api_client import LottoBrandenburgApiClient
from lotto.config import parse_game
from lotto.csv_io import DataPaths
from lotto.scraper_service import LotteryScraperService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download draw data for Eurojackpot or LOTTO 6aus49 via API.")
    parser.add_argument("game", help="eurojackpot | lotto (alias: 6aus49)")
    parser.add_argument("--from-date", dest="from_date", help="Only include draws from DD.MM.YYYY")
    parser.add_argument("--data-dir", default="data", help="Directory for draw and statistics CSV files")
    parser.add_argument("--draws-file", help="Optional custom draws CSV path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    game = parse_game(args.game)

    paths = DataPaths(args.data_dir)
    draws_file = Path(args.draws_file) if args.draws_file else paths.draws(game)

    service = LotteryScraperService(LottoBrandenburgApiClient(), game, draws_file)
    stats = service.run(from_date=args.from_date)

    print("=" * 60)
    print(f"Game: {game.label}")
    print(f"Output: {draws_file}")
    print(f"Added: {stats.added}")
    print(f"Skipped existing: {stats.skipped_existing}")
    print(f"Skipped by date filter: {stats.skipped_date_filter}")
    print(f"Errors: {stats.errors}")
    print("=" * 60)
    return 0 if stats.errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
