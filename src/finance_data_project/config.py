"""Project-level configuration values.

These constants are intentionally explicit so the meaning of numeric values is
clear at the point of use.
"""

from __future__ import annotations

TRADING_DAYS_PER_YEAR = 252
"""Trading days used for annualising daily volatility."""

DEFAULT_PERIOD = "1y"
"""Default yfinance period used by the market-data fetcher."""

DEFAULT_INTERVAL = "1d"
"""Default yfinance interval used by the market-data fetcher."""

