from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price
import os
from dotenv import load_dotenv

load_dotenv()

def place_stop_limit(symbol, side, quantity, price, stop_price):
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    client = BinanceClient(api_key, api_secret)
    manager = OrderManager(client)
    return manager.place_stop_limit_order(
        validate_symbol(symbol), 
        validate_side(side), 
        validate_quantity(quantity), 
        validate_price(price), 
        validate_price(stop_price)
    )

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 6:
        print("Usage: python src/advanced/stop_limit.py <symbol> <side> <quantity> <price> <stop_price>")
    else:
        print(place_stop_limit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
