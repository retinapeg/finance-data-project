# Codebase Guide

## How this repository is organised

- `src/finance_data_project/` contains the main application code.
- repository root `src/` is the package source root.
- `tests/` contains pytest tests for both analytics and CLI paths.
- `requirements.txt` contains runtime dependencies.
- `requirements-dev.txt` contains development test dependency.

## Entry points

Primary:

```bash
PYTHONPATH=src python -m finance_data_project AAPL
```

This runs `finance_data_project.__main__`, which delegates to `finance_data_project.cli.main`
and prints a market summary.

When running from the repository root without package installation, set `PYTHONPATH=src`.

## Data ingestion flow

1. `cli.run()` parses command-line input.
2. Ticker/period/interval inputs are validated by `validation.validate_ticker`,
   `validate_period`, and `validate_interval`.
3. `market_data.download_stock_data()` calls `yfinance.download(...)`.
4. Downloaded columns are normalised (`_normalize_column_names`) for predictable names.
5. Data schema is validated (`Close`, `Volume`, numeric, finite, non-empty).

## Calculation flow

1. `analytics.calculate_metrics()` receives validated DataFrame.
2. `Close` and `Volume` are extracted and validated again locally.
3. Daily returns are computed as `pct_change()` on close prices.
4. Metrics are assembled into `MarketMetrics`.

`analytics.calculate_moving_average()` also reads the `Close` column and applies
`rolling(window).mean()`.

## Result flow

- `calculate_metrics()` returns `MarketMetrics` (a dataclass).
- `MarketMetrics.as_dict()` gives a plain dictionary if that shape is required.
- `reporting.format_market_summary()` converts the metrics into printable output.

## Validation flow

- `validation.py` owns shared validation checks:
  - string format checks
  - non-empty input checks
  - column and type checks
  - positive integer checks
- Analytics adds a local, calculation-specific guard before computing.

## Testing flow

- Unit tests cover normal calculations and expected error paths:
  - valid metrics
  - moving average window boundaries
  - validation failures
  - CLI execution path (mocked market download)
- Tests avoid calling external services directly by monkeypatching `yf.download`.

## Dependency directions

- CLI (`cli.py`) depends on analytics and market-data.
- Analytics (`analytics.py`) depends on models and validation helpers.
- Market-data (`market_data.py`) depends on validator and exception modules.

## Python concepts encountered

The following features are used in this version:

- **Dataclasses**
  - used in `models.py` for `MarketMetrics`.
  - reason: clear, explicit, readable output container.
  - simple equivalent:
    ```python
    class MarketMetrics:
        def __init__(self, latest_close, average_close, total_return, annualised_volatility, best_day, worst_day, average_volume):
            self.latest_close = latest_close
            ...
    ```

- **Type hints**
  - used on function signatures and return types.
  - reason: readable contracts and easier test/IDE feedback.
  - equivalent in untyped form is the same function without annotations.

- **Tuple unpacking**
  - used in `analytics._extract_price_series()` return type.
  - explicit form:
    ```python
    pair = _extract_price_series(data)
    close = pair[0]
    volume = pair[1]
    ```

- **`argparse`**
  - used for CLI parsing in `cli.py`.
  - explicit alternative:
    ```python
    if len(sys.argv) == 1: ...
    ```

- **Logging**
  - used with standard `logging` module.
  - explicit equivalent:
    `print()` statements for every event.

- **Dataclass `frozen=True`**
  - makes `MarketMetrics` immutable once created.
  - equivalent would be mutable attributes that could change accidentally.

## How to trace a full request

1. Start at `finance_data_project.cli.run()`.
2. Read validation in `validation.py`.
3. Follow provider call in `market_data.download_stock_data()`.
4. Follow metrics in `analytics.calculate_metrics()`.
5. Follow output in `reporting.format_market_summary()`.
