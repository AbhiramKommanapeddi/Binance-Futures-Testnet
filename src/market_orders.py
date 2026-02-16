from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_quantity
import os
from dotenv import load_dotenv

load_dotenv()

def place_market(symbol, side, quantity):
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    client = BinanceClient(api_key, api_secret)
    manager = OrderManager(client)
    return manager.place_market_order(validate_symbol(symbol), validate_side(side), validate_quantity(quantity))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python src/market_orders.py <symbol> <side> <quantity>")
    else:
        print(place_market(sys.argv[1], sys.argv[2], sys.argv[3]))
