from __future__ import annotations

from math import sqrt

import pandas as pd
import pytest
import numpy as np
from finance_data_project.analytics import calculate_metrics, calculate_moving_average
from finance_data_project.cli import run
from finance_data_project.market_data import download_stock_data
from finance_data_project.validation import (
    validate_ticker,
    validate_positive_integer,
    validate_numeric_series,
)
from finance_data_project.errors import DataValidationError, MarketDataError
from finance_data_project.future_scaffolding import (
    calculate_log_returns,
    estimate_beta,
)
from finance_data_project.market_data import _normalize_column_names

from finance_data_project.analytics import (
    calculate_metrics,
    calculate_moving_average,
    calculate_portfolio_variance_matrix,
    calculate_sample_covariance_matrix,
)


def test_calculate_metrics():
    data = pd.DataFrame(
        {
            "Close": [100, 110, 99],
            "Volume": [1000, 2000, 3000],
        }
    )

    metrics = calculate_metrics(data)

    expected_volatility = sqrt(0.02) * sqrt(252)

    assert metrics.latest_close == 99
    assert metrics.average_close == pytest.approx(103)
    assert metrics.average_volume == 2000
    assert metrics.total_return == pytest.approx(-0.01)
    assert metrics.best_day == pytest.approx(0.10)
    assert metrics.worst_day == pytest.approx(-0.10)
    assert metrics.annualised_volatility == pytest.approx(expected_volatility)


def test_calculate_moving_average():
    data = pd.DataFrame({"Close": [100, 110, 120, 130, 140], "Volume": [500, 700, 900, 1100, 1300]})

    result = calculate_moving_average(data, 3)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == pytest.approx(110)
    assert result.iloc[3] == pytest.approx(120)
    assert result.iloc[4] == pytest.approx(130)


def test_calculate_moving_average_zero_window():
    data = pd.DataFrame({"Close": [100, 110, 120, 130, 140], "Volume": [500, 700, 900, 1100, 1300]})
    with pytest.raises(DataValidationError):
        calculate_moving_average(data, 0)


def test_calculate_moving_average_negative_window():
    data = pd.DataFrame({"Close": [100, 110, 120, 130, 140], "Volume": [500, 700, 900, 1100, 1300]})
    with pytest.raises(DataValidationError):
        calculate_moving_average(data, -1)


def test_calculate_metrics_empty_input_raises():
    with pytest.raises(DataValidationError):
        calculate_metrics(pd.DataFrame())


def test_calculate_metrics_missing_columns():
    with pytest.raises(DataValidationError):
        calculate_metrics(pd.DataFrame({"Close": [100, 110, 120]}))


def test_calculate_metrics_one_row_has_defined_structure():
    data = pd.DataFrame({"Close": [100], "Volume": [3000]})

    metrics = calculate_metrics(data)

    assert metrics.latest_close == 100.0
    assert metrics.total_return == pytest.approx(0.0)
    assert pd.isna(metrics.best_day)
    assert pd.isna(metrics.worst_day)
    assert pd.isna(metrics.annualised_volatility)


def test_validate_ticker_normalises_and_rejects_bad_values():
    assert validate_ticker("  aapl ") == "AAPL"
    with pytest.raises(DataValidationError):
        validate_ticker("")
    with pytest.raises(DataValidationError):
        validate_ticker("AAPL/USD")


def test_validate_positive_integer_rejects_invalid_types_and_booleans():
    with pytest.raises(DataValidationError):
        validate_positive_integer(0, "window")
    with pytest.raises(DataValidationError):
        validate_positive_integer(-1, "window")
    with pytest.raises(DataValidationError):
        validate_positive_integer(True, "window")


def test_validate_numeric_series_rejects_non_numeric_data():
    with pytest.raises(DataValidationError):
        validate_numeric_series(pd.Series(["a", "b", "c"]), "Close")


def test_download_stock_data_raises_on_empty_provider_response(monkeypatch):
    def fake_download(*args, **kwargs):
        return pd.DataFrame()

    monkeypatch.setattr("finance_data_project.market_data.yf.download", fake_download)

    with pytest.raises(MarketDataError):
        download_stock_data("AAPL")


def test_download_stock_data_raises_on_none_provider_response(monkeypatch):
    monkeypatch.setattr("finance_data_project.market_data.yf.download", lambda *args, **kwargs: None)

    with pytest.raises(MarketDataError):
        download_stock_data("AAPL")


