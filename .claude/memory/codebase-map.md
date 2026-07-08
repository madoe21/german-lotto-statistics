# Codebase map (onboarding 2026-07-08)

**German Lotto Statistics** — statistical analysis for **LOTTO 6aus49** and
**Eurojackpot**, auto-updated after every draw and published as an interactive
GitHub Pages site.

## Layout
- `src/scraper.py` — fetches new draw results (Lotto Brandenburg API).
- `src/analyzer.py` — statistics: frequent numbers, pairs, triples, quadruples.
- `src/__init__.py` — package init.
- `docs/index.html` — the interactive charts (GitHub Pages front end).
- `.venv/` — local virtualenv (not committed).
- `README.md` / `README.de.md` (keep in sync).

## Data flow
GitHub Actions (post-draw) → `scraper.py` pulls results → `analyzer.py`
computes stats → output feeds `docs/` → Pages redeploys.

## Conventions
- Pure Python; keep scraper/analyzer separable and testable.
- Data auto-updates via CI; no manual steps.
- No secrets in the repo (public API); keep both READMEs in sync.

## Notes
Validation = run scraper+analyzer locally against recent draws; check the
generated stats/charts. See [[codebase-map]] of german-lotto-generator (sibling
project, same domain).
