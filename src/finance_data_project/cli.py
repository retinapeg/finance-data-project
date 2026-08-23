"""Command-line interface for market metrics."""

from __future__ import annotations

import argparse
import logging
import sys

from .analytics import calculate_metrics
from .config import DEFAULT_INTERVAL, DEFAULT_PERIOD
from .errors import DataValidationError, FinanceProjectError, MarketDataError
from .market_data import download_stock_data
from .reporting import format_market_summary
from .validation import validate_ticker, validate_period, validate_interval


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute baseline market metrics.")
    parser.add_argument("ticker", help="Ticker symbol, for example AAPL.")
    parser.add_argument(
        "--period",
        default=DEFAULT_PERIOD,
        help=f"Data period (default: {DEFAULT_PERIOD})",
    )
    parser.add_argument(
        "--interval",
        default=DEFAULT_INTERVAL,
        help=f"Data interval (default: {DEFAULT_INTERVAL})",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Console logging level.",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    """Execute CLI flow and return a shell exit code."""
    args = _build_parser().parse_args(argv)
    logging.basicConfig(level=args.log_level, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    try:
        ticker = validate_ticker(args.ticker)
        validate_period(args.period)
        validate_interval(args.interval)

        logger.info("Fetching data for %s", ticker)
        data = download_stock_data(ticker=ticker, period=args.period, interval=args.interval)
        logger.info("Fetched %s rows", len(data))

        logger.info("Calculating metrics")
        metrics = calculate_metrics(data)
        output = format_market_summary(ticker, metrics)
        print(output)
    except (MarketDataError, DataValidationError, FinanceProjectError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        logger.warning("Execution interrupted.")
        return 130

    return 0


def main() -> int:
    """Main entry point expected by __main__ modules."""
    return run()

