"""Output helpers for command-line reporting."""

from __future__ import annotations

from .models import MarketMetrics


def format_market_summary(ticker: str, metrics: MarketMetrics) -> str:
    """Render the current metrics in a human-readable summary."""
    lines = [
        "",
        f"{ticker} MARKET SUMMARY",
        "-" * 30,
        f"Latest close:           ${metrics.latest_close:.2f}",
        f"Average close:          ${metrics.average_close:.2f}",
        f"Total return:            {metrics.total_return:.2%}",
        f"Annualised volatility:   {metrics.annualised_volatility:.2%}",
        f"Best trading day:        {metrics.best_day:.2%}",
        f"Worst trading day:       {metrics.worst_day:.2%}",
        f"Average daily volume:    {metrics.average_volume:,.0f}",
    ]
    return "\n".join(lines)