def test_download_stock_data_normalises_multiindex_columns(monkeypatch):
    raw = pd.DataFrame(
        {("AAPL", "Close"): [100, 110], ("AAPL", "Volume"): [1000, 2000]},
        index=pd.date_range("2026-01-01", periods=2),
    )

    def fake_download(*args, **kwargs):
        return raw

    monkeypatch.setattr("finance_data_project.market_data.yf.download", fake_download)

    result = download_stock_data("aapl")
    assert set(result.columns) == {"Close", "Volume"}
    assert len(result) == 2


def test_normalize_column_names_raises_on_duplicate_flattened_names():
    raw = pd.DataFrame(
        {("AAPL", "Close"): [100], ("MSFT", "Close"): [110], ("AAPL", "Volume"): [1000], ("MSFT", "Volume"): [2000]},
        index=[pd.Timestamp("2026-01-01")],
    )
    with pytest.raises(DataValidationError):
        _normalize_column_names(raw)


def test_download_stock_data_rejects_duplicate_columns(monkeypatch):
    raw = pd.DataFrame(
        [[100, 101, 1000, 1001], [110, 111, 2000, 2001]],
        index=pd.date_range("2026-01-01", periods=2),
        columns=["Close", "Close", "Volume", "Volume"],
    )

    monkeypatch.setattr("finance_data_project.market_data.yf.download", lambda *args, **kwargs: raw)

    with pytest.raises(DataValidationError):
        download_stock_data("AAPL")


def test_cli_run_prints_expected_output(monkeypatch, capsys):
    sample = pd.DataFrame(
        {"Close": [100, 110, 99], "Volume": [1000, 2000, 3000]},
        index=pd.date_range("2026-01-01", periods=3),
    )

    monkeypatch.setattr(
        "finance_data_project.cli.download_stock_data",
        lambda ticker, period, interval: sample,
    )

    exit_code = run(["AAPL", "--period", "1y", "--interval", "1d"])

    captured = capsys.readouterr().out
    assert exit_code == 0
    assert "AAPL MARKET SUMMARY" in captured
    assert "Latest close" in captured


def test_future_scaffold_functions_are_explicitly_unimplemented():
    with pytest.raises(NotImplementedError):
        calculate_log_returns(pd.Series([1.0, 1.1, 1.2]))
    with pytest.raises(NotImplementedError):
        estimate_beta(pd.Series([1, 2, 3]), pd.Series([2, 3, 4]))

def test_normalize_real_yfinance_multiindex():
    columns = pd.MultiIndex.from_tuples(
        [
            ("Close", "AAPL"),
            ("High", "AAPL"),
            ("Low", "AAPL"),
            ("Open", "AAPL"),
            ("Volume", "AAPL"),
        ],
        names=["Price", "Ticker"],
    )

    raw = pd.DataFrame(
        [[100.0, 102.0, 99.0, 101.0, 1_000_000]],
        columns=columns,
    )

    result = _normalize_column_names(raw)

    assert list(result.columns) == [
        "Close",
        "High",
        "Low",
        "Open",
        "Volume",
    ]

def test_calculate_portfolio_variance_matrix():
    weights = np.array([0.5, 0.5])

    covariance_matrix = np.array([
        [0.04, 0.01],
        [0.01, 0.09],
    ])

    result = calculate_portfolio_variance_matrix(
        weights,
        covariance_matrix,
    )

    assert result == pytest.approx(0.0375)

def test_calculate_sample_covariance_matrix():
    returns = np.array([
        [0.01, 0.02],
        [0.02, 0.04],
        [0.03, 0.06],
    ])

    result = calculate_sample_covariance_matrix(returns)

    expected = np.array([
        [0.0001, 0.0002],
        [0.0002, 0.0004],
    ])

    assert np.allclose(result, expected)

def test_covariance_to_portfolio_variance_pipeline():
    returns = np.array([
        [0.01, 0.02],
        [0.02, 0.04],
        [0.03, 0.06],
    ])

    weights = np.array([0.5, 0.5])

    covariance_matrix = calculate_sample_covariance_matrix(returns)

    portfolio_variance = calculate_portfolio_variance_matrix(
        weights,
        covariance_matrix,
    )

    assert portfolio_variance == pytest.approx(0.000225)