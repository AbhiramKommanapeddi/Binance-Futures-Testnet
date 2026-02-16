import argparse
import sys
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price
from src.advanced.twap import TWAPStrategy
from bot.logging_config import logger

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT", "TWAP", "OCO"], help="Order type")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, help="Order price (required for LIMIT, STOP_LIMIT, OCO)")
    parser.add_argument("--stop_price", type=float, help="Stop price (required for STOP_LIMIT, OCO)")
    parser.add_argument("--limit_price", type=float, help="Limit price for STOP_LIMIT part of OCO")
    parser.add_argument("--duration", type=int, help="TWAP duration in minutes")
    parser.add_argument("--chunks", type=int, default=5, help="TWAP number of chunks")

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        logger.error("API Key or Secret missing in .env file.")
        print("Error: Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file.")
        sys.exit(1)

    try:
        # Validate Inputs
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)
        stop_price = validate_price(args.stop_price)
        limit_price = validate_price(args.limit_price)

        client = BinanceClient(api_key, api_secret, base_url)
        manager = OrderManager(client)

        if args.type == 'MARKET':
            response = manager.place_market_order(symbol, side, quantity)
        elif args.type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT order")
            response = manager.place_limit_order(symbol, side, quantity, price)
        elif args.type == 'STOP_LIMIT':
            if price is None or stop_price is None:
                raise ValueError("Price and Stop Price are required for STOP_LIMIT order")
            response = manager.place_stop_limit_order(symbol, side, quantity, price, stop_price)
        elif args.type == 'TWAP':
            if not args.duration:
                raise ValueError("Duration is required for TWAP strategy")
            from src.advanced.twap import TWAPStrategy
            twap = TWAPStrategy(manager)
            twap.execute(symbol, side, quantity, args.duration, args.chunks)
            print("TWAP Strategy initiated. Check bot.log for progress.")
            return
        elif args.type == 'OCO':
            if price is None or stop_price is None or limit_price is None:
                raise ValueError("Price (TP), Stop Price (Trigger), and Limit Price (SL) are required for OCO")
            from src.advanced.oco import OCOStrategy
            oco = OCOStrategy(manager)
            response = oco.place_oco(symbol, side, quantity, price, stop_price, limit_price)
            print("\n--- OCO Orders Placed Successfully ---")
            print(f"TP Order ID: {response['limit_order'].get('orderId')}")
            print(f"SL Order ID: {response['stop_limit_order'].get('orderId')}")
            return

        print("\n--- Order Placed Successfully ---")
        print(f"Status: {response.get('status')}")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Symbol: {response.get('symbol')}")
        print(f"Price: {response.get('avgPrice') or response.get('price')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print("---------------------------------\n")

    except Exception as e:
        logger.error(f"Execution Error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
