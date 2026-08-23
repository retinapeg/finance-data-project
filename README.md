# finance-data-project

## What this project is

This repository is a small educational quantitative-finance Python codebase.
Its current scope is:

- downloading market data from `yfinance`,
- validating incoming data,
- calculating a small set of baseline metrics already implemented in the repo,
- exposing them via a readable command-line workflow.

The project intentionally does **not** yet implement advanced formulas you have not yet
derived yourself (for example portfolio optimisation, PCA, regression, etc.).

## Current capabilities

- Market data ingestion with basic validation
- Existing metric calculations:
  - latest close
  - average close
  - total return
  - annualised volatility from simple daily returns
  - best and worst daily return
  - average daily volume
- Simple moving average calculation
- CLI entrypoint: `python -m finance_data_project <TICKER>`
- Result model with explicit fields via a dataclass
- Expanded tests for success and failure cases

## Architecture

- `src/finance_data_project/`
  - `market_data.py`: data ingestion and schema normalisation
  - `analytics.py`: metric calculations and moving average
  - `cli.py`: command-line workflow and error presentation
  - `validation.py`: reusable validation helpers
  - `models.py`: typed metric result container
  - `errors.py`: domain-specific exceptions
- repository root `src/` is the package source root.

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running the project

From repo root (without package installation):

```bash
PYTHONPATH=src python -m finance_data_project AAPL
```

Optional flags:

```bash
PYTHONPATH=src python -m finance_data_project AAPL --period 1y --interval 1d --log-level DEBUG
```

To run benchmark script with the same package layout:

```bash
PYTHONPATH=src python scripts/performance_benchmark.py
```

## Running tests

```bash
pytest -q
```

## Development

- Use the tests as the first source of truth.
- Keep functions explicit and readable.
- Add validation before performing calculations.
- Extend architecture with new modules only when a concrete implementation need exists.

## Planned roadmap (math will be derived separately)

Planned future areas are:

- log returns
- variance and covariance estimates
- portfolio risk tools
- regression / beta estimation
- factor models
- optimisation
- Monte Carlo
- derivative Greeks
- stochastic processes and Ito-based modules

Do not implement these formulas until you have derived them separately and want
to insert them into the existing interface.
