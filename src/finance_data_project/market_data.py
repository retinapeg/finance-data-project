"""Market-data ingress and shape normalisation."""

from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd
import yfinance as yf

from .config import DEFAULT_INTERVAL, DEFAULT_PERIOD
from .errors import DataValidationError, MarketDataError
from .validation import (
    validate_interval,
    validate_non_empty_frame,
    validate_numeric_series,
    validate_period,
    validate_required_columns,
    validate_ticker,
)

LOGGER = logging.getLogger(__name__)

REQUIRED_COLUMNS = ("Close", "Volume")


PRICE_FIELDS = {
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
}


def _flatten_multiindex_columns(columns: pd.MultiIndex) -> list[str]:
    """Extract market-data field names from yfinance MultiIndex columns."""

    if "Price" in columns.names:
        return [
            str(value)
            for value in columns.get_level_values("Price")
        ]

    flattened: list[str] = []

    for column in columns:
        field_name = None

        for part in column:
            if str(part) in PRICE_FIELDS:
                field_name = str(part)
                break

        if field_name is None:
            raise DataValidationError(
                f"Could not identify price field in column {column!r}."
            )

        flattened.append(field_name)

    return flattened


def _normalize_column_names(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Normalize returned columns so downstream code can use stable labels."""
    if isinstance(raw_data.columns, pd.MultiIndex):
        normalised_columns = _flatten_multiindex_columns(raw_data.columns)
        if pd.Series(normalised_columns).duplicated().any():
            raise DataValidationError("Downloaded data has duplicate normalised columns.")
        normalised = raw_data.copy()
        normalised.columns = normalised_columns
        return normalised
    return raw_data


def _validate_data_schema(data: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Run project-specific checks before calculations."""
    validate_non_empty_frame(data, f"Market data for {ticker}")
    if data.columns.duplicated().any():
        raise DataValidationError(f"{ticker} Market data has duplicate columns.")
    validate_required_columns(data, REQUIRED_COLUMNS, f"Market data for {ticker}")

    close = validate_numeric_series(data["Close"], f"{ticker} Close")
    volume = validate_numeric_series(data["Volume"], f"{ticker} Volume")

    if (close < 0).any():
        raise DataValidationError(f"{ticker} Close contains negative values.")

    if (volume < 0).any():
        raise DataValidationError(f"{ticker} Volume contains negative values.")

    if close.isna().all():
        raise DataValidationError(f"{ticker} Close is all missing values.")

    if volume.isna().all():
        raise DataValidationError(f"{ticker} Volume is all missing values.")

    return data


def download_stock_data(
    ticker: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> pd.DataFrame:
    """Download OHLCV market data from yfinance.

    Parameters
    ----------
    ticker:
        One ticker symbol.
    period:
        yfinance period string, e.g. "1y".
    interval:
        yfinance interval string, e.g. "1d".

    Returns
    -------
    pd.DataFrame
        Normalised market data frame containing at least Close and Volume.
    """
    normalised_ticker = validate_ticker(ticker)
    validated_period = validate_period(period)
    validated_interval = validate_interval(interval)

    LOGGER.info("Downloading data for %s", normalised_ticker)
    LOGGER.debug(
        "Parameters: period=%s, interval=%s", validated_period, validated_interval
    )

    try:
        raw_data = yf.download(
            normalised_ticker,
            period=validated_period,
            interval=validated_interval,
            progress=False,
        )
    except Exception as exc:  # pragma: no cover - provider error behaviour
        raise MarketDataError(f"Download failed for {normalised_ticker}.") from exc

    if raw_data is None:
        raise MarketDataError(f"Download failed for {normalised_ticker}: provider returned None.")

    if raw_data.empty:
        raise MarketDataError(f"No rows returned for {normalised_ticker}.")

    LOGGER.info("Downloaded %s rows for %s", len(raw_data), normalised_ticker)

    normalised = _normalize_column_names(raw_data)
    validated = _validate_data_schema(normalised, normalised_ticker)

    return validated
