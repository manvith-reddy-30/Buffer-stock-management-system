import pytest
from inference.medak import predict_next_7_days

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# Valid sample of 30 prices (oldest → newest)
VALID_PRICES = [
    900.0,
    2750.0,
    1750.0,
    1200.0,
    1250.0,
    1100.0,
    1100.0,
    1100.0,
    1100.0,
    1500.0,
    1100.0,
    900.0,
    1100.0,
    1400.0,
    1400.0,
    1100.0,
    1500.0,
    1500.0,
    1400.0,
    1400.0,
    1800.0,
    1400.0,
    1800.0,
    1250.0,
    1250.0,
    1800.0,
    1500.0,
    1800.0,
    1500.0,
    1500.0,
]


def test_valid_prediction_output():
    """
    Test that prediction returns a list of 7 float values.
    """
    result = predict_next_7_days(VALID_PRICES)
    print(result)
    assert isinstance(result, list)
    assert len(result) == 7
    assert all(isinstance(x, float) for x in result)


def test_invalid_input_length():
    """
    Test that function raises ValueError for invalid input size.
    """
    short_prices = VALID_PRICES[:25]  # less than 30
    with pytest.raises(ValueError, match="Exactly 30 prices are required as input."):
        predict_next_7_days(short_prices)


def test_extreme_prices():
    """
    Test the model with extremely high prices to check stability.
    """
    extreme_prices = [10000.0] * 30
    result = predict_next_7_days(extreme_prices)

    assert len(result) == 7
    assert all(isinstance(x, float) for x in result)


test_invalid_input_length()
