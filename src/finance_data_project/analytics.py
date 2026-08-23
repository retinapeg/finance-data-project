"""Analytics that are already present in the project.

The calculations in this file are intentionally limited to existing repository
capabilities. No new formulas are introduced here.
"""

from __future__ import annotations

from math import sqrt

import pandas as pd
import numpy as np
from .config import TRADING_DAYS_PER_YEAR
from .errors import DataValidationError
from .models import MarketMetrics
from .validation import (
    validate_non_empty_frame,
    validate_positive_integer,
    validate_required_columns,
    validate_numeric_series,
)


def _extract_price_series(data: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Extract and validate Close and Volume series with clear error messages."""
    validate_non_empty_frame(data, "Market data")
    validate_required_columns(data, ("Close", "Volume"), "Market data")

    close = validate_numeric_series(data["Close"], "Close")
    volume = validate_numeric_series(data["Volume"], "Volume")

    return close, volume


def calculate_metrics(
    data: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> MarketMetrics:
    """Calculate existing project-level metrics from market data.

    Parameters
    ----------
    data:
        DataFrame with Close and Volume columns.
    trading_days:
        Number of trading days used for annualisation.
    """
    validated_trading_days = validate_positive_integer(trading_days, "trading_days")
    close, volume = _extract_price_series(data)

    daily_returns = close.pct_change().dropna()

    latest_close = float(close.iloc[-1])
    average_close = float(close.mean())
    total_return = float(close.iloc[-1] / close.iloc[0] - 1)
    annualised_volatility = float(daily_returns.std() * sqrt(validated_trading_days))
    best_day = float(daily_returns.max()) if not daily_returns.empty else float("nan")
    worst_day = float(daily_returns.min()) if not daily_returns.empty else float("nan")
    average_volume = float(volume.mean())

    return MarketMetrics(
        latest_close=latest_close,
        average_close=average_close,
        total_return=total_return,
        annualised_volatility=annualised_volatility,
        best_day=best_day,
        worst_day=worst_day,
        average_volume=average_volume,
    )


def calculate_moving_average(data: pd.DataFrame, window: int) -> pd.Series:
    """Calculate a simple moving average over the Close column."""
    validated_window = validate_positive_integer(window, "window")
    close, _ = _extract_price_series(data)
    return close.rolling(validated_window).mean()

def calculate_two_asset_portfolio_variance(
    weight_1: float,
    weight_2: float,
    variance_1: float,
    variance_2: float,
    covariance: float,
) -> float:
    """Calculate the variance of a two-asset portfolio."""

    portfolio_variance = weight_1**2*variance_1 + 2*weight_1*weight_2*covariance+ weight_2**2*variance_2

    return portfolio_variance

def calculate_portfolio_variance_matrix(
    weights: np.ndarray,
    covariance_matrix: np.ndarray,
)   -> float:
    portfolio_variance = weights.transpose() @ covariance_matrix @ weights

    return float(portfolio_variance)

def calculate_sample_covariance_matrix(
    returns: np.ndarray,
    ) -> np.ndarray:
    n_observations = returns.shape[0]
    mean_returns = returns.mean(axis=0)
    centered_returns = returns - mean_returns
    sum_of_products = centered_returns.transpose() @ centered_returns
    covariance_matrix = sum_of_products / (n_observations - 1)
    return covariance_matrix