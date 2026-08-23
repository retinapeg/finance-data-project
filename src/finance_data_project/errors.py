"""Domain-specific exceptions used by the finance project."""


class FinanceProjectError(Exception):
    """Base exception for project-defined failures."""


class MarketDataError(FinanceProjectError):
    """Raised when market data cannot be downloaded from the provider."""


class DataValidationError(FinanceProjectError):
    """Raised when input data fails project validation."""

