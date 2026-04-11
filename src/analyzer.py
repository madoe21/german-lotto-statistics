from __future__ import annotations

import argparse
from pathlib import Path

from lotto.analyzer_service import LotteryAnalyzerService
from lotto.config import parse_game
from lotto.csv_io import DataPaths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create statistics for Eurojackpot or LOTTO 6aus49.")
    parser.add_argument("game", help="eurojackpot | lotto (alias: 6aus49)")
    parser.add_argument("--data-dir", default="data", help="Directory for draw and statistics CSV files")
    parser.add_argument("--draws-file", help="Optional custom draws CSV path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    game = parse_game(args.game)

    paths = DataPaths(args.data_dir)
    draws_file = Path(args.draws_file) if args.draws_file else paths.draws(game)

    service = LotteryAnalyzerService(game=game, draws_file=draws_file, output_dir=Path(args.data_dir))
    draw_count = service.run()

    print("=" * 60)
    print(f"Game: {game.label}")
    print(f"Input: {draws_file}")
    print(f"Output dir: {Path(args.data_dir)}")
    print(f"Processed draws: {draw_count}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
