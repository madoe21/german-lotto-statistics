# German Lotto Statistics

Statistical analysis for **LOTTO 6aus49** and **Eurojackpot** - automatically updated after every draw.

**[View Live Statistics](https://madoe21.github.io/german-lotto-statistics/)**

## Features

- Automatic retrieval of new draw results via Lotto Brandenburg API
- Statistical analysis: most frequent numbers, pairs, triples, quadruples
- Interactive chart visualization on GitHub Pages
- GitHub Actions updates data automatically after every draw

## Update Schedule

| Game | Draw | Data Update |
|------|------|-------------|
| Eurojackpot | Tue + Fri | Wed + Sat 08:00 UTC |
| LOTTO 6aus49 | Wed + Sat | Thu + Sun 08:00 UTC |

## Usage

### Scraper

Fetch new draw results:

```bash
python src/scraper.py lotto
python src/scraper.py eurojackpot
python src/scraper.py lotto --from-date 01.01.2024
```

### Analyzer

Generate statistics from draw data:

```bash
python src/analyzer.py lotto
python src/analyzer.py eurojackpot
```

### Options

| Option | Description |
|--------|-------------|
| `--from-date DD.MM.YYYY` | Only include draws from this date |
| `--data-dir data` | Directory for CSV files |
| `--draws-file <path>` | Custom path for draws CSV |

## Project Structure

```
src/
  scraper.py              # CLI: fetch draw data
  analyzer.py             # CLI: generate statistics
  lotto/
    api_client.py          # Lotto Brandenburg API client
    config.py              # Game configuration (6aus49, Eurojackpot)
    csv_io.py              # CSV read/write operations
    scraper_service.py     # Scraper logic
    analyzer_service.py    # Analyzer logic
data/
  *_draws.csv              # Raw draw data
  *_most_frequent_*.csv    # Statistical results
  *_statistics_summary.csv # Summaries
docs/
  index.html               # GitHub Pages visualization
```

## API Source

Lotto Brandenburg endpoints:

- `/app/getDrawResultYears` - Available years
- `/app/getDrawResultDates` - Draw dates for a year
- `/app/getDrawResults` - Result of a single draw

Example requests: [lotto_api_examples.http](lotto_api_examples.http)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Found a bug or have a suggestion? Feel free to create an issue or pull request.

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
