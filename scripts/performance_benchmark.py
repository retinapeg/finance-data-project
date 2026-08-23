"""Small performance exploration script for current implemented operations.

Run from repository root with the package source on ``PYTHONPATH``:

    PYTHONPATH=src python scripts/performance_benchmark.py
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from finance_data_project.analytics import calculate_metrics, calculate_moving_average


def _sample_data(n_rows: int = 2_000) -> pd.DataFrame:
    prices = pd.Series(np.linspace(100.0, 200.0, n_rows))
    volumes = pd.Series(np.arange(1, n_rows + 1) * 1000)
    dates = pd.date_range("2020-01-01", periods=n_rows, freq="B")
    return pd.DataFrame(
        {
            "Close": prices.to_numpy(),
            "Volume": volumes.to_numpy(),
        },
        index=dates,
    )


def run_benchmarks() -> None:
    data = _sample_data()

    start = time.perf_counter()
    for _ in range(200):
        calculate_metrics(data)
    print(f"calculate_metrics x200: {time.perf_counter() - start:.4f}s")

    start = time.perf_counter()
    for _ in range(200):
        calculate_moving_average(data, 20)
    print(f"calculate_moving_average x200: {time.perf_counter() - start:.4f}s")


if __name__ == "__main__":
    run_benchmarks()
