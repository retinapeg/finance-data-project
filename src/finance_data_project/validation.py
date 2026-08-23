"""Validation helpers used by data loading and analytics layers."""

from __future__ import annotations

import re
from typing import Iterable

import numpy as np
import pandas as pd

from .errors import DataValidationError


def validate_ticker(ticker: str) -> str:
    """Validate and normalise a ticker string.

    Parameters
    ----------
    ticker:
        Raw ticker symbol provided by user input.

    Returns
    -------
    str
        Normalised ticker symbol in upper-case with trimmed whitespace.
    """
    if not isinstance(ticker, str):
        raise DataValidationError("Ticker must be a string.")

    normalised = ticker.strip().upper()
    if not normalised:
        raise DataValidationError("Ticker cannot be empty.")

    if not re.fullmatch(r"[A-Z0-9.\-^]+", normalised):
        raise DataValidationError(
            "Ticker contains unsupported characters. Use letters, numbers, '.', '-' or '^'."
        )

    return normalised


def validate_period(period: str) -> str:
    """Validate yfinance period input.

    The function keeps checks deliberately lightweight because the underlying API
    already supports many period strings.
    """
    if not isinstance(period, str):
        raise DataValidationError("Period must be a string.")

    normalised = period.strip()
    if not normalised:
        raise DataValidationError("Period cannot be empty.")

    return normalised


def validate_interval(interval: str) -> str:
    """Validate yfinance interval input."""
    if not isinstance(interval, str):
        raise DataValidationError("Interval must be a string.")

    normalised = interval.strip()
    if not normalised:
        raise DataValidationError("Interval cannot be empty.")

    return normalised


def validate_non_empty_frame(data: pd.DataFrame, context: str) -> pd.DataFrame:
    """Ensure a DataFrame is not empty and has at least one row."""
    if not isinstance(data, pd.DataFrame):
        raise DataValidationError(f"{context} must be a pandas DataFrame.")

    if data.empty:
        raise DataValidationError(f"{context} is empty.")

    return data


def validate_required_columns(data: pd.DataFrame, required: Iterable[str], context: str) -> None:
    """Check that all required columns are present."""
    missing = [column for column in required if column not in data.columns]
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise DataValidationError(f"{context} is missing required columns: {missing_text}.")


def validate_positive_integer(value: int, name: str) -> int:
    """Validate strictly positive integers used by windowing/statistical settings."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise DataValidationError(f"{name} must be an integer.")
    if value <= 0:
        raise DataValidationError(f"{name} must be greater than zero.")
    return value


def validate_numeric_series(series: pd.Series, name: str) -> pd.Series:
    """Validate a numeric, finite price/volume series."""
    if not pd.api.types.is_numeric_dtype(series):
        raise DataValidationError(f"{name} must contain numeric values.")

    if series.isna().any():
        raise DataValidationError(f"{name} contains missing values.")

    if not bool(np.isfinite(series).all()):
        raise DataValidationError(f"{name} contains non-finite values.")

    return series
