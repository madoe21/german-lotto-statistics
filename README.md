# Lotto Tool Suite (Eurojackpot + 6aus49)

This project supports two games:

- `eurojackpot`
- `lotto` (LOTTO 6aus49)

The tooling is API-based and no longer uses Selenium/browser scraping.

## Architecture

```text
src/
  scraper.py
  analyzer.py
    scraper.py
  analyzer.py
  lotto/
    api_client.py
    config.py
    csv_io.py
    scraper_service.py
    analyzer_service.py
data/
  <draw files and generated statistics>
lotto_api_examples.http
```

## API Source

The implementation uses these Lotto Brandenburg endpoints:

- `/app/getDrawResultYears`
- `/app/getDrawResultDates`
- `/app/getDrawResults`

Game mapping:

- Eurojackpot -> `gameType=EURO`
- LOTTO 6aus49 -> `gameType=LOTTO`

Request examples are in `lotto_api_examples.http`.

## Usage

All commands take a `game` argument:

- `eurojackpot`
- `lotto` (alias: `6aus49`)

### 1) Scraper

```bash
python src/scraper.py eurojackpot
python src/scraper.py lotto
python src/scraper.py lotto --from-date 01.01.2024
```

Options:

- `--from-date DD.MM.YYYY`
- `--data-dir data`
- `--draws-file <custom path>`

Default draw files:

- `data/eurojackpot_draws.csv`
- `data/lotto_draws.csv`

### 2) Analyzer

```bash
python src/analyzer.py eurojackpot
python src/analyzer.py lotto
```

Outputs are written to `data/`, for example:

- `data/eurojackpot_most_frequent_numbers.csv`
- `data/eurojackpot_most_frequent_special_numbers.csv`
- `data/eurojackpot_most_frequent_pairs.csv`
- `data/eurojackpot_most_frequent_triples.csv`
- `data/eurojackpot_most_frequent_quadruples.csv`
- `data/eurojackpot_most_frequent_special_pairs.csv` (Eurojackpot only)
- `data/eurojackpot_statistics_summary.csv`

Equivalent files are generated for `lotto_*`.



## Notes

- Legacy root scripts were removed.
- Use only the `src/*.py` entrypoints shown above.
- No browser dependencies are required.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Found a bug or have a suggestion for improvement? Please create an issue or pull request.

I appreciate everyone who supports me and the project! For any requests and suggestions, feel free to provide feedback.

<p>
  <a href="https://www.buymeacoffee.com/madoe21">
    <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" height="50" alt="Buy Me a Coffee">
  </a>

  <a href="https://ko-fi.com/madoe21">
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" height="50" alt="Ko-fi">
  </a>

  <a href="https://paypal.me/MartinD809">
    <img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg" height="50" alt="PayPal">
  </a>
</p>