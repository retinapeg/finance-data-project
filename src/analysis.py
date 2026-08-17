from math import sqrt


def calculate_metrics(data):
    close = data["Close"].squeeze()
    volume = data["Volume"].squeeze()
    daily_returns = close.pct_change().dropna()
    latest_close = close.iloc[-1]
    average_close = close.mean()
    total_return = close.iloc[-1] / close.iloc[0] - 1
    annualised_volatility =  daily_returns.std() * sqrt(252)
    best_day = daily_returns.max()
    worst_day = daily_returns.min()
    average_volume = volume.mean()

    return {
    "latest_close": latest_close,
    "average_close": average_close,
    "total_return": total_return,
    "annualised_volatility": annualised_volatility,
    "best_day": best_day,
    "worst_day": worst_day,
    "average_volume": average_volume,
    }