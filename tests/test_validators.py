import pytest
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price

def test_validate_symbol():
    assert validate_symbol("BTCUSDT") == "BTCUSDT"
    assert validate_symbol("btcusdt") == "BTCUSDT"
    with pytest.raises(ValueError):
        validate_symbol("BTC") # Too short

def test_validate_side():
    assert validate_side("BUY") == "BUY"
    assert validate_side("sell") == "SELL"
    with pytest.raises(ValueError):
        validate_side("HOLD")

def test_validate_quantity():
    assert validate_quantity(1.5) == 1.5
    assert validate_quantity("0.01") == 0.01
    with pytest.raises(ValueError):
        validate_quantity(-1)

def test_validate_price():
    assert validate_price(45000) == 45000.0
    assert validate_price(None) is None
    with pytest.raises(ValueError):
        validate_price("abc")
