# Serenity & Velocity

Two investment funds of $2 billion built with the Markowitz model: Serenity for cautious clients,
Velocity for clients who accept more risk. 25 assets each, three years of daily data
(November 2023 to November 2026).

**Website:** https://moha-ne.github.io/portfolio-optimization/

| | Serenity | Velocity |
|---|---|---|
| Sharpe ratio | 1.97 | 2.04 |
| Expected return (annual) | 20.5% | 38.4% |
| Volatility (annual) | 8.4% | 16.9% |
| Beta vs S&P 500 | 0.26 | 1.12 |
| Alpha (annual) | +13.5% | +28.7% |
| VaR 99%, 10 days, on $2bn | $61.6M | $126.0M |

## What's in the repository

- `docs/`: the website (published with GitHub Pages)
  - `index.html`: home page with the two funds and the report
  - `1.html`, `2.html`: dashboards of Serenity and Velocity, six charts each
  - `analytics/`: one page per chart, with comments
  - `report.html`: results, method and limits
  - `code.html`: the Python scripts, readable in the browser
- `docs/scripts/1` (Serenity) and `docs/scripts/2` (Velocity): the Python scripts
  - `1.py`: prices, returns, Markowitz simulation (10,000 portfolios), efficient frontier,
    risk contribution, Value at Risk
  - `2.py`: z-scores (momentum, volatility, beta)
  - `3.py`: beta and alpha against the S&P 500
  - `4.py`: latest news on the largest positions
  - `gauge.py`: volatility gauge of the home page
  - `par84.py`: chart style and output folder

## Run the scripts

```bash
pip install -r requirements.txt
cd docs/scripts/1
python 1.py
```

The charts are written to `docs/img/1` (or `docs/img/2` for Velocity). The data is downloaded
from Yahoo Finance, so the numbers change a little when the scripts are run on a later date.

## Context

Team assignment for the Portfolio Management course of the MBA Finance & Data Performance at
ESLSCA Paris (2026), built on the course's Python scripts. This is the version we handed in,
with a report page, a code page and one chart fix added afterwards.

Mohamed Moussa Moha
