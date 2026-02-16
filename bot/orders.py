from .client import BinanceClient
from .logging_config import logger

class OrderManager:
    def __init__(self, client: BinanceClient):
        self.client = client

    def place_market_order(self, symbol, side, quantity):
        logger.info(f"Placing Market Order: {side} {quantity} {symbol}")
        return self.client.place_order(symbol, side, 'MARKET', quantity)

    def place_limit_order(self, symbol, side, quantity, price):
        logger.info(f"Placing Limit Order: {side} {quantity} {symbol} at {price}")
        return self.client.place_order(symbol, side, 'LIMIT', quantity, price=price)

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        logger.info(f"Placing Stop-Limit Order: {side} {quantity} {symbol} trigger: {stop_price} price: {price}")
        return self.client.place_order(symbol, side, 'STOP_LIMIT', quantity, price=price, stop_price=stop_price)
