from math import sqrt

import pandas as pd
import pytest

from src.analysis import calculate_metrics, calculate_moving_average


def test_calculate_metrics():
    data = pd.DataFrame({
        "Close": [100, 110, 99],
        "Volume": [1000, 2000, 3000],
    })

    metrics = calculate_metrics(data)

    expected_volatility = sqrt(0.02) * sqrt(252)

    assert metrics['latest_close'] == 99 
    assert metrics['average_close'] == pytest.approx(103)
    assert metrics['average_volume'] == 2000
    assert metrics['total_return'] == pytest.approx(-0.01)
    assert metrics["best_day"] == pytest.approx(0.10)
    assert metrics["worst_day"] == pytest.approx(-0.10)
    assert metrics["annualised_volatility"] == pytest.approx(expected_volatility)


def test_calculate_moving_average():

    data: pd.DataFrame,
    window: int
    -> pd.Series:

    data = pd.DataFrame({
        "Close": [100, 110, 120, 130, 140]
    })

    result = calculate_moving_average(data, 3)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == pytest.approx(110)
    assert result.iloc[3] == pytest.approx(120)
    assert result.iloc[4] == pytest.approx(130)


def test_calculate_moving_average_zero_window():
    data = pd.DataFrame({
        "Close": [100, 110, 120, 130, 140]
    })
    with pytest.raises(ValueError):
        calculate_moving_average(data, 0)


def test_calculate_moving_average_negative_window():
    data = pd.DataFrame({
    "Close": [100, 110, 120, 130, 140]
})

    with pytest.raises(ValueError):
        calculate_moving_average(data,-1)
