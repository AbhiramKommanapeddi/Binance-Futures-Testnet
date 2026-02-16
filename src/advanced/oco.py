from bot.logging_config import logger

class OCOStrategy:
    def __init__(self, order_manager):
        self.order_manager = order_manager

    def place_oco(self, symbol, side, quantity, price, stop_price, limit_price):
        """
        Simulate OCO in Futures by placing a Limit order and a Stop-Limit order.
        Note: True OCO is more native in Spot, but in Futures we manage two linked orders.
        """
        logger.info(f"Placing OCO: {side} {quantity} {symbol} (Limit: {price}, Stop: {stop_price}, Stop-Limit: {limit_price})")
        
        # 1. Place the Limit Order (Take Profit)
        try:
            limit_res = self.order_manager.place_limit_order(symbol, side, quantity, price)
            logger.info(f"OCO Part 1 (Limit) Placed: {limit_res.get('orderId')}")
        except Exception as e:
            logger.error(f"OCO Part 1 failed: {e}")
            raise

        # 2. Place the Stop-Limit Order (Stop Loss)
        try:
            stop_res = self.order_manager.place_stop_limit_order(symbol, side, quantity, limit_price, stop_price)
            logger.info(f"OCO Part 2 (Stop-Limit) Placed: {stop_res.get('orderId')}")
        except Exception as e:
            logger.error(f"OCO Part 2 failed: {e}. Note: Part 1 was successful, manual cleanup may be needed.")
            raise

        return {"limit_order": limit_res, "stop_limit_order": stop_res}
