"""Scaffolded interfaces for future quantitative modules.

These are intentionally not implemented yet because the maths are to be derived
in a separate step.
"""

from __future__ import annotations

import pandas as pd


def calculate_log_returns(close_prices: pd.Series) -> pd.Series:
    """TODO(math): derive log-return formula, then implement here."""
    raise NotImplementedError("Mathematical derivation for log returns has not been implemented yet.")


def estimate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
    """TODO(math): derive beta from regression, then implement here."""
    raise NotImplementedError("Beta estimation implementation is intentionally pending derivation.")

