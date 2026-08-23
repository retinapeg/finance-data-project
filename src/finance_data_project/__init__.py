"""Core package for the finance-data project.

The module intentionally keeps imports small and explicit so that a reader can
trace each dependency directly.
"""

from .analytics import calculate_metrics, calculate_moving_average
from .cli import run as run_cli
from .errors import DataValidationError, MarketDataError
from .market_data import download_stock_data
from .models import MarketMetrics

__all__ = [
    "calculate_metrics",
    "calculate_moving_average",
    "download_stock_data",
    "MarketMetrics",
    "DataValidationError",
    "MarketDataError",
    "run_cli",
]

__version__ = "0.2.0"

