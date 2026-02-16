import re

def validate_symbol(symbol):
    if not re.match(r'^[A-Z0-9]{5,15}$', symbol):
        raise ValueError(f"Invalid symbol: {symbol}")
    return symbol.upper()

def validate_side(side):
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
    return side.upper()

def validate_quantity(quantity):
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        return qty
    except ValueError:
        raise ValueError(f"Invalid quantity: {quantity}")

def validate_price(price):
    if price is None:
        return None
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be positive.")
        return p
    except ValueError:
        raise ValueError(f"Invalid price: {price}")
