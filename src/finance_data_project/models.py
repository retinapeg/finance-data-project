"""Data models used by analytics outputs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketMetrics:
    """Container for current market-metric results.

    Fields are kept explicit so every metric is discoverable while reading the
    code.
    """

    latest_close: float
    average_close: float
    total_return: float
    annualised_volatility: float
    best_day: float
    worst_day: float
    average_volume: float

    def as_dict(self) -> dict[str, float]:
        """Return a plain dictionary representation."""
        return {
            "latest_close": self.latest_close,
            "average_close": self.average_close,
            "total_return": self.total_return,
            "annualised_volatility": self.annualised_volatility,
            "best_day": self.best_day,
            "worst_day": self.worst_day,
            "average_volume": self.average_volume,
        }

